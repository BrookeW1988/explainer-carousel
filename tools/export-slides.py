#!/usr/bin/env python3
"""
export-slides.py — render each .slide in a built carousel HTML to a 1080x1350 PNG.

Usage:
    python3 export-slides.py <carousel.html> <out_dir> [--prefix name]

Writes <out_dir>/<prefix>-01.png ... one PNG per .slide node, in document order.
Uses file:// so local logo SVGs + photos load. Requires Playwright Chromium.
"""
import sys, os
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    html = os.path.abspath(sys.argv[1])
    out_dir = os.path.abspath(sys.argv[2])
    prefix = _flag("--prefix", Path(html).stem)
    os.makedirs(out_dir, exist_ok=True)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Run:\n  pip install playwright && playwright install chromium")
        sys.exit(2)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        page.goto(f"file://{html}", wait_until="networkidle")
        page.wait_for_timeout(800)  # let webfonts paint
        slides = page.query_selector_all(".slide")
        if not slides:
            print("No .slide nodes found."); browser.close(); sys.exit(3)
        for i, s in enumerate(slides, 1):
            path = os.path.join(out_dir, f"{prefix}-{i:02d}.png")
            s.screenshot(path=path)
            print(f"ok: {path}")
        browser.close()
    print(f"\n{len(slides)} slides exported to {out_dir}")

def _flag(name, default):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default

if __name__ == "__main__":
    main()
