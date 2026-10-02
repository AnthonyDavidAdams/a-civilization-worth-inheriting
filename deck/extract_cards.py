"""Build deck/cards.json from the manuscript: one record per pattern.

Everything printed on a card comes from the book's own text, so the deck and
the book cannot drift apart. Re-run after any manuscript change.
"""
import json, re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
cfg = yaml.safe_load((ROOT / "book.yaml").read_text())
glance = (ROOT / "manuscript/00-FRONT/02-the-patterns-at-a-glance.md").read_text()
summary = {int(n): d.strip() for n, _, d in re.findall(r"^(\d+)\. \*\*([^*]+)\*\* — (.+)$", glance, flags=re.M)}
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]

cards, n = [], 0
for pi, part in enumerate(cfg["parts"]):
    part_name = re.sub(r"^Part [IVX]+ — ", "", part["title"])
    for f in part["chapters"]:
        n += 1
        md = (ROOT / f).read_text()
        title = re.match(r"# (.+)", md).group(1).strip()
        bolds = re.findall(r"^\*\*(.+?)\*\*\s*$", md, flags=re.M)
        statement = next((b for b in bolds if b.startswith("Therefore")), None)
        if not statement:                       # pattern 1 states it under "## The pattern"
            statement = re.search(r"## The pattern\s+\*\*(.+?)\*\*", md, flags=re.S).group(1).strip()
        first = re.search(r"## (?:A first move|Begin with one decision)\s+(.+?)(?:\n\n|\Z)", md, flags=re.S).group(1).strip()
        m = re.search(r"\*\*Connected patterns:\*\*\s*(.+)", md)
        if m:
            connected = [int(x) for x in re.findall(r"\((\d+)\)", m.group(1))]
        else:                                   # pattern 1 names them in prose, in its closing section
            section = md.split("## How the patterns connect")[-1]
            connected = [int(x) for x in re.findall(r"\*\*[^*]+\((\d+)\)\*\*", section)]
        opening = re.search(r"^# .+\n\n(?:\*\*.+\*\*\n\n)?(.+)", md).group(1).strip()
        cards.append({"n": n, "title": title, "part": pi + 1, "part_roman": ROMAN[pi], "part_name": part_name,
                      "summary": summary[n], "statement": statement, "first_move": first,
                      "connected": connected, "opening": opening, "file": f})

(ROOT / "deck/cards.json").write_text(json.dumps(cards, indent=1, ensure_ascii=False))
none = [c["n"] for c in cards if not c["connected"]]
print(f"{len(cards)} cards; without connections: {none or 'none'}")
