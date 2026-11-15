"""Build a glossary for Japanese words/patterns that appear in the lesson text but not in a vocabulary list.
Meanings are taken only from places where the course states them explicitly:
headings ("X — meaning"), reference tables, "X (romaji, meaning)" glosses and definition bullets."""
import re
J = r'[々぀-ヿ㐀-鿿～〜～・ー]+'
JRE = re.compile(J)
HASJ = re.compile(r'[぀-ヿ㐀-鿿]')
ROMA = re.compile(r"^[a-zA-Zāīūēōâîûêô'’\-/\s.…~]+$")
KANA = re.compile(r'^[぀-ヿー・\s/]+$')
JP_COLS = {'Kanji', 'Kana', 'Day'}

def md(t):
    t = re.sub(r'\*\*|\*|`', '', t or '')
    return re.sub(r'\s+', ' ', t).strip(' ,،;؛:：—–-/').strip()

def key(t):
    return re.sub(r'^[〜～]+', '', t.strip())

def toks(t):
    return [key(x) for x in JRE.findall(t) if HASJ.search(x)]

def first_sentence(t):
    t = re.split(r'(?<=[^\d])[.。!?؟](\s|$)', t, 1)[0]
    return md(t)

def build_gloss(en_lines, tr_lines, skip_after='=lesson about'):
    G = {}
    def put(k, m='', r='', p=1, force=False):
        k = key(k)
        if not k or len(k) > 24: return
        m = md(m); r = md(r)
        if len(m) > 130: m = ''
        if not m and not r: return
        g = G.setdefault(k, {'m': '', 'r': '', 'p': 0})
        if m:
            if p > g['p']: g['m'] = m; g['p'] = p
            elif p == g['p'] == 4 and m not in g['m'] and len(g['m']) + len(m) < 110: g['m'] += ' · ' + m
        if r and not g['r'] and r != k: g['r'] = r
    table = None
    for en, tr in zip(en_lines, tr_lines):
        e = en.strip(); t = tr.strip()
        if e.startswith(skip_after): break
        if not e: table = None; continue
        if table is not None and e.startswith('- '):
            kind, hen, htr = table
            if kind != 'table': continue
            ce = [c.strip() for c in e[2:].split('|')]; ct = [c.strip() for c in t[2:].split('|')]
            if len(ce) != len(ct): continue
            # split every cell into Japanese tokens and the remaining gloss text
            romtab = 'Things (general)' in hen or 'Verb' in hen
            info = []
            for j, c in enumerate(ct):
                tk = toks(c)
                rest = md(JRE.sub(' ', c).replace('(', ' ').replace(')', ' ').replace('（', ' ').replace('）', ' '))
                h = hen[j] if j < len(hen) else ''
                info.append((tk, rest, h, htr[j] if j < len(htr) else ''))
            # 1) cells that carry their own gloss: "いつか some day", "行く / 来る (go / come)"
            for tk, rest, h, ht in info:
                if tk and rest and re.search(r'[^\W\d_]|\d', rest) and not re.search(r'[→・、]', c) and not (ROMA.match(rest) and romtab):
                    parts = [p.strip() for p in rest.split(' / ')]
                    for i, k in enumerate(tk):
                        put(k, parts[i] if len(parts) == len(tk) and len(tk) > 1 else rest, p=3)
                    kan = [k for k in tk if not KANA.match(k)]; kn = [k for k in tk if KANA.match(k)]
                    if len(kan) == 1 and len(kn) == 1: put(kan[0], r=kn[0])
            # 2) known table shapes
            row_m = ''
            if 'English' in hen and hen[0] != 'English':
                row_m = ct[hen.index('English')]
            elif 'Value' in hen: row_m = ct[hen.index('Value')]
            elif hen and hen[0] in ('Number',): row_m = ct[0]
            elif hen and hen[0] in ('', 'Day', 'English'): row_m = md(ct[0])
            elif hen and hen[0].startswith('Plain verb'): row_m = info[0][1]
            if row_m:
                for j, (tk, rest, h, ht) in enumerate(info):
                    if not tk or (rest and not (ROMA.match(rest) and romtab)) or re.search(r'[→・、]', ct[j]): continue
                    if j == 0 and hen[0] in ('', 'English'): continue
                    if hen[0].startswith('Plain verb') and j == 0: continue
                    if h == 'Day' and j == 0: continue
                    extra = (' · ' + md(JRE.sub('', ht))) if (j > 0 and h and h not in JP_COLS and h not in ('Rōmaji',) and hen[0] in ('', 'English') or hen[0].startswith('Plain verb')) and md(JRE.sub('', ht)) else ''
                    kan = [k for k in tk if not KANA.match(k)]; kn = [k for k in tk if KANA.match(k)]
                    for k in tk: put(k, row_m + extra, p=2)
                    if len(kan) == 1 and len(kn) == 1: put(kan[0], r=kn[0])
                # reading from a Kana column for the Kanji column
                if 'Kanji' in hen and 'Kana' in hen:
                    a = toks(ct[hen.index('Kanji')]); b = ct[hen.index('Kana')]
                    if len(a) == 1 and b: put(a[0], r=b.split('/')[0].strip())
            continue
        if e.startswith('vocab:'): table = ('vocab', [], []); continue
        if e.startswith('table:'):
            he = [c.strip() for c in e.split('::', 1)[1].split('|')]; ht = [c.strip() for c in t.split('::', 1)[1].split('|')]
            table = ('table', he, ht); continue
        if e.startswith('=part') or e.startswith('=lesson') or re.match(r'^(ex|q|ans|fix|rule|fig|kana|counters|raw):', e): continue
        # headings: "X / Y — meaning"
        if t.startswith('== ') or t.startswith('=== '):
            body = t.split(' ', 1)[1]
            if '—' in body:
                left, right = body.split('—', 1)
                tk = toks(left); right = md(right)
                kan = [k for k in tk if not KANA.match(k)]
                # readings in parentheses: 前に (まえに)
                for m in re.finditer(r'(' + J + r')\s+\((' + J + r')\)', left):
                    put(m.group(1), r=m.group(2))
                parts = [p.strip() for p in right.split(' / ')]
                forms = [f for f in re.split(r'\s/\s', re.sub(r'\([^)]*\)', '', left)) if HASJ.search(f)]
                for i, f in enumerate(forms):
                    mm = parts[i] if len(parts) == len(forms) and len(forms) > 1 else right
                    for k in toks(f): put(k, mm, p=4)
                for m in re.finditer(r'\((' + J + r')\)', left):
                    for k in toks(m.group(1)): put(k, right, p=4)
            continue
        text = re.sub(r'^(li|note|warn|tip|p):\s?', '', t)
        is_li = e.startswith('li:')
        # definition bullets: "**得意** (とくい): good at something…", "これ / この (*kore / kono*): …"
        if is_li:
            m = re.match(r'^(\*{0,2})((?:' + J + r'|\s/\s)+)\*{0,2}\s*(?:\(([^()]*)\))?\s*([:：])?\s*(.+)$', text)
            if m and not (m.group(4) or m.group(1)): m = None
            if m: m = type('M', (), {'group': lambda self, i, _m=m: _m.group(i + 1)})()
            if m and HASJ.search(m.group(1)):
                rest = m.group(4)
                if not m.group(3): rest = rest.split(':')[0]
                mean = first_sentence(rest)
                par = md(m.group(2) or '')
                rd = par if (par and (ROMA.match(par) or KANA.match(par))) else ''
                forms = toks(m.group(1)); rds = [x.strip() for x in rd.split('/')] if rd else []
                if mean and not HASJ.search(mean[:3]):
                    for i, k in enumerate(forms): put(k, mean, rds[i] if len(rds) == len(forms) else '', p=2.5)
        # "X / Y / Z (a / b / c)" lists
        for m in re.finditer(r'((?:' + J + r')(?:\s/\s' + J + r')+)\s*\(([^()*]+)\)', text):
            f = toks(m.group(1)); p = [x.strip() for x in m.group(2).split(' / ')]
            if len(f) == len(p) and not any(HASJ.search(x) for x in p):
                for k, v in zip(f, p): put(k, v)
        # "X (*romaji*, meaning)" and "X (*romaji*)"
        for m in re.finditer(r'(' + J + r')\s*\(\*([^*()]+)\*(?:\s*[,،]\s*([^()]+))?\)', text):
            if ' / ' in m.group(2): continue
            put(m.group(1), m.group(3) or '', m.group(2))
        # "漢字 (かな, meaning)" and "漢字 (かな)"
        for m in re.finditer(r'(' + J + r')\s+\(([぀-ヿー]+)(?:\s*[,،]\s*([^()]+))?\)', text):
            put(m.group(1), m.group(3) or '', m.group(2))
    return {k: {'m': v['m'], 'r': v['r']} for k, v in G.items() if v['m']}
