#!/usr/bin/env python3
"""Generate three reports from result/<alias>/*_quick_match_metric_result.json:
  - leaderboard.txt / .json           — main board (clean inputs), excludes *_degraded
  - leaderboard_degraded.txt / .json  — degraded-input board, only *_degraded
  - ablation.txt / .json              — pair clean vs degraded with deltas
"""
import json
import os
import glob
import datetime
import argparse


def load_metrics(path):
    d = json.load(open(path))
    te = d['text_block']['all']['Edit_dist']['ALL_page_avg']
    cdm = d['display_formula']['all']['CDM']['all']
    fe = d['display_formula']['all']['Edit_dist']['ALL_page_avg']
    tb = d['table']['all']['TEDS']['all']
    tbs = d['table']['all']['TEDS_structure_only']['all']
    tbe = d['table']['all']['Edit_dist']['ALL_page_avg']
    ro = d['reading_order']['all']['Edit_dist']['ALL_page_avg']
    overall = ((1 - te) * 100 + tb * 100 + cdm * 100) / 3
    return {
        'overall': overall,
        'text_edit_page_avg': te,
        'formula_cdm': cdm,
        'formula_edit_page_avg': fe,
        'table_teds': tb,
        'table_teds_s': tbs,
        'table_edit_page_avg': tbe,
        'reading_order_edit_page_avg': ro,
    }


HEADER_FMT = '{:<4} {:<28} {:>9} {:>10} {:>12} {:>11} {:>13} {:>15}\n'
ROW_FMT = '{:>2}.  {:<28} {:>9.2f} {:>10.4f} {:>12.4f} {:>11.4f} {:>13.4f} {:>15.4f}\n'


def write_board(path, title, models, metrics, generated_utc, formula_str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'# {title} ({len(models)} models)\n')
        f.write(f'# generated: {generated_utc}\n')
        f.write(f'# eval: OmniDocBench v1.6 quick_match  |  Overall = {formula_str}\n\n')
        f.write(HEADER_FMT.format('Rank', 'Alias', 'Overall↑', 'TextEdit↓', 'FormulaCDM↑', 'TableTEDS↑', 'TableTEDS-S↑', 'ReadOrderEdit↓'))
        for i, a in enumerate(models, 1):
            m = metrics[a]
            f.write(ROW_FMT.format(i, a, m['overall'], m['text_edit_page_avg'], m['formula_cdm'], m['table_teds'], m['table_teds_s'], m['reading_order_edit_page_avg']))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--result-root', default=os.environ.get('PDB_RESULT_ROOT', 'result'))
    ap.add_argument('--out-dir', default=os.environ.get('PDB_SCORING_OUT_DIR', 'scoring'))
    args = ap.parse_args()

    metrics = {}
    for f in sorted(glob.glob(os.path.join(args.result_root, '*/*_quick_match_metric_result.json'))):
        alias = os.path.basename(os.path.dirname(f))
        try:
            metrics[alias] = load_metrics(f)
        except Exception as e:
            print(f'[skip] {alias}: {e}')

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    formula_str = '((1-TextEdit_page_avg)*100 + TableTEDS*100 + FormulaCDM*100) / 3'

    main_aliases = sorted([a for a in metrics if not a.endswith('_degraded')], key=lambda a: -metrics[a]['overall'])
    write_board(os.path.join(args.out_dir, 'leaderboard.txt'), 'PureDocBench Leaderboard - clean inputs', main_aliases, metrics, now, formula_str)
    with open(os.path.join(args.out_dir, 'leaderboard.json'), 'w', encoding='utf-8') as f:
        json.dump({
            'meta': {'eval': 'OmniDocBench v1.6 quick_match', 'overall_formula': formula_str, 'page_count': 1474, 'generated_utc': now, 'inputs': 'clean', 'total_models': len(main_aliases)},
            'leaderboard': [{'alias': a, **{k: round(v, 6) for k, v in metrics[a].items()}} for a in main_aliases],
        }, f, ensure_ascii=False, indent=2)
    print(f'[main]      wrote leaderboard.txt/.json ({len(main_aliases)} models)')

    deg_aliases = sorted([a for a in metrics if a.endswith('_degraded')], key=lambda a: -metrics[a]['overall'])
    if deg_aliases:
        write_board(os.path.join(args.out_dir, 'leaderboard_degraded.txt'), 'PureDocBench Leaderboard - degraded inputs', deg_aliases, metrics, now, formula_str)
        with open(os.path.join(args.out_dir, 'leaderboard_degraded.json'), 'w', encoding='utf-8') as f:
            json.dump({
                'meta': {'eval': 'OmniDocBench v1.6 quick_match', 'overall_formula': formula_str, 'page_count': 1474, 'generated_utc': now, 'inputs': 'degraded', 'total_models': len(deg_aliases)},
                'leaderboard': [{'alias': a, **{k: round(v, 6) for k, v in metrics[a].items()}} for a in deg_aliases],
            }, f, ensure_ascii=False, indent=2)
        print(f'[degraded]  wrote leaderboard_degraded.txt/.json ({len(deg_aliases)} models)')

    ablation_pairs = []
    for a in deg_aliases:
        base = a[:-len('_degraded')]
        ablation_pairs.append((base if base in metrics else None, a))

    if ablation_pairs:
        def sort_key(p):
            base, deg = p
            if base is None or base not in metrics:
                return 0
            return metrics[deg]['overall'] - metrics[base]['overall']
        ablation_pairs.sort(key=sort_key)

        ab_txt = os.path.join(args.out_dir, 'ablation.txt')
        with open(ab_txt, 'w', encoding='utf-8') as f:
            f.write(f'# PureDocBench Ablation: image degradation impact\n')
            f.write(f'# generated: {now}\n')
            f.write(f'# pairs: <base> (clean) vs <base>_degraded (degraded), sorted by Overall delta (worst regression first)\n\n')

            f.write(f'## Summary (Overall delta, sorted)\n\n')
            f.write('{:<28} {:>8} {:>10} {:>8} {:>8}\n'.format('Model', 'Clean', 'Degraded', 'Delta', 'Rel%'))
            f.write('-' * 68 + '\n')
            for base, deg in ablation_pairs:
                if base is None:
                    f.write('{:<28} {:>8} {:>10.2f} {:>8} {:>8}\n'.format(deg, '-', metrics[deg]['overall'], '-', '-'))
                else:
                    cv = metrics[base]['overall']
                    dv = metrics[deg]['overall']
                    delta = dv - cv
                    rel = (delta / cv * 100) if cv else 0.0
                    f.write('{:<28} {:>8.2f} {:>10.2f} {:>+8.2f} {:>+7.2f}%\n'.format(base, cv, dv, delta, rel))
            f.write('\n')

            f.write(f'## Per-pair detail\n\n')
            for base, deg in ablation_pairs:
                f.write(f'### {base or "-"} vs {deg}\n\n')
                if base is None:
                    f.write('(no clean baseline available)\n\n')
                    continue
                c, d = metrics[base], metrics[deg]
                f.write('{:<18} {:>10} {:>10} {:>10} {:>8}\n'.format('Metric', 'clean', 'degraded', 'delta', 'rel%'))
                f.write('-' * 62 + '\n')
                rows = [
                    ('Overall',          'overall'),
                    ('TextEdit',         'text_edit_page_avg'),
                    ('FormulaCDM',       'formula_cdm'),
                    ('FormulaEdit',      'formula_edit_page_avg'),
                    ('TableTEDS',        'table_teds'),
                    ('TableTEDS-S',      'table_teds_s'),
                    ('TableEdit',        'table_edit_page_avg'),
                    ('ReadOrderEdit',    'reading_order_edit_page_avg'),
                ]
                for label, key in rows:
                    cv, dv = c[key], d[key]
                    delta = dv - cv
                    rel = (delta / cv * 100) if cv else 0.0
                    if key == 'overall':
                        f.write('{:<18} {:>10.2f} {:>10.2f} {:>+10.2f} {:>+7.2f}%\n'.format(label, cv, dv, delta, rel))
                    else:
                        f.write('{:<18} {:>10.4f} {:>10.4f} {:>+10.4f} {:>+7.2f}%\n'.format(label, cv, dv, delta, rel))
                f.write('\n')

        ab_json = os.path.join(args.out_dir, 'ablation.json')
        entries = []
        for base, deg in ablation_pairs:
            entry = {'degraded_alias': deg, 'base_alias': base}
            if base is not None:
                entry['clean'] = {k: round(v, 6) for k, v in metrics[base].items()}
                entry['degraded'] = {k: round(v, 6) for k, v in metrics[deg].items()}
                entry['delta'] = {k: round(metrics[deg][k] - metrics[base][k], 6) for k in metrics[base]}
            else:
                entry['degraded'] = {k: round(v, 6) for k, v in metrics[deg].items()}
            entries.append(entry)
        with open(ab_json, 'w', encoding='utf-8') as f:
            json.dump({
                'meta': {'description': 'Image degradation ablation: same model on clean vs degraded inputs', 'generated_utc': now, 'pair_count': len(ablation_pairs)},
                'pairs': entries,
            }, f, ensure_ascii=False, indent=2)
        print(f'[ablation]  wrote ablation.txt/.json ({len(ablation_pairs)} pairs)')


if __name__ == '__main__':
    main()
