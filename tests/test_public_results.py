"""Protect released decimal values, model identity, and historical submissions."""

import hashlib
import importlib.util
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("public_leaderboard", ROOT / "results/build_public_leaderboard.py")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class PublicResultsTests(unittest.TestCase):
    def test_current_schema_and_precise_reference_values(self):
        models = BUILDER.load_data()
        current = [model for model in models if model["source"] == "paper"]
        self.assertEqual(len(current), 58)
        self.assertEqual(Counter(model["architecture"] for model in current), {"Pipeline": 13, "E2E": 19, "General VLM": 26})
        reference = {row["model_key"]: row for row in BUILDER.read_csv("leaderboard.csv")}
        components = {(row["model_key"], row["track"]): row for row in BUILDER.read_csv("components.csv")}
        for model in current:
            self.assertRegex(model["release_month"], r"^20\d\d-\d\d$")
            self.assertTrue(model["url"].startswith("https://"))
            self.assertEqual(model["avg3"], reference[model["key"]]["avg3"])
            for track in BUILDER.TRACKS:
                self.assertEqual(model["scores"][track]["overall"], reference[model["key"]][track])
                for metric in ("text_edit", "formula_cdm", "table_teds", "reading_edit"):
                    self.assertEqual(model["scores"][track][metric], components[(model["key"], track)][metric])

    def test_current_models_are_unique_and_community_is_separate(self):
        models = BUILDER.load_data()
        self.assertEqual(len({model["key"] for model in models}), 59)
        self.assertEqual([model["name"] for model in models if model["source"] == "community"], ["NaviDC-OCR"])
        self.assertEqual(sum("OpenDoc" in model["name"] for model in models), 1)
        self.assertNotIn("UniRec-0.1B", {model["name"] for model in models})
        self.assertNotIn("PaddleOCR-VL-1.5", {model["name"] for model in models})

    def test_category_coverage(self):
        rows = BUILDER.read_csv("category_components.csv")
        self.assertEqual(len(rows), 1590)
        self.assertEqual(len({row["model_key"] for row in rows}), 53)
        counts = Counter((row["model_key"], row["category"]) for row in rows)
        self.assertEqual(set(counts.values()), {3})
        self.assertEqual(set(Counter(row["model_key"] for row in rows).values()), {30})

    def test_original_community_submission_is_unchanged(self):
        actual = hashlib.sha256((ROOT / "data/wevisdoc_results.tsv").read_bytes()).hexdigest()
        self.assertEqual(actual, "751d231e9706bca3ae1a35d83ebdc3370638e675a0144aa6bc707480f3c036da")
        archived = json.loads((ROOT / "data/archive/leaderboard-2026-09-21.json").read_text())
        self.assertEqual(len(archived), 44)
        self.assertEqual(next(row[19] for row in archived if row[0] == "WeVisDoc-2B"), 73.86)


if __name__ == "__main__":
    unittest.main()
