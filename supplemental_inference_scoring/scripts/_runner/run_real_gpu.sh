#!/bin/bash
set -u
GPU=$1; shift
SLUGS="$@"

cd ${PDB_SUPPLEMENTAL_ROOT}
export CUDA_VISIBLE_DEVICES=$GPU
export PDBV2_JSON=${PDB_MANIFEST_JSON}
export PDBV2_IMAGES_ROOT=${PDB_DATASET_ROOT}/images/real_degraded_gt_1474
export PDBV2_IMAGE_LIST=${PDB_SUPPLEMENTAL_ROOT}/.cache/image_list_real_gt_1474.txt
export TMPDIR=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp}
export TMP=$TMPDIR TEMP=$TMPDIR
export XDG_CACHE_HOME=${PDB_SUPPLEMENTAL_ROOT}/.cache
export HF_HOME=${HF_HOME:-.cache/huggingface}
export TORCHINDUCTOR_CACHE_DIR=${TORCHINDUCTOR_CACHE_DIR:-/tmp/pdbv2_torch_inductor_cache}
export VLLM_CACHE_ROOT=${VLLM_CACHE_ROOT:-/tmp/pdbv2_vllm_cache}
export TRITON_CACHE_DIR=${TRITON_CACHE_DIR:-/tmp/pdbv2_triton_cache}
export VLLM_NO_USAGE_STATS=1 DO_NOT_TRACK=1
export MONKEY_REPO=${PDB_REPOS_ROOT}/MonkeyOCR
mkdir -p $TMPDIR ${PDB_LOG_ROOT:-logs} outputs_smoke_real predictions_real

LOG=${PDB_LOG_ROOT:-logs}
PY_QWEN=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
PY_MONKEY=${PDB_ENV_ROOT}/monkey_env/bin/python
PY_YOUTU=${PDB_ENV_ROOT}/youtu_parsing/bin/python
SMOKE_TIMEOUT=1800
FULL_TIMEOUT=64800

py_for() {
  case "$1" in
    qwen3_*|dolphin_v2) echo $PY_QWEN ;;
    monkey_*|paddleocr_*) echo $PY_MONKEY ;;
    youtu_*) echo $PY_YOUTU ;;
  esac
}

cleanup() {
  local slug=$1
  pkill -9 -f "tools/model_infer/$slug.py" 2>/dev/null || true
  sleep 3
}

run_smoke() {
  local slug=$1
  local py=$(py_for $slug)
  case "$slug" in
    youtu_parsing)
      mkdir -p outputs_smoke_real/$slug
      timeout --signal=KILL $SMOKE_TIMEOUT $py tools/model_infer/$slug.py --image-root $PDBV2_IMAGES_ROOT --save-dir outputs_smoke_real/$slug --image-list $PDBV2_IMAGE_LIST --limit 5
      ;;
    dolphin_v2)
      mkdir -p outputs_smoke_real/$slug/predictions
      timeout --signal=KILL $SMOKE_TIMEOUT $py tools/model_infer/$slug.py --smoke --n 5 --tensor-parallel-size 1 --image-root $PDBV2_IMAGES_ROOT --image-list $PDBV2_IMAGE_LIST --save-dir outputs_smoke_real/$slug --pred-dir outputs_smoke_real/$slug/predictions
      ;;
    *)
      timeout --signal=KILL $SMOKE_TIMEOUT env PDBV2_SMOKE_ROOT=outputs_smoke_real $py tools/model_infer/$slug.py --smoke --n 5
      ;;
  esac
}

run_full() {
  local slug=$1
  local py=$(py_for $slug)
  case "$slug" in
    youtu_parsing)
      mkdir -p predictions_real/$slug
      timeout --signal=KILL $FULL_TIMEOUT $py tools/model_infer/$slug.py --image-root $PDBV2_IMAGES_ROOT --save-dir predictions_real/$slug --image-list $PDBV2_IMAGE_LIST
      ;;
    dolphin_v2)
      mkdir -p predictions_real/$slug
      timeout --signal=KILL $FULL_TIMEOUT $py tools/model_infer/$slug.py --tensor-parallel-size 1 --image-root $PDBV2_IMAGES_ROOT --image-list $PDBV2_IMAGE_LIST --pred-dir predictions_real/$slug --save-dir .cache/dolphin_v2_real
      ;;
    *)
      timeout --signal=KILL $FULL_TIMEOUT env PDBV2_PRED_ROOT=predictions_real $py tools/model_infer/$slug.py
      ;;
  esac
}

for slug in $SLUGS; do
  echo "====[GPU$GPU $(date '+%F %T')] SMOKE $slug START"
  run_smoke $slug > $LOG/${slug}_real_smoke.log 2>&1 || true
  cleanup $slug
  if [ "$slug" = "dolphin_v2" ]; then
    cnt=$(ls outputs_smoke_real/$slug/predictions/*.md 2>/dev/null | wc -l)
  elif [ "$slug" = "youtu_parsing" ]; then
    cnt=$(ls outputs_smoke_real/$slug/*.md 2>/dev/null | wc -l)
  else
    cnt=$(ls outputs_smoke_real/$slug/*.md 2>/dev/null | wc -l)
  fi
  if [ "$cnt" -lt 5 ]; then
    echo "====[GPU$GPU $(date '+%F %T')] SMOKE $slug FAIL md=$cnt -- SKIP full"
    continue
  fi
  echo "====[GPU$GPU $(date '+%F %T')] SMOKE $slug PASS md=$cnt"
  echo "====[GPU$GPU $(date '+%F %T')] FULL $slug START"
  run_full $slug > $LOG/${slug}_real_full.log 2>&1 || true
  cleanup $slug
  fcnt=$(ls predictions_real/$slug/*.md 2>/dev/null | wc -l)
  echo "====[GPU$GPU $(date '+%F %T')] FULL $slug DONE md=$fcnt"
done

echo "====[GPU$GPU $(date '+%F %T')] ALL DONE"
