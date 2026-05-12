# Inference And Scoring

This repository includes a small public CLI so users do not need to depend on the original internal server layout.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

You can then run either:

```bash
puredocbench --help
python -m puredocbench --help
```

## Run Inference

`puredocbench infer` is model-agnostic. It recursively scans an image directory and calls your command once per image. Your command should write one Markdown file to `{output}`.

```bash
puredocbench infer \
  --images /path/to/puredocbench-v1.0/images/clean \
  --output-dir predictions/my_model_clean \
  --command-template 'python my_model_infer.py --image {image} --out {output}' \
  --workers 4
```

If your command needs shell features such as inline environment variables, pipes, or redirection, add `--shell`:

```bash
puredocbench infer \
  --images /path/to/images \
  --output-dir predictions/my_model \
  --command-template 'CUDA_VISIBLE_DEVICES=0 python my_model_infer.py --image "{image}" --out "{output}"' \
  --shell
```

Available placeholders:

| Placeholder | Meaning |
|---|---|
| `{image}` | Absolute or relative path to the current image |
| `{output}` | Target `.md` prediction path |
| `{output_dir}` | Parent directory of `{output}` |
| `{stem}` | Image filename stem |
| `{relpath}` | Image path relative to `--images` |

Useful dry run:

```bash
puredocbench infer \
  --images /path/to/images \
  --output-dir predictions/my_model \
  --command-template 'python my_model_infer.py --image {image} --out {output}' \
  --limit 3 \
  --dry-run
```

## Fast Sanity Scoring

The bundled scorer is a lightweight public scorer for fast development and sanity checks. It compares Markdown predictions against source-derived GT text, formula, table, and reading-order targets.

```bash
puredocbench score \
  --release-root /path/to/puredocbench-v1.0 \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --track clean \
  --pred-dir predictions/my_model_clean \
  --limit 20 \
  --out-dir scores/my_model_clean
```

Outputs:

```text
scores/my_model_clean/
├── page_metrics.csv
├── report.md
└── summary.json
```

The summary contains percentage-style scores:

- `overall_score`
- `text_score`
- `formula_score`
- `table_score`
- `reading_order_score`

This scorer is intentionally dependency-light and is not a byte-for-byte replacement for OmniDocBench. Use it to catch missing files, path mismatches, and obvious model failures quickly.

## Platform-Aligned OmniDocBench Scoring

For leaderboard-style numbers, run the same OmniDocBench evaluator family used by the platform. Current platform deployments use an OmniDocBench main-branch evaluator, so FormulaCDM and TableTEDS may differ from older frozen evaluator snapshots even when TextEdit and ROEdit match.

Recommended smoke test:

```bash
git clone https://github.com/opendatalab/OmniDocBench.git third_party/OmniDocBench

puredocbench score-omnidocbench \
  --release-root /path/to/puredocbench-v1.0 \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --track clean \
  --pred-dir predictions/my_model_clean \
  --limit 20 \
  --omnidocbench-root third_party/OmniDocBench \
  --out-dir omnidocbench_scores/my_model_clean_smoke
```

Full-track scoring:

```bash
puredocbench score-omnidocbench \
  --release-root /path/to/puredocbench-v1.0 \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --track clean \
  --pred-dir predictions/my_model_clean \
  --strict \
  --omnidocbench-root third_party/OmniDocBench \
  --out-dir omnidocbench_scores/my_model_clean
```

The command first writes OmniDocBench-ready inputs, then runs:

```bash
python /path/to/OmniDocBench/pdf_validation.py \
  --config omnidocbench_scores/my_model_clean/omnidocbench_config.yaml
```

You can also export the inputs without running the evaluator:

```bash
puredocbench export-omnidocbench \
  --release-root /path/to/puredocbench-v1.0 \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --track clean \
  --pred-dir predictions/my_model_clean \
  --out-dir omnidocbench_inputs/my_model_clean
```

This writes:

```text
omnidocbench_inputs/my_model_clean/
├── gt.json
├── omnidocbench_config.yaml
└── predictions/
```

Use the same OmniDocBench checkout for every model in a comparison. That is the important alignment point: CDM/TEDS are evaluator-version-sensitive, while TextEdit/ROEdit are much less sensitive.
