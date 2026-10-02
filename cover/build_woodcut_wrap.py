"""Woodcut edition of the flag cover: one carved-blue block across the whole wrap.

  cover/wrap-bg.png            the coarse block, fitted to the wrap for the current page count
  cover/art-flag-woodcut.png   the front panel cut from it, with the rings printed in position
  cover/front-flag-woodcut.png the same with type (via render_front.py flag-art)

The rings are not left to the image model. They are lifted from the linocut
emblem print and registered to the design: centred on the trimmed front, 36%
down, 2.88 in across. Run again whenever the page count changes (the spine
moves the front panel along the block).
"""
import re, subprocess, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DPI, BLEED, TRIM_W, TRIM_H, PAGE_IN = 300, 0.125, 6.0, 9.0, 0.0025          # cream paper
pdf = ROOT / "build/dist/a-civilization-worth-inheriting.pdf"
pages = int(re.search(r"Pages:\s+(\d+)", subprocess.check_output(["pdfinfo", str(pdf)], text=True)).group(1))
B, TW, TH = round(BLEED * DPI), round(TRIM_W * DPI), round(TRIM_H * DPI)
SPINE = round(pages * PAGE_IN * DPI)
W, H = 2 * B + 2 * TW + SPINE, TH + 2 * B
FRONT_X0 = B + TW + SPINE

block = Image.open(ROOT / "cover/art-blue-block-coarse.png").convert("RGB")
s = max(W / block.width, H / block.height)
block = block.resize((round(block.width * s), round(block.height * s)), Image.LANCZOS)
l, t = (block.width - W) // 2, (block.height - H) // 2
wrap = block.crop((l, t, l + W, t + H))

# Two adjustments to the block as printed, both for reading:
#  1. Its flecks of bare paper are the same cream as the type and break up
#     letters wherever they fall, so they print as a faint lighter-blue scuff.
#  2. The gouge marks are pulled back toward the flat ink colour. At full
#     strength the carved lines compete with 10-point text on the back; at
#     TEXTURE the block still reads as hand-cut at arm's length.
TEXTURE = 0.42                         # 1.0 = the block as carved, 0 = flat blue
SCUFF = (44, 86, 186)
r_ch = wrap.split()[0]
fleck = r_ch.point(lambda v: 0 if v < 38 else round(min(1.0, (v - 38) / 150) * 255))
wrap = Image.composite(Image.new("RGB", wrap.size, SCUFF), wrap, fleck)
flat = Image.new("RGB", wrap.size, tuple(round(c) for c in __import__("PIL.ImageStat", fromlist=["Stat"]).Stat(wrap).mean))
wrap = Image.blend(flat, wrap, TEXTURE)
wrap.save(ROOT / "cover/wrap-bg.png", dpi=(DPI, DPI))

# Front panel = the right-hand end of the block, plus the rings.
front = wrap.crop((FRONT_X0, 0, FRONT_X0 + TW + B, H))
rings = Image.open(ROOT / "cover/art-flag-linocut-registered.png").convert("RGB")     # already in position
cx, cy, half = 900, B + round(TH * 0.36), round(4 * 0.72 * DPI * 0.60)
r, g, _ = rings.split()
cream = Image.merge("RGB", (r, g, r)).convert("L")                # bright only where paper shows
alpha = cream.point(lambda v: 0 if v < 95 else 255 if v > 185 else round((v - 95) / 90 * 255))
window = Image.new("L", rings.size, 0); window.paste(255, (cx - half, cy - half, cx + half, cy + half))
alpha = Image.composite(alpha, Image.new("L", rings.size, 0), window)
front.paste(rings, (0, 0), alpha)
front.save(ROOT / "cover/art-flag-woodcut.png", dpi=(DPI, DPI))
subprocess.run([sys.executable, str(ROOT / "cover/render_front.py"), "flag-art",
                str(ROOT / "cover/front-flag-woodcut.png"), str(ROOT / "cover/art-flag-woodcut.png")], check=True)
print(f"pages {pages} | spine {SPINE / DPI:.3f} in | wrap {W}x{H}px | front panel starts at x={FRONT_X0}")
