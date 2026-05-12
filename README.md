# PureDocBench

<p align="center">
  <strong>How far is document parsing from solved?</strong><br>
  A source-traceable benchmark for OCR and document parsing across clean, digitally degraded, and real-degraded document settings.
</p>

<p align="center">
  <a href="https://huggingface.co/datasets/zhihengli-casia/puredocbench"><img alt="Hugging Face Dataset" src="https://img.shields.io/badge/Dataset-Hugging%20Face-yellow"></a>
  <a href="LICENSE_DATA"><img alt="Data License" src="https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey"></a>
  <a href="LICENSE"><img alt="Code License" src="https://img.shields.io/badge/Code-MIT-green"></a>
  <a href="https://arxiv.org/abs/2605.07492"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2605.07492-b31b1b"></a>
</p>

<p align="center">
  <a href="docs/README_ZH.md">Chinese README</a> |
  <a href="https://huggingface.co/datasets/zhihengli-casia/puredocbench">Dataset</a> |
  <a href="https://arxiv.org/abs/2605.07492">Paper</a>
</p>

PureDocBench uses HTML/CSS document sources as hidden anchors: each page is rendered into images and annotated from the same structured source. This gives a benchmark where text, tables, formulas, captions, and reading order can be scored with less post-hoc annotation noise.

<p align="center">
  <img src="assets/figures/fig3_data_overview_final.png" alt="PureDocBench overview" width="92%">
</p>

## At A Glance

| Item | Count |
|---|---:|
| Official pages | 1,475 |
| Official images | 4,425 |
| Top-level domains | 10 |
| Fine-grained subcategories | 66 |
| Image tracks | clean, digital-degraded, real-degraded |
| Scored structures | text, formulas, tables, reading order |

## Main Leaderboard

The paper evaluates 40 systems across pipeline specialists, end-to-end document parsers, and general-purpose VLMs. Table 2 is the main leaderboard: each track reports Overall, TextEdit, FormulaCDM, TableTEDS, and ROEdit; Avg3 averages the three track Overall scores.

<p align="center">
  <img src="assets/figures/table_main_leaderboard.png" alt="Table 2: three-track leaderboard on PureDocBench" width="98%">
</p>

## Diagnostics

The diagnostic panel shows where current systems still have headroom. Formula recognition is the largest single bottleneck, and real degradation changes rankings more sharply than digital degradation.

<p align="center">
  <img src="assets/figures/fig_diagnostic_panels.png" alt="Diagnostic panels" width="96%">
</p>

## Case Studies

The four case studies below are all taken from the paper. They show failures that aggregate scores can hide: notation loss, reading-order mistakes, annotation contamination, table-structure errors, character-level corruption, and missing visual authentication cues.

### Case 1: Academic

<p align="center">
  <img src="assets/figures/fig_case_study_academic.png" alt="Case study 1: academic structured lab report" width="96%">
</p>

### Case 2: Business

<p align="center">
  <img src="assets/figures/fig_case_study_business.png" alt="Case study 2: business product specification table" width="96%">
</p>

### Case 3: Finance

<p align="center">
  <img src="assets/figures/fig_case_study_actuarial.png" alt="Case study 3: finance actuarial valuation report" width="96%">
</p>

### Case 4: Certificate

<p align="center">
  <img src="assets/figures/fig_case_study_certificate.png" alt="Case study 4: Chinese product quality certificate" width="96%">
</p>

## Appendix Highlights

The appendix documents the degradation design and per-category behavior used to make the benchmark reproducible.

<p align="center">
  <img src="assets/figures/fig_degradation_ops.png" alt="Degradation operations" width="96%">
</p>

<p align="center">
  <img src="assets/figures/fig_degradation_scenarios.png" alt="Degradation scenarios" width="96%">
</p>

<p align="center">
  <img src="assets/figures/fig_per_category_overview.png" alt="Per-category overview" width="92%">
</p>

## Download

The full image/GT/HTML release is hosted on Hugging Face:

```bash
# After downloading all files from Hugging Face:
shasum -a 256 -c SHA256SUMS.txt
cat pdb_full.tar.part-* | tar -xf -
```

Verify the split archive and reconstructed release:

```bash
python scripts/verify_split_archive.py /path/to/downloaded/files

python scripts/validate_release_manifest.py \
  --release-root /path/to/puredocbench-v1.0 \
  --manifest manifests/release_manifest_candidate_1475.csv
```

## Inference And Scoring

PureDocBench includes a public CLI for model-agnostic inference, fast lightweight scoring, and OmniDocBench-aligned evaluation. Use `puredocbench score` for quick sanity checks; use `puredocbench score-omnidocbench` with an OmniDocBench checkout for platform-aligned CDM/TEDS numbers.

```bash
pip install -e .

puredocbench infer \
  --images /path/to/puredocbench-v1.0/images/clean \
  --output-dir predictions/my_model_clean \
  --command-template 'python my_model_infer.py --image {image} --out {output}'

puredocbench score \
  --release-root /path/to/puredocbench-v1.0 \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --pred-dir predictions/my_model_clean \
  --track clean \
  --limit 20 \
  --out-dir scores/my_model_clean

puredocbench score-omnidocbench \
  --release-root /path/to/puredocbench-v1.0 \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --pred-dir predictions/my_model_clean \
  --track clean \
  --omnidocbench-root /path/to/OmniDocBench \
  --out-dir omnidocbench_scores/my_model_clean
```

See [docs/INFERENCE_SCORING.md](docs/INFERENCE_SCORING.md) for the full interface and evaluator-version notes.

## Repository Contents

```text
manifests/                         Release and sample manifests
metadata/                          Dataset card and Croissant metadata
scripts/                           Rendering, degradation, validation, leaderboard tools
puredocbench/                      Public inference, scoring, and OmniDocBench export CLI
model_inference/                   Sanitized model inference configs and runners
supplemental_inference_scoring/    API/local inference and scoring utilities
assets/figures/                    Figures from the paper
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Render one HTML page:

```bash
python scripts/render_single_image.py \
  --html /path/to/page.html \
  --out /path/to/page.png \
  --dpi 300
```

Apply a deterministic degradation profile:

```bash
python scripts/apply_degradation_ablation.py \
  --input /path/to/clean_images \
  --output /path/to/degraded_images \
  --profile full_medium
```

## License

- Dataset assets are released under **CC BY 4.0**; see [LICENSE_DATA](LICENSE_DATA).
- Code in this repository is released under the license in [LICENSE](LICENSE).
- Model weights are not redistributed.

## Citation

```bibtex
@article{li2026puredocbench,
  title   = {How Far Is Document Parsing from Solved? PureDocBench: A Source-Traceable Benchmark across Clean, Degraded, and Real-World Settings},
  author  = {Li, Zhiheng and Ma, Zongyang and Chen, Jiaxian and Zhang, Jianing and Su, Zhaolong and Zhang, Yutong and Yu, Zhiyin and Liu, Ruiqi and Lv, Xiaolei and Li, Bo and Gao, Jun and Zhang, Ziqi and Yuan, Chunfeng and Li, Bing and Hu, Weiming},
  journal = {arXiv preprint arXiv:2605.07492},
  year    = {2026},
  doi     = {10.48550/arXiv.2605.07492},
  url     = {https://arxiv.org/abs/2605.07492}
}
```
