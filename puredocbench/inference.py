from __future__ import annotations

import concurrent.futures
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


@dataclass
class InferenceJob:
    image: Path
    output: Path
    relpath: str


def collect_images(images_dir: Path, limit: int | None = None) -> list[Path]:
    images = [path for path in sorted(images_dir.rglob("*")) if path.suffix.lower() in IMAGE_SUFFIXES]
    return images[:limit] if limit is not None else images


def build_jobs(images_dir: Path, output_dir: Path, limit: int | None = None) -> list[InferenceJob]:
    jobs: list[InferenceJob] = []
    for image in collect_images(images_dir, limit):
        rel = image.relative_to(images_dir)
        out_rel = rel.with_suffix(".md")
        jobs.append(InferenceJob(image=image, output=output_dir / out_rel, relpath=rel.as_posix()))
    return jobs


def format_command(template: str, job: InferenceJob) -> list[str]:
    return shlex.split(render_command(template, job))


def render_command(template: str, job: InferenceJob) -> str:
    mapping = {
        "image": str(job.image),
        "output": str(job.output),
        "stem": job.image.stem,
        "relpath": job.relpath,
        "output_dir": str(job.output.parent),
    }
    return template.format(**mapping)


def run_inference(
    images_dir: Path,
    output_dir: Path,
    command_template: str,
    workers: int = 1,
    limit: int | None = None,
    skip_existing: bool = True,
    dry_run: bool = False,
    shell: bool = False,
) -> dict[str, int]:
    jobs = build_jobs(images_dir, output_dir, limit)
    output_dir.mkdir(parents=True, exist_ok=True)

    selected: list[InferenceJob] = []
    skipped = 0
    for job in jobs:
        if skip_existing and job.output.exists():
            skipped += 1
        else:
            selected.append(job)

    if dry_run:
        for job in selected[:20]:
            if shell:
                print(render_command(command_template, job))
            else:
                print(" ".join(shlex.quote(part) for part in format_command(command_template, job)))
        if len(selected) > 20:
            print(f"... {len(selected) - 20} more commands")
        return {"total": len(jobs), "scheduled": len(selected), "skipped": skipped, "failed": 0}

    def run_one(job: InferenceJob) -> tuple[InferenceJob, int]:
        job.output.parent.mkdir(parents=True, exist_ok=True)
        if shell:
            proc = subprocess.run(render_command(command_template, job), shell=True)
        else:
            proc = subprocess.run(format_command(command_template, job))
        return job, proc.returncode

    failed = 0
    if workers <= 1:
        for job in selected:
            _, code = run_one(job)
            failed += int(code != 0)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(run_one, job) for job in selected]
            for future in concurrent.futures.as_completed(futures):
                _, code = future.result()
                failed += int(code != 0)
    return {"total": len(jobs), "scheduled": len(selected), "skipped": skipped, "failed": failed}
