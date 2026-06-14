# PureDocBench GT Annotation Corrections

This page defines the public correction flow for PureDocBench GT bounding-box annotations.

## Current Public GT

- The GT bbox data is released with a community-facing semantic version, for example `puredocbench-gt-bbox-v1.0.0`.
- Hugging Face should keep every released version under `gt_bbox/versions/<public-version>/`.
- `gt_bbox/latest/manifest.json` may point to the newest version, but papers and evaluation reports should cite the exact public annotation version.
- Maintainer repair tokens such as `internal_build_token` are kept only for provenance and should not be used as the public release name.

## Review App Entry

The review app is a static HTML app stored in this repository:

- Public review app: [Open GT Review App](https://zhihengli-casia.github.io/PureDocBench/review/gt_case_compare_all_fixed7/index.html?cb=puredocbench_gt_bbox_v1_0_0_web_updates)
- Repository file: [`review/gt_case_compare_all_fixed7/index.html`](../review/gt_case_compare_all_fixed7/index.html)
- GitHub issue template: [New GT annotation correction issue](https://github.com/zhihengli-casia/PureDocBench/issues/new?template=annotation_error.yml)

Recommended local launch:

```bash
python3 -m http.server 8767 --directory review/gt_case_compare_all_fixed7
```

Then open:

```text
http://127.0.0.1:8767/index.html?cb=puredocbench_gt_bbox_v1_0_0_web_updates
```

If GitHub Pages is enabled for the repository, the same static app can be published at:

```text
https://zhihengli-casia.github.io/PureDocBench/review/gt_case_compare_all_fixed7/index.html?cb=puredocbench_gt_bbox_v1_0_0_web_updates
```

The repository does not store the full image release. Local launches read `review/gt_case_compare_all_fixed7/assets/images` by default. A GitHub Pages deployment can load images from an unpacked Hugging Face clean-image mirror through `public_image_base_url` or an `imageBase=` query parameter.

## Community Correction Flow

1. Open the review app with the current public annotation version.
2. Find the case with a visible annotation problem.
3. For an existing bbox error, drag or resize the box in the app.
4. For missing annotations, wrong type, duplicate boxes, or reading-order issues, write a case-level correction note.
5. Mark uncertain/problematic items as `Problem` or `Unsure` and add an item note when useful.
6. Click `Export Correction Patch`.
7. Submit the exported JSON in a GitHub issue or pull request.

Maintainers will verify each patch against the clean image and source HTML before batching it into the next GT release.

## Patch Format

The review app exports this schema:

```json
{
  "schema_version": "puredocbench-gt-correction-patch-v1",
  "base_annotation_version": "puredocbench-gt-bbox-v1.0.0",
  "base_internal_token": "maintainer-provenance-token",
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
  --out-root dist/hf_gt_bbox \
  --write-latest
```

7. Upload the generated package to Hugging Face:

```bash
huggingface-cli upload your-org/PureDocBench \
  dist/hf_gt_bbox/puredocbench-gt-bbox-v1.0.0 \
  gt_bbox/versions/puredocbench-gt-bbox-v1.0.0 \
  --repo-type dataset \
  --commit-message "Add GT bbox annotations puredocbench-gt-bbox-v1.0.0"

huggingface-cli upload your-org/PureDocBench \
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
