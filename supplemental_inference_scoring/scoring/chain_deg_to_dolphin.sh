#!/bin/bash
set -u
LOG=${PDB_SUPPLEMENTAL_ROOT}/result/_chain_dolphin.log
echo "[chain] watching pdbv2v2_deg from $(date)" > "$LOG"
while tmux has-session -t pdbv2v2_deg 2>/dev/null; do sleep 60; done
echo "[chain] pdbv2v2_deg ended at $(date)" >> "$LOG"
sleep 30
if tmux has-session -t pdbv2v2_dolphin 2>/dev/null; then
  echo "[chain] dolphin already running" >> "$LOG"
else
  tmux new -d -s pdbv2v2_dolphin 'bash ${PDB_SUPPLEMENTAL_ROOT}/scoring/batch_dolphin.sh > ${PDB_SUPPLEMENTAL_ROOT}/result/_batch_dolphin.log 2>&1'
  echo "[chain] dolphin started at $(date)" >> "$LOG"
fi
