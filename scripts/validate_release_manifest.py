#!/usr/bin/env python3
"""Validate that a reconstructed PureDocBench release matches a manifest."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED_COLUMNS = {
    "page_id",
    "gt_rel",
    "html_rel",
    "clean_rel",
    "digital_rel",
    "real_rel",
}


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit(f"Manifest is empty: {path}")
    missing = REQUIRED_COLUMNS - set(rows[0])
    if missing:
        raise SystemExit(f"Manifest missing columns: {sorted(missing)}")
    return rows


def check_gt(path: Path) -> tuple[bool, str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"invalid JSON: {exc}"
    if "layout_dets" not in payload or "page_info" not in payload:
        return False, "missing layout_dets or page_info"
    layout = payload["layout_dets"]
    if not isinstance(layout, list):
        return False, "layout_dets is not a list"
    anno_ids = [item.get("anno_id") for item in layout if isinstance(item, dict)]
    if anno_ids != list(range(len(anno_ids))):
        return False, "anno_id sequence is not contiguous from 0"
    return True, ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()

    rows = read_manifest(args.manifest)
    missing: list[str] = []
    bad_gt: list[str] = []

    for row in rows:
        paths = [
            args.release_root / "gt" / row["gt_rel"],
            args.release_root / "html" / row["html_rel"],
            args.release_root / "images" / "clean" / row["clean_rel"],
            args.release_root / "images" / "digital_degraded" / row["digital_rel"],
            args.release_root / "images" / "real_degraded" / row["real_rel"],
        ]
        for path in paths:
            if not path.exists():
                missing.append(str(path))

        gt_path = args.release_root / "gt" / row["gt_rel"]
        if gt_path.exists():
            ok, reason = check_gt(gt_path)
            if not ok:
                bad_gt.append(f"{gt_path}: {reason}")

    if missing or bad_gt:
        if missing:
            print(f"Missing files: {len(missing)}")
            for item in missing[:50]:
                print(item)
        if bad_gt:
            print(f"Bad GT files: {len(bad_gt)}")
            for item in bad_gt[:50]:
                print(item)
        raise SystemExit(2)

    print(f"OK: {len(rows)} manifest rows validated.")


if __name__ == "__main__":
    main()
