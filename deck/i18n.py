"""Language-specific strings, fonts and parsing rules for the deck and the extractor."""
F = "/Users/anthony/Library/Fonts/"

LANGS = {
    "en": {
        "root": ".", "deck_dir": "deck", "book_yaml": "book.yaml",
        "fonts": {"Regular": F + "EBGaramond-Regular.otf", "Italic": F + "EBGaramond-Italic.otf",
                  "Medium": F + "EBGaramond-Medium.otf", "SemiBold": F + "EBGaramond-SemiBold.otf"},
        "cjk": False,
        "part_label": lambda roman, name, cn: f"PART {roman}  ·  {name.upper()}",
        "first_move": "A FIRST MOVE", "connected": "CONNECTED PATTERNS",
        "patterns_range": lambda a, b: f"PATTERNS {a} TO {b}", "part_word": lambda roman, cn: f"PART {roman}",
        "deck_tag": "THE PATTERN DECK  ·  108 PATTERNS", "using": "USING THE CARDS",
        "steps": ["Read the front for the picture and the name.", "Turn it over for the pattern in brief and a first move.",
                  "Follow the connected patterns to the next card."],
        "talk": "Talk with the book", "scan": "Scan to ask the coach about any pattern. civilization.galley.so",
        "credit": "From the book by Anthony David Adams. Text CC BY-NC-SA 4.0.",
        "title_lines": ["A Civilization", "Worth Inheriting"], "subtitle_lines": ["A Pattern Language", "for the Next Thousand Years"],
        # extractor
        "glance_re": r"^(\d+)\. \*\*([^*]+)\*\* — (.+)$", "first_move_re": r"## (?:A first move|Begin with one decision)\s+(.+?)(?:\n\n|\Z)",
        "connected_re": r"\*\*Connected patterns:\*\*\s*(.+)", "connected_num_re": r"\((\d+)\)", "statement_prefix": "Therefore",
        "pattern_section_re": r"## The pattern\s+\*\*(.+?)\*\*", "connect_section": "## How the patterns connect",
        "connect_prose_re": r"\*\*[^*]+\((\d+)\)\*\*",
    },
    "zh": {
        "root": "zh", "deck_dir": "zh/deck", "book_yaml": "zh/book.yaml",
        "fonts": {"Regular": F + "NotoSerifCJKsc-Regular.otf", "Italic": F + "LXGWWenKai-Regular.ttf",
                  "Medium": F + "NotoSerifCJKsc-Bold.otf", "SemiBold": F + "NotoSerifCJKsc-Bold.otf"},
        "cjk": True,
        "part_label": lambda roman, name, cn: f"{cn}  ·  {name}",
        "first_move": "第一步", "connected": "相关模式",
        "patterns_range": lambda a, b: f"模式 {a} 至 {b}", "part_word": lambda roman, cn: cn,
        "deck_tag": "模式牌  ·  108 个模式", "using": "使用说明",
        "steps": ["正面是图画和模式的名称。", "翻过来是模式的要点和第一步。", "沿着相关模式，找到下一张牌。"],
        "talk": "与本书对话", "scan": "扫描二维码，向教练询问任何一个模式。civilization.galley.so",
        "credit": "出自安东尼·大卫·亚当斯的同名著作。文本采用 CC BY-NC-SA 4.0 授权。",
        "title_lines": ["值得继承的文明"], "subtitle_lines": ["下一个千年的模式语言"],
        "glance_re": r"^(\d+)\. \*\*([^*]+)\*\* —— (.+)$", "first_move_re": r"## (?:第一步|从一个决定开始)\s+(.+?)(?:\n\n|\Z)",
        "connected_re": r"\*\*相关模式：\*\*\s*(.+)", "connected_num_re": r"（(\d+)）", "statement_prefix": "因此",
        "pattern_section_re": r"## 模式\s+\*\*(.+?)\*\*", "connect_section": "## 这些模式如何相连",
        "connect_prose_re": r"\*\*[^*]+（(\d+)）\*\*",
    },
}
CN_NUM = ["一","二","三","四","五","六","七","八","九","十","十一","十二"]
def part_cn(n): return f"第{CN_NUM[n-1]}部分"

def pick(argv):
    if "--lang" in argv:
        return LANGS[argv[argv.index("--lang") + 1]]
    return LANGS["en"]
