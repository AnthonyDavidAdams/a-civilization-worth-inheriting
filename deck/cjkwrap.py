import re as _re
_CJK = _re.compile(r"[\u3000-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef]")
_NO_START = set("。，、；：？！）》」』”’…·—～﹑")      # may not begin a line
_NO_END = set("（《「『“‘")                            # may not end a line
def has_cjk(s): return bool(_CJK.search(s))
def cjk_tokens(s):
    """CJK characters one by one; Latin words, numbers and URLs as whole tokens."""
    return _re.findall(r"[A-Za-z0-9][A-Za-z0-9./:@%_\-]*|\s+|.", s)
def wrap_cjk(text, measure, width):
    lines, cur = [], ""
    for tok in cjk_tokens(text.replace("\n", "")):
        if tok.isspace():
            if cur: cur += " "
            continue
        if measure(cur + tok) <= width or not cur or (tok in _NO_START and len(tok) == 1):
            cur += tok
        else:
            if cur and cur[-1] in _NO_END:            # carry an opening bracket down with its text
                lines.append(cur[:-1]); cur = cur[-1] + tok
            else:
                lines.append(cur.rstrip()); cur = tok
    if cur: lines.append(cur.rstrip())
    return lines
