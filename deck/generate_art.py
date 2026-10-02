"""Draw the card pictures with fal-ai/gpt-image-2 (ChatGPT image), in three inks.

The model draws ONLY the picture. All type is set by render_cards.py in real
EB Garamond, so spelling, size and trim are exact on every card.

Each picture is a three-colour linocut: the flag's blue, a near-black, and the
accent of the pattern's part (palette.py), placed on what the pattern is about
(scenes.py). Output: art/NNN-linocut3.png at 1024 x 1104. Existing files are
skipped, so the script can be re-run until the deck is complete.

Usage: FAL_KEY=... python deck/generate_art.py [n n n ...]     (default: every missing card)
"""
import sys, json, time, urllib.request, concurrent.futures as cf
from pathlib import Path
import fal_client

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from palette import PART_COLOURS      # noqa: E402
from scenes import SCENES             # noqa: E402

cards = {c["n"]: c for c in json.loads((ROOT / "cards.json").read_text())}

def style(n):
    name, hexv = PART_COLOURS[cards[n]["part"]]
    return (
        "Three-colour linocut relief print. Inks: deep ultramarine blue (hex 023CA7), near-black indigo, and "
        f"{name} (hex {hexv.lstrip('#')}) used sparingly as an accent on about a tenth of the image, specifically on "
        f"{SCENES[n][1]}. Printed on warm cream paper (hex F3EEE3) which shows through as the lightest tone. Bold "
        "simplified shapes, confident carved lines, visible hand-cut texture and slight ink grain, flat areas of "
        "colour, no gradients, no photographic detail. The composition fills the whole frame edge to edge: no "
        "border, no frame, no margin, no text, no letters, no numbers, no signature, no watermark. Keep the important "
        "subject inside the middle 80 percent of the frame. Timeless and calm; no recognisable era, brand or modern gadget.")

def make(n, tries=3):
    out = ROOT / "art" / f"{n:03d}-linocut3.png"
    if out.exists():
        return n, "cached"
    for attempt in range(1, tries + 1):
        try:
            r = fal_client.subscribe("fal-ai/gpt-image-2", arguments={
                "prompt": f"{SCENES[n][0]} {style(n)}", "image_size": {"width": 1024, "height": 1104},
                "quality": "high", "num_images": 1, "output_format": "png"})
            urllib.request.urlretrieve(r["images"][0]["url"], out)
            return n, "ok" if attempt == 1 else f"ok (attempt {attempt})"
        except Exception as e:
            err = repr(e)[:200]; time.sleep(8 * attempt)
    return n, f"FAILED: {err}"

if __name__ == "__main__":
    nums = [int(x) for x in sys.argv[1:]] or [n for n in sorted(SCENES)
            if not (ROOT / "art" / f"{n:03d}-linocut3.png").exists() and not (ROOT / "art" / f"{n:03d}-linocut.png").exists()]
    print(f"drawing {len(nums)} pictures", flush=True)
    done = 0
    with cf.ThreadPoolExecutor(6) as ex:
        for f in cf.as_completed([ex.submit(make, n) for n in nums]):
            n, status = f.result(); done += 1
            print(f"[{done}/{len(nums)}] {n:>3} {cards[n]['title']}: {status}", flush=True)
