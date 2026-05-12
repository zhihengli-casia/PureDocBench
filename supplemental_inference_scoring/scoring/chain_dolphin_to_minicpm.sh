#!/bin/bash
set -u
LOG=${PDB_SUPPLEMENTAL_ROOT}/result/_chain_minicpm.log
echo "[chain] watching pdbv2v2_dolphin from $(date)" > "$LOG"
while tmux has-session -t pdbv2v2_dolphin 2>/dev/null; do sleep 60; done
echo "[chain] pdbv2v2_dolphin ended at $(date)" >> "$LOG"
sleep 30
if tmux has-session -t pdbv2v2_minicpm 2>/dev/null; then
  echo "[chain] minicpm already running" >> "$LOG"
else
  tmux new -d -s pdbv2v2_minicpm 'bash ${PDB_SUPPLEMENTAL_ROOT}/scoring/batch_minicpm.sh > ${PDB_SUPPLEMENTAL_ROOT}/result/_batch_minicpm.log 2>&1'
  echo "[chain] minicpm started at $(date)" >> "$LOG"
fi
