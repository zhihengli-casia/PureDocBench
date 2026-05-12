# PureDocBench — 推理复现指南（internal inference session）

记录这次 session 在 internal（`<internal-server>`）上经手过的模型推理：脚本、环境、启动命令、已知问题。每条都验证过能跑通。

## 通用约定

```
REPO=${PDB_SUPPLEMENTAL_ROOT}
PDBV2_JSON=${PDB_MANIFEST_JSON}
PDBV2_IMAGES_ROOT=${PDB_DATASET_ROOT}/images/clean               # clean
PDBV2_IMAGES_ROOT=${PDB_DATASET_ROOT}/images/digital_degraded   # deg
PDBV2_PRED_ROOT=predictions          # clean -> $REPO/predictions/<slug>/
PDBV2_PRED_ROOT=predictions_degraded # deg
```

每个推理脚本都支持 `--smoke --n N` 抽样测试，full 模式 resume by md exists。Tmux 包装（避免 SSH 断开）：

```bash
tmux new-session -d -s <slug>_full "
  export CUDA_VISIBLE_DEVICES=0  # 按需改
  export PDBV2_IMAGES_ROOT=...   # 按需 clean/deg
  export PDBV2_PRED_ROOT=...
  cd $REPO
  $PYTHON -u tools/model_infer/<slug>.py 2>&1 | tee ${PDB_LOG_ROOT:-logs}/<slug>.log
"
```

## Env 总览

| Env | 路径 | freeze | 核心包 | 谁用 |
|---|---|---|---|---|
| `vllm_qwen3` | `${PDB_ENV_ROOT}/vllm_qwen3` | `repro/envs/_vllm_qwen3.txt` (177 行) | vllm 0.19.1, transformers 4.51, torch 2.6 | 所有 vLLM 0.19.1 模型 + dolphin + API client |
| `monkey_env` | `${PDB_ENV_ROOT}/monkey_env` | `repro/envs/_monkey_env.txt` (197 行) | magic_pdf, transformers 4.51.1, vllm 0.8.5 | monkey 系列 |
| `youtu_parsing` | `${PDB_ENV_ROOT}/youtu_parsing` | `repro/envs/_youtu_parsing.txt` (52 行) | torch 2.6, transformers 4.51.3, youtu-hf-parser 0.1.0 | youtu_parsing |
| `paddle_vl` | `${PDB_ENV_ROOT}/paddle_vl` | `repro/envs/_paddle_vl.txt` (106 行) | paddleocr 3.5, paddlepaddle-gpu 3.3.1 | paddle 1.0 + 1.5 pipeline 客户端 |

**LD_LIBRARY_PATH 注意**：vllm_qwen3 跑 vLLM 时必须加 `export LD_LIBRARY_PATH=${PDB_VLLM_LIB:-}`（NCCL/CUDA libs），否则 vllm 起不来。

## 1. Qwen3.5 系列（vLLM 0.19.1，单卡）

模型：`qwen3_5_0_8b`、`qwen3_5_2b`、`qwen3_5_4b`、`qwen3_5_9b`

- 脚本：`tools/model_infer/<slug>.py`
- yaml：`configs/models/<slug>.yaml`（vLLM serve 配置）
- prompt：`prompts/<slug>.txt`
- env：`vllm_qwen3`
- freeze：`repro/envs/<slug>.txt` (per-model 184 行)

启动：

```bash
PY=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
export LD_LIBRARY_PATH=${PDB_VLLM_LIB:-}
export CUDA_VISIBLE_DEVICES=0     # 单卡
export TMPDIR=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp}
export HF_HOME=${HF_HOME:-.cache/huggingface}
export VLLM_NO_USAGE_STATS=1
cd $REPO
$PY -u tools/model_infer/qwen3_5_2b.py    # smoke: 加 --smoke --n 5
```

脚本内部直接 `from vllm import LLM` 起 in-process engine，单卡 `tensor_parallel_size=1`，按 chunk 跑（mm_len 24576）。

## 2. Qwen3-VL Instruct 系列（vLLM 0.19.1）

模型：`qwen3_vl_2b_instruct`、`qwen3_vl_4b_instruct`、`qwen3_vl_8b_instruct`

- 脚本/yaml/prompt/env/freeze 命名同 Qwen3.5 系列
- **已知坑**：宽高比 > 100 的图会让 vLLM processor 异常 → kill 整个 engine。脚本内已加过滤（看代码 `aspect_ratio` 检查）

启动方式同 Qwen3.5 系列。

## 3. Monkey-Pro 系列（magic_pdf SDK，pipeline 模式）

模型：`monkey_pro_1_2b`、`monkey_pro_3b`

- 脚本：`tools/model_infer/<slug>.py`
- yaml：`configs/models/<slug>_inference.yaml`（magic_pdf 内部 config，路径模型权重）
- env：`monkey_env`
- 权重：`${PDB_MODEL_ROOT}/MonkeyOCR-pro-{1.2B,3B}/`（Structure / Relation / Recognition 三个）

启动：

```bash
PY=${PDB_ENV_ROOT}/monkey_env/bin/python
export CUDA_VISIBLE_DEVICES=0
cd $REPO
$PY -u tools/model_infer/monkey_pro_1_2b.py    # 同 monkey_pro_3b
```

每张图 SDK 内部 layout → 元素 → recognition 三阶段，单图 ~2-15s。

## 4. youtu_parsing（transformers，单卡）

- 脚本：`tools/model_infer/youtu_parsing.py`
- env：`youtu_parsing`
- 权重：`${PDB_MODEL_ROOT}/Youtu-Parsing/`（`youtu-hf-parser`/`youtu-parsing-utils` 配套）

启动：

```bash
PY=${PDB_ENV_ROOT}/youtu_parsing/bin/python
export CUDA_VISIBLE_DEVICES=0
cd $REPO
$PY tools/model_infer/youtu_parsing.py \
    --image-root ${PDB_DATASET_ROOT}/images/clean \
    --save-dir $REPO/predictions/youtu_parsing \
    --image-list ${PDB_IMAGE_LIST_ROOT}/image_list_pdb.txt
```

**慢**：~0.013 pages/s（~75s/张），全量 1474 张要 30+h。

## 5. dolphin_v2（vLLM 0.19.1，可双卡分片）

- 脚本：`tools/model_infer/dolphin_v2.py`
- yaml：`configs/models/dolphin_v2.yaml`
- env：`vllm_qwen3`
- 权重：`${PDB_MODEL_ROOT}/dolphin_v2/`

启动（单卡）：

```bash
PY=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
export LD_LIBRARY_PATH=${PDB_VLLM_LIB:-}
export CUDA_VISIBLE_DEVICES=0
export TMPDIR=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp}
cd $REPO
$PY tools/model_infer/dolphin_v2.py \
    --image-root ${PDB_DATASET_ROOT}/images/clean \
    --pred-dir $REPO/predictions/dolphin_v2 \
    --tensor-parallel-size 1 --gpu-memory-utilization 0.85
```

双卡：起两份脚本各 `CUDA_VISIBLE_DEVICES=1` 和 `=2`，写同一 `--pred-dir`，resume 自然分工。

## 6. SiliconFlow API 5 个

模型：`kimi_k2_6`、`qwen3_5_27b`、`qwen3_5_122b_a10b`、`qwen3_5_35b_a3b`、`qwen3_5_397b_a17b`

- 脚本：`tools/api_infer/<slug>.py`（async httpx，resume 友好，重试 4 次指数退避）
- prompt：`prompts/<slug>.txt`
- env：用 `vllm_qwen3` 跑（只需要 httpx）
- 输出位置：`predictions/api/<slug>/`（注意子目录 `api/`）

`.env`（**不进 git**）：

```
SILICONFLOW_API_KEY=<填>
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
```

启动：

```bash
PY=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
cd $REPO
$PY tools/api_infer/kimi_k2_6.py --concurrency 8        # 默认全 1474 张，resume 跳过已 done
```

**已知**：高峰期 ReadTimeout / 503 频发。低峰期 conc=8 比较稳；conc=16 会触发限流。kimi/27b 在某些 case 上会持续 503，重试无效（API 端识别后拒绝）。

## 7. PaddleOCR-VL 1.0 + 1.5（pipeline + vLLM serve）

这次 session 从 0 搭的最复杂的一条链。**两阶段**：

### 7.1 启动 vllm serve（持久化跑）

paddle 1.5（GPU 2，port 8015）：

```bash
PY=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
tmux new-session -d -s vllm_paddle_1_5 "
  export CUDA_VISIBLE_DEVICES=2
  export LD_LIBRARY_PATH=${PDB_VLLM_LIB:-}
  export TMPDIR=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp}
  export HF_HOME=${HF_HOME:-.cache/huggingface}
  export VLLM_NO_USAGE_STATS=1
  $PY -m vllm.entrypoints.openai.api_server \
      --model ${PDB_MODEL_ROOT}/PaddleOCR-VL-1.5 \
      --served-model-name PaddleOCR-VL-1.5-0.9B \
      --trust-remote-code \
      --max-num-batched-tokens 16384 \
      --no-enable-prefix-caching \
      --mm-processor-cache-gb 0 \
      --gpu-memory-utilization 0.85 \
      --port 8015
"
```

paddle 1.0（GPU 1，port 8011）：

```bash
tmux new-session -d -s vllm_paddle_1_0 "
  export CUDA_VISIBLE_DEVICES=1
  export LD_LIBRARY_PATH=${PDB_VLLM_LIB:-}
  ...（同上）
  $PY -m vllm.entrypoints.openai.api_server \
      --model ${PDB_MODEL_ROOT}/PaddleOCR-VL \
      --served-model-name PaddleOCR-VL-0.9B \
      （余下参数同 1.5）\
      --port 8011
"
```

权重：`${PDB_MODEL_ROOT}/PaddleOCR-VL{,-1.5}/`（tmpfs，避免 cfs-fuse 文件丢失，从 modelscope `PaddlePaddle/PaddleOCR-VL{,-1.5}` 下载）。

`served-model-name` **必须设**（pipeline v1 期待 `PaddleOCR-VL-0.9B`、v1.5 期待 `PaddleOCR-VL-1.5-0.9B`，看 `paddlex/configs/pipelines/PaddleOCR-VL{,-1.5}.yaml` 内 `vl_recognition.model_name`）。

### 7.2 启动 pipeline 客户端

```bash
PY=${PDB_ENV_ROOT}/paddle_vl/bin/python   # 注意是 paddle_vl env 不是 vllm_qwen3
cd $REPO
# paddle 1.5
$PY -u tools/api_infer/paddleocr_vl_1_5_pipeline.py --concurrency 32
# paddle 1.0
$PY -u tools/api_infer/paddleocr_vl_pipeline.py --concurrency 32
```

脚本内部：
- pipeline_version 写死（v1 或 v1.5）
- `vl_rec_max_concurrency=32` 让 pipeline 内部并发请求 vllm
- chunked 处理（CHUNK=32）— 每批完后落 .md，可见进度，可中断 resume

### 7.3 后处理 normalize

paddle 输出格式跟 GT 偏离（每个上下标都被 `$ ^{...} $` 包，table 带 inline style 等），用 `tools/post_process/paddle_normalize.py` normalize：

```bash
$PY tools/post_process/paddle_normalize.py \
    predictions/paddleocr_vl_1_5 \
    predictions/paddleocr_vl_1_5_norm
```

normalize 规则（按官方 vLLM recipe 严格对齐 + GT 风格）：
- 去 LaTeX 两端空格 `$ x $` → `$x$`
- 简单 LaTeX → unicode：`\dagger` → `†`、`\Delta` → `Δ`、`\pm` → `±` 等
- 数字+符号上下标 → unicode：`^{1-3}` → `¹⁻³`、`_{2}` → `₂`
- 字母上下标保留 LaTeX（GT 也用 `E_a` 这种）
- table HTML：`<table>` → `<table border="1">`，第一行 `<td>` → `<th>`

**已知**：normalize 对评分提升微弱（0.02-0.07），主要 paddle vl 模型 LaTeX 化输出风格根本性差异。**paddle 1.0 的失败是 PP-DocLayoutV2 + VL 1.0 自身能力限制**（多张 case layout 漏检 → 0 字节输出），换 V3 layout 是 hack，未在线上做。

## 已知 Pitfalls

1. **cfs-fuse 写文件 null bytes**：写权重/脚本到 cfs-fuse 路径偶尔会损坏（变 null bytes 文件），写完用 `ast.parse` 或 `head -c` 验证；权重一律放 tmpfs `${PDB_TMP_ROOT}/`。
2. **vllm 0.19.1 detokenize bug**：某些模型（如 deepseek_ocr）出 GPT-2 byte-level token，需用 vLLM nightly 0.19.2rc1 替代（`deepseekocr2_vllm_nightly` env，本次未用到 deepseek）。
3. **vLLM spawn worker 不释放**：kill -9 父进程后 GPU 不释放，需 `pkill -9 -f multiprocessing.spawn`。
4. **多 chain tmux 间 pkill 误杀**：用精准 PID kill 而非广 pkill。
5. **uv install 卡死**：网络不稳定从 wheels.vllm.ai 拉 nightly 时偶发，`UV_CACHE_DIR=${PDB_TMP_ROOT}/...` 走 tmpfs cache 加 `--index-url https://pypi.tuna.tsinghua.edu.cn/simple` + `--extra-index-url` 副源能避大多数。
6. **API 余额 / 限流**：SiliconFlow 高峰 503 / ReadTimeout 频发；conc=8 是稳态上限。

## 复现 Checklist（新机器从头）

1. clone 本 repo，准备 `.env`、IMAGES、PDBV2_JSON
2. 安装 uv（已有 `uv`）
3. 按 envs 表建对应 venv：`uv venv <env>` + `uv pip install -r repro/envs/_<env>.txt`
4. 下载权重到 `${PDB_TMP_ROOT:-/tmp/pdbv2}/`（PaddleOCR-VL 走 modelscope；其他官方按 README）
5. 验证 import：每个 env `bin/python -c "import vllm; import torch; print(torch.cuda.is_available())"`
6. 起 tmux + smoke `--smoke --n 5`
7. smoke 通过后跑 full
