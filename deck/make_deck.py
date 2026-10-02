"""Assemble the finished deck from the rendered cards.

  print/                 242 press-ready PNGs (121 cards x front, back)
  deck-review.pdf        every card, front then back, in deck order, at half size for reading on screen
  sheets/fronts-all.png  all 121 fronts on one sheet
  sheets/part-NN.png     each part: its part card and nine patterns, fronts over backs
  manifest.csv           card id, title, part, front file, back file (the upload order)

Deck order: the title card, then for each part its part card followed by its nine patterns.
Run render_cards.py and render_extras.py first; this script only checks and assembles.
"""
import csv, json, sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n import pick
L = pick(sys.argv)
ROOT = Path(__file__).resolve().parent.parent / L["deck_dir"]
cards = json.loads((ROOT / "cards.json").read_text())
order = [("T00", "A Civilization Worth Inheriting", 0)]
for part in range(1, 13):
    mine = [c for c in cards if c["part"] == part]
    order.append((f"P{part:02d}", f"{mine[0].get('part_cn') if L['cjk'] else 'Part ' + mine[0]['part_roman']}: {mine[0]['part_name']}", part))
    order += [(f"{c['n']:03d}", f"{c['n']} {c['title']}", part) for c in mine]

missing = [f"{cid}-{side}" for cid, _, _ in order for side in ("front", "back") if not (ROOT / "print" / f"{cid}-{side}.png").exists()]
if missing:
    sys.exit(f"{len(missing)} card faces not rendered yet, e.g. {missing[:6]}")
bad = [p.name for p in (ROOT / "print").glob("*.png") if Image.open(p).size != (900, 1500)]
assert not bad, bad

with open(ROOT / "manifest.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["position", "card", "title", "part", "front", "back"])
    for i, (cid, title, part) in enumerate(order, 1):
        w.writerow([i, cid, title, part or "", f"print/{cid}-front.png", f"print/{cid}-back.png"])

B = R = 38
def trimmed(cid, side, s):
    im = Image.open(ROOT / "print" / f"{cid}-{side}.png").convert("RGB").crop((B, B, 900 - B, 1500 - B))
    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=R, fill=255)
    size = (round(im.width * s), round(im.height * s)); return im.resize(size, Image.LANCZOS), mask.resize(size, Image.LANCZOS)

(ROOT / "sheets").mkdir(exist_ok=True)
BG = (58, 60, 66)
# all fronts, 11 x 11
s = 0.26; cw, ch = trimmed("T00", "front", s)[0].size; pad = 14
sheet = Image.new("RGB", (11 * cw + 12 * pad, 11 * ch + 12 * pad), BG)
for i, (cid, _, _) in enumerate(order):
    im, m = trimmed(cid, "front", s); sheet.paste(im, (pad + (i % 11) * (cw + pad), pad + (i // 11) * (ch + pad)), m)
sheet.save(ROOT / "sheets" / "fronts-all.png")
# one sheet per part: fronts above backs
s = 0.42; cw, ch = trimmed("T00", "front", s)[0].size; pad = 22
for part in range(1, 13):
    ids = [cid for cid, _, p in order if p == part]
    sh = Image.new("RGB", (len(ids) * cw + (len(ids) + 1) * pad, 2 * ch + 3 * pad), BG)
    for i, cid in enumerate(ids):
        for row, side in enumerate(("front", "back")):
            im, m = trimmed(cid, side, s); sh.paste(im, (pad + i * (cw + pad), pad + row * (ch + pad)), m)
    sh.save(ROOT / "sheets" / f"part-{part:02d}.png")
# review PDF at half size
pages = [Image.open(ROOT / "print" / f"{cid}-{side}.png").convert("RGB").resize((450, 750), Image.LANCZOS) for cid, _, _ in order for side in ("front", "back")]
pages[0].save(ROOT / "deck-review.pdf", "PDF", resolution=150, save_all=True, append_images=pages[1:])
size = sum(p.stat().st_size for p in (ROOT / "print").glob("*.png")) / 1e6
print(f"{len(order)} cards, {2 * len(order)} faces, print folder {size:.0f} MB, review PDF {(ROOT / 'deck-review.pdf').stat().st_size / 1e6:.1f} MB")
