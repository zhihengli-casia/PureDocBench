#!/usr/bin/env python3
"""DeepSeek-OCR inference on PureDocBench using the official HF path.

This follows the model README's document-mode recipe:
  prompt = "<image>\n<|grounding|>Convert the document to markdown. "
  model.infer(..., base_size=1024, image_size=640, crop_mode=True,
              save_results=True, test_compress=True)

The previous vLLM "Free OCR" path is faster, but it is the no-layout OCR mode
and does not match the markdown/document parsing setting used for evaluation.
"""
from __future__ import annotations

import os
import argparse
import gc
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
MODEL_SLUG = "deepseek_ocr_pdbv2"
MODEL_DIR = os.environ.get("PDB_MODEL_DIR", str(Path(os.environ.get("PDB_MODEL_ROOT", "models")) / "DeepSeek-OCR"))
DATASET_DIR = Path(os.environ.get("PDB_DATASET_DIR", "images/clean"))
PROMPT_FILE = BASE / "prompts" / f"{MODEL_SLUG}.txt"
TMP_ROOT = Path(os.environ.get("PDB_TMPDIR", "/tmp/pdbv2_tmp"))

BASE_SIZE = 1024
IMAGE_SIZE = 640
CROP_MODE = True
SAVE_RESULTS = True
TEST_COMPRESS = True

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def list_images() -> list[Path]:
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
    # Official DeepSeek-OCR can emit grounding/layout markers. Preserve text,
    # but remove bounding boxes and marker tokens before writing predictions.
    s = re.sub(r"<\|det\|>.*?<\|/det\|>", "", s, flags=re.DOTALL)
    s = re.sub(r"<\|ref\|>(.*?)<\|/ref\|>", r"\1", s, flags=re.DOTALL)
    s = re.sub(r"<\|/?(?:ref|det)\|>", "", s)
    return s.replace("<|endoftext|>", "").strip()


def load_model():
    import torch
    from transformers import AutoModel, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, trust_remote_code=True)
    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

    kwargs = dict(
        trust_remote_code=True,
        use_safetensors=True,
        torch_dtype=dtype,
    )
    try:
        model = AutoModel.from_pretrained(
            MODEL_DIR,
            _attn_implementation="flash_attention_2",
            **kwargs,
        )
        print(f"[{MODEL_SLUG}] loaded with flash_attention_2", flush=True)
    except Exception as exc:
        print(
            f"[{MODEL_SLUG}] flash_attention_2 unavailable, using default attention: "
            f"{type(exc).__name__}: {str(exc)[:160]}",
            flush=True,
        )
        model = AutoModel.from_pretrained(MODEL_DIR, **kwargs)

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = model.eval().to(device)
    if torch.cuda.is_available():
        model = model.to(torch.bfloat16)
    return tokenizer, model, torch


def main() -> int:
    global DATASET_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--shard", type=int, default=0, help="0-indexed shard id")
    ap.add_argument("--num-shards", type=int, default=1, help="total shards across GPUs")
    ap.add_argument("--dataset-dir", default=str(DATASET_DIR))
    ap.add_argument("--predictions-root", default=str(BASE / "predictions"))
    ap.add_argument("--smoke-root", default=str(BASE / "outputs_smoke"))
    args = ap.parse_args()
    DATASET_DIR = Path(args.dataset_dir)

    out_dir = Path(args.smoke_root if args.smoke else args.predictions_root) / MODEL_SLUG
    if args.smoke and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    prompt_text = PROMPT_FILE.read_text(encoding="utf-8").strip()
    all_imgs = list_images()
    if not all_imgs:
        print(f"FATAL no images under {DATASET_DIR}", flush=True)
        return 2
    if args.num_shards > 1:
        all_imgs = [p for i, p in enumerate(all_imgs) if i % args.num_shards == args.shard]
        print(f"[{MODEL_SLUG}] shard {args.shard}/{args.num_shards}: {len(all_imgs)} images", flush=True)

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
    tokenizer, model, torch = load_model()

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
                save_results=SAVE_RESULTS,
                test_compress=TEST_COMPRESS,
            )
            text = ""
            if infer_ret is not None:
                text = str(infer_ret).strip()
                if text.lower() == "none":
                    text = ""
            mmd = Path(scratch) / "result.mmd"
            if mmd.exists():
                mmd_text = mmd.read_text(encoding="utf-8").strip()
                if mmd_text:
                    text = mmd_text
            text = strip_output(text)
            if text:
                (out_dir / (p.stem + ".md")).write_text(text, encoding="utf-8")
                ok += 1
            else:
                err += 1
                print(f"EMPTY {p.name}", flush=True)
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
