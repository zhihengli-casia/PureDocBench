#!/usr/bin/env python3
"""PureDocBench inference: PaddleOCR-VL-1.5 via official pipeline.

Uses paddleocr.PaddleOCRVL pipeline (page-level layout detection + element-level
recognition), backed by a local vLLM serve instance. This is the official
recommended way per PaddleOCR-VL-1.5 README; raw integer-page calls to vLLM
trigger repetition / hallucination on tables and ledger-style content.

Pre-requisite:
  - vLLM serve running on port 8015 with --served-model-name PaddleOCR-VL-1.5-0.9B
  - paddle_vl env (has paddleocr 3.5+, paddlepaddle-gpu 3.2+)
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

# ---- model identification ---------------------------------------------------
MODEL_SLUG = "paddleocr_vl_1_5"
MODEL_NAME = "PaddleOCR-VL-1.5"
SERVE_PORT = 8015
SERVE_URL = f"http://127.0.0.1:{SERVE_PORT}/v1"

# ---- repo paths -------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
PRED_DIR_FULL = REPO_ROOT / os.environ.get("PDBV2_PRED_ROOT", "predictions") / MODEL_SLUG
PRED_DIR_SMOKE = REPO_ROOT / os.environ.get("PDBV2_SMOKE_ROOT", "outputs_smoke") / MODEL_SLUG

IMAGES_ROOT = Path(os.environ.get("PDBV2_IMAGES_ROOT", "images/clean"))
PDBV2_JSON = Path(os.environ.get("PDBV2_JSON", "manifest.json"))


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--concurrency", type=int, default=32)
    args = ap.parse_args()

    out_dir = PRED_DIR_SMOKE if args.smoke else PRED_DIR_FULL
    out_dir.mkdir(parents=True, exist_ok=True)

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

    print(f"[{MODEL_SLUG}] importing PaddleOCRVL pipeline...", flush=True)
    from paddleocr import PaddleOCRVL

    print(f"[{MODEL_SLUG}] creating pipeline (vllm-server={SERVE_URL}, concurrency={args.concurrency})...", flush=True)
    pipeline = PaddleOCRVL(
        vl_rec_backend="vllm-server",
        vl_rec_server_url=SERVE_URL,
        vl_rec_max_concurrency=args.concurrency,
    )
    print(f"[{MODEL_SLUG}] pipeline ready", flush=True)

    image_paths = [str(p) for _, p in images]

    t0 = time.time()
    ok = err = 0
    total = len(image_paths)
    CHUNK = 32
    print(f"[{MODEL_SLUG}] predict on {total} images, chunk={CHUNK}...", flush=True)

    for chunk_start in range(0, total, CHUNK):
        chunk = image_paths[chunk_start:chunk_start + CHUNK]
        try:
            for res in pipeline.predict(chunk):
                try:
                    res.save_to_markdown(save_path=str(out_dir))
                    ok += 1
                except Exception as e:
                    err += 1
                    print(f"[{MODEL_SLUG}] save_md ERR ({type(e).__name__}): {str(e)[:240]}", flush=True)
        except Exception as e:
            err += len(chunk)
            print(f"[{MODEL_SLUG}] CHUNK ERR ({type(e).__name__}): {str(e)[:300]}", flush=True)
        done = ok + err
        dt = time.time() - t0
        speed = done / dt if dt > 0 else 0
        eta = (total - done) / speed if speed > 0 else 0
        print(
            f"[{MODEL_SLUG}] {done}/{total} ok={ok} err={err} {speed:.2f}/s ETA={eta:.0f}s",
            flush=True,
        )

    dt = time.time() - t0
    print(f"[{MODEL_SLUG}] DONE ok={ok} err={err} elapsed={dt:.0f}s", flush=True)


if __name__ == "__main__":
    sys.exit(main())
