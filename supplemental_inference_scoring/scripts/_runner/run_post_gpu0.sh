#!/bin/bash
# GPU0 post-chain v2: each task does smoke 5 -> verify -> full or skip-on-fail.
# Reordered: stable tasks first, problematic models last.
set -u
GPU=${1:-0}
cd ${PDB_SUPPLEMENTAL_ROOT}
export CUDA_VISIBLE_DEVICES=$GPU
export TMPDIR=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp}
export TMP=$TMPDIR
export TEMP=$TMPDIR
export XDG_CACHE_HOME=${PDB_SUPPLEMENTAL_ROOT}/.cache
export HF_HOME=${HF_HOME:-.cache/huggingface}
export TORCHINDUCTOR_CACHE_DIR=${TORCHINDUCTOR_CACHE_DIR:-/tmp/pdbv2_torch_inductor_cache}
export VLLM_CACHE_ROOT=${VLLM_CACHE_ROOT:-/tmp/pdbv2_vllm_cache}
export TRITON_CACHE_DIR=${TRITON_CACHE_DIR:-/tmp/pdbv2_triton_cache}
export VLLM_NO_USAGE_STATS=1 DO_NOT_TRACK=1
mkdir -p $TMPDIR ${PDB_LOG_ROOT:-logs}
LOG=${PDB_LOG_ROOT:-logs}

PY_QWEN=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
PY_YOUTU=${PDB_ENV_ROOT}/youtu_parsing/bin/python

cleanup_task() {
  local pyfile=$1
  pkill -9 -f "tools/model_infer/$pyfile" 2>/dev/null || true
  sleep 8
}

# Args: task_name, smoke_dir, full_dir, smoke_cmd..., -- full_cmd...
run_task() {
  local task=$1; shift
  local smoke_dir=$1; shift
  local full_dir=$1; shift
  local pyfile=$1; shift
  # Remaining args are: smoke_cmd... '--' full_cmd...
  local smoke_cmd=()
  local full_cmd=()
  local in_full=0
  for arg in "$@"; do
    if [ "$arg" = '--' ]; then in_full=1; continue; fi
    if [ $in_full -eq 0 ]; then smoke_cmd+=("$arg"); else full_cmd+=("$arg"); fi
  done

  echo "====[GPU$GPU $(date '+%F %T')] [$task] SMOKE START"
  mkdir -p "$smoke_dir"
  timeout --signal=KILL 1800 "${smoke_cmd[@]}" > $LOG/post_gpu0_${task}_smoke.log 2>&1 || true
  cleanup_task $pyfile
  local cnt=$(find "$smoke_dir" -name '*.md' 2>/dev/null | wc -l)
  if [ "$cnt" -lt 5 ]; then
    echo "====[GPU$GPU $(date '+%F %T')] [$task] SMOKE FAIL md=$cnt — skip full, next task"
    return 1
  fi
  echo "====[GPU$GPU $(date '+%F %T')] [$task] SMOKE PASS md=$cnt"
  echo "====[GPU$GPU $(date '+%F %T')] [$task] FULL START"
  mkdir -p "$full_dir"
  timeout --signal=KILL 64800 "${full_cmd[@]}" > $LOG/post_gpu0_${task}_full.log 2>&1 || true
  cleanup_task $pyfile
  local fcnt=$(find "$full_dir" -name '*.md' 2>/dev/null | wc -l)
  echo "====[GPU$GPU $(date '+%F %T')] [$task] FULL DONE md=$fcnt"
  return 0
}

# 1. youtu_parsing deg (resume from 97 already done; uses --limit 5 for smoke)
run_task youtu_parsing_deg   ${PDB_SUPPLEMENTAL_ROOT}/outputs_smoke_degraded/youtu_parsing   ${PDB_SUPPLEMENTAL_ROOT}/predictions_degraded/youtu_parsing   youtu_parsing.py   $PY_YOUTU tools/model_infer/youtu_parsing.py --image-root ${PDB_DATASET_ROOT}/images/digital_degraded --save-dir ${PDB_SUPPLEMENTAL_ROOT}/outputs_smoke_degraded/youtu_parsing --image-list ${PDB_IMAGE_LIST_ROOT}/image_list_pdb.txt --limit 5   --   $PY_YOUTU tools/model_infer/youtu_parsing.py --image-root ${PDB_DATASET_ROOT}/images/digital_degraded --save-dir ${PDB_SUPPLEMENTAL_ROOT}/predictions_degraded/youtu_parsing --image-list ${PDB_IMAGE_LIST_ROOT}/image_list_pdb.txt

# 2. dolphin_v2 clean
run_task dolphin_v2_clean   ${PDB_SUPPLEMENTAL_ROOT}/outputs_smoke/dolphin_v2   ${PDB_SUPPLEMENTAL_ROOT}/predictions/dolphin_v2   dolphin_v2.py   $PY_QWEN tools/model_infer/dolphin_v2.py --image-root ${PDB_DATASET_ROOT}/images/clean --pred-dir ${PDB_SUPPLEMENTAL_ROOT}/outputs_smoke/dolphin_v2 --tensor-parallel-size 1 --gpu-memory-utilization 0.85 --smoke --n 5   --   $PY_QWEN tools/model_infer/dolphin_v2.py --image-root ${PDB_DATASET_ROOT}/images/clean --pred-dir ${PDB_SUPPLEMENTAL_ROOT}/predictions/dolphin_v2 --tensor-parallel-size 1 --gpu-memory-utilization 0.85

# 3. dolphin_v2 deg
run_task dolphin_v2_deg   ${PDB_SUPPLEMENTAL_ROOT}/outputs_smoke_degraded/dolphin_v2   ${PDB_SUPPLEMENTAL_ROOT}/predictions_degraded/dolphin_v2   dolphin_v2.py   $PY_QWEN tools/model_infer/dolphin_v2.py --image-root ${PDB_DATASET_ROOT}/images/digital_degraded --pred-dir ${PDB_SUPPLEMENTAL_ROOT}/outputs_smoke_degraded/dolphin_v2 --tensor-parallel-size 1 --gpu-memory-utilization 0.85 --smoke --n 5   --   $PY_QWEN tools/model_infer/dolphin_v2.py --image-root ${PDB_DATASET_ROOT}/images/digital_degraded --pred-dir ${PDB_SUPPLEMENTAL_ROOT}/predictions_degraded/dolphin_v2 --tensor-parallel-size 1 --gpu-memory-utilization 0.85

# 4. paddleocr_vl_1_5 clean (problematic - moved to end)
run_task paddleocr_vl_1_5_clean   ${PDB_SUPPLEMENTAL_ROOT}/outputs_smoke/paddleocr_vl_1_5   ${PDB_SUPPLEMENTAL_ROOT}/predictions/paddleocr_vl_1_5   paddleocr_vl_1_5.py   $PY_QWEN tools/model_infer/paddleocr_vl_1_5.py --smoke --n 5   --   $PY_QWEN tools/model_infer/paddleocr_vl_1_5.py

# 5. paddleocr_vl_1_5 deg
PDBV2_IMAGES_ROOT=${PDB_DATASET_ROOT}/images/digital_degraded PDBV2_SMOKE_ROOT=outputs_smoke_degraded PDBV2_PRED_ROOT=predictions_degraded   run_task paddleocr_vl_1_5_deg   ${PDB_SUPPLEMENTAL_ROOT}/outputs_smoke_degraded/paddleocr_vl_1_5   ${PDB_SUPPLEMENTAL_ROOT}/predictions_degraded/paddleocr_vl_1_5   paddleocr_vl_1_5.py   env PDBV2_IMAGES_ROOT=${PDB_DATASET_ROOT}/images/digital_degraded PDBV2_SMOKE_ROOT=outputs_smoke_degraded PDBV2_PRED_ROOT=predictions_degraded $PY_QWEN tools/model_infer/paddleocr_vl_1_5.py --smoke --n 5   --   env PDBV2_IMAGES_ROOT=${PDB_DATASET_ROOT}/images/digital_degraded PDBV2_SMOKE_ROOT=outputs_smoke_degraded PDBV2_PRED_ROOT=predictions_degraded $PY_QWEN tools/model_infer/paddleocr_vl_1_5.py

echo "====[GPU$GPU $(date '+%F %T')] ALL POST GPU0 TASKS DONE"
