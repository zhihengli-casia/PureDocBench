#!/usr/bin/env python3
"""
PureDocBench Digital Degradation Pipeline v2
10 scene-based degradation profiles, GT-preserving only.
"""

import os
import sys
import json
import time
import argparse
import numpy as np
import cv2
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

# ============================================================
# Degradation Operations (pure OpenCV + numpy, no augraphy)
# ============================================================

def add_paper_texture(img, strength=0.3):
    """Add subtle paper grain texture."""
    h, w = img.shape[:2]
    noise = np.random.normal(0, 8 * strength, (h, w)).astype(np.float32)
    noise = cv2.GaussianBlur(noise, (5, 5), 1.5)
    result = img.astype(np.float32)
    for c in range(3):
        result[:, :, c] += noise
    return np.clip(result, 0, 255).astype(np.uint8)


def yellowing(img, strength=0.5):
    """Simulate paper aging / yellowing."""
    overlay = np.full_like(img, [50, 180, 240])  # warm yellow in BGR
    alpha = 0.08 * strength
    result = cv2.addWeighted(img, 1 - alpha, overlay, alpha, 0)
    # Reduce contrast slightly
    result = cv2.convertScaleAbs(result, alpha=1.0 - 0.15 * strength, beta=10 * strength)
    return result


def foxing_spots(img, strength=0.5):
    """Add aged foxing spots (brown dots)."""
    h, w = img.shape[:2]
    n_spots = int(30 * strength)
    result = img.copy()
    for _ in range(n_spots):
        cx, cy = np.random.randint(0, w), np.random.randint(0, h)
        radius = np.random.randint(3, int(8 + 10 * strength))
        color = (
            int(np.random.randint(60, 100)),
            int(np.random.randint(100, 150)),
            int(np.random.randint(150, 200)),
        )
        cv2.circle(result, (cx, cy), radius, color, -1)
        result = cv2.GaussianBlur(result, (5, 5), 1.0)
    return result


def fade_ink(img, strength=0.5):
    """Simulate faded ink / reduced contrast."""
    gray_target = np.full_like(img, 200)
    alpha = 0.3 * strength
    return cv2.addWeighted(img, 1 - alpha, gray_target, alpha, 0)


def book_curl(img, strength=0.5):
    """Simulate book page curl with mesh warp."""
    h, w = img.shape[:2]
    # Create a sinusoidal displacement field
    amplitude = int(15 * strength)
    cols = np.arange(w)
    # Horizontal displacement: stronger near left edge (binding)
    x_shift = amplitude * np.sin(np.pi * cols / w) * (1 - cols / w)
    map_x = np.zeros((h, w), dtype=np.float32)
    map_y = np.zeros((h, w), dtype=np.float32)
    for y in range(h):
        map_x[y, :] = cols + x_shift
        map_y[y, :] = y
    result = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return result


def binding_shadow(img, strength=0.5):
    """Add shadow gradient near left edge (book binding)."""
    h, w = img.shape[:2]
    shadow_width = int(w * 0.15 * strength)
    if shadow_width < 5:
        return img
    result = img.astype(np.float32)
    gradient = np.linspace(0.4, 1.0, shadow_width)
    for x in range(shadow_width):
        result[:, x, :] *= gradient[x]
    return np.clip(result, 0, 255).astype(np.uint8)


def bleed_through(img, strength=0.3):
    """Simulate reverse-side text bleeding through."""
    h, w = img.shape[:2]
    flipped = cv2.flip(img, 1)
    gray = cv2.cvtColor(flipped, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    thresh = cv2.GaussianBlur(thresh, (7, 7), 2.0)
    mask = (thresh / 255.0 * 0.08 * strength).astype(np.float32)
    result = img.astype(np.float32)
    for c in range(3):
        result[:, :, c] -= mask * 80
    return np.clip(result, 0, 255).astype(np.uint8)


def copy_contrast_boost(img, strength=0.5):
    """Simulate photocopier contrast enhancement."""
    alpha = 1.0 + 0.5 * strength
    beta = -30 * strength
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)


def dirty_drum(img, strength=0.5):
    """Simulate copier dirty drum marks (periodic vertical lines)."""
    h, w = img.shape[:2]
    result = img.copy()
    n_lines = int(3 + 5 * strength)
    for _ in range(n_lines):
        x = np.random.randint(0, w)
        thickness = np.random.randint(1, 3)
        alpha = np.random.uniform(0.05, 0.15) * strength
        cv2.line(result, (x, 0), (x, h), (100, 100, 100), thickness)
    return cv2.addWeighted(img, 1 - 0.3 * strength, result, 0.3 * strength, 0)


def generation_loss(img, strength=0.5):
    """Simulate multi-generation copy loss: blur + noise + contrast."""
    n_gen = int(2 + 3 * strength)
    result = img.copy()
    for _ in range(n_gen):
        ksize = 3
        result = cv2.GaussianBlur(result, (ksize, ksize), 0.8)
        noise = np.random.normal(0, 3, result.shape).astype(np.float32)
        result = np.clip(result.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        result = cv2.convertScaleAbs(result, alpha=1.05, beta=-5)
    return result


def thermal_effect(img, strength=0.5):
    """Simulate thermal/fax printer output."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Push toward binary
    alpha = 1.5 + strength
    beta = -60 * strength
    gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    # Add horizontal streaks
    h, w = gray.shape
    n_streaks = int(10 + 20 * strength)
    for _ in range(n_streaks):
        y = np.random.randint(0, h)
        thickness = np.random.randint(1, 2)
        gray[y:y + thickness, :] = np.clip(
            gray[y:y + thickness, :].astype(np.int16) + np.random.randint(-40, 40),
            0, 255
        ).astype(np.uint8)
    # Slight yellowing
    result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    yellow_tint = np.full_like(result, [200, 230, 245])
    result = cv2.addWeighted(result, 0.85, yellow_tint, 0.15 * strength, 0)
    return result


def low_quality_print(img, strength=0.5):
    """Simulate low-quality printer: banding + toner shortage."""
    h, w = img.shape[:2]
    result = img.astype(np.float32)
    # Horizontal banding (toner roller artifacts)
    band_period = int(30 + 50 * (1 - strength))
    for y in range(0, h, band_period):
        band_h = min(int(band_period * 0.3), h - y)
        fade = np.random.uniform(0.85, 0.95)
        result[y:y + band_h, :, :] *= fade
    # Random toner shortage streaks
    n_streaks = int(5 + 10 * strength)
    for _ in range(n_streaks):
        y_start = np.random.randint(0, h)
        y_end = min(y_start + np.random.randint(20, 60), h)
        x_start = np.random.randint(0, w)
        x_width = np.random.randint(2, 6)
        result[y_start:y_end, x_start:x_start + x_width, :] *= 0.7
    return np.clip(result, 0, 255).astype(np.uint8)


def ink_bleed(img, strength=0.5):
    """Simulate ink bleeding / spreading on paper."""
    # Dilate dark regions
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    ksize = int(3 + 2 * strength)
    if ksize % 2 == 0:
        ksize += 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    dilated_mask = cv2.dilate(mask, kernel, iterations=1)
    # Blur the dilated mask for soft edges
    dilated_mask = cv2.GaussianBlur(dilated_mask, (5, 5), 1.5)
    # Apply to image
    result = img.astype(np.float32)
    blend = dilated_mask.astype(np.float32) / 255.0 * 0.4 * strength
    for c in range(3):
        result[:, :, c] = result[:, :, c] * (1 - blend) + 50 * blend
    return np.clip(result, 0, 255).astype(np.uint8)


def jpeg_compress(img, quality=50):
    """Apply JPEG compression artifacts."""
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, buf = cv2.imencode('.jpg', img, encode_param)
    return cv2.imdecode(buf, cv2.IMREAD_COLOR)


def resolution_downup(img, scale=0.5):
    """Downsample then upsample to simulate resolution loss."""
    h, w = img.shape[:2]
    small = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR)


def uneven_lighting(img, strength=0.5):
    """Apply strong uneven lighting gradient."""
    h, w = img.shape[:2]
    # Random gradient direction
    angle = np.random.uniform(0, 2 * np.pi)
    cx, cy = w / 2, h / 2
    Y, X = np.mgrid[0:h, 0:w]
    gradient = ((X - cx) * np.cos(angle) + (Y - cy) * np.sin(angle))
    gradient = gradient / (max(w, h) / 2)  # normalize to [-1, 1]
    gradient = 1.0 + gradient * 0.35 * strength
    gradient = np.clip(gradient, 0.5, 1.5).astype(np.float32)
    result = img.astype(np.float32)
    for c in range(3):
        result[:, :, c] *= gradient
    return np.clip(result, 0, 255).astype(np.uint8)


def vignette(img, strength=0.5):
    """Add dark vignette around edges."""
    h, w = img.shape[:2]
    Y, X = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2, h / 2
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    max_dist = np.sqrt(cx ** 2 + cy ** 2)
    mask = 1.0 - (dist / max_dist) ** 2 * 0.5 * strength
    mask = np.clip(mask, 0.3, 1.0).astype(np.float32)
    result = img.astype(np.float32)
    for c in range(3):
        result[:, :, c] *= mask
    return np.clip(result, 0, 255).astype(np.uint8)


def perspective_warp(img, strength=0.5):
    """Apply perspective distortion."""
    h, w = img.shape[:2]
    max_shift = int(20 * strength)
    pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    shifts = np.random.randint(-max_shift, max_shift + 1, (4, 2)).astype(np.float32)
    # Keep corners roughly in place
    pts2 = pts1 + shifts
    M = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)


def barrel_distortion(img, strength=0.3):
    """Apply barrel/pincushion lens distortion."""
    h, w = img.shape[:2]
    k1 = 0.3 * strength * np.random.choice([-1, 1])
    cx, cy = w / 2, h / 2
    Y, X = np.mgrid[0:h, 0:w].astype(np.float32)
    X_n = (X - cx) / cx
    Y_n = (Y - cy) / cy
    r2 = X_n ** 2 + Y_n ** 2
    X_d = X_n * (1 + k1 * r2)
    Y_d = Y_n * (1 + k1 * r2)
    map_x = (X_d * cx + cx).astype(np.float32)
    map_y = (Y_d * cy + cy).astype(np.float32)
    return cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def rotation(img, max_angle=3.0):
    """Random slight rotation."""
    angle = np.random.uniform(-max_angle, max_angle)
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)


def gaussian_noise(img, sigma=15):
    """Add Gaussian noise."""
    noise = np.random.normal(0, sigma, img.shape).astype(np.float32)
    return np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def motion_blur(img, ksize=7, angle=0):
    """Apply motion blur."""
    if ksize < 3:
        return img
    kernel = np.zeros((ksize, ksize))
    mid = ksize // 2
    kernel[mid, :] = 1.0 / ksize
    M = cv2.getRotationMatrix2D((mid, mid), angle, 1.0)
    kernel = cv2.warpAffine(kernel, M, (ksize, ksize))
    kernel = kernel / kernel.sum()
    return cv2.filter2D(img, -1, kernel)


def color_temp_shift(img, shift='warm'):
    """Shift color temperature."""
    result = img.astype(np.float32)
    if shift == 'warm':
        result[:, :, 2] = np.clip(result[:, :, 2] * 1.08, 0, 255)  # R up
        result[:, :, 0] = np.clip(result[:, :, 0] * 0.92, 0, 255)  # B down
    else:
        result[:, :, 0] = np.clip(result[:, :, 0] * 1.08, 0, 255)  # B up
        result[:, :, 2] = np.clip(result[:, :, 2] * 0.92, 0, 255)  # R down
    return result.astype(np.uint8)


# ============================================================
# Scene Profiles
# ============================================================

SCENE_PROFILES = {
    "aged_archive": {
        "description": "Aged archival document: yellowed paper, faded ink, foxing spots",
        "apply": lambda img, s: foxing_spots(
            fade_ink(yellowing(add_paper_texture(img, s), s), s), s
        ),
    },
    "book_binding": {
        "description": "Book page scan: page curl, binding shadow, bleed-through",
        "apply": lambda img, s: bleed_through(
            binding_shadow(book_curl(add_paper_texture(img, s * 0.3), s), s), s
        ),
    },
    "multi_gen_copy": {
        "description": "Multi-generation photocopy: contrast loss, blur, drum marks",
        "apply": lambda img, s: dirty_drum(
            generation_loss(copy_contrast_boost(img, s * 0.5), s), s
        ),
    },
    "fax_thermal": {
        "description": "Fax/thermal print: near-binary, streaks, yellowing",
        "apply": lambda img, s: thermal_effect(img, s),
    },
    "low_quality_print": {
        "description": "Low quality printer: banding, toner shortage, streaks",
        "apply": lambda img, s: low_quality_print(
            add_paper_texture(img, s * 0.3), s
        ),
    },
    "ink_bleed": {
        "description": "Ink bleeding: text spreading, paper absorption",
        "apply": lambda img, s: add_paper_texture(
            ink_bleed(img, s), s * 0.5
        ),
    },
    "heavy_compression": {
        "description": "Heavy JPEG compression + resolution loss",
        "apply": lambda img, s: jpeg_compress(
            resolution_downup(img, max(0.3, 1.0 - 0.5 * s)),
            max(15, int(80 - 60 * s))
        ),
    },
    "uneven_lighting": {
        "description": "Strong uneven lighting with vignette and overexposure",
        "apply": lambda img, s: vignette(
            uneven_lighting(img, s), s
        ),
    },
    "geometric_distort": {
        "description": "Perspective + barrel distortion + rotation",
        "apply": lambda img, s: rotation(
            barrel_distortion(perspective_warp(img, s), s * 0.5),
            max_angle=1.0 + 3.0 * s
        ),
    },
    "noise_blur_combo": {
        "description": "Heavy noise + motion blur + color temperature shift",
        "apply": lambda img, s: color_temp_shift(
            motion_blur(
                gaussian_noise(img, sigma=int(10 + 30 * s)),
                ksize=max(3, int(3 + 8 * s)),
                angle=np.random.uniform(0, 180)
            ),
            shift=np.random.choice(['warm', 'cool'])
        ),
    },
}

SEVERITY_MAP = {
    "mild": 0.3,
    "moderate": 0.6,
    "severe": 0.9,
}


def process_single(args):
    """Process a single image with a given scene and severity."""
    src_path, dst_path, param_path, scene_name, severity_val = args
    try:
        img = cv2.imread(str(src_path), cv2.IMREAD_COLOR)
        if img is None:
            return f"FAIL: cannot read {src_path}"

        profile = SCENE_PROFILES[scene_name]
        degraded = profile["apply"](img, severity_val)

        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        cv2.imwrite(str(dst_path), degraded)

        # Save params
        os.makedirs(os.path.dirname(param_path), exist_ok=True)
        params = {
            "source": str(src_path),
            "scene": scene_name,
            "severity": severity_val,
            "description": profile["description"],
        }
        with open(str(param_path), 'w') as f:
            json.dump(params, f, ensure_ascii=False, indent=2)

        return f"OK: {os.path.basename(dst_path)}"
    except Exception as e:
        return f"FAIL: {src_path} -> {e}"


def main():
    parser = argparse.ArgumentParser(description="PureDocBench Degradation Pipeline")
    parser.add_argument("--src", required=True, help="Source image directory")
    parser.add_argument("--dst", required=True, help="Output directory")
    parser.add_argument("--scenes", nargs="+", default=list(SCENE_PROFILES.keys()),
                        help="Scenes to apply (default: all)")
    parser.add_argument("--severity", default="moderate", choices=list(SEVERITY_MAP.keys()),
                        help="Severity level")
    parser.add_argument("--workers", type=int, default=8, help="Parallel workers")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of images (0=all)")
    args = parser.parse_args()

    src_root = Path(args.src)
    dst_root = Path(args.dst)
    severity_val = SEVERITY_MAP[args.severity]

    # Collect all source images
    all_images = sorted(src_root.rglob("*.png"))
    if args.limit > 0:
        all_images = all_images[:args.limit]

    print(f"Source: {src_root}")
    print(f"Found {len(all_images)} images")
    print(f"Scenes: {args.scenes}")
    print(f"Severity: {args.severity} ({severity_val})")
    print(f"Workers: {args.workers}")

    # Assign scenes round-robin
    scene_list = args.scenes
    tasks = []
    for i, src_path in enumerate(all_images):
        rel = src_path.relative_to(src_root)
        scene = scene_list[i % len(scene_list)]
        stem = src_path.stem
        suffix = f"__{scene}"

        dst_path = dst_root / scene / rel.parent / f"{stem}{suffix}.png"
        param_path = dst_root / "params" / scene / rel.parent / f"{stem}{suffix}.json"
        tasks.append((str(src_path), str(dst_path), str(param_path), scene, severity_val))

    print(f"\nTotal tasks: {len(tasks)}")
    print(f"Starting...")

    t0 = time.time()
    done = 0
    fail = 0
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(process_single, t) for t in tasks]
        for future in as_completed(futures):
            result = future.result()
            if result.startswith("FAIL"):
                fail += 1
                print(result)
            else:
                done += 1
            if done % 100 == 0:
                elapsed = time.time() - t0
                speed = done / elapsed
                eta = (len(tasks) - done) / speed if speed > 0 else 0
                print(f"  [{done}/{len(tasks)}] {speed:.1f} img/s, ETA {eta:.0f}s")

    elapsed = time.time() - t0
    print(f"\nDone: {done} ok, {fail} fail, {elapsed:.1f}s total")

    # Write manifest
    manifest = {
        "source": str(src_root),
        "output": str(dst_root),
        "scenes": args.scenes,
        "severity": args.severity,
        "severity_val": severity_val,
        "total_images": len(all_images),
        "total_outputs": done,
        "failed": fail,
        "elapsed_seconds": round(elapsed, 1),
    }
    manifest_path = dst_root / "manifest.json"
    os.makedirs(dst_root, exist_ok=True)
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
