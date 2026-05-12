#!/usr/bin/env python3
"""OCRVerse inference on PureDocBench.

Standalone (no shared helpers per feedback_pdbv2_per_model_script).
vLLM + Qwen3-VL chat template. GPU bound externally via CUDA_VISIBLE_DEVICES.
"""
from __future__ import annotations

import os
import argparse
import base64
import gc
import shutil
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
MODEL_SLUG = "dots_ocr_pdbv2"
MODEL_DIR = os.environ.get("PDB_MODEL_DIR", str(Path(os.environ.get("PDB_MODEL_ROOT", "models")) / "dots.ocr"))
DATASET_DIR = Path(os.environ.get("PDB_DATASET_DIR", "images/clean"))
PROMPT_FILE = BASE / "prompts" / f"{MODEL_SLUG}.txt"

MM_LEN = 24576
GPU_MEM_UTIL = 0.85
MAX_NUM_SEQS = 8
MAX_NUM_BATCHED_TOKENS = 49152
BATCH = 8
MAX_TOKENS = 8192

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def list_images():
    return sorted(
        p for p in DATASET_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    )


def img_to_data_url(path: Path) -> str:
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    ext = path.suffix.lower().lstrip(".")
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    return f"data:image/{mime};base64,{b64}"


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

    prompt = PROMPT_FILE.read_text(encoding="utf-8").strip()
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

    from vllm import LLM, SamplingParams
    import torch

    llm = LLM(
        model=MODEL_DIR,
        trust_remote_code=True,
        dtype="bfloat16",
        max_model_len=MM_LEN,
        max_num_seqs=MAX_NUM_SEQS,
        max_num_batched_tokens=MAX_NUM_BATCHED_TOKENS,
        gpu_memory_utilization=GPU_MEM_UTIL,
        tensor_parallel_size=1,
        limit_mm_per_prompt={"image": 1},
    )
    sp = SamplingParams(temperature=0.0, max_tokens=MAX_TOKENS)

    t0 = time.time()
    ok = err = processed = 0
    for i in range(0, len(todo), BATCH):
        chunk = todo[i : i + BATCH]
        convs = [
            [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": img_to_data_url(p)}},
                        {"type": "text", "text": prompt},
                    ],
                }
            ]
            for p in chunk
        ]
        try:
            outs = llm.chat(messages=convs, sampling_params=sp, use_tqdm=False)
            for p, out in zip(chunk, outs):
                text = strip_output(out.outputs[0].text)
                if text:
                    (out_dir / (p.stem + ".md")).write_text(text, encoding="utf-8")
                    ok += 1
                else:
                    err += 1
        except Exception as exc:
            print(f"BATCH_ERR: {str(exc)[:200]}", flush=True)
            err += len(chunk)
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
    del llm
    gc.collect()
    torch.cuda.empty_cache()
    return 0 if err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
