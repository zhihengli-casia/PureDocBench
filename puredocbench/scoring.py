from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from statistics import mean
from typing import Any

from .common import normalize_space, read_json, read_manifest, safe_stem, track_column, write_json

try:
    from bs4 import BeautifulSoup
except Exception:  # pragma: no cover - optional dependency fallback
    BeautifulSoup = None  # type: ignore[assignment]


TEXT_TYPES = {
    "text_block",
    "title",
    "reference",
    "code_txt",
    "list",
    "paragraph",
}
FORMULA_TYPES = {"equation_isolated", "display_formula", "formula"}
TABLE_TYPES = {"table"}
IGNORED_TYPES = {
    "figure_caption",
    "table_caption",
    "header",
    "footer",
    "page_number",
    "page_footnote",
}


@dataclass
class PageTarget:
    page_id: str
    category: str
    subcategory: str
    gt_path: Path
    prediction_keys: list[str]


def _ordered_items(gt_payload: dict[str, Any]) -> list[dict[str, Any]]:
    items = [item for item in gt_payload.get("layout_dets", []) if isinstance(item, dict)]
    return sorted(items, key=lambda item: (item.get("order") is None, item.get("order") or 10**9, item.get("anno_id") or 0))


def _item_text(item: dict[str, Any]) -> str:
    for key in ("text", "latex", "html"):
        value = item.get(key)
        if isinstance(value, str):
            return value
    return ""


def _normalize_html_table(html: str) -> str:
    if BeautifulSoup is None:
        text = re.sub(r"<\s*/\s*(tr|p|div|li)\s*>", "\n", html, flags=re.IGNORECASE)
        text = re.sub(r"<\s*/?\s*(td|th)\b[^>]*>", " | ", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        return normalize_space(text)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        return normalize_space(BeautifulSoup(html, "html.parser").get_text(" "))
    rows: list[str] = []
    for tr in table.find_all("tr"):
        cells = [normalize_space(cell.get_text(" ")) for cell in tr.find_all(["th", "td"])]
        if cells:
            rows.append(" | ".join(cells))
    return "\n".join(rows)


def serialize_gt(gt_payload: dict[str, Any]) -> dict[str, Any]:
    text_parts: list[str] = []
    formula_parts: list[str] = []
    table_parts: list[str] = []
    order_parts: list[str] = []

    for item in _ordered_items(gt_payload):
        category = str(item.get("category_type", ""))
        if category in IGNORED_TYPES:
            continue
        if category in TEXT_TYPES:
            content = _item_text(item)
            if content:
                text_parts.append(content)
                order_parts.append("text")
        elif category in FORMULA_TYPES:
            content = item.get("latex") or item.get("text") or ""
            if content:
                formula_parts.append(str(content))
                order_parts.append("formula")
        elif category in TABLE_TYPES:
            content = item.get("html") or item.get("text") or ""
            if content:
                table_parts.append(_normalize_html_table(str(content)))
                order_parts.append("table")
        else:
            content = _item_text(item)
            if content:
                text_parts.append(content)
                order_parts.append("text")

    return {
        "text": normalize_space("\n\n".join(text_parts)),
        "formula": normalize_space("\n\n".join(formula_parts)),
        "table": normalize_space("\n\n".join(table_parts)),
        "order": order_parts,
    }


def _extract_markdown_tables(markdown: str) -> tuple[str, str]:
    html_tables = re.findall(r"<table[\s\S]*?</table>", markdown, flags=re.IGNORECASE)
    table_chunks = [_normalize_html_table(chunk) for chunk in html_tables]
    without = re.sub(r"<table[\s\S]*?</table>", "\n", markdown, flags=re.IGNORECASE)

    lines = without.splitlines()
    keep_lines: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < len(lines) else ""
        is_md_table = "|" in line and re.search(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", next_line)
        if is_md_table:
            chunk = [line, next_line]
            i += 2
            while i < len(lines) and "|" in lines[i].strip():
                chunk.append(lines[i])
                i += 1
            table_chunks.append("\n".join(chunk))
            continue
        keep_lines.append(line)
        i += 1
    return normalize_space("\n\n".join(table_chunks)), "\n".join(keep_lines)


def _extract_formulas(markdown: str) -> tuple[str, str]:
    patterns = [
        r"\$\$([\s\S]*?)\$\$",
        r"\\\[([\s\S]*?)\\\]",
        r"\\begin\{(?:equation|align|gather|multline)\*?\}([\s\S]*?)\\end\{(?:equation|align|gather|multline)\*?\}",
    ]
    formulas: list[str] = []
    without = markdown
    for pattern in patterns:
        for match in re.finditer(pattern, without):
            formulas.append(match.group(1))
        without = re.sub(pattern, "\n", without)

    latex_line = re.compile(r"(\\frac|\\sum|\\int|\\sqrt|\\begin|\\alpha|\\beta|\\gamma|[_^]=?|[=<>≤≥])")
    remaining_lines: list[str] = []
    for line in without.splitlines():
        stripped = line.strip()
        if stripped and latex_line.search(stripped) and len(stripped) < 240:
            formulas.append(stripped.strip("$"))
        else:
            remaining_lines.append(line)
    return normalize_space("\n\n".join(formulas)), "\n".join(remaining_lines)


def serialize_prediction(markdown: str) -> dict[str, Any]:
    table_text, without_tables = _extract_markdown_tables(markdown)
    formula_text, without_formulas = _extract_formulas(without_tables)
    text = re.sub(r"```[\s\S]*?```", "\n", without_formulas)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s{0,3}[-*+]\s+", "", text, flags=re.MULTILINE)

    order: list[str] = []
    for block in re.split(r"\n\s*\n", markdown):
        b = block.strip()
        if not b:
            continue
        if "<table" in b.lower() or "|" in b:
            order.append("table")
        elif "$$" in b or "\\[" in b or re.search(r"\\(frac|sum|int|sqrt|begin)", b):
            order.append("formula")
        else:
            order.append("text")

    return {
        "text": normalize_space(text),
        "formula": formula_text,
        "table": table_text,
        "order": order,
    }


def similarity(reference: str, prediction: str) -> float | None:
    reference = normalize_space(reference)
    prediction = normalize_space(prediction)
    if not reference:
        return None
    if not prediction:
        return 0.0
    return SequenceMatcher(None, reference, prediction, autojunk=False).ratio()


def order_similarity(reference: list[str], prediction: list[str]) -> float | None:
    if not reference:
        return None
    if not prediction:
        return 0.0
    return SequenceMatcher(None, reference, prediction, autojunk=False).ratio()


def score_page(gt_payload: dict[str, Any], prediction_text: str) -> dict[str, float | None]:
    gt = serialize_gt(gt_payload)
    pred = serialize_prediction(prediction_text)
    scores = {
        "text_score": similarity(gt["text"], pred["text"]),
        "formula_score": similarity(gt["formula"], pred["formula"]),
        "table_score": similarity(gt["table"], pred["table"]),
        "reading_order_score": order_similarity(gt["order"], pred["order"]),
    }
    applicable = [value for value in scores.values() if value is not None]
    scores["overall_score"] = mean(applicable) if applicable else None
    return scores


def build_prediction_index(pred_dir: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in sorted(pred_dir.rglob("*.md")):
        rel = path.relative_to(pred_dir).as_posix()
        keys = {rel, path.name, path.stem}
        for key in keys:
            index.setdefault(key, path)
    return index


def build_targets(release_root: Path, manifest_path: Path, track: str, limit: int | None = None) -> list[PageTarget]:
    rows = read_manifest(manifest_path)
    column = track_column(track)
    targets: list[PageTarget] = []
    for row in rows[:limit]:
        track_rel = row[column]
        clean_rel = row["clean_rel"]
        page_id = row["page_id"]
        keys = [
            Path(track_rel).with_suffix(".md").as_posix(),
            Path(track_rel).with_suffix(".md").name,
            safe_stem(track_rel),
            Path(clean_rel).with_suffix(".md").as_posix(),
            Path(clean_rel).with_suffix(".md").name,
            safe_stem(clean_rel),
            safe_stem(page_id),
        ]
        targets.append(
            PageTarget(
                page_id=page_id,
                category=row.get("category", ""),
                subcategory=row.get("subcategory", ""),
                gt_path=release_root / "gt" / row["gt_rel"],
                prediction_keys=list(dict.fromkeys(keys)),
            )
        )
    return targets


def _pct(value: float | None) -> float | None:
    return None if value is None else round(value * 100.0, 4)


def _mean(values: list[float | None]) -> float | None:
    clean = [value for value in values if value is not None]
    return None if not clean else round(mean(clean), 4)


def run_score(
    release_root: Path,
    manifest_path: Path,
    pred_dir: Path,
    out_dir: Path,
    track: str = "clean",
    limit: int | None = None,
    strict: bool = False,
) -> dict[str, Any]:
    targets = build_targets(release_root, manifest_path, track, limit)
    pred_index = build_prediction_index(pred_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    page_rows: list[dict[str, Any]] = []
    missing: list[str] = []

    for target in targets:
        pred_path = next((pred_index[key] for key in target.prediction_keys if key in pred_index), None)
        if pred_path is None:
            missing.append(target.page_id)
            prediction_text = ""
        else:
            prediction_text = pred_path.read_text(encoding="utf-8", errors="replace")
        gt_payload = read_json(target.gt_path)
        metrics = score_page(gt_payload, prediction_text)
        page_rows.append(
            {
                "page_id": target.page_id,
                "category": target.category,
                "subcategory": target.subcategory,
                "prediction_file": "" if pred_path is None else str(pred_path),
                "missing_prediction": pred_path is None,
                **{key: _pct(value) for key, value in metrics.items()},
            }
        )

    if strict and missing:
        raise SystemExit(f"missing {len(missing)} predictions; first missing page_id: {missing[0]}")

    metric_keys = ["overall_score", "text_score", "formula_score", "table_score", "reading_order_score"]
    summary = {
        "scorer": "puredocbench-lite",
        "note": "Lightweight public scorer. Use export-omnidocbench plus the intended OmniDocBench evaluator snapshot for leaderboard-style metrics.",
        "track": track,
        "release_root": str(release_root),
        "manifest": str(manifest_path),
        "pred_dir": str(pred_dir),
        "pages": len(page_rows),
        "missing_predictions": len(missing),
        "metrics": {key: _mean([row[key] for row in page_rows]) for key in metric_keys},
    }

    with (out_dir / "page_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(page_rows[0].keys()) if page_rows else [])
        writer.writeheader()
        writer.writerows(page_rows)
    write_json(out_dir / "summary.json", summary)
    write_report(out_dir / "report.md", summary)
    return summary


def write_report(path: Path, summary: dict[str, Any]) -> None:
    metrics = summary["metrics"]
    lines = [
        "# PureDocBench Lite Score",
        "",
        f"- Track: `{summary['track']}`",
        f"- Pages: {summary['pages']}",
        f"- Missing predictions: {summary['missing_predictions']}",
        "",
        "| Metric | Score |",
        "|---|---:|",
    ]
    for key, label in [
        ("overall_score", "Overall"),
        ("text_score", "Text"),
        ("formula_score", "Formula"),
        ("table_score", "Table"),
        ("reading_order_score", "Reading order"),
    ]:
        value = metrics.get(key)
        lines.append(f"| {label} | {'n/a' if value is None else f'{value:.2f}'} |")
    lines.extend(
        [
            "",
            "> This is the lightweight public scorer bundled with the repository. It is useful for quick model development and sanity checks. For leaderboard-style numbers, export the inputs with `puredocbench export-omnidocbench` and run the intended OmniDocBench evaluator snapshot.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
