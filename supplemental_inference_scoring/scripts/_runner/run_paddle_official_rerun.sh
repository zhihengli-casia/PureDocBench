#!/usr/bin/env bash
set -euo pipefail
REPO=${PDB_SUPPLEMENTAL_ROOT}
PY=${PDB_ENV_ROOT}/paddle_vl/bin/python
cd "$REPO"
MODEL=${1:?model: paddleocr_vl|paddleocr_vl_1_5}
SPLIT=${2:?split: clean|degraded|real}
MODE=${3:?mode: smoke|full|postprocess}
SERVER_URL=${4:-}
CONCURRENCY=${PADDLE_VL_CONCURRENCY:-32}
CHUNK_SIZE=${PADDLE_VL_CHUNK_SIZE:-32}
case "$MODEL" in
  paddleocr_vl) SLUG=paddleocr_vl_official_rerun; DEFAULT_URL=http://127.0.0.1:8011/v1 ;;
  paddleocr_vl_1_5) SLUG=paddleocr_vl_1_5_official_rerun; DEFAULT_URL=http://127.0.0.1:8080/v1 ;;
  *) echo "bad MODEL=$MODEL" >&2; exit 2 ;;
esac
SERVER_URL=${SERVER_URL:-$DEFAULT_URL}
case "$SPLIT" in
  clean) PRED_ROOT=predictions; SMOKE_ROOT=outputs_smoke ;;
  degraded) PRED_ROOT=predictions_degraded; SMOKE_ROOT=outputs_smoke_degraded ;;
  real) PRED_ROOT=predictions_real; SMOKE_ROOT=outputs_smoke_real ;;
  *) echo "bad SPLIT=$SPLIT" >&2; exit 2 ;;
esac
if [[ "$MODE" == smoke ]]; then
  exec "$PY" tools/model_infer/paddleocr_vl_official_pipeline.py --model "$MODEL" --split "$SPLIT" --server-url "$SERVER_URL" --output-slug "$SLUG" --smoke --n 5 --concurrency "$CONCURRENCY" --chunk-size "$CHUNK_SIZE"
elif [[ "$MODE" == full ]]; then
  exec "$PY" tools/model_infer/paddleocr_vl_official_pipeline.py --model "$MODEL" --split "$SPLIT" --server-url "$SERVER_URL" --output-slug "$SLUG" --concurrency "$CONCURRENCY" --chunk-size "$CHUNK_SIZE"
elif [[ "$MODE" == postprocess ]]; then
  exec "$PY" tools/post_process/paddle_official_postprocess.py --src "$REPO/$PRED_ROOT/$SLUG" --dst "$REPO/$PRED_ROOT/${SLUG}_pp"
else
  echo "bad MODE=$MODE" >&2; exit 2
fi
