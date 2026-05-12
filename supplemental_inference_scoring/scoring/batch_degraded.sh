#!/bin/bash
set -u
RUN=${PDB_SUPPLEMENTAL_ROOT}/scoring/run_eval.sh
ALIASES=(
  mineru_2_5_pro_degraded
  mineru_2_5_degraded
  olmocr_7b_0825_degraded
  olmocr_2_7b_degraded
  fd_rl_degraded
  dotsmocr_degraded
  logics_parsing_v2_degraded
  hunyuan_ocr_degraded
  dots_ocr_degraded
  ocrflux_3b_degraded
  nanonets_ocr2_3b_degraded
  qianfan_ocr_degraded
  monkey_pro_1_2b_degraded
  monkey_pro_3b_degraded
  step3_vl_10b_pdbv2_degraded
  qwen3_5_0_8b_degraded
  qwen3_5_2b_degraded
  qwen3_5_4b_degraded
  qwen3_5_9b_degraded
  qwen3_vl_2b_instruct_degraded
  qwen3_vl_4b_instruct_degraded
  qwen3_vl_8b_instruct_degraded
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
