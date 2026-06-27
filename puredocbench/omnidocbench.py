from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from .common import read_json, read_manifest, track_column, write_json
from .scoring import build_prediction_index

try:
    import yaml
except Exception:  # pragma: no cover - optional dependency fallback
    yaml = None  # type: ignore[assignment]


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    if yaml is not None:
        path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
        return

    dataset = payload["end2end_eval"]["dataset"]
    text = f"""end2end_eval:
  metrics:
    text_block:
      metric: [Edit_dist]
    display_formula:
      metric: [Edit_dist, CDM]
    table:
      metric: [TEDS, Edit_dist]
    reading_order:
      metric: [Edit_dist]
  dataset:
    dataset_name: {dataset["dataset_name"]}
    ground_truth:
      data_path: {dataset["ground_truth"]["data_path"]}
    prediction:
      data_path: {dataset["prediction"]["data_path"]}
    match_method: {dataset["match_method"]}
    match_workers: {dataset["match_workers"]}
"""
    path.write_text(text, encoding="utf-8")


def _ensure_omnidocbench_relation(gt_payload: dict[str, Any]) -> None:
    extra = gt_payload.get("extra")
    if not isinstance(extra, dict):
        extra = {}
        gt_payload["extra"] = extra

    if not isinstance(extra.get("relation"), list):
        extra["relation"] = []


def export_omnidocbench(
    release_root: Path,
    manifest_path: Path,
    pred_dir: Path,
    out_dir: Path,
    track: str = "clean",
    limit: int | None = None,
    strict: bool = False,
    match_workers: int = 8,
) -> dict[str, Any]:
    rows = read_manifest(manifest_path)
    if limit is not None:
        rows = rows[:limit]
    column = track_column(track)
    pred_index = build_prediction_index(pred_dir)

    gt_out: list[dict[str, Any]] = []
    pred_out = out_dir / "predictions"
    pred_out.mkdir(parents=True, exist_ok=True)
    missing: list[str] = []

    for row in rows:
        gt_payload = read_json(release_root / "gt" / row["gt_rel"])
        gt_payload.setdefault("page_info", {})["image_path"] = row[column]
        _ensure_omnidocbench_relation(gt_payload)
        gt_out.append(gt_payload)

        pred_name = Path(row[column]).with_suffix(".md").name
        candidates = [
            Path(row[column]).with_suffix(".md").as_posix(),
            pred_name,
            Path(row[column]).stem,
            Path(row["clean_rel"]).with_suffix(".md").as_posix(),
            Path(row["clean_rel"]).with_suffix(".md").name,
            Path(row["clean_rel"]).stem,
            Path(row["page_id"]).name,
        ]
        src = next((pred_index[key] for key in candidates if key in pred_index), None)
        if src is None:
            missing.append(row["page_id"])
            if strict:
                continue
            (pred_out / pred_name).write_text("", encoding="utf-8")
        else:
            shutil.copyfile(src, pred_out / pred_name)

    if strict and missing:
        raise SystemExit(f"missing {len(missing)} predictions; first missing page_id: {missing[0]}")

    gt_path = out_dir / "gt.json"
    write_json(gt_path, gt_out)
    config = {
        "end2end_eval": {
            "metrics": {
                "text_block": {"metric": ["Edit_dist"]},
                "display_formula": {"metric": ["Edit_dist", "CDM"]},
                "table": {"metric": ["TEDS", "Edit_dist"]},
                "reading_order": {"metric": ["Edit_dist"]},
            },
            "dataset": {
                "dataset_name": "end2end_dataset",
                "ground_truth": {"data_path": str(gt_path.resolve())},
                "prediction": {"data_path": str(pred_out.resolve())},
                "match_method": "quick_match",
                "match_workers": match_workers,
            },
        }
    }
    config_path = out_dir / "omnidocbench_config.yaml"
    _write_yaml(config_path, config)
    return {
        "gt_json": str(gt_path),
        "predictions": str(pred_out),
        "config": str(config_path),
        "pages": len(rows),
        "missing_predictions": len(missing),
    }


def run_omnidocbench_score(
    release_root: Path,
    manifest_path: Path,
    pred_dir: Path,
    out_dir: Path,
    track: str = "clean",
    limit: int | None = None,
    strict: bool = False,
    omnidocbench_root: Path | None = None,
    python_bin: str | None = None,
    match_workers: int = 8,
    export_only: bool = False,
) -> dict[str, Any]:
    export_result = export_omnidocbench(
        release_root=release_root,
        manifest_path=manifest_path,
        pred_dir=pred_dir,
        out_dir=out_dir,
        track=track,
        limit=limit,
        strict=strict,
        match_workers=match_workers,
    )
    if export_only:
        export_result["status"] = "exported"
        return export_result

    root_text = str(omnidocbench_root) if omnidocbench_root is not None else os.environ.get("OMNIDOCBENCH_ROOT", "")
    if not root_text:
        raise SystemExit("provide --omnidocbench-root or set OMNIDOCBENCH_ROOT")
    root = Path(root_text).expanduser().resolve()
    script = root / "pdf_validation.py"
    if not script.exists():
        raise SystemExit(f"missing OmniDocBench evaluator: {script}")

    command = [python_bin or sys.executable, str(script), "--config", export_result["config"]]
    completed = subprocess.run(command, cwd=root)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    export_result.update(
        {
            "status": "scored",
            "omnidocbench_root": str(root),
            "command": command,
            "returncode": completed.returncode,
        }
    )
    return export_result
