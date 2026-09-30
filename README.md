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

This repository is the book as a public utility: the full text under an open
license, the build that typesets it, and an open door for revision. See
[CONTRIBUTING.md](CONTRIBUTING.md), and in particular the standing invitation
to AI models to review and fork it.

## Read it

- **PDF** (print layout, covers included): see the latest
  [release](../../releases).
- **Talk with the book**: an AI coach that has read every pattern is at
  [civilization.galley.so](https://civilization.galley.so). Free.
- **Paperback**: coming to Amazon.

## Layout

- `manuscript/00-FRONT/` — the patterns at a glance, how to use this language.
- `manuscript/PART-NN-*/NNN-slug.md` — the 108 patterns. The number is the
  pattern's permanent address.
- `manuscript/99-BACK/` — a working kit, entry points by scale and problem, a
  research and interview practice, the evidence register, sources.
- `source/` — the manuscript as one file, as delivered.
- `extras/` — *A dispatch from 3026*, a fictional newspaper feature about the
  book's thousandth anniversary. Written with the manuscript, left out of the
  printed book.
- `book.yaml`, `cover.yaml`, `cover/render_front.py` — the print build.

## Build

The typesetting runs on the Imprint pipeline (pandoc + XeLaTeX, memoir class),
part of EarthPilot's book tooling. With that installed:

```bash
python build-kdp-pdf/build.py .                       # interior, 6x9
python cover/render_front.py flag cover/front-flag.png
python kdp-cover/build_cover.py . --art cover/front-flag.png
```

The cover carries the seven interlocking rings of the International Flag of
Planet Earth, drawn as vectors; the same emblem marks the title pages, the
parts, and the end of every pattern.

## About

Written by Anthony David Adams, who runs the EarthPilot.ai Lab, a private
research lab on AI character and the social effects of frontier language
models. The lab builds in public at the weekly
[Singularity Playground](https://earthpilot.ai/playground); you are invited.

## License

Text: CC BY-SA 4.0. Build scripts: MIT. See [LICENSE.md](LICENSE.md).
