#!/usr/bin/env python3
"""PureDocBench API inference: Kimi-K2.6 (via SiliconFlow).

Standalone async client. Reads SILICONFLOW_API_KEY from <repo>/.env.
No GPU usage; pure I/O.

Usage:
  python qwen3_5_27b.py                 # full 1474 pages
  python qwen3_5_27b.py --smoke         # first 5 pages -> outputs_smoke/api/
  python qwen3_5_27b.py --concurrency 16
"""
import argparse
import asyncio
import base64
import json
import os
import sys
import time
from pathlib import Path

# ---- model identification (edit these per model) ----------------------------
MODEL_SLUG = "kimi_k2_6"
MODEL_API_ID = "Pro/moonshotai/Kimi-K2.6"
ENABLE_THINKING = False

# ---- repo paths -------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPT_FILE = REPO_ROOT / "prompts" / f"{MODEL_SLUG}.txt"
PRED_DIR_FULL = REPO_ROOT / os.environ.get("PDBV2_PRED_ROOT", "predictions") / "api" / MODEL_SLUG
PRED_DIR_SMOKE = REPO_ROOT / os.environ.get("PDBV2_SMOKE_ROOT", "outputs_smoke") / "api" / MODEL_SLUG
ENV_FILE = REPO_ROOT / ".env"
SUBSET_FILE = REPO_ROOT / "configs" / "api_subset_600.json"

IMAGES_ROOT = Path(os.environ.get("PDBV2_IMAGES_ROOT", "images/clean"))
PDBV2_JSON = Path(os.environ.get("PDBV2_JSON", "manifest.json"))

# ---- API params -------------------------------------------------------------
DEFAULT_API_BASE_URL = "https://api.siliconflow.cn/v1"
TEMPERATURE = 0.0
MAX_OUTPUT_TOKENS = 8192
DEFAULT_CONCURRENCY = 8

REQUEST_TIMEOUT = float(os.environ.get("PDB_API_REQUEST_TIMEOUT", "180"))  # seconds (per-request)
RETRY_MAX = int(os.environ.get("PDB_API_RETRY_MAX", "4"))
RETRY_BACKOFF = float(os.environ.get("PDB_API_RETRY_BACKOFF", "5"))  # base seconds, exponential


def load_env() -> tuple[str, str]:
    api_key = os.environ.get("SILICONFLOW_API_KEY")
    base_url = os.environ.get("SILICONFLOW_BASE_URL")
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            v = v.strip().strip('"').strip("'")
            if k.strip() == "SILICONFLOW_API_KEY" and not api_key:
                api_key = v
            elif k.strip() == "SILICONFLOW_BASE_URL" and not base_url:
                base_url = v
    if not api_key:
        raise RuntimeError("SILICONFLOW_API_KEY not found (env or .env)")
    return api_key, base_url or DEFAULT_API_BASE_URL


def build_image_index() -> list[tuple[str, Path]]:
    data = json.loads(PDBV2_JSON.read_text(encoding="utf-8"))
    manifest_basenames = [e["page_info"]["image_path"] for e in data]
    if not SUBSET_FILE.exists():
        raise FileNotFoundError(f"Required subset file missing: {SUBSET_FILE}")
    subset = set(json.loads(SUBSET_FILE.read_text(encoding="utf-8"))["basenames"])
    basenames = manifest_basenames  # FULL 1474, subset disabled
    print(f"[{MODEL_SLUG}] FULL: {len(basenames)} pages (subset disabled)", flush=True)
    fs_index: dict[str, Path] = {}
    for p in IMAGES_ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            fs_index[p.name] = p
    pairs: list[tuple[str, Path]] = []
    missing: list[str] = []
    for bn in basenames:
        if bn in fs_index:
            pairs.append((bn, fs_index[bn]))
        else:
            missing.append(bn)
    if missing:
        print(f"[{MODEL_SLUG}] WARN: {len(missing)} images missing on disk, first 3: {missing[:3]}", flush=True)
    return pairs


def img_to_data_url(p: Path) -> str:
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}[p.suffix.lower()]
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def strip_noise(text: str) -> str:
    s = text.strip()
    if s.startswith("```"):
        lines = s.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        s = "\n".join(lines).strip()
    for prefix in ("assistant\n", "assistant:", "Assistant\n", "Assistant:"):
        if s.lstrip().startswith(prefix):
            s = s.lstrip()[len(prefix):].lstrip()
            break
    return s.strip()


async def call_one(client, base_url, prompt_text, bn, p, out_dir, sem, stats):
    async with sem:
        out_path = out_dir / (Path(bn).stem + ".md")
        if out_path.exists():
            stats["skip"] += 1
            return
        data_url = img_to_data_url(p)
        payload = {
            "model": MODEL_API_ID,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": data_url}},
                        {"type": "text", "text": prompt_text},
                    ],
                }
            ],
            "temperature": TEMPERATURE,
            "max_tokens": MAX_OUTPUT_TOKENS,
        }
        if not ENABLE_THINKING:
            payload["enable_thinking"] = False

        last_err = "(no attempt)"
        for attempt in range(RETRY_MAX):
            try:
                resp = await client.post(
                    f"{base_url}/chat/completions",
                    json=payload,
                    timeout=REQUEST_TIMEOUT,
                )
                if resp.status_code == 200:
                    body = resp.json()
                    content = body.get("choices", [{}])[0].get("message", {}).get("content") or ""
                    text = strip_noise(content)
                    if text:
                        out_path.write_text(text, encoding="utf-8")
                        stats["ok"] += 1
                        return
                    else:
                        stats["empty"] += 1
                        print(f"[{MODEL_SLUG}] EMPTY: {bn} (finish={body.get('choices',[{}])[0].get('finish_reason')})", flush=True)
                        return
                elif resp.status_code in (429, 500, 502, 503, 504):
                    last_err = f"HTTP {resp.status_code}: {resp.text[:160]}"
                else:
                    # 4xx other than 429: don't retry
                    print(f"[{MODEL_SLUG}] HTTP_{resp.status_code} {bn}: {resp.text[:240]}", flush=True)
                    stats["err"] += 1
                    return
            except Exception as e:
                last_err = f"{type(e).__name__}: {str(e)[:160]}"
            if attempt < RETRY_MAX - 1:
                await asyncio.sleep(RETRY_BACKOFF * (2 ** attempt))
        stats["err"] += 1
        print(f"[{MODEL_SLUG}] FAIL {bn} after {RETRY_MAX} retries: {last_err}", flush=True)


async def main_async(args):
    out_dir = PRED_DIR_SMOKE if args.smoke else PRED_DIR_FULL
    out_dir.mkdir(parents=True, exist_ok=True)

    images = build_image_index()
    if args.smoke:
        images = images[: args.n]
        print(f"[{MODEL_SLUG}] SMOKE: {len(images)} pages -> {out_dir}", flush=True)
    else:
        # resume: filter out already-done
        done_stems = {p.stem for p in out_dir.glob("*.md")}
        before = len(images)
        images = [(bn, p) for bn, p in images if Path(bn).stem not in done_stems]
        print(f"[{MODEL_SLUG}] FULL: {len(images)} pending (resumed; {before - len(images)} already done) -> {out_dir}", flush=True)
        if not images:
            print(f"[{MODEL_SLUG}] nothing to do", flush=True)
            return

    prompt_text = PROMPT_FILE.read_text(encoding="utf-8").strip()
    print(f"[{MODEL_SLUG}] prompt loaded: {len(prompt_text)} chars", flush=True)

    api_key, base_url = load_env()
    print(f"[{MODEL_SLUG}] api base_url={base_url} concurrency={args.concurrency}", flush=True)

    import httpx

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    limits = httpx.Limits(max_connections=args.concurrency * 2, max_keepalive_connections=args.concurrency)

    async with httpx.AsyncClient(headers=headers, limits=limits, http2=False) as client:
        sem = asyncio.Semaphore(args.concurrency)
        stats = {"ok": 0, "err": 0, "empty": 0, "skip": 0}
        t0 = time.time()
        total = len(images)

        async def progress_loop():
            while True:
                await asyncio.sleep(60)
                done = stats["ok"] + stats["skip"] + stats["empty"] + stats["err"]
                dt = time.time() - t0
                speed = done / dt if dt > 0 else 0
                eta = (total - done) / speed if speed > 0 else 0
                print(
                    f"[{MODEL_SLUG}] {done}/{total} ok={stats['ok']} err={stats['err']} empty={stats['empty']} skip={stats['skip']} {speed:.2f}/s ETA={eta:.0f}s",
                    flush=True,
                )

        prog_task = asyncio.create_task(progress_loop())
        try:
            await asyncio.gather(
                *[call_one(client, base_url, prompt_text, bn, p, out_dir, sem, stats) for bn, p in images]
            )
        finally:
            prog_task.cancel()

        dt = time.time() - t0
        print(
            f"[{MODEL_SLUG}] DONE ok={stats['ok']} err={stats['err']} empty={stats['empty']} skip={stats['skip']} elapsed={dt:.0f}s",
            flush=True,
        )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true", help="run only first --n images")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    args = ap.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
