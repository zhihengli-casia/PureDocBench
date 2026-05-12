#!/usr/bin/env python3
"""GLM-OCR pipeline inference on PureDocBench.

Uses official glmocr SDK in selfhosted mode:
  - PP-DocLayoutV3 (transformers) for layout analysis
  - vLLM serving GLM-OCR for OCR/recognition

Requires `vllm serve` running externally on OCR_API_PORT.
"""
from __future__ import annotations

import os
import argparse
import gc
import shutil
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
MODEL_SLUG = "glm_ocr_pdbv2"
CONFIG_PATH = os.environ.get("GLM_OCR_CONFIG", "configs/glm_ocr_selfhosted.yaml")
DATASET_DIR = Path(os.environ.get("PDB_DATASET_DIR", "images/clean"))

OCR_API_HOST = "127.0.0.1"
OCR_API_PORT = 18080
LAYOUT_DEVICE = "cuda"

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def list_images():
    return sorted(
        p for p in DATASET_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    )


def extract_markdown(d):
    mr = d.get("markdown_result")
    if isinstance(mr, str):
        return mr
    if isinstance(mr, list):
        parts = []
        for item in mr:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(item.get("markdown") or item.get("content") or "")
        return "\n\n".join(p for p in parts if p)
    return d.get("markdown") or d.get("content_md") or ""


def main():
    global DATASET_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--dataset-dir", default=str(DATASET_DIR))
    ap.add_argument("--predictions-root", default=str(BASE / "predictions"))
    ap.add_argument("--smoke-root", default=str(BASE / "outputs_smoke"))
    ap.add_argument("--ocr-port", type=int, default=OCR_API_PORT)
    ap.add_argument("--config", default=CONFIG_PATH)
    args = ap.parse_args()
    DATASET_DIR = Path(args.dataset_dir)

    out_dir = Path(args.smoke_root if args.smoke else args.predictions_root) / MODEL_SLUG
    if args.smoke and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    all_imgs = list_images()
    if not all_imgs:
        print(f"FATAL no images under {DATASET_DIR}", flush=True)
        return 2

    if args.smoke:
        todo = all_imgs[: args.n]
        print(f"[{MODEL_SLUG}] SMOKE {len(todo)} images -> {out_dir}", flush=True)
    else:
        done = {p.stem for p in out_dir.glob("*.md")}
        todo = [p for p in all_imgs if p.stem not in done]
        print(f"[{MODEL_SLUG}] FULL {len(todo)}/{len(all_imgs)} remaining -> {out_dir}", flush=True)
        if not todo:
            print(f"[{MODEL_SLUG}] ALL DONE", flush=True)
            return 0

    from glmocr import GlmOcr

    parser = GlmOcr(
        config_path=args.config,
        mode="selfhosted",
        ocr_api_host=OCR_API_HOST,
        ocr_api_port=args.ocr_port,
        layout_device=LAYOUT_DEVICE,
        log_level="WARNING",
    )

    t0 = time.time()
    ok = err = processed = 0
    for p in todo:
        try:
            res = parser.parse(str(p), save_layout_visualization=False)
            md = extract_markdown(res.to_dict())
            if md.strip():
                (out_dir / (p.stem + ".md")).write_text(md, encoding="utf-8")
                ok += 1
            else:
                err += 1
                print(f"EMPTY {p.name}", flush=True)
        except Exception as exc:
            err += 1
            print(f"ERR {p.name}: {str(exc)[:200]}", flush=True)
        processed += 1
        if processed % 10 == 0 or processed == len(todo):
            dt = time.time() - t0
            speed = processed / dt if dt > 0 else 0
            eta = (len(todo) - processed) / speed if speed > 0 else 0
            print(
                f"[{MODEL_SLUG}] {processed}/{len(todo)} ok={ok} err={err} "
                f"{speed:.2f}img/s ETA={eta:.0f}s",
                flush=True,
            )

    dt = time.time() - t0
    print(
        f"[{MODEL_SLUG}] DONE ok={ok} err={err} {dt:.0f}s "
        f"({processed/max(dt,1e-6):.2f}img/s)",
        flush=True,
    )
    del parser
    gc.collect()
    return 0 if err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
