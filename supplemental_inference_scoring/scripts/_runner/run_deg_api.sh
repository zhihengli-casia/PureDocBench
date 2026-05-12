#!/bin/bash
# API degradation runner: smoke 5 -> full. Per-model tmux.
# Usage: run_deg_api.sh <slug>
set -u
slug=$1
cd ${PDB_SUPPLEMENTAL_ROOT}
export PDBV2_IMAGES_ROOT=${PDB_DATASET_ROOT}/images/digital_degraded
PY=${PDB_ENV_ROOT}/vllm_qwen3/bin/python
LOG=${PDB_LOG_ROOT:-logs}
CONC=2
mkdir -p outputs_smoke_degraded predictions_degraded $LOG

echo "====[$slug $(date '+%F %T')] SMOKE START (conc=$CONC)"
PDBV2_SMOKE_ROOT=outputs_smoke_degraded $PY tools/api_infer/$slug.py --smoke --n 5 --concurrency $CONC > $LOG/${slug}_deg_smoke.log 2>&1
cnt=$(ls outputs_smoke_degraded/api/$slug/*.md 2>/dev/null | wc -l)
if [ "$cnt" -lt 5 ]; then
  echo "====[$slug $(date '+%F %T')] SMOKE FAIL md=$cnt -- skip full"
  exit 1
fi
echo "====[$slug $(date '+%F %T')] SMOKE PASS md=$cnt"

echo "====[$slug $(date '+%F %T')] FULL START (conc=$CONC)"
PDBV2_PRED_ROOT=predictions_degraded $PY tools/api_infer/$slug.py --concurrency $CONC > $LOG/${slug}_deg_full.log 2>&1
echo "====[$slug $(date '+%F %T')] FULL DONE EXIT=$?"
