#!/usr/bin/env python3
"""Clean minicpm-v 4.5 thinking-model output.

Format observed:
  <think>
  [actual markdown OCR result — tables, formulas, HTML, etc.]
  </think>

  [post-think English summary — NOT useful for evaluation]

Strategy:
  - If both <think> and </think> present: keep ONLY the content between them.
  - Otherwise: keep file as-is.
  - Strip leading/trailing whitespace.
"""
import os
import re
import argparse

THINK_RE = re.compile(r'<think>\s*(.*?)\s*</think>', re.DOTALL)


def clean_text(s: str) -> str:
    m = THINK_RE.search(s)
    if m:
        return m.group(1).strip() + '\n'
    return s.strip() + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--dst', required=True)
    args = ap.parse_args()

    os.makedirs(args.dst, exist_ok=True)
    files = sorted(f for f in os.listdir(args.src) if f.endswith('.md'))
    print(f"[clean] {len(files)} .md files in {args.src}")

    n_think = n_no_think = 0
    sample_before = sample_after = None
    for fn in files:
        with open(os.path.join(args.src, fn), 'r', encoding='utf-8') as f:
            raw = f.read()
        if '<think>' in raw and '</think>' in raw:
            n_think += 1
        else:
            n_no_think += 1
        cleaned = clean_text(raw)
        if sample_before is None and cleaned != raw.strip() + '\n':
            sample_before = raw[:300]
            sample_after = cleaned[:300]
        with open(os.path.join(args.dst, fn), 'w', encoding='utf-8') as f:
            f.write(cleaned)

    print(f"[clean] wrote {len(files)} files to {args.dst}")
    print(f"[clean] with_think={n_think} without_think={n_no_think}")
    if sample_before is not None:
        print("\n=== sample BEFORE (300 chars) ===")
        print(sample_before)
        print("\n=== sample AFTER (300 chars) ===")
        print(sample_after)


if __name__ == '__main__':
    main()
