#!/usr/bin/env python3
"""
Generate the full reusable sticker pack via chatgpt-image-latest, chroma-keyed to
true transparency. Two colour sets:
  Set A (pastel)  -> assets/stickers/pastel/<shape>.png
  Set B (brand)   -> assets/stickers/brand/<shape>.png

Reuses the generate + chroma_key pipeline from gen-sticker.py.
Run:  python3 tools/gen-sticker-pack.py            # all 14 shapes x 2 sets
      python3 tools/gen-sticker-pack.py folder star # just named shapes
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from importlib import import_module
g = import_module("gen-sticker")

CLAY = ("3D claymation style, soft rounded puffy edges, glossy smooth clay "
        "texture, gentle soft studio lighting, subtle soft shadow ON the object "
        "only, cute friendly icon, high detail, single object centred")

# shape -> short description
SHAPES = {
    "folder":  "a cute file folder icon",
    "star":    "a single rounded five-point star",
    "sparkle":  "a four-point sparkle / twinkle shape",
    "heart":   "a plump rounded heart",
    "arrow":   "a chunky rounded arrow pointing right",
    "screen":  "a tiny rounded computer monitor / window with a blank screen",
    "tick":    "a rounded check mark / tick inside a soft rounded square",
    "bubble":  "a rounded speech bubble",
    "bolt":    "a rounded lightning bolt",
    "flower":  "a simple rounded five-petal daisy flower",
    "cloud":   "a soft puffy rounded cloud",
    "pin":     "a rounded push pin / map pin",
    "bow":     "a cute ribbon bow",
    "lock":    "a small rounded padlock",
}

SETS = {
    "pastel": "warm cream, soft blush pink, sage green and terracotta pastel colour palette, matte-soft finish",
    # EDIT ME: describe YOUR brand palette (name the hexes from templates/brand.css)
    "brand":  "palette of slate blue (#3d5a80), warm amber (#e3a72f), light blue (#98c1d9) and off-white (#f5f3ee), playful",
}


def main():
    only = set(sys.argv[1:])
    base = os.path.join(os.path.dirname(__file__), "..", "assets", "stickers")
    made, failed = [], []
    for setname, palette in SETS.items():
        outdir = os.path.join(base, setname)
        os.makedirs(outdir, exist_ok=True)
        for shape, desc in SHAPES.items():
            if only and shape not in only:
                continue
            out = os.path.join(outdir, f"{shape}.png")
            prompt = f"{desc}, {CLAY}, {palette}."
            try:
                raw = g.generate(prompt, "1024x1024")
                g.chroma_key(raw, out)
                made.append(f"{setname}/{shape}")
                print("ok:", f"{setname}/{shape}")
            except Exception as e:
                failed.append(f"{setname}/{shape}: {type(e).__name__} {str(e)[:120]}")
                print("FAIL:", f"{setname}/{shape}", e)
            time.sleep(1)
    print(f"\nDONE — {len(made)} made, {len(failed)} failed")
    for f in failed:
        print("  ", f)


if __name__ == "__main__":
    main()
