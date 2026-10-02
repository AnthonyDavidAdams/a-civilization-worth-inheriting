# Translator brief: A Civilization Worth Inheriting → 简体中文

You are translating one slice of a book of 108 "patterns" (after Christopher
Alexander's *A Pattern Language*) into Simplified Chinese for a printed
edition. The Chinese must read as a book written in Chinese by a careful
author, not as a translation. Tone: calm, exact, plain, unhurried. The English
uses short sentences; keep them short. No translationese: avoid long 的-chains,
avoid stacking modifiers before a noun, prefer verbs, prefer concrete words.
Do not add, soften, or omit anything. Do not explain. Do not leave English in
the text except proper names in parentheses on first use where helpful (e.g.
克里斯托弗·亚历山大), URLs, and source codes like [S05].

## The glossary is binding

`zh/glossary.json` holds the Chinese for every pattern title, part name, part
epigraph, section heading and key term. Use them exactly, every time:

- A pattern file's first line `# Title` becomes `# <glossary title>` (no number).
- `## The problem` → `## 问题`; `## The pattern` → `## 模式`;
  `## A workable form` → `## 一种可行的形式`; `## Where it fails` → `## 失效之处`;
  `## A first move` → `## 第一步`. Pattern 1 has extra headings; translate them
  naturally.
- The bold statement that begins **Therefore, …** becomes **因此，…** (bold kept).
- The closing line `**Connected patterns:** Title (N), Title (N).` becomes
  `**相关模式：**<glossary title>（N）、<glossary title>（N）。` with the SAME
  numbers, full-width parentheses and 、 between items.
- Cross-references to other patterns inside prose (e.g. "see Pay for Care (43)")
  use the glossary title with the number in full-width parentheses.
- *A Pattern Language* → 《模式语言》. The book's own title → 《值得继承的文明》.

## Form

- Keep the markdown structure exactly: same headings in the same order, same
  number of paragraphs, bold where the English is bold, italics (`*…*`) kept as
  `*…*` (the typesetter renders them in 楷体). Blank lines as in the source.
- Chinese punctuation throughout: ，。：；？！“”‘’（）、——…… ; no half-width
  commas or periods in Chinese sentences. Numbers stay Arabic (108, 1977, 2026).
- Lists keep their markers (`-` or `1.`). Tables, if any, keep their pipes.
- Source codes `[S01]`…`[S16]` and URLs are copied unchanged. In the sources
  chapter, keep each work's original title and author as printed, and
  translate only the descriptive sentences.
- Do not translate file names. Write each translated file to the mirrored path
  under `zh/manuscript/` with the SAME file name.

## Quality bar

Before you finish, reread every file once as a Chinese reader: fix anything
that sounds like English wearing Chinese clothes, check every glossary title
is used verbatim, and check every `（N）` number matches the source.

Report: list the files you wrote, and any term or sentence you were unsure
about with the choice you made.
