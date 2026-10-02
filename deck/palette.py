"""The deck's colours. Two constant inks plus one accent per part (the suit)."""

CREAM, INK, BLUE = (243, 238, 227), (22, 28, 45), (2, 60, 167)

# part number -> (ink name for art prompts, hex). Printmaker's earths and
# mineral colours. Dialled in on 2026-09-30 by measured perceptual distance
# (CIE Lab): the closest pair is now 19 apart, up from 15, and every accent
# carries small caps on cream at 4.5:1 or better. `python deck/palette.py`
# prints the figures.
PART_COLOURS = {
    1:  ("golden ochre",   "#8F6208"),   # Responsibility across time
    2:  ("brick red",      "#B13B2B"),   # Becoming human together
    3:  ("leaf green",     "#3B7431"),   # The living planet
    4:  ("umber",          "#6B4423"),   # Places and material life
    5:  ("olive",          "#6B6A1A"),   # An economy that supports life
    6:  ("wine",           "#8A1C3C"),   # Power that remains answerable
    7:  ("violet",         "#6B3FA0"),   # A civilization that can know
    8:  ("deep teal",      "#0D7371"),   # Living with artificial minds
    9:  ("burnt orange",   "#B0500F"),   # Continuity through disruption
    10: ("plum",           "#8A2585"),   # Neighbors in the cosmos
    11: ("rose",           "#B83E70"),   # Lives worth living
    12: ("graphite",       "#4E5B66"),   # Putting the language to work
}

def rgb(hexv):
    h = hexv.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def contrast(a, b):
    def lum(c):
        f = lambda v: v / 255 / 12.92 if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])
    hi, lo = max(lum(a), lum(b)), min(lum(a), lum(b))
    return (hi + 0.05) / (lo + 0.05)

if __name__ == "__main__":
    import colorsys, itertools
    for p, (name, hexv) in PART_COLOURS.items():
        c = rgb(hexv); h = colorsys.rgb_to_hls(*[v / 255 for v in c])[0] * 360
        print(f"{p:>2} {name:<14} {hexv}  on cream {contrast(c, CREAM):.1f}:1  vs blue ΔRGB {sum((a-b)**2 for a,b in zip(c,BLUE))**.5:.0f}  hue {h:.0f}°")
    closest = min(itertools.combinations(PART_COLOURS.items(), 2), key=lambda ab: sum((x - y) ** 2 for x, y in zip(rgb(ab[0][1][1]), rgb(ab[1][1][1]))))
    print("closest pair:", closest[0][1][0], "/", closest[1][1][0], f"ΔRGB {sum((x-y)**2 for x,y in zip(rgb(closest[0][1][1]), rgb(closest[1][1][1])))**.5:.0f}")
