# Furigana for example sentences, derived from each sentence's own reading line (kana or rōmaji) so it never
# contradicts the course. A sentence whose reading cannot be aligned with its text gets no furigana.
import re, html, unicodedata
KANJI = r'々〆ヶ㐀-鿿'
def is_kanji(c): return bool(re.match('[' + KANJI + ']', c))
def is_kana(c): return '぀' <= c <= 'ヿ'
def hira(s): return ''.join(chr(ord(c) - 96) if 'ァ' <= c <= 'ヶ' else c for c in s)
PUNCT = '。、！？!?「」『』（）()・…　 ,.~〜～：:'
OO = set('大多遠通十氷')

# kana -> rōmaji pieces
K2R = {}
_rows = [('', 'あいうえお'), ('k', 'かきくけこ'), ('s', 'さしすせそ'), ('t', 'たちつてと'), ('n', 'なにぬねの'), ('h', 'はひふへほ'), ('m', 'まみむめも'),
         ('r', 'らりるれろ'), ('g', 'がぎぐげご'), ('z', 'ざじずぜぞ'), ('d', 'だぢづでど'), ('b', 'ばびぶべぼ'), ('p', 'ぱぴぷぺぽ')]
for c, ks in _rows:
    for v, k in zip('aiueo', ks): K2R[k] = c + v
K2R.update({'し': 'shi', 'ち': 'chi', 'つ': 'tsu', 'ふ': 'fu', 'じ': 'ji', 'ぢ': 'ji', 'づ': 'zu', 'や': 'ya', 'ゆ': 'yu', 'よ': 'yo', 'わ': 'wa', 'を': 'o', 'ん': 'n',
            'ぁ': 'a', 'ぃ': 'i', 'ぅ': 'u', 'ぇ': 'e', 'ぉ': 'o', 'ゔ': 'vu'})
YOON = {'き': 'ky', 'ぎ': 'gy', 'し': 'sh', 'じ': 'j', 'ち': 'ch', 'ぢ': 'j', 'に': 'ny', 'ひ': 'hy', 'び': 'by', 'ぴ': 'py', 'み': 'my', 'り': 'ry'}
R2K = {}
for k, r in K2R.items():
    if k not in 'ぢづぁぃぅぇぉを': R2K.setdefault(r, k)
for k, r in YOON.items():
    if k in 'ぢ': continue
    for v, sm in zip('auo', 'ゃゅょ'): R2K[r + v] = k + sm
R2K.update({'wo': 'を', 'she': 'しぇ', 'che': 'ちぇ', 'je': 'じぇ', 'ti': 'てぃ', 'di': 'でぃ', 'fa': 'ふぁ', 'fi': 'ふぃ', 'fe': 'ふぇ', 'fo': 'ふぉ', 'wi': 'うぃ', 'we': 'うぇ'})
LONG = {'ā': 'a', 'ī': 'i', 'ū': 'u', 'ē': 'e', 'ō': 'o'}

def roma_to_hira(r, oo=False):
    """Hepburn (with macrons) -> hiragana. oo: write ō as おお instead of おう."""
    r = r.lower(); out = ''; i = 0
    while i < len(r):
        c = r[i]
        if c in "'-":
            i += 1; continue
        if c in LONG:   # a bare long vowel
            out += R2K[LONG[c]] + {'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'お' if oo else 'う'}[LONG[c]]; i += 1; continue
        done = False
        for n in (3, 2, 1):
            seg = r[i:i+n]; base = ''.join(LONG.get(x, x) for x in seg)
            if base in R2K and (n == 1 or seg[:-1] == base[:-1]):
                out += R2K[base]
                if seg[-1] in LONG: out += {'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'お' if oo else 'う'}[base[-1]]
                i += n; done = True; break
        if done: continue
        if c == 'n' or (c == 'm' and i + 1 < len(r) and r[i+1] in 'bpm'):
            out += 'ん'; i += 1; continue
        if i + 1 < len(r) and (r[i+1] == c or (c == 't' and r[i+1:i+3] == 'ch')) and c not in 'aiueo':
            out += 'っ'; i += 1; continue
        return None
    return out

VOW = {'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'お'}
def kana_regex(run):
    """Regex (over de-macroned rōmaji) for a run of kana; long-vowel kana are optional."""
    run = hira(run); out = ''; i = 0; last = ''
    while i < len(run):
        c = run[i]; nx = run[i+1] if i + 1 < len(run) else ''
        if c == 'ー': i += 1; continue
        if c == 'っ':
            # doubled consonant of the following syllable (tch / cch for ち)
            j = i + 1; r = ''
            if j < len(run):
                r = (YOON[run[j]] if run[j] in YOON and j + 1 < len(run) and run[j+1] in 'ゃゅょ' else K2R.get(run[j], ''))
            out += '(?:t|c)' if r.startswith('ch') else (re.escape(r[0]) if r and r[0] not in 'aiueo' else '')
            i += 1; continue
        if c in YOON and nx and nx in 'ゃゅょ':
            r = YOON[c] + {'ゃ': 'a', 'ゅ': 'u', 'ょ': 'o'}[nx]; i += 2
        elif c in K2R:
            r = K2R[c]; i += 1
        else:
            return None
        v = r[-1]
        piece = re.escape(r)
        if c == 'は': piece = '(?:ha|wa)'
        elif c == 'へ': piece = '(?:he|e)'
        elif c == 'を': piece = '(?:wo|o)'
        elif c == 'ん': piece = "(?:n|m)"
        # a vowel kana that only lengthens the previous syllable may be missing after de-macroning
        if r in VOW and last and (r == last or (last == 'o' and r == 'u') or (last == 'e' and r == 'i')): piece = '(?:' + piece + ')?'
        out += piece; last = v if c != 'ん' else ''
    return out

def segments(jp):
    """Split into ('k', kanji run) / ('n', kana run) / ('d', digits or latin) / ('p', punctuation)."""
    segs = []
    for c in jp:
        t = 'k' if is_kanji(c) else 'n' if (is_kana(c) and c not in '・') else 'p' if (c in PUNCT or c.isspace()) else 'd'
        if segs and segs[-1][0] == t: segs[-1][1] += c
        else: segs.append([t, c])
    return segs

def merge_digits(segs):
    out = []
    for t, x in segs:
        if out and out[-1][0] == 'k' and t in 'kd': out[-1] = ['k', out[-1][1] + x]
        elif t == 'd': out.append(['k', x])
        else: out.append([t, x])
    return out

def ruby(segs, reads):
    out = ''; it = iter(reads)
    for t, s in segs:
        out += f'<ruby>{html.escape(s)}<rt>{html.escape(next(it))}</rt></ruby>' if t == 'k' else html.escape(s)
    return out

PREQ = r'\s*[、，,。.!?！？…「」『』（）()—-]+\s*'; POPT = r'[\s、，,。.!?！？…「」『』（）()—-]*'
def solve(tokens, text, valid):
    """tokens: ('lit', [regex alternatives]) or ('grp', seg). Returns the list of group strings, or None."""
    memo = {}
    def go(ti, pos):
        key = (ti, pos)
        if key in memo: return memo[key]
        res = None
        if ti == len(tokens):
            res = [] if not text[pos:].strip(' 。.!?！？') else None
        elif tokens[ti][0] == 'lit':
            for pat in tokens[ti][1]:
                m = re.compile(pat).match(text, pos)
                if m:
                    r = go(ti + 1, m.end())
                    if r is not None: res = r; break
        else:
            for end in range(pos + 1, len(text) + 1):
                v = valid(tokens[ti][1], pos, end)
                if v is None: continue
                r = go(ti + 1, end)
                if r is not None: res = [v] + r; break
        memo[key] = res
        return res
    return go(0, 0)

def by_kana(jp, rd):
    rd = hira(rd.strip()); segs = merge_digits(segments(jp)); toks = []
    for t, s in segs:
        if t == 'k': toks.append(('grp', s))
        elif t == 'n': toks.append(('lit', [r'\s*' + r'\s*'.join(re.escape(c) for c in hira(s)) + r'\s*']))
        else: toks.append(('lit', [PREQ, POPT]))
    def valid(seg, a, b):
        r = rd[a:b]
        if r != r.strip() and r.strip() == '': return None
        r = r.replace(' ', '')
        nk = len(re.findall('[' + KANJI + ']', seg)) + (1 if re.search(r'\d', seg) else 0)
        if not re.fullmatch('[぀-ゟー]+', r) or len(r) < nk or len(r) > 6 * max(1, len(seg)): return None
        if rd[a] == ' ' or rd[b-1] == ' ': return None
        return r
    reads = solve(toks, rd, valid)
    return ruby(segs, reads) if reads is not None else None

def by_romaji(jp, rd):
    orig = unicodedata.normalize('NFC', rd.lower()); loose = ''; idx = []
    for i, c in enumerate(orig):
        b = LONG.get(c, c)
        if b.isalpha() and b.isascii(): loose += b; idx.append(i)
    segs = merge_digits(segments(jp)); toks = []
    for t, s in segs:
        if t == 'k': toks.append(('grp', s))
        elif t == 'n':
            kr = kana_regex(s)
            if kr is None: return None
            toks.append(('lit', [kr, kr.replace(')?', ')??')]))
    def valid(seg, a, b):
        part = re.sub(r"[^a-zāīūēō']", '', orig[idx[a]:idx[b-1]+1])
        h = roma_to_hira(part, oo=bool(set(seg) & OO))
        nk = len(re.findall('[' + KANJI + ']', seg)) + (1 if re.search(r'\d', seg) else 0)
        if not h or len(h) < nk or len(h) > 6 * max(1, len(seg)): return None
        return h
    reads = solve(toks, loose, valid)
    return ruby(segs, reads) if reads is not None else None

def one(jp, rd):
    return by_kana(jp, rd) if re.search('[぀-ヿ]', rd) else by_romaji(jp, rd)

def build_furi(lines):
    out = {}; fail = []; n = 0
    for l in lines:
        if not l.startswith('ex:'): continue
        p = [x.strip() for x in l[3:].split('|')]
        jp, rd = (p + ['', ''])[:2]
        if not re.search('[' + KANJI + ']', jp): continue
        n += 1; r = None
        if rd:
            if '→' in jp:
                a, b = [x.strip() for x in jp.split('→')], [x.strip() for x in rd.split('→')]
                if len(a) == len(b):
                    parts = [one(x, y) if re.search('[' + KANJI + ']', x) else html.escape(x) for x, y in zip(a, b)]
                    if all(parts): r = ' → '.join(parts)
            else: r = one(jp, rd)
        if r: out[jp] = r
        else: fail.append(jp)
    return out, fail, n
