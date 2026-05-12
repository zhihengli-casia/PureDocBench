#!/usr/bin/env python3
"""MiniCPM-V 4.5 inference on PureDocBench.

vLLM 0.19.x. Monkey-patches AutoTokenizer.from_pretrained to inject
*_id attrs (im_start_id etc) that processing_minicpmv.py expects but
TokenizersBackend doesn't expose by default.
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

BASE = Path(__file__).resolve().parents[2]
MODEL_SLUG = "minicpm_v_45_pdbv2"
MODEL_DIR = os.environ.get("PDB_MODEL_DIR", str(Path(os.environ.get("PDB_MODEL_ROOT", "models")) / "MiniCPM-V-4_5"))
DATASET_DIR = Path(os.environ.get("PDB_DATASET_DIR", "images/clean"))
PROMPT_FILE = BASE / "prompts" / f"{MODEL_SLUG}.txt"

MM_LEN = 24576
GPU_MEM_UTIL = 0.88
MAX_NUM_SEQS = 2
MAX_NUM_BATCHED_TOKENS = 24576
BATCH = 8
MAX_TOKENS = 8192

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def _patch_autotokenizer():
    """Inject missing *_id attrs onto MiniCPM-V tokenizer instances."""
    import transformers

    _orig = transformers.AutoTokenizer.from_pretrained

    def _patched(*args, **kwargs):
        tok = _orig(*args, **kwargs)
        injections = [
            ("im_start_id", "<image>"),
            ("im_end_id", "</image>"),
            ("slice_start_id", "<slice>"),
            ("slice_end_id", "</slice>"),
            ("im_id_start", "<image_id>"),
            ("im_id_end", "</image_id>"),
        ]
        for attr, token_str in injections:
            if not hasattr(tok, attr):
                try:
                    tid = tok.convert_tokens_to_ids(token_str)
                    if tid is not None and tid != tok.unk_token_id:
                        setattr(tok, attr, tid)
                except Exception:
                    pass
        if not hasattr(tok, "bos_id") and getattr(tok, "bos_token_id", None) is not None:
            setattr(tok, "bos_id", tok.bos_token_id)
        if not hasattr(tok, "eos_id") and getattr(tok, "eos_token_id", None) is not None:
            setattr(tok, "eos_id", tok.eos_token_id)
        return tok

    transformers.AutoTokenizer.from_pretrained = _patched


def list_images():
    return sorted(
        p for p in DATASET_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    )


def strip_output(text: str) -> str:
    s = text.strip()
    # MiniCPM-V 4.5 reasoning prefix: drop everything before </think>
    if "</think>" in s:
        s = s.rsplit("</think>", 1)[-1].strip()
    # Drop unclosed opening <think> line
    if s.startswith("<think>"):
        s = s.split("\n", 1)[1].strip() if "\n" in s else ""
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

    _patch_autotokenizer()

    from vllm import LLM, SamplingParams
    from transformers import AutoTokenizer
    import torch

    tok = AutoTokenizer.from_pretrained(MODEL_DIR, trust_remote_code=True)
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

    def build_input(img_path: Path):
        img = Image.open(img_path).convert("RGB")
        msgs = [{"role": "user", "content": "(<image>./</image>)\n" + prompt}]
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        return {"prompt": text, "multi_modal_data": {"image": img}}

    t0 = time.time()
    ok = err = processed = 0
    for i in range(0, len(todo), BATCH):
        chunk = todo[i : i + BATCH]
        try:
            inputs = [build_input(p) for p in chunk]
            outs = llm.generate(inputs, sampling_params=sp, use_tqdm=False)
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
