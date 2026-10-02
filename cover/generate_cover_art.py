"""Cover pictures in the deck's linocut style (fal-ai/gpt-image-2).

The model draws only the picture; render_front_linocut.py sets the type.
Sized for the front panel's picture area: 6.125 x 5.68 in at ~313 DPI.

Usage: FAL_KEY=... python cover/generate_cover_art.py [name ...]
"""
import sys, urllib.request, concurrent.futures as cf
from pathlib import Path
import fal_client

STYLE = (
    "Three-colour linocut relief print. Inks: deep ultramarine blue (hex 023CA7), near-black indigo, and a golden "
    "ochre (hex C8901A) used sparingly as an accent on about a tenth of the image, printed on warm cream paper "
    "(hex F3EEE3) which shows through as the lightest tone. Bold simplified shapes, confident carved lines, visible "
    "hand-cut texture and slight ink grain, flat areas of colour, no gradients, no photographic detail. The "
    "composition fills the whole frame edge to edge: no border, no frame, no margin, no text, no letters, no "
    "numbers, no signature, no watermark. Keep the important subject inside the middle 80 percent of the frame. "
    "Timeless and calm; no recognisable era, brand or modern gadget.")

SCENES = {
    "handing-on": "An old person and a child kneeling together to plant a young tree on a hillside, their hands in the "
                  "soil; behind them a wide valley with a winding river, terraced fields, a small town and distant "
                  "mountains under a big sky with a low rising sun. The sun and the sapling's leaves are the ochre accent.",
    "open-door":  "An open doorway in a long old stone wall, the wooden door standing wide; through it a path winds "
                  "across fields past a river and a small town toward distant mountains and a rising sun; a newly "
                  "planted sapling stands beside the door and a lit lantern hangs by the doorway. The sun, the lantern "
                  "light and the sapling's leaves are the ochre accent.",
    "valley":     "A whole living valley seen from a high hill at dawn, like a map of a good place: a river running from "
                  "mountain springs through forest, fields, orchards and a small town with a bridge to the sea, tiny "
                  "figures working and walking, birds overhead, and the last stars fading above a rising sun. The sun, "
                  "the lit windows and the ripe fields are the ochre accent.",
}

def make(name):
    out = Path(f"cover/art-{name}.png")
    if out.exists():
        return name, "cached"
    r = fal_client.subscribe("fal-ai/gpt-image-2", arguments={
        "prompt": f"{SCENES[name]} {STYLE}", "image_size": {"width": 1920, "height": 1776},
        "quality": "high", "num_images": 1, "output_format": "png"})
    urllib.request.urlretrieve(r["images"][0]["url"], out)
    return name, "ok"

if __name__ == "__main__":
    names = sys.argv[1:] or list(SCENES)
    with cf.ThreadPoolExecutor(3) as ex:
        for f in cf.as_completed([ex.submit(make, n) for n in names]):
            try: print(*f.result())
            except Exception as e: print("FAILED:", repr(e)[:400])
