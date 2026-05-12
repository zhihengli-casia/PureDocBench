#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

FORBIDDEN = [
    "assistant:",
    "assistant\n",
    "<think>",
    "i cannot",
    "i can't",
    "sorry",
]

def summarize(text: str, width: int = 90) -> str:
    text = " ".join(text.split())
    return text[:width] + ("..." if len(text) > width else "")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pred_dir")
    ap.add_argument("--expected", type=int, default=5)
    ap.add_argument("--min-len", type=int, default=50)
    args = ap.parse_args()

    pred_dir = Path(args.pred_dir)
    files = sorted(pred_dir.glob("*.md"))
    if len(files) < args.expected:
        print(f"SMOKE_FAIL md_count={len(files)} expected>={args.expected}")
        return 2

    digests = []
    for md in files[: args.expected]:
        text = md.read_text(encoding="utf-8", errors="ignore").strip()
        digest = hashlib.sha1(text.encode("utf-8")).hexdigest()
        digests.append(digest)
        low = text.lower()
        if len(text) < args.min_len:
            print(f"SMOKE_FAIL short {md.name} len={len(text)}")
            return 2
        if any(x in low for x in FORBIDDEN):
            print(f"SMOKE_FAIL forbidden {md.name}")
            return 2
        print(f"SMOKE_SAMPLE {md.name} len={len(text)} :: {summarize(text)}")

    unique_ratio = len(set(digests)) / max(len(digests), 1)
    if unique_ratio < 0.8:
        print(f"SMOKE_FAIL duplicate_ratio={1 - unique_ratio:.2f}")
        return 2

    print(f"SMOKE_PASS files={args.expected} unique_ratio={unique_ratio:.2f}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
