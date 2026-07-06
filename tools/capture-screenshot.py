#!/usr/bin/env python3
"""
capture-screenshot.py — grab a clean, retina screenshot of a URL for a
screenshot-card slide. Output is a PNG cropped to the visible viewport,
ready to drop into the .browser frame in the template.

Usage:
    python3 capture-screenshot.py <url> <out.png> [--w 1100] [--h 760] [--full]
    python3 capture-screenshot.py https://notion.so /tmp/notion.png --w 1100 --h 720

--full captures the whole scrollable page (good for tables/dashboards);
default captures just the viewport (cleaner for app UIs).

Requires Playwright Chromium. If it's not installed the script prints the
one-line install command instead of failing silently.
"""
import sys, subprocess

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    url, out = sys.argv[1], sys.argv[2]
    w = int(_flag("--w", 1100)); h = int(_flag("--h", 760))
    full = "--full" in sys.argv
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Run:\n  pip install playwright && playwright install chromium")
        sys.exit(2)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        # networkidle is ideal but busy marketing sites never go idle — fall back gracefully
        try:
            page.goto(url, wait_until="networkidle", timeout=20000)
        except Exception:
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
            except Exception:
                page.goto(url, wait_until="load", timeout=30000)
        page.wait_for_timeout(2500)  # let lazy content + fonts settle
        # dismiss common cookie / consent banners so they don't cover the hero
        for sel in ["text=/^Accept all$/i", "text=/^Accept$/i", "text=/^Reject all$/i",
                    "text=/^Got it$/i", "text=/^I agree$/i", "button:has-text('Accept')"]:
            try:
                el = page.locator(sel).first
                if el.is_visible(timeout=600):
                    el.click(timeout=600); page.wait_for_timeout(500); break
            except Exception:
                pass
        page.screenshot(path=out, full_page=full)
        browser.close()
    print(f"ok: {out}")

def _flag(name, default):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default

if __name__ == "__main__":
    main()
