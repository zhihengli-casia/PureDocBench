#!/usr/bin/env python3
"""Post-process PaddleOCR-VL markdown outputs for PureDocBench scoring.

This is intentionally prediction-only cleanup: no GT lookup. It removes markup
that Paddle emits but the benchmark generally does not score as document text,
and normalizes common HTML/LaTeX surface forms to the evaluator's convention.
"""
import argparse
import os
import html
import re
import sys
from pathlib import Path

FENCE_RE = re.compile(r"^\s*```(?:markdown|md)?\s*\n(.*?)\n```\s*$", re.DOTALL | re.IGNORECASE)
ASSISTANT_RE = re.compile(r"^\s*(?:assistant\s*:|assistant\s*\n)", re.IGNORECASE)
IMG_BLOCK_RE = re.compile(r"\s*<div[^>]*>\s*<img\b[^>]*?/?>\s*</div>\s*", re.IGNORECASE)
IMG_RE = re.compile(r"\s*<img\b[^>]*?/?>\s*", re.IGNORECASE)
DIV_OPEN_RE = re.compile(r"<div\b[^>]*>", re.IGNORECASE)
DIV_CLOSE_RE = re.compile(r"</div>", re.IGNORECASE)
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
MULTI_BLANK_RE = re.compile(r"\n{3,}")

SUPER = {
    "0": "?", "1": "?", "2": "?", "3": "?", "4": "?", "5": "?", "6": "?", "7": "?", "8": "?", "9": "?",
    "+": "?", "-": "?", "=": "?", "(": "?", ")": "?", ",": ",",
}
SUB = {
    "0": "?", "1": "?", "2": "?", "3": "?", "4": "?", "5": "?", "6": "?", "7": "?", "8": "?", "9": "?",
    "+": "?", "-": "?", "=": "?", "(": "?", ")": "?",
}
SIMPLE_CMDS = {
    r"\dagger": "?", r"\ddagger": "?", r"\pm": "?", r"\mp": "?", r"\times": "?", r"\div": "?", r"\cdot": "?",
    r"\leq": "?", r"\le": "?", r"\geq": "?", r"\ge": "?", r"\neq": "?", r"\ne": "?", r"\approx": "?",
    r"\rightarrow": "?", r"\to": "?", r"\leftarrow": "?", r"\Rightarrow": "?", r"\Leftarrow": "?",
    r"\infty": "?", r"\partial": "?", r"\nabla": "?", r"\sum": "?", r"\prod": "?", r"\int": "?",
    r"\degree": "?", r"\circ": "?", r"\bullet": "?", r"\ldots": "?", r"\cdots": "?",
    r"\alpha": "?", r"\beta": "?", r"\gamma": "?", r"\delta": "?", r"\epsilon": "?", r"\theta": "?",
    r"\lambda": "?", r"\mu": "?", r"\pi": "?", r"\rho": "?", r"\sigma": "?", r"\omega": "?",
    r"\Delta": "?", r"\Gamma": "?", r"\Theta": "?", r"\Lambda": "?", r"\Omega": "?",
}


def chars_map(content: str, mapping: dict[str, str]) -> str | None:
    out = []
    for ch in content:
        if ch not in mapping:
            return None
        out.append(mapping[ch])
    return "".join(out)


def replace_simple_cmds(text: str) -> str:
    for cmd in sorted(SIMPLE_CMDS, key=len, reverse=True):
        text = re.sub(re.escape(cmd) + r"(?![a-zA-Z])", SIMPLE_CMDS[cmd], text)
    return text


def normalize_math_surface(text: str) -> str:
    def process(content: str) -> str:
        content = replace_simple_cmds(content.strip())
        content = re.sub(r"\^\{([^{}]+)\}", lambda m: chars_map(m.group(1), SUPER) or m.group(0), content)
        content = re.sub(r"_\{([^{}]+)\}", lambda m: chars_map(m.group(1), SUB) or m.group(0), content)
        return content

    text = re.sub(r"\$\$\s*([^$]+?)\s*\$\$", lambda m: f"$${process(m.group(1))}$$", text, flags=re.DOTALL)

    def inline(m):
        inner = process(m.group(1))
        if not any(ch in inner for ch in "\\{}^_"):
            return inner
        return f"${inner}$"
    return re.sub(r"(?<!\$)\$([^$\n]+?)\$(?!\$)", inline, text)


def fix_tables(text: str) -> str:
    for r in ATTR_RES:
        text = r.sub("", text)
    text = BORDER_NO_QUOTE_RE.sub(r'\1"\2"', text)
    text = re.sub(r"<table\s*>", '<table border="1">', text, flags=re.IGNORECASE)

    def fix_one(m):
        body = m.group(0)
        first = re.search(r"<tr>(.*?)</tr>", body, flags=re.DOTALL | re.IGNORECASE)
        if not first:
            return body
        row = first.group(1)
        # Paddle often serializes header rows as td; PureDocBench GT uses th for header cells.
        if "<th" not in row.lower():
            row = re.sub(r"<td(\s[^>]*)?>", r"<th\1>", row, flags=re.IGNORECASE)
            row = re.sub(r"</td>", "</th>", row, flags=re.IGNORECASE)
            body = body[:first.start(1)] + row + body[first.end(1):]
        return body
    return re.sub(r"<table[^>]*>.*?</table>", fix_one, text, flags=re.DOTALL | re.IGNORECASE)


def clean_text(text: str) -> str:
    text = text.replace("\x00", "")
    m = FENCE_RE.match(text)
    if m:
        text = m.group(1)
    text = ASSISTANT_RE.sub("", text)
    text = html.unescape(text)
    text = IMG_BLOCK_RE.sub("\n", text)
    text = IMG_RE.sub("", text)
    text = DIV_OPEN_RE.sub("", text)
    text = DIV_CLOSE_RE.sub("", text)
    text = fix_tables(text)
    text = normalize_math_surface(text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = MULTI_BLANK_RE.sub("\n\n", text)
    text = text.strip()
    return text + ("\n" if text else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--dst", type=Path, required=True)
    args = ap.parse_args()
    args.dst.mkdir(parents=True, exist_ok=True)
    files = sorted(args.src.glob("*.md"))
    changed = empty = tiny = 0
    bytes_before = bytes_after = 0
    for f in files:
        raw = f.read_text(encoding="utf-8", errors="ignore")
        out = clean_text(raw)
        changed += int(out != raw)
        empty += int(not out.strip())
        tiny += int(0 < len(out.strip()) < 20)
        bytes_before += len(raw)
        bytes_after += len(out)
        (args.dst / f.name).write_text(out, encoding="utf-8")
    print(f"[paddle_align] src={args.src} dst={args.dst} files={len(files)} changed={changed} empty={empty} tiny_lt20={tiny} bytes={bytes_before}->{bytes_after}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
