#!/usr/bin/env python3
"""Conservative post-process for paddleocr_vl predictions.
  - decode HTML entities
  - strip ONLY noise attributes: style, class, align, width, cellspacing, cellpadding
  - keep border (GT keeps border="1")
  - normalize border=1 -> border="1" to match GT
  - collapse 3+ newlines
"""
import argparse
import html
import os
import re

ENTITY_RE = re.compile(r'&[a-z#0-9]+;', re.IGNORECASE)
STYLE_RE = re.compile(r"\s+style\s*=\s*(['\"])[^'\"]*\1", re.IGNORECASE)
CLASS_RE = re.compile(r"\s+class\s*=\s*(['\"])[^'\"]*\1", re.IGNORECASE)
ALIGN_RE = re.compile(r"\s+align\s*=\s*(['\"])[^'\"]*\1", re.IGNORECASE)
CELLSPACING_RE = re.compile(r"\s+cellspacing\s*=\s*(['\"]?\d+['\"]?)", re.IGNORECASE)
CELLPADDING_RE = re.compile(r"\s+cellpadding\s*=\s*(['\"]?\d+['\"]?)", re.IGNORECASE)
WIDTH_RE = re.compile(r"\s+width\s*=\s*(['\"]?\d+%?['\"]?)", re.IGNORECASE)
BORDER_NO_QUOTE_RE = re.compile(r"(\s+border\s*=)\s*(\d+)(?!['\"])", re.IGNORECASE)
MULTI_BLANK_RE = re.compile(r'\n{3,}')


def clean_text(s: str) -> str:
    if ENTITY_RE.search(s):
        s = html.unescape(s)
    s = STYLE_RE.sub('', s)
    s = CLASS_RE.sub('', s)
    s = ALIGN_RE.sub('', s)
    s = CELLSPACING_RE.sub('', s)
    s = CELLPADDING_RE.sub('', s)
    s = WIDTH_RE.sub('', s)
    s = BORDER_NO_QUOTE_RE.sub(r'\1"\2"', s)
    s = MULTI_BLANK_RE.sub('\n\n', s)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--dst', required=True)
    args = ap.parse_args()

    os.makedirs(args.dst, exist_ok=True)
    files = sorted(f for f in os.listdir(args.src) if f.endswith('.md'))
    print(f"[clean v2] {len(files)} .md files in {args.src}")
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
            if sample_before is None and '<table' in raw:
                i = raw.find('<table')
                sample_before = raw[i:i+300]
                j = cleaned.find('<table')
                sample_after = cleaned[j:j+300]
        bytes_before += len(raw)
        bytes_after += len(cleaned)
        with open(p_out, 'w', encoding='utf-8') as f:
            f.write(cleaned)

    print(f"[clean v2] wrote {len(files)} files to {args.dst}")
    print(f"[clean v2] changed={n_changed}")
    print(f"[clean v2] bytes: {bytes_before:,} -> {bytes_after:,} ({(bytes_before-bytes_after)/bytes_before*100:.1f}%)")
    if sample_before:
        print("\n=== sample table BEFORE ===")
        print(sample_before)
        print("\n=== sample table AFTER ===")
        print(sample_after)


if __name__ == '__main__':
    main()
