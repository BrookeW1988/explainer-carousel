#!/usr/bin/env python3
"""
Slice a row sprite-sheet of cutout objects into individual transparent PNGs.

Generate the sheet first (e.g. with an image model): one wide image containing
N objects in a single row on a PURE WHITE background — "realistic cutout
objects on white, evenly spaced in one row". Then:

  python3 tools/slice-collage-objects.py <sheet.png> <name1> <name2> ... [--out assets/stickers/collage]

Each cell is cropped, the white background is keyed to transparency, and the
result is auto-cropped to the object's bounding box.
"""
import argparse, os
from PIL import Image


def near_white(c, tol=22):
    return all(c[i] >= 255 - tol for i in range(3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet", help="row sprite-sheet PNG on white background")
    ap.add_argument("names", nargs="+", help="one name per object, left to right")
    ap.add_argument("--out", default="assets/stickers/collage")
    args = ap.parse_args()

    sheet = Image.open(args.sheet).convert("RGBA")
    W, H = sheet.size
    n = len(args.names)
    cellw = W // n
    os.makedirs(args.out, exist_ok=True)
    inset = int(cellw * 0.05)  # trim cell edges so neighbours never bleed in

    for i, name in enumerate(args.names):
        cell = sheet.crop((i * cellw + inset, 0, (i + 1) * cellw - inset, H))
        px = cell.load()
        cw, ch = cell.size
        for y in range(ch):
            for x in range(cw):
                r, g, b, a = px[x, y]
                if near_white((r, g, b)):
                    px[x, y] = (r, g, b, 0)
        bbox = cell.getbbox()
        if bbox:
            cell = cell.crop(bbox)
        out = os.path.join(args.out, f"{name}.png")
        cell.save(out)
        print(f"{out} {cell.size}")


if __name__ == "__main__":
    main()
