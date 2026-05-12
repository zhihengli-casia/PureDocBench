#!/usr/bin/env bash
# Generic single-model runner for puredocbench inference.
# Usage:
#   ./tools/run_one.sh <model_slug_without_pdbv2> <gpu_id> <dataset_dir> <output_root> [extra args...]
# Examples:
#   ./tools/run_one.sh ocrverse 0 /path/to/digital_degraded /path/to/predictions_degraded
#   ./tools/run_one.sh ocrverse 0 /path/to/images /path/to/predictions --smoke --n 5
set -e
SLUG=$1; GPU=$2; DATASET=$3; OUTPUT=$4
shift 4
BASE=$(dirname "$(readlink -f "$0")")/..
SCRIPT=$BASE/tools/model_infer/${SLUG}_pdbv2.py

# Resolve env from yaml (simple grep, no yq dep)
YAML=$BASE/configs/models/${SLUG}_pdbv2.yaml
PY=$(grep '^python_bin:' $YAML | sed 's/python_bin: *"\(.*\)"//')
LIB=$(grep '^ld_library_path:' $YAML | sed 's/ld_library_path: *"\(.*\)"//' || echo "")
EXTRA_ENV=""
case $SLUG in
  mineru_2_5|mineru_2_5_pro)
    EXTRA_ENV="PYTHONPATH=${MINERU_THIRD_PARTY:-third_party} "
    ;;
esac

[ -n "$LIB" ] && export LD_LIBRARY_PATH=$LIB
echo "[run_one] $SLUG -> GPU $GPU"
echo "[run_one] python: $PY"
echo "[run_one] dataset: $DATASET"
echo "[run_one] output: $OUTPUT"

# Detect smoke vs full from extra args
if echo "$@" | grep -q -- '--smoke'; then
  exec env CUDA_VISIBLE_DEVICES=$GPU $EXTRA_ENV $PY $SCRIPT --dataset-dir $DATASET --smoke-root $OUTPUT "$@"
else
  exec env CUDA_VISIBLE_DEVICES=$GPU $EXTRA_ENV $PY $SCRIPT --dataset-dir $DATASET --predictions-root $OUTPUT "$@"
fi
