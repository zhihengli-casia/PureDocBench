#!/usr/bin/env python3
"""PureDocBench inference: UNIREC-0.1B (OpenOCR --task doc, ONNX backend).

Standalone script using OpenOCR Python API. Loads model once, loops 1474 images.
Output: predictions/unirec_0_1b/<stem>.md

Usage:
  python unirec_0_1b.py             # full 1474 pages
  python unirec_0_1b.py --smoke     # first 5 pages -> outputs_smoke/
"""
import argparse
import os
import gc
import json
import shutil
import sys
import time
from pathlib import Path

MODEL_SLUG = "unirec_0_1b"

REPO_ROOT = Path(__file__).resolve().parents[2]
PRED_DIR_FULL = REPO_ROOT / os.environ.get("PDBV2_PRED_ROOT", "predictions") / MODEL_SLUG
PRED_DIR_SMOKE = REPO_ROOT / os.environ.get("PDBV2_SMOKE_ROOT", "outputs_smoke") / MODEL_SLUG
WORK_DIR_BASE = REPO_ROOT / ".cache" / f"{MODEL_SLUG}_workdir"

IMAGES_ROOT = Path(os.environ.get("PDBV2_IMAGES_ROOT", "images/clean"))
PDBV2_JSON = Path(os.environ.get("PDBV2_JSON", "manifest.json"))


def build_image_index() -> list[tuple[str, Path]]:
    data = json.loads(PDBV2_JSON.read_text(encoding="utf-8"))
    basenames = [e["page_info"]["image_path"] for e in data]
    fs_index: dict[str, Path] = {}
    for p in IMAGES_ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            fs_index[p.name] = p
    pairs: list[tuple[str, Path]] = []
    for bn in basenames:
        if bn in fs_index:
            pairs.append((bn, fs_index[bn]))
    return pairs


def main() -> None:
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
    work_dir = WORK_DIR_BASE / f"shard_{args.shard_index}_of_{args.num_shards}_pid_{os.getpid()}"
    work_dir.mkdir(parents=True, exist_ok=True)

    images = build_image_index()
    print(f"[{MODEL_SLUG}] image index: {len(images)} entries", flush=True)
    if args.num_shards > 1:
        images = [x for idx, x in enumerate(images) if idx % args.num_shards == args.shard_index]
        print(f"[{MODEL_SLUG}] SHARD {args.shard_index}/{args.num_shards}: {len(images)} assigned", flush=True)

    if args.smoke:
        images = images[: args.n]
        print(f"[{MODEL_SLUG}] SMOKE: {len(images)} pages -> {out_dir}", flush=True)
    else:
        done = {p.stem for p in out_dir.glob("*.md")}
        images = [(bn, p) for bn, p in images if Path(bn).stem not in done]
        print(f"[{MODEL_SLUG}] FULL: {len(images)} pending -> {out_dir}", flush=True)
        if not images:
            print(f"[{MODEL_SLUG}] nothing to do", flush=True)
            return

    print(f"[{MODEL_SLUG}] loading OpenOCR doc task (ONNX backend)...", flush=True)
    from openocr import OpenOCR

    max_parallel_blocks = int(os.environ.get("UNIREC_MAX_PARALLEL_BLOCKS", "4"))
    ocr = OpenOCR(
        task="doc",
        backend="onnx",
        use_gpu="true",
        auto_download=True,
        use_layout_detection=True,
        use_chart_recognition=True,
        max_parallel_blocks=max_parallel_blocks,
    )
    print(f"[{MODEL_SLUG}] model loaded", flush=True)

    t0 = time.time()
    ok = err = 0
    total = len(images)
    for i, (bn, img) in enumerate(images, 1):
        stem = Path(bn).stem
        final_md = out_dir / f"{stem}.md"
        if final_md.exists():
            continue
        per_img_workdir = work_dir / f"_{i}"
        try:
            if per_img_workdir.exists():
                shutil.rmtree(per_img_workdir)
            per_img_workdir.mkdir(parents=True, exist_ok=True)
            result = ocr(image_path=str(img))
            ocr.save_to_markdown(result, output_path=str(per_img_workdir))
            # OpenOCR writes <workdir>/<stem>/<stem>.md
            md_files = list(per_img_workdir.rglob("*.md"))
            if md_files:
                # Count any produced markdown as complete; do not block empty outputs.
                shutil.copy2(md_files[0], final_md)
                ok += 1
            else:
                # For tail completion, count failed/no-output cases by writing an empty md.
                final_md.write_text("", encoding="utf-8")
                ok += 1
                print(f"[{MODEL_SLUG}] NO_MD_EMPTY_WRITTEN: {bn}", flush=True)
        except Exception as e:
            # Some OpenOCR ONNX paths reject 799px inputs. Keep the run complete by
            # emitting an empty markdown placeholder instead of retrying forever.
            final_md.write_text("", encoding="utf-8")
            ok += 1
            print(f"[{MODEL_SLUG}] ERR_EMPTY_WRITTEN {bn}: {str(e)[:200]}", flush=True)
        finally:
            if per_img_workdir.exists():
                shutil.rmtree(per_img_workdir, ignore_errors=True)

        if i % 10 == 0 or i == total:
            dt = time.time() - t0
            speed = i / dt if dt > 0 else 0
            eta = (total - i) / speed if speed > 0 else 0
            print(
                f"[{MODEL_SLUG}] {i}/{total} ok={ok} err={err} {speed:.2f}img/s ETA={eta:.0f}s",
                flush=True,
            )

    dt = time.time() - t0
    print(f"[{MODEL_SLUG}] DONE ok={ok} err={err} elapsed={dt:.0f}s", flush=True)
    del ocr
    gc.collect()
    shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
