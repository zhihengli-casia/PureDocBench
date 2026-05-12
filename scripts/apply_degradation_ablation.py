"""
PureDocBench - Ablation Degradation Pipeline

For each clean PNG, produce degraded versions under controlled profiles:
  - single operation profiles (14): isolate one degradation factor
  - stage-level profiles (4): isolate one pipeline stage
  - cumulative profiles: progressively stack stages
  - full pipeline: medium / hard (original behavior)

Output structure:
    data/degraded_ablation/{profile_name}/{same_category_structure}/xxx.png

Usage:
    # List all available profiles
    python scripts/apply_degradation_ablation.py --list-profiles

    # Run a single profile on specific categories
    python scripts/apply_degradation_ablation.py --profile skew_only --category 01_academic
    python scripts/apply_degradation_ablation.py --profile stage3_capture --category 03_legal_gov

    # Run ALL single-op profiles on a category (for heatmap)
    python scripts/apply_degradation_ablation.py --all-single-ops --category 01_academic

    # Run all profiles (full ablation matrix)
    python scripts/apply_degradation_ablation.py --all-profiles --category 01_academic

    # Dry run
    python scripts/apply_degradation_ablation.py --profile skew_only --dry-run
"""

import os
import json
import argparse
import hashlib
import random
import time
from pathlib import Path
from collections import OrderedDict

import numpy as np
import cv2

# Reuse all degradation functions from the original script
from apply_degradation import (
    apply_ink_bleed, apply_toner_variation,
    apply_paper_aging, apply_stains, apply_wrinkles, apply_fold_lines,
    apply_skew, apply_perspective, apply_uneven_lighting,
    apply_defocus_blur, apply_motion_blur,
    apply_resolution_loss, apply_jpeg_compression,
    apply_sensor_noise, apply_color_shift,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGE_BASE = PROJECT_ROOT / "data" / "images"
ABLATION_BASE = PROJECT_ROOT / "data" / "degraded_ablation"


# ============================================================
# Operation Registry
# ============================================================

OPERATIONS = OrderedDict([
    # Stage 1: Print
    ("ink_bleed",        {"stage": "stage1_print",   "func": apply_ink_bleed}),
    ("toner_variation",  {"stage": "stage1_print",   "func": apply_toner_variation}),
    # Stage 2: Paper
    ("paper_aging",      {"stage": "stage2_paper",   "func": apply_paper_aging}),
    ("stains",           {"stage": "stage2_paper",   "func": apply_stains}),
    ("wrinkles",         {"stage": "stage2_paper",   "func": apply_wrinkles}),
    ("fold_lines",       {"stage": "stage2_paper",   "func": apply_fold_lines}),
    # Stage 3: Capture
    ("skew",             {"stage": "stage3_capture", "func": apply_skew}),
    ("perspective",      {"stage": "stage3_capture", "func": apply_perspective}),
    ("uneven_lighting",  {"stage": "stage3_capture", "func": apply_uneven_lighting}),
    ("defocus_blur",     {"stage": "stage3_capture", "func": apply_defocus_blur}),
    ("motion_blur",      {"stage": "stage3_capture", "func": apply_motion_blur}),
    # Stage 4: Digital
    ("resolution_loss",  {"stage": "stage4_digital", "func": apply_resolution_loss}),
    ("jpeg_compression", {"stage": "stage4_digital", "func": apply_jpeg_compression}),
    ("sensor_noise",     {"stage": "stage4_digital", "func": apply_sensor_noise}),
    ("color_shift",      {"stage": "stage4_digital", "func": apply_color_shift}),
])

STAGE_ORDER = ["stage1_print", "stage2_paper", "stage3_capture", "stage4_digital"]

STAGE_NAMES = {
    "stage1_print":   "Stage 1: Print Simulation",
    "stage2_paper":   "Stage 2: Paper Condition",
    "stage3_capture": "Stage 3: Capture Simulation",
    "stage4_digital": "Stage 4: Digitization Artifacts",
}


# ============================================================
# Profile Definitions
# ============================================================

def build_profiles():
    """Build all ablation profiles."""
    profiles = OrderedDict()

    # --- Single operation profiles (14) ---
    for op_name in OPERATIONS:
        profiles[f"{op_name}_only"] = {
            "description": f"Only {op_name} (isolate single factor)",
            "type": "single_op",
            "operations": {op_name: 0.7},  # fixed medium-high strength
        }

    # --- Stage-level profiles (4) ---
    for stage in STAGE_ORDER:
        stage_ops = {k: 0.7 for k, v in OPERATIONS.items() if v["stage"] == stage}
        short = stage.split("_", 1)[1]  # e.g. "print", "paper"
        profiles[f"stage_{short}"] = {
            "description": STAGE_NAMES[stage],
            "type": "stage",
            "operations": stage_ops,
        }

    # --- Cumulative profiles (4) ---
    cumulative_ops = {}
    for i, stage in enumerate(STAGE_ORDER):
        stage_ops = {k: 0.7 for k, v in OPERATIONS.items() if v["stage"] == stage}
        cumulative_ops.update(stage_ops)
        short_parts = [s.split("_", 1)[1] for s in STAGE_ORDER[:i+1]]
        name = "cumul_" + "+".join(short_parts)
        profiles[name] = {
            "description": f"Cumulative: stages 1-{i+1}",
            "type": "cumulative",
            "operations": dict(cumulative_ops),
        }

    # --- Full pipeline: medium & hard ---
    all_ops_medium = {k: 0.5 for k in OPERATIONS}
    all_ops_hard = {k: 1.0 for k in OPERATIONS}
    profiles["full_medium"] = {
        "description": "Full pipeline (medium strength=0.5)",
        "type": "full",
        "operations": all_ops_medium,
    }
    profiles["full_hard"] = {
        "description": "Full pipeline (hard strength=1.0)",
        "type": "full",
        "operations": all_ops_hard,
    }

    # --- Severity variants for key operations ---
    key_ops = ["skew", "jpeg_compression", "defocus_blur", "sensor_noise", "stains"]
    for op in key_ops:
        for level, s in [("light", 0.3), ("medium", 0.6), ("hard", 1.0)]:
            profiles[f"{op}_{level}"] = {
                "description": f"{op} at {level} severity (strength={s})",
                "type": "severity",
                "operations": {op: s},
            }

    return profiles


ALL_PROFILES = build_profiles()


# ============================================================
# Deterministic Degradation (no randomness jitter)
# ============================================================

def degrade_with_profile(img: np.ndarray, filename: str, profile: dict):
    """Apply degradation according to a fixed profile. Deterministic."""
    # Seed from filename for reproducibility of stochastic ops (stain position etc.)
    seed = int(hashlib.md5(filename.encode()).hexdigest(), 16) % (2**32)
    random.seed(seed)
    np.random.seed(seed)

    result = img.copy()
    params_log = {
        "filename": filename,
        "profile": profile.get("description", ""),
        "operations_applied": {},
    }

    # Apply operations in canonical order
    for op_name, op_info in OPERATIONS.items():
        if op_name in profile["operations"]:
            strength = profile["operations"][op_name]
            result = op_info["func"](result, strength)
            params_log["operations_applied"][op_name] = {"strength": strength}

    return result, params_log


# ============================================================
# Batch Processing
# ============================================================

def load_image_files(input_base: Path, category: str = None, image_list: Path = None):
    """Collect input PNGs from either a category tree or a flat image list."""
    if image_list is not None:
        names = [line.strip() for line in image_list.read_text(encoding="utf-8").splitlines() if line.strip()]
        image_files = []
        for name in names:
            candidate = input_base / name
            if not candidate.exists():
                raise FileNotFoundError(f"Image listed in {image_list} not found under {input_base}: {name}")
            image_files.append(candidate)
        return image_files

    search_dir = input_base / category if category else input_base
    image_files = sorted(search_dir.rglob("*.png"))

    # Keep the historical numbered-category filtering for tree-style datasets,
    # but do not discard flat workspaces where filenames live directly under input_base.
    if category is None:
        filtered = []
        for path in image_files:
            rel = path.relative_to(input_base)
            if len(rel.parts) == 1:
                filtered.append(path)
                continue
            if rel.parts[0][:3].replace("_", "").isdigit():
                filtered.append(path)
        if filtered:
            image_files = filtered

    return image_files


def process_profile(profile_name: str, profile: dict,
                    input_base: Path, output_base: Path,
                    category: str = None, image_list: Path = None,
                    force: bool = False, dry_run: bool = False):
    """Process all images under one profile."""

    # Collect input PNGs
    image_files = load_image_files(input_base, category=category, image_list=image_list)

    out_base = output_base / profile_name

    to_process = []
    for img_path in image_files:
        rel = img_path.relative_to(input_base)
        out_path = out_base / rel.parent / (rel.stem + ".png")
        if out_path.exists() and not force:
            continue
        to_process.append(img_path)

    print(f"\n{'='*60}")
    print(f"Profile: {profile_name}")
    print(f"  {profile['description']}")
    print(f"  Operations: {list(profile['operations'].keys())}")
    print(f"  Images: {len(image_files)} total, {len(to_process)} to process")
    print(f"  Output: {out_base}")

    if dry_run:
        for f in to_process[:5]:
            print(f"    → {f.relative_to(input_base)}")
        if len(to_process) > 5:
            print(f"    ... +{len(to_process)-5} more")
        return 0, 0

    if not to_process:
        print("  Nothing to process (all done).")
        return 0, 0

    success = errors = 0
    t0 = time.time()

    for i, img_path in enumerate(to_process):
        rel = img_path.relative_to(input_base)
        img = cv2.imread(str(img_path))
        if img is None:
            errors += 1
            print(f"  [{i+1}/{len(to_process)}] ✗ Cannot read: {rel}")
            continue

        try:
            degraded, params = degrade_with_profile(img, img_path.name, profile)

            out_dir = out_base / rel.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / (rel.stem + ".png")
            cv2.imwrite(str(out_path), degraded, [cv2.IMWRITE_PNG_COMPRESSION, 6])

            # Save params
            params_dir = out_base / "_params" / rel.parent
            params_dir.mkdir(parents=True, exist_ok=True)
            params_path = params_dir / (img_path.stem + ".json")
            with open(params_path, "w", encoding="utf-8") as f:
                json.dump(params, f, indent=2, ensure_ascii=False)

            success += 1
            if (i + 1) % 20 == 0 or i == len(to_process) - 1:
                print(f"  [{i+1}/{len(to_process)}] ✓ {success} done")

        except Exception as e:
            errors += 1
            print(f"  [{i+1}/{len(to_process)}] ✗ {rel}: {e}")

    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s — Success: {success}, Errors: {errors}")
    return success, errors


def main():
    parser = argparse.ArgumentParser(description="PureDocBench Ablation Degradation")
    parser.add_argument("--input-dir", type=Path, default=IMAGE_BASE,
                        help=f"Input image root (default: {IMAGE_BASE})")
    parser.add_argument("--output-dir", type=Path, default=ABLATION_BASE,
                        help=f"Output root (default: {ABLATION_BASE})")
    parser.add_argument("--image-list", type=Path, default=None,
                        help="Optional image list file. Paths are resolved relative to --input-dir.")
    parser.add_argument("--profile", type=str, default=None,
                        help="Profile name to run")
    parser.add_argument("--category", type=str, default=None,
                        help="Only process this category (e.g. 01_academic)")
    parser.add_argument("--all-single-ops", action="store_true",
                        help="Run all 15 single-operation profiles")
    parser.add_argument("--all-stages", action="store_true",
                        help="Run all 4 stage-level profiles")
    parser.add_argument("--all-profiles", action="store_true",
                        help="Run ALL profiles (full ablation matrix)")
    parser.add_argument("--force", action="store_true",
                        help="Re-process even if output exists")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show plan without processing")
    parser.add_argument("--list-profiles", action="store_true",
                        help="List all available profiles")
    args = parser.parse_args()

    if args.list_profiles:
        print(f"{'Profile Name':<35s} {'Type':<12s} {'#Ops':>4s}  Description")
        print("-" * 90)
        for name, p in ALL_PROFILES.items():
            print(f"{name:<35s} {p['type']:<12s} {len(p['operations']):>4d}  {p['description']}")
        print(f"\nTotal: {len(ALL_PROFILES)} profiles")
        return

    # Determine which profiles to run
    profiles_to_run = []
    if args.all_profiles:
        profiles_to_run = list(ALL_PROFILES.items())
    elif args.all_single_ops:
        profiles_to_run = [(k, v) for k, v in ALL_PROFILES.items() if v["type"] == "single_op"]
    elif args.all_stages:
        profiles_to_run = [(k, v) for k, v in ALL_PROFILES.items() if v["type"] == "stage"]
    elif args.profile:
        if args.profile not in ALL_PROFILES:
            print(f"Unknown profile: {args.profile}")
            print(f"Use --list-profiles to see options")
            return
        profiles_to_run = [(args.profile, ALL_PROFILES[args.profile])]
    else:
        parser.print_help()
        return

    total_success = total_errors = 0
    t_global = time.time()

    for name, profile in profiles_to_run:
        s, e = process_profile(
            name,
            profile,
            input_base=args.input_dir,
            output_base=args.output_dir,
            category=args.category,
            image_list=args.image_list,
            force=args.force,
            dry_run=args.dry_run,
        )
        total_success += s
        total_errors += e

    elapsed = time.time() - t_global
    print(f"\n{'='*60}")
    print(f"All done in {elapsed:.1f}s — {total_success} images, {total_errors} errors")
    print(f"Profiles run: {len(profiles_to_run)}")


if __name__ == "__main__":
    main()
