#!/usr/bin/env python3
"""Post-process paddleocr_vl predictions to remove eval-noise:
  - decode HTML entities (&#x27; -> ', &amp; -> &, ...)
  - strip inline table attributes (style='...', border=N, class='...')
  - collapse 3+ newlines
"""
import argparse
import html
import os
import re

ENTITY_RE = re.compile(r'&[a-z#0-9]+;', re.IGNORECASE)
STYLE_RE = re.compile(r"\s+style\s*=\s*(['\"])[^'\"]*\1", re.IGNORECASE)
BORDER_RE = re.compile(r"\s+border\s*=\s*(['\"]?\d+['\"]?)", re.IGNORECASE)
CLASS_RE = re.compile(r"\s+class\s*=\s*(['\"])[^'\"]*\1", re.IGNORECASE)
ALIGN_RE = re.compile(r"\s+align\s*=\s*(['\"])[^'\"]*\1", re.IGNORECASE)
CELLSPACING_RE = re.compile(r"\s+cellspacing\s*=\s*(['\"]?\d+['\"]?)", re.IGNORECASE)
CELLPADDING_RE = re.compile(r"\s+cellpadding\s*=\s*(['\"]?\d+['\"]?)", re.IGNORECASE)
WIDTH_RE = re.compile(r"\s+width\s*=\s*(['\"]?\d+%?['\"]?)", re.IGNORECASE)
MULTI_BLANK_RE = re.compile(r'\n{3,}')


def clean_text(s: str) -> str:
    if ENTITY_RE.search(s):
        s = html.unescape(s)
    s = STYLE_RE.sub('', s)
    s = BORDER_RE.sub('', s)
    s = CLASS_RE.sub('', s)
    s = ALIGN_RE.sub('', s)
    s = CELLSPACING_RE.sub('', s)
    s = CELLPADDING_RE.sub('', s)
    s = WIDTH_RE.sub('', s)
    s = MULTI_BLANK_RE.sub('\n\n', s)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--dst', required=True)
    args = ap.parse_args()

    os.makedirs(args.dst, exist_ok=True)
    files = sorted(f for f in os.listdir(args.src) if f.endswith('.md'))
    print(f"[clean] {len(files)} .md files in {args.src}")
    n_changed = 0
    bytes_before = bytes_after = 0
    sample_before = sample_after = None
    for fn in files:
        p_in = os.path.join(args.src, fn)
        p_out = os.path.join(args.dst, fn)
        with open(p_in, 'r', encoding='utf-8') as f:
            raw = f.read()
        cleaned = clean_text(raw)
        if cleaned != raw:
            n_changed += 1
            if sample_before is None:
                sample_before, sample_after = raw[:400], cleaned[:400]
        bytes_before += len(raw)
        bytes_after += len(cleaned)
        with open(p_out, 'w', encoding='utf-8') as f:
            f.write(cleaned)

    print(f"[clean] wrote {len(files)} files to {args.dst}")
    print(f"[clean] changed={n_changed} unchanged={len(files)-n_changed}")
    print(f"[clean] bytes: {bytes_before:,} -> {bytes_after:,} (saved {bytes_before-bytes_after:,}, {(bytes_before-bytes_after)/bytes_before*100:.1f}%)")
    if sample_before is not None:
        print("\n=== sample BEFORE (first 400 chars) ===")
        print(sample_before)
        print("\n=== sample AFTER (first 400 chars) ===")
        print(sample_after)


if __name__ == '__main__':
    main()
