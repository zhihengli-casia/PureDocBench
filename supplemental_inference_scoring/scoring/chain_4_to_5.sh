#!/bin/bash
set -u
LOG=${PDB_SUPPLEMENTAL_ROOT}/result/_chain_45.log
echo "[chain] watching batch4 from $(date)" > "$LOG"
while tmux has-session -t pdbv2v2_batch4 2>/dev/null; do sleep 60; done
echo "[chain] batch4 ended at $(date)" >> "$LOG"
sleep 30
if tmux has-session -t pdbv2v2_batch5 2>/dev/null; then
  echo "[chain] batch5 already running, exit" >> "$LOG"
else
  tmux new -d -s pdbv2v2_batch5 "bash ${PDB_SUPPLEMENTAL_ROOT}/scoring/batch_round5.sh > ${PDB_SUPPLEMENTAL_ROOT}/result/_batch_round5.log 2>&1"
  echo "[chain] batch5 started at $(date)" >> "$LOG"
fi
