# The Pattern Deck — design system

108 pattern cards from *A Civilization Worth Inheriting*, in tarot format: a
picture and the pattern's name on the front, the pattern in brief on the back.

The whole deck is rendered: `print/` holds the press-ready files, `proof/` the
same with trim and safe lines, `deck.pdf` every card front and back in order,
and `sheets/` contact sheets to look through.

## Principles

1. **One picture, one idea.** Each card shows a single concrete scene taken
   from the pattern, never a diagram or an abstraction. A person can pick the
   card up and say what is happening in it.
2. **Two inks and the paper.** Every picture is a linocut in the Earth flag's
   blue and a near-black, with the cream stock as the third tone. 108 pictures
   drawn over any length of time stay one deck.
3. **The picture is drawn; the words are set.** The image model draws only the
   art. All type is real EB Garamond placed by `render_cards.py`, so spelling,
   size and trim are exact and the deck matches the book.
4. **Nothing on the card the book does not say.** Title, summary, statement,
   first move and connections are extracted from the manuscript by
   `extract_cards.py`. Change the book, re-run, and the deck follows.
5. **The number is the address.** It is the largest thing on the front after
   the picture, as it is on every pattern's opening page in the book.

## Format (verified against printers' templates, 2026-09-30)

| | |
|---|---|
| Trim | 2.75 x 4.75 in (70 x 121 mm), standard tarot |
| Bleed | 0.125 in on every edge |
| File | 3.0 x 5.0 in, **900 x 1500 px at 300 DPI**, RGB PNG |
| Safe area | **0.20 in** inside the trim; no text outside it |
| Rules and frames | none nearer than 0.25 in to the trim |
| Corners | die-cut; 0.125 in radius at most printers, about 6 mm at MakePlayingCards |
| Deck | 121 cards: 108 patterns, 12 part cards, 1 title card. About 35 to 42 mm thick |

What each printer asks for, read from its own template or spec page:

| | MakePlayingCards | The Game Crafter | PrintNinja | Shuffled Ink | DriveThruCards |
|---|---|---|---|---|---|
| File at 300 DPI | 897 x 1497 min | 900 x 1500 | 900 x 1500 | ~881 x 1481 | 900 x 1500 |
| Bleed per edge | 0.12 in | 0.125 in | 3 mm / 0.125 in | ~0.094 in | 0.125 in |
| Safe inside trim | 0.12 in | 0.125 in | 0.125 in or 5 mm | 0.1875 in | 0.125 in |
| Colour | RGB or CMYK | RGB only | CMYK | CMYK (converts) | CMYK, 240% max |
| Upload | PNG/JPG/TIFF | PNG/JPG | PDF | PSD/AI/TIFF/JPG | PDF/X-1a |
| Unique backs | yes, free | yes, free | yes, ~$1.18/deck | likely; confirm | yes, free |
| Minimum | 1 deck | 1 deck | 500 decks | not stated | 1 deck |
| One deck of 121 | $42.90 | $36.92 | n/a | quote | $29.04 |
| 100 decks, each | $22.20 | $20.15 | n/a | quote | $21.78 |
| 500 decks, each | $14.35 | $16.90 | $13.68 to $16.23 boxed | quote | $20.33 |
| One box for 121 | yes (tuck or rigid) | Small Stout Box only | two-piece | quote | no |

Prices are cards only unless marked, before shipping, and were read or computed
from the printers' pages on 2026-09-30; confirm in a cart before ordering.

The 0.20 in safe area is wider than most printers require because Shuffled
Ink's template wants 0.1875 in and PrintNinja's tarot page says 5 mm; one
master then fits all five. Cut drift of up to 1/8 in is normal and is worse on
backs, which is why there is no border on either side.

**Colour will shift in print.** The flag blue `#023CA7` is outside the CMYK
gamut: run through The Game Crafter's GRACoL profile it lands near C99 M83 Y0
K1 and comes back as roughly `#244692`, visibly duller. The cream converts to
about C5 M5 Y11; on offset, tints under 10% can print almost white. No printer
listed offers an uncoated or cream stock, so the cream must be printed. Order a
single proof deck and judge the blue and the cream on paper before a run.

Two cautions from The Game Crafter that apply here: dark colour at the cut edge
can chip and show white (the pictures run dark to three edges), and flat
backgrounds show drift more than textured ones (the backs are flat cream).

**For a first physical proof:** MakePlayingCards, one deck, with a box that
fits 130 cards, about $43 plus box and shipping. It takes RGB PNGs as they are,
prints unique backs at no charge, and has no minimum.

## Colour

| Role | Hex | Use |
|---|---|---|
| Flag blue | `#023CA7` | art ink, rules, labels, emblem |
| Ink | `#161C2D` | art ink, all reading text |
| Cream | `#F3EEE3` | card stock colour, art paper tone |
| Hairline | `#C8C0B0` | the one rule on the back |

Blue on cream is 8.2:1 and ink on cream 14.7:1, so every label clears AA at
its printed size. For offset printing, flag blue is close to Pantone 2728 C;
confirm against a swatch, since the screen value is what was sampled from the
EarthPilot mark.

## Type

EB Garamond throughout, the book's face.

| Element | Style | Size |
|---|---|---|
| Front numeral | Regular | 25 pt |
| Front title | Italic | 15.5 pt, two lines at most, steps down to 12 |
| Part label | Medium caps, tracked | 5.4 pt, flag blue |
| Back heading (number + title) | Italic | 12.5 pt |
| Back summary | Italic, centred | 11.2 pt |
| Back statement and first move | Regular | 8.9 pt on 11.6 |
| Back labels | Medium caps, tracked | 5.2 pt, flag blue |
| Connected patterns | Regular | 7.1 pt |

A long back scales all its text together, never below 78 percent. All twelve
samples set at full size.

## Front

- Picture: full bleed off the top and both sides, 3.22 in tall. No border, so
  a cut that drifts a millimetre cannot show as an uneven frame.
- A 5 px ink line closes the picture, like the edge of a printed block.
- Cream panel beneath: numeral, title in italic, a short blue rule, the part.

## Back

Emblem, heading, part, rule, then four things in order of how fast they can be
read: the **summary** (one sentence), the **statement** (the pattern's
"Therefore"), **a first move** (what to try), and the **connected patterns**
by number and name, which is how a reader walks from one card to the next.

Backs are therefore different on every card. That suits reading, teaching and
laying cards out face up. For drawing cards unseen, deal picture side down is
no use either; if blind draws matter, print a second edition with a uniform
emblem back and move the text to a booklet.

## Art direction

The style block every prompt ends with (see `generate_art.py`):

> Two-colour linocut relief print. Inks: deep ultramarine blue (hex 023CA7)
> and near-black indigo, printed on warm cream paper (hex F3EEE3) which shows
> through as the third tone. Bold simplified shapes, confident carved lines,
> visible hand-cut texture and slight ink grain, flat areas of colour, no
> gradients, no photographic detail. The composition fills the whole frame
> edge to edge: no border, no frame, no margin, no text, no letters, no
> numbers, no signature, no watermark. Keep the important subject inside the
> middle 80 percent of the frame. Timeless and calm; no recognisable era,
> brand or modern gadget.

Scene rules:

- Start from the pattern's own opening image; most patterns begin with one.
- People are ordinary and varied; no heroes, no faces in close-up.
- Technology appears as its effect on people, never as a device. Artificial
  minds are drawn through metaphor (the kite and its string for Delegated
  Intelligence).
- No words in the picture, ever.
- Generated at 1024 x 1104 with `fal-ai/gpt-image-2`, quality high, and
  scaled to the 900 px card width. One image per call, about 1.5 minutes.

An engraving style (single blue ink, fine hatching) was tried on two cards and
dropped: paler, fussier, and weak at card size.

## The third colour (optional, `--accent`)

Each of the twelve parts is a suit with its own accent, defined in
`palette.py` and checked there for contrast on cream (all 4.5:1 or better):

| Part | Accent | Part | Accent |
|---|---|---|---|
| I | golden ochre `#8F6208` | VII | violet `#6B3FA0` |
| II | brick red `#B13B2B` | VIII | deep teal `#0D7371` |
| III | leaf green `#3B7431` | IX | burnt orange `#B0500F` |
| IV | umber `#6B4423` | X | plum `#8A2585` |
| V | olive `#6B6A1A` | XI | rose `#B83E70` |
| VI | wine `#8A1C3C` | XII | graphite `#4E5B66` |

The accent does two jobs:

- **In the frame**: a band under the picture (visible when cards are fanned),
  the short rule, and every small-caps label. The emblem stays flag blue.
- **In the picture**: a third ink, used on about a tenth of the image and
  placed on the thing the pattern is about (the bread on the common table, the
  fields in the watershed, the lamp in the reboot workshop). `add_third_ink.py`
  adds it to a finished two-ink picture with the edit endpoint, so the
  composition does not change.

Dialled in by measured perceptual distance: the closest pairs (wine and rose,
brick red and burnt orange) are 19 apart in Lab, up from 15. Still worth a
printed swatch before a full run; inks shift on uncoated cream.

## Cost (fal price table, September 2026)

`gpt-image-2` at high quality costs about $0.17 to $0.21 an image at this size
(the table lists $0.165 for 1024 x 1536 and $0.211 for 1024 x 1024; billing is
by image tokens). An edit costs about the same. Medium quality is roughly a
quarter of that.

| | Images | About |
|---|---|---|
| Whole deck as drawn (108 pictures, 12 third-ink edits, 14 early samples) | 134 | about $26 |
| Full deck, two inks (108 + 13 part and title cards) | 121 | $25 |
| Third ink added by edit to every picture | +121 | +$25 |
| Full deck drawn in three inks in one pass | 121 | $25 |

Allow half again for redraws.

## Status (2026-09-30)

All 121 cards are rendered front and back: 108 patterns, 12 part cards, one
title card. Every picture was checked for stray lettering; none has any.

Before a print run:

- **Order one proof deck** and judge the blue, the cream and the accents on
  paper. Blue on a printed cream ground shifts darker and duller than on
  screen.
- **Redraw candidates.** The guardian in 27 and the official in 46 came out in
  robes that read as ancient rather than timeless. Part XII's graphite accent
  is quiet in the pictures (it shows mainly in the band and labels); that is
  in keeping with the part, but a stronger hue is an option.
- **Look through the whole set** for repeated compositions and for dress that
  reads as one particular culture where the pattern is universal.
- **A box.** MakePlayingCards sells tuck and rigid boxes sized for 130 cards;
  the wrap can use the woodcut blue of the book cover.
- **Blind draws.** Backs are unique. If drawing unseen matters, a second
  edition needs a uniform back and the text in a booklet.

Re-drawing one card costs about 20 cents: delete `art/NNN-linocut3.png`, edit
its scene in `scenes.py`, and run `generate_art.py NNN`, then
`render_cards.py NNN` and `make_deck.py`.

## Files

```
deck/
  extract_cards.py   manuscript -> cards.json (all 108)
  scenes.py          one scene per pattern and where its third ink goes
  palette.py         the two inks, the cream, the twelve part accents
  generate_art.py    scene + style -> art/NNN-linocut3.png (three inks)
  add_third_ink.py   adds the accent ink to an older two-ink picture
  render_cards.py    art + cards.json -> print/ and proof/  (--two-ink -> print-two-ink/)
  render_extras.py   title card and twelve part cards
  make_deck.py       checks everything is there; builds deck-review.pdf, sheets/, manifest.csv
  print/             242 press-ready PNGs     proof/   the same with trim and safe lines
  book-bw/           two-tone greyscale versions for the book interior
```
