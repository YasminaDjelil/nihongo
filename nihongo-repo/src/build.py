import re, html, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from figs import FIGS

# ---------------- kana -> Hepburn romaji ----------------
H = {}
rows = {
 '': 'あいうえお', 'k': 'かきくけこ', 's': 'さしすせそ', 't': 'たちつてと', 'n': 'なにぬねの',
 'h': 'はひふへほ', 'm': 'まみむめも', 'r': 'らりるれろ', 'g': 'がぎぐげご', 'z': 'ざじずぜぞ',
 'd': 'だぢづでど', 'b': 'ばびぶべぼ', 'p': 'ぱぴぷぺぽ'}
for c, ks in rows.items():
    for v, k in zip('aiueo', ks):
        H[k] = c + v
H.update({'し': 'shi', 'ち': 'chi', 'つ': 'tsu', 'ふ': 'fu', 'じ': 'ji', 'ぢ': 'ji', 'づ': 'zu',
          'や': 'ya', 'ゆ': 'yu', 'よ': 'yo', 'わ': 'wa', 'を': 'o', 'ん': 'n', 'ゐ': 'i', 'ゑ': 'e'})
SMALL = {'ゃ': 'ya', 'ゅ': 'yu', 'ょ': 'yo'}
SMALLV = {'ぁ': 'a', 'ぃ': 'i', 'ぅ': 'u', 'ぇ': 'e', 'ぉ': 'o'}

def to_hira(s):
    return ''.join(chr(ord(ch) - 0x60) if 'ァ' <= ch <= 'ヶ' else ch for ch in s)

def romaji(kana):
    s = to_hira(kana)
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        nxt = s[i + 1] if i + 1 < len(s) else ''
        if ch in H and nxt in SMALL:
            base = H[ch]
            if base in ('shi', 'chi', 'ji'):
                syl = base[:-1] + SMALL[nxt][1]
            else:
                syl = base[:-1] + SMALL[nxt]
            out.append(syl); i += 2; continue
        if ch in H and nxt in SMALLV:
            out.append(H[ch][:-1] + SMALLV[nxt]); i += 2; continue
        if ch == 'っ':
            out.append('\x01'); i += 1; continue
        if ch == 'ー':
            out.append('\x02'); i += 1; continue
        if ch in H:
            out.append(H[ch]); i += 1; continue
        out.append(ch); i += 1
    # resolve sokuon / long marks
    res = ''
    for k, p in enumerate(out):
        if p == '\x01':
            n = out[k + 1] if k + 1 < len(out) else ''
            res += ('t' if n.startswith('ch') else (n[:1] if n and n[0].isalpha() else ''))
        elif p == '\x02':
            res = res[:-1] + {'a': 'ā', 'i': 'ī', 'u': 'ū', 'e': 'ē', 'o': 'ō'}.get(res[-1:], res[-1:])
        else:
            if res.endswith('n') and out[k - 1] == 'n' and p[:1] in 'aiueoy':
                res += "'"
            res += p
    res = res.replace('ou', 'ō').replace('oo', 'ō').replace('uu', 'ū').replace('aa', 'ā')
    return res

FURI = {}
# ---------------- inline formatting ----------------
JRUN = re.compile(r'([々぀-ヿ㐀-鿿～〜～・ー（）]+(?:[぀-ヿ㐀-鿿。、？！]*))')

def inline(t, wrapj=True):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)', r'<i>\1</i>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    if wrapj:
        def rep(m):
            s = m.group(1)
            if not re.search(r'[぀-ヿ㐀-鿿]', s):
                return s
            return f'<span class="j" lang="ja">{s}</span>'
        t = JRUN.sub(rep, t)
    t = t.replace('-&gt;', '→')
    return t

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

# ---------------- generated blocks ----------------
GOJUON = [
 ('a', 'あいうえお', 'アイウエオ', ['a','i','u','e','o']),
 ('k', 'かきくけこ', 'カキクケコ', ['ka','ki','ku','ke','ko']),
 ('s', 'さしすせそ', 'サシスセソ', ['sa','shi','su','se','so']),
 ('t', 'たちつてと', 'タチツテト', ['ta','chi','tsu','te','to']),
 ('n', 'なにぬねの', 'ナニヌネノ', ['na','ni','nu','ne','no']),
 ('h', 'はひふへほ', 'ハヒフヘホ', ['ha','hi','fu','he','ho']),
 ('m', 'まみむめも', 'マミムメモ', ['ma','mi','mu','me','mo']),
 ('y', 'や・ゆ・よ', 'ヤ・ユ・ヨ', ['ya','','yu','','yo']),
 ('r', 'らりるれろ', 'ラリルレロ', ['ra','ri','ru','re','ro']),
 ('w', 'わ・・・を', 'ワ・・・ヲ', ['wa','','','','wo (o)']),
 ('n', 'ん・・・・', 'ン・・・・', ['n','','','','']),
]
DAKU = [
 ('g', 'がぎぐげご', 'ガギグゲゴ', ['ga','gi','gu','ge','go']),
 ('z', 'ざじずぜぞ', 'ザジズゼゾ', ['za','ji','zu','ze','zo']),
 ('d', 'だぢづでど', 'ダヂヅデド', ['da','ji','zu','de','do']),
 ('b', 'ばびぶべぼ', 'バビブベボ', ['ba','bi','bu','be','bo']),
 ('p', 'ぱぴぷぺぽ', 'パピプペポ', ['pa','pi','pu','pe','po']),
]
YOON_BASE = [('き','キ','k'),('ぎ','ギ','g'),('し','シ','sh'),('じ','ジ','j'),('ち','チ','ch'),('に','ニ','n'),
             ('ひ','ヒ','h'),('び','ビ','b'),('ぴ','ピ','p'),('み','ミ','m'),('り','リ','r')]

def kana_grid(kind, script):
    idx = 1 if script == 'hira' else 2
    cells = []
    if kind in ('basic', 'daku'):
        data = GOJUON if kind == 'basic' else DAKU
        # columns = consonant rows (read right-to-left traditionally; we go left-to-right), rows = vowels
        out = ['<div class="kgrid" style="--cols:%d">' % len(data)]
        for v in range(5):
            for row in data:
                ch = row[idx][v]
                ro = row[3][v]
                if ch == '・' or not ro:
                    out.append('<div class="kc empty"></div>')
                else:
                    out.append(f'<button class="kc" lang="ja" data-say="{ch}"><span class="kch">{ch}</span><span class="kro">{ro}</span></button>')
        out.append('</div>')
        return '\n'.join(out)
    if kind == 'yoon':
        out = ['<div class="kgrid" style="--cols:11">']
        for sm, sk, ro in [('ゃ','ャ','a'),('ゅ','ュ','u'),('ょ','ョ','o')]:
            for h_, k_, c in YOON_BASE:
                base = h_ if script == 'hira' else k_
                small = sm if script == 'hira' else sk
                r = (c + ro) if c in ('sh', 'j', 'ch') else (c + 'y' + ro)
                ch = base + small
                out.append(f'<button class="kc" lang="ja" data-say="{ch}"><span class="kch sm">{ch}</span><span class="kro">{r}</span></button>')
        out.append('</div>')
        return '\n'.join(out)

COUNTERS = [
 ('つ', 'general things', 'box',
  'ひとつ ふたつ みっつ よっつ いつつ むっつ ななつ やっつ ここのつ とお', {}),
 ('人', 'people', 'person',
  'ひとり ふたり さんにん よにん ごにん ろくにん しちにん/ななにん はちにん きゅうにん じゅうにん', {1,2,4}),
 ('匹', 'small animals', 'cat',
  'いっぴき にひき さんびき よんひき ごひき ろっぴき ななひき はっぴき きゅうひき じゅっぴき', {1,3,6,8,10}),
 ('頭', 'large animals', 'cow',
  'いっとう にとう さんとう よんとう ごとう ろくとう ななとう はっとう きゅうとう じゅっとう', {1,8,10}),
 ('本', 'long, thin objects', 'pencil',
  'いっぽん にほん さんぼん よんほん ごほん ろっぽん ななほん はっぽん きゅうほん じゅっぽん', {1,3,6,8,10}),
 ('冊', 'books, notebooks', 'book',
  'いっさつ にさつ さんさつ よんさつ ごさつ ろくさつ ななさつ はっさつ きゅうさつ じゅっさつ', {1,8,10}),
 ('枚', 'flat objects', 'sheet',
  'いちまい にまい さんまい よんまい ごまい ろくまい ななまい はちまい きゅうまい じゅうまい', set()),
 ('個', 'small objects', 'ball',
  'いっこ にこ さんこ よんこ ごこ ろっこ ななこ はっこ きゅうこ じゅっこ', {1,6,8,10}),
 ('台', 'machines, vehicles', 'car',
  'いちだい にだい さんだい よんだい ごだい ろくだい ななだい はちだい きゅうだい じゅうだい', set()),
 ('着', 'clothes', 'shirt',
  'いっちゃく にちゃく さんちゃく よんちゃく ごちゃく ろくちゃく ななちゃく はっちゃく きゅうちゃく じゅっちゃく', {1,8,10}),
 ('足', 'pairs of shoes / socks', 'sock',
  'いっそく にそく さんぞく よんそく ごそく ろくそく ななそく はっそく きゅうそく じゅっそく', {1,3,8,10}),
 ('杯', 'cups, glasses, bowls', 'cup',
  'いっぱい にはい さんばい よんはい ごはい ろっぱい ななはい はっぱい きゅうはい じゅっぱい', {1,3,6,8,10}),
 ('回', 'times (occurrences)', 'loop',
  'いっかい にかい さんかい よんかい ごかい ろっかい ななかい はっかい きゅうかい じゅっかい', {1,6,8,10}),
 ('階', 'floors of a building', 'building',
  'いっかい にかい さんがい よんかい ごかい ろっかい ななかい はっかい きゅうかい じゅっかい', {1,3,6,8,10}),
 ('歳', 'age (years old)', 'cake',
  'いっさい にさい さんさい よんさい ごさい ろくさい ななさい はっさい きゅうさい じゅっさい', {1,8,10}),
]
ICONS = {
 'box': '<rect x="6" y="10" width="28" height="22" rx="2"/><path d="M6 16h28" class="s-paper" stroke-width="2"/>',
 'person': '<circle cx="20" cy="11" r="6"/><rect x="11" y="19" width="18" height="16" rx="7"/>',
 'cat': '<ellipse cx="20" cy="26" rx="12" ry="8"/><circle cx="20" cy="14" r="7"/><path d="M13 12l1-8 5 5zM27 12l-1-8-5 5z"/>',
 'cow': '<rect x="6" y="14" width="26" height="14" rx="6"/><rect x="9" y="27" width="4" height="8"/><rect x="25" y="27" width="4" height="8"/><circle cx="33" cy="15" r="5"/>',
 'pencil': '<rect x="17" y="4" width="7" height="26" rx="1" transform="rotate(30 20 20)"/><path d="M8 34l2-7 5 3z"/>',
 'book': '<path d="M6 8h12a3 3 0 0 1 3 3v24a3 3 0 0 0-3-3H6zM34 8H24a3 3 0 0 0-3 3v24a3 3 0 0 1 3-3h10z"/>',
 'sheet': '<rect x="9" y="5" width="22" height="30" rx="2"/><path d="M13 13h14M13 19h14M13 25h9" class="s-paper" stroke-width="2"/>',
 'ball': '<circle cx="20" cy="22" r="11"/>',
 'car': '<rect x="4" y="18" width="32" height="10" rx="3"/><path d="M10 18l4-7h12l4 7z"/><circle cx="12" cy="30" r="4"/><circle cx="28" cy="30" r="4"/>',
 'shirt': '<path d="M14 6l-10 6 4 7 4-2v17h16V17l4 2 4-7-10-6c-1 3-3 5-6 5s-5-2-6-5z"/>',
 'sock': '<path d="M14 4h10v16l6 6a5 5 0 0 1-7 7l-9-9z"/>',
 'cup': '<path d="M9 10h20l-3 22H12z"/><path d="M29 14h4v8h-5" class="s-ink" fill="none" stroke-width="3"/>',
 'loop': '<path d="M30 20a10 10 0 1 1-4-8" fill="none" class="s-ink" stroke-width="4"/><path d="M24 5l6 6-8 3z"/>',
 'building': '<rect x="10" y="4" width="20" height="32"/><g class="f-paper"><rect x="14" y="8" width="4" height="4"/><rect x="22" y="8" width="4" height="4"/><rect x="14" y="16" width="4" height="4"/><rect x="22" y="16" width="4" height="4"/><rect x="14" y="24" width="4" height="4"/><rect x="22" y="24" width="4" height="4"/></g>',
 'cake': '<rect x="7" y="18" width="26" height="16" rx="2"/><rect x="18" y="8" width="4" height="9"/><path d="M20 3c3 3 0 5 0 5s-3-2 0-5z" class="f-acc"/>',
}

TR = {}
def L(x):
    return TR.get(x, x)

def fig(name):
    def r(m):
        t = m.group(1); st = t.strip()
        return '>' + (t.replace(st, html.escape(L(st), quote=False)) if st and st in TR else t) + '<'
    return re.sub(r'>([^<>]+)<', r, FIGS[name])

def counters_block():
    out = ['<div class="counters">']
    for k, label, icon, readings, irr in COUNTERS:
        rs = readings.split()
        items = []
        nums = '一二三四五六七八九十'
        for i, r in enumerate(rs, 1):
            cls = ' class="irr"' if i in irr else ''
            disp = r.replace('/', ' / ')
            kj = (nums[i - 1] + k) if k != 'つ' else (nums[i - 1] + ('つ' if i < 10 else ''))
            items.append(f'<li{cls}><span class="n">{i}</span><span class="j" lang="ja" data-say="{r.split("/")[0]}">{disp}</span></li>')
        out.append(f'''<div class="ctr"><div class="ctr-h"><svg viewBox="0 0 40 40" class="ico f-acc2" aria-hidden="true">{ICONS[icon]}</svg>
<div><span class="ctr-k j" lang="ja">〜{k}</span><span class="ctr-l">{L(label)}</span></div></div><ol>{''.join(items)}</ol></div>''')
    out.append('</div>')
    return '\n'.join(out)

# ---------------- parser ----------------
def build(lines):
    toc = []
    body = []
    state = {'mode': None, 'buf': [], 'lesson_open': False, 'part': None}
    exs, lis, qs, ans = [], [], [], []
    table = None

    def flush():
        nonlocal exs, lis, qs, ans, table
        if exs:
            body.append('<div class="exs">' + ''.join(exs) + '</div>'); exs = []
        if lis:
            body.append('<ul class="pts">' + ''.join(f'<li>{x}</li>' for x in lis) + '</ul>'); lis = []
        if qs:
            body.append('<ol class="qs">' + ''.join(f'<li>{x}</li>' for x in qs) + '</ol>'); qs = []
        if ans:
            body.append('<details class="ans"><summary>' + L('Show answers') + '</summary><ol>' + ''.join(f'<li>{x}</li>' for x in ans) + '</ol></details>'); ans = []
        if table:
            kind, title, head, rows_ = table
            if kind == 'vocab':
                h = '<thead><tr>' + ''.join(f'<th>{L(x)}</th>' for x in ('Kanji', 'Kana', 'Rōmaji', 'English')) + '<th class="ac"></th></tr></thead>'
                trs = []
                for r in rows_:
                    r = (r + ['', '', '', ''])[:4]
                    kj, kn, ro, en = r
                    if ro == '~' or ro == '':
                        ro = romaji(kn.split('/')[0].strip()) if kn else ''
                    say = kj or kn
                    trs.append(f'<tr data-v="{html.escape(kn + "|" + kj)}"><td class="kj" lang="ja"><span class="j" data-say="{html.escape(kn or kj)}">{html.escape(kj)}</span></td><td lang="ja">{html.escape(kn)}</td><td class="ro">{html.escape(ro)}</td><td class="mean"><span>{inline(en)}</span></td><td class="ac"><button class="addc" type="button" aria-pressed="false">＋</button></td></tr>')
                cap = f'<div class="tcap"><span>{inline(title) if title else L("Lesson vocabulary")}</span><span class="tbtns"><button class="mini addall" type="button" data-i="addall">Add all</button><button class="mini quizbtn" type="button">{L("Hide meanings")}</button></span></div>'
                body.append(f'<div class="vocab">{cap}<div class="tw"><table class="vt">{h}<tbody>{"".join(trs)}</tbody></table></div></div>')
            else:
                h = '<thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead>'
                trs = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows_)
                cap = f'<div class="tcap"><span>{inline(title)}</span></div>' if title else ''
                body.append(f'<div class="gtable">{cap}<div class="tw"><table>{h}<tbody>{trs}</tbody></table></div></div>')
            table = None

    def close_lesson():
        if state['lesson_open']:
            body.append('</section>')
            state['lesson_open'] = False

    chap_n = 0
    for _ in (0,):
        for raw in lines:
            line = raw.rstrip('\n')
            s = line.strip()
            if table is not None and s.startswith('- '):
                table[3].append([c.strip() for c in s[2:].split('|')]); continue
            if not s:
                flush(); continue
            if s.startswith('//'):
                continue
            if s.startswith('=part '):
                flush(); close_lesson()
                pid, label, title = [x.strip() for x in s[6:].split('|')]
                toc.append(('part', pid, label, title))
                body.append(f'<header class="part" id="{pid}"><span class="plabel">{label}</span><h1>{inline(title, False)}</h1></header>')
                continue
            if s.startswith('=lesson '):
                flush(); close_lesson()
                lid, label, title = [x.strip() for x in s[8:].split('|')]
                toc.append(('lesson', lid, label, title))
                chap_n = 0
                body.append(f'<section class="lesson" id="{lid}"><div class="lhead"><span class="lnum">{label}</span><h2>{inline(title)}</h2></div>')
                state['lesson_open'] = True
                continue
            if s.startswith('=== '):
                flush(); body.append(f'<h4>{inline(s[4:])}</h4>'); continue
            if s.startswith('== '):
                flush(); chap_n += 1
                body.append(f'<h3><span class="cn">{chap_n}</span><span>{inline(s[3:])}</span></h3>'); continue
            m = re.match(r'^(\w+):\s?(.*)$', s)
            key, val = (m.group(1), m.group(2)) if m and m.group(1) in (
                'ex', 'rule', 'note', 'warn', 'tip', 'li', 'vocab', 'table', 'fig', 'kana', 'counters', 'q', 'ans', 'raw', 'p', 'fix') else (None, s)
            if key != 'ex' and exs:
                body.append('<div class="exs">' + ''.join(exs) + '</div>'); exs = []
            if key != 'li' and lis:
                body.append('<ul class="pts">' + ''.join(f'<li>{x}</li>' for x in lis) + '</ul>'); lis = []
            if key == 'ex':
                parts = [x.strip() for x in val.split('|')]
                jp, ro, en = (parts + ['', '', ''])[:3]
                exs.append(f'<div class="ex"><p class="jp" lang="ja" data-say="{html.escape(jp)}">{FURI.get(jp) or html.escape(jp)}</p>' +
                           (f'<p class="ro">{inline(ro, False)}</p>' if ro else '') +
                           f'<p class="en">{inline(en, False)}</p></div>')
            elif key == 'rule':
                chips = [x.strip() for x in val.split(' + ')]
                inner = '<span class="plus">+</span>'.join(f'<span class="chip">{inline(c)}</span>' for c in chips)
                body.append(f'<div class="rule">{inner}</div>')
            elif key in ('note', 'warn', 'tip', 'fix'):
                lab = L({'note': 'Note', 'warn': 'Watch out', 'tip': 'Study tip', 'fix': 'Corrected'}[key])
                body.append(f'<aside class="call {key}"><b class="cl">{lab}</b><div>{inline(val)}</div></aside>')
            elif key == 'li':
                lis.append(inline(val))
            elif key == 'vocab':
                flush(); table = ['vocab', val, None, []]
            elif key == 'table':
                flush()
                title, _, head = val.partition('::')
                table = ['table', title.strip(), [c.strip() for c in head.split('|')], []]
            elif key == 'fig':
                name, _, cap = val.partition('|')
                body.append(f'<figure class="fig">{fig(name.strip())}' + (f'<figcaption>{inline(cap.strip())}</figcaption>' if cap.strip() else '') + '</figure>')
            elif key == 'kana':
                kind, script = val.split()
                body.append(kana_grid(kind, script))
            elif key == 'counters':
                body.append(counters_block())
            elif key == 'q':
                qs.append(inline(val))
            elif key == 'ans':
                if qs:
                    body.append('<ol class="qs">' + ''.join(f'<li>{x}</li>' for x in qs) + '</ol>'); qs = []
                ans.append(inline(val))
            elif key == 'raw':
                body.append(val)
            else:
                body.append(f'<p>{inline(val)}</p>')
        flush()
    close_lesson()
    return toc, '\n'.join(body)


def toc_html(toc):
    out = ['<nav class="toc" aria-label="Contents"><ol>']
    open_part = False
    for kind, i, label, title in toc:
        if kind == 'part':
            if open_part: out.append('</ol></li>')
            out.append(f'<li class="tp"><a href="#{i}">{label}</a><ol>')
            open_part = True
        else:
            t = re.sub(r'<[^>]+>', '', inline(title, False))
            item = f'<li><a href="#{i}"><span>{label}</span> {t}</a></li>'
            out.append(item if open_part else f'<li class="tpre"><ol>{item}</ol></li>')
    if open_part: out.append('</ol></li>')
    out.append('</ol></nav>')
    return '\n'.join(out)


if __name__ == '__main__':
    import json as _j, i18n
    d = os.path.dirname(os.path.abspath(__file__))
    src = []
    for f in i18n.FILES:
        src += open(os.path.join(d, f), encoding='utf-8').read().split('\n') + ['']
    import gloss
    import kanji as _kj
    import furi as _fu
    FURI.update(_fu.build_furi(src)[0])
    def _words(fn):
        rows = []
        for l in open(os.path.join(d, fn), encoding='utf-8'):
            p = l.rstrip('\n').split('|')
            if len(p) == 4: rows.append(p)
        return rows
    WJSON = _j.dumps({'n5': _words('words_n5.txt'), 'n4': _words('words_n4.txt')}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    import icons as _ic
    import icons2 as _ic2
    import icons3 as _ic3
    ICJSON = _ic.build_icons()[0]
    kvg = os.path.join(d, 'vendor', 'kanjivg')
    KJSON = _kj.build_kanji(d, kvg if os.path.isdir(kvg) else os.path.join(d, '..', 'kv', 'whl', 'kanji'))
    import re as _re
    gx = _j.load(open(os.path.join(d, 'gloss_extra.json'), encoding='utf-8')); GL = {}
    tpls = []
    for lang in ('en', 'fr', 'pt', 'ar'):
        TR.clear()
        if lang != 'en':
            tr, miss = i18n.load(lang); TR.update(tr)
        lines = i18n.walk(src, lambda x: TR.get(x, x))
        g = gloss.build_gloss(src, lines)
        for k, v in gx.items(): g[k] = {'m': v[lang], 'r': v.get('r', '')}
        g.pop('い', None)
        for k in list(g):
            mm = _re.fullmatch(r'(\d+)日', g[k]['m'])
            if mm: g[k]['m'] = {'en': 'day %s of the month', 'fr': 'le %s du mois', 'pt': 'dia %s do mês', 'ar': 'اليوم %s من الشهر'}[lang] % mm.group(1)
        GL[lang] = g
        toc, body = build(lines)
        tpls.append(f'<template id="tpl-{lang}"><div class="t-toc">{toc_html(toc)}</div><div class="t-body">{body}</div></template>')
    TR.clear()
    tpl = open(os.path.join(d, 'template.html'), encoding='utf-8').read()
    ui = _j.load(open(os.path.join(d, 'ui.json'), encoding='utf-8'))
    page = tpl.replace('%%TEMPLATES%%', '\n'.join(tpls)).replace('%%HERO%%', FIGS['hero']).replace('%%UI%%', _j.dumps(ui, ensure_ascii=False)).replace('%%GLOSS%%', _j.dumps(GL, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')).replace('%%KANJI%%', KJSON).replace('%%ICONS%%', ICJSON).replace('%%WORDS%%', WJSON)
    up = os.path.join(d, '..', 'userfile', 'audio.json'); ap = os.path.join(d, 'audio.json')
    voice = ''
    rp = os.path.join(d, '..', 'audio.json'); vp = os.path.join(d, 'voice.txt')
    if os.path.exists(up):
        u = _j.load(open(up)); aud = u['clips']; voice = u['voice']
    elif os.path.exists(rp):   # repository layout: the recorded clips sit next to index.html
        aud = _j.load(open(rp, encoding='utf-8')); voice = open(vp, encoding='utf-8').read().strip() if os.path.exists(vp) else ''
    else:
        aud = _j.load(open(ap)) if os.path.exists(ap) else {}
    attr = f' data-voice="{html.escape(voice)}"' if voice else ''
    page = page.replace('%%AUDIO%%', f'<script id="aud" type="application/json"{attr}>' + _j.dumps(aud, ensure_ascii=False).replace('</', '<\\/') + '</script>' if aud else '')
    out = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == 'hosted':
        # hosted variant: no document wrapper, audio in a side file, no print / cloud / own theme toggle
        os.makedirs(out, exist_ok=True)
        hp = tpl.replace('%%TEMPLATES%%', '\n'.join(tpls)).replace('%%HERO%%', FIGS['hero']).replace('%%UI%%', _j.dumps(ui, ensure_ascii=False)).replace('%%GLOSS%%', _j.dumps(GL, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')).replace('%%KANJI%%', KJSON).replace('%%ICONS%%', ICJSON).replace('%%WORDS%%', WJSON).replace('%%HOSTED%%', 'true')
        hp = hp.replace('%%AUDIO%%', f'<script id="aud" type="application/json"{attr} data-src="audio.json">{{}}</script>')
        head, rest = hp.split('<style>', 1)
        css, rest = rest.split('</style>', 1)
        bodyhtml = rest.split('<body>', 1)[1].rsplit('</body>', 1)[0]
        css += '''
#t-print,#t-cloud,#t-theme,.mrow.cloud,.keybox{display:none!important}
.bar{top:env(safe-area-inset-top,0px)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--paper)}
.bar-in,.wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
'''
        doc = '<title>Japanese N5–N4 Course</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n<style>' + css + '</style>\n' + bodyhtml
        open(os.path.join(out, 'course.html'), 'w', encoding='utf-8').write(doc)
        _j.dump(aud, open(os.path.join(out, 'audio.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        print('hosted', len(doc), os.path.getsize(os.path.join(out, 'audio.json')))
        sys.exit(0)
    if len(sys.argv) > 2 and sys.argv[2] == 'pwa':
        # installable web app: full document, audio in a side file, service worker for offline use
        os.makedirs(out, exist_ok=True)
        pp = tpl.replace('%%TEMPLATES%%', '\n'.join(tpls)).replace('%%HERO%%', FIGS['hero']).replace('%%UI%%', _j.dumps(ui, ensure_ascii=False)).replace('%%GLOSS%%', _j.dumps(GL, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')).replace('%%KANJI%%', KJSON).replace('%%ICONS%%', ICJSON).replace('%%WORDS%%', WJSON).replace('%%HOSTED%%', 'true')
        pp = pp.replace('%%AUDIO%%', f'<script id="aud" type="application/json"{attr} data-src="audio.json">{{}}</script>')
        pp = pp.replace('<meta name="viewport" content="width=device-width, initial-scale=1">', '''<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Nihongo">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#fbf8f2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#16181c" media="(prefers-color-scheme: dark)">''')
        pp = pp.replace('</style>', '''#t-print,#t-cloud,.mrow.cloud,.keybox{display:none!important}
.bar-in,.wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{padding-bottom:calc(80px + env(safe-area-inset-bottom,0px))}
html{-webkit-tap-highlight-color:transparent}
</style>''', 1)
        pp = pp.replace('</body>', '''<script>
if('serviceWorker' in navigator && (location.protocol==='https:'||location.hostname==='localhost')){
  window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){})});
}
</script>
</body>''')
        assert 'manifest.webmanifest' in pp and "register('sw.js')" in pp
        open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(pp)
        _j.dump(aud, open(os.path.join(out, 'audio.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        print('pwa', len(pp)); sys.exit(0)
    page = page.replace('%%HOSTED%%', 'false')
    open(out, 'w', encoding='utf-8').write(page)
    print('written', out, len(page))
