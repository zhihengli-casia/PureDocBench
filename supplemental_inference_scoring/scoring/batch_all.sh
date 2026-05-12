#!/bin/bash
# Serial batch over all 7 local vLLM models (≥1450 pages).
# API subset (kimi/qwen3_5_122b/27b/35b/397b) is intentionally excluded — to be handled later.
set -u

RUN=${PDB_SUPPLEMENTAL_ROOT}/scoring/run_eval.sh

ALIASES=(
  qwen3_5_0_8b
  qwen3_5_2b
  qwen3_5_4b
  qwen3_5_9b
  qwen3_vl_2b_instruct
  qwen3_vl_4b_instruct
  qwen3_vl_8b_instruct
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
