"""Have Astra (openai/gpt-6-astra via OpenRouter) write the workbook's exploration prompts.

One call per part: the part's nine chapters go in, a JSON object of four or five prompts per
pattern comes out, is validated (count, length, no em dashes, no stock AI phrasing) and
merged into workbook/prompts.json. Usage and cost are logged to workbook/build/astra-usage.log.
Stops on 402/429 rather than retrying into a wall.

  ~/.fal-venv/bin/python workbook/write_prompts.py            # all parts not yet written
  ~/.fal-venv/bin/python workbook/write_prompts.py 3 7        # just these parts
"""
import json, os, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WB = ROOT / "workbook"; (WB / "build").mkdir(exist_ok=True)
PROMPTS = WB / "prompts.json"; LOG = WB / "build" / "astra-usage.log"
MODEL = "openai/gpt-6-astra"
PRICE_IN, PRICE_OUT = 10 / 1e6, 50 / 1e6

key = next((l.split("=", 1)[1].strip().strip('"') for l in (Path.home() / "personality-bench/.env.local").read_text().splitlines()
            if l.startswith("OPENROUTER_API_KEY")), None)
assert key, "no OpenRouter key"

cards = json.load(open(ROOT / "deck/cards.json"))
existing = json.load(open(PROMPTS)) if PROMPTS.exists() else {}
EXEMPLARS = {k: existing[k] for k in ("1", "65") if k in existing}

BRIEF = """You are writing the exploration prompts for a workbook that accompanies "A Civilization Worth Inheriting: A Pattern Language for the Next Thousand Years" by Anthony David Adams. The book has 108 patterns. The workbook gives each pattern a two-page spread: on the left, the pattern in brief, its "first move" (quoted from the book), and four or five prompts for the reader to answer in writing; on the right, a blank page. Your job is the prompts.

Who answers them: a reader who has drawn this pattern's card, or who is facing a real decision in a household, company, neighborhood, school, watershed, institution, or project. They need help exploring the first move in their own place, not a summary of the pattern.

What a good prompt does
- Points at the reader's own situation. Second person. Concrete nouns: a budget line, a meeting, a river, a contract, a person.
- Draws on the chapter: its workable form, where it fails, the first move. Each set should carry the chapter's specific ideas, not generic reflection.
- Across the four or five prompts, cover different kinds of work: where this is already partly true here; who carries the cost or is missing from the room; what the chapter says goes wrong, and whether it is going wrong here; what would tell the reader in a month that it worked or failed; one small act with a date. Vary the order and wording from pattern to pattern. Do not follow a template.
- One sentence or two. At most 26 words per prompt. A question or an instruction, not both every time.
- Reading level: a good newspaper's front page. Short sentences. Everyday words. A twelve-year-old should follow every question without help. Prefer "money" to "funding", "fix" to "remediate", "the people it affects" to "stakeholders". No word a reader would need the book to define, except the pattern's own title.
- Do not restate the first move; it is printed directly above the prompts.

Hard rules
- No em dashes anywhere. No "not just X but Y". No "reflect on", "consider how", "think about", "take a moment", "dig deep", "journey", "unpack", "lean into", "at the end of the day". No weekday as a symbol for ordinary life. No bullet lists inside a prompt. No quotation marks around invented phrases.
- Do not invent facts, statistics, or named examples. Stay with what the chapter says and the reader's own place.
- American spelling.

Output: a JSON object whose keys are the pattern numbers as strings and whose values are arrays of four or five prompt strings. Nothing else.

Two sets written by the author as the register to match:
""" + json.dumps(EXEMPLARS, indent=1, ensure_ascii=False)

BAD = re.compile(r"—|–|\bnot just\b|\breflect on\b|\bconsider how\b|\bthink about\b|\btake a moment\b|\bdig deep|\bjourney\b|\bunpack\b|\blean into\b|\bat the end of the day\b|\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b", re.I)


def chapter_text(c):
    md = (ROOT / c["file"]).read_text()
    md = re.sub(r"^\*\*Connected patterns:\*\*.*$", "", md, flags=re.M)
    md = re.sub(r"\[S\d+\]", "", md)
    return md.strip()


def call(messages):
    body = json.dumps({"model": MODEL, "messages": messages, "temperature": 0.7,
                       "response_format": {"type": "json_object"}}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "HTTP-Referer": "https://anthonydavidadams.github.io/a-civilization-worth-inheriting/", "X-Title": "Pattern Workbook prompts"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code in (402, 429):
            sys.exit(f"HTTP {e.code} from OpenRouter: stopping, not retrying. {e.read()[:300]}")
        raise


def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w: return 0
    s = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee", "ye")): s -= 1
    return max(1, s)


def fk_grade(text):
    sents = max(1, len(re.findall(r"[.!?]+", text)))
    words = re.findall(r"[A-Za-z']+", text); n = max(1, len(words))
    return 0.39 * n / sents + 11.8 * sum(syllables(w) for w in words) / n - 15.59


def validate(part_cards, out):
    problems = []
    for c in part_cards:
        ps = out.get(str(c["n"]))
        if isinstance(ps, list) and ps:
            g = fk_grade(" ".join(str(p) for p in ps))
            if g > 9.5:
                problems.append(f"{c['n']}: reads at about grade {g:.0f}; use shorter sentences and everyday words (target grade 7)")
    for c in part_cards:
        ps = out.get(str(c["n"]))
        if not isinstance(ps, list) or not 4 <= len(ps) <= 5:
            problems.append(f"{c['n']}: {len(ps) if isinstance(ps, list) else 'missing'} prompts"); continue
        for p in ps:
            if not isinstance(p, str) or len(p.split()) > 28:
                problems.append(f"{c['n']}: too long: {str(p)[:60]}")
            m = BAD.search(p or "")
            if m:
                problems.append(f"{c['n']}: banned phrase '{m.group(0)}' in: {p[:60]}")
    return problems


def write_part(part):
    mine = [c for c in cards if c["part"] == part]
    chapters = "\n\n".join(f"=== PATTERN {c['n']}: {c['title']}\nSummary: {c['summary']}\n\n{chapter_text(c)}" for c in mine)
    user = (f"Part {mine[0]['part_roman']}: {mine[0]['part_name']}. Write the prompt sets for these nine patterns. "
            f"Return JSON with keys {', '.join(str(c['n']) for c in mine)}.\n\n{chapters}")
    messages = [{"role": "system", "content": BRIEF}, {"role": "user", "content": user}]
    for attempt in (1, 2):
        t0 = time.time()
        res = call(messages)
        u = res.get("usage", {}); cost = u.get("prompt_tokens", 0) * PRICE_IN + u.get("completion_tokens", 0) * PRICE_OUT
        text = res["choices"][0]["message"]["content"]
        try:
            out = json.loads(text)
        except json.JSONDecodeError:
            m = re.search(r"\{.*\}", text, re.S); out = json.loads(m.group(0)) if m else {}
        problems = validate(mine, out)
        with open(LOG, "a") as f:
            f.write(f"part {part} attempt {attempt}: {u.get('prompt_tokens')} in / {u.get('completion_tokens')} out, ${cost:.3f}, {time.time()-t0:.0f}s, {len(problems)} problems\n")
        if not problems:
            return out, cost
        # one revision pass, naming exactly what failed
        messages = messages + [{"role": "assistant", "content": text},
                               {"role": "user", "content": "Fix these and return the complete JSON again:\n" + "\n".join(problems)}]
    with open(LOG, "a") as f:
        f.write(f"part {part}: accepted with {len(problems)} remaining problems: {problems[:5]}\n")
    return out, cost


if __name__ == "__main__":
    wanted = [int(x) for x in sys.argv[1:]] or [p for p in range(1, 13)
              if not all(str(c["n"]) in existing and existing.get("_source", {}).get(str(c["n"])) == "astra" for c in cards if c["part"] == p)]
    total = 0.0
    for part in wanted:
        out, cost = write_part(part); total += cost
        existing = json.load(open(PROMPTS)) if PROMPTS.exists() else {}
        src = existing.get("_source", {})
        for k, v in out.items():
            if k.isdigit():
                existing[k] = v; src[k] = "astra"
        existing["_source"] = src
        PROMPTS.write_text(json.dumps(existing, indent=1, ensure_ascii=False) + "\n")
        print(f"part {part} written (${cost:.2f}); running total ${total:.2f}", flush=True)
    done = sum(1 for c in cards if str(c["n"]) in existing)
    print(f"done: {done}/108 patterns have prompts; this run ${total:.2f}")
