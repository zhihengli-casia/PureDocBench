#!/bin/bash
cd ${PDB_SUPPLEMENTAL_ROOT}
export CUDA_VISIBLE_DEVICES=0
export TMPDIR=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp} TMP=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp} TEMP=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp}
export XDG_CACHE_HOME=${PDB_SUPPLEMENTAL_ROOT}/.cache HF_HOME=${HF_HOME:-.cache/huggingface}
export TORCHINDUCTOR_CACHE_DIR=${TORCHINDUCTOR_CACHE_DIR:-/tmp/pdbv2_torch_inductor_cache}
export VLLM_CACHE_ROOT=${VLLM_CACHE_ROOT:-/tmp/pdbv2_vllm_cache}
export TRITON_CACHE_DIR=${TRITON_CACHE_DIR:-/tmp/pdbv2_triton_cache}
export VLLM_NO_USAGE_STATS=1 DO_NOT_TRACK=1
PY=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
for m in qwen3_5_9b qwen3_5_4b qwen3_5_2b; do
  echo "==START $m $(date)"
  $PY tools/model_infer/$m.py 2>&1 | tee logs/${m}_full.log
  echo "==DONE $m EXIT=${PIPESTATUS[0]} $(date)"
done
echo "==ALL_DONE_A $(date)"
