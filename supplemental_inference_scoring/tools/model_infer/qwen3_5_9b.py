#!/usr/bin/env python3
"""PureDocBench inference: Qwen3.5-9B.

Standalone script, no shared helpers. Run on a single GPU
(set CUDA_VISIBLE_DEVICES externally).

Usage:
  python qwen3_5_9b.py             # full 1474 pages
  python qwen3_5_9b.py --smoke     # first 5 pages -> outputs_smoke/
  python qwen3_5_9b.py --smoke --n 10
"""
import argparse
import os
import base64
import gc
import json
import sys
import time
from pathlib import Path

# ---- model + dataset constants (edit these per model) -----------------------
MODEL_SLUG = "qwen3_5_9b"
MODEL_DIR = os.environ.get("PDB_MODEL_DIR", str(Path(os.environ.get("PDB_MODEL_ROOT", "models")) / "Qwen3.5-9B"))
ENABLE_THINKING = False  # Qwen3-VL Instruct has no thinking mode; kwarg is a no-op but harmless

# ---- repo paths -------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPT_FILE = REPO_ROOT / "prompts" / f"{MODEL_SLUG}.txt"
PRED_DIR_FULL = REPO_ROOT / os.environ.get("PDBV2_PRED_ROOT", "predictions") / MODEL_SLUG
PRED_DIR_SMOKE = REPO_ROOT / os.environ.get("PDBV2_SMOKE_ROOT", "outputs_smoke") / MODEL_SLUG

IMAGES_ROOT = Path(os.environ.get("PDBV2_IMAGES_ROOT", "images/clean"))
PDBV2_JSON = Path(os.environ.get("PDBV2_JSON", "manifest.json"))

# ---- vLLM engine params (per 稼先 spec) -------------------------------------
MAX_MODEL_LEN = 24576
GPU_MEMORY_UTILIZATION = 0.90
MAX_NUM_SEQS = 32
MAX_NUM_BATCHED_TOKENS = 32768
BATCH_SIZE = 32

MAX_OUTPUT_TOKENS = 8192
TEMPERATURE = 0.0


def load_prompt() -> str:
    return PROMPT_FILE.read_text(encoding="utf-8").strip()


def build_image_index() -> list[tuple[str, Path]]:
    data = json.loads(PDBV2_JSON.read_text(encoding="utf-8"))
    basenames = [e["page_info"]["image_path"] for e in data]
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
        print(f"[{MODEL_SLUG}] WARN: {len(missing)} images missing on disk, first 3: {missing[:3]}", flush=True)
    return pairs


def img_to_data_url(path: Path) -> str:
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}[path.suffix.lower()]
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def strip_noise(text: str) -> str:
    s = text.strip()
    if s.startswith("```"):
        lines = s.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        s = "\n".join(lines).strip()
    for prefix in ("assistant\n", "assistant:", "Assistant\n", "Assistant:"):
        if s.lstrip().startswith(prefix):
            s = s.lstrip()[len(prefix):].lstrip()
            break
    return s.strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true", help="run only first --n images")
    ap.add_argument("--n", type=int, default=5, help="smoke sample count (default 5)")
    args = ap.parse_args()

    out_dir = PRED_DIR_SMOKE if args.smoke else PRED_DIR_FULL
    out_dir.mkdir(parents=True, exist_ok=True)

    images = build_image_index()
    print(f"[{MODEL_SLUG}] image index: {len(images)} entries", flush=True)
    if args.smoke:
        images = images[: args.n]
        print(f"[{MODEL_SLUG}] SMOKE: {len(images)} images -> {out_dir}", flush=True)
    else:
        done_stems = {p.stem for p in out_dir.glob("*.md")}
        images = [(bn, p) for bn, p in images if Path(bn).stem not in done_stems]
        print(f"[{MODEL_SLUG}] FULL: {len(images)} pending -> {out_dir}", flush=True)
        if not images:
            print(f"[{MODEL_SLUG}] nothing to do, all .md present", flush=True)
            return

    prompt_text = load_prompt()
    print(f"[{MODEL_SLUG}] prompt loaded: {len(prompt_text)} chars", flush=True)

    from vllm import LLM, SamplingParams

    llm = LLM(
        model=MODEL_DIR,
        trust_remote_code=True,
        dtype="bfloat16",
        max_model_len=MAX_MODEL_LEN,
        gpu_memory_utilization=GPU_MEMORY_UTILIZATION,
        max_num_seqs=MAX_NUM_SEQS,
        max_num_batched_tokens=MAX_NUM_BATCHED_TOKENS,
        tensor_parallel_size=1,
        limit_mm_per_prompt={"image": 1},
    )
    sp = SamplingParams(
        temperature=TEMPERATURE,
        top_p=1.0,
        repetition_penalty=1.0,
        max_tokens=MAX_OUTPUT_TOKENS,
    )

    chat_kwargs: dict = {}
    if not ENABLE_THINKING:
        chat_kwargs["chat_template_kwargs"] = {"enable_thinking": False}

    t0 = time.time()
    ok = err = processed = 0
    total = len(images)
    for i in range(0, total, BATCH_SIZE):
        chunk = images[i : i + BATCH_SIZE]
        convs = [
            [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": img_to_data_url(p)}},
                        {"type": "text", "text": prompt_text},
                    ],
                }
            ]
            for _, p in chunk
        ]
        try:
            outs = llm.chat(messages=convs, sampling_params=sp, use_tqdm=False, **chat_kwargs)
            for (bn, _), o in zip(chunk, outs):
                try:
                    text = strip_noise(o.outputs[0].text)
                    if text:
                        (out_dir / (Path(bn).stem + ".md")).write_text(text, encoding="utf-8")
                        ok += 1
                    else:
                        err += 1
                        print(f"[{MODEL_SLUG}] EMPTY: {bn}", flush=True)
                except Exception as e:
                    err += 1
                    print(f"[{MODEL_SLUG}] WRITE_ERR {bn}: {e}", flush=True)
        except Exception as e:
            err += len(chunk)
            print(f"[{MODEL_SLUG}] BATCH_ERR: {str(e)[:240]}", flush=True)

        processed += len(chunk)
        dt = time.time() - t0
        speed = processed / dt if dt > 0 else 0
        eta = (total - processed) / speed if speed > 0 else 0
        print(
            f"[{MODEL_SLUG}] {processed}/{total} ok={ok} err={err} {speed:.2f}img/s ETA={eta:.0f}s",
            flush=True,
        )

    dt = time.time() - t0
    print(f"[{MODEL_SLUG}] DONE ok={ok} err={err} elapsed={dt:.0f}s", flush=True)
    del llm
    gc.collect()
    try:
        import torch

        torch.cuda.empty_cache()
    except Exception:
        pass


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.set_start_method("spawn", force=True)
    sys.exit(main())
