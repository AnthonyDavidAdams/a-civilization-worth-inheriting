"""Showcase sheet: each rendered card cut to its die line, front beside back."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
B = R = 38
nums = sorted(int(p.name[:3]) for p in (ROOT / "print").glob("*-front.png"))

def trimmed(path, s=0.5):
    im = Image.open(path).convert("RGB").crop((B, B, 900 - B, 1500 - B))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=R, fill=255)
    size = (round(im.width * s), round(im.height * s))
    return im.resize(size, Image.LANCZOS), mask.resize(size, Image.LANCZOS)

cw, ch = trimmed(ROOT / "print" / f"{nums[0]:03d}-front.png")[0].size
gap, pad, cols = 16, 44, 3
pw = 2 * cw + gap
rows = (len(nums) + cols - 1) // cols
sheet = Image.new("RGB", (cols * pw + (cols + 1) * pad, rows * ch + (rows + 1) * pad), (58, 60, 66))
for i, n in enumerate(nums):
    x, y = pad + (i % cols) * (pw + pad), pad + (i // cols) * (ch + pad)
    for j, side in enumerate(("front", "back")):
        im, m = trimmed(ROOT / "print" / f"{n:03d}-{side}.png")
        sheet.paste(im, (x + j * (cw + gap), y), m)
sheet.save(ROOT / "sample-cards.png")
print("sample-cards.png", sheet.size)
