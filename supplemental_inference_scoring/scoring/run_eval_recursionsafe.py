#!/usr/bin/env python3
"""Wrapper for OmniDocBench pdf_validation.py that bumps Python's recursion
limit before running. Some pages (e.g., ocrflux_3b on degraded data) trigger
deep backtrack() recursion in src/dataset/end2end_dataset.py. Default 1000
isn't enough; raise to 50000.

Usage: python run_eval_recursionsafe.py --config /path/to/alias.yaml
"""
import sys
sys.setrecursionlimit(50000)
sys.path.insert(0, '${OMNIDOCBENCH_ROOT}')
from src.cli import main
main(sys.argv[1:])
