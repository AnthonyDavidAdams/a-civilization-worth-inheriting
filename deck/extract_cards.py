"""Build deck/cards.json from the manuscript: one record per pattern.

Everything printed on a card comes from the book's own text, so the deck and
the book cannot drift apart. Re-run after any manuscript change.
"""
import json, re, sys
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n import pick, part_cn

L = pick(sys.argv)
BOOK = Path(__file__).resolve().parent.parent
ROOT = BOOK / L["root"]                                    # the edition's book dir (., or zh)
OUT = BOOK / L["deck_dir"]; OUT.mkdir(exist_ok=True)
cfg = yaml.safe_load((BOOK / L["book_yaml"]).read_text())
glance = (ROOT / "manuscript/00-FRONT/02-the-patterns-at-a-glance.md").read_text()
summary = {int(n): d.strip() for n, _, d in re.findall(L["glance_re"], glance, flags=re.M)}
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]

cards, n = [], 0
for pi, part in enumerate(cfg["parts"]):
    part_name = re.sub(r"^Part [IVX]+ — ", "", part["title"])
    for f in part["chapters"]:
        n += 1
        md = (ROOT / f).read_text()
        title = re.match(r"# (.+)", md).group(1).strip()
        bolds = re.findall(r"^\*\*(.+?)\*\*\s*$", md, flags=re.M)
        statement = next((b for b in bolds if b.startswith(L["statement_prefix"])), None)
        if not statement:                       # pattern 1 states it under its "the pattern" heading
            statement = re.search(L["pattern_section_re"], md, flags=re.S).group(1).strip()
        fm = re.search(L["first_move_re"], md, flags=re.S)
        first = fm.group(1).strip()
        m = re.search(L["connected_re"], md)
        if m:
            connected = [int(x) for x in re.findall(L["connected_num_re"], m.group(1))]
        else:                                   # pattern 1 names them in prose, in its closing section
            section = md.split(L["connect_section"])[-1]
            connected = [int(x) for x in re.findall(L["connect_prose_re"], section)]
        opening = re.search(r"^# .+\n\n(?:\*\*.+\*\*\n\n)?(.+)", md).group(1).strip()
        cards.append({"n": n, "title": title, "part": pi + 1, "part_roman": ROMAN[pi], "part_cn": part_cn(pi + 1), "part_name": part_name,
                      "summary": summary[n], "statement": statement, "first_move": first,
                      "connected": connected, "opening": opening, "file": f})

(OUT / "cards.json").write_text(json.dumps(cards, indent=1, ensure_ascii=False))
none = [c["n"] for c in cards if not c["connected"]]
print(f"{len(cards)} cards; without connections: {none or 'none'}")
