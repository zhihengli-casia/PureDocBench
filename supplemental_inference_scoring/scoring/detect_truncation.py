#!/usr/bin/env python3
"""Detect truncated prediction .md files for a given alias.

Composite signals (need 2+ to flag as truncated):
  S1. file size in top 5% (p95) — likely hit max_tokens budget
  S2. tail ends mid-word (not at sentence terminator / markdown structural close)
  S3. pred text length << GT total text length (ratio < 0.5)
  S4. tail 400 chars contains a repeating phrase (>=3 reps of >=20-char run)

Output: truncated_cases.tsv with cols: file, size, signals, last80, gt_len, pred_len
"""
import os
import json
import re
import sys
import argparse
from glob import glob

GT_PATH = "${PDB_MANIFEST_JSON}"

# Acceptable terminal characters (sentence end / markdown structural close)
TERMINATOR_RE = re.compile(
    r'[\s\n]*(?:[.。!?！？;；:：,，)\]}>"\'"”’]|---+|\*\*\*+|```|<\/[a-z]+>|\|)\s*$'
)

# Mid-word termination — letter or CJK char without punctuation
MID_WORD_RE = re.compile(r'[A-Za-z0-9一-鿿]\s*$')


def has_repetition(text: str, min_reps: int = 3, min_run: int = 20) -> bool:
    """True if `text` ends with the same substring repeated >= min_reps times."""
    n = len(text)
    for run_len in range(min_run, min(200, n // min_reps) + 1):
        for start in range(max(0, n - run_len * (min_reps + 1)), n - run_len * min_reps + 1):
            chunk = text[start:start + run_len]
            count = 1
            pos = start + run_len
            while pos + run_len <= n and text[pos:pos + run_len] == chunk:
                count += 1
                pos += run_len
            if count >= min_reps:
                return True
    return False


def gt_text_length(sample) -> int:
    total = 0
    for det in sample.get("layout_dets", []):
        if det.get("ignore"):
            continue
        t = det.get("text") or ""
        total += len(str(t))
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size-pct", type=float, default=95.0,
                    help="size percentile threshold for S1 (default 95)")
    ap.add_argument("--len-ratio", type=float, default=0.5,
                    help="pred/gt length ratio threshold for S3 (default 0.5)")
    args = ap.parse_args()

    print(f"[detect] pred_dir={args.pred_dir}")

    gt = json.load(open(GT_PATH))
    gt_by_basename = {}
    for s in gt:
        b = os.path.basename(s["page_info"]["image_path"]).rsplit(".", 1)[0]
        gt_by_basename[b] = s

    files = sorted(glob(os.path.join(args.pred_dir, "*.md")))
    print(f"[detect] {len(files)} .md files")

    sizes = [(os.path.getsize(f), f) for f in files]
    sizes.sort()
    p95_size = sizes[int(len(sizes) * args.size_pct / 100.0)][0] if sizes else 0
    print(f"[detect] p{args.size_pct:.0f}_size = {p95_size}")

    rows = []
    for f in files:
        size = os.path.getsize(f)
        with open(f, "r", encoding="utf-8", errors="replace") as g:
            text = g.read()

        # S1: large file
        s1 = size >= p95_size

        # S2: ends mid-word
        tail = text[-200:]
        ends_clean = bool(TERMINATOR_RE.search(text))
        s2 = MID_WORD_RE.search(text) and not ends_clean

        # S3: too short vs GT
        base = os.path.basename(f).rsplit(".", 1)[0]
        gt_sample = gt_by_basename.get(base)
        gt_len = gt_text_length(gt_sample) if gt_sample else 0
        pred_len = len(text)
        s3 = gt_len > 0 and pred_len < args.len_ratio * gt_len

        # S4: ending repetition
        s4 = has_repetition(text[-400:])

        signals = (1 if s1 else 0) + (1 if s2 else 0) + (1 if s3 else 0) + (1 if s4 else 0)
        if signals >= 2 or s4:
            sig_str = "".join("1" if x else "0" for x in (s1, s2, s3, s4))
            last80 = text[-80:].replace("\n", "\\n").replace("\t", " ")
            rows.append((os.path.basename(f), size, sig_str, last80, gt_len, pred_len))

    rows.sort(key=lambda r: -r[1])
    with open(args.out, "w", encoding="utf-8") as g:
        g.write("file\tsize\tsig(S1S2S3S4)\tlast80\tgt_len\tpred_len\n")
        for r in rows:
            g.write("\t".join(str(x) for x in r) + "\n")

    print(f"[detect] flagged: {len(rows)} / {len(files)} ({100*len(rows)/len(files):.1f}%)")
    print(f"[detect] saved to: {args.out}")
    print(f"\n=== top 20 by size ===")
    for r in rows[:20]:
        print(f"  size={r[1]:>6}  sig={r[2]}  gt={r[4]:>5} pred={r[5]:>5}  last80={r[3][:60]}...  | {r[0]}")


if __name__ == "__main__":
    main()
