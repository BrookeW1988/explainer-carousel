---
name: explainer-carousel
description: Build an explainer carousel (photo cover + bold statement + numbered logo list + framed screenshot card + comment-keyword CTA) in the user's brand, defined in templates/brand.css. Real product logos from a local library, real screenshots via Playwright (AI mockup fallback). Use when the user says "explainer carousel", "logo carousel", "make a carousel with logos/screenshots", or "tools/stack carousel".
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
argument-hint: <topic or angle> [--keyword KEYWORD] [--cover photo-name] [--count N]
---

# /explainer-carousel

Builds the **logo + screenshot explainer carousel** style — photo cover, numbered list of real product logos, framed app screenshots, comment-keyword CTA. Renders one 1080×1350 PNG per slide (IG 4:5 portrait).

## ⚠️ First-run check

If `templates/brand.css` still contains the starter palette (the file says so in its header comment) or `assets/photos/` is empty, STOP and point the user at `MAKE-IT-YOURS.md` before building anything. A carousel in the starter palette is a demo, not a deliverable.

## ⚠️ ALWAYS verify your own work before showing the user

After EVERY render, **Read the output PNG yourself and look at it critically** before presenting it. Don't just confirm "it rendered" — judge it like a designer:
- Is the headline ONE clean block, or ragged/staircased strips? (`box-decoration-break:clone` makes per-line bands that don't align — avoid for multi-line headlines; use a single background container instead.)
- Does text overlap the busy part of the photo / clip a doodle / get cut off at an edge?
- Is everything sized consistently (headline vs subbar vs sticker), or does something look tiny/cramped?
- Do the colours/fonts match the chosen theme, or is something falling back to base styling?

If it looks messy, FIX IT and re-render before showing — iterate until it's clean.

## Themes (pick ONE per carousel — for feed variety)

Add one theme class to a wrapper or `<body>`. Same 5 slide types, different flavour. Rotate themes across posts so the feed doesn't look samey. All themes read colours/fonts from `templates/brand.css`.

**On-brand themes** (your brand.css palette):

| Theme | Vibe | When to use |
|---|---|---|
| `theme-scrappy` | Busy, bold ink blocks, offset hard shadows, halftone dots, taped stickers. The "24 things to install" energy. | Punchy tool/stack lists, "everything you need" posts, high-energy hooks |
| `theme-clean` | Structured cards, soft fills, calm white space, one accent. | Premium/considered topics, frameworks, dense content that needs to breathe |
| `theme-photo` | Full-bleed lifestyle photo, bold white headline blocks, save badge. | Photo-first covers, strong scroll-stop |
| `theme-editorial theme-brand` | Calm editorial layout on your palette. | "The mistake → the fix" posts, premium-but-warm |

**Looser themes** (softer self-contained palettes, deliberately off-brand for variety):

| Theme | Vibe | When to use |
|---|---|---|
| `theme-y2k` | Checkerboard cover, pink TV-frame card, gridded paper, rounded multi-colour headers, pixel stickers. | Playful, nostalgic round-ups; lighter topics |
| `theme-y2k y2k-mess` | Maximalist scrapbook chaos: rows tilt different ways, mixed box colours, big hard shadows. | Vibey "tools I use" round-ups |
| `theme-editorial` | Soft cream paper, gridded bg, rounded headers + mono eyebrows, gentle shadows. | Calm/considered posts |
| `theme-scrapbook` | Warm paper texture, tilted index cards, dashed stickers, handwritten feel. | Lists of books/products/picks, curated round-ups |
| `theme-zine` | Aged paper, serif italic headline, olive/pink/tan info boxes, collaged screenshots. | Editorial "pick this if" comparisons |
| `collage` (scrapbook-collage) | Gridded notebook paper + spiral edge, big display name, coloured info boxes, screenshots as flat tilted cutout CARDS, realistic cutout objects scattered. Stylesheet: `templates/themes/scrapbook-collage.css`. | Tool/app round-ups, "my stack" — the premium editorial pick |

> ⚠️ The `y2k-device` slide (screenshot composited onto a tiny retro device screen) exists in themes.css but reads badly at feed size — letterboxing, fiddly screen-rect calibration. Prefer big-logo tiles or `y2k-mess` with devices as small decoration. Only use screen-compositing if explicitly asked.

### Doodle accents
Scattered flat hand-drawn marker doodles make slides feel handmade. PNGs live at `assets/stickers/doodles/` (the user generates their own — see MAKE-IT-YOURS.md). Drop as absolutely-positioned `<img class="doodle">` (z-index above content), ~70–140px, scattered in corners/edges. Small scattered doodles read better than big stickers.

### Scrapbook-collage layout notes
- **Per tool slide:** `.collage` slide → `.spiral` (18 `<i>` rings) + `.pagepill` + `.tab` + `.logochip` (real logo top-right) + `.name` + `.url` + `.box.olive` ("I use it for") + `.box.cream` ("how I actually use it") + `.card.tilt-l/-r` (screenshot as flat cutout with `.cap`) + `.box.outline` ("why it wins") + ONE `.obj` cutout bottom-left.
- **Gotcha:** keep `.obj` out of the box zones — bottom-left (`bottom:160px; left:130px`) is the proven clean spot. ONE object per inner slide; cluster several only on the cover.

### Screenshot frames (texture + depth)
Wrap any screenshot `<img>` in `<div class="screenshot frame-X">`:
- `.frame-soft` — cream card: thin border, soft drop-shadow, slight tilt. **DEFAULT.** Add `.flat` or `.tilt-r` to change tilt.
- `.frame-browser` — mac chrome bar (traffic-light dots + URL). Add a `.bar` div with `.d.r/.d.y/.d.g` + `.url`.
- `.frame-polaroid` — taped photo + handwritten `.cap`. Small/square images only.

## Story / launch carousels (not just lists)

The templates also work for a NARRATIVE arc (cover → claim → claim → CTA), not only tool/logo lists. Pattern: pick a theme, write a cover hook + 3–4 `statement`/claim beats teasing the arc, end on the comment-keyword CTA. No hard revenue figures presented as typical; don't invent urgency.

## Row styles (mix into any theme)

The theme controls decoration; the **row style** controls layout:
- `.row` (default) — number + **logo tile** + name + desc. For app/tool lists.
- `.row.folder` — number + **macOS folder glyph** + name + desc. For non-app lists.
- `.row.float` — number + **floating cover image** (book/product) + name + desc. For book/product round-ups.

## Receipts slide (social proof)

`.slide.receipts` frames the user's OWN post screenshots as proof (view counts, results). Only ever use the user's real screenshots — never fabricate metrics, never use someone else's posts.

## The 5 slide types

A carousel mixes these (typically 5–8 slides):

1. **Cover** — brand photo + chunky headline block + curiosity sub-bar + "save this" sticker. Headline 5–10 words, ONE `--pop` highlight phrase.
2. **Statement** — solid accent/ink bg, big display-font claim, one highlighted phrase, a supporting line. The "here's the premise" beat.
3. **Logo list** — numbered rows, each with a **real product logo** + name + one-line description. The signature slide. 4–8 rows max (more = split into two list slides).
4. **Screenshot card** — "NN / THE THING" heading + a lede + a framed screenshot + a footnote. Real Playwright capture OR an AI/HTML mockup.
5. **CTA** — brand photo + "COMMENT [KEYWORD]" (keyword in `--pop` box) + one line + the user's @handle + brand lockup.

Typical structure: Cover → Statement → Logo list → Screenshot card(s) → CTA.

## Brand

Everything visual comes from `templates/brand.css` — colours (`--ink --paper --accent --pop --fill`) and fonts (`--font-display --font-body --font-hand --font-round --font-mono --font-serif --font-grotesque`). Never hardcode colours or fonts in slide HTML; never edit brand.css during a build (that's the user's file).

Write copy in the user's voice. If they have a style guide or banned-phrases list, load it before writing. Either way, no LLM-tells: "game-changing", "unlock", "dive in", "level up", "Whether you're X, Y, or Z".

## Assets (all local, in this skill folder)

- **Logos:** `assets/logos/<name>.svg` — add with `tools/logo-fetch.py <name> <slug> <hex>` (Simple Icons via jsDelivr; falls back to a branded tile).
- **Photos:** `assets/photos/covers/` (cover-grade) + `assets/photos/lifestyle/` (candid, catalogued in `PHOTO-INDEX.md` with face-position tags).
- **Doodles/stickers:** `assets/stickers/doodles/` + `assets/stickers/collage/` (user-generated; `tools/gen-sticker.py`).
- **Screenshots:** `assets/screenshots/` — real captures + `mockups/` + `source/` (the user's own shots).
- **Template:** `templates/explainer-carousel.html` — the 5 types with `{{...}}` placeholders.

## Workflow

### Stage 1 — Parse + plan slides
1. Take the topic/angle. Extract flags: `--keyword`, `--cover <photo-name>`, `--count`.
2. Decide the slide list (which types, in order). Default: Cover → Statement → 1 Logo list → 1 Screenshot card → CTA.
3. Write the copy for each slide (word limits per type above, user's voice).
4. For the **logo list**, map each row to a real logo file in `assets/logos/`. Missing → `tools/logo-fetch.py`.
5. For each **screenshot card**, decide the source:
   - **Real URL** → `tools/capture-screenshot.py <url> .tmp/<name>.png` (Playwright, retina). JS-heavy / Cloudflare-walled apps will time out — use a mockup or ask the user for a real screenshot instead.
   - **User's real screenshot** (best for their private setup) → copy to `assets/screenshots/source/`. To scrub private bits: `tools/edit-image.py <in> <out> "keep everything the same but <change>"`.
   - **No URL + no real shot** → generate a plausible UI mockup (`tools/gen-sticker.py`-style call). Keep mockups plausible — don't invent numbers that misrepresent.
6. **Present the slide plan + copy and wait for approval** before building HTML. Show: each slide's type, headline/copy, which logos, which screenshot source.

### Stage 2 — Build HTML
1. Copy `templates/explainer-carousel.html` to `.tmp/explainer-<slug>.html`.
2. Fill placeholders (including `{{BRAND_WORD_1}}/{{BRAND_WORD_2}}` and `{{HANDLE}}` from the user's brand). For logo lists, repeat the `.row` block per item. For screenshot cards, set `{{SHOT_IMG}}` to the captured PNG (relative path).
3. Asset paths are relative: `../assets/photos/covers/<file>`.

### Stage 3 — Render to PNG
```
.venv/bin/python tools/export-slides.py .tmp/explainer-<slug>.html .tmp/out --prefix <slug>
```
Outputs one 1080×1350 PNG per slide (2× retina). **Use the skill's `.venv/bin/python`** — export + screenshot tools need Playwright + Pillow. If `.venv` is missing: `python3 -m venv .venv && .venv/bin/pip install playwright pillow && .venv/bin/python -m playwright install chromium`.

### Stage 4 — Review + deliver
1. Read the rendered PNGs back and eyeball (YOUR self-check, per the verify rule): headline not clipped, ≤8 logo rows, screenshot legible, highlight on the right phrase, photo subject not covered by text.
2. **🛑 All-slides preview — the user's visual gate.** Build + open the review page so they approve the whole carousel in ONE look:
   ```
   python3 tools/build-preview.py .tmp/out --title "<Carousel title>" --open
   ```
   Wait for approval; fix + re-render + rebuild the preview if anything is flagged.
3. Tell the user where the finals are + a suggested caption/keyword.

## Quality gates (check before delivering)
- Cover headline ≤10 words, exactly ONE `--pop` highlight phrase.
- Logo list ≤8 rows. Every logo is a real file (no broken `<img>`). Flag any fallback-tile logos.
- Screenshot legible at phone size and doesn't misrepresent (no invented metrics presented as real).
- CTA keyword is a REAL keyword wired into the user's DM automation (ManyChat or similar) — ask if unsure; NEVER invent one. Keyword CTAs are Instagram-only; on other platforms use a URL.
- Photo subject's face NOT buried under a text block — see card placement below. Check EVERY photo slide.
- Stickers/doodles ≥40px from every edge, AND check the source PNG is clean (a corrupt sprite shows as a sliver at the edge — inspect the PNG on a contrasting bg, not just its CSS position).

### Card placement over faces (theme-photo) — the recurring trap
On `theme-photo` statement slides the `.card` is CENTRED by default (`top:50%`), so on a portrait photo it lands on the face. Fix with position modifiers (in themes.css):
- `.card.card-top` → card hugs the top (face in the LOWER half)
- `.card.card-bottom` → card hugs the bottom (face in the UPPER half)
- no modifier (centred) → only OK on `[no-face]` photos (food/scenery/object)

Don't eyeball this each time — every photo in `assets/photos/lifestyle/PHOTO-INDEX.md` carries a `[face-upper]` / `[face-lower]` / `[face-centre]` / `[no-face]` tag. Map: `[face-upper]`→`card-bottom`, `[face-lower]`→`card-top`, `[face-centre]`→top or bottom (never centred), `[no-face]`→centred fine. New photos: preview once, add the tag.

## Adding a logo later
```
python3 tools/logo-fetch.py <name> [simpleicons-slug] [hexcolour]
# e.g. python3 tools/logo-fetch.py canva canva 00C4CC
```

## Adding new photos (camera-roll dump → library)
**The recurring trap: naive HEIC→JPG conversion strips the EXIF orientation flag, so portrait shots land SIDEWAYS.** Use the import tool — it reads the ORIGINAL EXIF orientation and rotates each upright automatically:
```
python3 tools/import-photos.py ~/Downloads/IMG_28*.HEIC   # or a folder
```
This converts + auto-rotates into `assets/photos/lifestyle/_staging/` with a `_TODO.md` checklist. Then:
1. **Eyeball each** staged JPG — auto-rotate is ~95%; rare EXIF cases still flip wrong (`sips -r 180 <f> --out <f>` on macOS).
2. **Rename** to `<category>-<desc>.jpg` (the user's own category prefixes).
3. **Move** up into `assets/photos/lifestyle/` (out of `_staging/`).
4. **Add a row** to `PHOTO-INDEX.md` under the right section with the face-position tag.
