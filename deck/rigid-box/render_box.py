"""Print file for the MakePlayingCards rigid box (lid + base) that holds the 130-card tarot deck.

Geometry is read from MPC's own template (template.pdf, 1144.35 x 736.72 pt, lid die on the
left, base die on the right). We paint our own artwork onto a page of exactly that size and
hand MPC a PDF with the template layer absent, as their steps ask.

  lid cover   the woodcut front cover of the book, portrait, top toward the top of the page
  lid walls   the carved-blue block at the same TEXTURE as the book's wrap, cream type
  base        the same blue; the bottom panel carries the deck's "how to use" card and the coach QR

Outputs (deck/rigid-box/): box.pdf (upload this), box.png, proof-over-template.png (alignment check).
Run:  ~/.fal-venv/bin/python deck/rigid-box/render_box.py
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageStat
import pymupdf

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
sys.argv = [sys.argv[0]]
import render_cards as rc                      # noqa: E402  fonts, emblem, tracked type
import render_extras as rx                     # noqa: E402  the title card back (how to use + QR)
from palette import CREAM, BLUE                # noqa: E402

DPI = 300
S = DPI / 72
PAGE_PT = (1144.35, 736.718)
PAGE = (round(PAGE_PT[0] * S), round(PAGE_PT[1] * S))
px = lambda v: round(v * S)
R = lambda x0, y0, x1, y1: (px(x0), px(y0), px(x1), px(y1))

# --- from template.pdf (points). Red = die/fold lines, blue = safe area, cyan fill = bleed.
LID_COVER = (163.0, 184.2, 387.2, 552.5)       # 79.1 x 129.9 mm
LID_COVER_BLEED = (161.6, 181.4, 388.6, 555.3)  # run the art under the fold lines
LID_WALL_TOP = (163.0, 73.7, 387.2, 184.2)      # safe y >= 73.7; turn-in beyond 70.0
LID_WALL_BOTTOM = (163.0, 552.5, 387.2, 663.0)
LID_WALL_LEFT = (52.4, 182.8, 163.0, 553.9)
LID_WALL_RIGHT = (387.2, 182.8, 497.8, 553.9)
LID_BLEED_RECTS = [(154.5, 21.8, 395.7, 714.9), (0.0, 140.3, 550.2, 596.4)]
BASE_COVER = (741.5, 190.8, 953.0, 546.0)
BASE_COVER_BLEED = (740.1, 187.9, 954.4, 548.8)
BASE_BLEED_RECTS = [(733.0, 0.0, 961.5, 736.7), (550.2, 146.8, 1144.3, 589.9)]

TEXTURE, SCUFF = 0.42, (44, 86, 186)           # as cover/build_woodcut_wrap.py


def carved_blue(size):
    block = Image.open(BOOK / "cover/art-blue-block-coarse.png").convert("RGB")
    s = max(size[0] / block.width, size[1] / block.height)
    block = block.resize((round(block.width * s), round(block.height * s)), Image.LANCZOS)
    l, t = (block.width - size[0]) // 2, (block.height - size[1]) // 2
    img = block.crop((l, t, l + size[0], t + size[1]))
    fleck = img.split()[0].point(lambda v: 0 if v < 38 else round(min(1.0, (v - 38) / 150) * 255))
    img = Image.composite(Image.new("RGB", img.size, SCUFF), img, fleck)
    flat = Image.new("RGB", img.size, tuple(round(c) for c in ImageStat.Stat(img).mean))
    return Image.blend(flat, img, TEXTURE)


def cover_fit(img, size):
    s = max(size[0] / img.width, size[1] / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    l, t = (img.width - size[0]) // 2, (img.height - size[1]) // 2
    return img.crop((l, t, l + size[0], t + size[1]))


def tracked_image(text, f, fill, tracking):
    """Tracked small caps rendered on a transparent strip so it can be rotated onto a wall."""
    widths = [f.getlength(ch) for ch in text]
    w = round(sum(widths) + tracking * (len(text) - 1)) + 4
    h = round(f.size * 1.4)
    strip = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(strip)
    x = 2
    for ch, wd in zip(text, widths):
        d.text((x, 0), ch, font=f, fill=fill + (255,)); x += wd + tracking
    return strip


def paste_centre(canvas, strip, rect_pt, rotate=0):
    strip = strip.rotate(rotate, expand=True, resample=Image.BICUBIC)
    x0, y0, x1, y1 = R(*rect_pt)
    canvas.paste(strip, (round((x0 + x1) / 2 - strip.width / 2), round((y0 + y1) / 2 - strip.height / 2)), strip)


def emblem_on(canvas, rect_pt, r):
    x0, y0, x1, y1 = R(*rect_pt)
    rc.emblem(canvas, (x0 + x1) // 2, (y0 + y1) // 2, r, CREAM)


def build():
    canvas = Image.new("RGB", PAGE, (255, 255, 255))
    blue = carved_blue(PAGE)
    mask = Image.new("L", PAGE, 0); md = ImageDraw.Draw(mask)
    for rect in LID_BLEED_RECTS + BASE_BLEED_RECTS:
        md.rectangle(R(*rect), fill=255)
    canvas.paste(blue, (0, 0), mask)

    # Lid cover: the book's woodcut front, portrait, top toward the top of the page.
    art = Image.open(BOOK / "cover/front-flag-woodcut.png").convert("RGB")
    x0, y0, x1, y1 = R(*LID_COVER_BLEED)
    canvas.paste(cover_fit(art, (x1 - x0, y1 - y0)), (x0, y0))

    # Lid walls. Every wall's top edge is its fold to the cover, so type "up" points at the cover:
    # bottom wall upright, top wall upside down, left wall rotated so up = +x, right wall up = -x.
    lab = rc.font("Medium", rc.PT(7.2)); small = rc.font("Medium", rc.PT(5.4))
    paste_centre(canvas, tracked_image("THE PATTERN DECK", lab, CREAM, 9), LID_WALL_BOTTOM, 0)
    paste_centre(canvas, tracked_image("108 PATTERNS  ·  EARTHPILOT.ORG", small, CREAM, 6), LID_WALL_TOP, 180)
    paste_centre(canvas, tracked_image("A CIVILIZATION WORTH INHERITING", lab, CREAM, 9), LID_WALL_LEFT, -90)
    paste_centre(canvas, tracked_image("A PATTERN LANGUAGE FOR THE NEXT THOUSAND YEARS", small, CREAM, 6), LID_WALL_RIGHT, 90)

    # Base: blue walls (the strip that shows beneath the lid) and the title card's back underneath.
    back = rx.title_back()
    x0, y0, x1, y1 = R(*BASE_COVER_BLEED)
    canvas.paste(cover_fit(back, (x1 - x0, y1 - y0)), (x0, y0))
    return canvas


def write_pdf(img, path):
    doc = pymupdf.open(); page = doc.new_page(width=PAGE_PT[0], height=PAGE_PT[1])
    tmp = HERE / "box.jpg"; img.save(tmp, quality=95, dpi=(DPI, DPI), subsampling=0)
    page.insert_image(page.rect, filename=str(tmp))
    doc.save(path, deflate=True); doc.close()


if __name__ == "__main__":
    img = build()
    img.save(HERE / "box.png", dpi=(DPI, DPI))
    write_pdf(img, HERE / "box.pdf")
    tpl = pymupdf.open(HERE / "template.pdf")[0].get_pixmap(dpi=DPI, alpha=False)
    tpl = Image.frombytes("RGB", (tpl.width, tpl.height), tpl.samples).resize(PAGE)
    Image.blend(img, tpl, 0.45).save(HERE / "proof-over-template.png")
    print("wrote box.pdf / box.png / proof-over-template.png", PAGE)
