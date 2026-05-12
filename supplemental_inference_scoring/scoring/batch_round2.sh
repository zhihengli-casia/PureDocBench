#!/bin/bash
# Round-2 batch: 4 newly-completed inference targets (2 API + UNIREC + YouTu).
set -u

RUN=${PDB_SUPPLEMENTAL_ROOT}/scoring/run_eval.sh

ALIASES=(
  kimi_k2_6
  qwen3_5_397b_a17b
  unirec_0_1b
  youtu_parsing
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
