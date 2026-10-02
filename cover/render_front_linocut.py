"""Front cover in the deck's linocut style: a picture over a cream title panel.

Same rule as the cards: the picture is drawn (generate_cover_art.py), the
words are set here in EB Garamond. Output is sized for kdp-cover's --art:
(trim width + one bleed) x (trim height + two bleeds) at 300 DPI, so it butts
the spine on the left and bleeds on the other three edges.

Usage: python cover/render_front_linocut.py cover/art-open-door.png cover/front-open-door.png
"""
import sys
from PIL import Image, ImageDraw, ImageFont

DPI = 300
TRIM_W, TRIM_H, BLEED = 6.0, 9.0, 0.125
W, H, B = round((TRIM_W + BLEED) * DPI), round((TRIM_H + 2 * BLEED) * DPI), round(BLEED * DPI)
CX = TRIM_W * DPI / 2                        # centre of the trimmed front, not of the file
ART_H = B + round(5.62 * DPI)                # picture runs off the top and the outer edge
CREAM, INK, BLUE, OCHRE = (243, 238, 227), (22, 28, 45), (2, 60, 167), (168, 116, 15)
F = "/Users/anthony/Library/Fonts/EBGaramond-"
font = lambda style, px: ImageFont.truetype(f"{F}{style}.otf", px)

art_path, out = sys.argv[1], sys.argv[2]
img = Image.new("RGB", (W, H), CREAM)
art = Image.open(art_path).convert("RGB")
scale = max(W / art.width, ART_H / art.height)
art = art.resize((round(art.width * scale), round(art.height * scale)), Image.LANCZOS)
left, top = (art.width - W) // 2, (art.height - ART_H) // 2
img.paste(art.crop((left, top, left + W, top + ART_H)), (0, 0))
d = ImageDraw.Draw(img)
d.rectangle([0, ART_H, W, ART_H + 8], fill=INK)
d.rectangle([0, ART_H + 8, W, ART_H + 26], fill=BLUE)

def centred(text, f, y, fill, tracking=0):
    if tracking:
        ws = [f.getlength(c) for c in text]; x = CX - (sum(ws) + tracking * (len(text) - 1)) / 2
        for c, w in zip(text, ws):
            d.text((x, y), c, font=f, fill=fill); x += w + tracking
        return
    d.text((CX - f.getlength(text) / 2, y), text, font=f, fill=fill)

def emblem(cx, cy, r, colour):
    """The seven rings of the Earth flag, drawn as vectors. r = ring radius."""
    from math import cos, sin, pi
    ss, size = 4, int(r * 4.6)
    big = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0)); e = ImageDraw.Draw(big); c = size * ss / 2
    for a in [None] + [k * pi / 3 for k in range(6)]:
        x, yy = (c, c) if a is None else (c + r * ss * cos(a), c + r * ss * sin(a))
        e.ellipse([x - r * ss, yy - r * ss, x + r * ss, yy + r * ss], outline=colour + (255,), width=round(0.11 * r * ss))
    small = big.resize((size, size), Image.LANCZOS)
    img.paste(small, (int(cx - size / 2), int(cy - size / 2)), small)

y = ART_H + 26 + 70
tf = font("Regular", 154)
for line in ("A Civilization", "Worth Inheriting"):
    centred(line, tf, y, INK); y += round(154 * 1.05)
R = 37                                       # emblem spans 4R = 0.49 in
y += 46 + 2 * R
emblem(CX, y, R, BLUE); y += 2 * R + 34
sf = font("Italic", 60)
centred("A Pattern Language for the Next Thousand Years", sf, y, INK)
centred("ANTHONY DAVID ADAMS", font("Medium", 48), B + TRIM_H * DPI - round(0.58 * DPI), INK, tracking=13)
img.save(out, dpi=(DPI, DPI)); print(out, img.size)
