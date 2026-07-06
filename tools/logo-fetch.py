#!/usr/bin/env python3
"""
logo-fetch.py — add a brand logo to the explainer-carousel logo library.

Pulls a clean coloured SVG from the Simple Icons CDN. If the brand isn't on
Simple Icons (or the network blocks it), writes a branded fallback tile SVG
(first letter on a coloured square) so the carousel never renders a broken image.

Usage:
    python3 logo-fetch.py <name> [slug] [hexcolour]
    python3 logo-fetch.py slack                  # tries slug=slack, brand colour
    python3 logo-fetch.py descript descript 000  # explicit slug + colour
    python3 logo-fetch.py mybrand "" 3d5a80      # force fallback tile (empty slug)

Logos land in ../assets/logos/<name>.svg  (kebab-case name = what you reference).
"""
import sys, os, urllib.request

LOGO_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "logos")

def fallback_tile(name, colour):
    letter = name[0].upper()
    col = colour.lstrip("#") or "262b33"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        f'<rect width="100" height="100" rx="22" fill="#{col}"/>'
        f'<text x="50" y="50" font-family="Arial,Helvetica,sans-serif" font-weight="700" '
        f'font-size="56" fill="#ffffff" text-anchor="middle" dominant-baseline="central">{letter}</text>'
        f'</svg>'
    )

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    name = sys.argv[1].lower()
    slug = sys.argv[2] if len(sys.argv) > 2 else name
    colour = (sys.argv[3] if len(sys.argv) > 3 else "").lstrip("#")
    os.makedirs(LOGO_DIR, exist_ok=True)
    out = os.path.join(LOGO_DIR, f"{name}.svg")

    if slug:
        # jsDelivr-pinned simple-icons is the reliable source (the cdn.simpleicons.org
        # convenience host 404s on many slugs). SVGs are monochrome — inject brand fill.
        url = f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
            data = urllib.request.urlopen(req, timeout=15).read()
            if b"<svg" in data[:200].lower():
                svg = data.decode("utf-8")
                if colour and "fill=" not in svg[:60]:
                    svg = svg.replace("<svg ", f'<svg fill="#{colour}" ', 1)
                with open(out, "w") as f:
                    f.write(svg)
                print(f"ok (simple-icons): {out}")
                return
            print(f"not an svg from {url} — using fallback tile")
        except Exception as e:
            print(f"fetch failed ({e}) — using fallback tile")

    with open(out, "w") as f:
        f.write(fallback_tile(name, colour))
    print(f"ok (fallback tile): {out}")

if __name__ == "__main__":
    main()
