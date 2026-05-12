#!/bin/bash
# Per-GPU degradation runner: smoke 5 -> verify -> full.
# All python runs wrapped with timeout + post-cleanup pkill to handle vLLM 0.8.5 NCCL hang.
set -u
GPU=$1; shift
SLUGS="$@"

cd ${PDB_SUPPLEMENTAL_ROOT}
export CUDA_VISIBLE_DEVICES=$GPU
export PDBV2_IMAGES_ROOT=${PDB_DATASET_ROOT}/images/digital_degraded
export TMPDIR=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp}
export TMP=$TMPDIR TEMP=$TMPDIR
export XDG_CACHE_HOME=${PDB_SUPPLEMENTAL_ROOT}/.cache
export HF_HOME=${HF_HOME:-.cache/huggingface}
export TORCHINDUCTOR_CACHE_DIR=${TORCHINDUCTOR_CACHE_DIR:-/tmp/pdbv2_torch_inductor_cache}
export VLLM_CACHE_ROOT=${VLLM_CACHE_ROOT:-/tmp/pdbv2_vllm_cache}
export TRITON_CACHE_DIR=${TRITON_CACHE_DIR:-/tmp/pdbv2_triton_cache}
export VLLM_NO_USAGE_STATS=1 DO_NOT_TRACK=1
mkdir -p $TMPDIR ${PDB_LOG_ROOT:-logs} outputs_smoke_degraded predictions_degraded

LOG=${PDB_LOG_ROOT:-logs}

PY_QWEN=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
PY_MONKEY=${PDB_ENV_ROOT}/monkey_env/bin/python
PY_UNIREC=${PDB_ENV_ROOT}/openocr_unirec/bin/python
PY_YOUTU=${PDB_ENV_ROOT}/youtu_parsing/bin/python

SMOKE_TIMEOUT=1800
FULL_TIMEOUT=64800

py_for() {
  case "$1" in
    qwen3_*) echo $PY_QWEN ;;
    monkey_*) echo $PY_MONKEY ;;
    unirec_*) echo $PY_UNIREC ;;
    youtu_*) echo $PY_YOUTU ;;
  esac
}

run_smoke() {
  local slug=$1
  local py=$(py_for $slug)
  if [ "$slug" = "youtu_parsing" ]; then
    mkdir -p outputs_smoke_degraded/$slug
    timeout --signal=KILL $SMOKE_TIMEOUT $py tools/model_infer/$slug.py --image-root ${PDB_DATASET_ROOT}/images/digital_degraded --save-dir outputs_smoke_degraded/$slug --image-list ${PDB_IMAGE_LIST_ROOT}/image_list_pdb.txt --limit 5
  else
    timeout --signal=KILL $SMOKE_TIMEOUT env PDBV2_SMOKE_ROOT=outputs_smoke_degraded $py tools/model_infer/$slug.py --smoke --n 5
  fi
  return 0
}

run_full() {
  local slug=$1
  local py=$(py_for $slug)
  if [ "$slug" = "youtu_parsing" ]; then
    mkdir -p predictions_degraded/$slug
    timeout --signal=KILL $FULL_TIMEOUT $py tools/model_infer/$slug.py --image-root ${PDB_DATASET_ROOT}/images/digital_degraded --save-dir predictions_degraded/$slug --image-list ${PDB_IMAGE_LIST_ROOT}/image_list_pdb.txt
  else
    timeout --signal=KILL $FULL_TIMEOUT env PDBV2_PRED_ROOT=predictions_degraded $py tools/model_infer/$slug.py
  fi
  return 0
}

cleanup() {
  local slug=$1
  pkill -9 -f "tools/model_infer/$slug.py" 2>/dev/null || true
  sleep 3
}

for slug in $SLUGS; do
  echo "====[GPU$GPU $(date '+%F %T')] SMOKE $slug START"
  run_smoke $slug > $LOG/${slug}_deg_smoke.log 2>&1 || true
  cleanup $slug
  cnt=$(ls outputs_smoke_degraded/$slug/*.md 2>/dev/null | wc -l)
  if [ "$cnt" -lt 5 ]; then
    echo "====[GPU$GPU $(date '+%F %T')] SMOKE $slug FAIL md=$cnt -- SKIP full"
    continue
  fi
  echo "====[GPU$GPU $(date '+%F %T')] SMOKE $slug PASS md=$cnt"
  echo "====[GPU$GPU $(date '+%F %T')] FULL $slug START"
  run_full $slug > $LOG/${slug}_deg_full.log 2>&1 || true
  cleanup $slug
  fcnt=$(ls predictions_degraded/$slug/*.md 2>/dev/null | wc -l)
  echo "====[GPU$GPU $(date '+%F %T')] FULL $slug DONE md=$fcnt"
done

echo "====[GPU$GPU $(date '+%F %T')] ALL DONE"
