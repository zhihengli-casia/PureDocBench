#!/usr/bin/env python3
"""PureDocBench inference: OpenDoc-0.1B (OpenOCR pipeline, ONNX runtime).

Layout (PP-DocLayoutV2) + UniRec recognition. Outputs unicode markdown.
Auto-downloads ONNX weights to ~/.cache/openocr/ on first run.

Usage:
  python opendoc_0_1b.py            # full
  python opendoc_0_1b.py --smoke
"""
import argparse
import json
import os
import shutil
import sys
import time
import traceback
from pathlib import Path

MODEL_SLUG = "opendoc_0_1b"

REPO_ROOT = Path(__file__).resolve().parents[2]
PRED_DIR_FULL = REPO_ROOT / os.environ.get("PDBV2_PRED_ROOT", "predictions") / MODEL_SLUG
PRED_DIR_SMOKE = REPO_ROOT / os.environ.get("PDBV2_SMOKE_ROOT", "outputs_smoke") / MODEL_SLUG
WORKDIR = REPO_ROOT / ".cache" / f"{MODEL_SLUG}_workdir"

IMAGES_ROOT = Path(os.environ.get("PDBV2_IMAGES_ROOT", "images/clean"))
PDBV2_JSON = Path(os.environ.get("PDBV2_JSON", "manifest.json"))


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
    ap.add_argument("--use-gpu", action="store_true", help="enable CUDAExecutionProvider")
    ap.add_argument("--num-shards", type=int, default=1)
    ap.add_argument("--shard-index", type=int, default=0)
    args = ap.parse_args()
    if args.num_shards < 1 or not (0 <= args.shard_index < args.num_shards):
        raise ValueError(f"bad shard args: shard_index={args.shard_index}, num_shards={args.num_shards}")

    out_dir = PRED_DIR_SMOKE if args.smoke else PRED_DIR_FULL
    out_dir.mkdir(parents=True, exist_ok=True)
    workdir = WORKDIR / f"s{args.shard_index}_of_{args.num_shards}_pid_{os.getpid()}"
    workdir.mkdir(parents=True, exist_ok=True)

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

    import logging
    logging.disable(logging.INFO)
    print(f"[{MODEL_SLUG}] importing OpenDocONNX...", flush=True)
    # Avoid shadowing the installed official openocr package by local
    # tools/model_infer/openocr.py.
    script_dir = str(Path(__file__).resolve().parent)
    sys.path = [x for x in sys.path if str(Path(x or ".").resolve()) != script_dir]
    from openocr.tools.infer_doc_onnx import OpenDocONNX

    print(f"[{MODEL_SLUG}] init pipeline (use_gpu={args.use_gpu}, auto_download=True)...", flush=True)
    pipe = OpenDocONNX(use_gpu=args.use_gpu, auto_download=True)
    print(f"[{MODEL_SLUG}] pipeline ready", flush=True)

    t0 = time.time()
    ok = err = 0
    total = len(images)

    for i, (bn, img_path) in enumerate(images, 1):
        stem = Path(bn).stem
        per_workdir = workdir / f"_{i}"
        try:
            if per_workdir.exists():
                shutil.rmtree(per_workdir)
            per_workdir.mkdir(parents=True, exist_ok=True)
            result = pipe(img_path=str(img_path), merge_layout_blocks=True)
            pipe.save_to_markdown(result, str(per_workdir))
            # save_to_markdown writes <workdir>/<stem>/<stem>.md, copy to out_dir/<stem>.md
            md_src = per_workdir / stem / f"{stem}.md"
            if md_src.exists() and md_src.stat().st_size > 0:
                shutil.copy2(md_src, out_dir / f"{stem}.md")
                ok += 1
            else:
                err += 1
                print(f"[{MODEL_SLUG}] EMPTY: {bn}", flush=True)
        except Exception as e:
            err += 1
            print(f"[{MODEL_SLUG}] ERR {bn}: {str(e)[:240]}", flush=True)
            traceback.print_exc()
        finally:
            if per_workdir.exists():
                shutil.rmtree(per_workdir, ignore_errors=True)
        if i % 5 == 0 or i == total:
            dt = time.time() - t0
            speed = i / dt if dt > 0 else 0
            eta = (total - i) / speed if speed > 0 else 0
            print(f"[{MODEL_SLUG}] {i}/{total} ok={ok} err={err} {speed:.2f}img/s ETA={eta:.0f}s", flush=True)

    dt = time.time() - t0
    print(f"[{MODEL_SLUG}] DONE ok={ok} err={err} elapsed={dt:.0f}s", flush=True)


if __name__ == "__main__":
    sys.exit(main())
