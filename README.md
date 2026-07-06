# Explainer Carousel Skill

A Claude Code skill that builds Instagram-style explainer carousels — the photo cover + bold statement + numbered list of real product logos + framed screenshot + comment-keyword CTA format you see all over creator feeds. Claude writes the copy, builds the HTML, and renders one 1080×1350 PNG per slide, ready to post.

Give it a topic, or give it a **reel you just filmed** — hand over the video or its transcript and it builds a companion carousel from the points you actually said on camera, with the same CTA keyword, so the reel and carousel ship as a pair.

Built by [Brooke Wright](https://wrightmode.com) (Wright Mode) for her own content system, then open-sourced as the *system* — templates, themes, tools, and workflow.

**What's deliberately NOT in here: my brand.** No fonts, no palette, no photos, no sticker packs. The templates ship with a plain starter palette that works out of the box but looks like nobody. Before you post anything from this repo, read [MAKE-IT-YOURS.md](MAKE-IT-YOURS.md) and build your own brand kit and asset libraries. If you skip that step your carousels will look like every other person who cloned this repo — and the entire reason this format works is that it looks unmistakably like *one person's* feed.

## What you get

- **`SKILL.md`** — the skill itself. Drop the repo in `~/.claude/skills/` and Claude Code picks it up.
- **5 slide types** — cover, statement, logo list, screenshot card, CTA. A carousel mixes them (typically 5–8 slides).
- **8 themes** — scrappy, clean, scrapbook, y2k (+ messy modifier), editorial, brand-editorial, photo, zine, plus a scrapbook-collage format — so your feed doesn't look samey post after post.
- **`templates/brand.css`** — ONE file holding every colour and font. Edit it and all themes restyle themselves.
- **Python tools** — render slides to PNG (Playwright), capture real website screenshots, fetch real product logos (Simple Icons), generate transparent stickers/doodles (OpenAI image API), slice cutout-object sprite sheets, import and auto-rotate camera-roll photos, build a review page.

## Quick start

```bash
# 1. Clone into your Claude Code skills folder
git clone https://github.com/BrookeW1988/explainer-carousel ~/.claude/skills/explainer-carousel

# 2. Set up the render environment (Playwright + Pillow)
cd ~/.claude/skills/explainer-carousel
python3 -m venv .venv
.venv/bin/pip install playwright pillow
.venv/bin/python -m playwright install chromium

# 3. In Claude Code, run the guided setup — the skill interviews you:
#    your colours, fonts, handle, the tools you talk about, your photos,
#    and (optional) connecting an OpenAI key to generate your own
#    doodle/sticker set in YOUR palette:
#    /explainer-carousel setup

# 4. Then build:
#    /explainer-carousel my 5 favourite AI tools --keyword TOOLS
#    — or from a reel you just filmed:
#    /explainer-carousel ~/Downloads/reel-draft.mp4 --keyword TOOLS
```

The first run refuses to ship the starter palette — setup walks you through making it yours (the manual version of the same steps is in [MAKE-IT-YOURS.md](MAKE-IT-YOURS.md)).

Optional: set `OPENAI_API_KEY` in your environment if you want the sticker/doodle generation and image-edit tools.

## How a build works

1. **Plan** — Claude turns your topic into a slide list (cover → statement → logo list → screenshot card → CTA) and writes the copy.
2. **Build** — it clones `templates/explainer-carousel.html`, picks a theme, and fills the placeholders with your logos, photos and screenshots.
3. **Render** — `tools/export-slides.py` screenshots each slide node into a 1080×1350 PNG (2× retina).
4. **Review** — `tools/build-preview.py` opens every slide in one browser page so you approve the whole carousel in one look.

## Credit

The five-slide structure is modelled on formats popularised by creator-education accounts on Instagram. The point of this repo is not to copy anyone's *look* — theirs or mine — it's the reusable machinery for building your own.

MIT licensed. Do what you like with the code; the aesthetic you build on top of it is yours.
