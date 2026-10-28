# Current evaluation results

The current release contains **58 models**: 13 pipeline / multi-stage specialists, 19 end-to-end specialists, and 26 general-purpose VLMs. Model families follow the same order as the repository's main table.

| File | Contents |
| --- | --- |
| [leaderboard.csv](leaderboard.csv) | Clean, Digital, Real Overall and Avg3 for 58 models |
| [components.csv](components.csv) | Text Edit, Formula CDM, Table TEDS, Reading Edit and Overall; 174 model–track records |
| [category_components.csv](category_components.csv) | Per-domain components; 1,590 records covering 53 models, 10 domains and 3 tracks |
| [models.json](models.json) | Model names, architecture groups, families, release months and official links |
| [categories.json](categories.json) | Domain names and source-page counts |
| [manifest.json](manifest.json) | Metric definitions, counts and SHA-256 checksums |

The [interactive leaderboard](../leaderboard.html) defaults to these 58 models. Its community view preserves the author-reported NaviDC-OCR result. The main PaddleOCR-VL-1.6 entry uses the rescore below. Current WeVisDoc and OvisOCR2 values come from the supplied evaluation results in these CSV files; earlier external submissions remain in the [historical archive](../data/README.md).

## DocLayoutV3 rescore

Evaluated **2026-10-27 (America/Chicago)** from an externally supplied Markdown prediction bundle labeled **DocLayoutV3**. All **4,425 predictions** were matched: 1,475 each for Clean, Digital and Real, with zero missing or empty outputs. The prediction provider confirmed **[PP-DocLayoutV3](https://huggingface.co/PaddlePaddle/PP-DocLayoutV3) + [PaddleOCR-VL-1.6](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.6)**: layout analysis followed by region recognition. Exact checkpoint revisions and generation settings are awaiting documentation. The existing **PaddleOCR-VL-1.6 main-table row** uses these scores, with the confirmed PP-DocLayoutV3 layout stage recorded in the run metadata. The updated row appears in the default current-results view of the [interactive leaderboard](https://zhihengli-casia.github.io/PureDocBench/leaderboard.html?search=paddleocr-vl-1.6).

| Track | Overall ↑ | TextEdit ↓ | FormulaCDM ↑ | TableTEDS ↑ | ROEdit ↓ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Clean | **72.65** | 0.305 | 64.77 | 83.73 | 0.446 |
| Digital | **67.01** | 0.376 | 61.44 | 77.22 | 0.494 |
| Real | **61.96** | 0.420 | 55.24 | 72.62 | 0.519 |

**Avg₃ = 67.20595803916726**, displayed as **67.21**. Values are aggregated at full precision before display rounding.

| Record | Contents |
| --- | --- |
| [Run metadata](submissions/doclayoutv3/run.json) | Exact GT/evaluator revisions, input hashes, coverage and full-precision overall scores |
| [Track components](submissions/doclayoutv3/components.csv) | Three track records, using the component schema above |
| [Domain components](submissions/doclayoutv3/category_components.csv) | Ten domains × three tracks; blank fields mark inapplicable formula/Overall scores for Certificate |
| [Complete score table](submissions/doclayoutv3/scores.tsv) · [Full-precision JSON](submissions/doclayoutv3/metrics.json) | Global and domain scores |
| [Supplied baseline](submissions/doclayoutv3/original_scores.tsv) · [Run comparison](submissions/doclayoutv3/comparison.tsv) | Original rounded values and differences against this run |
| [Page manifest](submissions/doclayoutv3/page_manifest.csv) · [Input hashes](submissions/doclayoutv3/input_manifest.json) | Exact page mapping and per-page GT/prediction hashes |
| [Verification](submissions/doclayoutv3/verification.json) · [Aggregation checks](submissions/doclayoutv3/aggregation_checks.json) | Input integrity and independently recomputed page means |
| [Python packages](submissions/doclayoutv3/environment_packages.txt) · [System runtime](submissions/doclayoutv3/runtime.json) | Scoring environment |
| [Artifact checksums](submissions/doclayoutv3/checksums.json) | SHA-256 of the files in this result record |

GT: **2026-10-07**, downloaded from [HF revision `4665b40a3333f7643bad7c8675a9062b482511ad`](https://huggingface.co/datasets/zhihengli-casia/puredocbench/blob/4665b40a3333f7643bad7c8675a9062b482511ad/gt/latest.json). Archive SHA-256: `4340c7120be012fe324ce13832c92869dd5eae7d384c473d335a7bed934ab534`.

Evaluator: [OmniDocBench `f133a71e9e91c3621c7ce8994200a7b394a06eb3`](https://github.com/opendatalab/OmniDocBench/tree/f133a71e9e91c3621c7ce8994200a7b394a06eb3), `quick_match`, Python 3.11, macOS, TeX Live 2025 / `pdflatex`. Prediction bytes and GT annotation content were preserved; exported page metadata identifies the track and domain. Per-page text/reading distances use length weighting within each page. CDM/TEDS use arithmetic means within each page, followed by page means.

Per track, TextEdit covers 1,475 pages; CDM covers 224 formula pages and 867 matched formula rows; TEDS covers 1,174 table pages and 3,840 matched tables. Four GT pages have empty `order` annotations, so the evaluator computes ROEdit over **1,471 pages**. See [reading-order coverage](submissions/doclayoutv3/reading_order_coverage.json).

The local libxml2 Unicode-string transport failed on 29 table-scoring instances containing supplementary-plane characters (11 Clean, 10 Digital, 8 Real). Losslessly encoding the same normalized HTML as UTF-8 allowed the original TEDS implementation to score these cases. Both transports produced equal parse trees for all successfully parsed strings. Final TEDS errors and CDM exceptions are zero; [transport checks and corrections](submissions/doclayoutv3/table_transport_checks.json) preserve the evidence.

The supplied baseline has Avg₃ **66.98666666666666**, computed from its rounded Overall values; this run differs by **+0.21929137250059227** points. The baseline's GT and evaluator revisions are unspecified, so this comparison describes two runs whose differences may include GT and runtime effects.

The previous main-table PaddleOCR-VL-1.6 entry (**64.46 / 59.29 / 54.24**, Avg₃ **59.33**) is preserved in the [superseded-result archive](archive/paddleocr_vl_1_6_before_rescore_20261027.json). The original-score TSV linked above records the separately supplied prediction-bundle baseline.

## Metric definitions

Text Edit and Reading Edit are normalized distances (lower is better). Formula CDM and Table TEDS use a 0–100 scale (higher is better). Per-track Overall is `(100 * (1 - TextEdit) + FormulaCDM + TableTEDS) / 3`; Avg3 averages the three track Overalls. Reading order is evaluated separately. Category summaries use the same definitions within each category; their unweighted mean is not a replacement for the global result.

Supplied reference values retain their original decimal precision. Some historical component summaries were rounded before release, so recomputation can differ from reference Overall or Avg3. Both tables and the interactive view use the supplied reference scores, with display rounding only. The main results include all 1,475 pages in each track.

The current 58-model table combines the updated PaddleOCR-VL-1.6 evaluation with the other released scores. Earlier runs retain their supplied precision and provenance. Historical entries have incomplete per-model GT/evaluator version records; exact revisions for the PaddleOCR-VL-1.6 rescore are recorded above. New evaluations should record the exact GT revision, evaluator revision, page manifest and inference configuration with their results.

## Summarize component tables

`summarize.py` uses Python 3.10+ and the standard library. Its input columns are `model_key,track,text_edit,formula_cdm,table_teds,reading_edit`; `overall` and `category` are optional. Every model/category must contain `clean`, `digital` and `real` exactly once.

```bash
python results/summarize.py --input results/components.csv \
  --reference results/leaderboard.csv --output-dir /tmp/puredocbench-summary

python results/summarize.py --input results/category_components.csv \
  --output-dir /tmp/puredocbench-categories
```

For new results, supply the component CSV as `--input` and omit `--reference`. A supplied `overall` is retained, while `overall_recomputed` records the calculation from the available components. `--reference` preserves released track scores and Avg3, with the arithmetic result in separate `*_recomputed` columns. The output also includes track changes relative to Clean and track-averaged components.

## Update the web table

```bash
python results/build_public_leaderboard.py
python results/build_public_leaderboard.py --check
```

The builder validates all result checksums and model/track mappings, then writes [data/leaderboard.js](../data/leaderboard.js). The optional `--readme-table /tmp/leaderboard.html` produces the compact main-table HTML. Model parameters retained from the earlier public table are stored separately in [data/model_parameters.json](../data/model_parameters.json); unspecified parameter counts are displayed as —.
