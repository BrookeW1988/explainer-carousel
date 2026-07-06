# Stickers + doodles

Generate your own — see MAKE-IT-YOURS.md §4. Needs OPENAI_API_KEY.

- `doodles/` — flat hand-drawn marker doodles (transparent PNGs, ~70–140px on slide)
- `collage/` — realistic cutout objects from YOUR daily life (collage theme)

```
python3 tools/gen-sticker.py "a flat hand-drawn marker star doodle, single colour" assets/stickers/doodles/star.png
python3 tools/slice-collage-objects.py sheet.png matcha glasses books keys
```
