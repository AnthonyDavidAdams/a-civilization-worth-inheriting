"""Revisions to cover pictures with fal-ai/gpt-image-2/edit (composition kept)."""
import sys, urllib.request, concurrent.futures as cf
from pathlib import Path
import fal_client

JOBS = {
    # cover 2, the child redrawn as a young girl
    "handing-on-girl": ("cover/art-handing-on.png", (1920, 1776),
        "Change the child into a young girl of about eight, with long hair tied back in a loose braid, wearing a simple "
        "short-sleeved dress, kneeling in the same place and the same pose with her hands in the soil beside the old man's, "
        "planting the young tree together. Keep everything else exactly as it is: the old man, the sapling and its ochre "
        "leaves, the valley, river, town, mountains, the ochre sun and its rays, the three ink colours (ultramarine blue, "
        "near-black, golden ochre) on cream paper, and the hand-carved linocut texture. No text, no border."),
    # the current flag cover as a relief print
    "flag-linocut": ("cover/flag-rings-input.png", (1664, 2512),
        "Redraw this emblem as a hand-carved linocut relief print. A solid block of deep ultramarine blue ink (hex 023CA7) "
        "printed on warm cream paper (hex F3EEE3); the seven interlocking rings are carved away so the cream paper shows "
        "through as the rings. Keep the rings' geometry, size and position exactly as in the input: one ring in the centre "
        "and six around it, all the same size, evenly overlapping. Give it the character of a real relief print: fine "
        "gouge marks and carved texture in the blue field, slight ink grain and mottling, small hand-cut irregularities "
        "along the edges of the rings. The blue field fills the whole frame edge to edge: no border, no margin, no text, "
        "no letters, no other objects."),
}

def run(name):
    src, (w, h), prompt = JOBS[name]
    out = Path(f"cover/art-{name}.png")
    if out.exists(): return name, "cached"
    url = fal_client.upload_file(src)
    r = fal_client.subscribe("fal-ai/gpt-image-2/edit", arguments={
        "prompt": prompt, "image_urls": [url], "image_size": {"width": w, "height": h},
        "quality": "high", "num_images": 1, "output_format": "png"})
    urllib.request.urlretrieve(r["images"][0]["url"], out)
    return name, "ok"

if __name__ == "__main__":
    names = sys.argv[1:] or list(JOBS)
    with cf.ThreadPoolExecutor(3) as ex:
        for f in cf.as_completed([ex.submit(run, n) for n in names]):
            try: print(*f.result())
            except Exception as e: print("FAILED:", repr(e)[:400])
