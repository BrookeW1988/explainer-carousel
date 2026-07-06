#!/usr/bin/env python3
"""
build-preview.py — generate the ALL-SLIDES review page for one or more carousels.

Approve a carousel in one look: every slide side by side in the browser,
numbered, grouped into a section per carousel. Static HTML, no server needed
(absolute file:// img paths), though `python3 -m http.server` works too.

Usage:
    python3 build-preview.py <png_dir> [<png_dir> ...] [--out FILE] [--title TITLE] [--open]

Slide PNGs must follow the export-slides.py convention: <prefix>-01.png, <prefix>-02.png ...
Each distinct <prefix> becomes its own carousel section (so a batch of several
carousels in one dir still groups correctly). Any other PNGs are ignored.

Defaults: --out <first_dir>/preview.html, --title "Carousel review".
--open opens the file in the default browser when done.
"""
import html
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

SLIDE_RE = re.compile(r"^(?P<prefix>.+)-(?P<num>\d{1,3})\.png$", re.IGNORECASE)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  :root {{ --ink:#262b33; --accent:#3d5a80; --pop:#e3a72f; --fill:#98c1d9; --paper:#f5f3ee; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding:32px 40px 80px; background:var(--paper); color:var(--ink);
         font-family:system-ui,"Helvetica Neue",Arial,sans-serif; }}
  h1 {{ font-size:28px; margin:0 0 4px; }}
  .meta {{ color:var(--accent); margin:0 0 28px; font-size:14px; }}
  section {{ margin-bottom:48px; }}
  h2 {{ font-size:20px; margin:0 0 2px; border-left:6px solid var(--pop); padding-left:10px; }}
  .count {{ color:var(--accent); font-size:13px; margin:0 0 14px; padding-left:16px; }}
  .grid {{ display:flex; flex-wrap:wrap; gap:18px; }}
  figure {{ margin:0; width:270px; }}
  .shot {{ position:relative; border:3px solid var(--ink); border-radius:6px; overflow:hidden;
           box-shadow:6px 6px 0 0 var(--ink); background:#fff; }}
  .shot img {{ display:block; width:100%; height:auto; }}
  .n {{ position:absolute; top:8px; left:8px; background:var(--ink); color:var(--paper);
        font-weight:700; font-size:14px; padding:2px 9px; border-radius:999px; }}
  figcaption {{ font-size:12px; color:var(--accent); margin-top:6px; word-break:break-all; }}
</style>
</head>
<body>
<h1>{title}</h1>
<p class="meta">{total} slide{s} · {ncar} carousel{sc} · generated {stamp}</p>
{sections}
</body>
</html>
"""

SECTION = """<section>
<h2>{name}</h2>
<p class="count">{n} slides · {dir}</p>
<div class="grid">
{figs}
</div>
</section>
"""

FIG = """<figure><div class="shot"><span class="n">{num}</span><img src="{src}" alt="{name} slide {num}"></div><figcaption>{file}</figcaption></figure>"""


def _flag(name, default=None):
    if name in sys.argv:
        v = sys.argv[sys.argv.index(name) + 1]
        sys.argv.remove(v); sys.argv.remove(name)
        return v
    return default


def main():
    do_open = "--open" in sys.argv
    if do_open:
        sys.argv.remove("--open")
    out = _flag("--out")
    title = _flag("--title", "Carousel review")
    dirs = [Path(d).resolve() for d in sys.argv[1:]]
    if not dirs:
        print(__doc__); sys.exit(1)

    # Group slides: (dir, prefix) -> [(num, path)]
    groups = defaultdict(list)
    for d in dirs:
        if not d.is_dir():
            print(f"skip (not a dir): {d}"); continue
        for f in sorted(d.iterdir()):
            m = SLIDE_RE.match(f.name)
            if m:
                groups[(d, m["prefix"])].append((int(m["num"]), f))
    if not groups:
        print("No <prefix>-NN.png slides found in the given dirs."); sys.exit(2)

    out = Path(out).resolve() if out else dirs[0] / "preview.html"
    sections, total = [], 0
    for (d, prefix), slides in sorted(groups.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        slides.sort()
        figs = "\n".join(
            FIG.format(num=n, src=f"file://{html.escape(str(p))}",
                       name=html.escape(prefix), file=html.escape(p.name))
            for n, p in slides
        )
        sections.append(SECTION.format(name=html.escape(prefix), n=len(slides),
                                       dir=html.escape(str(d)), figs=figs))
        total += len(slides)

    import datetime
    out.write_text(PAGE.format(
        title=html.escape(title), total=total, s="s" if total != 1 else "",
        ncar=len(groups), sc="s" if len(groups) != 1 else "",
        stamp=datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        sections="\n".join(sections)))
    print(f"ok: {out}  ({total} slides, {len(groups)} carousel(s))")
    if do_open:
        subprocess.run(["open", str(out)])


if __name__ == "__main__":
    main()
