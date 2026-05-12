#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any


METRIC_KEYS = ("text_ned", "formula_edit", "table_teds", "reading_order_ned")
SUMMARY_REQUIRED_KEYS = ("display_formula", "reading_order", "table", "text_block")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def round2(value: float | None) -> float | None:
    if value is None:
        return None
    return round(float(value), 2)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_aliases(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    payload = read_json(path)
    if not isinstance(payload, dict):
        raise ValueError(f"alias file must be a dict: {path}")
    aliases: dict[str, dict[str, Any]] = {}
    for model_key, meta in payload.items():
        if not isinstance(meta, dict):
            raise ValueError(f"alias entry must be a dict for {model_key}")
        aliases[model_key] = meta
    return aliases


def reverse_aliases(aliases: dict[str, dict[str, Any]]) -> dict[str, str]:
    reverse: dict[str, str] = {}
    for model_key, meta in aliases.items():
        display_name = str(meta.get("display_name", model_key))
        reverse[display_name] = model_key
        for alias in meta.get("aliases", []):
            reverse[str(alias)] = model_key
    return reverse


def display_name_for(model_key: str, aliases: dict[str, dict[str, Any]]) -> str:
    meta = aliases.get(model_key, {})
    return str(meta.get("display_name", model_key))


def extra_notes_for(model_key: str, aliases: dict[str, dict[str, Any]]) -> list[str]:
    meta = aliases.get(model_key, {})
    note = meta.get("notes")
    return [str(note)] if note else []


def find_first_file(base: Path, patterns: list[str]) -> Path | None:
    for pattern in patterns:
        matches = sorted(base.glob(pattern))
        if matches:
            return matches[0]
    return None


def load_json_loose(path: Path, required_keys: tuple[str, ...] | None = None) -> Any:
    text = path.read_bytes().decode("utf-8", errors="ignore")
    stripped = text.lstrip("\x00\r\n\t ")
    try:
        payload = json.loads(stripped)
        if required_keys and isinstance(payload, dict):
            if not set(required_keys).issubset(payload.keys()):
                raise ValueError(f"required keys missing in {path}")
        return payload
    except Exception:
        pass

    decoder = json.JSONDecoder()
    best_obj: Any = None
    best_score: tuple[int, int, int] = (-1, -1, -1)

    for idx, ch in enumerate(text):
        if ch not in "{[":
            continue
        try:
            obj, end = decoder.raw_decode(text[idx:])
        except Exception:
            continue

        matched_keys = 0
        full_match = 0
        if required_keys and isinstance(obj, dict):
            matched_keys = len(set(required_keys) & set(obj.keys()))
            full_match = int(matched_keys == len(required_keys))
        score = (full_match, matched_keys, end)
        if score > best_score:
            best_score = score
            best_obj = obj
            if required_keys and full_match:
                break

    if best_obj is None:
        raise ValueError(f"unable to parse JSON payload from {path}")
    if required_keys and isinstance(best_obj, dict):
        if not set(required_keys).issubset(best_obj.keys()):
            raise ValueError(f"required keys missing in best candidate for {path}")
    return best_obj


def summary_metrics_from_payload(payload: dict[str, Any]) -> dict[str, float]:
    return {
        "text_ned": round2((1.0 - payload["text_block"]["page"]["Edit_dist"]["ALL"]) * 100.0),
        "formula_edit": round2((1.0 - payload["display_formula"]["page"]["Edit_dist"]["ALL"]) * 100.0),
        "table_teds": round2(payload["table"]["page"]["TEDS"]["ALL"] * 100.0),
        "reading_order_ned": round2((1.0 - payload["reading_order"]["page"]["Edit_dist"]["ALL"]) * 100.0),
    }


def compute_formula_cdm_from_per_sample(cdm_dir: Path) -> float | None:
    sample_file = find_first_file(
        cdm_dir,
        [
            "*_quick_match_display_formula_per_sample_CDM.json",
            "*_quick_match_display_formula_cdmcalc_per_sample_CDM.json",
        ],
    )
    if sample_file is None or not sample_file.exists():
        return None
    payload = load_json_loose(sample_file)
    if not isinstance(payload, dict):
        raise ValueError(f"per-sample CDM file must be dict: {sample_file}")

    grouped: dict[str, list[float]] = defaultdict(list)
    for sample_key, value in payload.items():
        page_key = str(sample_key).rsplit("_[", 1)[0]
        grouped[page_key].append(float(value))

    if not grouped:
        return None
    return round2(mean(mean(values) for values in grouped.values()) * 100.0)


def build_snapshot_entry(
    model_key: str,
    model_root: Path,
    aliases: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    cdm_dir = model_root / "cdm"
    nocdm_dir = model_root / "nocdm"
    cdm_metric_file = find_first_file(cdm_dir, ["*_quick_match_metric_result.json"])
    nocdm_metric_file = find_first_file(nocdm_dir, ["*_quick_match_metric_result.json"])

    cdm_metric = None
    nocdm_metric = None
    notes = extra_notes_for(model_key, aliases)
    source_files: dict[str, str] = {}

    if cdm_metric_file is not None and cdm_metric_file.exists():
        try:
            cdm_metric = load_json_loose(cdm_metric_file, required_keys=SUMMARY_REQUIRED_KEYS)
            source_files["cdm_metric"] = str(cdm_metric_file)
        except Exception:
            notes.append("CDM metric summary parse failed; using fallback sources where possible")

    if nocdm_metric_file is not None and nocdm_metric_file.exists():
        try:
            nocdm_metric = load_json_loose(nocdm_metric_file, required_keys=SUMMARY_REQUIRED_KEYS)
            source_files["nocdm_metric"] = str(nocdm_metric_file)
        except Exception:
            notes.append("NOCDM metric summary parse failed")

    base_metric = cdm_metric or nocdm_metric
    if base_metric is None:
        return None

    metrics = summary_metrics_from_payload(base_metric)
    formula_cdm = None
    if cdm_metric is not None:
        formula_cdm = round2(cdm_metric["display_formula"]["page"]["CDM"]["ALL"] * 100.0)
    elif cdm_dir.exists():
        formula_cdm = compute_formula_cdm_from_per_sample(cdm_dir)
        if formula_cdm is not None:
            notes.append("Formula CDM regrouped from per-sample file")
            sample_file = find_first_file(
                cdm_dir,
                [
                    "*_quick_match_display_formula_per_sample_CDM.json",
                    "*_quick_match_display_formula_cdmcalc_per_sample_CDM.json",
                ],
            )
            if sample_file is not None:
                source_files["formula_cdm_regroup"] = str(sample_file)

    avg4_edit = round2(mean(metrics[key] for key in METRIC_KEYS))
    avg4_cdm = None
    status = "partial"
    if formula_cdm is not None:
        avg4_cdm = round2(mean([metrics["text_ned"], metrics["table_teds"], formula_cdm, metrics["reading_order_ned"]]))
        status = "done"

    return {
        "rank": None,
        "model_name": display_name_for(model_key, aliases),
        "model_key": model_key,
        "status": status,
        "metrics": {
            **metrics,
            "formula_cdm": formula_cdm,
            "avg4_edit": avg4_edit,
            "avg4_cdm": avg4_cdm,
        },
        "notes": " | ".join(dict.fromkeys(note for note in notes if note)),
        "sources": source_files,
    }


def sort_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    done_entries = [entry for entry in entries if entry["metrics"].get("avg4_cdm") is not None]
    partial_entries = [entry for entry in entries if entry["metrics"].get("avg4_cdm") is None]

    done_entries.sort(
        key=lambda entry: (
            -float(entry["metrics"]["avg4_cdm"]),
            -float(entry["metrics"].get("avg4_edit") or -1.0),
            entry["model_name"].lower(),
        )
    )
    partial_entries.sort(
        key=lambda entry: (
            -float(entry["metrics"].get("avg4_edit") or -1.0),
            entry["model_name"].lower(),
        )
    )

    for index, entry in enumerate(done_entries, start=1):
        entry["rank"] = index
    for entry in partial_entries:
        entry["rank"] = None

    return done_entries + partial_entries


def render_metric(value: float | None) -> str:
    return "—" if value is None else f"{value:.2f}"


def render_markdown(board: dict[str, Any]) -> str:
    lines = [
        f"# {board['board_title']}",
        "",
        f"- Board ID: `{board['board_id']}`",
        f"- Generated at: `{board['generated_at']}`",
        f"- Source: `{board['source']}`",
        "- Metrics: `Avg4(CDM) = mean(Text NED, Table TEDS, Formula CDM, Reading Order NED)`; `Avg4(Edit) = mean(Text NED, Table TEDS, Formula Edit, Reading Order NED)`",
        "",
        "| Rank | Model | Status | Text NED | Table TEDS | Formula CDM | Formula Edit | Reading Order NED | Avg4(CDM) | Avg4(Edit) | Notes |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]

    for entry in board["entries"]:
        metrics = entry["metrics"]
        lines.append(
            "| "
            + " | ".join(
                [
                    "—" if entry["rank"] is None else str(entry["rank"]),
                    entry["model_name"],
                    entry["status"],
                    render_metric(metrics.get("text_ned")),
                    render_metric(metrics.get("table_teds")),
                    render_metric(metrics.get("formula_cdm")),
                    render_metric(metrics.get("formula_edit")),
                    render_metric(metrics.get("reading_order_ned")),
                    render_metric(metrics.get("avg4_cdm")),
                    render_metric(metrics.get("avg4_edit")),
                    entry.get("notes", ""),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def write_board(
    board_id: str,
    board_title: str,
    source: str,
    entries: list[dict[str, Any]],
    output_json: Path,
    output_md: Path,
) -> None:
    sorted_entries = sort_entries(entries)
    board = {
        "board_id": board_id,
        "board_title": board_title,
        "generated_at": now_iso(),
        "source": source,
        "entries": sorted_entries,
    }
    write_json(output_json, board)
    write_text(output_md, render_markdown(board))


def load_extra_entries(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    payload = read_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"extra entries file must be a list: {path}")
    return payload


def merge_entries(base_entries: list[dict[str, Any]], extra_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for entry in base_entries:
        merged[entry["model_key"]] = entry
    for entry in extra_entries:
        merged[entry["model_key"]] = entry
    return list(merged.values())


def build_summary_entry(
    model_name: str,
    summary_payload: dict[str, Any],
    aliases: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    reverse = reverse_aliases(aliases)
    model_key = reverse.get(model_name, model_name)
    notes = extra_notes_for(model_key, aliases)

    nocdm = summary_payload.get("nocdm", {})
    cdm = summary_payload.get("cdm", {})

    cdm_done = cdm.get("status") == "done"
    nocdm_done = nocdm.get("status") == "done"
    base = cdm if cdm_done else nocdm if nocdm_done else {}

    metrics = {
        "text_ned": round2(base.get("text")),
        "formula_edit": round2(base.get("formula_edit")),
        "table_teds": round2(base.get("table")),
        "reading_order_ned": round2(base.get("reading_order")),
        "formula_cdm": round2(cdm.get("formula_cdm")) if cdm_done else None,
        "avg4_edit": round2(base.get("avg4_formula_edit")),
        "avg4_cdm": round2(cdm.get("avg4_formula_cdm")) if cdm_done else None,
    }

    status = "done" if metrics["avg4_cdm"] is not None else "partial" if metrics["avg4_edit"] is not None else "pending"

    cdm_src = cdm.get("cdm_src")
    sources = {"summary": "summary_json"}
    if cdm_src:
        sources["formula_cdm"] = str(cdm_src)

    return {
        "rank": None,
        "model_name": model_name,
        "model_key": model_key,
        "status": status,
        "metrics": metrics,
        "notes": " | ".join(dict.fromkeys(note for note in notes if note)),
        "sources": sources,
    }


def command_from_summary(args: argparse.Namespace) -> None:
    aliases = load_aliases(args.model_aliases)
    summary_payload = read_json(args.summary_json)
    entries = [
        build_summary_entry(model_name, payload, aliases)
        for model_name, payload in summary_payload.items()
    ]
    entries = merge_entries(entries, load_extra_entries(args.extra_entries))
    write_board(args.board_id, args.board_title, args.source, entries, args.output_json, args.output_md)


def command_from_snapshots(args: argparse.Namespace) -> None:
    aliases = load_aliases(args.model_aliases)
    include_set = set(args.include_model_key or [])
    entries: list[dict[str, Any]] = []

    for model_root in sorted(args.result_snapshots_root.iterdir()):
        if not model_root.is_dir():
            continue
        model_key = model_root.name
        if include_set and model_key not in include_set:
            continue
        entry = build_snapshot_entry(model_key, model_root, aliases)
        if entry is not None:
            entries.append(entry)

    write_board(args.board_id, args.board_title, args.source, entries, args.output_json, args.output_md)


def command_upsert_from_snapshots(args: argparse.Namespace) -> None:
    aliases = load_aliases(args.model_aliases)
    board_json = args.board_json
    board_md = args.board_md
    board_json.parent.mkdir(parents=True, exist_ok=True)
    board_md.parent.mkdir(parents=True, exist_ok=True)

    if board_json.exists():
        board = read_json(board_json)
        entries = list(board.get("entries", []))
        board_id = board.get("board_id", args.board_id)
        board_title = board.get("board_title", args.board_title)
        source = board.get("source", args.source)
    else:
        entries = []
        board_id = args.board_id
        board_title = args.board_title
        source = args.source

    model_root = args.result_snapshots_root / args.model_key
    entry = build_snapshot_entry(args.model_key, model_root, aliases)
    if entry is None:
        raise SystemExit(f"no usable score snapshot for model_key={args.model_key}")

    entries = merge_entries(entries, [entry])
    write_board(board_id, board_title, source, entries, board_json, board_md)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build and update frozen leaderboard artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    summary_parser = subparsers.add_parser("from-summary", help="Build leaderboard from a frozen summary JSON.")
    summary_parser.add_argument("--summary-json", type=Path, required=True)
    summary_parser.add_argument("--model-aliases", type=Path)
    summary_parser.add_argument("--extra-entries", type=Path)
    summary_parser.add_argument("--board-id", required=True)
    summary_parser.add_argument("--board-title", required=True)
    summary_parser.add_argument("--source", required=True)
    summary_parser.add_argument("--output-json", type=Path, required=True)
    summary_parser.add_argument("--output-md", type=Path, required=True)
    summary_parser.set_defaults(func=command_from_summary)

    snapshots_parser = subparsers.add_parser("from-snapshots", help="Build leaderboard from result_snapshots directory.")
    snapshots_parser.add_argument("--result-snapshots-root", type=Path, required=True)
    snapshots_parser.add_argument("--model-aliases", type=Path)
    snapshots_parser.add_argument("--include-model-key", action="append")
    snapshots_parser.add_argument("--board-id", required=True)
    snapshots_parser.add_argument("--board-title", required=True)
    snapshots_parser.add_argument("--source", required=True)
    snapshots_parser.add_argument("--output-json", type=Path, required=True)
    snapshots_parser.add_argument("--output-md", type=Path, required=True)
    snapshots_parser.set_defaults(func=command_from_snapshots)

    upsert_parser = subparsers.add_parser("upsert-from-snapshots", help="Upsert one model entry into a leaderboard JSON/Markdown pair.")
    upsert_parser.add_argument("--result-snapshots-root", type=Path, required=True)
    upsert_parser.add_argument("--model-key", required=True)
    upsert_parser.add_argument("--model-aliases", type=Path)
    upsert_parser.add_argument("--board-id", required=True)
    upsert_parser.add_argument("--board-title", required=True)
    upsert_parser.add_argument("--source", required=True)
    upsert_parser.add_argument("--board-json", type=Path, required=True)
    upsert_parser.add_argument("--board-md", type=Path, required=True)
    upsert_parser.set_defaults(func=command_upsert_from_snapshots)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
