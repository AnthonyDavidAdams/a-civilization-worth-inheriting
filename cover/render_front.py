"""Render the front cover panel for A Civilization Worth Inheriting.

Purely typographic + geometric, no generated art: the emblem is the seven
interlocking rings of the International Flag of Planet Earth (the EarthPilot
mark), drawn as vectors at 300 DPI. Output is sized for kdp-cover's --art
input: (trim width + one bleed) x (trim height + two bleeds), so the panel
bleeds on the outer three edges and butts the spine on the left.

Usage: python render_front.py flag|paper out.png
"""
import sys
from PIL import Image, ImageDraw, ImageFont
from math import cos, sin, pi

DPI = 300
TRIM_W, TRIM_H, BLEED = 6.0, 9.0, 0.125
W = round((TRIM_W + BLEED) * DPI)          # 1838
H = round((TRIM_H + 2 * BLEED) * DPI)      # 2775
B = round(BLEED * DPI)                     # 38
SS = 3                                     # supersample for smooth rings

FLAG_BLUE = (2, 60, 167)                   # sampled from the EarthPilot mark
CREAM = (243, 238, 227)
INK = (22, 28, 45)
WHITE = (255, 255, 255)

FONTS = "/Users/anthony/Library/Fonts/"
def font(style, px):
    return ImageFont.truetype(FONTS + f"EBGaramond-{style}.otf", px)

variant, out = sys.argv[1], sys.argv[2]

if variant == "emblem":
    # Standalone rings on a transparent field, for the spine (and anywhere else
    # a raster emblem is needed). Colour from argv[3] as hex, default white.
    size = 1200
    colour = tuple(int(sys.argv[3].lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) if len(sys.argv) > 3 else WHITE
    big = Image.new("RGBA", (size * SS, size * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    rr = size / 4.6; c = size / 2
    for a in [None] + [k * pi / 3 for k in range(6)]:
        x, y = (c, c) if a is None else (c + rr * cos(a), c + rr * sin(a))
        d.ellipse([(x - rr) * SS, (y - rr) * SS, (x + rr) * SS, (y + rr) * SS],
                  outline=colour + (255,), width=round(0.11 * rr * SS))
    big.resize((size, size), Image.Resampling.LANCZOS).save(out)
    print(out, "emblem"); sys.exit(0)

if variant == "flag":
    field, ring, text, rule = FLAG_BLUE, WHITE, WHITE, (255, 255, 255, 170)
else:
    field, ring, text, rule = CREAM, FLAG_BLUE, INK, (22, 28, 45, 140)

img = Image.new("RGB", (W, H), field)

# --- Seven rings (flower-of-life arrangement: one centre, six at distance r) ---
cx, cy = TRIM_W * DPI / 2, B + TRIM_H * DPI * 0.36
r = 0.72 * DPI            # ring radius; group spans 4r = 2.9in of the 6in width
stroke = 0.11 * r         # stroke ratio measured off the EarthPilot mark
big = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
d = ImageDraw.Draw(big)
centres = [(cx, cy)] + [(cx + r * cos(a), cy + r * sin(a))
                        for a in [k * pi / 3 for k in range(6)]]
for (x, y) in centres:
    d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS],
              outline=ring + (255,), width=round(stroke * SS))
rings = big.resize((W, H), Image.Resampling.LANCZOS)
img.paste(rings, (0, 0), rings)

draw = ImageDraw.Draw(img, "RGBA")
def centred(txt, f, y, fill, tracking=0):
    if tracking:
        widths = [f.getlength(c) for c in txt]
        total = sum(widths) + tracking * (len(txt) - 1)
        x = cx - total / 2
        for c, w in zip(txt, widths):
            draw.text((x, y), c, font=f, fill=fill)
            x += w + tracking
        return total
    w = f.getlength(txt)
    draw.text((cx - w / 2, y), txt, font=f, fill=fill)
    return w

# --- Title ---
tf = font("Regular", 168)
y = B + TRIM_H * DPI * 0.575
for line in ["A Civilization", "Worth Inheriting"]:
    centred(line, tf, y, text)
    y += 168 * 1.08

# --- Rule + subtitle ---
y += 70
draw.line([(cx - 0.55 * DPI, y), (cx + 0.55 * DPI, y)], fill=rule, width=3)
y += 62
sf = font("Italic", 64)
for line in ["A Pattern Language", "for the Next Thousand Years"]:
    centred(line, sf, y, text)
    y += 64 * 1.25

# --- Author, letterspaced caps at the foot ---
af = font("Medium", 52)
centred("ANTHONY DAVID ADAMS", af, B + TRIM_H * DPI - 0.62 * DPI, text, tracking=14)

img.save(out, dpi=(DPI, DPI))
print(out, img.size)
