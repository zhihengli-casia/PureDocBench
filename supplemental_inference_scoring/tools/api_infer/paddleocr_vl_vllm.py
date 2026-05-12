#!/usr/bin/env python3
"""PureDocBench vLLM client for PaddleOCR-VL (1.0).

Talks to local vLLM OpenAI-compatible server (started elsewhere).
Per official README: max_pixels = 1280 * 28 * 28 (~1M); larger images are
resized client-side before send to avoid vision-token bloat that triggers
repetition / hallucination.
"""
import argparse
import asyncio
import base64
import io
import json
import os
import sys
import time
from pathlib import Path

# ---- model identification (PaddleOCR-VL 1.0) -------------------------------
MODEL_SLUG = "paddleocr_vl"
MODEL_NAME = "PaddleOCR-VL"
SERVE_PORT = 8011
SERVED_MODEL_NAME = "paddleocr_vl"

# ---- repo paths ------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPT_FILE = REPO_ROOT / "prompts" / f"{MODEL_SLUG}.txt"
PRED_DIR_FULL = REPO_ROOT / os.environ.get("PDBV2_PRED_ROOT", "predictions") / MODEL_SLUG
PRED_DIR_SMOKE = REPO_ROOT / os.environ.get("PDBV2_SMOKE_ROOT", "outputs_smoke") / MODEL_SLUG

IMAGES_ROOT = Path(os.environ.get("PDBV2_IMAGES_ROOT", "images/clean"))
PDBV2_JSON = Path(os.environ.get("PDBV2_JSON", "manifest.json"))

# ---- inference params (per official README) --------------------------------
TEMPERATURE = 0.0
MAX_OUTPUT_TOKENS = 8192
MAX_PIXELS = 1280 * 28 * 28
DEFAULT_CONCURRENCY = 32
REQUEST_TIMEOUT = 600.0
RETRY_MAX = 3
RETRY_BACKOFF = 3.0


def build_image_index() -> list[tuple[str, Path]]:
    data = json.loads(PDBV2_JSON.read_text(encoding="utf-8"))
    basenames = [e["page_info"]["image_path"] for e in data]
    print(f"[{MODEL_SLUG}] FULL: {len(basenames)} pages", flush=True)
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
        print(f"[{MODEL_SLUG}] WARN: {len(missing)} missing, first 3: {missing[:3]}", flush=True)
    return pairs


def img_to_data_url(p: Path) -> str:
    from PIL import Image as _PIL
    img = _PIL.open(p).convert("RGB")
    w, h = img.size
    if w * h > MAX_PIXELS:
        ratio = (MAX_PIXELS / (w * h)) ** 0.5
        nw, nh = max(28, int(w * ratio)), max(28, int(h * ratio))
        img = img.resize((nw, nh), _PIL.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=False)
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"


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
        loop = asyncio.get_running_loop()
        data_url = await loop.run_in_executor(None, img_to_data_url, p)
        payload = {
            "model": SERVED_MODEL_NAME,
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
            "repetition_penalty": 1.03,
        }

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

    if not PROMPT_FILE.exists():
        raise FileNotFoundError(f"prompt missing: {PROMPT_FILE}")
    prompt_text = PROMPT_FILE.read_text(encoding="utf-8").strip()
    print(f"[{MODEL_SLUG}] prompt loaded: {len(prompt_text)} chars", flush=True)

    images = build_image_index()
    if args.smoke:
        images = images[: args.n]
        print(f"[{MODEL_SLUG}] SMOKE: {len(images)} pages -> {out_dir}", flush=True)
    else:
        done_stems = {p.stem for p in out_dir.glob("*.md")}
        before = len(images)
        images = [(bn, p) for bn, p in images if Path(bn).stem not in done_stems]
        print(f"[{MODEL_SLUG}] FULL: {len(images)} pending (resumed; {before - len(images)} already done) -> {out_dir}", flush=True)
        if not images:
            print(f"[{MODEL_SLUG}] nothing to do", flush=True)
            return

    base_url = f"http://127.0.0.1:{SERVE_PORT}/v1"
    print(f"[{MODEL_SLUG}] base_url={base_url} concurrency={args.concurrency} max_pixels={MAX_PIXELS}", flush=True)

    import httpx

    headers = {"Authorization": "Bearer EMPTY", "Content-Type": "application/json"}
    limits = httpx.Limits(max_connections=args.concurrency * 2, max_keepalive_connections=args.concurrency)

    async with httpx.AsyncClient(headers=headers, limits=limits, http2=False) as client:
        sem = asyncio.Semaphore(args.concurrency)
        stats = {"ok": 0, "err": 0, "empty": 0, "skip": 0}
        t0 = time.time()
        total = len(images)

        async def progress_loop():
            while True:
                await asyncio.sleep(30)
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
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    args = ap.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
