"""Build a QPMN order's Design Data from the deck manifest.

QPMN orders carry, per material view (Card_Front, Card_Back), a list of
designs indexed from 0, each pointing at a public image URL. This script
reads the product's Design Schema (downloaded from the QPMN dashboard) and
the deck manifest and writes the designData block. The order wrapper, base
URL and auth are filled in once QPMN's per-product API document arrives.

Usage:
  python deck/qpmn/qpmn_order.py --schema design-schema.json \
      --base-url https://where-the-print-files-are-hosted/ --out design-data.json
"""
import argparse, csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True, help="Design Schema JSON from the QPMN dashboard")
    ap.add_argument("--base-url", required=True, help="public URL prefix where print-qpmn/*.png are hosted")
    ap.add_argument("--out", default=str(ROOT / "qpmn" / "design-data.json"))
    ap.add_argument("--effect", default="CMYK")
    a = ap.parse_args()

    schema = json.loads(Path(a.schema).read_text())
    rows = list(csv.DictReader(open(ROOT / "manifest.csv")))
    fronts = [f"{a.base_url.rstrip('/')}/{Path(r['front']).name}" for r in rows]
    backs = [f"{a.base_url.rstrip('/')}/{Path(r['back']).name}" for r in rows]

    materials = schema.get("materials") or schema.get("data", {}).get("materials") or []
    out = []
    for m in materials:
        views = []
        for v in m.get("views", []):
            code = v.get("code", "")
            urls = fronts if "front" in code.lower() else backs if "back" in code.lower() else None
            if urls is None:
                continue
            qty = int(v.get("qty", len(urls)))
            if qty != len(urls):
                raise SystemExit(f"view {code} takes {qty} images but the deck has {len(urls)}; "
                                 "set the store SKU's card count to 121 (or confirm unique backs are allowed)")
            views.append({"code": code, "designs": [
                {"index": i, "effectImages": [{"effect": a.effect, "url": u}]} for i, u in enumerate(urls)]})
        out.append({"code": m.get("code"), "views": views})
    Path(a.out).write_text(json.dumps(out, indent=1))
    print(f"wrote {a.out}: {sum(len(v['designs']) for mm in out for v in mm['views'])} images across "
          f"{sum(len(mm['views']) for mm in out)} views")

if __name__ == "__main__":
    main()
