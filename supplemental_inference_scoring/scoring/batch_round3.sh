#!/bin/bash
# Round-3: 2 more API subset models
set -u
RUN=${PDB_SUPPLEMENTAL_ROOT}/scoring/run_eval.sh
ALIASES=( qwen3_5_122b_a10b qwen3_5_35b_a3b )
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
