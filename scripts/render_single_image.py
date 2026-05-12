"""
PureDocBench - Render HTML to single full-page PNG

One HTML → one PNG (full page screenshot, not paginated).

Usage:
    python scripts/render_single_image.py                              # All files
    python scripts/render_single_image.py --category academic/academic_paper
    python scripts/render_single_image.py --file-list mvp_files.txt
"""

import sys
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HTML_BASE = PROJECT_ROOT / "data" / "html"
IMAGE_BASE = PROJECT_ROOT / "data" / "images"


def render_batch(html_files: list, dpi: int = 300):
    """Render HTML files to full-page PNG screenshots."""
    scale = dpi / 96.0
    success = errors = 0

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 794, "height": 1123},  # A4 at 96dpi
            device_scale_factor=scale,
        )

        for i, html_path in enumerate(html_files):
            html_path = Path(html_path)
            rel = html_path.parent.relative_to(HTML_BASE)
            out_dir = IMAGE_BASE / rel
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / html_path.name.replace(".html", ".png")

            if out_path.exists():
                print(f"  [{i+1}/{len(html_files)}] skip {html_path.name}")
                continue

            try:
                page.goto(f"file://{html_path.resolve()}", wait_until="load", timeout=120000)
                page.wait_for_timeout(500)
                page.screenshot(path=str(out_path), full_page=True, type="png")
                success += 1
                print(f"  [{i+1}/{len(html_files)}] ✓ {html_path.name}")
            except Exception as e:
                errors += 1
                print(f"  [{i+1}/{len(html_files)}] ✗ {html_path.name}: {e}")

        browser.close()

    print(f"\nDone! Success: {success}, Errors: {errors}, Output: {IMAGE_BASE}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", type=str, default=None)
    parser.add_argument("--file-list", type=str, default=None)
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()

    if args.file_list:
        with open(args.file_list) as f:
            html_files = [HTML_BASE / line.strip() for line in f if line.strip()]
    elif args.category:
        html_files = sorted((HTML_BASE / args.category).glob("*.html"))
    else:
        html_files = sorted(HTML_BASE.rglob("*.html"))

    print(f"Rendering {len(html_files)} HTML files to single-image PNG (DPI={args.dpi})")
    render_batch(html_files, args.dpi)


if __name__ == "__main__":
    main()
