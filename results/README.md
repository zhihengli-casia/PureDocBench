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

The [interactive leaderboard](../leaderboard.html) defaults to these 58 models. Its separate community view preserves the author-reported NaviDC-OCR result. Current WeVisDoc and OvisOCR2 values come from the supplied evaluation results in these CSV files; earlier external submissions remain in the [historical archive](../data/README.md).

## Metric definitions

Text Edit and Reading Edit are normalized distances (lower is better). Formula CDM and Table TEDS use a 0–100 scale (higher is better). Per-track Overall is `(100 * (1 - TextEdit) + FormulaCDM + TableTEDS) / 3`; Avg3 averages the three track Overalls. Reading order is evaluated separately. Category summaries use the same definitions within each category; their unweighted mean is not a replacement for the global result.

Supplied reference values retain their original decimal precision. Some historical component summaries were rounded before release, so recomputation can differ from reference Overall or Avg3. Both tables and the interactive view use the supplied reference scores, with display rounding only. The main results include all 1,475 pages in each track.

These are released evaluation summaries. This repository update did not rerun inference or rescore the models. Per-model hashes for every historical ground-truth and evaluator version are unavailable; the public `puredocbench-gt-latest` alias therefore does not establish which GT revision produced each historical entry. New evaluations should record the exact GT revision, evaluator revision, page manifest and inference configuration with their results.

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
