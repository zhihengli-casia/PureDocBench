#!/usr/bin/env python3
"""Strip logics_parsing_v2 outer-wrapper HTML tags from prediction .md files.

Removes:
  <p data-bbox="...">              -> ''
  </p>                             -> '\n'
  <div class="formula" data-bbox=...> / <div class="table" data-bbox=...> /
  <div class="table caption" data-bbox=...>                     -> ''
  </div>                           -> '\n'
  <img data-bbox="..."/>           -> ''

Keeps inner <table>...</table>, <tr>, <td>, $$...$$ (TableTEDS / FormulaCDM need them).
Original files untouched; cleaned copies go to <src>_clean.
"""
import os
import re
import argparse


P_OPEN = re.compile(r'<p\s+data-bbox="[^"]*">')
P_CLOSE = re.compile(r'</p>')
DIV_OPEN = re.compile(r'<div\s+class="(?:formula|table caption|table)"\s+data-bbox="[^"]*">')
DIV_CLOSE = re.compile(r'</div>')
IMG_BBOX = re.compile(r'<img\s+data-bbox="[^"]*"\s*/?>')
MULTI_BLANK = re.compile(r'\n{3,}')


def clean_text(s: str) -> str:
    s = P_OPEN.sub('', s)
    s = P_CLOSE.sub('\n', s)
    s = DIV_OPEN.sub('', s)
    s = DIV_CLOSE.sub('\n', s)
    s = IMG_BBOX.sub('', s)
    s = MULTI_BLANK.sub('\n\n', s)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--dst', required=True)
    args = ap.parse_args()

    os.makedirs(args.dst, exist_ok=True)
    files = sorted(f for f in os.listdir(args.src) if f.endswith('.md'))
    print(f"[clean] {len(files)} .md files in {args.src}")
    n_changed = n_unchanged = 0
    sample_before = sample_after = None
    for fn in files:
        with open(os.path.join(args.src, fn), 'r', encoding='utf-8') as f:
            raw = f.read()
        cleaned = clean_text(raw)
        if cleaned != raw:
            n_changed += 1
            if sample_before is None:
                sample_before, sample_after = raw[:400], cleaned[:400]
        else:
            n_unchanged += 1
        with open(os.path.join(args.dst, fn), 'w', encoding='utf-8') as f:
            f.write(cleaned)

    print(f"[clean] wrote {len(files)} files to {args.dst}")
    print(f"[clean] changed={n_changed} unchanged={n_unchanged}")
    if sample_before is not None:
        print("\n=== sample BEFORE (400 chars) ===")
        print(sample_before)
        print("\n=== sample AFTER (400 chars) ===")
        print(sample_after)


if __name__ == '__main__':
    main()
