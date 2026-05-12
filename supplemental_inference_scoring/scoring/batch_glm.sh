#!/bin/bash
set -u
ALIASES=( glm_ocr_pdbv2 glm_ocr_pdbv2_degraded )
echo "[batch] start $(date)"
for alias in "${ALIASES[@]}"; do
  metric_json=${PDB_SUPPLEMENTAL_ROOT}/result/${alias}/${alias}_quick_match_metric_result.json
  if [ -f "$metric_json" ]; then echo "[batch] skip $alias"; continue; fi
  echo "[batch] ==> $alias";
  bash ${PDB_SUPPLEMENTAL_ROOT}/scoring/run_eval.sh "$alias" || echo "[batch] !! $alias exit $?"
done
echo "[batch] all done $(date)"
