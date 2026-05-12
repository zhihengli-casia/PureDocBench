#!/usr/bin/env python3
"""Clean DeepSeek-OCR markdown predictions for PureDocBench scoring.

The cleaner is intentionally conservative: it removes model/chat wrapper tags
and only strips code fences when they wrap the whole file. Internal markdown
fences are preserved.
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

REAL_SUFFIX_RE = re.compile(r"__real_.*$")
SPECIAL_TOKEN_RE = re.compile(r"<\|[^>]{0,80}\|>|<｜[^>]{0,80}｜>")
THINK_RE = re.compile(r"<think>.*?</think>", re.IGNORECASE | re.DOTALL)
ROLE_LINE_RE = re.compile(r"^\s*(?:assistant|user|system)\s*:\s*$", re.IGNORECASE)
FENCE_RE = re.compile(r"^\s*```(?:markdown|md|text)?\s*$", re.IGNORECASE)
HTML_WRAPPER_RE = re.compile(r"^\s*</?(?:html|body|document|markdown)>\s*$", re.IGNORECASE)


def _strip_outer_fences(text: str) -> str:
    lines = text.splitlines()
    if not lines:
        return text

    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    if start >= end:
        return ""

    # Remove one or more wrapper fences at file boundaries. Do not touch
    # internal fences such as SQL/Python listings.
    changed = True
    while changed and start < end:
        changed = False
        if FENCE_RE.match(lines[start]):
            start += 1
            changed = True
            while start < end and not lines[start].strip():
                start += 1
        if end > start and FENCE_RE.match(lines[end - 1]):
            end -= 1
            changed = True
            while end > start and not lines[end - 1].strip():
                end -= 1
    return "\n".join(lines[start:end]).strip() + "\n"


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    text = THINK_RE.sub("\n", text)
    text = SPECIAL_TOKEN_RE.sub("", text)
    lines = []
    for line in text.split("\n"):
        if ROLE_LINE_RE.match(line):
            continue
        if HTML_WRAPPER_RE.match(line):
            continue
        lines.append(line)
    text = "\n".join(lines)
    text = _strip_outer_fences(text)
    # Trim excessive blank lines introduced by wrapper removal while preserving
    # paragraph breaks.
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip() + "\n"


def normalized_name(path: Path) -> str:
    return REAL_SUFFIX_RE.sub("", path.stem) + ".md"


def clean_dir(src: Path, dst: Path, *, overwrite: bool = False) -> None:
    if not src.is_dir():
        raise FileNotFoundError(f"source directory not found: {src}")
    if dst.exists():
        if not overwrite:
            raise FileExistsError(f"destination exists: {dst}")
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    seen = set()
    changed = 0
    for f in sorted(src.glob("*.md")):
        out_name = normalized_name(f)
        if out_name in seen:
            raise RuntimeError(f"duplicate normalized filename: {out_name}")
        seen.add(out_name)
        raw = f.read_text(encoding="utf-8", errors="ignore")
        cleaned = clean_text(raw)
        if cleaned != raw:
            changed += 1
        (dst / out_name).write_text(cleaned, encoding="utf-8")
    print(f"source_md={len(seen)} changed_files={changed} output={dst}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, type=Path)
    ap.add_argument("--dst", required=True, type=Path)
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()
    clean_dir(args.src, args.dst, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
