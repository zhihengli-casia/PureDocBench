#!/usr/bin/env python3
"""PureDocBench PaddleOCR-VL official pipeline runner.

Runs PaddleOCRVL page-level pipeline backed by a local vLLM/genai server.
This script is intentionally generic so PaddleOCR-VL 1.0 and 1.5 can use the
same implementation while writing to separate rerun aliases.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = Path('${PDB_MANIFEST_JSON}')
SPLITS = {
    'clean': {
        'images_root': Path('${PDB_DATASET_ROOT}/images/clean'),
        'pred_root': 'predictions',
        'smoke_root': 'outputs_smoke',
    },
    'degraded': {
        'images_root': Path('${PDB_DATASET_ROOT}/images/digital_degraded'),
        'pred_root': 'predictions_degraded',
        'smoke_root': 'outputs_smoke_degraded',
    },
    'real': {
        'images_root': Path('${PDB_DATASET_ROOT}/images/real_degraded_gt_1474'),
        'pred_root': 'predictions_real',
        'smoke_root': 'outputs_smoke_real',
    },
}
MODELS = {
    'paddleocr_vl': {
        'pipeline_version': 'v1',
        'default_server_url': 'http://127.0.0.1:8011/v1',
        'default_output_slug': 'paddleocr_vl_official_rerun',
    },
    'paddleocr_vl_1_5': {
        'pipeline_version': None,
        'default_server_url': 'http://127.0.0.1:8080/v1',
        'default_output_slug': 'paddleocr_vl_1_5_official_rerun',
    },
}


def build_image_index(manifest: Path, images_root: Path) -> list[tuple[str, Path]]:
    data = json.loads(manifest.read_text(encoding='utf-8'))
    basenames = [e['page_info']['image_path'] for e in data]
    fs_index: dict[str, Path] = {}
    for p in images_root.rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.png', '.jpg', '.jpeg'}:
            fs_index[p.name] = p
    pairs: list[tuple[str, Path]] = []
    missing: list[str] = []
    for bn in basenames:
        p = fs_index.get(Path(bn).name)
        if p is None:
            missing.append(bn)
        else:
            pairs.append((Path(bn).name, p))
    if missing:
        print(f'[paddle_official] WARN missing={len(missing)} first={missing[:5]}', flush=True)
    return pairs


def count_bad_md(out_dir: Path) -> tuple[int, int, int]:
    files = list(out_dir.glob('*.md'))
    empty = 0
    tiny = 0
    for f in files:
        txt = f.read_text(encoding='utf-8', errors='ignore').replace('\x00', '').strip()
        if not txt:
            empty += 1
        if len(txt) < 20:
            tiny += 1
    return len(files), empty, tiny


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True, choices=sorted(MODELS))
    ap.add_argument('--split', required=True, choices=sorted(SPLITS))
    ap.add_argument('--server-url', default=None)
    ap.add_argument('--output-slug', default=None)
    ap.add_argument('--manifest', type=Path, default=Path(os.environ.get('PDBV2_JSON', DEFAULT_MANIFEST)))
    ap.add_argument('--images-root', type=Path, default=None)
    ap.add_argument('--pred-root', default=None)
    ap.add_argument('--smoke-root', default=None)
    ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--n', type=int, default=5)
    ap.add_argument('--concurrency', type=int, default=32)
    ap.add_argument('--chunk-size', type=int, default=32)
    args = ap.parse_args()

    model_cfg = MODELS[args.model]
    split_cfg = SPLITS[args.split]
    server_url = args.server_url or os.environ.get('PADDLE_VL_SERVER_URL') or model_cfg['default_server_url']
    output_slug = args.output_slug or model_cfg['default_output_slug']
    images_root = args.images_root or Path(os.environ.get('PDBV2_IMAGES_ROOT', split_cfg['images_root']))
    pred_root = args.pred_root or os.environ.get('PDBV2_PRED_ROOT', split_cfg['pred_root'])
    smoke_root = args.smoke_root or os.environ.get('PDBV2_SMOKE_ROOT', split_cfg['smoke_root'])
    out_dir = REPO_ROOT / (smoke_root if args.smoke else pred_root) / output_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f'[paddle_official] model={args.model} split={args.split} output_slug={output_slug}', flush=True)
    print(f'[paddle_official] server_url={server_url} concurrency={args.concurrency} chunk_size={args.chunk_size}', flush=True)
    print(f'[paddle_official] manifest={args.manifest}', flush=True)
    print(f'[paddle_official] images_root={images_root}', flush=True)
    print(f'[paddle_official] out_dir={out_dir}', flush=True)

    images = build_image_index(args.manifest, images_root)
    if args.smoke:
        images = images[:args.n]
        print(f'[paddle_official] SMOKE pages={len(images)}', flush=True)
    else:
        done = {p.stem for p in out_dir.glob('*.md')}
        before = len(images)
        images = [(bn, p) for bn, p in images if Path(bn).stem not in done]
        print(f'[paddle_official] FULL pending={len(images)} resumed_done={before-len(images)}', flush=True)
        if not images:
            files, empty, tiny = count_bad_md(out_dir)
            print(f'[paddle_official] nothing to do files={files} empty={empty} tiny_lt20={tiny}', flush=True)
            return 0

    from paddleocr import PaddleOCRVL

    kwargs = {
        'vl_rec_backend': 'vllm-server',
        'vl_rec_server_url': server_url,
        'vl_rec_max_concurrency': args.concurrency,
    }
    if model_cfg['pipeline_version']:
        kwargs['pipeline_version'] = model_cfg['pipeline_version']
    print(f'[paddle_official] creating PaddleOCRVL with {kwargs}', flush=True)
    pipeline = PaddleOCRVL(**kwargs)
    print('[paddle_official] pipeline ready', flush=True)

    t0 = time.time()
    ok = err = 0
    total = len(images)
    failed: list[str] = []
    for start in range(0, total, args.chunk_size):
        chunk = images[start:start + args.chunk_size]
        chunk_paths = [str(p) for _, p in chunk]
        try:
            produced = 0
            for res in pipeline.predict(chunk_paths):
                try:
                    res.save_to_markdown(save_path=str(out_dir))
                    produced += 1
                    ok += 1
                except Exception as e:
                    err += 1
                    failed.append(f'save:{type(e).__name__}:{str(e)[:160]}')
                    print(f'[paddle_official] save_md ERR {type(e).__name__}: {str(e)[:240]}', flush=True)
            if produced != len(chunk):
                missed = len(chunk) - produced
                err += max(0, missed)
                failed.extend([bn for bn, _ in chunk[produced:]])
                print(f'[paddle_official] WARN chunk produced={produced} expected={len(chunk)}', flush=True)
        except Exception as e:
            err += len(chunk)
            failed.extend([bn for bn, _ in chunk])
            print(f'[paddle_official] CHUNK ERR {type(e).__name__}: {str(e)[:300]}', flush=True)
        done = min(total, start + len(chunk))
        dt = time.time() - t0
        speed = done / dt if dt > 0 else 0
        eta = (total - done) / speed if speed > 0 else 0
        files, empty, tiny = count_bad_md(out_dir)
        print(f'[paddle_official] {done}/{total} ok={ok} err={err} files={files} empty={empty} tiny_lt20={tiny} speed={speed:.3f}/s ETA={eta:.0f}s', flush=True)

    if failed:
        fail_path = out_dir / '_failed_cases.txt'
        fail_path.write_text('\n'.join(failed) + '\n', encoding='utf-8')
        print(f'[paddle_official] failed cases written: {fail_path}', flush=True)
    files, empty, tiny = count_bad_md(out_dir)
    print(f'[paddle_official] DONE files={files} empty={empty} tiny_lt20={tiny} ok={ok} err={err} elapsed={time.time()-t0:.0f}s', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
