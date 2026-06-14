#!/usr/bin/env python3
"""Package versioned GT bbox annotations for Hugging Face dataset release."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_REVIEW_DIR = Path(
    "/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_gzip_json(source: Path, target: Path) -> None:
    with source.open("rb") as src, gzip.open(target, "wb", compresslevel=9) as dst:
        shutil.copyfileobj(src, dst)


def json_load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_matching_reports(review_dir: Path, token: str) -> list[Path]:
    reports_dir = review_dir / "reports"
    matches: list[Path] = []
    if not reports_dir.exists():
        return matches
    for path in sorted(reports_dir.glob("*.json")):
        try:
            report = json_load(path)
        except Exception:
            continue
        if not isinstance(report, dict):
            continue
        if report.get("token") == token or report.get("new_token") == token:
            matches.append(path)
    return matches


def file_entry(path: Path, base_dir: Path) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(base_dir)),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def package_release(
    review_dir: Path,
    out_root: Path,
    token: str | None,
    public_version: str | None,
    dataset_version: str,
    write_latest: bool,
) -> dict[str, Any]:
    review_json = review_dir / "review_data.json"
    repair_log = review_dir / "GT_REPAIR_LOG.md"
    if not review_json.exists():
        raise FileNotFoundError(review_json)
    if not repair_log.exists():
        raise FileNotFoundError(repair_log)

    data = json_load(review_json)
    metadata = data.get("meta", {})
    internal_token = token or metadata.get("internal_build_token") or metadata.get("build_token") or metadata.get("created_at")
    if not internal_token:
        raise ValueError("Could not infer annotation token from review_data.json")
    annotation_version = public_version or metadata.get("public_annotation_version") or internal_token

    release_dir = out_root / annotation_version
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True)

    data_gz = release_dir / "review_data.json.gz"
    write_gzip_json(review_json, data_gz)
    shutil.copy2(repair_log, release_dir / "GT_REPAIR_LOG.md")
    repo_root = review_dir.parent.parent
    correction_guide = repo_root / "docs" / "ANNOTATION_CORRECTIONS.md"
    copied_guide = None
    if correction_guide.exists():
        guide_target = release_dir / "docs" / "ANNOTATION_CORRECTIONS.md"
        guide_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(correction_guide, guide_target)
        copied_guide = guide_target

    report_paths = collect_matching_reports(review_dir, internal_token)
    copied_reports: list[Path] = []
    if report_paths:
        report_dir = release_dir / "reports"
        report_dir.mkdir()
        for report_path in report_paths:
            target = report_dir / report_path.name
            shutil.copy2(report_path, target)
            copied_reports.append(target)

    cases = data.get("cases", [])
    manifest = {
        "annotation_version": annotation_version,
        "annotation_version_label": metadata.get("public_annotation_version_label") or annotation_version,
        "internal_build_token": internal_token,
        "source_annotation_token": internal_token,
        "base_dataset_version": dataset_version,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_review_dir": str(review_dir),
        "data_file": "review_data.json.gz",
        "repair_log": "GT_REPAIR_LOG.md",
        "reports": [str(path.relative_to(release_dir)) for path in copied_reports],
        "stats": {
            "total_cases": metadata.get("case_count") or metadata.get("total_cases") or len(cases),
            "total_annotations": metadata.get("total_items"),
            "boxed_annotations": metadata.get("items_with_bbox"),
            "no_bbox_annotations": metadata.get("items_unmatched"),
            "low_similarity_annotations": metadata.get("items_low_similarity"),
        },
        "split_policy": {
            "stable_split": "recommended: fixed 70% core cases",
            "rolling_split": "recommended: periodically refreshed 30% cases",
            "note": "Scores should cite the exact annotation_version, not only latest.",
        },
        "community_corrections": {
            "schema_version": "puredocbench-gt-correction-patch-v1",
            "guide": str(copied_guide.relative_to(release_dir)) if copied_guide else "docs/ANNOTATION_CORRECTIONS.md",
            "github_repo": "https://github.com/zhihengli-casia/PureDocBench",
        },
    }

    manifest_path = release_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    release_readme = release_dir / "README.md"
    release_readme.write_text(
        "\n".join(
            [
                f"# PureDocBench GT BBox {annotation_version}",
                "",
                "This directory is a versioned GT bounding-box annotation release for Hugging Face.",
                f"The public annotation version is `{annotation_version}`.",
                f"The maintainer-only repair provenance token is `{internal_token}`.",
                "",
                "- `review_data.json.gz`: compressed review data with GT annotations.",
                "- `manifest.json`: version, statistics, and file checksums.",
                "- `GT_REPAIR_LOG.md`: human-readable repair history.",
                "- `reports/`: machine-readable repair reports for this token when available.",
                "",
                "Evaluation reports should cite this exact `annotation_version`.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    checksums = {
        "annotation_version": annotation_version,
        "internal_build_token": internal_token,
        "files": [
            file_entry(path, release_dir)
            for path in sorted(release_dir.rglob("*"))
            if path.is_file() and path.name != "checksums.json"
        ],
    }
    checksums_path = release_dir / "checksums.json"
    checksums_path.write_text(json.dumps(checksums, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if write_latest:
        latest_dir = out_root / "latest"
        if latest_dir.exists():
            shutil.rmtree(latest_dir)
        latest_dir.mkdir(parents=True)
        shutil.copy2(manifest_path, latest_dir / "manifest.json")
        shutil.copy2(data_gz, latest_dir / "review_data.json.gz")
        latest_pointer = {
            "annotation_version": annotation_version,
            "internal_build_token": internal_token,
            "source_annotation_token": internal_token,
            "manifest": "manifest.json",
            "data_file": "review_data.json.gz",
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        (latest_dir / "latest.json").write_text(
            json.dumps(latest_pointer, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return {
        "annotation_version": annotation_version,
        "internal_build_token": internal_token,
        "release_dir": str(release_dir),
        "latest_dir": str(out_root / "latest") if write_latest else None,
        "stats": manifest["stats"],
        "files": checksums["files"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-dir", type=Path, default=DEFAULT_REVIEW_DIR)
    parser.add_argument("--out-root", type=Path, default=Path("dist/hf_gt_bbox"))
    parser.add_argument("--token", help="Internal repair/build token. Defaults to review_data.json meta.")
    parser.add_argument("--public-version", help="Community-facing annotation version, e.g. puredocbench-gt-bbox-v1.0.0.")
    parser.add_argument("--dataset-version", default="puredocbench-v1.0")
    parser.add_argument("--write-latest", action="store_true")
    args = parser.parse_args()

    result = package_release(
        review_dir=args.review_dir,
        out_root=args.out_root,
        token=args.token,
        public_version=args.public_version,
        dataset_version=args.dataset_version,
        write_latest=args.write_latest,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
