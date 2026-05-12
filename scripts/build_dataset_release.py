#!/usr/bin/env python3
"""Build a clean PureDocBench dataset release from a manifest.

This script copies only files listed in a manifest CSV. It intentionally avoids
raw directory crawls because the active dataset tree contains backups and unused
working files.
"""

from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-root",
        required=True,
        type=Path,
        help="PureDocBench_eval source root on the server.",
    )
    parser.add_argument(
        "--manifest",
        required=True,
        type=Path,
        help="Release or sample manifest CSV.",
    )
    parser.add_argument(
        "--output-root",
        required=True,
        type=Path,
        help="Output directory for the clean release package.",
    )
    parser.add_argument(
        "--dataset-card",
        type=Path,
        help="Optional DATASET_CARD.md draft to copy into the release root.",
    )
    parser.add_argument(
        "--sample-readme",
        type=Path,
        help="Optional README.md to copy into sample releases.",
    )
    parser.add_argument(
        "--metadata-dir",
        type=Path,
        help="Optional directory containing LICENSE, Croissant, and Kaggle metadata templates.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check expected files without copying.",
    )
    return parser.parse_args()


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit(f"Manifest is empty: {path}")
    required = {
        "page_id",
        "gt_rel",
        "html_rel",
        "clean_rel",
        "digital_rel",
        "real_rel",
    }
    missing = required - set(rows[0])
    if missing:
        raise SystemExit(f"Manifest missing columns: {sorted(missing)}")
    return rows


def copy_file(src: Path, dst: Path, dry_run: bool) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    if dry_run:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_manifest(rows: list[dict[str, str]], out_path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    rows = read_manifest(args.manifest)

    copies: list[tuple[Path, Path]] = []
    for row in rows:
        copies.extend(
            [
                (
                    args.source_root / "gt" / row["gt_rel"],
                    args.output_root / "gt" / row["gt_rel"],
                ),
                (
                    args.source_root / "html" / row["html_rel"],
                    args.output_root / "html" / row["html_rel"],
                ),
                (
                    args.source_root / "images" / row["clean_rel"],
                    args.output_root / "images" / "clean" / row["clean_rel"],
                ),
                (
                    args.source_root / "degraded_v2_merged" / row["digital_rel"],
                    args.output_root / "images" / "digital_degraded" / row["digital_rel"],
                ),
                (
                    args.source_root / "real_degraded" / row["real_rel"],
                    args.output_root / "images" / "real_degraded" / row["real_rel"],
                ),
            ]
        )

    missing: list[str] = []
    for src, _ in copies:
        if not src.exists():
            missing.append(str(src))

    if missing:
        print(f"Missing files: {len(missing)}")
        for item in missing[:50]:
            print(item)
        raise SystemExit(2)

    for src, dst in copies:
        copy_file(src, dst, args.dry_run)

    manifest_name = "release_manifest_1475.csv" if len(rows) > 100 else "sample_manifest_66.csv"
    write_manifest(rows, args.output_root / "manifests" / manifest_name, args.dry_run)

    if args.dataset_card:
        copy_file(args.dataset_card, args.output_root / "DATASET_CARD.md", args.dry_run)
    if args.sample_readme:
        copy_file(args.sample_readme, args.output_root / "README.md", args.dry_run)
    if args.metadata_dir:
        optional_files = [
            ("LICENSE", "LICENSE"),
            ("croissant_puredocbench_draft.json", "croissant.json"),
            ("kaggle_dataset_metadata.template.json", "dataset-metadata.template.json"),
        ]
        for src_name, dst_name in optional_files:
            src = args.metadata_dir / src_name
            if src.exists():
                copy_file(src, args.output_root / dst_name, args.dry_run)

    print("mode:", "dry-run" if args.dry_run else "copy")
    print("pages:", len(rows))
    print("files checked:", len(copies))
    print("output:", args.output_root)


if __name__ == "__main__":
    main()
