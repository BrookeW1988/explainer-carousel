---
name: explainer-carousel
description: Build an explainer carousel (photo cover + bold statement + numbered logo list + framed screenshot card + comment-keyword CTA) in the user's brand, defined in templates/brand.css. Works from a topic OR from a filmed reel/video (transcript-driven companion carousel). Real product logos from a local library, real screenshots via Playwright (AI mockup fallback). Use when the user says "explainer carousel", "logo carousel", "make a carousel with logos/screenshots", "tools/stack carousel", or "turn this reel/video into a carousel".
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
argument-hint: <topic, transcript path, or video file> [--keyword KEYWORD] [--cover photo-name] [--count N]
---

# /explainer-carousel

Builds the **logo + screenshot explainer carousel** style — photo cover, numbered list of real product logos, framed app screenshots, comment-keyword CTA. Renders one 1080×1350 PNG per slide (IG 4:5 portrait).

## Two input modes

1. **Topic mode** — the user gives a topic/angle ("my 5 favourite AI tools"). You plan the content from scratch.
2. **Reel mode** — the user gives a filmed reel/video (a video file, a transcript file, or pasted transcript). The carousel is a COMPANION POST to the reel: it expands the points they actually said on camera into slides, so the reel and the carousel ship as a pair. See "Reel mode" under Stage 1.

## ⚠️ First run = ONBOARDING (do this before any build)

If `templates/brand.css` still contains the starter palette (the header comment says so) or `assets/photos/` is empty, don't build a carousel yet — **run the guided setup below**. A carousel in the starter palette is a demo, not a deliverable. The user can also trigger this any time with "set up the carousel skill" / "/explainer-carousel setup".

Interview the user step by step (use AskUserQuestion where options fit; keep it conversational — one topic at a time, not a form dump). Apply each answer immediately so setup ends with a working, branded system:

1. **Colours.** Ask for their existing brand hexes, or their website/IG handle so you can look at what they already use, or offer to help pick. Map their answers to the 5 roles (`--ink --paper --accent --pop --fill` — explain each in one plain-English line) and write them into `templates/brand.css`.
2. **Fonts.** Ask for the vibe (chunky + loud / clean + premium / soft + handmade / editorial) and any fonts they already use. Suggest 2–3 Google Fonts pairings per vibe, get a pick, then update `brand.css` AND the font-load line in `templates/explainer-carousel.html`.
3. **Identity.** Ask for their brand name (for the two-word lockup) and @handle. Record them in a short `BRAND.md` at the repo root so future builds fill `{{BRAND_WORD_1}}/{{BRAND_WORD_2}}` and `{{HANDLE}}` without asking again. Also ask: do they use comment-keyword DM automation (ManyChat etc.)? If yes, note their real keywords in BRAND.md; if no, CTAs use a link/URL line instead.
4. **Logos.** Ask which 10–20 tools/products they actually talk about, then fetch them: `python3 tools/logo-fetch.py <name> <slug> <hex>` (slugs at simpleicons.org). Report any that fell back to letter tiles.
5. **Doodles/stickers (optional but high-value).** Ask if they want their own hand-drawn-style doodle set. If yes, help them connect an OpenAI API key: check `echo $OPENAI_API_KEY` first; if unset, tell them where to create one (platform.openai.com → API keys) and add `export OPENAI_API_KEY=...` to their shell profile (or the `env` block in `~/.claude/settings.json` for Claude Code). Then ask which style — flat marker doodles / cute 8-bit pixel stickers / realistic cutouts — and generate a starter set of 8–10 shapes IN THEIR PALETTE with `tools/gen-sticker.py`, naming their brand.css hexes in the prompt. Show them the results. If they skip the key, that's fine — slides work without stickers.
6. **Photos.** Ask them to point you at 10–20 photos of themselves/their life (a Downloads dump is fine). Run `tools/import-photos.py`, then walk them through renaming + face-tagging into `assets/photos/lifestyle/PHOTO-INDEX.md` (explain WHY: the tags place text cards off their face automatically, forever).
7. **Environment + test render.** Ensure `.venv` exists (`python3 -m venv .venv && .venv/bin/pip install playwright pillow && .venv/bin/python -m playwright install chromium`), then render `templates/explainer-carousel.html`, Read the PNGs yourself, and show them their palette live. Ask: "does this look like YOUR brand?" Iterate colours/fonts until they say yes.

Steps 4–6 can be deferred ("we can do this later") but 1, 2, 3 and 7 are the minimum before the first real carousel. Point at `MAKE-IT-YOURS.md` for the deeper reasoning behind each step.

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
1. Take the topic/angle OR the reel input. Extract flags: `--keyword`, `--cover <photo-name>`, `--count`.
2. Decide the slide list (which types, in order). Default: Cover → Statement → 1 Logo list → 1 Screenshot card → CTA.
3. Write the copy for each slide (word limits per type above, user's voice).

**Reel mode (input is a video or transcript):**
- **Video file** → get a transcript first. If the `whisper` CLI is installed, use it (`whisper <file> --model base --output_format txt`); otherwise extract audio (`ffmpeg -i <video> -vn audio.mp3`) and ask the user to transcribe, or ask them to paste the transcript. Never invent what was said.
- **The FILMED transcript is the source of truth** — build slides from what they actually said, not from a pre-filming script (people rewrite themselves on camera).
- Derive the slide plan from the transcript: the reel's hook → cover headline territory (reworded, not copied verbatim — the carousel should ADD to the reel, not repeat it); each distinct point/tool mentioned → a list row or statement slide; anything they showed on screen → a screenshot card candidate.
- Use the SAME CTA keyword as the reel's caption so the funnel is consistent across both posts. If no keyword is given, ask — never invent one.
- Skip the interview questions topic mode would need; the transcript already answers them. Still pause at the plan-approval step (Stage 1 step 6).
4. For the **logo list**, map each row to a real logo file in `assets/logos/`. Missing → `tools/logo-fetch.py`.
5. For each **screenshot card**, decide the source:
   - **Real URL** → `tools/capture-screenshot.py <url> .tmp/<name>.png` (Playwright, retina). JS-heavy / Cloudflare-walled apps will time out — use a mockup or ask the user for a real screenshot instead.
   - **User's real screenshot** (best for their private setup) → copy to `assets/screenshots/source/`. To scrub private bits: `tools/edit-image.py <in> <out> "keep everything the same but <change>"`.
   - **No URL + no real shot** → generate a plausible UI mockup (`tools/gen-sticker.py`-style call). Keep mockups plausible — don't invent numbers that misrepresent.
6. **Present the slide plan + copy and wait for approval** before building HTML. Show: each slide's type, headline/copy, which logos, which screenshot source.

### Stage 2 — Build HTML
1. Copy `templates/explainer-carousel.html` to `.tmp/explainer-<slug>.html`.
2. Fill placeholders (`{{BRAND_WORD_1}}/{{BRAND_WORD_2}}` and `{{HANDLE}}` come from `BRAND.md`, written during onboarding). For logo lists, repeat the `.row` block per item. For screenshot cards, set `{{SHOT_IMG}}` to the captured PNG (relative path).
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
