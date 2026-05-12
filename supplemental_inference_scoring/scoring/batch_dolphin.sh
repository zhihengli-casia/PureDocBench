#!/bin/bash
set -u
RUN=${PDB_SUPPLEMENTAL_ROOT}/scoring/run_eval.sh
ALIASES=(
  dolphin_v2
  dolphin_v2_degraded
  qwen3_5_122b_a10b_degraded
  qwen3_5_35b_a3b_degraded
  qwen3_5_397b_a17b_degraded
)
echo "[batch] start $(date) total=${#ALIASES[@]}"
for alias in "${ALIASES[@]}"; do
  metric_json=${PDB_SUPPLEMENTAL_ROOT}/result/${alias}/${alias}_quick_match_metric_result.json
  if [ -f "$metric_json" ]; then echo "[batch] skip $alias"; continue; fi
  echo "[batch] ==> $alias start $(date)"
  bash "$RUN" "$alias" || echo "[batch] !! $alias exit $?"
  echo "[batch] <== $alias end $(date)"
done
echo "[batch] all done $(date)"
