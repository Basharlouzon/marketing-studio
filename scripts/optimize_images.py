#!/usr/bin/env python3
"""Build step: make light WebP copies of the showcase PNGs for the landing page.

The PNGs in docs-site/showcase/ stay the source of truth (CI preverifies them).
The landing page loads docs-site/img/<name>-<width>.webp instead, so a first
visit downloads a few hundred KB instead of several MB.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs-site" / "showcase"
OUT = ROOT / "docs-site" / "img"
WIDTHS = (480, 960)

OUT.mkdir(exist_ok=True)
count = 0
for png in sorted(SRC.glob("*.png")):
    with Image.open(png) as im:
        im = im.convert("RGB")
        for w in WIDTHS:
            if w > im.width:
                w = im.width
            h = round(im.height * w / im.width)
            dest = OUT / f"{png.stem}-{w}.webp"
            im.resize((w, h), Image.LANCZOS).save(dest, "WEBP", quality=80, method=6)
            count += 1
print(f"optimize_images: wrote {count} webp files to {OUT.relative_to(ROOT)}")
