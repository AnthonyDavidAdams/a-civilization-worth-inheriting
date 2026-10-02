"""Render print-ready card fronts and backs for the pattern deck.

Card: tarot size, 2.75 x 4.75 in trim, 0.125 in bleed on every edge, so each
file is 3.0 x 5.0 in = 900 x 1500 px at 300 DPI. Live text stays inside a
safe area 0.125 in in from the trim. Corners are die-cut at 0.125 in radius.

  print/NNN-front.png, NNN-back.png   full bleed, no marks: what the printer gets
  proof/NNN-front.png, NNN-back.png   same, with trim (red) and safe (green) guides
  print/sample-cards.pdf              fronts and backs alternating, 3 x 5 in pages

Art is drawn by generate_art.py; every letter here is real EB Garamond.
Usage: python deck/render_cards.py [n n n ...]   (default: every card with art)
"""
import json, sys
from math import cos, sin, pi
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DPI = 300
IN = lambda x: round(x * DPI)
# Verified against the printers' own templates on 2026-09-30 (see DESIGN.md):
# 900 x 1500 px is the exact upload size at The Game Crafter, PrintNinja and
# DriveThruCards and within 3 px of MakePlayingCards'. SAFE is 0.20 in, not
# 0.125: Shuffled Ink's template wants 0.1875 in and PrintNinja's tarot page
# 5 mm, and one master should satisfy all five.
TRIM_W, TRIM_H, BLEED, SAFE, RADIUS = 2.75, 4.75, 0.125, 0.20, 0.125
RULE_INSET = 0.25                                           # any rule stays this far inside the trim
MPC_RADIUS = 0.235                                          # MakePlayingCards cuts a rounder corner (~6 mm)
W, H = IN(TRIM_W + 2 * BLEED), IN(TRIM_H + 2 * BLEED)      # 900 x 1500
B = IN(BLEED)
SX0, SY0, SX1, SY1 = B + IN(SAFE), B + IN(SAFE), W - B - IN(SAFE), H - B - IN(SAFE)
CX = W // 2
PT = lambda pt: round(pt * DPI / 72)                         # type size in points -> px

sys.path.insert(0, str(Path(__file__).resolve().parent))
from palette import CREAM, INK, BLUE, PART_COLOURS, rgb      # noqa: E402

# Each part (suit) has its own third colour: a band under the picture that
# shows when cards are fanned, the rules and labels, and an ink in the picture.
# `--two-ink` renders the earlier blue-only look into print-two-ink/.
ACCENT = "--two-ink" not in sys.argv
def accent(c):
    return rgb(PART_COLOURS[c["part"]][1]) if ACCENT else BLUE
ART_H = IN(3.22)                                             # art runs off top, left, right
FONTS = "/Users/anthony/Library/Fonts/EBGaramond-"
font = lambda style, px: ImageFont.truetype(f"{FONTS}{style}.otf", px)

ROOT = Path(__file__).resolve().parent
cards = {c["n"]: c for c in json.loads((ROOT / "cards.json").read_text())}


def wrap(text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if f.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur); cur = word
    return lines + [cur] if cur else lines


def tracked(draw, text, f, cx, y, fill, tracking):
    widths = [f.getlength(ch) for ch in text]
    x = cx - (sum(widths) + tracking * (len(text) - 1)) / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=f, fill=fill); x += w + tracking


def centred_lines(draw, lines, f, y, fill, leading):
    for ln in lines:
        draw.text((CX - f.getlength(ln) / 2, y), ln, font=f, fill=fill); y += leading
    return y


def left_lines(draw, lines, f, x, y, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill); y += leading
    return y


def emblem(img, cx, cy, r, colour):
    """Seven interlocking rings; r is the ring radius, group spans 4r."""
    ss = 4; size = int(r * 4.6)
    big = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(big); c = size * ss / 2
    for a in [None] + [k * pi / 3 for k in range(6)]:
        x, y = (c, c) if a is None else (c + r * ss * cos(a), c + r * ss * sin(a))
        d.ellipse([x - r * ss, y - r * ss, x + r * ss, y + r * ss], outline=colour + (255,), width=max(2, round(0.11 * r * ss)))
    small = big.resize((size, size), Image.LANCZOS)
    img.paste(small, (int(cx - size / 2), int(cy - size / 2)), small)


def part_label(c):
    return f"PART {c['part_roman']}  ·  {c['part_name'].upper()}"


def front(c, art_path):
    img = Image.new("RGB", (W, H), CREAM)
    art = Image.open(art_path).convert("RGB")
    scale = W / art.width
    art = art.resize((W, round(art.height * scale)), Image.LANCZOS)
    top = max(0, (art.height - ART_H) // 2)
    img.paste(art.crop((0, top, W, top + ART_H)), (0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, ART_H, W, ART_H + 5], fill=INK)             # a printed edge under the picture
    if ACCENT:
        d.rectangle([0, ART_H + 5, W, ART_H + 19], fill=accent(c))   # the suit band

    num_f, lab_f = font("Regular", PT(25)), font("Medium", PT(5.4))
    size = 15.5
    while True:                                                 # title shrinks only if it must
        title_f = font("Italic", PT(size)); lines = wrap(c["title"], title_f, SX1 - SX0)
        if len(lines) <= 2 or size <= 12: break
        size -= 0.5
    lead = round(PT(size) * 1.12)
    block = PT(25) + 26 + lead * len(lines) + 34 + 3 + 30 + PT(5.4)
    y = ART_H + 5 + ((SY1 - (ART_H + 5)) - block) // 2 + 4
    num = str(c["n"])
    d.text((CX - num_f.getlength(num) / 2, y - PT(25) * 0.22), num, font=num_f, fill=INK); y += PT(25) + 26 - round(PT(25) * 0.22)
    y = centred_lines(d, lines, title_f, y, INK, lead) + 30
    d.line([(CX - IN(0.22), y), (CX + IN(0.22), y)], fill=accent(c), width=3); y += 26
    tracked(d, part_label(c), lab_f, CX, y, accent(c), 3.2)
    return img


def back(c):
    img = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(img)
    width = SX1 - SX0
    emblem(img, CX, SY0 + 58, 25, BLUE)
    y = SY0 + 140
    head_f = font("Italic", PT(12.5)); head = wrap(f"{c['n']}  {c['title']}", head_f, width)
    y = centred_lines(d, head, head_f, y, INK, round(PT(12.5) * 1.15)) + 12
    tracked(d, part_label(c), font("Medium", PT(5)), CX, y, accent(c), 3.0); y += PT(5) + 34
    d.line([(CX - IN(0.22), y), (CX + IN(0.22), y)], fill=accent(c), width=3); y += 38

    conn = "  ·  ".join(f"{n} {cards[n]['title']}" for n in c["connected"])
    scale = 1.0
    while True:                                                 # one scale for the whole back
        sum_f, body_f, lab_f, con_f = (font("Italic", PT(11.2 * scale)), font("Regular", PT(8.9 * scale)),
                                       font("Medium", PT(5.2)), font("Regular", PT(7.1 * scale)))
        s_lines = wrap(c["summary"], sum_f, width - 40)
        t_lines = wrap(c["statement"], body_f, width)
        f_lines = wrap(c["first_move"], body_f, width)
        c_lines = wrap(conn, con_f, width)
        s_lead, b_lead, c_lead = round(PT(11.2 * scale) * 1.22), round(PT(8.9 * scale) * 1.3), round(PT(7.1 * scale) * 1.3)
        foot = PT(5.2) + 16 + c_lead * len(c_lines)
        need = s_lead * len(s_lines) + 40 + b_lead * len(t_lines) + 40 + PT(5.2) + 18 + b_lead * len(f_lines) + 44 + foot
        if y + need <= SY1 or scale <= 0.78: break
        scale -= 0.03
    y = centred_lines(d, s_lines, sum_f, y, INK, s_lead) + 40
    y = left_lines(d, t_lines, body_f, SX0, y, INK, b_lead) + 40
    tracked(d, "A FIRST MOVE", lab_f, SX0 + font("Medium", PT(5.2)).getlength("A FIRST MOVE") / 2 + 3.0 * 5.5, y, accent(c), 3.0); y += PT(5.2) + 18
    left_lines(d, f_lines, body_f, SX0, y, INK, b_lead)
    if not c["connected"]:
        return img, scale
    fy = SY1 - foot                                             # connections sit on the foot of the safe area
    d.line([(B + IN(RULE_INSET), fy - 22), (W - B - IN(RULE_INSET), fy - 22)], fill=(200, 192, 176), width=2)
    tracked(d, "CONNECTED PATTERNS", lab_f, SX0 + font("Medium", PT(5.2)).getlength("CONNECTED PATTERNS") / 2 + 3.0 * 8.5, fy, accent(c), 3.0)
    left_lines(d, c_lines, con_f, SX0, fy + PT(5.2) + 16, INK, c_lead)
    return img, scale


def with_guides(img):
    g = img.copy(); d = ImageDraw.Draw(g)
    d.rounded_rectangle([B, B, W - B, H - B], radius=IN(RADIUS), outline=(220, 30, 30), width=2)   # trim
    d.rounded_rectangle([B, B, W - B, H - B], radius=IN(MPC_RADIUS), outline=(230, 140, 30), width=2)   # MPC's rounder cut
    d.rectangle([SX0, SY0, SX1, SY1], outline=(30, 160, 60), width=2)                              # safe
    return g


if __name__ == "__main__":
    have = sorted({int(p.name[:3]) for p in (ROOT / "art").glob("*-linocut*.png")})
    nums = [int(x) for x in sys.argv[1:] if x.isdigit()] or have
    OUT = "print" if ACCENT else "print-two-ink"
    PROOF = "proof" if ACCENT else "proof-two-ink"
    (ROOT / OUT).mkdir(exist_ok=True); (ROOT / PROOF).mkdir(exist_ok=True)
    pages = []
    for n in nums:
        c = cards[n]
        two, three = ROOT / "art" / f"{n:03d}-linocut.png", ROOT / "art" / f"{n:03d}-linocut3.png"
        art = three if (three.exists() and (ACCENT or not two.exists())) else two
        f = front(c, art); b, scale = back(c)
        for side, im in (("front", f), ("back", b)):
            im.save(ROOT / OUT / f"{n:03d}-{side}.png", dpi=(DPI, DPI))
            with_guides(im).save(ROOT / PROOF / f"{n:03d}-{side}.png", dpi=(DPI, DPI))
            pages.append(im)
        print(f"{n:>3} {c['title']:<40} back text scale {scale:.2f}")
    if len(nums) < 108:                       # a partial run; the whole deck's PDF is built by make_deck.py
        pages[0].save(ROOT / OUT / "sample-cards.pdf", "PDF", resolution=DPI, save_all=True, append_images=pages[1:])
    print(f"{len(nums)} cards -> {W}x{H}px at {DPI} DPI ({TRIM_W}x{TRIM_H} in trim + {BLEED} in bleed)")
