# PureDocBench GT Annotation Corrections

This page defines the correction workflow for PureDocBench GT annotations.

## Current Public Release

Current release ID: `puredocbench-2026-06-14`.

This update refreshes GT annotations and opens the correction workflow for community review.

## Review App

The review app is a static HTML app for inspecting the GT annotations visually:

- Public review app: [Open GT Review App](https://zhihengli-casia.github.io/PureDocBench/review/gt_case_compare_all_fixed7/index.html?cb=puredocbench_2026_06_14_clean_ui)
- Repository file: [`review/gt_case_compare_all_fixed7/index.html`](../review/gt_case_compare_all_fixed7/index.html)
- GitHub issue template: [New GT annotation correction issue](https://github.com/zhihengli-casia/PureDocBench/issues/new?template=annotation_error.yml)

The GitHub repository does not include the full image release. For visual review, download the Hugging Face release, open the public review app, click `Load Images`, and select the extracted `images/clean` folder. The app uses `review_data.json` as a compact inspection view of the GT annotations.

Local launch:

```bash
mkdir -p review/gt_case_compare_all_fixed7/assets
ln -s /path/to/puredocbench-2026-06-14/images/clean review/gt_case_compare_all_fixed7/assets/images
python3 -m http.server 8767 --directory review/gt_case_compare_all_fixed7
```

Open:

```text
http://127.0.0.1:8767/index.html?cb=puredocbench_2026_06_14_clean_ui
```

Static app URL:

```text
https://zhihengli-casia.github.io/PureDocBench/review/gt_case_compare_all_fixed7/index.html?cb=puredocbench_2026_06_14_clean_ui
```

## Correction Flow

1. Open the review app with the current public release version.
2. Find the case with a visible annotation problem.
3. For an existing bbox error, drag or resize the box in the app.
4. For missing annotations, wrong type, duplicate boxes, or reading-order issues, write a case-level correction note.
5. Mark uncertain or problematic items as `Problem` or `Unsure`.
6. Click `Export Correction Patch`.
7. Submit the exported JSON in a GitHub issue or pull request.

The GitHub issue form accepts either English or Chinese. If you cannot export a patch, describe the problem and attach a screenshot.

Accepted corrections are verified against the clean image and source HTML before the next GT release.

## Patch Format

The review app exports this schema:

```json
{
  "schema_version": "puredocbench-annotation-correction-patch-v1",
  "base_annotation_version": "puredocbench-2026-06-14",
  "summary": {
    "case_count": 1,
    "bbox_update_count": 1,
    "annotation_flag_count": 0,
    "case_note_count": 0,
    "added_annotations": 0,
    "removed_annotations": 0
  },
  "cases": [
    {
      "case_id": "01_academic/01_journal_paper/example",
      "changes": [
        {
          "op": "update_bbox",
          "anno_id": 6,
          "index": 6,
          "type": "text_block",
          "old_bbox": [192, 520, 2294, 726],
          "new_bbox": [197, 519, 2290, 918],
          "note": "Summary block was truncated."
        }
      ]
    }
  ]
}
```

For missing or duplicate annotations, use the case-level correction note. Maintainers will convert accepted notes into explicit `add_annotation`, `delete_annotation`, `update_type`, `update_text`, or `update_reading_order` changes in the next release log.

## Maintainer Release Flow

1. Review correction patches visually.
2. Apply accepted patches to `review_data.json`.
3. Update `review_data.js`, `index.html` cache tags, and `GT_REPAIR_LOG.md`.
4. Generate cover/outline previews for changed cases.
5. Run validation.
6. Package the HF release:

```bash
python scripts/package_hf_gt_release.py \
  --review-dir review/gt_case_compare_all_fixed7 \
  --out-root dist/hf_gt \
  --write-latest
```

7. Upload the generated package to Hugging Face:

```bash
huggingface-cli upload zhihengli-casia/puredocbench \
  dist/hf_gt/puredocbench-2026-06-14 \
  gt/versions/puredocbench-2026-06-14 \
  --repo-type dataset \
  --commit-message "Add GT puredocbench-2026-06-14"

huggingface-cli upload zhihengli-casia/puredocbench \
  dist/hf_gt/latest \
  gt/latest \
  --repo-type dataset \
  --commit-message "Update latest GT manifest"
```
