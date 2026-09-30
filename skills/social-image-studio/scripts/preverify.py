#!/usr/bin/env python3
"""preverify.py — cheap pre-QA before spending a visual-judge wave.
Usage: python3 preverify.py <image-folder> [more-folders...]
Checks per PNG: exact dimensions, transparent-corner alpha (broken-asset tell),
and contiguous same-color dead bands (top band under any header, bottom band
above any footer) larger than the thresholds below.
"""
import sys, os
from PIL import Image

TOP_BAND_MAX = 260    # px of empty space allowed between y=160 and first content
BOTTOM_BAND_MAX = 300 # px of empty space allowed above y=1620 (CTA zone)
DIFF = 55             # per-channel-sum threshold vs background sample

def scan(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    issues = []
    # transparency tell (re-open as RGBA on a copy of the file bytes)
    rgba = Image.open(path).convert("RGBA")
    corners = [rgba.getpixel(p)[3] for p in [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]]
    if any(a < 250 for a in corners):  # <250 = genuinely transparent (255±1 is gradient dither)
        issues.append("transparent corners (not a flattened render — broken-asset tell)")
    bg = im.getpixel((10, h // 2))
    # top band: scan down from y=170 at three x positions
    first = None
    for y in range(170, h // 2, 2):
        for x in range(100, w - 100, 24):
            px = im.getpixel((x, y))
            if abs(px[0]-bg[0]) + abs(px[1]-bg[1]) + abs(px[2]-bg[2]) > DIFF:
                first = y
                break
        if first:
            break
    if first and first - 160 > TOP_BAND_MAX:
        issues.append(f"TOP dead band {first-160}px (content starts y={first})")
    # bottom band: scan up from y=int(h*0.84)
    last = None
    for y in range(int(h * 0.84), h // 2, -2):
        for x in range(100, w - 100, 24):
            px = im.getpixel((x, y))
            if abs(px[0]-bg[0]) + abs(px[1]-bg[1]) + abs(px[2]-bg[2]) > DIFF:
                last = y
                break
        if last:
            break
    if last and (int(h * 0.84) - last) > BOTTOM_BAND_MAX:
        issues.append(f"BOTTOM dead band {int(h*0.84)-last}px (content ends y={last})")
    return f"{os.path.basename(path)} {w}x{h}: " + ("; ".join(issues) if issues else "ok")

if __name__ == "__main__":
    folders = sys.argv[1:]
    for folder in folders:
        for f in sorted(os.listdir(folder)):
            if f.lower().endswith(".png"):
                try:
                    print(scan(os.path.join(folder, f)))
                except Exception as e:
                    print(f"{f}: ERROR {e}")
