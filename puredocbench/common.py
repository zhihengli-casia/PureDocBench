from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any


TRACK_TO_COLUMN = {
    "clean": "clean_rel",
    "digital": "digital_rel",
    "digital_degraded": "digital_rel",
    "real": "real_rel",
    "real_degraded": "real_rel",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"empty manifest: {path}")
    required = {"page_id", "gt_rel", "clean_rel", "digital_rel", "real_rel"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"manifest missing columns {sorted(missing)}: {path}")
    return rows


def track_column(track: str) -> str:
    try:
        return TRACK_TO_COLUMN[track]
    except KeyError as exc:
        valid = ", ".join(sorted(TRACK_TO_COLUMN))
        raise ValueError(f"unknown track {track!r}; choose one of: {valid}") from exc


def normalize_space(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def safe_stem(path_text: str) -> str:
    return Path(path_text).stem
