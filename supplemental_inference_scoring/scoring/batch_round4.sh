#!/bin/bash
# Round-4: 17 newly-uploaded models. mineru_2_5_pro placed first as ProcessPool sanity for long-tail behavior.
# Note: deepseek_ocr_2 yaml points to predictions/deepseek_ocr_2_clean (markers stripped).
set -u

RUN=${PDB_SUPPLEMENTAL_ROOT}/scoring/run_eval.sh

ALIASES=(
  mineru_2_5_pro
  mineru_2_5
  olmocr_7b_0825
  olmocr_2_7b
  logics_parsing_v2
  fd_rl
  dotsmocr
  dolphin_v2
  dots_ocr
  firered_ocr
  ocrverse
  ocrflux_3b
  nanonets_ocr2_3b
  qianfan_ocr
  hunyuan_ocr
  deepseek_ocr_2
  deepseek_ocr
)

echo "[batch] start $(date) total=${#ALIASES[@]}"
for alias in "${ALIASES[@]}"; do
  metric_json=${PDB_SUPPLEMENTAL_ROOT}/result/${alias}/${alias}_quick_match_metric_result.json
  if [ -f "$metric_json" ]; then
    echo "[batch] skip $alias (already scored)"
    continue
  fi
  echo "[batch] ==> $alias start $(date)"
  bash "$RUN" "$alias" || echo "[batch] !! $alias exit $?"
  echo "[batch] <== $alias end $(date)"
done
echo "[batch] all done $(date)"
