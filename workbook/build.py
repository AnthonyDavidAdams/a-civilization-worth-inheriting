"""The Pattern Workbook, complete: 8.5 x 11 in, for KDP paperback on white paper.

  front: title page, rights page, how to use (three cadences), entry points by scale and problem
  body:  twelve parts, each a divider page then nine spreads (left: the pattern in brief, its first
         move, the prompts; right: a dot-grid notes page), in deck order
  back:  twelve copies of the book's ten-question pattern worksheet

Text comes from deck/cards.json and the manuscript; prompts from workbook/prompts.json (written by
Astra, see write_prompts.py). Patterns without prompts get a placeholder so the layout can be
checked before the writing is done.

  ~/.fal-venv/bin/python workbook/build.py          -> workbook/build/workbook.pdf
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "deck"))
from palette import PART_COLOURS  # noqa: E402

XELATEX = Path.home() / "Library/TinyTeX/bin/universal-darwin/xelatex"
OUT = ROOT / "workbook/build"; OUT.mkdir(parents=True, exist_ok=True)
cards = {c["n"]: c for c in json.load(open(ROOT / "deck/cards.json"))}
prompts = json.load(open(ROOT / "workbook/prompts.json"))
cfg_parts = __import__("yaml").safe_load(open(ROOT / "book.yaml"))["parts"]   # titles + epigraphs
PLACEHOLDER = ["Where is this already partly true in your place?", "Who carries the cost of the first move, and who is missing from the room?",
               "What does the chapter say goes wrong, and is it going wrong here?", "What would tell you in a month that it worked or failed?"]


def tex(s):
    return (str(s).replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
            .replace("#", r"\#").replace("_", r"\_").replace("{", r"\{").replace("}", r"\}"))


def md_to_tex(path):
    """Back-matter markdown -> LaTeX body (pandoc), headings unnumbered, no page breaks."""
    r = subprocess.run(["pandoc", "--from=markdown+smart", "--to=latex", "--wrap=none", "--top-level-division=section", str(path)],
                       capture_output=True, text=True, check=True)
    body = re.sub(r"^\\section\{.*\}\\label\{.*\}\n", "", r.stdout, count=1, flags=re.M)      # the H1 is the page title
    body = body.replace("\\subsection{", "\\sect{").replace("\\subsubsection{", "\\sect{")
    body = re.sub(r"\\label\{[^}]*\}", "", body)
    body = re.sub(r"\\hypertarget\{[^}]*\}\{%?\n?", "", body)
    return body


def spread(n):
    c = cards[n]; acc = PART_COLOURS[c["part"]][1].lstrip("#")
    conn = ", ".join(f"{cards[m]['title']} ({m})" for m in c["connected"] if m in cards)
    ps = prompts.get(str(n)) or PLACEHOLDER
    ps_tex = "".join(rf"\prompt{{{tex(p)}}}" + "\n" for p in ps[:5])
    return rf"""
\cleartoevenpage
\definecolor{{accent}}{{HTML}}{{{acc}}}
\noindent{{\color{{accent}}\rule{{\linewidth}}{{3pt}}}}\par\vspace{{6pt}}
\noindent{{\color{{accent}}\scshape\addfontfeature{{LetterSpace=14}}\small Part {c['part_roman']} \,·\, {tex(c['part_name'])}}}\par\vspace{{14pt}}
\noindent{{\fontsize{{40}}{{40}}\selectfont\color{{muted}}{n}}}\hspace{{12pt}}{{\fontsize{{26}}{{28}}\selectfont\itshape {tex(c['title'])}}}\par\vspace{{10pt}}
\noindent{{\fontsize{{13}}{{17}}\selectfont\itshape\color{{ink}}{tex(c['summary'])}}}\par\vspace{{10pt}}
\sect{{The first move}}
\noindent {tex(c['first_move'])}\par\vspace{{8pt}}
\sect{{Questions}}
{ps_tex}
\vfill
\noindent{{\color{{muted}}\small\scshape\addfontfeature{{LetterSpace=10}}Connected patterns}}\par\vspace{{2pt}}
\noindent{{\small\color{{ink}}{tex(conn)}}}
\clearpage
\noindent{{\color{{accent}}\rule{{\linewidth}}{{3pt}}}}\par\vspace{{6pt}}
\noindent{{\color{{muted}}\scshape\addfontfeature{{LetterSpace=14}}\small Notes \,·\, {n} {tex(c['title'])}}}\hfill{{\color{{muted}}\small Place \rule{{1.6in}}{{0.3pt}}\quad Date \rule{{1.1in}}{{0.3pt}}}}\par\vspace{{10pt}}
\noindent\dotgrid
\vfill
\noindent{{\color{{muted}}\small Came from card \rule{{0.6in}}{{0.3pt}}\qquad Next card \rule{{0.6in}}{{0.3pt}}\qquad Worksheet? \rule{{0.5in}}{{0.3pt}}}}
"""


def divider(part):
    mine = [c for n, c in sorted(cards.items()) if c["part"] == part]
    acc = PART_COLOURS[part][1].lstrip("#"); p = cfg_parts[part - 1]
    name = re.sub(r"^Part [IVX]+ — ", "", p["title"])
    items = "\n".join(rf"\noindent{{\color{{muted}}{c['n']}}}\quad {tex(c['title'])}\par\vspace{{3pt}}" for c in mine)
    return rf"""
\cleardoublepage
\definecolor{{accent}}{{HTML}}{{{acc}}}
\vspace*{{1.6in}}
\noindent{{\color{{accent}}\rule{{1.4in}}{{3pt}}}}\par\vspace{{16pt}}
\noindent{{\color{{accent}}\scshape\addfontfeature{{LetterSpace=16}}\large Part {mine[0]['part_roman']}}}\par\vspace{{10pt}}
\noindent{{\fontsize{{34}}{{38}}\selectfont\itshape {tex(name)}}}\par\vspace{{18pt}}
\noindent{{\fontsize{{14}}{{20}}\selectfont\color{{ink}}{tex(p['epigraph'])}}}\par\vspace{{34pt}}
\sect{{The nine patterns}}
{items}
\vfill
\noindent{{\color{{muted}}\small Week \rule{{0.45in}}{{0.3pt}} of twelve \qquad Started \rule{{1.1in}}{{0.3pt}} \qquad Monday's card \rule{{0.5in}}{{0.3pt}}}}
"""


WORKSHEET = [
    ("Place and purpose.", "Where are we working, and what should become better for whom?"),
    ("Current conditions.", "What is already happening? What do we know through observation, and what are we assuming?"),
    ("People and other lives affected.", "Who benefits, who bears burdens, and who is missing from the decision? Who represents absent interests, and how are they accountable?"),
    ("Selected patterns.", "Which three to seven patterns matter most? What does each require here?"),
    ("Tensions and alternatives.", "Where do the patterns pull in different directions? What are at least two feasible responses, including doing nothing?"),
    ("Authority and consent.", "Who can decide, refuse, appeal, pause, or require a change? Which permissions are needed before beginning?"),
    ("Resources and care.", "Who will do the work, pay the costs, maintain the result, and inherit unfinished duties?"),
    ("Trial and boundaries.", "What can we learn through a limited first step? What would cause us to stop? How will we end responsibly?"),
    ("Evidence and review.", "What would count as improvement or harm? Who will examine the result independently, and when?"),
    ("Public memory.", "What should be shared, what should remain private, and where will the account be kept for successors?"),
]
LINES3 = r"\par\vspace{{9pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{14pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{14pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{9pt}}"


def worksheet(k):
    q = lambda i, a, b: rf"\noindent{{\bfseries {i}. {tex(a)}}} {{\color{{muted}}{tex(b)}}}" + LINES3.format() + "\n"
    first = "".join(q(i, a, b) for i, (a, b) in enumerate(WORKSHEET[:5], 1))
    second = "".join(q(i, a, b) for i, (a, b) in enumerate(WORKSHEET[5:], 6))
    return rf"""
\cleartoevenpage
\noindent{{\color{{blue}}\rule{{\linewidth}}{{3pt}}}}\par\vspace{{6pt}}
{{\fontsize{{24}}{{28}}\selectfont\itshape The pattern worksheet}}\hfill{{\color{{muted}}\small {k} of 12\quad Decision \rule{{1.6in}}{{0.3pt}}\quad Date \rule{{0.9in}}{{0.3pt}}}}\par\vspace{{6pt}}
{{\small\color{{muted}}Use one worksheet for each big decision. Change it as the work changes. Keep the answers short enough that the people involved can read them and push back.}}\par\vspace{{4pt}}
{first}
\clearpage
\noindent{{\color{{blue}}\rule{{\linewidth}}{{3pt}}}}\par\vspace{{14pt}}
{second}
\vfill
\noindent{{\color{{muted}}\small Review date \rule{{0.9in}}{{0.3pt}}\qquad Independent reader \rule{{1.5in}}{{0.3pt}}\qquad Record kept at \rule{{1.3in}}{{0.3pt}}}}
"""


PARTS = {}
for c in cards.values():
    PARTS.setdefault(c["part"], (c["part_roman"], c["part_name"]))
weeks = "\n".join(rf"{w} & {PARTS[w][0]} & {tex(PARTS[w][1])} & \rule{{1.5in}}{{0.3pt}} \\[4pt]" for w in range(1, 13))
entry_points = md_to_tex(ROOT / "manuscript/99-BACK/02-entry-points-by-scale-and-problem.md")

doc = rf"""
\documentclass[letterpaper,11pt,twoside,openright]{{memoir}}
\usepackage{{fontspec,xcolor,graphicx,tikz,array,hyperref}}
\hypersetup{{hidelinks,pdftitle={{A Civilization Worth Inheriting: The Workbook}},pdfauthor={{Anthony David Adams}}}}
\setmainfont{{EB Garamond}}
\definecolor{{blue}}{{HTML}}{{023CA7}}\definecolor{{ink}}{{HTML}}{{161C2D}}\definecolor{{muted}}{{HTML}}{{5A6070}}\definecolor{{cream}}{{HTML}}{{F3EEE3}}\definecolor{{rulec}}{{HTML}}{{C9C1B0}}
\setlrmarginsandblock{{0.9in}}{{0.75in}}{{*}}\setulmarginsandblock{{0.8in}}{{0.8in}}{{*}}\checkandfixthelayout
\setlength{{\parindent}}{{0pt}}\setlength{{\parskip}}{{0pt}}
\setsecnumdepth{{none}}
\makepagestyle{{folio}}\makeevenfoot{{folio}}{{}}{{\color{{muted}}\small\thepage}}{{}}\makeoddfoot{{folio}}{{}}{{\color{{muted}}\small\thepage}}{{}}
\pagestyle{{folio}}
\newcommand{{\sect}}[1]{{\par\vspace{{4pt}}\noindent{{\color{{blue}}\scshape\addfontfeature{{LetterSpace=14}}\small #1}}\par\vspace{{4pt}}}}
\newcommand{{\prompt}}[1]{{\noindent #1\par\vspace{{9pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{13pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{7pt}}}}
\newcommand{{\dotgrid}}{{\begin{{tikzpicture}}
  \foreach \x in {{0,0.25,...,6.85}} \foreach \y in {{0,0.25,...,7.75}} \fill[rulec] (\x in,\y in) circle (0.35pt);
\end{{tikzpicture}}}}
\begin{{document}}
% ---- title page
\thispagestyle{{empty}}
\vspace*{{2.2in}}
\begin{{center}}
\includegraphics[width=1.6in]{{{ROOT}/cover/emblem-white.png}}\par\vspace{{0.5in}}
{{\fontsize{{34}}{{40}}\selectfont A Civilization Worth Inheriting}}\par\vspace{{14pt}}
{{\color{{blue}}\rule{{1.2in}}{{0.4pt}}}}\par\vspace{{14pt}}
{{\fontsize{{20}}{{26}}\selectfont\itshape The Workbook}}\par\vspace{{10pt}}
{{\fontsize{{12}}{{16}}\selectfont\color{{muted}}Questions and room to write, for each of the 108 patterns}}\par\vspace{{1.6in}}
{{\scshape\addfontfeature{{LetterSpace=22}}\small Anthony David Adams}}
\end{{center}}
\clearpage
% ---- rights
\thispagestyle{{empty}}
\vspace*{{\fill}}
{{\small\color{{muted}}
\noindent A Civilization Worth Inheriting: The Workbook\par\vspace{{6pt}}
\noindent Copyright © 2026 Anthony David Adams.\par\vspace{{6pt}}
\noindent The pattern texts are from \emph{{A Civilization Worth Inheriting: A Pattern Language for the Next Thousand Years}}. Like the book, the text of this workbook is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0. Copy it, adapt it and share it for non-commercial purposes with credit and a link to the original project, under the same license. Commercial rights are reserved by the author.\par\vspace{{6pt}}
\noindent License: creativecommons.org/licenses/by-nc-sa/4.0\par
\noindent Original project: github.com/AnthonyDavidAdams/a-civilization-worth-inheriting\par
\noindent The book's coach, which has read every pattern: civilization.galley.so\par\vspace{{6pt}}
\noindent The seven-ring emblem is the International Flag of Planet Earth, a design by Oskar Pernefeldt.
}}
\clearpage
% ---- how to use
\thispagestyle{{empty}}
\begingroup\setlength{{\parskip}}{{7pt}}
{{\fontsize{{28}}{{32}}\selectfont\itshape How to use this workbook}}\par\vspace{{14pt}}
Every pattern in the book gets two pages here. On the left: what the pattern says, its first move, and a few questions written just for it. On the right: a blank page to write on. The numbers match the cards. Draw a card, open to its number, write. Here are three ways to use it.\par\vspace{{10pt}}
\sect{{A card a day}}
Draw one card. Read its two pages. Answer one question, and write down where its first move would land in your own life. 108 cards takes about four months. Skip the ones that do not fit you. Come back to the ones that do.\par\vspace{{10pt}}
\sect{{A part a week}}
Twelve weeks, one part a week. Read the part's nine patterns during the week. On Monday, draw one card from that part and carry its first move with you. At the weekend, fill in one worksheet for a real decision the part touched. Week twelve pulls the earlier weeks together. Each part opens with a page where you can write the week you began.\par\vspace{{8pt}}
{{\small\begin{{tabular}}{{@{{}}>{{\color{{muted}}}}r l l l@{{}}}}
{weeks}
\end{{tabular}}}}\par\vspace{{10pt}}
\sect{{When a decision comes}}
Go straight to the worksheets at the back. Their ten questions come from the book. In question four you pick three to seven patterns. Turn to their pages to work out what each one asks of you. The next page lists the patterns by size of place and by problem, to help you find them.\par\vspace{{10pt}}
\sect{{Rules of the house}}
Keep answers short enough that someone else could read them and push back. Put a date on everything. When you come back, say what you changed. The book makes the case. This is where you keep the record.
\endgroup
\clearpage
% ---- entry points
\begingroup\setlength{{\parskip}}{{6pt}}
{{\fontsize{{24}}{{28}}\selectfont\itshape Entry points by scale and problem}}\par\vspace{{10pt}}
{entry_points}
\endgroup
% ---- the twelve parts
{"".join(divider(p) + "".join(spread(n) for n in sorted(cards) if cards[n]["part"] == p) for p in range(1, 13))}
% ---- worksheets
{"".join(worksheet(k) for k in range(1, 13))}
\end{{document}}
"""

(OUT / "workbook.tex").write_text(doc)
for _ in range(2):
    r = subprocess.run([str(XELATEX), "-interaction=nonstopmode", "-halt-on-error", "workbook.tex"], cwd=OUT, capture_output=True, text=True)
if r.returncode:
    print(r.stdout[-3000:]); sys.exit("xelatex failed")
log = (OUT / "workbook.log").read_text(errors="ignore")
over = re.findall(r"Overfull \\[hv]box \(([0-9.]+)pt", log)
pages = re.search(r"Pages:\s+(\d+)", subprocess.check_output(["pdfinfo", str(OUT / "workbook.pdf")], text=True)).group(1)
missing = [n for n in cards if str(n) not in prompts]
print(f"wrote {OUT / 'workbook.pdf'}: {pages} pages; overfull boxes {len(over)} (max {max(map(float, over)) if over else 0:.0f}pt); "
      f"{len(missing)} patterns still on placeholder prompts{': ' + str(missing[:10]) if missing else ''}")
