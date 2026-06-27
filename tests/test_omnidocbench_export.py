from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from puredocbench.omnidocbench import export_omnidocbench


class OmniDocBenchExportTest(unittest.TestCase):
    def test_export_fills_missing_relation_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            release_root = root / "release"
            gt_path = release_root / "gt" / "sample.json"
            gt_path.parent.mkdir(parents=True)
            gt_path.write_text(
                json.dumps(
                    {
                        "layout_dets": [],
                        "page_info": {"image_path": "old/path.png"},
                        "extra": {},
                    }
                ),
                encoding="utf-8",
            )

            manifest_path = root / "manifest.csv"
            manifest_path.write_text(
                "\n".join(
                    [
                        "page_id,gt_rel,clean_rel,digital_rel,real_rel,category,subcategory",
                        "sample,sample.json,images/clean/sample.png,images/digital/sample.png,images/real/sample.png,test,test",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            pred_dir = root / "predictions"
            pred_dir.mkdir()
            (pred_dir / "sample.md").write_text("prediction", encoding="utf-8")

            out_dir = root / "out"
            export_omnidocbench(
                release_root=release_root,
                manifest_path=manifest_path,
                pred_dir=pred_dir,
                out_dir=out_dir,
            )

            exported_gt = json.loads((out_dir / "gt.json").read_text(encoding="utf-8"))
            self.assertEqual(exported_gt[0]["extra"]["relation"], [])


if __name__ == "__main__":
    unittest.main()
