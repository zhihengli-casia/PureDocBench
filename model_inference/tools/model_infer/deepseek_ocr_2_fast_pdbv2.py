#!/usr/bin/env python3
"""DeepSeek-OCR-2 inference on PureDocBench.

Standalone (no shared helpers per feedback_pdbv2_per_model_script).
Uses HF AutoModel + model.infer() — designed for transformers 4.x.

Run with omni_hf_flash env (transformers 4.57.6, torch 2.9.1+cu128 + torchvision).
cuDNN INIT fails on this env, so cuDNN is disabled (slower native conv).
"""
from __future__ import annotations

import os
import argparse
import gc
import shutil
import sys
import tempfile
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
MODEL_SLUG = "deepseek_ocr_2_fast_pdbv2"
MODEL_DIR = os.environ.get("PDB_MODEL_DIR", str(Path(os.environ.get("PDB_MODEL_ROOT", "models")) / "DeepSeek-OCR-2"))
DATASET_DIR = Path(os.environ.get("PDB_DATASET_DIR", "images/clean"))
PROMPT_FILE = BASE / "prompts" / f"{MODEL_SLUG}.txt"
TMP_ROOT = Path(os.environ.get("PDB_TMPDIR", "/tmp/pdbv2_tmp"))

BASE_SIZE = 640
IMAGE_SIZE = 512
CROP_MODE = True

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def list_images():
    return sorted(
        p for p in DATASET_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    )


def strip_output(text: str) -> str:
    s = text.strip()
    if s.startswith("```"):
        lines = s.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        s = "\n".join(lines).strip()
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--n", type=int, default=5)
    args = ap.parse_args()

    out_dir = BASE / ("outputs_smoke" if args.smoke else "predictions") / MODEL_SLUG
    if args.smoke and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    prompt_text = PROMPT_FILE.read_text(encoding="utf-8").strip()
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

    TMP_ROOT.mkdir(parents=True, exist_ok=True)

    import torch
    from transformers import AutoModel, AutoTokenizer

    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, trust_remote_code=True, use_fast=False)
    model = AutoModel.from_pretrained(MODEL_DIR, trust_remote_code=True, torch_dtype=dtype)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = model.to(device).eval()

    t0 = time.time()
    ok = err = 0
    for i, p in enumerate(todo):
        scratch = tempfile.mkdtemp(prefix=f"{MODEL_SLUG}_", dir=str(TMP_ROOT))
        try:
            infer_ret = model.infer(
                tokenizer,
                prompt=prompt_text,
                image_file=str(p),
                output_path=scratch,
                base_size=BASE_SIZE,
                image_size=IMAGE_SIZE,
                crop_mode=CROP_MODE,
                save_results=True,
            )
            text = ""
            if infer_ret is not None:
                text = str(infer_ret).strip()
                if text.lower() == "none":
                    text = ""
            mmd = Path(scratch) / "result.mmd"
            if not text and mmd.exists():
                text = mmd.read_text(encoding="utf-8").strip()
            text = strip_output(text)
            if text:
                (out_dir / (p.stem + ".md")).write_text(text, encoding="utf-8")
                ok += 1
            else:
                err += 1
        except Exception as exc:
            print(f"IMG_ERR {p.name}: {str(exc)[:200]}", flush=True)
            err += 1
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
        processed = i + 1
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
        f"({len(todo)/max(dt,1e-6):.2f}img/s)",
        flush=True,
    )
    del model
    gc.collect()
    torch.cuda.empty_cache()
    return 0 if err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
