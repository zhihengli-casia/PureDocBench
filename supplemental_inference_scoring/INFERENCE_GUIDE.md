# Inference Guide — Run on a New Dataset

本指南说明如何用 `puredocbench` 仓库对**新数据集**做推理。所有推理脚本已经支持环境变量切换数据集，**无需修改代码**。

---

## 1. 数据集格式要求

### 1.1 图片
- 任意目录结构，递归查找 `.png` / `.jpg` / `.jpeg`
- 通过 basename 与 manifest 对齐

### 1.2 Manifest JSON
最小要求格式：
```json
[
  {"page_info": {"image_path": "doc_001.png"}},
  {"page_info": {"image_path": "doc_002.png"}},
  ...
]
```

> Tip：可参考 `${PDB_MANIFEST_JSON}` 作为模板。

---

## 2. 配置环境变量

```bash
# 数据集
export PDBV2_IMAGES_ROOT=/path/to/new_dataset/images
export PDBV2_JSON=/path/to/new_dataset/manifest.json

# 输出（如不设则用默认 predictions/ 与 outputs_smoke/）
export PDBV2_PRED_ROOT=predictions_NEW          # 输出 -> predictions_NEW/<slug>/
export PDBV2_SMOKE_ROOT=outputs_smoke_NEW       # smoke -> outputs_smoke_NEW/<slug>/

# tmpfs / cache（推荐）
export TMPDIR=${PDB_TMP_ROOT}/ocr_tmp
export TORCHINDUCTOR_CACHE_DIR=${PDB_TMP_ROOT}/torch_inductor_cache
export VLLM_CACHE_ROOT=${PDB_TMP_ROOT}/vllm_cache
export TRITON_CACHE_DIR=${PDB_TMP_ROOT}/triton_cache
export VLLM_NO_USAGE_STATS=1
```

---

## 3. 启动单模型推理

每个模型有**独立 standalone 脚本**（不共享 helper）+ 对应 env。

### 3.1 通用模式（local vLLM）

```bash
ENV_PY=${PDB_TMP_ROOT}/envs/vllm_qwen3/bin/python      # 见 ENVS_MAPPING.md
SLUG=qwen3_5_9b

# Smoke (5 张验证)
CUDA_VISIBLE_DEVICES=0 $ENV_PY tools/model_infer/$SLUG.py --smoke --n 5

# Full (全集，自动 resume by md)
CUDA_VISIBLE_DEVICES=0 $ENV_PY tools/model_infer/$SLUG.py
```

### 3.2 Monkey 系列（不同 env）

```bash
ENV_PY=${PDB_TMP_ROOT}/monkey_env/bin/python
CUDA_VISIBLE_DEVICES=0 $ENV_PY tools/model_infer/monkey_pro_1_2b.py
```

### 3.3 SiliconFlow API

```bash
# .env 文件设 SILICONFLOW_API_KEY
export SILICONFLOW_API_KEY=REPLACE_ME

ENV_PY=${PDB_TMP_ROOT}/envs/vllm_qwen3/bin/python
$ENV_PY tools/api_infer/qwen3_5_397b_a17b.py --concurrency 8
```

> Concurrency 建议从 conc=8 起步，撞 TPM 后降至 conc=2-4。

### 3.4 youtu_parsing（argparse 参数式）

```bash
ENV_PY=${PDB_TMP_ROOT}/envs/youtu_parsing/bin/python
$ENV_PY tools/model_infer/youtu_parsing.py \
  --image-root $PDBV2_IMAGES_ROOT \
  --save-dir predictions/youtu_parsing \
  --image-list <list.txt>
```

### 3.5 dolphin_v2（two-stage pipeline）

```bash
ENV_PY=${PDB_TMP_ROOT}/envs/vllm_qwen3/bin/python
$ENV_PY tools/model_infer/dolphin_v2.py \
  --image-root $PDBV2_IMAGES_ROOT \
  --pred-dir predictions/dolphin_v2 \
  --tensor-parallel-size 1 \
  --gpu-memory-utilization 0.85
```

---

## 4. 多 GPU 并行 chain

仓库提供 chain launcher，单 GPU 串行多个模型：

```bash
# scripts/_runner/run_deg_gpu.sh — 默认数据集 = degraded_v2_merged
# 需要新数据集时手动 export PDBV2_IMAGES_ROOT 或者修 launcher 开头硬编码
tmux new -d -s pdbv2_gpu0 -c ${PDB_SUPPLEMENTAL_ROOT} \
  'export PDBV2_IMAGES_ROOT=/path/to/new; \
   bash scripts/_runner/run_deg_gpu.sh 0 qwen3_5_9b qwen3_vl_8b_instruct'
```

每个任务自动 smoke (5 张) → 通过转 full → cleanup → 下一个任务。

---

## 5. 输出格式

每个模型输出到 `<PDBV2_PRED_ROOT>/<slug>/<basename_no_ext>.md`，1 张图 1 个 markdown。

例：`predictions_NEW/qwen3_5_9b/doc_001.md`

---

## 6. Resume 行为

所有脚本启动时扫描输出目录，跳过已存在的 .md。中断重启不会重复推理。

---

## 7. 需要做的检查（新数据集启动前）

1. **manifest JSON 格式**：确保 `page_info.image_path` 字段是图片 basename
2. **图片可读**：`find $PDBV2_IMAGES_ROOT -name '*.png' | wc -l` 与 manifest 长度对齐
3. **GPU 可用**：`nvidia-smi`，权重要 `<gpu_memory_utilization>×80GB` 余量
4. **磁盘空间**：每模型 1474 张 .md ≈ 30 MB；system disk别满（推荐 cache 重定向到 tmpfs/local scratch）
5. **smoke 5 张**：跑通后再 full

---

## 8. 已知坑

- **cfs-fuse 写易丢字节** → 写脚本后必须 `python3 -c 'import ast; ast.parse(open(...).read())'` 验证；模型权重建议先 cp 到 `${PDB_TMP_ROOT}/`
- **vLLM 0.8.5 NCCL hang**（monkey 用） → 脚本末尾加 `os._exit(0)`
- **vLLM spawn worker zombie** → kill 主进程后必须 `pkill -9 -f multiprocessing.spawn` 才释放 GPU 内存（注意：会误伤其他 chain 的 vLLM worker，慎用）
- **port 占用** → vLLM serve 模式重启用不同 port 避免 TIME_WAIT
- **transformers 5.5+ 内置 PaddleOCRVL 与 model config 错配** → 用 transformers 4.51.x（如 monkey_env）走 trust_remote_code dynamic load

---

## 9. 推理后续

- 评测：`${OMNIDOCBENCH_ROOT}/` 仓库（OmniDocBench 流程）
- 评分集成 `predictions/<slug>/` 目录到 OmniDocBench `eval_predictions_pdbv2/`

详细 eval 流程参考 `feedback_cdm_texlive2025_dependency.md` 等 memory。

---

## 10. 评测 / 榜单流程（OmniDocBench）

### 10.1 单 alias 评分

```bash
# 1. 准备 prediction 目录：predictions/<alias>/<image>.md
# 2. 写 yaml：scoring/configs/<alias>.yaml（参考现有的 dotsmocr.yaml clone）
#    关键字段：dataset.prediction.data_path 指向 predictions/<alias>
# 3. 跑评分（独立 SHM_CWD + TexLive 2025 + ProcessPool）：
bash scoring/run_eval.sh <alias>
# 完成后 result/<alias>/<basename>_quick_match_metric_result.json
# 注意：basename 来自 prediction.data_path basename，与 alias 不同时（如 _clean 版本）
# 必须 mv rename 为 <alias>_quick_match_metric_result.json，否则 generate_reports.py 扫不到
```

### 10.2 批量评分（推荐 tmux 跑，避免 SSH 断连）

```bash
# 写 batch 脚本（参考 scoring/batch_*.sh），列入要跑的 alias，串行跑：
tmux new -d -s pdbv2v2_batch \
  'cd ${PDB_SUPPLEMENTAL_ROOT}/scoring && bash batch_<name>.sh > ${PDB_SUPPLEMENTAL_ROOT}/result/_<name>.log 2>&1'
```

每个 alias 单独评分，ProcessPool patch 后单 alias ~9-15 min（vs 之前单核 GIL 5+ 小时）。

### 10.3 生成 / 更新榜单

```bash
python3 scoring/generate_reports.py
# 输出 3 份榜单：
#   scoring/leaderboard.txt / .json           （clean 41 模型，按 Overall 降序）
#   scoring/leaderboard_degraded.txt / .json  （degraded 36 模型）
#   scoring/ablation.txt / .json              （36 对 clean vs degraded 对比，按 Δ 排序）
# Overall = ((1-TextEdit)*100 + TableTEDS*100 + FormulaCDM*100) / 3
```

`generate_reports.py` 自动配对：alias 命名 `<base>_degraded` 会与 `<base>` 拼成 ablation pair。

### 10.4 后处理（解决格式污染再评分）

部分模型预测含 marker / 包装 / metadata 噪声，需要 clean 后再评：

| 工具 | 用途 |
|---|---|
| `scoring/clean_minicpm_v_45.py` | 剥 `<think>...</think>` 包装 |
| `scoring/clean_deepseek_ocr2.py` | 剥 `<\|ref\|>...<\|/det\|>` grounding marker |
| `scoring/clean_logics_parsing_v2.py` | 剥 `<p data-bbox=...>` 等 HTML 包装 |
| `scoring/clean_paddleocr_vl_v2.py` | HTML noise（style/class/align/cellspacing）+ entity 解码 + 多空行折叠（保留 `border="1"`）|

输出到 `predictions/<alias>_clean/`，写新 config 指向 cleaned 目录再评。

---

## 11. Mistakes 分析工具

### 11.1 自动抽取 top-N 失分 case

```bash
python3 scoring/extract_mistakes.py
# 输入：result/<alias>/*_per_page_edit.json + GT json + 原图 + prediction
# 输出：mistakes_analysis/<group>/<model>/case_NN_<image_stem>/
#   ├── image.png            # 原图（来自 puredocbench/images/）
#   ├── gt_vs_pred.md        # GT + 模型输出对比 + per-metric 分数
#   └── reason.md            # 失分原因诊断（自动 tag）
```

默认抽取 9 个代表模型 × 各 20 个最差 case = 180 个 case 子目录。

### 11.2 跨模型 hotspot 案例（论文配图准备）

`mistakes_analysis/special_case/` 含 4 个跨域 hotspot：

```
case_01_slides_030_meta_irony/      学术 2-in-1 科研幻灯片
case_02_brochure_menu_gym/          商业宣传页
case_03_slides_chemistry/           STEM 教学（含化学公式 + 嵌入分子图）
case_04_court_doc/                  中文正式法律文书（印章 + 公章）
```

每个 case 含：
- `original_image.png` / `ground_truth.md` / `all_models_summary.md`（40 模型对比）
- `feature_models/`：6 个失败模式代表 + 1 个 baseline 锚点
- `figure_prompt.md`：附录配图提示词（中英双语）

---

## 12. 已知坑（评测阶段）

- **OmniDocBench `backtrack` RecursionError**：`ocrflux_3b_degraded` 退化输入触发递归 >1000 → 评分崩溃。需要在 ProcessPool worker init 加 `sys.setrecursionlimit(100000)` 才能修复。
- **prediction.data_path basename ≠ alias 时输出文件名错位**：`run_eval.sh` 完成后必须手动 mv 改名，否则 `generate_reports.py` 扫描不到。
- **cfs-fuse 写大 yaml/sh/md 偶发 NUL bytes**：写完必须 `python3 -c 'ast.parse(...)'` / `bash -n` / `yaml.safe_load(...)` / 检查文件大小 + 头部内容。同名 inode 缓存命中 → 写入失败但 size 正确，需要换新文件名重写再 mv。
- **rm -rf 大目录在 cfs-fuse 极慢**：用 mv 到 `result_discarded/` 替代。
- **API max_tokens 截断（gemini）**：输出在 1K-2K 字符就停了，导致评分极低；非模型能力问题，重跑时把 `max_output_tokens` 设到 16K-32K。
