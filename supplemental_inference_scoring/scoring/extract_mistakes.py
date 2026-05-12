#!/usr/bin/env python3
"""Extract top-N worst cases per model and produce mistakes_analysis/ directory.

Output structure:
  mistakes_analysis/
    README.md
    pipeline/<model>/_summary.md
    pipeline/<model>/case_NN_<image_stem>/{image.png, gt_vs_pred.md, reason.md}
    end_to_end/<model>/...
    general_vlm/<model>/...
"""
import argparse
import json
import os
import re
import shutil
import sys
from collections import Counter

# ---------- Config ----------

GT_PATH = '${PDB_MANIFEST_JSON}'
IMAGES_BASE = '${PDB_DATASET_ROOT}/images/clean'
RESULT_BASE = '${PDB_SUPPLEMENTAL_ROOT}/result'
CONFIG_BASE = '${PDB_SUPPLEMENTAL_ROOT}/scoring/configs'
DEFAULT_OUT = '${PDB_TMP_ROOT:-/tmp/pdbv2}/mistakes_build'

MODEL_GROUPS = {
    'pipeline': ['paddleocr_vl', 'mineru_2_5_pro', 'logics_parsing_v2'],
    'end_to_end': ['deepseek_ocr_2', 'fd_rl', 'ocrverse'],
    'general_vlm': ['qwen3_5_397b_a17b', 'qwen3_5_27b', 'qwen3_5_35b_a3b'],
}

TOP_N = 20

CATEGORY_LABELS = {
    '01_academic': '学术论文',
    '02_education': '教育考试',
    '03_legal_gov': '法律政务',
    '04_business': '商业文书',
    '05_finance': '金融报表',
    '06_medical': '医疗记录',
    '07_publishing': '出版书籍',
    '08_technical': '技术文档',
    '09_logistics': '物流单据',
    '10_certificate': '证书证件',
}

# ---------- Helpers ----------

def build_image_index(base):
    """Walk images/ tree to build {basename: full_path, basename: category_dir}."""
    full_path = {}
    category = {}
    for root, _, files in os.walk(base):
        for fn in files:
            if fn.lower().endswith('.png'):
                full_path[fn] = os.path.join(root, fn)
                rel = os.path.relpath(root, base)
                top = rel.split(os.sep)[0] if rel != '.' else 'unknown'
                category[fn] = top
    return full_path, category


def read_config_data_path(alias):
    cfg = os.path.join(CONFIG_BASE, f'{alias}.yaml')
    with open(cfg) as f:
        for line in f:
            m = re.search(r'data_path:\s*(\S+)', line)
            if m:
                data_path = m.group(1)
                if not data_path.endswith('.json'):
                    return data_path
    raise RuntimeError(f'no prediction data_path in {cfg}')


def load_gt_index(path):
    """Build image_path -> sample dict, plus extract concatenated GT text per page."""
    samples = json.load(open(path))
    by_img = {}
    for s in samples:
        img = s.get('page_info', {}).get('image_path')
        if img:
            by_img[img] = s
    return by_img


def extract_gt_text(sample, max_chars=2000):
    """Concatenate text/html across layout_dets sorted by anno_id, with category labels."""
    dets = sample.get('layout_dets', [])
    rows = sorted(dets, key=lambda d: d.get('anno_id', 0))
    parts = []
    for d in rows:
        cat = d.get('category_type', 'unknown')
        text = d.get('text') or d.get('html') or ''
        text = text.strip()
        if not text:
            continue
        parts.append(f'[{cat}] {text}')
    full = '\n\n'.join(parts)
    if len(full) > max_chars:
        full = full[:max_chars] + f'\n\n... (+{len(full)-max_chars} chars truncated)'
    return full


def doc_type_from_name(image_basename):
    """e.g. 'academic_paper_001_JACS_xxx.png' -> 'academic_paper'."""
    stem = os.path.splitext(image_basename)[0]
    parts = stem.split('_')
    typed = []
    for p in parts:
        if p.isdigit() or (len(p) > 0 and p[0].isdigit()):
            break
        typed.append(p)
    return '_'.join(typed) if typed else 'unknown'


def read_metric_per_page(alias, metric_name, data_path_basename=None):
    """Try alias-derived path first, then data_path basename (for cleaned-variant outputs)."""
    candidates = [f'{alias}_quick_match_{metric_name}_per_page_edit.json']
    if data_path_basename and data_path_basename != alias:
        candidates.append(f'{data_path_basename}_quick_match_{metric_name}_per_page_edit.json')
    for fn in candidates:
        path = os.path.join(RESULT_BASE, alias, fn)
        if os.path.exists(path):
            return json.load(open(path))
    return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=DEFAULT_OUT)
    ap.add_argument('--top', type=int, default=TOP_N)
    ap.add_argument('--probe', action='store_true', help='Only print model availability + index size, do not write output')
    args = ap.parse_args()

    print(f'[probe] building image index from {IMAGES_BASE} ...')
    img_full, img_cat = build_image_index(IMAGES_BASE)
    print(f'[probe] image index: {len(img_full)} png files')

    print(f'[probe] checking model availability:')
    for group, aliases in MODEL_GROUPS.items():
        for alias in aliases:
            try:
                dp = read_config_data_path(alias)
            except Exception as e:
                dp = f'(err: {e})'
            dpb = os.path.basename(dp) if isinstance(dp, str) else None
            te = read_metric_per_page(alias, 'text_block', dpb)
            n_pred = len(os.listdir(dp)) if isinstance(dp, str) and os.path.isdir(dp) else '?'
            print(f'  [{group}] {alias}: text_block_per_page={len(te)}  data_path_base={dpb}  pred_files={n_pred}')

    if args.probe:
        # Quick GT text extraction sanity check on one sample
        gt = load_gt_index(GT_PATH)
        print(f'\n[probe] GT samples: {len(gt)}')
        first_img = next(iter(gt))
        print(f'[probe] first GT image: {first_img}')
        print(f'[probe] doc_type: {doc_type_from_name(first_img)}')
        print(f'[probe] GT text preview (first 300 chars):')
        print(extract_gt_text(gt[first_img], 300))
        return

    # placeholder for next step
    print('[next step] case extraction not yet implemented — add in next pass')


if __name__ == '__main__':
    main()
