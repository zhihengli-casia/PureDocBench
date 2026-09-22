# Supplementary leaderboard results

## WeVisDoc (2026-09-21)

[`wevisdoc_results.tsv`](wevisdoc_results.tsv) contains the submitted results for **WeVisDoc-2B** and **WeVisDoc-4B**: 66 rows covering 10 domains plus `ALL`, three image tracks, and five metrics (`Overall`, `TextEdit`, `FormulaCDM`, `TableTEDS`, and `ROEdit`). The original file is preserved byte for byte. Its `2B` and `4B` labels map to WeVisDoc-2B and WeVisDoc-4B, respectively.

These are author-reported results. The six `ALL` rows match the component results in [Table 3 of the WeVisDoc paper](https://arxiv.org/html/2609.20423v1#S4.T3). The paper reports scores averaged over three inference runs. Exact ground-truth and evaluator revisions and the evaluated page manifest are unspecified. The submitted summary does not contain page-level predictions or per-run scores. Per-domain component metrics are provided by the submitted TSV; the paper cross-check covers the `ALL` aggregates.

The leaderboard uses the `ALL` rows directly. Avg3 is the arithmetic mean of the three track Overall scores, rounded to two decimal places: **73.86** for WeVisDoc-2B and **75.54** for WeVisDoc-4B. `TextEdit` and `ROEdit` are lower-is-better; the other metrics are higher-is-better.

Sources:

- [Official WeVisDoc repository, pinned revision](https://github.com/Tencent/WeVisDoc/blob/bcbc0eacb976ecb8d69675fe6bcee123f5640777/README.md#puredocbench)
- [WeVisDoc-2B model card, pinned revision](https://huggingface.co/tencent/WeVisDoc-2B/blob/86ecb7330566296b695d4f91aea807a260cc84a7/README.md#puredocbench)
- [WeVisDoc-4B model card, pinned revision](https://huggingface.co/tencent/WeVisDoc-4B/blob/1754bfa79ba1a6e24aacc001da2e7bb39b9fbc34/README.md#puredocbench)
- [WeVisDoc technical report v1: evaluation protocol](https://arxiv.org/html/2609.20423v1#S3.SS4.SSS3)

The 40 original paper baselines retain their published values. These supplementary entries record the authors’ evaluation results; no new inference or rescoring was performed for this leaderboard update.
