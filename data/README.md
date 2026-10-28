# Leaderboard data and historical submissions

The [current result tables](../results/README.md) cover 58 evaluated models. The interactive leaderboard displays them by default and offers a community-results filter for NaviDC-OCR and the DocLayoutV3 rescore. Community entries identify author-reported scores or maintainer recomputation of submitted predictions, with their respective provenance.

| File | Role |
| --- | --- |
| [leaderboard.js](leaderboard.js) | Generated browser data: 58 current entries and two community entries |
| [community_results.json](community_results.json) | NaviDC-OCR's author-reported values and the maintainer-rescored DocLayoutV3 submission |
| [model_parameters.json](model_parameters.json) | Parameter counts retained from the public table or explicitly stated in model names |
| [archive/leaderboard-2026-09-21.json](archive/leaderboard-2026-09-21.json) | The previous public table's 44 entries, including superseded results |
| [wevisdoc_results.tsv](wevisdoc_results.tsv) | Original WeVisDoc submission, preserved byte for byte |
| [archive/wevisdoc-2026-09-21.md](archive/wevisdoc-2026-09-21.md) | Source references and evaluation notes that accompanied that submission |

## Current and historical values

The current WeVisDoc-2B/4B and OvisOCR2 rows use the supplied evaluation results in `results/`. Their earlier author-reported values remain in the historical files above. The original WeVisDoc TSV contains 66 rows: 10 domains plus `ALL`, three tracks, and five metrics. Its submitted three-run averages have Avg3 values of 73.86 (2B) and 75.54 (4B), while the current evaluation values are 73.69 and 75.57. These are separate result records; the original TSV has not been overwritten or relabeled.

The current model set includes PaddleOCR-VL-1.6 and reports OpenDoc-0.1B (UniRec) once. The earlier PaddleOCR-VL-1.5 and standalone UniRec records are preserved in the archive. OpenOCR remains a separate text-recognition pipeline.

NaviDC-OCR's values come from its [official repository](https://github.com/caipeng328/NaviDC-OCR#puredocbench). The source reports Text Edit, Formula CDM and Table TEDS for each track, with Reading Edit unavailable. The entry is marked **Community · author-reported** and remains outside the 58-model current evaluation set. Exact GT/evaluator revisions are unspecified for this community summary.

The [DocLayoutV3 submission](../results/README.md#doclayoutv3-rescore) was rescored on 2026-10-27 using HF GT `2026-10-07` and a pinned OmniDocBench revision. It is marked **Community · maintainer-rescored**, with Avg₃ **67.21**, complete components and ten-domain results. The prediction provider confirmed **PP-DocLayoutV3 + PaddleOCR-VL-1.6**, a **Pipeline** entry whose model link opens the official PaddleOCR-VL-1.6 page. Exact checkpoint revisions and generation settings are awaiting documentation; full-pipeline parameter count and release month remain unspecified.

The historical archive files originate from public repository commit `1d4abd6`. The archived JSON columns are `model, architecture, params, url, clean_overall, clean_text_edit, clean_formula_cdm, clean_table_teds, clean_reading_edit, digital_overall, digital_text_edit, digital_formula_cdm, digital_table_teds, digital_reading_edit, real_overall, real_text_edit, real_formula_cdm, real_table_teds, real_reading_edit, avg3`. A JSON `null` means the metric was unreported.

Historical scoring inputs are preserved. Newly rescored submissions include the version and verification records linked above. Ground-truth revisions and the limits of historical provenance are described with the [current results](../results/README.md#metric-definitions).
