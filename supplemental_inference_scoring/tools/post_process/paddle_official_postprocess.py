#!/usr/bin/env python3
"""Conservative PaddleOCR-VL markdown post-process for official reruns.

No GT access. Only removes format noise known to hurt Markdown/HTML matching:
HTML entities, style/class/layout-only table attrs, markdown fences, assistant
prefixes, excessive blank lines, and simple Paddle table tag quirks.
"""
import argparse
import html
import re
import sys
from pathlib import Path

FENCE_RE = re.compile(r'^\s*```(?:markdown|md)?\s*\n(.*?)\n```\s*$', re.DOTALL | re.IGNORECASE)
ASSISTANT_RE = re.compile(r'^\s*(?:assistant\s*:|assistant\s*\n)', re.IGNORECASE)
ATTR_RES = [
    re.compile(r"\s+style\s*=\s*(['\"])[^'\"]*\1", re.IGNORECASE),
    re.compile(r"\s+class\s*=\s*(['\"])[^'\"]*\1", re.IGNORECASE),
    re.compile(r"\s+align\s*=\s*(['\"])[^'\"]*\1", re.IGNORECASE),
    re.compile(r"\s+width\s*=\s*(['\"]?\d+%?['\"]?)", re.IGNORECASE),
    re.compile(r"\s+height\s*=\s*(['\"]?\d+%?['\"]?)", re.IGNORECASE),
    re.compile(r"\s+cellspacing\s*=\s*(['\"]?\d+['\"]?)", re.IGNORECASE),
    re.compile(r"\s+cellpadding\s*=\s*(['\"]?\d+['\"]?)", re.IGNORECASE),
]
BORDER_NO_QUOTE_RE = re.compile(r"(\s+border\s*=)\s*(\d+)(?!['\"])", re.IGNORECASE)
MULTI_BLANK_RE = re.compile(r'\n{3,}')


def clean_text(text: str) -> str:
    text = text.replace('\x00', '')
    m = FENCE_RE.match(text)
    if m:
        text = m.group(1)
    text = ASSISTANT_RE.sub('', text)
    text = html.unescape(text)
    for r in ATTR_RES:
        text = r.sub('', text)
    text = BORDER_NO_QUOTE_RE.sub(r'\1"\2"', text)
    text = re.sub(r'<table\s*>', '<table border="1">', text, flags=re.IGNORECASE)
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = MULTI_BLANK_RE.sub('\n\n', text)
    return text.strip() + ('\n' if text.strip() else '')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', type=Path, required=True)
    ap.add_argument('--dst', type=Path, required=True)
    args = ap.parse_args()
    args.dst.mkdir(parents=True, exist_ok=True)
    files = sorted(args.src.glob('*.md'))
    changed = 0
    empty = tiny = 0
    bytes_before = bytes_after = 0
    for f in files:
        raw = f.read_text(encoding='utf-8', errors='ignore')
        out = clean_text(raw)
        if out != raw:
            changed += 1
        if not out.strip():
            empty += 1
        if len(out.strip()) < 20:
            tiny += 1
        bytes_before += len(raw)
        bytes_after += len(out)
        (args.dst / f.name).write_text(out, encoding='utf-8')
    print(f'[paddle_pp] src={args.src} dst={args.dst} files={len(files)} changed={changed} empty={empty} tiny_lt20={tiny} bytes={bytes_before}->{bytes_after}', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
