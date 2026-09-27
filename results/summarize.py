#!/usr/bin/env python3
"""Summarize global or per-category component scores using exact decimals.

Python standard library only. Input scores have already been computed by the
formal evaluator; this script aggregates metrics and does not score predictions.
"""
from __future__ import annotations

import argparse
import csv
import warnings
from collections import OrderedDict
from decimal import Decimal, localcontext, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path

TRACKS = ("clean", "digital", "real")
METRICS = ("text_edit", "formula_cdm", "table_teds", "reading_edit")


def number(value: str, field: str, maximum=100, strict=True) -> Fraction:
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f"Invalid {field}: {value!r}") from error
    if not 0 <= result <= maximum:
        message = f"{field} is outside 0 to {maximum}: {value!r}"
        if strict:
            raise ValueError(message)
        warnings.warn(message + "; retaining the supplied value without clipping.", RuntimeWarning)
    return result


def decimal(value: Fraction) -> str:
    with localcontext() as context:
        context.prec = 60
        text = format(Decimal(value.numerator) / Decimal(value.denominator), "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def displayed(value: Fraction) -> str:
    with localcontext() as context:
        context.prec = 60
        return str((Decimal(value.numerator) / Decimal(value.denominator)).quantize(
            Decimal(".01"), rounding=ROUND_HALF_UP))


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize(rows: list[dict], reference: list[dict] | None = None):
    groups = OrderedDict()
    track_rows = []
    has_categories = any(row.get("category") for row in rows)
    if not rows:
        raise ValueError("Input has no rows.")
    if has_categories and (reference is not None or not all(row.get("category") for row in rows)):
        raise ValueError("Category inputs require a category on every row and no global reference.")
    reference_lookup = {}
    if reference is not None:
        for row in reference:
            key = row["model_key"]
            if key in reference_lookup:
                raise ValueError(f"Duplicate reference model: {key}")
            reference_lookup[key] = row
    for row in rows:
        key, track = row["model_key"].strip(), row["track"].strip()
        if not key or track not in TRACKS:
            raise ValueError(f"Invalid model/track: {key!r}/{track!r}")
        group_key = (key, row["category"]) if has_categories else (key,)
        group = groups.setdefault(group_key, {})
        if track in group:
            raise ValueError(f"Duplicate model/category/track: {group_key}/{track}")
        metrics = {m: number(row[m], f"{key}/{track}/{m}", 1 if m.endswith("_edit") else 100,
                             strict=False) for m in METRICS}
        text_score = 100 * (1 - metrics["text_edit"])
        reading_score = 100 * (1 - metrics["reading_edit"])
        computed = (text_score + metrics["formula_cdm"] + metrics["table_teds"]) / 3
        supplied = number(row["overall"], "overall", strict=False) if row.get("overall") else computed
        used = supplied
        if reference is not None:
            if key not in reference_lookup:
                raise ValueError(f"Missing reference model: {key}")
            used = number(reference_lookup[key][track], track)
            if displayed(used) != displayed(supplied):
                raise ValueError(f"Reference and input differ at two decimals: {key}/{track}")
        result = dict(model_key=key)
        if has_categories:
            result["category"] = row["category"]
        result.update(track=track, overall=decimal(used), overall_recomputed=decimal(computed),
                      text_score=decimal(text_score), formula_score=decimal(metrics["formula_cdm"]),
                      table_score=decimal(metrics["table_teds"]), reading_score=decimal(reading_score))
        track_rows.append(result)
        group[track] = result
    if reference is not None and set(reference_lookup) != {key[0] for key in groups}:
        raise ValueError("Reference and component inputs must contain the same models.")
    summaries = []
    for group_key, tracks in groups.items():
        if set(tracks) != set(TRACKS):
            raise ValueError(f"Expected Clean, Digital and Real for {group_key}; got {list(tracks)}")
        values = {t: Fraction(tracks[t]["overall"]) for t in TRACKS}
        mean = sum(values.values(), Fraction()) / 3
        reference_mean = number(reference_lookup[group_key[0]]["avg3"], "avg3") if reference is not None else mean
        summary = dict(model_key=group_key[0])
        if has_categories:
            summary["category"] = group_key[1]
        summary.update({t: decimal(values[t]) for t in TRACKS})
        summary.update(avg3=decimal(reference_mean), avg3_recomputed=decimal(mean),
                       digital_minus_clean=decimal(values["digital"] - values["clean"]),
                       real_minus_clean=decimal(values["real"] - values["clean"]))
        for component in ("text", "formula", "table", "reading"):
            summary[f"mean_{component}"] = decimal(sum(
                (Fraction(tracks[t][f"{component}_score"]) for t in TRACKS), Fraction()) / 3)
        summaries.append(summary)
    return track_rows, summaries


def write_csv(path: Path, rows: list[dict]):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Component CSV; optional category and overall columns.")
    parser.add_argument("--reference", type=Path, help="Optional reference leaderboard; preserves its three-track scores and Avg3.")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    reference = read_csv(args.reference) if args.reference else None
    tracks, models = summarize(read_csv(args.input), reference)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "track_scores.csv", tracks)
    write_csv(args.output_dir / "summary.csv", models)
    print(f"Wrote {len(tracks)} track records and {len(models)} summaries to {args.output_dir}")


if __name__ == "__main__":
    main()
