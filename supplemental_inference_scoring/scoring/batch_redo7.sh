#!/bin/bash
set -u
ALIASES=( glm_ocr_pdbv2 glm_ocr_pdbv2_degraded paddleocr_vl paddleocr_vl_1_5 paddleocr_vl_degraded paddleocr_vl_1_5_degraded youtu_parsing_degraded )
echo "[batch] start $(date) total=${#ALIASES[@]}"
for alias in "${ALIASES[@]}"; do
  metric_json=${PDB_SUPPLEMENTAL_ROOT}/result/${alias}/${alias}_quick_match_metric_result.json
  if [ -f "$metric_json" ]; then echo "[batch] skip $alias"; continue; fi
  echo "[batch] ==> $alias $(date)";
  bash ${PDB_SUPPLEMENTAL_ROOT}/scoring/run_eval.sh "$alias" || echo "[batch] !! $alias exit $?"
  echo "[batch] <== $alias $(date)";
done
echo "[batch] all done $(date)"
