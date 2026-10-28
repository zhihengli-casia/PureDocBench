"""Protect released decimal values, model identity, and historical submissions."""

import csv
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

    def test_doclayout_rescore_matches_versioned_result_record(self):
        entry = next(model for model in BUILDER.load_data() if model["key"] == "paddleocr-vl-1-6-layout-corrected")
        directory = ROOT / "results/submissions/doclayoutv3"
        record = json.loads((directory / "run.json").read_text())
        self.assertEqual(entry["evaluation_kind"], "maintainer-rescored")
        self.assertEqual(entry["architecture"], "Pipeline")
        self.assertEqual(entry["url"], "https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.6")
        self.assertEqual(entry["source"], "paper")
        self.assertEqual(entry["name"], "PaddleOCR-VL-1.6")
        self.assertEqual(record["canonical_model_key"], entry["key"])
        self.assertEqual(record["model_identity"]["confirmed_pipeline"], entry["pipeline"])
        self.assertEqual(entry["release_month"], "2026-05")
        self.assertEqual(record["inputs"]["total_predictions"], 4425)
        self.assertEqual(record["inputs"]["missing_predictions"], 0)
        self.assertEqual(record["ground_truth"]["revision"], "4665b40a3333f7643bad7c8675a9062b482511ad")
        self.assertEqual(record["evaluator"]["commit"], "f133a71e9e91c3621c7ce8994200a7b394a06eb3")
        self.assertEqual(record["denominators_per_track"]["reading_order_pages"], 1471)
        self.assertEqual(float(entry["avg3"]), record["avg3"])
        for row in record["scores"]:
            scores = entry["scores"][row["Track"]]
            for public, saved in [("overall", "Overall"), ("text_edit", "TextEdit"), ("formula_cdm", "FormulaCDM"), ("table_teds", "TableTEDS"), ("reading_edit", "ROEdit")]:
                self.assertEqual(float(scores[public]), row[saved])
        with (directory / "category_components.csv").open() as handle:
            category_rows = list(csv.DictReader(handle))
        self.assertEqual(len(category_rows), 30)
        for name, expected in json.loads((directory / "checksums.json").read_text()).items():
            self.assertEqual(hashlib.sha256((directory / name).read_bytes()).hexdigest(), expected, name)

    def test_readme_main_row_and_inapplicable_category_summary(self):
        text = (ROOT / "README.md").read_text()
        row = next(line for line in text.splitlines() if '<tr><td><a href="https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.6">' in line)
        for value in ["72.65", "67.01", "61.96", "67.21"]:
            self.assertIn(f'>{value}</td>', row)
        spec = importlib.util.spec_from_file_location("result_summaries", ROOT / "results/summarize.py")
        summaries = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(summaries)
        _, categories = summaries.summarize(BUILDER.read_csv("category_components.csv"))
        certificate = next(r for r in categories if r["model_key"] == "paddleocr-vl-1-6-layout-corrected" and r["category"] == "certificate")
        self.assertEqual(certificate["avg3"], "")
        self.assertEqual(certificate["mean_formula"], "")
        self.assertNotEqual(certificate["mean_table"], "")
        archived = json.loads((ROOT / "results/archive/paddleocr_vl_1_6_before_rescore_20261027.json").read_text())
        self.assertEqual(archived["leaderboard"][0]["avg3"], "59.33")


if __name__ == "__main__":
    unittest.main()
