#!/usr/bin/env python3
"""Verify the PureDocBench split tar archive downloaded from Kaggle."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path


EXPECTED_PARTS = [f"pdb_full.tar.part-{i:03d}" for i in range(10)]
EXPECTED_TAR_SHA256 = "b6da85b87e168ebc0d1277e9daa762fcfbb60993b86523b9c431000605507483"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_sha256sums(path: Path) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        digest, name = line.split(maxsplit=1)
        checksums[name.strip()] = digest
    return checksums


def stream_tar_sha256(parts: list[Path]) -> str:
    h = hashlib.sha256()
    for part in parts:
        with part.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
    return h.hexdigest()


def check_tar_listing(parts: list[Path]) -> None:
    cmd = ["tar", "-tf", "-"]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    for part in parts:
        with part.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                proc.stdin.write(chunk)
    proc.stdin.close()
    stdout = proc.stdout.read(1024 * 1024) if proc.stdout is not None else b""
    stderr = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr is not None else ""
    code = proc.wait()
    if code != 0:
        raise RuntimeError(f"tar listing failed with exit code {code}: {stderr}")
    if b"/images/clean/" not in stdout or b"/gt/" not in stdout:
        raise RuntimeError("tar listing did not expose the expected release layout")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("download_dir", type=Path, help="Directory containing the Kaggle full dataset files.")
    args = parser.parse_args()

    root = args.download_dir
    missing = [name for name in EXPECTED_PARTS + ["SHA256SUMS.txt"] if not (root / name).exists()]
    if missing:
        raise SystemExit(f"Missing required files: {missing}")

    expected = parse_sha256sums(root / "SHA256SUMS.txt")
    for name in EXPECTED_PARTS:
        got = sha256(root / name)
        want = expected.get(name)
        if got != want:
            raise SystemExit(f"Checksum mismatch for {name}: got {got}, expected {want}")

    parts = [root / name for name in EXPECTED_PARTS]
    tar_sha = stream_tar_sha256(parts)
    if tar_sha != EXPECTED_TAR_SHA256:
        raise SystemExit(f"Reconstructed tar checksum mismatch: got {tar_sha}")

    check_tar_listing(parts)
    print("OK: all split parts are present, checksummed, and readable as a tar stream.")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(1)
