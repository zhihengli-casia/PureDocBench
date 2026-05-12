#!/usr/bin/env python3
"""Clean DeepSeek-OCR-2 grounding markers from prediction .md files.

Removes inline tags:
  <|ref|>...<|/ref|>
  <|det|>[[...]]<|/det|>

Writes cleaned copies to a sibling directory (default: <src>_clean).
Original files are left untouched.
"""
import os
import re
import sys
import argparse

REF_RE = re.compile(r'<\|ref\|>.*?<\|/ref\|>', re.DOTALL)
DET_RE = re.compile(r'<\|det\|>.*?<\|/det\|>', re.DOTALL)
# Collapse 3+ blank lines to a single blank line
MULTI_BLANK_RE = re.compile(r'\n{3,}')


def clean_text(s: str) -> str:
    s = REF_RE.sub('', s)
    s = DET_RE.sub('', s)
    s = MULTI_BLANK_RE.sub('\n\n', s)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True, help='source predictions dir')
    ap.add_argument('--dst', required=True, help='output cleaned predictions dir')
    args = ap.parse_args()

    os.makedirs(args.dst, exist_ok=True)
    files = sorted(f for f in os.listdir(args.src) if f.endswith('.md'))
    print(f"[clean] {len(files)} .md files in {args.src}")
    n_changed = 0
    n_unchanged = 0
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
                sample_before, sample_after = raw[:300], cleaned[:300]
        else:
            n_unchanged += 1
        with open(p_out, 'w', encoding='utf-8') as f:
            f.write(cleaned)

    print(f"[clean] wrote {len(files)} files to {args.dst}")
    print(f"[clean] changed={n_changed} unchanged={n_unchanged}")
    if sample_before is not None:
        print("\n=== sample BEFORE (first 300 chars) ===")
        print(sample_before)
        print("\n=== sample AFTER (first 300 chars) ===")
        print(sample_after)


if __name__ == '__main__':
    main()
