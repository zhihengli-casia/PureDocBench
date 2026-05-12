"""
PureDocBench - Legacy Degradation Pipeline

For each clean PNG in data/images/, produce exactly one degraded image in
data/degraded/ with a deterministic medium/hard plan based on filename hash.

This script intentionally keeps the original 4-stage structure:
Print -> Paper -> Capture -> Digital

The input/output roots can be overridden from CLI so the same script can be run
directly against server-side dataset directories.
"""

import argparse
import hashlib
import json
import random
import time
from pathlib import Path

import cv2
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_IMAGE_BASE = PROJECT_ROOT / "data" / "images"
DEFAULT_DEGRADED_BASE = PROJECT_ROOT / "data" / "degraded"
DEFAULT_PARAMS_BASE = PROJECT_ROOT / "data" / "degradation_params"


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _seed_from_filename(filename: str) -> int:
    return int(hashlib.md5(filename.encode()).hexdigest(), 16) % (2**32)


# ============================================================
# Stage 1: Print Simulation
# ============================================================

def apply_ink_bleed(img: np.ndarray, strength: float) -> np.ndarray:
    """Expand dark strokes slightly to mimic ink bleeding."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, ink_mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    k = max(1, int(strength * 3))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    dilated_mask = cv2.dilate(ink_mask, kernel, iterations=1)

    expansion = cv2.subtract(dilated_mask, ink_mask)
    expansion_3ch = cv2.cvtColor(expansion, cv2.COLOR_GRAY2BGR).astype(np.float32) / 255.0

    result = img.astype(np.float32)
    dark_value = np.array([60, 60, 60], dtype=np.float32)
    blend_alpha = expansion_3ch * strength * 0.6
    result = result * (1 - blend_alpha) + dark_value * blend_alpha
    return np.clip(result, 0, 255).astype(np.uint8)


def apply_toner_variation(img: np.ndarray, strength: float) -> np.ndarray:
    """Apply low-frequency density drift typical of toner or ink variation."""
    h, w = img.shape[:2]
    small_h, small_w = max(2, h // 64), max(2, w // 64)
    field = np.random.normal(0.0, 1.0, (small_h, small_w)).astype(np.float32)
    field = cv2.GaussianBlur(field, (0, 0), sigmaX=1.2, sigmaY=1.2)
    field = cv2.resize(field, (w, h), interpolation=cv2.INTER_CUBIC)
    field = field / max(np.max(np.abs(field)), 1e-6)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    ink = (255.0 - gray) / 255.0
    modulation = 1.0 + field * (0.06 + 0.18 * strength)

    result = img.astype(np.float32)
    for c in range(3):
        result[:, :, c] = result[:, :, c] - ink * (1.0 - modulation) * 55.0

    return np.clip(result, 0, 255).astype(np.uint8)


# ============================================================
# Stage 2: Paper Condition
# ============================================================

def apply_paper_aging(img: np.ndarray, strength: float) -> np.ndarray:
    """Warm the page slightly and reduce local contrast."""
    result = img.astype(np.float32)
    yellow = np.array([18, 28, 42], dtype=np.float32)
    alpha = 0.10 + 0.20 * strength
    result = result * (1.0 - alpha) + (255.0 - yellow) * alpha
    result[:, :, 0] *= 1.0 - 0.04 * strength
    result[:, :, 2] *= 1.0 + 0.03 * strength
    return np.clip(result, 0, 255).astype(np.uint8)


def apply_stains(img: np.ndarray, strength: float) -> np.ndarray:
    """Overlay several semi-transparent stains on the page."""
    h, w = img.shape[:2]
    overlay = img.astype(np.float32).copy()
    n_stains = 2 + int(4 * strength)

    for _ in range(n_stains):
        cx = random.randint(0, w - 1)
        cy = random.randint(0, h - 1)
        rx = max(12, int(w * random.uniform(0.01, 0.05 + 0.07 * strength)))
        ry = max(12, int(h * random.uniform(0.01, 0.05 + 0.07 * strength)))
        angle = random.uniform(0, 180)
        stain = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(stain, (cx, cy), (rx, ry), angle, 0, 360, 255, -1)
        stain = cv2.GaussianBlur(stain, (0, 0), sigmaX=max(3, rx * 0.18), sigmaY=max(3, ry * 0.18))
        alpha = (stain.astype(np.float32) / 255.0) * random.uniform(0.05, 0.18 + 0.18 * strength)
        color = np.array([
            random.uniform(130, 180),
            random.uniform(150, 205),
            random.uniform(160, 220),
        ], dtype=np.float32)
        overlay = overlay * (1.0 - alpha[:, :, None]) + color * alpha[:, :, None]

    return np.clip(overlay, 0, 255).astype(np.uint8)


def apply_wrinkles(img: np.ndarray, strength: float) -> np.ndarray:
    """Add several faint wrinkle-like shading lines."""
    h, w = img.shape[:2]
    result = img.astype(np.float32).copy()
    n_lines = 2 + int(4 * strength)

    for _ in range(n_lines):
        horizontal = random.random() > 0.5
        layer = np.zeros((h, w), dtype=np.float32)
        if horizontal:
            y = random.randint(0, h - 1)
            thickness = max(1, int(h * (0.0008 + 0.003 * strength)))
            cv2.line(layer, (0, y), (w - 1, y), 1.0, thickness)
        else:
            x = random.randint(0, w - 1)
            thickness = max(1, int(w * (0.0008 + 0.003 * strength)))
            cv2.line(layer, (x, 0), (x, h - 1), 1.0, thickness)

        sigma = max(3.0, 9.0 + 18.0 * strength)
        layer = cv2.GaussianBlur(layer, (0, 0), sigmaX=sigma, sigmaY=sigma)
        amplitude = random.uniform(-1.0, 1.0) * (5.0 + 18.0 * strength)
        result += layer[:, :, None] * amplitude

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_fold_lines(img: np.ndarray, strength: float) -> np.ndarray:
    """Add one or two stronger fold lines with local shading."""
    h, w = img.shape[:2]
    result = img.astype(np.float32).copy()
    n_folds = 1 if strength < 0.6 else 2

    for _ in range(n_folds):
        horizontal = random.random() > 0.5
        layer = np.zeros((h, w), dtype=np.float32)
        if horizontal:
            y = random.randint(h // 6, h * 5 // 6)
            thickness = max(2, int(h * (0.001 + 0.005 * strength)))
            cv2.line(layer, (0, y), (w - 1, y), 1.0, thickness)
        else:
            x = random.randint(w // 6, w * 5 // 6)
            thickness = max(2, int(w * (0.001 + 0.005 * strength)))
            cv2.line(layer, (x, 0), (x, h - 1), 1.0, thickness)

        sigma = max(4.0, 12.0 + 22.0 * strength)
        layer = cv2.GaussianBlur(layer, (0, 0), sigmaX=sigma, sigmaY=sigma)
        dip = 10.0 + 30.0 * strength
        result -= layer[:, :, None] * dip

    return np.clip(result, 0, 255).astype(np.uint8)


# ============================================================
# Stage 3: Capture Simulation
# ============================================================

def apply_skew(img: np.ndarray, strength: float) -> np.ndarray:
    """Rotate the page by a small angle."""
    h, w = img.shape[:2]
    angle = random.uniform(-1.0, 1.0) * (1.0 + 3.0 * strength)
    M = cv2.getRotationMatrix2D((w / 2.0, h / 2.0), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)


def apply_perspective(img: np.ndarray, strength: float) -> np.ndarray:
    """Apply mild projective distortion."""
    h, w = img.shape[:2]
    max_shift = int(min(h, w) * (0.01 + 0.03 * strength))
    if max_shift <= 0:
        return img

    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    dst = np.float32([
        [random.uniform(0, max_shift), random.uniform(0, max_shift)],
        [w - random.uniform(0, max_shift), random.uniform(0, max_shift)],
        [w - random.uniform(0, max_shift), h - random.uniform(0, max_shift)],
        [random.uniform(0, max_shift), h - random.uniform(0, max_shift)],
    ])
    M = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)


def apply_uneven_lighting(img: np.ndarray, strength: float) -> np.ndarray:
    """Apply large-scale lighting gradient."""
    h, w = img.shape[:2]
    y_coords, x_coords = np.mgrid[0:h, 0:w].astype(np.float32)
    gx = random.uniform(-1, 1)
    gy = random.uniform(-1, 1)
    norm = max(abs(gx), abs(gy), 0.01)
    gx, gy = gx / norm, gy / norm

    gradient = 1.0 - strength * 0.35 * (
        gx * (x_coords / max(w, 1) - 0.5) + gy * (y_coords / max(h, 1) - 0.5)
    )
    gradient = np.clip(gradient, 0.70, 1.30)

    result = img.astype(np.float32) * gradient[:, :, np.newaxis]
    return np.clip(result, 0, 255).astype(np.uint8)


def apply_defocus_blur(img: np.ndarray, strength: float) -> np.ndarray:
    """Apply Gaussian blur simulating imperfect focus."""
    k = int(strength * 5) * 2 + 1
    k = max(3, min(k, 15))
    if k % 2 == 0:
        k += 1
    return cv2.GaussianBlur(img, (k, k), 0)


def apply_motion_blur(img: np.ndarray, strength: float) -> np.ndarray:
    """Apply directional motion blur."""
    k = max(3, int(strength * 7))
    if k <= 1:
        return img

    angle = random.uniform(0, 180)
    kernel = np.zeros((k, k), dtype=np.float32)
    center = k // 2
    kernel[center, :] = 1.0 / k
    M = cv2.getRotationMatrix2D((center, center), angle, 1.0)
    kernel = cv2.warpAffine(kernel, M, (k, k))
    kernel = kernel / (kernel.sum() + 1e-8)
    return cv2.filter2D(img, -1, kernel)


# ============================================================
# Stage 4: Digitization Artifacts
# ============================================================

def apply_resolution_loss(img: np.ndarray, strength: float) -> np.ndarray:
    """Downsample then upsample to simulate low effective DPI."""
    h, w = img.shape[:2]
    scale = 1.0 - strength * 0.4
    scale = max(0.35, scale)
    small = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR)


def apply_jpeg_compression(img: np.ndarray, strength: float) -> np.ndarray:
    """Inject JPEG compression artifacts."""
    quality = int(70 - strength * 40)
    quality = max(15, min(quality, 75))
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encoded = cv2.imencode(".jpg", img, encode_param)
    return cv2.imdecode(encoded, cv2.IMREAD_COLOR)


def apply_sensor_noise(img: np.ndarray, strength: float) -> np.ndarray:
    """Add Gaussian sensor noise."""
    result = img.astype(np.float32)
    sigma = strength * 20
    gauss = np.random.normal(0, sigma, result.shape).astype(np.float32)
    result = result + gauss
    return np.clip(result, 0, 255).astype(np.uint8)


def apply_color_shift(img: np.ndarray, strength: float) -> np.ndarray:
    """Apply a mild warm or cool channel shift."""
    result = img.astype(np.float32)
    if random.random() > 0.5:
        result[:, :, 2] *= 1.0 + strength * 0.10
        result[:, :, 0] *= 1.0 - strength * 0.08
    else:
        result[:, :, 0] *= 1.0 + strength * 0.08
        result[:, :, 2] *= 1.0 - strength * 0.08
    return np.clip(result, 0, 255).astype(np.uint8)


# ============================================================
# Legacy Pipeline
# ============================================================

LEGACY_STAGES = {
    "stage1_print": [
        ("ink_bleed", apply_ink_bleed),
        ("toner_variation", apply_toner_variation),
    ],
    "stage2_paper": [
        ("paper_aging", apply_paper_aging),
        ("stains", apply_stains),
        ("wrinkles", apply_wrinkles),
        ("fold_lines", apply_fold_lines),
    ],
    "stage3_capture": [
        ("skew", apply_skew),
        ("perspective", apply_perspective),
        ("uneven_lighting", apply_uneven_lighting),
        ("defocus_blur", apply_defocus_blur),
        ("motion_blur", apply_motion_blur),
    ],
    "stage4_digital": [
        ("resolution_loss", apply_resolution_loss),
        ("jpeg_compression", apply_jpeg_compression),
        ("sensor_noise", apply_sensor_noise),
        ("color_shift", apply_color_shift),
    ],
}


def get_difficulty(filename: str) -> str:
    h = int(hashlib.md5(filename.encode()).hexdigest(), 16)
    return "hard" if h % 2 == 0 else "medium"


def get_strength(difficulty: str) -> float:
    return {"medium": 0.5, "hard": 1.0}[difficulty]


def degrade_image(img: np.ndarray, filename: str):
    """Apply the deterministic legacy 4-stage degradation pipeline."""
    seed = _seed_from_filename(filename)
    random.seed(seed)
    np.random.seed(seed)

    difficulty = get_difficulty(filename)
    strength = get_strength(difficulty)
    params_log = {
        "filename": filename,
        "pipeline": "legacy",
        "difficulty": difficulty,
        "strength": strength,
        "stages": {},
    }

    result = img.copy()
    for stage_name, operations in LEGACY_STAGES.items():
        stage_params = {}
        for op_name, op_func in operations:
            threshold = 0.15 if difficulty == "hard" else 0.35
            do_apply = random.random() > threshold
            if do_apply:
                jitter = random.uniform(0.8, 1.2)
                effective_strength = min(1.0, strength * jitter)
                result = op_func(result, effective_strength)
                stage_params[op_name] = {"applied": True, "strength": round(effective_strength, 3)}
            else:
                stage_params[op_name] = {"applied": False}
        params_log["stages"][stage_name] = stage_params

    return result, params_log


# ============================================================
# Batch Processing
# ============================================================

def process_all(
    category: str = None,
    force: bool = False,
    dry_run: bool = False,
    save_params: bool = False,
    all_images: bool = False,
    output_format: str = "png",
    jpeg_quality: int = 90,
    image_root: Path = DEFAULT_IMAGE_BASE,
    output_root: Path = DEFAULT_DEGRADED_BASE,
    params_root: Path = DEFAULT_PARAMS_BASE,
):
    image_root = Path(image_root)
    output_root = Path(output_root)
    params_root = Path(params_root)

    search_dir = image_root / category if category else image_root
    image_files = sorted(search_dir.rglob("*.png"))

    if not all_images:
        image_files = [
            f for f in image_files
            if any(
                len(part) >= 4 and part[:2].isdigit() and part[2] == "_"
                for part in f.relative_to(image_root).parts
            )
        ]

    if not image_files:
        print(f"No PNG images found in {search_dir}")
        return

    out_ext = ".jpg" if output_format == "jpg" else ".png"
    to_process = []
    for img_path in image_files:
        rel = img_path.relative_to(image_root)
        out_path = output_root / rel.parent / (rel.stem + out_ext)
        if out_path.exists() and not force:
            continue
        to_process.append(img_path)

    medium_count = sum(1 for p in to_process if get_difficulty(p.name) == "medium")
    hard_count = len(to_process) - medium_count

    print(f"Clean images found: {len(image_files)}")
    print(f"Already degraded (skip): {len(image_files) - len(to_process)}")
    print(f"To process: {len(to_process)}")
    print(f"Pipeline: legacy")
    print(f"  Medium: {medium_count}, Hard: {hard_count}")
    print(f"Images: {image_root}")
    print(f"Output: {output_root}")
    if save_params:
        print(f"Params: {params_root}")

    if dry_run:
        print("\n[Dry run — no images processed]")
        for img_path in to_process[:10]:
            rel = img_path.relative_to(image_root)
            print(f"  {rel} -> {get_difficulty(img_path.name)}")
        if len(to_process) > 10:
            print(f"  ... and {len(to_process) - 10} more")
        return

    success = 0
    errors = 0
    t0 = time.time()

    for i, img_path in enumerate(to_process):
        rel = img_path.relative_to(image_root)
        img = cv2.imread(str(img_path))
        if img is None:
            errors += 1
            print(f"  [{i + 1}/{len(to_process)}] ✗ Cannot read: {rel}")
            continue

        try:
            degraded, params = degrade_image(img, img_path.name)
            out_dir = output_root / rel.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / (rel.stem + out_ext)
            if output_format == "jpg":
                cv2.imwrite(str(out_path), degraded, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality])
            else:
                cv2.imwrite(str(out_path), degraded, [cv2.IMWRITE_PNG_COMPRESSION, 6])

            if save_params:
                params_dir = params_root / rel.parent
                params_dir.mkdir(parents=True, exist_ok=True)
                params_path = params_dir / (img_path.stem + ".json")
                with open(params_path, "w", encoding="utf-8") as f:
                    json.dump(params, f, indent=2, ensure_ascii=False)

            success += 1
            print(f"  [{i + 1}/{len(to_process)}] ✓ {rel} [{params['difficulty']}]")
        except Exception as e:
            errors += 1
            print(f"  [{i + 1}/{len(to_process)}] ✗ {rel}: {e}")

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s — Success: {success}, Errors: {errors}")


def main():
    parser = argparse.ArgumentParser(description="PureDocBench Legacy Degradation")
    parser.add_argument("--category", type=str, default=None, help="Process only this category")
    parser.add_argument("--force", action="store_true", help="Re-process even if output exists")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without processing")
    parser.add_argument("--save-params", action="store_true", help="Save degradation parameters as JSON")
    parser.add_argument("--all", action="store_true", help="Include all PNGs, including legacy non-category dirs")
    parser.add_argument("--images-root", type=str, default=str(DEFAULT_IMAGE_BASE), help="Input image root")
    parser.add_argument("--output-root", type=str, default=str(DEFAULT_DEGRADED_BASE), help="Output image root")
    parser.add_argument("--params-root", type=str, default=str(DEFAULT_PARAMS_BASE), help="Output params root")
    parser.add_argument(
        "--format",
        type=str,
        default="png",
        choices=["jpg", "png"],
        help="Output format",
    )
    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=90,
        help="JPEG quality 1-100 when --format jpg is used",
    )
    args = parser.parse_args()

    process_all(
        category=args.category,
        force=args.force,
        dry_run=args.dry_run,
        save_params=args.save_params,
        all_images=args.all,
        output_format=args.format,
        jpeg_quality=args.jpeg_quality,
        image_root=Path(args.images_root),
        output_root=Path(args.output_root),
        params_root=Path(args.params_root),
    )


if __name__ == "__main__":
    main()
