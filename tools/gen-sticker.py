#!/usr/bin/env python3
"""
Generate a cute reusable sticker via OpenAI chatgpt-image-latest, then chroma-key
the flat background out to TRUE transparency.

Why chroma-key: chatgpt-image-latest ignores `background:transparent` and paints a
fake light background + white sticker outline. So we force a flat pure-magenta
(#FF00FF) backdrop in the prompt — a colour that never appears in a cute sticker —
then key it out cleanly. Anti-aliased edges via alpha falloff near the key colour.

Usage:
  python3 tools/gen-sticker.py "<subject prompt>" <out.png> [--size 1024x1024] [--keep-raw]

The script ADDS the background instruction automatically — your prompt should just
describe the object (e.g. "a cute 3D claymation star, soft pink").
Key: set the OPENAI_API_KEY environment variable (falls back to the
`env` block in ~/.claude/settings.json if you use Claude Code).
"""
import os, sys, json, base64, urllib.request, argparse

KEY_COLOUR = (255, 0, 255)  # magenta chroma key

BG_INSTRUCTION = (
    " The object is centred and isolated on a completely flat, solid, uniform "
    "pure magenta background (hex #FF00FF, RGB 255,0,255) that fills the entire "
    "frame edge to edge. No white border, no sticker outline, no drop shadow on "
    "the background, no gradient, no scene, no surface — just the object floating "
    "on flat magenta. The magenta must not appear anywhere on the object itself."
)


def load_key():
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    p = os.path.expanduser("~/.claude/settings.json")
    try:
        return json.load(open(p))["env"]["OPENAI_API_KEY"]
    except (FileNotFoundError, KeyError):
        sys.exit("Set the OPENAI_API_KEY environment variable first.")


def generate(prompt, size):
    key = load_key()
    body = json.dumps({
        "model": "chatgpt-image-latest",
        "prompt": prompt + BG_INSTRUCTION,
        "size": size,
        "n": 1,
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    r = json.load(urllib.request.urlopen(req, timeout=240))
    return base64.b64decode(r["data"][0]["b64_json"])


def _sample_bg(img):
    """Detect the actual flat background colour by averaging the four corners.
    chatgpt-image-latest often shifts our requested magenta to a hot pink, so we
    key out whatever it actually painted rather than a hardcoded colour."""
    w, h = img.size
    pts = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]
    rs = gs = bs = 0
    for x, y in pts:
        r, g, b, _ = img.getpixel((x, y))
        rs += r; gs += g; bs += b
    n = len(pts)
    return (rs // n, gs // n, bs // n)


def chroma_key(png_bytes, out_path):
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    kr, kg, kb = _sample_bg(img)
    px = img.load()
    w, h = img.size
    # Distance threshold: fully transparent at <=hard, opaque at >=soft, lerp between.
    hard = 80      # within this of the detected bg -> fully transparent
    soft = 150     # beyond this -> fully opaque (wider feather kills thin edge halos)
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            dist = (abs(r - kr) + abs(g - kg) + abs(b - kb))
            if dist <= hard:
                px[x, y] = (r, g, b, 0)
            elif dist < soft:
                frac = (dist - hard) / (soft - hard)
                px[x, y] = (r, g, b, int(255 * frac))
            # else: keep opaque
    # Trim transparent margins so the sticker is tightly cropped
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    img.save(out_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("out")
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--keep-raw", action="store_true")
    a = ap.parse_args()

    raw = generate(a.prompt, a.size)
    if a.keep_raw:
        open(a.out.replace(".png", "-raw.png"), "wb").write(raw)
    chroma_key(raw, a.out)
    print("ok:", a.out)


if __name__ == "__main__":
    main()
