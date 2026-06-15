# PureDocBench GT Annotation Corrections

This page defines the correction workflow for PureDocBench GT bounding-box annotations.

## Current Public GT

- The current GT bbox version is `puredocbench-gt-bbox-v1.0.0`.
- Hugging Face stores released versions under `gt_bbox/versions/<version>/`.
- `gt_bbox/latest/manifest.json` may point to the newest version, but papers and evaluation reports should cite the exact public annotation version.

## Review App

The review app is a static HTML app:

- Public review app: [Open GT Review App](https://zhihengli-casia.github.io/PureDocBench/review/gt_case_compare_all_fixed7/index.html?cb=puredocbench_gt_bbox_v1_0_0_local_images)
- Repository file: [`review/gt_case_compare_all_fixed7/index.html`](../review/gt_case_compare_all_fixed7/index.html)
- GitHub issue template: [New GT annotation correction issue](https://github.com/zhihengli-casia/PureDocBench/issues/new?template=annotation_error.yml)

The GitHub repository does not include the full image release. For visual review, download the Hugging Face release, open the public review app, click `Load Images`, and select the extracted `images/clean` folder.

Local launch:

```bash
mkdir -p review/gt_case_compare_all_fixed7/assets
ln -s /path/to/puredocbench-v1.0/images/clean review/gt_case_compare_all_fixed7/assets/images
python3 -m http.server 8767 --directory review/gt_case_compare_all_fixed7
```

Open:

```text
http://127.0.0.1:8767/index.html?cb=puredocbench_gt_bbox_v1_0_0_local_images
```

Static app URL:

```text
https://zhihengli-casia.github.io/PureDocBench/review/gt_case_compare_all_fixed7/index.html?cb=puredocbench_gt_bbox_v1_0_0_local_images
```

## Correction Flow

1. Open the review app with the current public annotation version.
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
  "schema_version": "puredocbench-gt-correction-patch-v1",
  "base_annotation_version": "puredocbench-gt-bbox-v1.0.0",
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

For missing or duplicate annotations, use the case-level correction note. Accepted notes are converted into explicit `add_annotation`, `delete_annotation`, `update_type`, `update_text`, or `update_reading_order` changes in the next release.

## Release Flow

1. Review correction patches visually.
2. Apply accepted patches to `review_data.json`.
3. Update `review_data.js` and `index.html` cache tags.
4. Generate cover/outline previews for changed cases.
5. Run validation.
6. Package the HF release:

```bash
python scripts/package_hf_gt_release.py \
  --review-dir review/gt_case_compare_all_fixed7 \
  --out-root dist/hf_gt_bbox \
  --write-latest
```

7. Upload the generated package to Hugging Face:

```bash
huggingface-cli upload zhihengli-casia/puredocbench \
  dist/hf_gt_bbox/puredocbench-gt-bbox-v1.0.0 \
  gt_bbox/versions/puredocbench-gt-bbox-v1.0.0 \
  --repo-type dataset \
  --commit-message "Add GT bbox annotations puredocbench-gt-bbox-v1.0.0"

huggingface-cli upload zhihengli-casia/puredocbench \
  dist/hf_gt_bbox/latest \
  gt_bbox/latest \
  --repo-type dataset \
  --commit-message "Update latest GT bbox annotation manifest"
```

## Evaluation Rule

Every public score should record:

- dataset version
- annotation version
- evaluation script version
- model output version

Do not report benchmark results against an implicit `latest` annotation set.
