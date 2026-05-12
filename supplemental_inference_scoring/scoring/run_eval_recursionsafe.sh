#!/bin/bash
# Usage: run_eval.sh <alias>
# Scores predictions in ${PDB_SUPPLEMENTAL_ROOT}/predictions/<alias>/*.md
# against PureDocBench GT, using OmniDocBench v1.6 quick_match.
set -e

ALIAS=$1
if [ -z "$ALIAS" ]; then
  echo "usage: run_eval.sh <alias>" >&2
  exit 2
fi


SKIP_FILE=${PDB_SUPPLEMENTAL_ROOT}/scoring/skip_aliases.txt
if [ -f "$SKIP_FILE" ] && grep -qx "$ALIAS" "$SKIP_FILE"; then
  echo "[run_eval] SKIP $ALIAS (listed in $SKIP_FILE)"
  exit 0
fi
HOST_CONFIG=${PDB_SUPPLEMENTAL_ROOT}/scoring/configs/${ALIAS}.yaml
HOST_RESULT=${PDB_SUPPLEMENTAL_ROOT}/result/${ALIAS}
SHM_CWD=${PDB_TMP_ROOT:-/tmp/pdbv2}/pdbv2v2_scoring_cwd_${ALIAS}
SHM_TMP=${PDB_TMP_ROOT:-/tmp/pdbv2}/pdbv2v2_scoring_tmp
TEXLIVE_ROOT=${PDB_TMP_ROOT:-/tmp/pdbv2}/texlive2025
TEXLIVE_BIN=${TEXLIVE_ROOT}/bin/x86_64-linux

if [ ! -f "$HOST_CONFIG" ]; then echo "missing config: $HOST_CONFIG" >&2; exit 3; fi
if [ ! -x "$TEXLIVE_BIN/xelatex" ]; then echo "missing TeX Live 2025 at $TEXLIVE_ROOT" >&2; exit 4; fi

rm -rf "$SHM_CWD"
mkdir -p "$HOST_RESULT" "$SHM_CWD" "$SHM_TMP"

cd "$SHM_CWD"

export PYTHONPATH=${OMNIDOCBENCH_ROOT}
export PATH="$TEXLIVE_BIN:$PATH"
export TMPDIR="$SHM_TMP" TMP="$SHM_TMP" TEMP="$SHM_TMP" MAGICK_TMPDIR="$SHM_TMP"
export CDM_PDFLATEX="$TEXLIVE_BIN/xelatex"
export CDM_TEXLIVE_ROOT="$TEXLIVE_ROOT"
export CDM_TEXLIVE_BIN="$TEXLIVE_BIN"
export CDM_KPSEWHICH="$TEXLIVE_BIN/kpsewhich"
export CDM_CJK_FONT=gkai

echo "[run_eval] ALIAS=$ALIAS" | tee "$HOST_RESULT/wrapper_status.log"
echo "[run_eval] HOST_CONFIG=$HOST_CONFIG" | tee -a "$HOST_RESULT/wrapper_status.log"
echo "[run_eval] HOST_RESULT=$HOST_RESULT  SHM_CWD=$SHM_CWD" | tee -a "$HOST_RESULT/wrapper_status.log"
echo "[run_eval] TEXLIVE_BIN=$TEXLIVE_BIN" | tee -a "$HOST_RESULT/wrapper_status.log"
echo "[run_eval] start $(date)" | tee -a "$HOST_RESULT/wrapper_status.log"

${PDB_SCORING_PYTHON:-python3} ${PDB_SUPPLEMENTAL_ROOT}/scoring/run_eval_recursionsafe.py --config "$HOST_CONFIG" 2>&1 | tee "$HOST_RESULT/run.log"
EC=${PIPESTATUS[0]}
echo "[run_eval] python exit=$EC $(date)" | tee -a "$HOST_RESULT/wrapper_status.log"

if [ -d "$SHM_CWD/result" ]; then
  cp -r "$SHM_CWD/result/." "$HOST_RESULT/"
  echo "[run_eval] result copied" | tee -a "$HOST_RESULT/wrapper_status.log"
else
  echo "[run_eval] NO result dir created" | tee -a "$HOST_RESULT/wrapper_status.log"
fi

rm -rf "$SHM_CWD"
echo "[run_eval] done $(date)" | tee -a "$HOST_RESULT/wrapper_status.log"
exit $EC
