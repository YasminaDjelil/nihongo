import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
D = os.path.dirname(os.path.abspath(__file__))
FILES = ['intro.txt', 'n5a.txt', 'n5b.txt', 'n4a.txt', 'n4b.txt', 'n4c.txt']
LAT = re.compile(r'[A-Za-z]{2,}')
SKIPCOL = {'Rōmaji', 'Kana', 'Kanji', 'Day', 'Number', 'Value'}
KEYS = ('ex', 'rule', 'note', 'warn', 'tip', 'li', 'vocab', 'table', 'fig', 'kana', 'counters', 'q', 'ans', 'raw', 'p', 'fix')
EXTRA = ['Note', 'Watch out', 'Study tip', 'Corrected', 'Show answers', 'Lesson vocabulary', 'Hide meanings', 'Show meanings',
         'Kanji', 'Kana', 'Rōmaji', 'English',
         'general things', 'people', 'small animals', 'large animals', 'long, thin objects', 'books, notebooks', 'flat objects',
         'small objects', 'machines, vehicles', 'clothes', 'pairs of shoes / socks', 'cups, glasses, bowls', 'times (occurrences)',
         'floors of a building', 'age (years old)']

def walk(lines, f):
    """Yield each DSL line with its translatable pieces passed through f."""
    out = []; table = None
    for raw in lines:
        line = raw.rstrip('\n'); s = line.strip()
        def t(x):
            x2 = x.strip()
            return f(x2) if x2 and LAT.search(x2) else x2
        if table is not None and s.startswith('- '):
            cells = [c.strip() for c in s[2:].split('|')]
            if table[0] == 'vocab':
                if len(cells) >= 4: cells[3] = t(cells[3])
            else:
                cells = [c if (i < len(table[1]) and table[1][i] in SKIPCOL) else t(c) for i, c in enumerate(cells)]
            out.append('- ' + ' | '.join(cells)); continue
        if not s: table = None; out.append(''); continue
        if s.startswith('//'): out.append(s); continue
        if s.startswith('=part ') or s.startswith('=lesson '):
            head, rest = s.split(' ', 1); a, b, c = [x.strip() for x in rest.split('|')]
            out.append(f'{head} {a} | {t(b)} | {t(c)}'); continue
        if s.startswith('=== '): out.append('=== ' + t(s[4:])); continue
        if s.startswith('== '): out.append('== ' + t(s[3:])); continue
        m = re.match(r'^(\w+):\s?(.*)$', s)
        key, val = (m.group(1), m.group(2)) if m and m.group(1) in KEYS else (None, s)
        if key == 'ex':
            p = [x.strip() for x in val.split('|')]; p = (p + ['', '', ''])[:3]; p[2] = t(p[2])
            out.append('ex: ' + ' | '.join(p))
        elif key == 'vocab':
            table = ['vocab', None]; out.append('vocab: ' + (t(val) if val.strip() else ''))
        elif key == 'table':
            title, _, head = val.partition('::'); heads = [c.strip() for c in head.split('|')]
            table = ['table', heads]
            out.append('table: ' + (t(title) if title.strip() else '') + ' :: ' + ' | '.join(h if h in SKIPCOL and h in ('Rōmaji','Kana','Kanji') and False else t(h) for h in heads))
        elif key == 'fig':
            name, _, cap = val.partition('|'); out.append('fig: ' + name.strip() + (' | ' + t(cap) if cap.strip() else ''))
        elif key in ('kana', 'counters', 'raw'): out.append(s)
        elif key: out.append(f'{key}: {t(val)}')
        else: out.append(t(val))
    return out

def fig_strings():
    from figs import FIGS
    res = []
    for name, svg in FIGS.items():
        for m in re.finditer(r'>([^<>]+)<', svg):
            x = m.group(1).strip()
            if LAT.search(x): res.append(x)
    return res

def collect():
    seen = {}
    def f(x): seen.setdefault(x, len(seen)); return x
    for fn in FILES: walk(open(os.path.join(D, fn), encoding='utf-8'), f)
    for x in fig_strings() + EXTRA: f(x)
    return list(seen)

def load(lang):
    import json
    tr = json.load(open(os.path.join(D, f'tr_{lang}.json'), encoding='utf-8'))
    return tr, [x for x in collect() if x not in tr]

if __name__ == '__main__':
    S = collect()
    with open(os.path.join(D, 'strings.txt'), 'w', encoding='utf-8') as o:
        for i, s in enumerate(S): o.write(f'{i}\t{s}\n')
    print(len(S), sum(len(s) for s in S))
