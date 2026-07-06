#!/usr/bin/env python3
"""
Import a dump of camera-roll photos into assets/photos/lifestyle/ with
orientation FIXED (the recurring HEIC trap: sips bakes raw pixels and drops
the EXIF rotation flag, so portrait shots land sideways).

Usage:
  import-photos.py <src-dir-or-files...>            # convert + auto-rotate into a staging dir
  import-photos.py ~/Downloads/IMG_28*.HEIC

What it does:
  1. Converts HEIC/HEIF -> JPG (via macOS `sips`).
  2. Reads the ORIGINAL EXIF Orientation and rotates the JPG upright
     (sips strips it on convert, so we re-apply it explicitly).
  3. Drops the upright JPGs in assets/photos/lifestyle/_staging/ with their
     original IMG_#### name, plus a checklist file.

Then a human (Claude) must: eyeball each in _staging/, rename to the
`<category>-<desc>.jpg` convention, move into lifestyle/, and add a row to
PHOTO-INDEX.md with the [face-*] tag. (Naming + face-tagging still needs eyes —
that part can't be automated reliably.)

Why staging not direct: orientation auto-fix is ~95% right but a few phone
shots have weird EXIF; the human glance in _staging catches the rare flip
before it pollutes the library.
"""
import sys, os, subprocess, glob

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIFE = os.path.join(SKILL, "assets", "photos", "lifestyle")
STAGE = os.path.join(LIFE, "_staging")

# EXIF Orientation value -> clockwise degrees sips must rotate to make upright.
# 1=normal(0) 3=180 6=90CW 8=270CW (the common phone values)
EXIF_ROT = {1: 0, 3: 180, 6: 90, 8: 270}

def exif_orientation(path):
    try:
        out = subprocess.run(["sips", "-g", "orientation", path],
                             capture_output=True, text=True, timeout=20).stdout
        for line in out.splitlines():
            if "orientation" in line.lower():
                v = line.strip().split()[-1]
                # sips prints names sometimes; map the digit if present
                return int(v) if v.isdigit() else 1
    except Exception:
        pass
    return 1

def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    files = []
    for a in args:
        if os.path.isdir(a):
            for ext in ("*.HEIC", "*.heic", "*.jpg", "*.jpeg", "*.png"):
                files += glob.glob(os.path.join(a, ext))
        else:
            files += glob.glob(a)
    files = sorted(set(files))
    if not files:
        sys.exit("No image files matched.")

    os.makedirs(STAGE, exist_ok=True)
    done = []
    for src in files:
        base = os.path.splitext(os.path.basename(src))[0]
        out = os.path.join(STAGE, base + ".jpg")
        # orientation from the ORIGINAL (before sips drops it)
        rot = EXIF_ROT.get(exif_orientation(src), 0)
        subprocess.run(["sips", "-s", "format", "jpeg", src, "--out", out],
                       capture_output=True, timeout=60)
        if rot:
            subprocess.run(["sips", "-r", str(rot), out, "--out", out],
                           capture_output=True, timeout=60)
        done.append((os.path.basename(out), rot))
        print(f"  {os.path.basename(out):<20} rotated {rot}CW")

    checklist = os.path.join(STAGE, "_TODO.md")
    with open(checklist, "w") as f:
        f.write("# Staged photos — eyeball, rename, file, tag\n\n")
        f.write("Auto-rotated on import. **Check each is upright** (rare EXIF cases flip wrong).\n")
        f.write("Then for each: rename to `<category>-<desc>.jpg`, move up into lifestyle/, "
                "add a PHOTO-INDEX.md row with the [face-upper|face-lower|face-centre|no-face] tag.\n\n")
        for name, rot in done:
            f.write(f"- [ ] `{name}` (rotated {rot}CW) -> rename + file + tag\n")
    print(f"\nStaged {len(done)} photos in {STAGE}")
    print(f"Next: eyeball each, then rename/file/tag per {checklist}")

if __name__ == "__main__":
    main()
