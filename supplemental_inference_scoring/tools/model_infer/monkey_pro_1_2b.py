#!/usr/bin/env python3
"""PureDocBench inference: MonkeyOCR-pro-1.2B.

Standalone script (no shared helpers). Loads MonkeyOCR once and loops 1474 images.
Mirrors `OmniDocBench/tools/model_infer/MonkeyOCR_img2md.py` (which itself is
MonkeyOCR's `parse.py`) but specialized to PureDocBench manifest.

Setup required:
  - MonkeyOCR repo cloned (default: ${PDB_WORK_ROOT}/repos/MonkeyOCR)
  - magic_pdf pip-installed in env (see repro/envs/monkey_pro_1_2b.txt)
  - Model weights at ${PDB_WORK_ROOT}/new_models/MonkeyOCR-pro-1.2B/{Structure,Relation,Recognition}
  - Inference config at configs/models/monkey_pro_1_2b_inference.yaml

Usage:
  CUDA_VISIBLE_DEVICES=0 python monkey_pro_1_2b.py             # full 1474 pages
  CUDA_VISIBLE_DEVICES=0 python monkey_pro_1_2b.py --smoke     # first 5 pages
"""
import argparse
import gc
import json
import os
import shutil
import sys
import time
import traceback
from pathlib import Path

# ---- model identification (edit per model) ----------------------------------
MODEL_SLUG = "monkey_pro_1_2b"
MODEL_NAME = "MonkeyOCR-pro-1.2B"

# ---- repo paths -------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
INFER_CFG = REPO_ROOT / "configs" / "models" / f"{MODEL_SLUG}_inference.yaml"
PRED_DIR_FULL = REPO_ROOT / os.environ.get("PDBV2_PRED_ROOT", "predictions") / MODEL_SLUG
PRED_DIR_SMOKE = REPO_ROOT / os.environ.get("PDBV2_SMOKE_ROOT", "outputs_smoke") / MODEL_SLUG
WORKDIR = REPO_ROOT / ".cache" / f"{MODEL_SLUG}_workdir"

IMAGES_ROOT = Path(os.environ.get("PDBV2_IMAGES_ROOT", "images/clean"))
PDBV2_JSON = Path(os.environ.get("PDBV2_JSON", "manifest.json"))

# ---- MonkeyOCR repo path (override via MONKEY_REPO env var) -----------------
MONKEY_REPO = os.environ.get("MONKEY_REPO", "${PDB_REPOS_ROOT}/MonkeyOCR")


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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true", help="run only first --n images")
    ap.add_argument("--n", type=int, default=5)
    args = ap.parse_args()

    if not INFER_CFG.exists():
        raise FileNotFoundError(f"Inference config missing: {INFER_CFG}")

    # MonkeyOCR magic_pdf may not be pip-installed in some envs; fallback to repo on sys.path.
    if Path(MONKEY_REPO).exists():
        sys.path.insert(0, MONKEY_REPO)

    out_dir = PRED_DIR_SMOKE if args.smoke else PRED_DIR_FULL
    out_dir.mkdir(parents=True, exist_ok=True)
    WORKDIR.mkdir(parents=True, exist_ok=True)

    images = build_image_index()
    print(f"[{MODEL_SLUG}] image index: {len(images)} entries", flush=True)
    if args.smoke:
        images = images[: args.n]
        print(f"[{MODEL_SLUG}] SMOKE: {len(images)} pages -> {out_dir}", flush=True)
    else:
        done = {p.stem for p in out_dir.glob("*.md")}
        images = [(bn, p) for bn, p in images if Path(bn).stem not in done]
        print(f"[{MODEL_SLUG}] FULL: {len(images)} pending -> {out_dir}", flush=True)
        if not images:
            print(f"[{MODEL_SLUG}] nothing to do, all .md present", flush=True)
            return

    print(f"[{MODEL_SLUG}] loading MonkeyOCR (config={INFER_CFG})...", flush=True)
    from magic_pdf.data.data_reader_writer import FileBasedDataReader, FileBasedDataWriter
    from magic_pdf.data.dataset import ImageDataset
    from magic_pdf.model.custom_model import MonkeyOCR
    from magic_pdf.model.doc_analyze_by_custom_model_llm import doc_analyze_llm

    model = MonkeyOCR(str(INFER_CFG))
    print(f"[{MODEL_SLUG}] model loaded", flush=True)

    reader = FileBasedDataReader()
    t0 = time.time()
    ok = err = 0
    total = len(images)
    for i, (bn, img_path) in enumerate(images, 1):
        stem = Path(bn).stem
        per_workdir = WORKDIR / f"_{i % 100}"
        try:
            if per_workdir.exists():
                shutil.rmtree(per_workdir)
            local_md_dir = per_workdir / stem
            local_image_dir = local_md_dir / "images"
            local_md_dir.mkdir(parents=True, exist_ok=True)
            local_image_dir.mkdir(parents=True, exist_ok=True)

            file_bytes = reader.read(str(img_path))
            ds = ImageDataset(file_bytes)
            infer = ds.apply(doc_analyze_llm, MonkeyOCR_model=model)

            image_writer = FileBasedDataWriter(str(local_image_dir))
            md_writer = FileBasedDataWriter(str(local_md_dir))
            pipe = infer.pipe_ocr_mode(image_writer, MonkeyOCR_model=model)
            pipe.dump_md(md_writer, f"{stem}.md", "images")

            md_path = local_md_dir / f"{stem}.md"
            if md_path.exists() and md_path.stat().st_size > 0:
                shutil.copy2(md_path, out_dir / f"{stem}.md")
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
            print(
                f"[{MODEL_SLUG}] {i}/{total} ok={ok} err={err} {speed:.2f}img/s ETA={eta:.0f}s",
                flush=True,
            )

    dt = time.time() - t0
    print(f"[{MODEL_SLUG}] DONE ok={ok} err={err} elapsed={dt:.0f}s", flush=True)
    del model
    gc.collect()


if __name__ == "__main__":
    main()
    os._exit(0)  # bypass vLLM 0.8.5 NCCL destroy hang
