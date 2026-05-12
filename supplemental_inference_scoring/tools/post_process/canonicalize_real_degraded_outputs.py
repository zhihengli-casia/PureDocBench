#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

if len(sys.argv) < 2:
    raise SystemExit('usage: canonicalize_real_degraded_outputs.py <pred_dir> [<pred_dir> ...]')

for arg in sys.argv[1:]:
    d = Path(arg)
    if not d.exists():
        print(f'SKIP missing {d}')
        continue
    backup = d.parent / '_backup_real_name_dups' / d.name
    backup.mkdir(parents=True, exist_ok=True)
    renamed = moved = 0
    for p in list(d.glob('*')):
        if not p.exists() or not p.is_file() or '__real_' not in p.stem:
            continue
        prefix, rest = p.stem.split('__real_', 1)
        suffix_tag = ''
        for tag in ('_layout', '_hierarchy'):
            if rest.endswith(tag):
                suffix_tag = tag
                break
        target = d / f'{prefix}{suffix_tag}{p.suffix}'
        if target.exists():
            if p.exists():
                shutil.move(str(p), str(backup / p.name))
                moved += 1
        else:
            try:
                p.rename(target)
                renamed += 1
            except FileNotFoundError:
                continue
    print(d, 'renamed', renamed, 'moved', moved)
