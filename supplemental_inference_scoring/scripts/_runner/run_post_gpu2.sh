#!/bin/bash
# Post-chain GPU2 queue:
#   1. GLM-OCR clean
#   2. GLM-OCR degraded
set -u
GPU=${1:-2}
cd ${PDB_SUPPLEMENTAL_ROOT}
LOG=${PDB_LOG_ROOT:-logs}

echo "====[GPU$GPU $(date '+%F %T')] [glm_ocr_clean] start"
bash scripts/_runner/run_glm_ocr.sh $GPU clean 2>&1 | tee $LOG/post_gpu2_glm_ocr_clean.log
sleep 5

echo "====[GPU$GPU $(date '+%F %T')] [glm_ocr_deg] start"
bash scripts/_runner/run_glm_ocr.sh $GPU deg 2>&1 | tee $LOG/post_gpu2_glm_ocr_deg.log
sleep 5

echo "====[GPU$GPU $(date '+%F %T')] ALL POST GPU2 TASKS DONE"
