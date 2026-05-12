#!/usr/bin/env python3
"""MiniCPM-o 4.5 inference on PureDocBench (transformers route).

Image-only path. Uses model.chat() per HF cookbook. Per-shard parallel.
Env: omni_hf_flash (torch 2.9 / transformers 4.57.6).
"""
from __future__ import annotations

import os
import argparse
import gc
import shutil
import sys
import time
from pathlib import Path

from PIL import Image
import torch
from transformers import AutoModel, AutoTokenizer

BASE = Path(__file__).resolve().parents[2]
MODEL_SLUG = "minicpm_o_45_pdbv2"
MODEL_DIR = os.environ.get("PDB_MODEL_DIR", str(Path(os.environ.get("PDB_MODEL_ROOT", "models")) / "MiniCPM-o-4_5"))
DATASET_DIR = Path(os.environ.get("PDB_DATASET_DIR", "images/clean"))
PROMPT_FILE = BASE / "prompts" / f"{MODEL_SLUG}.txt"

MAX_NEW_TOKENS = 8192

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
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--num-shards", type=int, default=1)
    args = ap.parse_args()

    out_dir = BASE / ("outputs_smoke" if args.smoke else "predictions") / MODEL_SLUG
    if args.smoke and args.shard == 0 and out_dir.exists():
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
        sharded = [p for i, p in enumerate(all_imgs) if i % args.num_shards == args.shard]
        done = {p.stem for p in out_dir.glob("*.md")}
        todo = [p for p in sharded if p.stem not in done]
        print(
            f"[{MODEL_SLUG}] shard={args.shard}/{args.num_shards} "
            f"FULL {len(todo)}/{len(sharded)} remaining -> {out_dir}",
            flush=True,
        )
        if not todo:
            print(f"[{MODEL_SLUG}] shard={args.shard} ALL DONE", flush=True)
            return 0

    model = AutoModel.from_pretrained(
        MODEL_DIR,
        trust_remote_code=True,
        attn_implementation="flash_attention_2",
        torch_dtype=torch.bfloat16,
        init_audio=False,
        init_tts=False,
    ).eval().cuda()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, trust_remote_code=True)

    t0 = time.time()
    ok = err = processed = 0
    for p in todo:
        try:
            image = Image.open(p).convert("RGB")
            msgs = [{"role": "user", "content": [image, prompt]}]
            answer = model.chat(
                msgs=msgs,
                tokenizer=tokenizer,
                use_tts_template=False,
                enable_thinking=False,
                max_new_tokens=MAX_NEW_TOKENS,
                temperature=0.0,
                do_sample=False,
            )
            text = strip_output(answer if isinstance(answer, str) else str(answer))
            if text:
                (out_dir / (p.stem + ".md")).write_text(text, encoding="utf-8")
                ok += 1
            else:
                err += 1
        except Exception as exc:
            print(f"IMG_ERR {p.name}: {str(exc)[:200]}", flush=True)
            err += 1
        processed += 1
        if processed % 5 == 0 or processed == len(todo):
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
        f"[{MODEL_SLUG}] DONE shard={args.shard} ok={ok} err={err} {dt:.0f}s "
        f"({processed/max(dt,1e-6):.2f}img/s)",
        flush=True,
    )
    del model
    gc.collect()
    torch.cuda.empty_cache()
    return 0 if err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
