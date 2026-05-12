#!/usr/bin/env python3
"""PureDocBench inference: PaddleOCR-VL-1.5 (transformers offline).

Standalone script per official HF README.
"""
import argparse
import gc
import json
import os
import sys
import time
import traceback
from pathlib import Path

MODEL_SLUG = 'paddleocr_vl'
MODEL_NAME = 'PaddleOCR-VL'
MODEL_DIR = '${PDB_MODEL_ROOT}/PaddleOCR-VL'

REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPT_FILE = REPO_ROOT / 'prompts' / f'{MODEL_SLUG}.txt'
PRED_DIR_FULL = REPO_ROOT / os.environ.get('PDBV2_PRED_ROOT', 'predictions') / MODEL_SLUG
PRED_DIR_SMOKE = REPO_ROOT / os.environ.get('PDBV2_SMOKE_ROOT', 'outputs_smoke') / MODEL_SLUG

IMAGES_ROOT = Path(os.environ.get('PDBV2_IMAGES_ROOT', '${PDB_DATASET_ROOT}/images/clean'))
PDBV2_JSON = Path(os.environ.get('PDBV2_JSON', '${PDB_MANIFEST_JSON}'))

MAX_NEW_TOKENS = 8192
MAX_PIXELS = 1280 * 28 * 28  # per official README


def build_image_index():
    data = json.loads(PDBV2_JSON.read_text(encoding='utf-8'))
    basenames = [e['page_info']['image_path'] for e in data]
    fs_index = {}
    for p in IMAGES_ROOT.rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.png', '.jpg', '.jpeg'}:
            fs_index[p.name] = p
    pairs = []
    missing = []
    for bn in basenames:
        if bn in fs_index:
            pairs.append((bn, fs_index[bn]))
        else:
            missing.append(bn)
    if missing:
        print(f'[{MODEL_SLUG}] WARN: {len(missing)} missing, first 3: {missing[:3]}', flush=True)
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--n', type=int, default=5)
    ap.add_argument('--shard', default='0/1', help='k/n shard')
    args = ap.parse_args()

    out_dir = PRED_DIR_SMOKE if args.smoke else PRED_DIR_FULL
    out_dir.mkdir(parents=True, exist_ok=True)
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(f'Prompt missing: {PROMPT_FILE}')
    prompt = PROMPT_FILE.read_text(encoding='utf-8').strip()
    print(f'[{MODEL_SLUG}] prompt: {prompt!r}', flush=True)

    images = build_image_index()
    print(f'[{MODEL_SLUG}] image index: {len(images)} entries', flush=True)
    if args.smoke:
        images = images[: args.n]
        print(f'[{MODEL_SLUG}] SMOKE: {len(images)} pages -> {out_dir}', flush=True)
    else:
        done = {p.stem for p in out_dir.glob('*.md')}
        images = [(bn, p) for bn, p in images if Path(bn).stem not in done]
        try:
            k_str, n_str = args.shard.split("/")
            k, n = int(k_str), int(n_str)
        except Exception:
            raise SystemExit(f"bad --shard {args.shard!r}, expected k/n")
        if n > 1:
            images = [pair for i, pair in enumerate(images) if i % n == k]
            print(f"[{MODEL_SLUG}] shard {k}/{n}: {len(images)} pending", flush=True)
        print(f'[{MODEL_SLUG}] FULL: {len(images)} pending -> {out_dir}', flush=True)
        if not images:
            print(f'[{MODEL_SLUG}] nothing to do, all .md present', flush=True)
            return

    print(f'[{MODEL_SLUG}] loading model from {MODEL_DIR}...', flush=True)
    import torch
    from PIL import Image
    from transformers import AutoProcessor, AutoModelForCausalLM

    DEVICE = 'cuda'
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR, torch_dtype=torch.bfloat16, trust_remote_code=True
    ).to(DEVICE).eval()
    processor = AutoProcessor.from_pretrained(MODEL_DIR, trust_remote_code=True)
    print(f'[{MODEL_SLUG}] model loaded', flush=True)

    t0 = time.time()
    ok = err = 0
    total = len(images)
    for i, (bn, img_path) in enumerate(images, 1):
        stem = Path(bn).stem
        try:
            image = Image.open(img_path).convert('RGB')
            messages = [
                {
                    'role': 'user',
                    'content': [
                        {'type': 'image', 'image': image},
                        {'type': 'text', 'text': prompt},
                    ],
                }
            ]
            inputs = processor.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors='pt',
                images_kwargs={
                    'size': {
                        'shortest_edge': processor.image_processor.min_pixels,
                        'longest_edge': MAX_PIXELS,
                    }
                },
            ).to(model.device)

            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS, use_cache=True, do_sample=False)
            result = processor.decode(outputs[0][inputs['input_ids'].shape[-1]:-1])
            (out_dir / f'{stem}.md').write_text(result or '', encoding='utf-8')
            ok += 1
        except Exception as e:
            err += 1
            print(f'[{MODEL_SLUG}] ERR {bn}: {str(e)[:200]}', flush=True)
            traceback.print_exc()
        if i % 5 == 0 or i == total:
            dt = time.time() - t0
            speed = i / dt if dt > 0 else 0
            eta = (total - i) / speed if speed > 0 else 0
            print(
                f'[{MODEL_SLUG}] {i}/{total} ok={ok} err={err} {speed:.2f}img/s ETA={eta:.0f}s',
                flush=True,
            )

    dt = time.time() - t0
    print(f'[{MODEL_SLUG}] DONE ok={ok} err={err} elapsed={dt:.0f}s', flush=True)
    del model
    gc.collect()
    torch.cuda.empty_cache()


if __name__ == '__main__':
    sys.exit(main())
