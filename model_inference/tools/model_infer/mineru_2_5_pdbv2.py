#!/usr/bin/env python3
"""MinerU2.5 inference on PureDocBench (MinerUClient two-stage).

Standalone (no shared helpers per feedback_pdbv2_per_model_script).
Uses MinerUClient (backend=vllm-engine) batch_two_step_extract — outputs structured
blocks (layout + content) which we concat as markdown in reading order.
GPU bound externally via CUDA_VISIBLE_DEVICES.

Requires:
- mineru_vl_utils via PYTHONPATH=${MINERU_THIRD_PARTY}
- aiofiles (uv pip installed)
- vllm-engine backend (glmocr_vllm_nightly env)
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
MODEL_SLUG = "mineru_2_5_pdbv2"
MODEL_DIR = os.environ.get("PDB_MODEL_DIR", str(Path(os.environ.get("PDB_MODEL_ROOT", "models")) / "MinerU2.5"))
DATASET_DIR = Path(os.environ.get("PDB_DATASET_DIR", "images/clean"))

# MinerUClient handles vllm-engine internally; mm_len/gmu config flow through env.
GPU_MEM_UTIL = 0.85
MAX_MODEL_LEN = 16384
MAX_NUM_SEQS = 8
MAX_NUM_BATCHED_TOKENS = 32768
BATCH = 8

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def list_images():
    return sorted(
        p for p in DATASET_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    )


def blocks_to_markdown(blocks):
    """blocks: list of dicts with at least 'content' field; concat in reading order."""
    parts = []
    for b in blocks or []:
        content = b.get("content") if isinstance(b, dict) else None
        if content:
            parts.append(str(content).strip())
    return "\n\n".join(p for p in parts if p)


def main():
    global DATASET_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--dataset-dir", default=str(DATASET_DIR))
    ap.add_argument("--predictions-root", default=str(BASE / "predictions"))
    ap.add_argument("--smoke-root", default=str(BASE / "outputs_smoke"))
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

    # Inject mineru_vl_utils path
    THIRD_PARTY = Path(os.environ.get("MINERU_THIRD_PARTY", "third_party"))
    if str(THIRD_PARTY) not in sys.path:
        sys.path.insert(0, str(THIRD_PARTY))

    from mineru_vl_utils import MinerUClient
    from PIL import Image
    import torch

    client = MinerUClient(
        backend="vllm-engine",
        model_path=MODEL_DIR,
        handle_equation_block=False,
    )

    t0 = time.time()
    ok = err = processed = 0
    for i in range(0, len(todo), BATCH):
        chunk = todo[i : i + BATCH]
        pil_images = []
        valid_paths = []
        for p in chunk:
            try:
                pil_images.append(Image.open(p).convert("RGB"))
                valid_paths.append(p)
            except Exception as exc:
                print(f"IMG_OPEN_ERR {p.name}: {str(exc)[:200]}", flush=True)
                err += 1
        if not pil_images:
            processed += len(chunk)
            continue
        try:
            blocks_list = client.batch_two_step_extract(pil_images)
            for p, blocks in zip(valid_paths, blocks_list):
                try:
                    md = blocks_to_markdown(blocks)
                    if md:
                        (out_dir / (p.stem + ".md")).write_text(md, encoding="utf-8")
                        ok += 1
                    else:
                        err += 1
                except Exception as exc:
                    print(f"BLOCK_ERR {p.name}: {str(exc)[:200]}", flush=True)
                    err += 1
        except Exception as exc:
            print(f"BATCH_ERR: {str(exc)[:200]}", flush=True)
            # fallback: try per-image
            for p, im in zip(valid_paths, pil_images):
                try:
                    one = client.batch_two_step_extract([im])
                    md = blocks_to_markdown(one[0] if one else None)
                    if md:
                        (out_dir / (p.stem + ".md")).write_text(md, encoding="utf-8")
                        ok += 1
                    else:
                        err += 1
                except Exception as e2:
                    print(f"FALLBACK_ERR {p.name}: {str(e2)[:200]}", flush=True)
                    err += 1
        processed += len(chunk)
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
    del client
    gc.collect()
    torch.cuda.empty_cache()
    return 0 if err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
