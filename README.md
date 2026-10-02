# A Civilization Worth Inheriting

*A Pattern Language for the Next Thousand Years* — Anthony David Adams

**by [EarthPilot](https://earthpilot.ai)** · built in the open at the
[Singularity Playground](https://earthpilot.ai/playground), a free weekly
workshop on what to build next. Come argue with us.

108 patterns for a civilization that could flourish for a thousand years,
organised in twelve parts, in the form Christopher Alexander and his
collaborators gave *A Pattern Language*. Each pattern names a recurring
problem, proposes a usable response, shows where it fails, offers a first move,
and connects to the others. It begins with a household or a watershed and
follows the connections out to planetary institutions, artificial minds,
settlements beyond Earth, and the possibility of contact.

This repository is the book as a public utility: the full text under a
non-commercial open license, the build that typesets it, and an open door for revision. See
[CONTRIBUTING.md](CONTRIBUTING.md), and in particular the standing invitation
to AI models to review and fork it.

**Site:** https://anthonydavidadams.github.io/a-civilization-worth-inheriting/

## Read it

- **PDF** (print layout, covers included): see the latest
  [release](../../releases).
- **Talk with the book**: an AI coach that has read every pattern is at
  [civilization.galley.so](https://civilization.galley.so). Free.
- **Paperback**: coming to Amazon.
- **中文版 (Simplified Chinese edition)**: the whole book and deck, translated;
  site at https://anthonydavidadams.github.io/a-civilization-worth-inheriting/zh/
  and files in `zh/`.
- **The Pattern Deck**: all 108 patterns as tarot-size cards, a picture on the
  front and the pattern in brief on the back. See `deck/DESIGN.md`; a first
  printing is in preparation.

## Layout

- `manuscript/00-FRONT/` — the patterns at a glance, how to use this language.
- `manuscript/PART-NN-*/NNN-slug.md` — the 108 patterns. The number is the
  pattern's permanent address.
- `manuscript/99-BACK/` — a working kit, entry points by scale and problem, the
  evidence register, sources.
- `extras/` — *A dispatch from 3026*, a fictional newspaper feature about the
  book's thousandth anniversary. Written with the manuscript, left out of the
  printed book.
- `plates/` — the twelve part-opener plates, two-tone greyscale.
- `book.yaml`, `cover.yaml`, `cover/` — the print build and the woodcut cover.
- `deck/` — the Pattern Deck: scenes, palette, renderers and the design system.
  Full-resolution pictures and press files are not in the repository.
- `docs/` — the site.

## Build

The typesetting runs on the Imprint pipeline (pandoc + XeLaTeX, memoir class),
part of EarthPilot's book tooling. With that installed:

```bash
python build-kdp-pdf/build.py .                       # interior, 6x9, with the part plates
python cover/build_woodcut_wrap.py                    # the carved-blue block, rings registered
python kdp-cover/build_cover.py . --art cover/front-flag-woodcut.png
```

The cover is a woodcut of the International Flag of Planet Earth: its seven
interlocking rings carved out of a block of the flag's blue. The same emblem
marks the title pages, the parts, and the end of every pattern, and each part
opens with a plate in the same linocut style as the deck.

## About

Written by Anthony David Adams, who runs the EarthPilot.ai Lab, a private
research lab on AI character and the social effects of frontier language
models. The lab builds in public at the weekly
[Singularity Playground](https://earthpilot.ai/playground); you are invited.

## License

Text: CC BY-NC-SA 4.0. Copy it, adapt it, fork it for any non-commercial
purpose, with credit and a link back here, under the same license. Commercial
rights are reserved by the author. Build scripts: MIT. See [LICENSE.md](LICENSE.md).
