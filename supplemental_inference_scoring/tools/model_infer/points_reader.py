#!/usr/bin/env python3
"""PureDocBench inference: POINTS-Reader (tencent, transformers).

Per official README:
  - Qwen2.5-3B-Instruct + ViT NaViT 600M
  - prompt: "Please extract all the text ... 1. tables HTML  2. text Markdown"
  - generation_config: max_new_tokens=2048, repetition_penalty=1.05,
    temperature=0.7, top_p=0.8, top_k=20, do_sample=True

Usage:
  python points_reader.py            # full
  python points_reader.py --smoke
"""
import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

MODEL_SLUG = "points_reader"
MODEL_DIR = "${PDB_TMP_ROOT:-/tmp/pdbv2}/POINTS-Reader"

REPO_ROOT = Path(__file__).resolve().parents[2]
PRED_DIR_FULL = REPO_ROOT / os.environ.get("PDBV2_PRED_ROOT", "predictions") / MODEL_SLUG
PRED_DIR_SMOKE = REPO_ROOT / os.environ.get("PDBV2_SMOKE_ROOT", "outputs_smoke") / MODEL_SLUG

IMAGES_ROOT = Path(os.environ.get("PDBV2_IMAGES_ROOT", "images/clean"))
PDBV2_JSON = Path(os.environ.get("PDBV2_JSON", "manifest.json"))

PROMPT = (
    "Please extract all the text from the image with the following requirements:\n"
    "1. Return tables in HTML format.\n"
    "2. Return all other text in Markdown format."
)

MAX_PIXELS = os.environ.get("POINTS_MAX_PIXELS")
MAX_PIXELS = int(MAX_PIXELS) if MAX_PIXELS else None

GEN_CONFIG = {
    "max_new_tokens": 2048,
    "repetition_penalty": 1.05,
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 20,
    "do_sample": True,
}


def build_image_index():
    data = json.loads(PDBV2_JSON.read_text(encoding="utf-8"))
    basenames = [e["page_info"]["image_path"] for e in data]
    fs_index = {}
    for p in IMAGES_ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            fs_index[p.name] = p
    pairs = []
    missing = []
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
    ap.add_argument("--num-shards", type=int, default=1)
    ap.add_argument("--shard-index", type=int, default=0)
    args = ap.parse_args()
    if args.num_shards < 1 or not (0 <= args.shard_index < args.num_shards):
        raise ValueError(f"bad shard args: shard_index={args.shard_index}, num_shards={args.num_shards}")

    out_dir = PRED_DIR_SMOKE if args.smoke else PRED_DIR_FULL
    out_dir.mkdir(parents=True, exist_ok=True)

    images = build_image_index()
    if args.num_shards > 1:
        images = [x for idx, x in enumerate(images) if idx % args.num_shards == args.shard_index]
        print(f"[{MODEL_SLUG}] SHARD {args.shard_index}/{args.num_shards}: {len(images)} assigned", flush=True)

    if args.smoke:
        images = images[: args.n]
        print(f"[{MODEL_SLUG}] SMOKE: {len(images)} pages -> {out_dir}", flush=True)
    else:
        done = {p.stem for p in out_dir.glob("*.md")}
        before = len(images)
        images = [(bn, p) for bn, p in images if Path(bn).stem not in done]
        print(f"[{MODEL_SLUG}] FULL: {len(images)} pending (resumed; {before - len(images)} already done) -> {out_dir}", flush=True)
        if not images:
            print(f"[{MODEL_SLUG}] nothing to do", flush=True)
            return

    print(f"[{MODEL_SLUG}] loading model from {MODEL_DIR}...", flush=True)
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, Qwen2VLImageProcessor

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, trust_remote_code=True)
    image_processor = Qwen2VLImageProcessor.from_pretrained(MODEL_DIR)
    print(f"[{MODEL_SLUG}] model loaded", flush=True)

    t0 = time.time()
    ok = err = 0
    total = len(images)

    for i, (bn, img_path) in enumerate(images, 1):
        stem = Path(bn).stem
        out_path = out_dir / f"{stem}.md"
        try:
            image_item = dict(type="image", image=str(img_path))
            if MAX_PIXELS is not None:
                image_item["max_pixels"] = MAX_PIXELS
            content = [
                image_item,
                dict(type="text", text=PROMPT),
            ]
            messages = [{"role": "user", "content": content}]
            response = model.chat(messages, tokenizer, image_processor, GEN_CONFIG)
            response = (response or "").strip()
            if response:
                out_path.write_text(response, encoding="utf-8")
                ok += 1
            else:
                err += 1
                print(f"[{MODEL_SLUG}] EMPTY: {bn}", flush=True)
        except Exception as e:
            err += 1
            print(f"[{MODEL_SLUG}] ERR {bn}: {str(e)[:240]}", flush=True)
            traceback.print_exc()
        if i % 5 == 0 or i == total:
            dt = time.time() - t0
            speed = i / dt if dt > 0 else 0
            eta = (total - i) / speed if speed > 0 else 0
            print(f"[{MODEL_SLUG}] {i}/{total} ok={ok} err={err} {speed:.2f}img/s ETA={eta:.0f}s", flush=True)

    dt = time.time() - t0
    print(f"[{MODEL_SLUG}] DONE ok={ok} err={err} elapsed={dt:.0f}s", flush=True)


if __name__ == "__main__":
    sys.exit(main())
