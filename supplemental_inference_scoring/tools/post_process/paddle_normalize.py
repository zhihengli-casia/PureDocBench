#!/usr/bin/env python3
r"""Post-process PaddleOCR-VL pipeline outputs to align with PureDocBench GT.

Paddle pipeline emits LaTeX-wrapped daggers, sub/superscripts and tables with
loose spacing/style attributes. The GT mixes plain unicode (†, ‡, ⁻¹, ²) with
selective LaTeX (`E_a`, `\Delta G^{\ddagger}`). Normalising paddle outputs
toward this convention reduces edit distance significantly without touching
true display formulas.

Rules applied (in order):
  1. Strip whitespace inside `$ ... $` and `$$ ... $$` blocks
  2. Replace simple LaTeX commands with unicode (\dagger, \ddagger, \pm, etc.)
  3. Convert digit/sign sub/superscripts to unicode (`^{1-3}` -> `¹⁻³`)
  4. Table fix: add `border="1"` if missing; first <tr>'s <td> -> <th>
  5. Keep complex math ($$...$$) and letter sub/superscripts intact

Usage:
  python paddle_normalize.py SRC_DIR DST_DIR
"""
import argparse
import os
import re
import sys
from pathlib import Path

SUPER = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
    "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
    "+": "⁺", "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾", ",": ",",
}
SUB = {
    "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄",
    "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉",
    "+": "₊", "-": "₋", "=": "₌", "(": "₍", ")": "₎",
}

SIMPLE_CMDS = {
    r"\dagger": "†",
    r"\ddagger": "‡",
    r"\pm": "±",
    r"\mp": "∓",
    r"\times": "×",
    r"\div": "÷",
    r"\cdot": "·",
    r"\le": "≤",
    r"\leq": "≤",
    r"\ge": "≥",
    r"\geq": "≥",
    r"\ne": "≠",
    r"\neq": "≠",
    r"\approx": "≈",
    r"\to": "→",
    r"\rightarrow": "→",
    r"\leftarrow": "←",
    r"\Rightarrow": "⇒",
    r"\Leftarrow": "⇐",
    r"\infty": "∞",
    r"\partial": "∂",
    r"\nabla": "∇",
    r"\sum": "∑",
    r"\prod": "∏",
    r"\int": "∫",
    r"\sqrt": "√",
    r"\degree": "°",
    r"\circ": "∘",
    r"\bullet": "•",
    r"\ldots": "…",
    r"\cdots": "…",
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ",
    r"\epsilon": "ε", r"\zeta": "ζ", r"\eta": "η", r"\theta": "θ",
    r"\iota": "ι", r"\kappa": "κ", r"\lambda": "λ", r"\mu": "μ",
    r"\nu": "ν", r"\xi": "ξ", r"\pi": "π", r"\rho": "ρ",
    r"\sigma": "σ", r"\tau": "τ", r"\upsilon": "υ", r"\phi": "φ",
    r"\chi": "χ", r"\psi": "ψ", r"\omega": "ω",
    r"\Gamma": "Γ", r"\Delta": "Δ", r"\Theta": "Θ", r"\Lambda": "Λ",
    r"\Xi": "Ξ", r"\Pi": "Π", r"\Sigma": "Σ", r"\Phi": "Φ",
    r"\Psi": "Ψ", r"\Omega": "Ω",
}


def to_super(content):
    out = []
    for ch in content:
        if ch in SUPER:
            out.append(SUPER[ch])
        else:
            return None
    return "".join(out)


def to_sub(content):
    out = []
    for ch in content:
        if ch in SUB:
            out.append(SUB[ch])
        else:
            return None
    return "".join(out)


def replace_simple_super(text):
    def _sub(m):
        u = to_super(m.group(1))
        return u if u is not None else m.group(0)
    return re.sub(r"\^\{([^{}]+)\}", _sub, text)


def replace_simple_sub(text):
    def _sub(m):
        u = to_sub(m.group(1))
        return u if u is not None else m.group(0)
    return re.sub(r"_\{([^{}]+)\}", _sub, text)


def replace_simple_cmds(text):
    # Use word boundary so \le doesnt grab \left, \sum doesnt grab \sumlimits, etc.
    for cmd in sorted(SIMPLE_CMDS.keys(), key=lambda k: -len(k)):
        # \cmd must not be followed by a letter
        pattern = re.escape(cmd) + r"(?![a-zA-Z])"
        text = re.sub(pattern, SIMPLE_CMDS[cmd].replace("\\", "\\\\"), text)
    return text


def strip_inline_dollar_spaces(text):
    # Display math: only strip leading/trailing spaces inside, NO newlines crossed.
    text = re.sub(r"\$\$[ \t]+([^$\n]*?)[ \t]+\$\$", r"$$\1$$", text)
    text = re.sub(r"\$[ \t]+([^$\n]*?)[ \t]+\$", r"$\1$", text)
    return text


def normalize_inside_dollars(text):
    def _process(content):
        content = replace_simple_cmds(content)
        content = replace_simple_super(content)
        content = replace_simple_sub(content)
        return content

    def _sub_display(m):
        return f"$${_process(m.group(1))}$$"
    text = re.sub(r"\$\$([^$]+?)\$\$", _sub_display, text, flags=re.DOTALL)

    def _sub_inline(m):
        inner = _process(m.group(1))
        if not any(c in inner for c in ("\\", "{", "}", "^", "_")):
            return inner
        return f"${inner}$"
    text = re.sub(r"(?<!\$)\$([^$\n]+?)\$(?!\$)", _sub_inline, text)
    return text


def fix_table_html(text):
    def _fix_table(m):
        body = m.group(0)
        if "<table>" in body[:50]:
            body = body.replace("<table>", '<table border="1">', 1)
        first_tr = re.search(r"<tr>(.*?)</tr>", body, flags=re.DOTALL)
        if first_tr:
            row = first_tr.group(1)
            row = re.sub(r"<td(\s[^>]*)?>", "<th>", row)
            row = row.replace("</td>", "</th>")
            body = body[:first_tr.start(1)] + row + body[first_tr.end(1):]
        return body
    return re.sub(r"<table[^>]*>.*?</table>", _fix_table, text, flags=re.DOTALL)


def normalize(text):
    text = strip_inline_dollar_spaces(text)
    text = normalize_inside_dollars(text)
    text = fix_table_html(text)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    args = ap.parse_args()
    args.dst.mkdir(parents=True, exist_ok=True)
    files = sorted(args.src.glob("*.md"))
    print(f"normalizing {len(files)} files: {args.src} -> {args.dst}")
    for f in files:
        out = normalize(f.read_text(encoding="utf-8"))
        (args.dst / f.name).write_text(out, encoding="utf-8")
    print(f"done; written {len(files)} files")


if __name__ == "__main__":
    sys.exit(main())
