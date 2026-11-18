import os, re, json
LANGS = ['en', 'fr', 'pt', 'ar']
def build_kanji(d, svgdir):
    k, m, x, lv = [], {l: [] for l in LANGS}, {}, None
    for line in open(os.path.join(d, 'kanji.tsv'), encoding='utf-8'):
        line = line.rstrip('\n')
        if not line: continue
        if line.startswith('#'): lv = line[1:]; continue
        p = line.split('|'); assert len(p) == 7, line
        strokes = []   # stroke order now lives in the separate Kanji app
        k.append([p[0], lv, p[1], p[2], strokes])
        for i, l in enumerate(LANGS): m[l].append(p[3 + i])
    for line in open(os.path.join(d, 'kanji_x.tsv'), encoding='utf-8'):
        p = line.rstrip('\n').split('|')
        if len(p) == 7: x[p[0]] = [p[1], p[2], dict(zip(LANGS, p[3:]))]
    return json.dumps({'k': k, 'm': m, 'x': x}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
