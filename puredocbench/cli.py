from __future__ import annotations

import argparse
from pathlib import Path

from .inference import run_inference
from .omnidocbench import export_omnidocbench, run_omnidocbench_score
from .scoring import run_score


def resolve_manifest(manifest: Path | None, release_root: Path) -> Path:
    if manifest is not None:
        return manifest
    repo_root = Path(__file__).resolve().parents[1]
    candidates = [
        release_root / "release_manifest_candidate_1475.csv",
        release_root / "manifests" / "release_manifest_candidate_1475.csv",
        Path("manifests/release_manifest_candidate_1475.csv"),
        repo_root / "manifests" / "release_manifest_candidate_1475.csv",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[-1]


def add_common_eval_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--release-root", type=Path, required=True, help="Reconstructed puredocbench-v1.0 release directory.")
    parser.add_argument("--manifest", type=Path, default=None, help="Release manifest CSV. Defaults to the release root or repository manifest.")
    parser.add_argument("--pred-dir", type=Path, required=True, help="Directory containing one Markdown prediction per page.")
    parser.add_argument("--track", default="clean", choices=["clean", "digital", "digital_degraded", "real", "real_degraded"])
    parser.add_argument("--limit", type=int, default=None, help="Evaluate/export only the first N manifest rows.")
    parser.add_argument("--strict", action="store_true", help="Fail when any prediction is missing.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="puredocbench", description="PureDocBench public inference and scoring CLI.")
    sub = parser.add_subparsers(dest="command", required=True)

    infer = sub.add_parser("infer", help="Run any image-to-Markdown model through a command template.")
    infer.add_argument("--images", type=Path, required=True, help="Input image directory, recursively scanned.")
    infer.add_argument("--output-dir", type=Path, required=True, help="Prediction output directory; mirrors image tree with .md files.")
    infer.add_argument(
        "--command-template",
        required=True,
        help="Command template with placeholders: {image}, {output}, {stem}, {relpath}, {output_dir}.",
    )
    infer.add_argument("--workers", type=int, default=1)
    infer.add_argument("--limit", type=int, default=None)
    infer.add_argument("--no-skip-existing", action="store_true", help="Re-run even when output .md already exists.")
    infer.add_argument("--dry-run", action="store_true", help="Print commands without running them.")
    infer.add_argument("--shell", action="store_true", help="Run command templates through the shell. Useful for env vars, pipes, and wrappers.")

    score = sub.add_parser("score", help="Run the lightweight bundled scorer on Markdown predictions.")
    add_common_eval_args(score)
    score.add_argument("--out-dir", type=Path, required=True, help="Directory for summary.json, page_metrics.csv, and report.md.")

    export = sub.add_parser("export-omnidocbench", help="Export flat GT/predictions/config for the OmniDocBench evaluator.")
    add_common_eval_args(export)
    export.add_argument("--out-dir", type=Path, required=True, help="Output directory for gt.json, predictions/, and config yaml.")
    export.add_argument("--match-workers", type=int, default=8, help="match_workers value written into the OmniDocBench config.")

    omni = sub.add_parser("score-omnidocbench", help="Export inputs and run an OmniDocBench evaluator checkout.")
    add_common_eval_args(omni)
    omni.add_argument("--out-dir", type=Path, required=True, help="Output directory for gt.json, predictions/, and config yaml.")
    omni.add_argument("--omnidocbench-root", type=Path, default=None, help="OmniDocBench checkout containing pdf_validation.py. Defaults to OMNIDOCBENCH_ROOT.")
    omni.add_argument("--python", default=None, help="Python executable used to run OmniDocBench. Defaults to the current interpreter.")
    omni.add_argument("--match-workers", type=int, default=8, help="match_workers value written into the OmniDocBench config.")
    omni.add_argument("--export-only", action="store_true", help="Only export OmniDocBench inputs; do not run pdf_validation.py.")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "infer":
        result = run_inference(
            images_dir=args.images,
            output_dir=args.output_dir,
            command_template=args.command_template,
            workers=args.workers,
            limit=args.limit,
            skip_existing=not args.no_skip_existing,
            dry_run=args.dry_run,
            shell=args.shell,
        )
        print(result)
    elif args.command == "score":
        manifest = resolve_manifest(args.manifest, args.release_root)
        summary = run_score(
            release_root=args.release_root,
            manifest_path=manifest,
            pred_dir=args.pred_dir,
            out_dir=args.out_dir,
            track=args.track,
            limit=args.limit,
            strict=args.strict,
        )
        print(f"Wrote {args.out_dir}/summary.json")
        print(summary["metrics"])
    elif args.command == "export-omnidocbench":
        manifest = resolve_manifest(args.manifest, args.release_root)
        result = export_omnidocbench(
            release_root=args.release_root,
            manifest_path=manifest,
            pred_dir=args.pred_dir,
            out_dir=args.out_dir,
            track=args.track,
            limit=args.limit,
            strict=args.strict,
            match_workers=args.match_workers,
        )
        print(result)
    elif args.command == "score-omnidocbench":
        manifest = resolve_manifest(args.manifest, args.release_root)
        result = run_omnidocbench_score(
            release_root=args.release_root,
            manifest_path=manifest,
            pred_dir=args.pred_dir,
            out_dir=args.out_dir,
            track=args.track,
            limit=args.limit,
            strict=args.strict,
            omnidocbench_root=args.omnidocbench_root,
            python_bin=args.python,
            match_workers=args.match_workers,
            export_only=args.export_only,
        )
        print(result)
    else:
        parser.error(f"unknown command: {args.command}")


if __name__ == "__main__":
    main()
