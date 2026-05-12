#!/bin/bash
set -u
ALIASES=( gemini_3_1_pro_preview_api_pdbv2 gemini_3_1_pro_preview_api_pdbv2_degraded )
echo "[batch] start $(date)"
for alias in "${ALIASES[@]}"; do
  metric_json=${PDB_SUPPLEMENTAL_ROOT}/result/${alias}/${alias}_quick_match_metric_result.json
  if [ -f "$metric_json" ]; then echo "[batch] skip $alias"; continue; fi
  echo "[batch] ==> $alias $(date)";
  bash ${PDB_SUPPLEMENTAL_ROOT}/scoring/run_eval.sh "$alias" || echo "[batch] !! $alias exit $?"
  echo "[batch] <== $alias $(date)";
done
echo "[batch] all done $(date)"
