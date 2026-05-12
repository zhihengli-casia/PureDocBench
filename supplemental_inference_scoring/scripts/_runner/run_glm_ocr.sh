#!/bin/bash
# GLM-OCR launcher (vLLM serve + glmocr SDK).
# Usage: bash run_glm_ocr.sh <gpu_id> [clean|deg]
set -u
GPU=$1
MODE=${2:-clean}

cd ${PDB_SUPPLEMENTAL_ROOT}

if [ "$MODE" = "deg" ]; then
  IMG_ROOT=${PDB_DATASET_ROOT}/images/digital_degraded
  SMOKE_DIR=outputs_smoke_degraded/glm_ocr
  PRED_DIR=predictions_degraded/glm_ocr
  LOG_TAG=deg
else
  IMG_ROOT=${PDB_DATASET_ROOT}/images/clean
  SMOKE_DIR=outputs_smoke/glm_ocr
  PRED_DIR=predictions/glm_ocr
  LOG_TAG=clean
fi

PORT=8081
PY=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
LOG=${PDB_LOG_ROOT:-logs}
SMOKE_INPUT=${PDB_TMP_ROOT:-/tmp/pdbv2}/glm_ocr_smoke_input_$LOG_TAG
GLM_CFG=${PDB_SUPPLEMENTAL_ROOT}/configs/models/glm_ocr_pipeline.yaml

mkdir -p $LOG $SMOKE_DIR $PRED_DIR $SMOKE_INPUT
rm -f $SMOKE_INPUT/*
export PYTHONPATH=${PDB_REPOS_ROOT}/glmocr_sdk
export CUDA_VISIBLE_DEVICES=$GPU
export TMPDIR=${PDB_TMP_ROOT:-/tmp/pdbv2}/glm_ocr_tmp
mkdir -p $TMPDIR
export VLLM_NO_USAGE_STATS=1 DO_NOT_TRACK=1
export TORCHINDUCTOR_CACHE_DIR=${TORCHINDUCTOR_CACHE_DIR:-/tmp/pdbv2_torch_inductor_cache}
export VLLM_CACHE_ROOT=${VLLM_CACHE_ROOT:-/tmp/pdbv2_vllm_cache}
export TRITON_CACHE_DIR=${TRITON_CACHE_DIR:-/tmp/pdbv2_triton_cache}

echo "====[glm_ocr_$LOG_TAG $(date '+%F %T')] starting vLLM serve on GPU $GPU"
$PY -m vllm.entrypoints.openai.api_server   --model ${PDB_MODEL_ROOT}/GLM-OCR   --served-model-name glm-ocr   --host 127.0.0.1 --port $PORT   --trust-remote-code   --max-model-len 32768   --max-num-batched-tokens 8192   --limit-mm-per-prompt '{"image":1}'   --dtype bfloat16   --gpu-memory-utilization 0.6   > $LOG/glm_ocr_${LOG_TAG}_vllm.log 2>&1 &
VLLM_PID=$!

deadline=$(($(date +%s) + 300))
while true; do
  if curl -s http://127.0.0.1:$PORT/v1/models 2>/dev/null | grep -q glm-ocr; then break; fi
  if ! kill -0 $VLLM_PID 2>/dev/null; then echo "vLLM died"; tail -40 $LOG/glm_ocr_${LOG_TAG}_vllm.log; exit 1; fi
  if [ $(date +%s) -ge $deadline ]; then echo "vLLM TIMEOUT"; kill -9 $VLLM_PID; exit 1; fi
  sleep 5
done
echo "====[glm_ocr_$LOG_TAG $(date '+%F %T')] vLLM ready"

# SMOKE
$PY -c "
import json, shutil, os
m = json.load(open('${PDB_MANIFEST_JSON}'))
basenames = [e['page_info']['image_path'] for e in m[:5]]
fs = {}
for r,_,fs2 in os.walk('$IMG_ROOT'):
    for f in fs2:
        if f.lower().endswith(('.png','.jpg','.jpeg')): fs[f] = os.path.join(r,f)
for b in basenames:
    if b in fs: shutil.copy2(fs[b], '$SMOKE_INPUT/')
"
$PY -m glmocr parse "$SMOKE_INPUT" --output "$SMOKE_DIR" --config "$GLM_CFG" --mode selfhosted --layout-device cuda --no-layout-vis > $LOG/glm_ocr_${LOG_TAG}_smoke.log 2>&1
SMOKE_CNT=$(find $SMOKE_DIR -name '*.md' | wc -l)
if [ "$SMOKE_CNT" -lt 5 ]; then
  echo "====[glm_ocr_$LOG_TAG $(date '+%F %T')] SMOKE FAIL md=$SMOKE_CNT"
  tail -40 $LOG/glm_ocr_${LOG_TAG}_smoke.log
  kill -9 $VLLM_PID 2>/dev/null
  pkill -9 -f 'multiprocessing.spawn' 2>/dev/null
  exit 2
fi
echo "====[glm_ocr_$LOG_TAG $(date '+%F %T')] SMOKE PASS md=$SMOKE_CNT"

# FULL
echo "====[glm_ocr_$LOG_TAG $(date '+%F %T')] FULL: 1474 pages"
$PY -m glmocr parse "$IMG_ROOT" --output "$PRED_DIR" --config "$GLM_CFG" --mode selfhosted --layout-device cuda --no-layout-vis > $LOG/glm_ocr_${LOG_TAG}_full.log 2>&1
FULL_CNT=$(find $PRED_DIR -name '*.md' | wc -l)
echo "====[glm_ocr_$LOG_TAG $(date '+%F %T')] FULL DONE md=$FULL_CNT"

kill -9 $VLLM_PID 2>/dev/null
pkill -9 -f 'multiprocessing.spawn' 2>/dev/null
sleep 5
echo "====[glm_ocr_$LOG_TAG $(date '+%F %T')] cleanup done"
