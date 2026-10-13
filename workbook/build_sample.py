"""Six-page sample of the Pattern Workbook: cover, how to use it, two pattern spreads, the worksheet.

8.5 x 11 in, white paper, EB Garamond, one accent colour per part (deck/palette.py). The
pattern text (title, summary, first move, connections) comes from deck/cards.json so the
workbook cannot drift from the deck or the book; the exploration prompts are new text and
live in prompts.json (two patterns so far).

  ~/.fal-venv/bin/python workbook/build_sample.py      -> workbook/build/sample.pdf
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
SAMPLE = [1, 65]


def tex(s):
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
             .replace("#", r"\#").replace("_", r"\_").replace("{", r"\{").replace("}", r"\}"))


def spread(n):
    c = cards[n]; acc = PART_COLOURS[c["part"]][1].lstrip("#")
    conn = ", ".join(f"{cards[m]['title']} ({m})" for m in c["connected"] if m in cards)
    ps = "".join(rf"\prompt{{{tex(p)}}}" + "\n" for p in prompts[str(n)])
    return rf"""
\cleartoevenpage
\definecolor{{accent}}{{HTML}}{{{acc}}}
\thispagestyle{{empty}}
\noindent{{\color{{accent}}\rule{{\linewidth}}{{3pt}}}}\par\vspace{{6pt}}
\noindent{{\color{{accent}}\scshape\addfontfeature{{LetterSpace=14}}\small Part {c['part_roman']} \,·\, {tex(c['part_name'])}}}\par\vspace{{14pt}}
\noindent{{\fontsize{{40}}{{40}}\selectfont\color{{muted}}{n}}}\hspace{{12pt}}{{\fontsize{{26}}{{28}}\selectfont\itshape {tex(c['title'])}}}\par\vspace{{10pt}}
\noindent{{\fontsize{{13}}{{17}}\selectfont\itshape\color{{ink}}{tex(c['summary'])}}}\par\vspace{{10pt}}
\sect{{The first move}}
\noindent {tex(c['first_move'])}\par\vspace{{8pt}}
\sect{{Questions}}
{ps}
\vfill
\noindent{{\color{{muted}}\small\scshape\addfontfeature{{LetterSpace=10}}Connected patterns}}\par\vspace{{2pt}}
\noindent{{\small\color{{ink}}{tex(conn)}}}
\clearpage
\thispagestyle{{empty}}
\noindent{{\color{{accent}}\rule{{\linewidth}}{{3pt}}}}\par\vspace{{6pt}}
\noindent{{\color{{muted}}\scshape\addfontfeature{{LetterSpace=14}}\small Notes \,·\, {n} {tex(c['title'])}}}\hfill{{\color{{muted}}\small Place \rule{{1.6in}}{{0.3pt}}\quad Date \rule{{1.1in}}{{0.3pt}}}}\par\vspace{{10pt}}
\noindent\dotgrid
\vfill
\noindent{{\color{{muted}}\small Came from card \rule{{0.6in}}{{0.3pt}}\qquad Next card \rule{{0.6in}}{{0.3pt}}\qquad Worksheet? \rule{{0.5in}}{{0.3pt}}}}
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

PARTS = {}
for c in cards.values():
    PARTS.setdefault(c["part"], (c["part_roman"], c["part_name"]))
weeks = "\n".join(rf"{w} & {PARTS[w][0]} & {tex(PARTS[w][1])} & \rule{{1.5in}}{{0.3pt}} \\[4pt]" for w in range(1, 13))

doc = rf"""
\documentclass[letterpaper,11pt,twoside,openright]{{memoir}}
\usepackage{{fontspec,xcolor,graphicx,tikz,array}}
\setmainfont{{EB Garamond}}
\definecolor{{blue}}{{HTML}}{{023CA7}}\definecolor{{ink}}{{HTML}}{{161C2D}}\definecolor{{muted}}{{HTML}}{{5A6070}}\definecolor{{cream}}{{HTML}}{{F3EEE3}}\definecolor{{rulec}}{{HTML}}{{C9C1B0}}
\setlrmarginsandblock{{0.9in}}{{0.75in}}{{*}}\setulmarginsandblock{{0.8in}}{{0.8in}}{{*}}\checkandfixthelayout
\setlength{{\parindent}}{{0pt}}\setlength{{\parskip}}{{0pt}}
\newcommand{{\sect}}[1]{{\noindent{{\color{{blue}}\scshape\addfontfeature{{LetterSpace=14}}\small #1}}\par\vspace{{4pt}}}}
% a prompt with two ruled lines to answer on
\newcommand{{\prompt}}[1]{{\noindent #1\par\vspace{{9pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{13pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{7pt}}}}
% a dot grid filling the text block below the header
\newcommand{{\dotgrid}}{{\begin{{tikzpicture}}
  \foreach \x in {{0,0.25,...,6.85}} \foreach \y in {{0,0.25,...,7.75}} \fill[rulec] (\x in,\y in) circle (0.35pt);
\end{{tikzpicture}}}}
\begin{{document}}
% ---- cover
\thispagestyle{{empty}}
\begin{{tikzpicture}}[remember picture,overlay]
  \fill[blue] (current page.south west) rectangle (current page.north east);
  \node at ([yshift=1.9in]current page.center) {{\includegraphics[width=2.6in]{{{ROOT}/cover/emblem-cream.png}}}};
  \node[text=cream,align=center,font=\fontsize{{40}}{{46}}\selectfont] at ([yshift=-0.9in]current page.center) {{A Civilization\\Worth Inheriting}};
  \node[text=cream] at ([yshift=-1.9in]current page.center) {{\color{{cream}}\rule{{1.2in}}{{0.4pt}}}};
  \node[text=cream,align=center,font=\fontsize{{20}}{{26}}\selectfont\itshape] at ([yshift=-2.55in]current page.center) {{The Workbook}};
  \node[text=cream,align=center,font=\fontsize{{12}}{{16}}\selectfont] at ([yshift=-3.2in]current page.center) {{Questions and room to write, for each of the 108 patterns}};
  \node[text=cream] at ([yshift=-4.6in]current page.center) {{\scshape\addfontfeature{{LetterSpace=22}}\small Anthony David Adams}};
\end{{tikzpicture}}
\cleardoublepage
% ---- how to use
\thispagestyle{{empty}}
\begingroup\setlength{{\parskip}}{{7pt}}
{{\fontsize{{28}}{{32}}\selectfont\itshape How to use this workbook}}\par\vspace{{14pt}}
Every pattern in the book gets two pages here. On the left: what the pattern says, its first move, and a few questions written just for it. On the right: a blank page to write on. The numbers match the cards. Draw a card, open to its number, write. Here are three ways to use it.\par\vspace{{10pt}}
\sect{{A card a day}}
Draw one card. Read its two pages. Answer one question, and write down where its first move would land in your own life. 108 cards takes about four months. Skip the ones that do not fit you. Come back to the ones that do.\par\vspace{{10pt}}
\sect{{A part a week}}
Twelve weeks, one part a week. Read the part's nine patterns during the week. On Monday, draw one card from that part and carry its first move with you. At the weekend, fill in one worksheet for a real decision the part touched. Week twelve pulls the earlier weeks together. Write your start date beside each part.\par\vspace{{8pt}}
{{\small\begin{{tabular}}{{@{{}}>{{\color{{muted}}}}r l l l@{{}}}}
{weeks}
\end{{tabular}}}}\par\vspace{{10pt}}
\sect{{When a decision comes}}
Go straight to the worksheet at the back. Its ten questions come from the book. In question four you pick three to seven patterns. Turn to their pages to work out what each one asks of you.\par\vspace{{10pt}}
\sect{{Rules of the house}}
Keep answers short enough that someone else could read them and push back. Put a date on everything. When you come back, say what you changed. The book makes the case. This is where you keep the record.
\endgroup
% ---- two sample spreads
{spread(1)}
{spread(65)}
% ---- worksheet
\cleartoevenpage
\thispagestyle{{empty}}
\noindent{{\color{{blue}}\rule{{\linewidth}}{{3pt}}}}\par\vspace{{6pt}}
{{\fontsize{{24}}{{28}}\selectfont\itshape The pattern worksheet}}\hfill{{\color{{muted}}\small Decision \rule{{1.8in}}{{0.3pt}}\quad Date \rule{{1in}}{{0.3pt}}}}\par\vspace{{6pt}}
{{\small\color{{muted}}Use one worksheet for each big decision. Change it as the work changes. Keep the answers short enough that the people involved can read them and push back.}}\par\vspace{{4pt}}
{"".join(rf"\noindent{{\bfseries {i}. {tex(a)}}} {{\color{{muted}}{tex(b)}}}\par\vspace{{9pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{14pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{14pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{9pt}}" + chr(10) for i, (a, b) in enumerate(WORKSHEET[:5], 1))}
\clearpage
\thispagestyle{{empty}}
\noindent{{\color{{blue}}\rule{{\linewidth}}{{3pt}}}}\par\vspace{{14pt}}
{"".join(rf"\noindent{{\bfseries {i}. {tex(a)}}} {{\color{{muted}}{tex(b)}}}\par\vspace{{9pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{14pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{14pt}}{{\color{{rulec}}\rule{{\linewidth}}{{0.3pt}}}}\par\vspace{{9pt}}" + chr(10) for i, (a, b) in enumerate(WORKSHEET[5:], 6))}
\vfill
\noindent{{\color{{muted}}\small Review date \rule{{1in}}{{0.3pt}}\qquad Independent reader \rule{{1.8in}}{{0.3pt}}\qquad Where the record is kept \rule{{1.6in}}{{0.3pt}}}}
\end{{document}}
"""

(OUT / "sample.tex").write_text(doc)
for _ in range(2):
    r = subprocess.run([str(XELATEX), "-interaction=nonstopmode", "-halt-on-error", "sample.tex"], cwd=OUT, capture_output=True, text=True)
if r.returncode:
    print(r.stdout[-3000:]); sys.exit("xelatex failed")
pages = re.search(r"Pages:\s+(\d+)", subprocess.check_output(["pdfinfo", str(OUT / "sample.pdf")], text=True)).group(1)
print(f"wrote {OUT / 'sample.pdf'} ({pages} pages)")
