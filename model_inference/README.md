# PureDocBench Model Inference Toolkit

Optional OCR/document-parsing inference scripts used to generate model predictions for PureDocBench.
Each model has a self-contained `tools/model_infer/<model>_pdbv2.py` runner — no shared base/helpers.

For a public, model-agnostic entrypoint that works with any image-to-Markdown command, use the repository-level CLI documented in `docs/INFERENCE_SCORING.md`:

```bash
puredocbench infer --images <images> --output-dir <predictions> --command-template 'python my_model.py --image {image} --out {output}'
puredocbench score --release-root <release> --pred-dir <predictions> --out-dir <scores>
```

## Repo layout

```
puredocbench/
├── tools/model_infer/<model>_pdbv2.py   # one standalone script per model
├── prompts/<model>_pdbv2.txt            # OCR prompt per model
├── configs/models/<model>_pdbv2.yaml    # env / param manifest per model
├── repro/envs/<env>.txt                 # uv pip freeze per shared env
├── predictions/<model>_pdbv2/           # full-run output (1 .md per image)
├── predictions_degraded/<model>_pdbv2/  # full-run output on degraded dataset
├── outputs_smoke/<model>_pdbv2/         # 5-image smoke test output
└── outputs_smoke_degraded/<model>_pdbv2/
```

## Run a single model on any dataset

Each `*_pdbv2.py` script accepts a unified argparse interface:

```bash
LD_LIBRARY_PATH=<env_lib> CUDA_VISIBLE_DEVICES=<gpu> <env_python>     tools/model_infer/<model>_pdbv2.py     --dataset-dir <abs_path_to_images_dir>     --predictions-root <abs_path_to_output_root>
```

Paths default to local workspace folders and can be overridden with CLI arguments or environment variables.

### Args (all scripts)

- `--smoke` : run only first `--n` images (default 5), output to `--smoke-root` instead
- `--n N` : smoke image count (default 5)
- `--dataset-dir <path>` : input image dir (recursive `*.png`/`*.jpg`/...)
- `--predictions-root <path>` : full-run output root (final = `<root>/<MODEL_SLUG>/`)
- `--smoke-root <path>` : smoke output root

### Args (sharded scripts only — deepseek_ocr_2)

- `--shard ID` `--num-shards N` : mod-based partition for multi-GPU parallel runs

## Env catalog (repro/envs/*.txt)

| env | python | torch | transformers | vllm | used by |
|---|---|---|---|---|---|
| `glmocr_vllm_nightly` | 3.10 | 2.11+cu128 | 5.6 | 0.19.1 | most VL OCR (15 models) |
| `deepseekocr2_vllm_nightly` | 3.10 | 2.11+cu128 | 5.6 | 0.19.2rc1 | deepseek_ocr / step3_vl_10b |
| `step3_vllm_nightly` | 3.10 | 2.11+cu128 | 5.6.2 | 0.19.2rc1.dev208 | (alt for step3, not currently used) |
| `omni_hf_flash` | 3.10 | 2.9.1+cu128 | 4.57.6 | — | minicpm_o_45 (transformers) |
| `ds2_official` | 3.12 | 2.6+cu118 | 4.46.3 | — | deepseek_ocr_2 (transformers, official deps) |

LD_LIBRARY_PATH for vLLM envs can be set through each YAML manifest or the shell environment.

## Model status

| slug | env | notes |
|---|---|---|
| ocrverse_pdbv2 | glmocr_vllm_nightly | golden path (vLLM chat, qwen3_vl arch) |
| dots_ocr_pdbv2 | glmocr_vllm_nightly | |
| dotsmocr_pdbv2 | glmocr_vllm_nightly | |
| fd_rl_pdbv2 | glmocr_vllm_nightly | |
| firered_ocr_pdbv2 | glmocr_vllm_nightly | |
| logics_parsing_v2_pdbv2 | glmocr_vllm_nightly | layout-aware HTML output |
| nanonets_ocr2_3b_pdbv2 | glmocr_vllm_nightly | tie_word_embeddings via hf_overrides |
| ocrflux_3b_pdbv2 | glmocr_vllm_nightly | |
| olmocr_2_7b_pdbv2 | glmocr_vllm_nightly | gmu=0.85 (OOM at 0.92) |
| olmocr_7b_0825_pdbv2 | glmocr_vllm_nightly | gmu=0.85 |
| qianfan_ocr_pdbv2 | glmocr_vllm_nightly | |
| tencent_hunyuan_hunyuanocr_pdbv2 | glmocr_vllm_nightly | |
| step3_vl_10b_pdbv2 | deepseekocr2_vllm_nightly | reasoning model — chat_template patched at /tmp to insert `<think>

</think>

` (skip thinking); enable_thinking=False kwarg in llm.chat |
| minicpm_v_45_pdbv2 | glmocr_vllm_nightly | reasoning model — `enable_thinking=False` passed to apply_chat_template; AutoTokenizer monkey-patched to inject im_start_id/slice_*_id attrs |
| mineru_2_5_pdbv2 | glmocr_vllm_nightly | MinerUClient, needs PYTHONPATH=${MINERU_THIRD_PARTY} |
| mineru_2_5_pro_pdbv2 | glmocr_vllm_nightly | same; max_model_len=8192 (model hard limit) |
| deepseek_ocr_pdbv2 | deepseekocr2_vllm_nightly | NGramPerReqLogitsProcessor + custom extra_args; mm_len=8192 (model limit) |
| deepseek_ocr_2_pdbv2 | ds2_official | transformers 4.46.3 (NOT 4.57); 6-shard parallel; --shard/--num-shards args |
| dolphin_v2_pdbv2 | glmocr_vllm_nightly | (script empty, regenerate if needed) |
| minicpm_o_45_pdbv2 | omni_hf_flash | broken: cuDNN_STATUS_NOT_INITIALIZED (skip until fixed) |

## How to add inference for a new dataset

1. Pick model + GPU. Read the model's yaml manifest for env / params / quirks.
2. Find env python from `python_bin` field; LD_LIBRARY_PATH from `ld_library_path`.
3. Run:

```bash
LD_LIBRARY_PATH=<lib> CUDA_VISIBLE_DEVICES=<gpu> <python>     tools/model_infer/<slug>.py     --dataset-dir /path/to/new_dataset/images     --predictions-root <new_output_root>
```

Output lands at `<new_output_root>/<slug>/<image_stem>.md`.

For multi-GPU sharding (deepseek_ocr_2):

```bash
for s in 0 1 2 3 4 5; do
  CUDA_VISIBLE_DEVICES=$((s/2 + 1)) <python> tools/model_infer/deepseek_ocr_2_pdbv2.py     --shard $s --num-shards 6     --dataset-dir <path> --predictions-root <root> &
done; wait
```

## Smoke test before full

```bash
<python> tools/model_infer/<slug>.py --smoke --n 5     --dataset-dir <path> --smoke-root <smoke_output_root>
```


## Release Notes

This directory was sanitized from the internal inference workspace. It excludes logs, predictions, smoke-test outputs, temporary run folders, and server-specific queue state. Absolute server paths were replaced by environment variables such as `PDB_DATASET_ROOT`, `PDB_MODEL_ROOT`, `PDB_ENV_ROOT`, `PDB_TMPDIR`, and `MINERU_THIRD_PARTY`. Model weights are not included in the dataset release.
