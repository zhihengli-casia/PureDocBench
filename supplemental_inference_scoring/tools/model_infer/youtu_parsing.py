"""Youtu-Parsing HF inference on PureDocBench.

Wraps YoutuOCRParserHF.parse_file over the image list.
Per-image output: {stem}.md / {stem}.json / {stem}_layout.png / {stem}_hierarchy.json.
Resume-by-scanning-markdown.

Ref: ${PDB_REPOS_ROOT}/youtu-parsing/README.md
"""

import argparse
import os
import sys
import time
import traceback

sys.path.insert(0, "${PDB_REPOS_ROOT}/youtu-parsing")
sys.path.insert(0, "${PDB_REPOS_ROOT}/youtu-parsing/youtu_hf_parser")

from youtu_hf_parser import YoutuOCRParserHF  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model-path", default="${PDB_MODEL_ROOT}/Youtu-Parsing")
    p.add_argument("--image-root", default="${PDB_DATASET_ROOT}/images/clean")
    p.add_argument("--image-list", default="${PDB_IMAGE_LIST_ROOT}/image_list_pdb.txt")
    p.add_argument("--save-dir", default="${PDB_WORK_ROOT}/outputs/youtu-parsing")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--num-shards", type=int, default=1)
    p.add_argument("--shard-index", type=int, default=0)
    p.add_argument("--no-layout-png", action="store_true",
                   help="delete _layout.png after each parse to save disk")
    args = p.parse_args()
    if args.num_shards < 1 or not (0 <= args.shard_index < args.num_shards):
        raise ValueError(f"bad shard args: shard_index={args.shard_index}, num_shards={args.num_shards}")

    pred_dir = args.save_dir
    os.makedirs(pred_dir, exist_ok=True)

    with open(args.image_list) as f:
        rels = [ln.strip() for ln in f if ln.strip()]
    if args.start:
        rels = rels[args.start:]
    if args.limit and args.limit > 0:
        rels = rels[: args.limit]
    if args.num_shards > 1:
        rels = [r for i, r in enumerate(rels) if i % args.num_shards == args.shard_index]
        print(
            f"[youtu-parsing] SHARD {args.shard_index}/{args.num_shards}: "
            f"{len(rels)} assigned",
            flush=True,
        )

    total_before = len(rels)
    done_stems = {
        os.path.splitext(fn)[0]
        for fn in os.listdir(pred_dir)
        if fn.endswith(".md")
    }
    rels = [r for r in rels if os.path.splitext(os.path.basename(r))[0] not in done_stems]
    skipped = total_before - len(rels)
    print(
        f"[youtu-parsing] images to process: {len(rels)} "
        f"(skipped {skipped} already done in {pred_dir})",
        flush=True,
    )

    print("[youtu-parsing] loading model...", flush=True)
    parser = YoutuOCRParserHF(
        model_path=args.model_path,
        enable_angle_correct=False,
    )
    print("[youtu-parsing] model loaded.", flush=True)

    t_start = time.time()
    ok = 0
    err = 0
    n = len(rels)
    for idx, rel in enumerate(rels, 1):
        stem = os.path.splitext(os.path.basename(rel))[0]
        input_path = os.path.join(args.image_root, rel)
        t0 = time.time()
        try:
            parser.parse_file(input_path=input_path, output_dir=pred_dir)
            if args.no_layout_png:
                for ext in ("_layout.png",):
                    p_del = os.path.join(pred_dir, f"{stem}{ext}")
                    if os.path.exists(p_del):
                        os.remove(p_del)
            ok += 1
        except Exception as exc:
            err += 1
            print(f"[err] {rel}: {exc}", flush=True)
            traceback.print_exc()

        if idx % 10 == 0 or idx == n:
            dt_total = time.time() - t_start
            rate = idx / max(dt_total, 1e-6)
            eta = (n - idx) / max(rate, 1e-6)
            print(
                f"[{idx}/{n}] ok={ok} err={err} last={time.time()-t0:.1f}s "
                f"rate={rate:.3f} pages/s eta={eta/60:.1f}min",
                flush=True,
            )

    print(
        f"[youtu-parsing] DONE ok={ok} err={err} total_time={time.time()-t_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
