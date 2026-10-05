"""Front panel art for the KDP hardcover (case laminate) edition.

The paperback front (cover/front-flag-woodcut.png) is trim + bleed. Handed straight to
build_cover.py --format hardcover it gets stretched over the whole hardcover panel, wrap
included, so the composition drifts right and the author line lands on the board edge.

This writes cover/front-flag-woodcut-hc.png at the hardcover panel size: the carved block
cropped exactly where the wrap builder will lay it, with the paperback front's trim box
(rings and type) set on the board face and feathered in. Then:

  ~/.fal-venv/bin/python ~/book-suite/plugins/imprint/skills/kdp-cover/build_cover.py . \
      --format hardcover --art cover/front-flag-woodcut-hc.png
"""
import re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path.home() / "book-suite/plugins/imprint/skills/kdp-cover"))
from build_cover import fit_cover, HC_WRAP_IN, HC_HINGE_IN, HC_BOARD_OVERHANG_IN, HC_SPINE_BOARD_IN, HC_PAPER_THICKNESS  # noqa: E402

DPI, TRIM_W, TRIM_H, BLEED = 300, 6.0, 9.0, 0.125
pdf = ROOT / "build/dist/a-civilization-worth-inheriting.pdf"
pages = int(re.search(r"Pages:\s+(\d+)", subprocess.check_output(["pdfinfo", str(pdf)], text=True)).group(1))

spine_in = pages * HC_PAPER_THICKNESS["cream"] + HC_SPINE_BOARD_IN
wrap, hinge = round(HC_WRAP_IN * DPI), round(HC_HINGE_IN * DPI)
tw, th = round(TRIM_W * DPI), round(TRIM_H * DPI)
panel_h = round((TRIM_H + HC_BOARD_OVERHANG_IN) * DPI)
spine = round(spine_in * DPI)
W = round((2 * HC_WRAP_IN + 2 * TRIM_W + 2 * HC_HINGE_IN + spine_in) * DPI)
H = round((2 * HC_WRAP_IN + TRIM_H + HC_BOARD_OVERHANG_IN) * DPI)
front_x0 = wrap + tw + hinge + spine + hinge          # as compose_cover() lays it out
art_w, art_h = tw + wrap, H                            # what build_cover expects for --art

# 1. the block, cropped exactly where build_cover will lay wrap_bg
bg = fit_cover(ROOT / "cover/wrap-bg.png", W, H).crop((front_x0, 0, front_x0 + art_w, H))

# 2. the paperback front's trim box, on the board face, centred in the overhang
pb = Image.open(ROOT / "cover/front-flag-woodcut.png").convert("RGB")
b = round(BLEED * DPI)
trim = pb.crop((0, b, tw, b + th))
y0 = wrap + (panel_h - th) // 2
mask = Image.new("L", trim.size, 255)
feather = 60
inner = Image.new("L", (trim.width - 2 * feather, trim.height - 2 * feather), 255)
mask = Image.new("L", trim.size, 0); mask.paste(inner, (feather, feather))
mask = mask.filter(ImageFilter.GaussianBlur(feather / 2))
bg.paste(trim, (0, y0), mask)

out = ROOT / "cover/front-flag-woodcut-hc.png"
bg.save(out, dpi=(DPI, DPI))
print(f"pages {pages} | spine {spine_in:.3f} in | canvas {W}x{H} | front art {bg.size} | board face y {y0}-{y0 + th} | wrote {out.name}")
