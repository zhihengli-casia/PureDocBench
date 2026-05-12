# Model → Env / Weights Mapping

每个 slug 对应：推理脚本 / yaml 配置 / prompt / Python env / 模型权重路径 / pip freeze 文件。

---

## 1. 本地推理（local vLLM / transformers）

| Slug | Inference Script | YAML | Prompt | Env Python | Weights | Freeze |
|---|---|---|---|---|---|---|
| qwen3_5_0_8b | `tools/model_infer/qwen3_5_0_8b.py` | `configs/models/qwen3_5_0_8b.yaml` | `prompts/qwen3_5_0_8b.txt` | `${PDB_TMP_ROOT}/envs/vllm_qwen3/bin/python` | `${PDB_WORK_ROOT}/.../new_models/Qwen3.5-0.8B/` | `repro/envs/_vllm_qwen3.txt` |
| qwen3_5_2b | `tools/model_infer/qwen3_5_2b.py` | 同上 pattern | 同上 | 同上 | `Qwen3.5-2B/` | 同上 |
| qwen3_5_4b | 同 | 同 | 同 | 同 | `Qwen3.5-4B/` | 同 |
| qwen3_5_9b | 同 | 同 | 同 | 同 | `Qwen3.5-9B/` | 同 |
| qwen3_vl_2b_instruct | 同 | 同 | 同 | 同 | `Qwen3-VL-2B-Instruct/` | 同 |
| qwen3_vl_4b_instruct | 同 | 同 | 同 | 同 | `Qwen3-VL-4B-Instruct/` | 同 |
| qwen3_vl_8b_instruct | 同 | 同 | 同 | 同 | `Qwen3-VL-8B-Instruct/` | 同 |
| monkey_pro_1_2b | `monkey_pro_1_2b.py` | `monkey_pro_1_2b.yaml` + `monkey_pro_1_2b_inference.yaml` | (SDK 内置) | `${PDB_TMP_ROOT}/monkey_env/bin/python` | `${PDB_WORK_ROOT}/.../new_models/MonkeyOCR-pro-1.2B/` | `repro/envs/_monkey_env.txt` |
| monkey_pro_3b | `monkey_pro_3b.py` | 同 pattern | 同 | 同 | `MonkeyOCR-pro-3B/` | 同 |
| youtu_parsing | `youtu_parsing.py` | (无 yaml) | (内置) | `${PDB_TMP_ROOT}/envs/youtu_parsing/bin/python` | `${PDB_WORK_ROOT}/.../new_models/Youtu-Parsing/` | `repro/envs/_youtu_parsing.txt` |
| unirec_0_1b | `unirec_0_1b.py` | (无 yaml) | (内置 OpenOCR) | `${PDB_TMP_ROOT}/envs/openocr_unirec/bin/python` | (modelscope `topdktu/unirec_0_1b_onnx` auto-download) | `repro/envs/_openocr_unirec.txt` |
| dolphin_v2 | `dolphin_v2.py` | `dolphin_v2.yaml` | (two-stage 内置) | `${PDB_TMP_ROOT}/envs/vllm_qwen3/bin/python` | `${PDB_WORK_ROOT}/.../new_models/Dolphin-v2/` | `repro/envs/_vllm_qwen3.txt` |
| paddleocr_vl_1_5 ⚠️ | `paddleocr_vl_1_5.py` | `paddleocr_vl_1_5.yaml` | `prompts/paddleocr_vl_1_5.txt` (`OCR:`) | `${PDB_TMP_ROOT}/monkey_env/bin/python` (workaround for transformers 5.5 builtin bug) | `${PDB_TMP_ROOT}/PaddleOCR-VL-1.5/` (tmpfs，避 cfs-fuse 丢失) | `repro/envs/_monkey_env.txt` |
| glm_ocr ⚠️ | (SDK pipeline) | `glm_ocr.yaml` + `glm_ocr_pipeline.yaml` | (SDK 内置) | (需要 vLLM nightly env，this internal server temporarily未建) | `${PDB_WORK_ROOT}/.../new_models/GLM-OCR/` | (待补) |

---

## 2. SiliconFlow API

| Slug | Inference Script | YAML | Prompt | Env Python | Provider Model ID |
|---|---|---|---|---|---|
| kimi_k2_6 | `tools/api_infer/kimi_k2_6.py` | `configs/api_models/kimi_k2_6.yaml` | `prompts/kimi_k2_6.txt` | `${PDB_TMP_ROOT}/envs/vllm_qwen3/bin/python` (httpx) | (查 yaml) |
| qwen3_5_27b | 同 pattern | 同 | 同 | 同 | 同 |
| qwen3_5_35b_a3b | 同 | 同 | 同 | 同 | 同 |
| qwen3_5_122b_a10b | 同 | 同 | 同 | 同 | 同 |
| qwen3_5_397b_a17b | 同 | 同 | 同 | 同 | 同 |

API key：`.env` 里 `SILICONFLOW_API_KEY=REPLACE_ME`，脚本读 env var。

---

## 3. Env 安装顺序

每个 env 用 `uv venv` 创建：

```bash
# 1. vllm_qwen3（Qwen 7 + dolphin + 5 API）
uv venv --python=3.10 ${PDB_TMP_ROOT}/envs/vllm_qwen3
uv pip install --python ${PDB_TMP_ROOT}/envs/vllm_qwen3/bin/python -r repro/envs/_vllm_qwen3.txt

# 2. monkey_env（Monkey + paddleocr_vl 复用）
conda create --prefix ${PDB_TMP_ROOT}/monkey_env python=3.10
${PDB_TMP_ROOT}/monkey_env/bin/pip install -r repro/envs/_monkey_env.txt

# 3. youtu_parsing
uv venv --python=3.10 ${PDB_TMP_ROOT}/envs/youtu_parsing
uv pip install --python ${PDB_TMP_ROOT}/envs/youtu_parsing/bin/python -r repro/envs/_youtu_parsing.txt
# flash_attn 需手动装：repro/envs/youtu_flash_attn.whl 或 GLIBC 兼容 wheel

# 4. openocr_unirec
uv venv --python=3.10 ${PDB_TMP_ROOT}/envs/openocr_unirec
uv pip install -r repro/envs/_openocr_unirec.txt

# 5. paddle_vl（Paddle CLI, 不是 PaddleOCR-VL 用的 env）
uv venv --python=3.10 ${PDB_TMP_ROOT}/envs/paddle_vl
uv pip install -r repro/envs/_paddle_vl.txt
```

> **重要**：装 vLLM nightly env (`glm_ocr_vllm`) 需另外做，this internal server temporarily缺。

---

## 4. 模型权重下载

ModelScope 命令模板：

```bash
modelscope download --model <ID> --local_dir ${PDB_WORK_ROOT}/new_models/<Name>/
```

| Slug | ModelScope ID |
|---|---|
| qwen3_5_0_8b | `Qwen/Qwen3.5-0.8B` 或类似（看 yaml weights_path） |
| ... | (从各 yaml `model.weights_path` 反查 HF/MS) |
| paddleocr_vl_1_5 | `PaddlePaddle/PaddleOCR-VL-1.5` |
| glm_ocr | `ZhipuAI/GLM-OCR`（HF）或 ModelScope 同名 |

权重大小：0.5–10 GB / 模型，建议先 `df -h /data` 确认空间。

---

## 5. 整体推理 GPU 调度参考

3 张 80GB A100 并行，按耗时均衡：

| GPU | 链上模型示例 |
|---|---|
| 0 | qwen3_5_9b → qwen3_vl_8b_instruct → youtu_parsing |
| 1 | monkey_pro_1_2b → monkey_pro_3b → qwen3_5_4b → qwen3_5_2b |
| 2 | qwen3_vl_4b_instruct → qwen3_vl_2b_instruct → qwen3_5_0_8b |

API 5 个独立 tmux，并发 conc=2-8 视 SiliconFlow TPM 而定。

---

## 6. 已知不可用

- ⚠️ **paddleocr_vl_1_5**: transformers 5.5.4 内置 PaddleOCRVL config 不兼容；workaround 用 monkey_env (transformers 4.51.1) 走 trust_remote_code
- ⚠️ **glm_ocr**: vLLM 0.19.1 加载 GLM-OCR weights 报 KeyError `eh_proj.weight`，需要 vLLM nightly

---

## 7. 二期补充模型映射（2026-04-26 ~ 2026-04-28，多数预测从 the companion server 同步过来）

the internal server很多 alias 的预测目录（`predictions/<alias>/`）实际是从 the companion server `predictions_pdbv2/` tar/scp 过来的。这些 alias **本机无对应推理脚本**，也不需要——只需要 prediction `.md` 用于 OmniDocBench 评分。

| Group | Alias | Source | Score config |
|---|---|---|---|
| pipeline | mineru_2_5 / mineru_2_5_pro | the companion server 同步 | `scoring/configs/mineru_2_5*.yaml` |
| pipeline | dotsmocr / dots_ocr | the companion server 同步 | `scoring/configs/dot*.yaml` |
| pipeline | logics_parsing_v2 | the companion server 同步（预测含 `<p data-bbox=...>` HTML 标签，已用 `clean_logics_parsing_v2.py` 清洗） | `predictions/logics_parsing_v2_clean/` |
| pipeline | nanonets_ocr2_3b | the companion server 同步 | 同 |
| pipeline | paddleocr_vl / paddleocr_vl_1_5 | internal local推理 | 同 |
| pipeline | paddleocr_vl_pp / paddleocr_vl_1_5_pp | `clean_paddleocr_vl_v2.py` 后处理（HTML 噪声清洗，+0.11 分） | 同 |
| pipeline | dolphin_v2 | internal local（vllm_qwen3 env） | 同 |
| pipeline | glm_ocr_pdbv2 | **the companion server 同步**（v3，公式恢复） | 同 |
| end_to_end | fd_rl / ocrverse / firered_ocr | the companion server 同步 | 同 |
| end_to_end | hunyuan_ocr / qianfan_ocr / step3_vl_10b_pdbv2 | the companion server 同步 | 同 |
| end_to_end | ocrflux_3b / olmocr_2_7b / olmocr_7b_0825 | the companion server 同步 | 同 |
| end_to_end | minicpm_v_45 | internal local（含 `<think>` 包装，已用 `clean_minicpm_v_45.py` 处理后再评） | `predictions/minicpm_v_45_clean/` 或 `predictions/minicpm_v_45/` |
| end_to_end | deepseek_ocr_2 | 含 `<\|ref\|>...<\|det\|>` grounding marker，已用 `clean_deepseek_ocr2.py` 清洗 | `predictions/deepseek_ocr_2_clean/` |
| end_to_end | deepseek_ocr_pdbv2 | **the companion server 同步**（重做版，替换原 deepseek_ocr 16.89 → 33.67） | `predictions/deepseek_ocr_pdbv2/` |
| general_vlm API | gemini_3_1_pro_preview_api_pdbv2 | **the companion server 同步**（API max_tokens 截断，输出仅 1K 字符） | `predictions/gemini_3_1_pro_preview_api_pdbv2/` |

> 评分 config（`scoring/configs/<alias>.yaml`）的 `prediction.data_path` 指向 cleaned 版本（`*_clean`）时，OmniDocBench 输出文件名会按 `_clean` basename 派生，**需要 mv rename** 到 `<alias>_quick_match_metric_result.json` 才能被 `generate_reports.py` 正确扫描。详见 `scoring/run_eval.sh` 末尾的 cp + 文件名规约。

---

## 8. 状态修正（vs §1 表）

| Slug | §1 标记 | 实际状态 |
|---|---|---|
| paddleocr_vl_1_5 | ⚠️ transformers 5.5 不兼容 | ✅ 已用 monkey_env (transformers 4.51.1) trust_remote_code 跑通 |
| glm_ocr | ⚠️ vLLM 0.19.1 KeyError eh_proj.weight | ✅ **从 the companion server 同步预测（v3，rank 19, 68.65）**；本机不再需要装 vLLM nightly env |

---

## 9. OmniDocBench 评分 env

`scoring/run_eval.sh` 用 host miniconda3 py3.10：

```
${PDB_SCORING_PYTHON:-python3} + OmniDocBench v1.6 quick_match + ProcessPool patch（避免 GIL 单核瓶颈，37× 加速）
+ TexLive 2025（用于 CDM 公式渲染，不能用 host TL 2019 否则 CDM 全 0）
+ 工作目录强制 ${PDB_TMP_ROOT}/pdbv2v2_scoring_cwd_<alias>（cfs-fuse 写不可靠）
+ 完成后 cp -r SHM/result/. host_result/<alias>/
```

不需要重建专用 env。
