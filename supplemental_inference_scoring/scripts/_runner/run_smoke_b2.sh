#!/bin/bash
cd ${PDB_SUPPLEMENTAL_ROOT}
export CUDA_VISIBLE_DEVICES=1
export TMPDIR=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp} TMP=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp} TEMP=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp}
export XDG_CACHE_HOME=${PDB_SUPPLEMENTAL_ROOT}/.cache HF_HOME=${HF_HOME:-.cache/huggingface}
export TORCHINDUCTOR_CACHE_DIR=${TORCHINDUCTOR_CACHE_DIR:-/tmp/pdbv2_torch_inductor_cache}
export VLLM_CACHE_ROOT=${VLLM_CACHE_ROOT:-/tmp/pdbv2_vllm_cache}
export TRITON_CACHE_DIR=${TRITON_CACHE_DIR:-/tmp/pdbv2_triton_cache}
export VLLM_NO_USAGE_STATS=1 DO_NOT_TRACK=1
PY=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
echo "==START qwen3_vl_2b_instruct $(date)"
$PY tools/model_infer/qwen3_vl_2b_instruct.py --smoke --n 5 2>&1 | tee logs/qwen3_vl_2b_instruct_smoke.log
echo "==DONE qwen3_vl_2b_instruct EXIT=${PIPESTATUS[0]} $(date)"
