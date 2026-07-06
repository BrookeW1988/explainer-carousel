# Make it yours

This repo ships a carousel *system*, not a brand. Out of the box it renders in a deliberately plain starter palette. This guide is the part that matters: how to turn the system into carousels that look like YOU — your colours, your fonts, your photos, your stickers.

Budget an hour for the whole thing. It's a one-off; every carousel after that is minutes.

## 1. Your brand kit (`templates/brand.css`) — 10 minutes

Every template and theme reads its colours and fonts from one file: [templates/brand.css](templates/brand.css). Keep the variable NAMES, change the VALUES.

### Colours — 5 roles

| Variable | Role | Pick something that… |
|---|---|---|
| `--ink` | text, borders, hard shadows | is near-black but tinted toward your palette (pure `#000` looks flat) |
| `--paper` | page background | is off-white/cream — never pure white, it reads clinical |
| `--accent` | statement backgrounds, kickers | is your main brand colour, dark enough for white text on top |
| `--pop` | THE highlighted word, CTA keyword box | is loud. This is the colour people will associate with your feed |
| `--fill` | stickers, soft highlight bars | is light/bright — must be readable with `--ink` text on it |

A quick way to get a palette that's actually yours: pull the dominant colours from your existing feed, website, or logo (any "extract palette from image" tool works), then adjust for the roles above.

### Fonts — 7 roles

Pick fonts on [Google Fonts](https://fonts.google.com), load them in the template `<head>`, then set the variables. The two that define your look:

- `--font-display` — the chunky headline font. This is 80% of your visual identity. Spend your time here. Avoid whatever is trending in AI-generated design this month; pick something you'd put on a T-shirt.
- `--font-hand` — the handwritten "save this!" accent font.

The other five (`--font-body`, `--font-round`, `--font-mono`, `--font-serif`, `--font-grotesque`) can stay near the defaults, but distinctive picks compound — a serif nobody else uses does more for recognisability than any colour.

**Test it:** render the master template once (`.venv/bin/python tools/export-slides.py templates/explainer-carousel.html .tmp/test`) and look at the PNGs. If the cover could belong to anyone, keep iterating.

## 2. Your photo inventory — 20 minutes, then ongoing

Photo covers are what stop the scroll, and they're the one asset nobody can copy from you. Build a small library once and every carousel build can pick from it.

### Set up the library

```
assets/photos/
  covers/      # your best "cover-grade" shots — polished or striking
  lifestyle/   # candid camera-roll shots, the "photo dump" aesthetic
```

Import a camera-roll dump (handles HEIC → JPG and auto-rotates using the original EXIF, so portraits don't land sideways):

```bash
python3 tools/import-photos.py ~/Downloads/IMG_28*.HEIC
```

That drops upright JPGs into `assets/photos/lifestyle/_staging/`. Then for each photo:

1. **Rename** to `<category>-<description>.jpg` — pick 6–10 categories that fit YOUR life. Examples: `work-`, `travel-`, `food-`, `event-`, `selfie-candid-`, `outdoor-`. The categories are how future builds find "a travel shot" without eyeballing 80 files.
2. **Tag the face position** and log it in `assets/photos/lifestyle/PHOTO-INDEX.md` (template provided): `[face-upper]`, `[face-lower]`, `[face-centre]`, or `[no-face]`.
3. **Move** it up out of `_staging/`.

### Why the face tags matter

Photo-theme slides put a white text card over the photo. The tag tells the build where the card can go WITHOUT covering your face:

- `[face-upper]` → card hugs the bottom (`card-bottom`)
- `[face-lower]` → card hugs the top (`card-top`)
- `[face-centre]` → top or bottom, never centred
- `[no-face]` → centred is fine

Tag once, and every future carousel places text correctly without anyone re-checking the image.

### What makes a good cover photo

Action beats posed. Big sky / negative space gives the headline somewhere to sit. Candid outperforms polished more often than you'd expect. And use YOUR photos — stock photography on this format reads instantly fake.

## 3. Your logo library — 5 minutes

The logo-list slide uses real product logos, stored locally so renders never depend on a CDN:

```bash
python3 tools/logo-fetch.py <name> <simpleicons-slug> <brand-hex>
# e.g.
python3 tools/logo-fetch.py notion notion 000000
python3 tools/logo-fetch.py canva canva 00C4CC
```

Slugs and brand hexes are at [simpleicons.org](https://simpleicons.org). If a tool isn't on Simple Icons, the script falls back to a branded letter tile, or grab the favicon: `https://www.google.com/s2/favicons?domain=<tool>.com&sz=256`.

Fetch the 15–25 tools YOU actually talk about. That's your library.

## 4. Your stickers and doodles — 15 minutes (optional, needs an OpenAI key)

Scattered doodles and stickers are the "texture" layer that makes slides feel handmade. Generate your own set instead of downloading a pack everyone else has:

```bash
# one sticker, chroma-keyed to true transparency:
python3 tools/gen-sticker.py "a flat hand-drawn marker star doodle, single colour, thick marker strokes" assets/stickers/doodles/star.png

# a whole pack (edit the SHAPES + SETS dicts in the script first —
# put YOUR palette hexes in the "brand" set prompt):
python3 tools/gen-sticker-pack.py
```

Style prompts that work well: "flat hand-drawn marker doodle" (messy, personal), "cute 8-bit pixel-art sticker" (y2k themes), "realistic photo cutout object on white" (collage theme). Pick ONE style family and generate 10–16 shapes in it — consistency across your set matters more than any individual sticker.

### Collage cutout objects — the "this is me" layer

The scrapbook-collage theme scatters realistic cutout objects (think: your actual coffee order, your sunglasses, your gym keys). This is the most personal asset in the whole system — choose objects from YOUR daily life, not generic ones:

```bash
# generate a row sprite-sheet with any image model:
#   "8 realistic cutout objects on a pure white background, evenly spaced in one row:
#    a matcha latte, tortoiseshell glasses, ..."
# then slice it into transparent PNGs:
python3 tools/slice-collage-objects.py sheet.png matcha glasses books keys phone croissant
```

Cluster several on the cover (the "life jumble"), then ONE per inner slide.

## 5. Your screenshots

- **Real app UIs:** `python3 tools/capture-screenshot.py <url> <out.png>` (Playwright, retina). Heavily JS-gated or Cloudflare-walled apps will block it — screenshot those by hand.
- **Your own setup:** screenshot it yourself, drop it in `assets/screenshots/source/`. To scrub private bits (names, numbers): `python3 tools/edit-image.py in.png out.png "keep everything the same but remove the sidebar thread names"`.
- **Receipts:** screenshot your own best-performing posts into `assets/photos/` for social-proof slides. Yours, not anyone else's.

## 6. Going further — your own theme

Once the brand kit is in, the eight themes already render "as you". If you want a look nobody else has:

1. Copy the closest theme block in [templates/themes/themes.css](templates/themes/themes.css) to a new class (e.g. `.theme-mine`).
2. Change the decoration language — border weight, shadow style (hard offset vs soft blur), corner radius, tilt angles, background texture. These choices, more than colour, are what make a feed recognisable.
3. Keep the slide-type bones (cover/statement/list/shot/cta) — that structure is what makes builds automatic.

## The one rule

Don't post the starter palette, and don't lift another creator's palette/fonts/photos into `brand.css`. The format is shared; the *look* is the asset. Build yours.
