#!/bin/bash
set -u
ALIASES=( paddle_low_vl_raw paddle_low_vl_norm paddle_low_vl_1_5_raw paddle_low_vl_1_5_norm )
echo "[batch] start $(date)"
for alias in "${ALIASES[@]}"; do
  metric_json=${PDB_SUPPLEMENTAL_ROOT}/result/${alias}/${alias}_quick_match_metric_result.json
  if [ -f "$metric_json" ]; then echo "[batch] skip $alias"; continue; fi
  echo "[batch] ==> $alias";
  bash ${PDB_SUPPLEMENTAL_ROOT}/scoring/run_eval.sh "$alias" || echo "[batch] !! $alias exit $?"
done
echo "[batch] all done $(date)"
