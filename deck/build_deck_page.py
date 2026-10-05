"""The standalone digital deck: docs/deck/index.html (+ its Open Graph image).

Shuffle the stack, draw a card, flip it, then follow its connected patterns from card to
card; the trail you walk is kept on the page and the current card is in the URL, so a card
can be shared. Built from deck/cards.json (text, parts, connections) and the web-size card
images make_deck.py already put in docs/assets/deck/.

  ~/.fal-venv/bin/python deck/build_deck_page.py            # English page
"""
import json, html, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "deck"))
from palette import PART_COLOURS  # noqa: E402

SITE = "https://anthonydavidadams.github.io/a-civilization-worth-inheriting"
cards = json.load(open(ROOT / "deck/cards.json"))
by = {c["n"]: c for c in cards}
parts = {}
for c in cards:
    parts.setdefault(c["part"], {"roman": c["part_roman"], "name": c["part_name"], "color": PART_COLOURS[c["part"]][1]})

data = [{"n": c["n"], "id": f"{c['n']:03d}", "t": c["title"], "p": c["part"], "s": c["summary"],
         "c": [m for m in c["connected"] if m in by]} for c in cards]
PARTS_JSON = json.dumps({k: v for k, v in sorted(parts.items())}, ensure_ascii=False)
DATA_JSON = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

# ---- Open Graph image: five fronts fanned on cream, title at left ---------------------------
def og_image(out: Path):
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), (243, 238, 227))
    d = ImageDraw.Draw(im)
    fonts = sorted((Path.home() / "Library/Fonts").glob("EBGaramond-Regular*.otf")) or \
            sorted(Path("/Library/Fonts").glob("*Garamond*.otf"))
    f_big = ImageFont.truetype(str(fonts[0]), 64) if fonts else ImageFont.load_default()
    f_small = ImageFont.truetype(str(fonts[0]), 26) if fonts else ImageFont.load_default()
    picks = [14, 32, 46, 64, 86]
    cw, ch = 262, 452
    for k, n in enumerate(picks):
        card = Image.open(ROOT / f"docs/assets/deck/{n:03d}-front.jpg").convert("RGB").resize((cw, ch), Image.LANCZOS)
        ang = (k - 2) * 7
        rot = card.rotate(ang, expand=True, resample=Image.BICUBIC, fillcolor=(243, 238, 227))
        mask = Image.new("L", card.size, 255).rotate(ang, expand=True, resample=Image.BICUBIC)
        x = 560 + k * 118 - rot.width // 2 + 130
        y = 330 - rot.height // 2 + abs(k - 2) * 14
        im.paste(rot, (x, y), mask)
    d.text((70, 200), "The Pattern Deck", font=f_big, fill=(2, 60, 167))
    d.text((72, 285), "108 patterns. Shuffle, draw, flip,", font=f_small, fill=(22, 28, 45))
    d.text((72, 320), "and follow the connections.", font=f_small, fill=(22, 28, 45))
    d.text((72, 390), "A Civilization Worth Inheriting", font=f_small, fill=(90, 96, 112))
    im.save(out, "JPEG", quality=88, optimize=True)

og_image(ROOT / "docs/assets/og-deck.jpg")

PAGE = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Pattern Deck</title>
<meta name="description" content="A digital deck of the 108 patterns from A Civilization Worth Inheriting. Shuffle the real cards, step through them, turn any card over, and follow its connected patterns.">
<link rel="canonical" href="{SITE}/deck/">
<link rel="alternate" hreflang="en" href="{SITE}/deck/">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="A Civilization Worth Inheriting">
<meta property="og:title" content="The Pattern Deck">
<meta property="og:description" content="108 patterns for a civilization worth inheriting. Shuffle, draw, flip, and follow the connections.">
<meta property="og:url" content="{SITE}/deck/">
<meta property="og:image" content="{SITE}/assets/og-deck.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="The Pattern Deck">
<meta name="twitter:description" content="108 patterns for a civilization worth inheriting. Shuffle, draw, flip, and follow the connections.">
<meta name="twitter:image" content="{SITE}/assets/og-deck.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Noto+Serif+SC:wght@400&display=swap" rel="stylesheet">
<style>
  :root{{ --cream:#F3EEE3; --ink:#161C2D; --muted:#5A6070; --blue:#023CA7; --rule:#D9D1C0; --panel:#FBF8F1; --shadow:rgba(0,0,0,.18); }}
  @media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{ --cream:#14161C; --ink:#EDE7DA; --muted:#A8AEBB; --blue:#7FA3F0; --rule:#2C3140; --panel:#1C1F27; --shadow:rgba(0,0,0,.5); }} }}
  :root[data-theme="dark"]{{ --cream:#14161C; --ink:#EDE7DA; --muted:#A8AEBB; --blue:#7FA3F0; --rule:#2C3140; --panel:#1C1F27; --shadow:rgba(0,0,0,.5); }}
  *{{box-sizing:border-box}}
  [hidden]{{display:none !important}}
  html{{-webkit-text-size-adjust:100%}}
  body{{margin:0;background:var(--cream);color:var(--ink);font-family:"EB Garamond",Georgia,"Times New Roman",serif;font-size:19px;line-height:1.5;min-height:100vh}}
  a{{color:var(--blue)}}
  .wrap{{max-width:1120px;margin:0 auto;padding:0 16px}}
  .topbar{{display:flex;justify-content:space-between;align-items:center;padding:14px 0 0;gap:12px}}
  .topbar .brand{{display:flex;align-items:center;gap:10px;color:var(--muted);font-size:15px;text-decoration:none}}
  .topbar .brand img{{width:26px;height:26px;border-radius:6px}}
  .langs{{display:inline-flex;border:1px solid var(--rule);border-radius:999px;overflow:hidden;font-size:15px}}
  .langs a{{padding:7px 16px;text-decoration:none;color:var(--blue)}}
  .langs a[aria-current="page"]{{background:var(--blue);color:#F3EEE3}}
  .langs a+a{{border-left:1px solid var(--rule)}}
  .langs a[lang="zh-Hans"]{{font-family:"Noto Serif SC","Songti SC",serif}}
  header{{padding:30px 0 6px;text-align:center}}
  .eyebrow{{font-variant:all-small-caps;letter-spacing:.14em;color:var(--blue);font-weight:500;margin:0 0 10px}}
  h1{{font-weight:400;font-size:clamp(34px,5vw,52px);line-height:1.08;margin:0 0 10px}}
  .lede{{color:var(--muted);max-width:640px;margin:0 auto}}
  .btn{{display:inline-block;padding:12px 20px;border-radius:8px;text-decoration:none;font-size:18px;border:1px solid var(--blue);background:transparent;color:var(--blue);font-family:inherit;cursor:pointer}}
  .btn.primary{{background:var(--blue);color:#F3EEE3}}
  .btn:disabled{{opacity:.45;cursor:default}}
  .btn.small{{padding:9px 14px;font-size:16px}}
  .actions{{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:18px 0 0}}
  /* the table: the deck on the left, what the top card says on the right */
  .table{{display:grid;grid-template-columns:minmax(280px,1fr) minmax(300px,1.1fr);gap:44px;align-items:start;padding:30px 0 10px}}
  .deckside{{display:flex;flex-direction:column;align-items:center}}
  .pile{{position:relative;width:min(100%,340px);aspect-ratio:600/1037;perspective:1400px;margin:14px auto 0;
         --r1:translate(2px,3px) rotate(.8deg); --r2:translate(-5px,5px) rotate(-1.8deg); --r3:translate(6px,8px) rotate(2.4deg)}}
  /* Stepping moves every card one slot: the under cards rise while the top card leaves,
     so the next card is already in the top position when the swap happens. */
  .under.to-top{{transform:none}} .under.to-1{{transform:var(--r1)}} .under.to-2{{transform:var(--r2)}} .under.to-3{{transform:var(--r3)}}
  .pile.noanim .under,.pile.noanim .card3d{{transition:none !important;animation:none !important}}
  .card3d.drop1{{animation:drop1 .5s cubic-bezier(.2,.7,.2,1) forwards}}
  @keyframes drop1{{to{{transform:var(--r1)}}}}
  .incoming{{position:absolute;inset:0;border-radius:16px;overflow:hidden;background:var(--panel);box-shadow:0 16px 38px var(--shadow);z-index:4;animation:comeBack .5s cubic-bezier(.2,.7,.2,1) both}}
  .incoming img{{width:100%;height:100%;object-fit:cover;display:block}}
  .under{{position:absolute;inset:0;border-radius:16px;overflow:hidden;box-shadow:0 10px 26px var(--shadow);background:var(--panel);transform:var(--rest);transition:transform .45s cubic-bezier(.2,.7,.2,1)}}
  .under img{{width:100%;height:100%;object-fit:cover;display:block}}
  .card3d{{position:absolute;inset:0;z-index:2;cursor:pointer;-webkit-transform-style:preserve-3d;transform-style:preserve-3d;transition:transform .7s cubic-bezier(.2,.7,.2,1);border-radius:16px;-webkit-tap-highlight-color:transparent;outline:none}}
  .card3d.flipped{{transform:rotateY(180deg)}}
  .card3d .face{{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;border-radius:16px;overflow:hidden;box-shadow:0 16px 38px var(--shadow);background:var(--panel)}}
  .card3d .face img{{width:100%;height:100%;object-fit:cover;display:block}}
  .card3d .back{{transform:rotateY(180deg)}}
  .card3d:focus-visible{{outline:3px solid var(--blue);outline-offset:6px}}
  /* step: the top card leaves to one side and the next one rises from the pile */
  .card3d.go-next{{animation:leaveLeft .45s cubic-bezier(.4,0,.8,.4) forwards}}
  .card3d.come-back{{animation:comeBack .5s cubic-bezier(.2,.7,.2,1)}}
  .card3d.arrive{{animation:arrive .5s cubic-bezier(.2,.7,.2,1)}}
  @keyframes leaveLeft{{to{{transform:translate(-70%,6%) rotate(-12deg);opacity:0}}}}
  @keyframes comeBack{{from{{transform:translate(-70%,6%) rotate(-12deg);opacity:0}} to{{transform:none;opacity:1}}}}
  @keyframes arrive{{from{{transform:translate(0,14px) scale(.97);opacity:.6}} to{{transform:none;opacity:1}}}}
  /* Riffle. A temporary layer of twenty real cards: 'split' fans them into two halves,
     'drop' lets them fall back into the middle one at a time, alternating sides (the
     --j delay), then the pile squares up and the new top card lifts off it. */
  .rlayer{{position:absolute;inset:0;pointer-events:none}}
  .rc{{position:absolute;inset:0;border-radius:16px;overflow:hidden;background:var(--panel);box-shadow:0 6px 18px var(--shadow);transform:translate(0,calc(var(--k) * -0.6px))}}
  .rc img{{width:100%;height:100%;object-fit:cover;display:block}}
  .rlayer.split .rc{{animation:split .42s cubic-bezier(.3,.7,.3,1) forwards;animation-delay:calc(var(--k) * 12ms)}}
  .rlayer.drop .rc{{animation:drop .46s cubic-bezier(.5,0,.6,1) both;animation-delay:calc(var(--j) * 38ms)}}
  @keyframes split{{
    to{{transform:translate(calc(var(--side) * 54%), calc(var(--k) * -1.4px - 3%)) rotate(calc(var(--side) * (7deg + var(--k) * 0.5deg)))}}
  }}
  @keyframes drop{{
    0%{{transform:translate(calc(var(--side) * 54%), calc(var(--k) * -1.4px - 3%)) rotate(calc(var(--side) * (7deg + var(--k) * 0.5deg)))}}
    55%{{transform:translate(calc(var(--side) * 10%), calc(var(--j) * -0.6px - 6%)) rotate(calc(var(--side) * 3deg))}}
    100%{{transform:translate(0,calc(var(--j) * -0.6px)) rotate(0)}}
  }}
  .pile.squaring .under,.pile.squaring .card3d{{animation:square .35s ease-out}}
  @keyframes square{{0%{{transform:translate(0,-6px) scale(1.015)}} 100%{{transform:var(--rest,none)}}}}
  .card3d.lift{{animation:lift .55s cubic-bezier(.2,.7,.2,1)}}
  @keyframes lift{{0%{{transform:translate(0,-2%) scale(1.04);box-shadow:none}} 100%{{transform:none}}}}
  .card3d.tuck{{animation:tuck .4s cubic-bezier(.4,0,.8,.4) forwards}}
  /* A connected pattern is pulled out of the deck: it slides out from under the pile to
     the side, comes over the top card, and lands on top. */
  .puller{{position:absolute;inset:0;border-radius:16px;overflow:hidden;background:var(--panel);box-shadow:0 16px 38px var(--shadow);z-index:0;animation:pullOut .85s cubic-bezier(.3,.6,.3,1) forwards}}
  .puller.over{{z-index:5}}
  .puller img{{width:100%;height:100%;object-fit:cover;display:block}}
  @keyframes pullOut{{
    0%{{transform:translate(0,6px) scale(.98)}}
    45%{{transform:translate(64%,-2%) rotate(9deg) scale(1)}}
    100%{{transform:none}}
  }}
  .card3d.settle{{animation:settle .4s ease-out .45s both}}
  @keyframes settle{{to{{transform:var(--r1)}}}}
  @keyframes tuck{{to{{transform:translate(0,10px) scale(.985);opacity:0}}}}
  .count{{color:var(--muted);font-size:15px;margin:12px 0 0;text-align:center}}
  .hint{{color:var(--muted);font-size:15px;margin:8px 0 0}}
  kbd{{font-family:inherit;border:1px solid var(--rule);border-radius:4px;padding:0 5px}}
  /* the reading side */
  .reading .part{{font-variant:all-small-caps;letter-spacing:.12em;font-size:16px;margin:0}}
  .reading h2{{font-weight:400;font-size:30px;margin:2px 0 6px;line-height:1.15}}
  .reading p.sum{{margin:0 0 6px;font-style:italic;font-size:21px}}
  /* The head keeps one height whether the title and summary take one line or two
     (longest title 36 characters, longest summary 85), so "Connected patterns"
     never moves between cards. */
  .reading .head{{min-height:222px}}
  .reading .connections{{margin:14px 0 0}}
  .reading .head,.reading .connections{{transition:opacity .28s ease,transform .28s ease}}
  .reading.changing .head,.reading.changing .connections{{opacity:0;transform:translateY(6px)}}
  .reading.changing .connections{{transition-delay:.04s}}
  .reading h3{{font-weight:400;font-size:21px;margin:0 0 8px}}
  .chips{{display:flex;flex-wrap:wrap;gap:10px}}
  .chip{{border:1px solid var(--rule);border-left:6px solid var(--acc,#999);background:var(--panel);color:var(--ink);border-radius:10px;padding:8px 12px;font:inherit;font-size:17px;cursor:pointer;text-align:left}}
  .chip:hover{{border-color:var(--blue)}}
  .chip small{{color:var(--muted);margin-right:6px}}
  footer{{border-top:1px solid var(--rule);margin-top:40px;padding:26px 0 48px;color:var(--muted);font-size:16px}}
  footer p{{margin:6px 0}}
  @media (max-width:760px){{ .table{{grid-template-columns:1fr;gap:26px}} .pile{{width:min(100%,300px)}} body{{font-size:18px}} .reading{{text-align:center}} .reading .head{{min-height:250px}} .chips{{justify-content:center}} }}
  @media (prefers-reduced-motion: reduce){{ .card3d,.under,.rc,.reading .head,.reading .connections{{transition:none;animation:none !important}} }}
</style>
</head>
<body>
<div class="wrap">
  <nav class="topbar" aria-label="Site">
    <a class="brand" href="../"><img src="../favicon.svg" alt="" width="26" height="26">A Civilization Worth Inheriting</a>
    <span class="langs"><a href="./" lang="en" aria-current="page">English</a><a href="../zh/" lang="zh-Hans" hreflang="zh-Hans">中文</a></span>
  </nav>
  <header>
    <p class="eyebrow">The Pattern Deck</p>
    <h1>Shuffle the deck</h1>
    <p class="lede">The 108 patterns as cards. Shuffle them, step through, turn any card over to read it, and follow its connections to the next.</p>
  </header>

  <section class="table" id="table">
    <div class="deckside">
      <div class="pile" id="pile">
        <div class="under" id="u3" style="--rest:var(--r3)"><img id="u3img" src="" alt="" width="600" height="1037"></div>
        <div class="under" id="u2" style="--rest:var(--r2)"><img id="u2img" src="" alt="" width="600" height="1037"></div>
        <div class="under" id="u1" style="--rest:var(--r1)"><img id="u1img" src="" alt="" width="600" height="1037"></div>
        <div class="card3d" id="card" role="button" tabindex="0" aria-label="Turn the top card over" aria-pressed="false">
          <span class="face front"><img id="cardFront" src="" width="600" height="1037" alt=""></span>
          <span class="face back"><img id="cardBack" src="" width="600" height="1037" alt=""></span>
        </div>
        <div class="rlayer" id="rlayer" aria-hidden="true" hidden></div>
      </div>
      <div class="actions">
        <button class="btn small" id="prevBtn" type="button" aria-label="Previous card">&larr; Previous</button>
        <button class="btn small" id="flipBtn" type="button">Turn it over</button>
        <button class="btn small" id="nextBtn" type="button" aria-label="Next card">Next &rarr;</button>
      </div>
      <div class="actions" style="margin-top:10px">
        <button class="btn primary" id="shuffleBtn" type="button">Shuffle</button>
        <a class="btn" id="shareLink" href="#">Link to this card</a>
      </div>
      <p class="count" id="count"></p>
      <p class="hint" style="text-align:center"><kbd>&larr;</kbd> <kbd>&rarr;</kbd> step · <kbd>space</kbd> turns it over · <kbd>s</kbd> shuffles</p>
    </div>

    <div class="reading">
      <div class="head">
        <p class="part" id="partLabel"></p>
        <h2 id="cardTitle"></h2>
        <p class="sum" id="cardSummary"></p>
        <p class="hint">The picture side names the pattern; the other side gives it in brief, with a first move. Tap the card to turn it.</p>
      </div>
      <div class="connections">
        <h3>Connected patterns</h3>
        <p class="hint" style="margin:0 0 10px">The patterns this card leans on. Pick one and it comes to the top of the deck.</p>
        <div class="chips" id="chips"></div>
      </div>
    </div>
  </section>
</div>

<footer>
  <div class="wrap">
    <p>These are the 108 patterns of <a href="../">A Civilization Worth Inheriting</a>. The printed deck has a picture on every front and the pattern in brief on the back; the book has the whole argument. <a href="https://civilization.galley.so">Talk with the book</a> if a card raises a question.</p>
    <p><strong>by <a href="https://earthpilot.ai">EarthPilot</a></strong> · built in the open at the <a href="https://earthpilot.ai/playground">Singularity Playground</a>. Text CC BY-NC-SA 4.0 · Copyright © 2026 Anthony David Adams. Some rights reserved.</p>
  </div>
</footer>

<script>
(function(){{
  var PARTS = {PARTS_JSON};
  var CARDS = {DATA_JSON};
  var byN = {{}}; CARDS.forEach(function(c){{ byN[c.n] = c; }});
  var IMG = '../assets/deck/';
  var $ = function(id){{ return document.getElementById(id); }};
  var card = $('card'), front = $('cardFront'), back = $('cardBack'), pile = $('pile');
  var unders = [$('u1img'), $('u2img'), $('u3img')];
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var order = [], pos = 0, busy = false;

  function newOrder(){{
    order = CARDS.map(function(c){{ return c.n; }});
    for (var i = order.length - 1; i > 0; i--) {{ var j = Math.floor(Math.random() * (i + 1)); var t = order[i]; order[i] = order[j]; order[j] = t; }}
  }}
  function src(n){{ return IMG + byN[n].id + '-front.jpg'; }}
  function setHash(n){{ if (history.replaceState) history.replaceState(null, '', '#' + n); else location.hash = String(n); }}
  var reading = document.querySelector('.reading'), fadeTimer = null;
  function render(){{
    paintCards();                       // pictures change at the hand-off, instantly
    if (reduced) {{ paintText(); return; }}
    // The words fade out, change while invisible, and fade back in.
    reading.classList.add('changing');
    clearTimeout(fadeTimer);
    fadeTimer = setTimeout(function(){{ paintText(); reading.classList.remove('changing'); }}, 290);
  }}
  function paintCards(){{
    var n = order[pos], c = byN[n];
    front.src = src(n); back.src = IMG + c.id + '-back.jpg';
    front.alt = 'Front of card ' + c.n + ', ' + c.t; back.alt = 'Back of card ' + c.n + ': ' + c.s;
    for (var k = 0; k < 3; k++) {{
      var m = order[(pos + 1 + k) % order.length];
      unders[k].src = src(m); unders[k].parentNode.style.visibility = order.length > k + 1 ? 'visible' : 'hidden';
    }}
    $('shareLink').href = '#' + c.n;
    document.title = c.n + ' · ' + c.t + ' · The Pattern Deck';
    new Image().src = src(order[(pos - 1 + order.length) % order.length]);
    setHash(n);
  }}
  function paintText(){{
    var n = order[pos], c = byN[n];
    var p = PARTS[c.p];
    $('partLabel').textContent = 'Part ' + p.roman + ' · ' + p.name; $('partLabel').style.color = p.color;
    $('cardTitle').textContent = c.n + ' · ' + c.t;
    $('cardSummary').textContent = c.s;
    $('count').textContent = 'Card ' + (pos + 1) + ' of ' + order.length + ' in this shuffle';
    var chips = $('chips'); chips.innerHTML = '';
    c.c.forEach(function(m){{
      var k = byN[m]; if (!k) return;
      var b = document.createElement('button'); b.type = 'button'; b.className = 'chip';
      b.style.setProperty('--acc', PARTS[k.p].color);
      b.innerHTML = '<small>' + k.n + '</small>' + k.t; b.title = k.s;
      b.addEventListener('click', function(){{ jump(m); }});
      chips.appendChild(b);
      new Image().src = src(m);
    }});
  }}
  // Never hard-reset a turned card: if it is showing its back, turn it face up first
  // (the normal flip transition), then carry on.
  function faceUp(then){{
    if (!card.classList.contains('flipped') || reduced) {{ card.classList.remove('flipped'); card.setAttribute('aria-pressed', 'false'); then(); return; }}
    card.classList.remove('flipped'); card.setAttribute('aria-pressed', 'false');
    setTimeout(then, 720);
  }}
  function step(dir){{
    if (busy) return;
    busy = true;
    faceUp(function(){{ stepNow(dir); }});
  }}
  var underEls = [$('u1'), $('u2'), $('u3')];
  // Swap the top card's picture only once it is decoded, so nothing flashes.
  function ready(n, then){{
    // Wait for the picture to decode, but never longer than the leave animation:
    // a hidden tab can defer decoding, and the deck must not lock up waiting.
    var im = new Image(), done = false; im.src = src(n);
    var go = function(){{ if (done) return; done = true; then(); }};
    if (im.decode) im.decode().then(go, go); else if (im.complete) go(); else {{ im.onload = go; im.onerror = go; }}
    setTimeout(go, 400);
  }}
  // Put every element back on its slot with no motion, then repaint the pile.
  function resetSlots(){{
    pile.classList.add('noanim');
    underEls.forEach(function(u){{ u.classList.remove('to-top', 'to-1', 'to-2', 'to-3'); }});
    card.classList.remove('go-next', 'drop1', 'settle', 'arrive', 'come-back', 'lift');
    void pile.offsetWidth;
    setTimeout(function(){{ pile.classList.remove('noanim'); }}, 30);
  }}
  function stepNow(dir){{
    if (reduced) {{ pos = (pos + dir + order.length) % order.length; render(); busy = false; return; }}
    if (dir > 0) {{
      // Next: the top card leaves left while the pile rises one slot; when the swap
      // comes, the next card is already sitting in the top position.
      var n = order[(pos + 1) % order.length];
      card.classList.add('go-next');
      underEls[0].classList.add('to-top'); underEls[1].classList.add('to-1'); underEls[2].classList.add('to-2');
      ready(n, function(){{
        setTimeout(function(){{
          pos = (pos + 1) % order.length;
          resetSlots(); render(); busy = false;
        }}, 450);
      }});
      return;
    }}
    // Previous: the earlier card slides back in over the top while the current top
    // eases down into the first slot and the pile drops one slot.
    var m = order[(pos - 1 + order.length) % order.length];
    var inc = document.createElement('div'); inc.className = 'incoming';
    var im = document.createElement('img'); im.src = src(m); im.alt = ''; im.width = 600; im.height = 1037; inc.appendChild(im);
    ready(m, function(){{
      pile.appendChild(inc);
      card.classList.add('drop1');
      underEls[0].classList.add('to-2'); underEls[1].classList.add('to-3');
      setTimeout(function(){{
        pos = (pos - 1 + order.length) % order.length;
        resetSlots(); render(); inc.remove(); busy = false;
      }}, 520);
    }});
  }}
  function jump(n){{
    if (busy) return;
    var i = order.indexOf(n); if (i < 0 || i === pos) return;
    busy = true;
    faceUp(function(){{ jumpNow(n, i); }});
  }}
  function jumpNow(n, i){{
    // Pull the card out of the deck and put it on top of where we are: Next goes on
    // from it, Previous returns to the card we came from.
    var place = function(){{
      order.splice(i, 1); if (i < pos) pos -= 1;        // take it out of the deck
      order.splice(pos + 1, 0, n); pos += 1; render();  // lay it on top of the card we were on
    }};
    if (reduced) {{ place(); busy = false; return; }}
    var pull = document.createElement('div'); pull.className = 'puller';
    var im = document.createElement('img'); im.src = src(n); im.alt = ''; im.width = 600; im.height = 1037; pull.appendChild(im);
    pile.insertBefore(pull, card);                      // behind the top card to start
    card.classList.remove('arrive', 'come-back', 'lift');
    card.classList.add('settle');
    underEls[0].classList.add('to-2'); underEls[1].classList.add('to-3');                       // the old top card eases back as the new one lands
    setTimeout(function(){{ pull.classList.add('over'); }}, 380);   // past the edge: now it crosses over the top
    setTimeout(function(){{
      resetSlots(); place(); pull.remove(); busy = false;
    }}, 880);
  }}
  var N_RIFFLE = 20;
  function shuffle(){{
    if (busy) return;
    busy = true;
    faceUp(shuffleNow);
  }}
  function shuffleNow(){{
    newOrder(); pos = 0;
    if (reduced) {{ render(); busy = false; return; }}
    var layer = $('rlayer');
    layer.innerHTML = '';
    // Build the layer from the NEW order so the card that ends on top is the one you
    // then see: drop index j lands j-th from the bottom, so j = N-1 is the top card.
    for (var j = 0; j < N_RIFFLE; j++) {{
      var d = document.createElement('div'); d.className = 'rc';
      d.style.setProperty('--j', j); d.style.setProperty('--k', Math.floor(j / 2)); d.style.setProperty('--side', j % 2 ? 1 : -1);
      d.style.zIndex = j;
      var im = document.createElement('img'); im.src = src(order[(N_RIFFLE - 1 - j) % order.length]); im.alt = ''; im.width = 600; im.height = 1037;
      d.appendChild(im); layer.appendChild(d);
    }}
    // 1. the top card tucks into the pile and the layer takes over
    card.classList.remove('arrive', 'lift'); card.classList.add('tuck');
    setTimeout(function(){{
      layer.hidden = false; card.style.visibility = 'hidden'; card.classList.remove('tuck');
      layer.classList.add('split');                                   // 2. two halves
      setTimeout(function(){{
        layer.classList.remove('split'); layer.classList.add('drop'); // 3. interleave
        var total = 460 + (N_RIFFLE - 1) * 38;
        setTimeout(function(){{
          resetSlots(); render();                                     // 4. square up, new top card lifts
          card.style.visibility = ''; layer.hidden = true; layer.classList.remove('drop'); layer.innerHTML = '';
          pile.classList.add('squaring'); card.classList.add('lift');
          setTimeout(function(){{ pile.classList.remove('squaring'); card.classList.remove('lift'); busy = false; }}, 560);
        }}, total + 60);
      }}, 520);
    }}, 380);
  }}
  function flip(){{ var f = card.classList.toggle('flipped'); card.setAttribute('aria-pressed', f ? 'true' : 'false'); }}

  card.addEventListener('click', flip);
  card.addEventListener('keydown', function(e){{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); flip(); }} }});
  $('flipBtn').addEventListener('click', flip);
  $('nextBtn').addEventListener('click', function(){{ step(1); }});
  $('prevBtn').addEventListener('click', function(){{ step(-1); }});
  $('shuffleBtn').addEventListener('click', shuffle);
  document.addEventListener('keydown', function(e){{
    if (e.target && /INPUT|TEXTAREA/.test(e.target.tagName)) return;
    if (e.key === 'ArrowRight') step(1);
    else if (e.key === 'ArrowLeft') step(-1);
    else if (e.key === 's' || e.key === 'S') shuffle();
    else if ((e.key === ' ' || e.key === 'f' || e.key === 'F') && document.activeElement !== card) {{ e.preventDefault(); flip(); }}
  }});
  window.addEventListener('hashchange', function(){{ var n = parseInt(location.hash.slice(1), 10); if (byN[n] && n !== order[pos]) jump(n); }});

  newOrder();
  var start = parseInt(location.hash.slice(1), 10);
  if (byN[start]) {{ var i = order.indexOf(start); order.splice(i, 1); order.unshift(start); }}
  paintCards(); paintText();
}})();
</script>
</body>
</html>
"""

out = ROOT / "docs/deck/index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(PAGE)
print(f"wrote {out.relative_to(ROOT)} ({len(PAGE)//1024} KB) and docs/assets/og-deck.jpg")
