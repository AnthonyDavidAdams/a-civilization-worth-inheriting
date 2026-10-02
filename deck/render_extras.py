"""The thirteen cards that carry no picture: a title card and one card per part.

  print/T00-front|back.png   title card: the flag emblem; how to use the deck (the book's own words) and the coach QR
  print/PNN-front|back.png   part card: the part in its accent colour; the nine patterns it holds

Same file spec as the pattern cards (render_cards.py).
"""
import io, re, sys
from pathlib import Path
from PIL import Image, ImageDraw
import segno

sys.argv = [a for a in sys.argv if a != "--two-ink"]
import render_cards as rc
from render_cards import (W, H, B, SX0, SY0, SX1, SY1, CX, DPI, PT, IN, ROOT, CREAM, INK, BLUE,
                          font, wrap, tracked, centred_lines, left_lines, emblem, cards, with_guides, RULE_INSET)
from palette import PART_COLOURS, rgb
from i18n import pick, part_cn
L = pick(sys.argv)

BOOK = Path(__file__).resolve().parent.parent
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
import yaml
cfg = yaml.safe_load((BOOK / L["book_yaml"]).read_text())
parts = [{"n": i + 1, "roman": ROMAN[i], "name": re.sub(r"^Part [IVX]+ — ", "", p["title"]), "epigraph": p["epigraph"],
          "cards": [c for c in cards.values() if c["part"] == i + 1]} for i, p in enumerate(cfg["parts"])]
WIDTH = SX1 - SX0


def part_front(p):
    acc = rgb(PART_COLOURS[p["n"]][1])
    img = Image.new("RGB", (W, H), acc); d = ImageDraw.Draw(img)
    title_f, epi_f, lab_f = font("Regular", PT(21)), font("Italic", PT(10.2)), font("Medium", PT(6))
    t_lines = wrap(p["name"], title_f, WIDTH); e_lines = wrap(p["epigraph"], epi_f, WIDTH - 40)
    t_lead, e_lead = round(PT(21) * 1.12), round(PT(10.2) * 1.32)
    block = 150 + 70 + PT(6) + 44 + t_lead * len(t_lines) + 46 + 3 + 46 + e_lead * len(e_lines)
    y = SY0 + (SY1 - SY0 - block) // 2 - 30
    emblem(img, CX, y + 75, 32, CREAM); y += 150 + 70
    tracked(d, L["part_word"](p["roman"], part_cn(p["n"])), lab_f, CX, y, CREAM, 5); y += PT(6) + 44
    y = centred_lines(d, t_lines, title_f, y, CREAM, t_lead) + 46
    d.line([(CX - IN(0.22), y), (CX + IN(0.22), y)], fill=CREAM, width=3); y += 46
    centred_lines(d, e_lines, epi_f, y, CREAM, e_lead)
    first, last = p["cards"][0]["n"], p["cards"][-1]["n"]
    tracked(d, L["patterns_range"](first, last), font("Medium", PT(5.2)), CX, SY1 - PT(5.2), CREAM, 3.2)
    return img


def part_back(p):
    acc = rgb(PART_COLOURS[p["n"]][1])
    img = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(img)
    y = SY0 + 6
    tracked(d, L["part_label"](p["roman"], p["name"], part_cn(p["n"])), font("Medium", PT(5.2)), CX, y, acc, 3.0); y += PT(5.2) + 30
    d.line([(CX - IN(0.22), y), (CX + IN(0.22), y)], fill=acc, width=3); y += 40
    scale = 1.0
    while True:
        name_f, sum_f, num_f = font("Regular" if L["cjk"] else "Italic", PT(10 * scale)), font("Regular", PT(7.4 * scale)), font("Regular", PT(10 * scale))
        n_lead, s_lead, gap = round(PT(10 * scale) * 1.18), round(PT(7.4 * scale) * 1.28), round(20 * scale)
        indent = round(num_f.getlength("108") + 22)
        rows = [(c, wrap(c["summary"], sum_f, WIDTH - indent)) for c in p["cards"]]
        need = sum(n_lead + s_lead * len(s) + gap for _, s in rows)
        if y + need <= SY1 or scale <= 0.8: break
        scale -= 0.02
    for c, s_lines in rows:
        d.text((SX0 + indent - 22 - num_f.getlength(str(c["n"])), y), str(c["n"]), font=num_f, fill=acc)
        d.text((SX0 + indent, y), c["title"], font=name_f, fill=INK); y += n_lead
        y = left_lines(d, s_lines, sum_f, SX0 + indent, y, (70, 76, 92), s_lead) + gap
    return img


def title_front():
    img = Image.new("RGB", (W, H), BLUE); d = ImageDraw.Draw(img)
    emblem(img, CX, SY0 + round((SY1 - SY0) * 0.31), 92, CREAM)
    y = SY0 + round((SY1 - SY0) * 0.60)
    tf = font("Regular", PT(19))
    y = centred_lines(d, L["title_lines"], tf, y, CREAM, round(PT(19) * 1.1)) + 34
    d.line([(CX - IN(0.22), y), (CX + IN(0.22), y)], fill=CREAM, width=3); y += 40
    centred_lines(d, L["subtitle_lines"], font("Italic", PT(9.6)), y, CREAM, round(PT(9.6) * 1.3))
    tracked(d, L["deck_tag"], font("Medium", PT(5.2)), CX, SY1 - PT(5.2), CREAM, 3.2)
    return img


def title_back():
    # The book's own sentences, lifted from the manuscript so they cannot drift.
    how = (BOOK / L["root"] / "manuscript/00-FRONT/03-how-to-use-this-language.md").read_text()
    if L["cjk"]:
        # the same two sentences, as the translators rendered them: the first sentence of
        # "A pattern is a proposal in context" and the last paragraph of the chapter
        paras = [x.strip() for x in how.split("\n\n") if x.strip() and not x.startswith("#")]
        a = re.split(r"(?<=。)", paras[3])[0]; b = paras[-1]
    else:
        a = re.search(r"Each pattern names a recurring problem and proposes a response\. Its usefulness depends on circumstances and on other patterns\.", how).group(0)
        b = re.search(r"Begin wherever you have a real relationship and some capacity to help\. The whole civilization is too large to hold in one pair of hands\. A useful responsibility is not\.", how).group(0)
    steps = L["steps"]
    qr = 250; qy = SY1 - qr
    scale = 1.0
    while True:                                   # everything above the code must clear it
        img = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(img)
        emblem(img, CX, SY0 + 58, 25, BLUE); y = SY0 + 140
        it_f, body_f, lab_f = font("Italic", PT(11.4 * scale)), font("Regular", PT(9.6 * scale)), font("Medium", PT(5.2))
        lead = round(PT(9.6 * scale) * 1.32)
        y = centred_lines(d, wrap(a, it_f, WIDTH - 30), it_f, y, INK, round(PT(11.4 * scale) * 1.25)) + round(38 * scale)
        d.line([(CX - IN(0.22), y), (CX + IN(0.22), y)], fill=BLUE, width=3); y += round(38 * scale)
        y = left_lines(d, wrap(b, body_f, WIDTH), body_f, SX0, y, INK, lead) + round(34 * scale)
        tracked(d, L["using"], lab_f, SX0 + lab_f.getlength(L["using"]) / 2 + 3.0 * 7, y, BLUE, 3.0); y += PT(5.2) + 16
        for st in steps:
            y = left_lines(d, wrap(st, body_f, WIDTH), body_f, SX0, y, INK, lead) + 6
        if y <= qy - 40 or scale <= 0.8: break
        scale -= 0.02
    # foot: coach QR + credit
    buf = io.BytesIO()
    segno.make("https://civilization.galley.so", error="h").save(buf, kind="png", scale=20, border=3, dark="#161C2D", light="#FFFFFF"); buf.seek(0)
    code = Image.open(buf).convert("RGB").resize((qr, qr), Image.LANCZOS)
    mask = Image.new("L", (qr * 4, qr * 4), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, qr * 4 - 1, qr * 4 - 1], radius=70, fill=255)
    img.paste(code, (SX0, qy), mask.resize((qr, qr), Image.LANCZOS))
    tx = SX0 + qr + 34; sm = font("Regular", PT(7.4)); sl = round(PT(7.4) * 1.3)
    d.text((tx, qy + 6), L["talk"], font=font("Italic", PT(10)), fill=INK)
    end = left_lines(d, wrap(L["scan"], sm, SX1 - tx), sm, tx, qy + 6 + round(PT(10) * 1.3), INK, sl)
    credit = wrap(L["credit"], sm, SX1 - tx)
    left_lines(d, credit, sm, tx, max(end + 10, qy + qr - len(credit) * sl - 4), (70, 76, 92), sl)
    return img


if __name__ == "__main__":
    (ROOT / "print").mkdir(exist_ok=True); (ROOT / "proof").mkdir(exist_ok=True)
    out = [("T00", title_front(), title_back())] + [(f"P{p['n']:02d}", part_front(p), part_back(p)) for p in parts]
    for cid, f, b in out:
        for side, im in (("front", f), ("back", b)):
            im.save(ROOT / "print" / f"{cid}-{side}.png", dpi=(DPI, DPI)); with_guides(im).save(ROOT / "proof" / f"{cid}-{side}.png", dpi=(DPI, DPI))
    print(len(out), "cards without pictures rendered")
