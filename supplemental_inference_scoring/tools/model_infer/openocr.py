#!/usr/bin/env python3
"""PureDocBench inference: OpenOCR (Topdu/OpenOCR).

Official stack: openocr-python unified API, task=ocr.
Default full-run setting here uses server/torch with GPU when available.
"""
import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

MODEL_SLUG = "openocr"
REPO_ROOT = Path(__file__).resolve().parents[2]
PDBV2_JSON = Path(os.environ.get("PDBV2_JSON", "manifest.json"))
IMAGES_ROOT = Path(os.environ.get("PDBV2_IMAGES_ROOT", "images/clean"))
PRED_ROOT = os.environ.get("PDBV2_PRED_ROOT", "predictions")
SMOKE_ROOT = os.environ.get("PDBV2_SMOKE_ROOT", "outputs_smoke")


def build_image_index():
    data = json.loads(PDBV2_JSON.read_text(encoding="utf-8"))
    basenames = [Path(e["page_info"]["image_path"]).name for e in data]
    fs_index = {}
    for p in IMAGES_ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp"}:
            fs_index[p.name] = p
    pairs, missing = [], []
    for bn in basenames:
        p = fs_index.get(bn)
        if p:
            pairs.append((bn, p))
        else:
            missing.append(bn)
    if missing:
        print(f"[{MODEL_SLUG}] WARN missing={len(missing)} first={missing[:5]}", flush=True)
    return pairs


def extract_text(result):
    records = []
    payload = result
    if isinstance(payload, tuple) and payload:
        payload = payload[0]
    if isinstance(payload, str):
        payload = [payload]
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, str) and "\t" in item:
                item = item.split("\t", 1)[1]
            if isinstance(item, str):
                try:
                    parsed = json.loads(item)
                    if isinstance(parsed, list):
                        records.extend(parsed)
                        continue
                except Exception:
                    pass
                if item.strip():
                    records.append({"transcription": item.strip()})
            elif isinstance(item, dict):
                records.append(item)
    elif isinstance(payload, dict):
        records.append(payload)

    lines = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        text = str(rec.get("transcription", "")).strip()
        if text:
            lines.append(text)
    return "\n".join(lines).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--num-shards", type=int, default=1)
    ap.add_argument("--shard-index", type=int, default=0)
    ap.add_argument("--backend", default=os.environ.get("OPENOCR_BACKEND", "torch"), choices=["torch", "onnx"])
    ap.add_argument("--mode", default=os.environ.get("OPENOCR_MODE", "server"), choices=["mobile", "server"])
    ap.add_argument("--use-gpu", default=os.environ.get("OPENOCR_USE_GPU", "true"), choices=["auto", "true", "false"])
    ap.add_argument("--rec-batch-num", type=int, default=int(os.environ.get("OPENOCR_REC_BATCH_NUM", "32")))
    ap.add_argument("--drop-score", type=float, default=float(os.environ.get("OPENOCR_DROP_SCORE", "0.5")))
    ap.add_argument("--empty-on-error", action="store_true", default=os.environ.get("OPENOCR_EMPTY_ON_ERROR", "0") == "1")
    args = ap.parse_args()

    if args.num_shards < 1 or not (0 <= args.shard_index < args.num_shards):
        raise ValueError(f"bad shard args: shard_index={args.shard_index}, num_shards={args.num_shards}")

    out_root = SMOKE_ROOT if args.smoke else PRED_ROOT
    out_dir = REPO_ROOT / out_root / MODEL_SLUG
    out_dir.mkdir(parents=True, exist_ok=True)

    work_dir = REPO_ROOT / ".cache" / "openocr_workdir" / f"{out_root}_s{args.shard_index}_of_{args.num_shards}_pid_{os.getpid()}"
    work_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(work_dir)

    images = build_image_index()
    if args.num_shards > 1:
        images = [x for idx, x in enumerate(images) if idx % args.num_shards == args.shard_index]
        print(f"[{MODEL_SLUG}] SHARD {args.shard_index}/{args.num_shards}: assigned={len(images)}", flush=True)
    if args.smoke:
        images = images[:args.n]
        print(f"[{MODEL_SLUG}] SMOKE pages={len(images)} -> {out_dir}", flush=True)
    else:
        before = len(images)
        images = [(bn, p) for bn, p in images if not (out_dir / f"{Path(bn).stem}.md").exists()]
        print(f"[{MODEL_SLUG}] FULL pending={len(images)} skipped={before-len(images)} -> {out_dir}", flush=True)
        if not images:
            return 0

    # OpenOCR logs full OCR JSON at INFO for every page; suppress package logs
    # so long full runs do not create multi-GB log files.
    import logging
    logging.disable(logging.INFO)
    print(f"[{MODEL_SLUG}] loading OpenOCR task=ocr mode={args.mode} backend={args.backend} use_gpu={args.use_gpu}", flush=True)
    # The script is intentionally named openocr.py; remove its directory so it
    # does not shadow the installed official openocr package.
    script_dir = str(Path(__file__).resolve().parent)
    sys.path = [x for x in sys.path if str(Path(x or ".").resolve()) != script_dir]
    from openocr import OpenOCR
    ocr = OpenOCR(
        task="ocr",
        mode=args.mode,
        backend=args.backend,
        use_gpu=args.use_gpu,
        drop_score=args.drop_score,
    )
    print(f"[{MODEL_SLUG}] model loaded", flush=True)

    t0 = time.time()
    ok = err = 0
    total = len(images)
    for i, (bn, img_path) in enumerate(images, 1):
        out_path = out_dir / f"{Path(bn).stem}.md"
        if out_path.exists() and not args.smoke:
            continue
        try:
            result = ocr(str(img_path), rec_batch_num=args.rec_batch_num)
            text = extract_text(result).replace("\x00", "").strip()
            if not text:
                raise RuntimeError("empty OCR text")
            tmp_path = out_path.with_suffix(out_path.suffix + f".tmp.{os.getpid()}")
            tmp_path.write_bytes((text + "\n").encode("utf-8"))
            stored = tmp_path.read_text(encoding="utf-8", errors="ignore").replace("\x00", "").strip()
            if not stored:
                tmp_path.unlink(missing_ok=True)
                raise RuntimeError("empty OCR text after write verification")
            tmp_path.replace(out_path)
            ok += 1
        except Exception as e:
            err += 1
            print(f"[{MODEL_SLUG}] ERR {bn}: {str(e)[:240]}", flush=True)
            traceback.print_exc()
            if args.empty_on_error:
                out_path.write_text("", encoding="utf-8")
                ok += 1
        if i % 5 == 0 or i == total:
            dt = time.time() - t0
            speed = i / dt if dt > 0 else 0.0
            eta = (total - i) / speed if speed > 0 else 0.0
            print(f"[{MODEL_SLUG}] {i}/{total} ok={ok} err={err} {speed:.2f}img/s ETA={eta:.0f}s", flush=True)
    print(f"[{MODEL_SLUG}] DONE ok={ok} err={err} elapsed={time.time()-t0:.0f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
