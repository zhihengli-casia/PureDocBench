#!/bin/bash
set -u
slug=$1
cd ${PDB_SUPPLEMENTAL_ROOT}
export PDBV2_JSON=${PDB_MANIFEST_JSON}
export PDBV2_IMAGES_ROOT=${PDB_DATASET_ROOT}/images/real_degraded_gt_1474
export PDBV2_SMOKE_ROOT=outputs_smoke_real
export PDBV2_PRED_ROOT=predictions_real
PY=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
LOG=${PDB_LOG_ROOT:-logs}
mkdir -p outputs_smoke_real predictions_real $LOG
CONC=${CONC:-1}
case "$slug" in
  kimi_k2_6|qwen3_5_397b_a17b)
    export PDB_API_REQUEST_TIMEOUT=${PDB_API_REQUEST_TIMEOUT:-600}
    export PDB_API_RETRY_MAX=${PDB_API_RETRY_MAX:-8}
    export PDB_API_RETRY_BACKOFF=${PDB_API_RETRY_BACKOFF:-15}
    ;;
  *)
    export PDB_API_REQUEST_TIMEOUT=${PDB_API_REQUEST_TIMEOUT:-420}
    export PDB_API_RETRY_MAX=${PDB_API_RETRY_MAX:-6}
    export PDB_API_RETRY_BACKOFF=${PDB_API_RETRY_BACKOFF:-10}
    ;;
esac

echo "====[$slug $(date '+%F %T')] SMOKE START (conc=$CONC)"
$PY tools/api_infer/$slug.py --smoke --n 5 --concurrency $CONC > $LOG/${slug}_real_smoke.log 2>&1 || true
cnt=$(ls outputs_smoke_real/api/$slug/*.md 2>/dev/null | wc -l)
if [ "$cnt" -lt 5 ]; then
  echo "====[$slug $(date '+%F %T')] SMOKE FAIL md=$cnt -- skip full"
  exit 1
fi
echo "====[$slug $(date '+%F %T')] SMOKE PASS md=$cnt"

echo "====[$slug $(date '+%F %T')] FULL START (conc=$CONC)"
$PY tools/api_infer/$slug.py --concurrency $CONC > $LOG/${slug}_real_full.log 2>&1 || true
echo "====[$slug $(date '+%F %T')] FULL DONE EXIT=$?"
