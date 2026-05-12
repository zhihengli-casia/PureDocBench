#!/bin/bash
set -euo pipefail
cd ${PDB_SUPPLEMENTAL_ROOT}
export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0,1,2,3}
export TMPDIR=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp} TMP=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp} TEMP=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp}
export XDG_CACHE_HOME=${PDB_SUPPLEMENTAL_ROOT}/.cache HF_HOME=${HF_HOME:-.cache/huggingface}
export TORCHINDUCTOR_CACHE_DIR=${TORCHINDUCTOR_CACHE_DIR:-/tmp/pdbv2_torch_inductor_cache}
export VLLM_CACHE_ROOT=${VLLM_CACHE_ROOT:-/tmp/pdbv2_vllm_cache}
export TRITON_CACHE_DIR=${TRITON_CACHE_DIR:-/tmp/pdbv2_triton_cache}
export VLLM_NO_USAGE_STATS=1 DO_NOT_TRACK=1
mkdir -p logs predictions/dolphin_v2 .cache/dolphin_v2
PY=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
$PY tools/model_infer/dolphin_v2.py   --tensor-parallel-size ${TP:-4}   --gpu-memory-utilization ${GPU_UTIL:-0.85}   --chunk ${CHUNK:-32}   2>&1 | tee logs/dolphin_v2_full.log
exit ${PIPESTATUS[0]}
