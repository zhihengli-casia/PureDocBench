#!/bin/bash
# Launch PaddleOCR-VL-1.5 across N GPUs (default 4), each shard one tmux + one card.
# Output: predictions/paddleocr_vl_1_5/ (clean) — all shards write same dir, file names unique.
set -e
cd ${PDB_SUPPLEMENTAL_ROOT}

GPUS="${GPUS:-0,1,2,3}"
IFS=, read -ra GPU_ARR <<< "$GPUS"
N=${#GPU_ARR[@]}
PY=${PDB_ENV_ROOT}/monkey_env/bin/python
LOG_DIR=${PDB_LOG_ROOT:-logs}
mkdir -p "$LOG_DIR"

# pre-create out dir to avoid race
mkdir -p predictions/paddleocr_vl_1_5

for ((k=0; k<N; k++)); do
  CARD=${GPU_ARR[k]}
  SESS="paddle_shard_${CARD}"
  LOG="$LOG_DIR/paddle_shard_${k}_of_${N}_gpu${CARD}.log"
  echo "[launch] shard $k/$N on GPU $CARD -> tmux $SESS, log $LOG"
  tmux kill-session -t "$SESS" 2>/dev/null || true
  tmux new-session -d -s "$SESS" "
    export CUDA_VISIBLE_DEVICES=$CARD
    export TMPDIR=${PDB_TMPDIR:-/tmp/pdbv2_ocr_tmp}
    export HF_HOME=${HF_HOME:-.cache/huggingface}
    export TORCHINDUCTOR_CACHE_DIR=${TORCHINDUCTOR_CACHE_DIR:-/tmp/pdbv2_torch_inductor_cache}
    cd ${PDB_SUPPLEMENTAL_ROOT}
    $PY -u tools/model_infer/paddleocr_vl_1_5.py --shard ${k}/${N} 2>&1 | tee $LOG
    echo \"[paddle_shard_${k}] EXIT \$? at \$(date +%T)\"
    sleep 86400
  "
done
echo "[launcher] $N shards started"
sleep 2
tmux ls 2>/dev/null | grep paddle_shard
