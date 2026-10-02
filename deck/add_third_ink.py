"""Add a third printing ink to an existing two-ink card picture.

Uses fal-ai/gpt-image-2/edit on the finished linocut, so the composition is
kept and only an accent layer is added. The accent colour is the card's part
colour (PART_COLOURS in render_cards.py).

Usage: FAL_KEY=... python deck/add_third_ink.py n n n ...
"""
import sys, json, urllib.request, concurrent.futures as cf
from pathlib import Path
import fal_client

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from palette import PART_COLOURS          # noqa: E402

cards = {c["n"]: c for c in json.loads((ROOT / "cards.json").read_text())}

from scenes import SCENES             # noqa: E402  (scene, where the third ink goes)

def make(n):
    out = ROOT / "art" / f"{n:03d}-linocut3.png"
    if out.exists():
        return n, "cached"
    name, hexv = PART_COLOURS[cards[n]["part"]]
    url = fal_client.upload_file(str(ROOT / "art" / f"{n:03d}-linocut.png"))
    prompt = (
        "This is a two-colour linocut relief print in ultramarine blue and near-black on cream paper. "
        f"Add a third printed ink layer in {name} (hex {hexv.lstrip('#')}), used sparingly as an accent on {SCENES[n][1]}: "
        "roughly a tenth of the image, as flat hand-carved shapes with the same cut texture and slight ink grain as the "
        "other two inks, like a real three-colour reduction print. Keep the composition, every carved line, the blue, "
        "the near-black and the cream paper exactly as they are. Do not add text, borders or new objects.")
    r = fal_client.subscribe("fal-ai/gpt-image-2/edit", arguments={
        "prompt": prompt, "image_urls": [url],
        "image_size": {"width": 1024, "height": 1104}, "quality": "high", "num_images": 1, "output_format": "png"})
    urllib.request.urlretrieve(r["images"][0]["url"], out)
    return n, "ok"

if __name__ == "__main__":
    nums = [int(x) for x in sys.argv[1:]] or [n for n in sorted(SCENES)
            if (ROOT / "art" / f"{n:03d}-linocut.png").exists() and not (ROOT / "art" / f"{n:03d}-linocut3.png").exists()]
    print("adding a third ink to", nums, flush=True)
    with cf.ThreadPoolExecutor(4) as ex:
        for f in cf.as_completed([ex.submit(make, n) for n in nums]):
            try: print(*f.result())
            except Exception as e: print("FAILED:", repr(e)[:400])
