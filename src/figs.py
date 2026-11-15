# Inline SVG illustrations (v2). Colours come from CSS classes so they follow light/dark themes.
# f-* = fill, s-* = stroke. t = UI text, tj = Japanese text.

def person(cx, by, c='f-acc2', hair='f-black', bow=0, smile=True):
    """Friendly figure standing on baseline `by`."""
    g = f'<g transform="rotate({bow} {cx} {by})">' if bow else '<g>'
    return (f'<ellipse cx="{cx}" cy="{by+3}" rx="30" ry="6" class="f-shadow"/>' + g +
            f'<path d="M{cx-22} {by} v-44 a22 22 0 0 1 44 0 v44 z" class="{c}"/>'
            f'<rect x="{cx-22}" y="{by-8}" width="44" height="8" class="f-black" opacity=".18"/>'
            f'<circle cx="{cx}" cy="{by-86}" r="20" class="f-skin"/>'
            f'<path d="M{cx-21} {by-88} a21 21 0 0 1 42 0 q-6 -9 -21 -8 q-15 -1 -21 8 z" class="{hair}"/>'
            f'<circle cx="{cx-7}" cy="{by-84}" r="2.2" class="f-black"/><circle cx="{cx+7}" cy="{by-84}" r="2.2" class="f-black"/>' +
            (f'<path d="M{cx-6} {by-76} q6 5 12 0" class="s-black" stroke-width="2" fill="none" stroke-linecap="round"/>' if smile else '') +
            '</g>')

def cat(cx, by, s=1):
    return (f'<g transform="translate({cx} {by}) scale({s})">'
            '<ellipse cx="0" cy="3" rx="44" ry="6" class="f-shadow"/>'
            '<path d="M-34 -6 q-22 -6 -16 -30" class="s-black" stroke-width="7" fill="none" stroke-linecap="round"/>'
            '<ellipse cx="-4" cy="-16" rx="32" ry="18" class="f-black"/>'
            '<circle cx="24" cy="-30" r="16" class="f-black"/>'
            '<path d="M12 -40 l2 -16 l10 10 z M27 -45 l10 -11 l2 16 z" class="f-black"/>'
            '<circle cx="19" cy="-32" r="2.6" class="f-gold"/><circle cx="30" cy="-32" r="2.6" class="f-gold"/>'
            '<path d="M22 -25 l2.5 2.5 l2.5 -2.5 z" class="f-acc"/>'
            '</g>')

def tree(x, by, s=1):
    return (f'<g transform="translate({x} {by}) scale({s})"><rect x="-4" y="-26" width="8" height="26" rx="2" class="f-soft2"/>'
            '<circle cx="0" cy="-42" r="22" class="f-leaf"/><circle cx="-14" cy="-30" r="14" class="f-leaf"/><circle cx="14" cy="-30" r="14" class="f-leaf"/></g>')

def cloud(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})" class="f-white" opacity=".92">'
            '<ellipse cx="0" cy="0" rx="26" ry="11"/><ellipse cx="-14" cy="-7" rx="13" ry="10"/><ellipse cx="8" cy="-10" rx="16" ry="12"/></g>')

def rb(x, y, kanji, kana, size, rs=None, anchor=True):
    """Kanji with its reading as furigana above it."""
    rs = rs or max(9, round(size * .5))
    a = ' text-anchor="middle"' if anchor else ''
    return (f'<text x="{x}" y="{y - round(size * .98)}"{a} class="tj" font-size="{rs}">{kana}</text>'
            f'<text x="{x}" y="{y}"{a} class="tj b" font-size="{size}">{kanji}</text>')

FIGS = {}

FIGS["hero"] = f"""<svg viewBox="0 0 640 260" role="img" aria-label="Mount Fuji, a torii gate and the rising sun">
<rect x="0" y="0" width="640" height="260" rx="22" class="f-sky"/>
<circle cx="452" cy="92" r="56" class="f-acc"/>
{cloud(150, 116, 1.1)}{cloud(560, 52, 1)}{cloud(330, 40, .8)}
<path d="M70 214 L262 58 Q276 46 290 58 L482 214 Z" class="f-mount"/>
<path d="M214 97 L262 58 Q276 46 290 58 L338 97 L318 88 L300 104 L282 90 L266 104 L248 88 L232 102 Z" class="f-white"/>
<path d="M0 214 q90 -46 190 -12 q90 30 180 -4 q120 -44 270 2 V260 H0 Z" class="f-leaf"/>
<g class="f-acc"><rect x="520" y="150" width="9" height="74"/><rect x="578" y="150" width="9" height="74"/>
<path d="M502 136 q52 12 104 0 l4 12 q-56 12 -112 0 z"/><rect x="512" y="164" width="84" height="7"/></g>
<g class="s-white" stroke-width="3" fill="none" opacity=".75" stroke-linecap="round">
<path d="M20 240 q14 -9 28 0 t28 0 t28 0 t28 0"/><path d="M250 246 q14 -9 28 0 t28 0 t28 0"/><path d="M430 240 q14 -9 28 0 t28 0"/></g>
<g class="f-pink"><circle cx="46" cy="150" r="6"/><circle cx="66" cy="132" r="5"/><circle cx="34" cy="126" r="4"/><circle cx="84" cy="158" r="4"/></g>
<text x="34" y="62" class="tj b" font-size="40">日本語</text>
<text x="36" y="88" class="t" font-size="13" letter-spacing="4">NIHONGO</text>
</svg>"""

FIGS["scripts"] = """<svg viewBox="0 0 640 230" role="img" aria-label="The three Japanese scripts">
<g text-anchor="middle">
<g><rect x="8" y="8" width="198" height="214" rx="18" class="f-soft"/><circle cx="107" cy="66" r="42" class="f-acc"/>
<text x="107" y="86" class="tj f-paper" font-size="52">あ</text>
<text x="107" y="136" class="t b" font-size="18">Hiragana</text>
<text x="107" y="160" class="t" font-size="13">grammar endings,</text><text x="107" y="178" class="t" font-size="13">particles, native words</text>
<rect x="34" y="190" width="146" height="24" rx="12" class="f-paper"/><text x="107" y="207" class="tj" font-size="14">たべ<tspan class="f-acc b">ます</tspan>・は・を</text></g>
<g><rect x="221" y="8" width="198" height="214" rx="18" class="f-soft"/><circle cx="320" cy="66" r="42" class="f-acc2"/>
<text x="320" y="86" class="tj f-paper" font-size="52">ア</text>
<text x="320" y="136" class="t b" font-size="18">Katakana</text>
<text x="320" y="160" class="t" font-size="13">foreign words, names,</text><text x="320" y="178" class="t" font-size="13">sound effects, emphasis</text>
<rect x="247" y="190" width="146" height="24" rx="12" class="f-paper"/><text x="320" y="207" class="tj" font-size="14">コーヒー・パン</text></g>
<g><rect x="434" y="8" width="198" height="214" rx="18" class="f-soft"/><circle cx="533" cy="66" r="42" class="f-ink"/>
<text x="533" y="86" class="tj f-paper" font-size="52">山</text>
<text x="533" y="136" class="t b" font-size="18">Kanji</text>
<text x="533" y="160" class="t" font-size="13">meaning: nouns,</text><text x="533" y="178" class="t" font-size="13">verb &amp; adjective stems</text>
<rect x="460" y="190" width="146" height="24" rx="12" class="f-paper"/><text x="533" y="207" class="tj" font-size="14">日本・食べる</text></g>
</g></svg>"""

FIGS["diacritics"] = """<svg viewBox="0 0 640 176" role="img" aria-label="Dakuten, handakuten and small tsu">
<g text-anchor="middle">
<rect x="8" y="8" width="198" height="160" rx="18" class="f-soft"/>
<rect x="60" y="18" width="94" height="24" rx="12" class="f-acc"/><text x="107" y="35" class="t b f-paper" font-size="13">dakuten ゛</text>
<text x="60" y="110" class="tj" font-size="50">か</text><path d="M92 92 h24 m-8 -8 l8 8 l-8 8" class="s-acc" stroke-width="3" fill="none" stroke-linecap="round"/>
<text x="154" y="110" class="tj f-acc" font-size="50">が</text><text x="107" y="150" class="t" font-size="14">ka → ga</text>
<rect x="221" y="8" width="198" height="160" rx="18" class="f-soft"/>
<rect x="262" y="18" width="116" height="24" rx="12" class="f-acc2"/><text x="320" y="35" class="t b f-paper" font-size="13">handakuten ゜</text>
<text x="273" y="110" class="tj" font-size="50">は</text><path d="M305 92 h24 m-8 -8 l8 8 l-8 8" class="s-acc2" stroke-width="3" fill="none" stroke-linecap="round"/>
<text x="367" y="110" class="tj f-acc2" font-size="50">ぱ</text><text x="320" y="150" class="t" font-size="14">ha → pa (only the h-row)</text>
<rect x="434" y="8" width="198" height="160" rx="18" class="f-soft"/>
<rect x="486" y="18" width="94" height="24" rx="12" class="f-ink"/><text x="533" y="35" class="t b f-paper" font-size="13">small っ</text>
<text x="533" y="108" class="tj" font-size="40">ゆ<tspan class="f-acc" font-size="28">っ</tspan>くり</text>
<text x="533" y="150" class="t" font-size="14">yu<tspan class="f-acc b">k</tspan>kuri (doubled k)</text>
</g></svg>"""

FIGS["sentence"] = f"""<svg viewBox="0 0 640 250" role="img" aria-label="Basic Japanese sentence order">
{person(86, 104)}
<g><ellipse cx="282" cy="107" rx="26" ry="5" class="f-shadow"/><circle cx="282" cy="80" r="24" class="f-acc"/>
<path d="M282 58 q2 -14 12 -16" class="s-ink" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M286 52 q14 -12 22 2 q-14 8 -22 -2z" class="f-leaf"/>
<circle cx="273" cy="72" r="5" class="f-white" opacity=".5"/></g>
<g><ellipse cx="500" cy="107" rx="40" ry="5" class="f-shadow"/><path d="M462 78 h76 a38 26 0 0 1 -76 0 z" class="f-soft2"/><rect x="456" y="72" width="88" height="8" rx="4" class="f-ink"/>
<path d="M486 64 q-6 -8 0 -16 M500 64 q-6 -8 0 -16 M514 64 q-6 -8 0 -16" class="s-soft" stroke-width="2.5" fill="none" stroke-linecap="round"/></g>
<g font-size="22" text-anchor="middle">
<rect x="20" y="130" width="132" height="56" rx="12" class="f-acc2"/><text x="86" y="166" class="tj f-paper">わたし</text>
<circle cx="184" cy="158" r="28" class="f-acc"/><text x="184" y="166" class="tj f-paper">は</text>
<rect x="216" y="130" width="132" height="56" rx="12" class="f-soft2"/><text x="282" y="166" class="tj">りんご</text>
<circle cx="380" cy="158" r="28" class="f-acc"/><text x="380" y="166" class="tj f-paper">を</text>
<rect x="412" y="130" width="176" height="56" rx="12" class="f-ink"/><text x="500" y="166" class="tj f-paper">たべます</text>
<text x="606" y="170" class="tj" font-size="30">。</text>
</g>
<g font-size="13" text-anchor="middle" class="t">
<text x="86" y="208">TOPIC</text><text x="184" y="208">particle</text><text x="282" y="208">OBJECT</text>
<text x="380" y="208">particle</text><text x="500" y="208">VERB (always last)</text>
<text x="320" y="238" font-style="italic" font-size="15">"I eat an apple."</text>
</g></svg>"""

FIGS["route"] = f"""<svg viewBox="0 0 640 230" role="img" aria-label="から and まで: from the house to the bank">
<rect x="0" y="170" width="640" height="60" rx="14" class="f-soft"/>
<circle cx="320" cy="34" r="20" class="f-gold"/>{cloud(210, 44, .8)}{cloud(430, 30, .7)}
{tree(182, 172, .9)}{tree(450, 172, .8)}
<g><path d="M34 112 L96 64 L158 112 Z" class="f-acc"/><rect x="48" y="110" width="96" height="62" class="f-paper"/><rect x="48" y="110" width="96" height="62" fill="none" class="s-ink" stroke-width="2.5"/>
<rect x="86" y="134" width="22" height="38" rx="3" class="f-acc2"/><rect x="58" y="122" width="20" height="18" rx="2" class="f-sky"/><rect x="116" y="122" width="20" height="18" rx="2" class="f-sky"/></g>
<g><path d="M482 96 L554 62 L626 96 Z" class="f-ink"/><rect x="488" y="96" width="132" height="10" class="f-ink"/>
<rect x="492" y="106" width="124" height="60" class="f-paper"/>
<g class="f-acc2"><rect x="500" y="108" width="12" height="56"/><rect x="528" y="108" width="12" height="56"/><rect x="568" y="108" width="12" height="56"/><rect x="596" y="108" width="12" height="56"/></g>
<rect x="484" y="164" width="140" height="8" class="f-ink"/><text x="554" y="90" text-anchor="middle" class="tj f-paper b" font-size="13">銀行</text></g>
<path d="M164 196 H470" class="s-acc" stroke-width="4" stroke-dasharray="2 12" stroke-linecap="round" fill="none"/>
<path d="M462 186 L478 196 L462 206" class="s-acc" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<g><ellipse cx="318" cy="200" rx="56" ry="5" class="f-shadow"/><rect x="266" y="146" width="104" height="44" rx="10" class="f-gold"/>
<g class="f-sky"><rect x="274" y="154" width="22" height="16" rx="3"/><rect x="302" y="154" width="22" height="16" rx="3"/><rect x="330" y="154" width="32" height="16" rx="3"/></g>
<circle cx="290" cy="192" r="9" class="f-black"/><circle cx="346" cy="192" r="9" class="f-black"/><circle cx="290" cy="192" r="3.5" class="f-white"/><circle cx="346" cy="192" r="3.5" class="f-white"/></g>
<g text-anchor="middle">
<text x="96" y="30" class="tj b" font-size="22">いえ<tspan class="f-acc">から</tspan></text><text x="96" y="50" class="t" font-size="13">from the house</text>
<text x="554" y="30" class="tj b" font-size="22">ぎんこう<tspan class="f-acc">まで</tspan></text><text x="554" y="50" class="t" font-size="13">as far as the bank</text>
<text x="318" y="132" class="tj b" font-size="20">バス<tspan class="f-acc">で</tspan></text><text x="318" y="224" class="t" font-size="13">で = by means of · へ = towards</text>
</g></svg>"""

FIGS["kosoado"] = f"""<svg viewBox="0 0 640 250" role="img" aria-label="これ, それ, あれ according to distance">
<ellipse cx="140" cy="176" rx="124" ry="50" class="f-acc2bg"/><ellipse cx="372" cy="176" rx="124" ry="50" class="f-accbg"/>
{person(92, 180, 'f-acc2')}{person(420, 180, 'f-acc', 'f-soft2')}
<g><rect x="156" y="150" width="46" height="34" rx="5" class="f-gold"/><rect x="162" y="150" width="6" height="34" class="f-black" opacity=".25"/></g>
<g><rect x="304" y="150" width="46" height="34" rx="5" class="f-leaf"/><rect x="310" y="150" width="6" height="34" class="f-black" opacity=".25"/></g>
<g><ellipse cx="573" cy="150" rx="34" ry="5" class="f-shadow"/><rect x="550" y="112" width="46" height="34" rx="5" class="f-pink"/><rect x="556" y="112" width="6" height="34" class="f-black" opacity=".25"/></g>
<path d="M118 120 q30 -8 44 22" class="s-acc2" stroke-width="2.5" fill="none" stroke-dasharray="4 5" stroke-linecap="round"/>
<path d="M394 120 q-30 -8 -44 22" class="s-acc" stroke-width="2.5" fill="none" stroke-dasharray="4 5" stroke-linecap="round"/>
<g text-anchor="middle">
<text x="179" y="210" class="tj b" font-size="21">これ</text><text x="179" y="228" class="t" font-size="12">near me</text>
<text x="327" y="210" class="tj b" font-size="21">それ</text><text x="327" y="228" class="t" font-size="12">near you</text>
<text x="573" y="180" class="tj b" font-size="21">あれ</text><text x="573" y="198" class="t" font-size="12">far from both</text>
<text x="92" y="52" class="t" font-size="13">speaker</text><text x="420" y="52" class="t" font-size="13">listener</text>
<rect x="508" y="30" width="130" height="28" rx="14" class="f-soft"/><text x="573" y="50" class="tj" font-size="15">どれ? = which?</text>
</g></svg>"""

_ticks = ''.join(f'<rect x="118.5" y="24" width="3" height="{12 if i % 3 == 0 else 6}" rx="1.5" class="f-ink" transform="rotate({i*30} 120 110)"/>' for i in range(12))
FIGS["clock"] = f"""<svg viewBox="0 0 640 220" role="img" aria-label="A clock showing 7:30">
<ellipse cx="120" cy="208" rx="70" ry="6" class="f-shadow"/>
<circle cx="120" cy="110" r="96" class="f-acc2"/><circle cx="120" cy="110" r="84" class="f-paper"/>
{_ticks}
<g text-anchor="middle" class="t b" font-size="15"><text x="120" y="56">12</text><text x="176" y="115">3</text><text x="120" y="176">6</text><text x="64" y="115">9</text></g>
<line x1="120" y1="110" x2="120" y2="42" class="s-acc" stroke-width="5" stroke-linecap="round" transform="rotate(180 120 110)"/>
<line x1="120" y1="110" x2="120" y2="64" class="s-ink" stroke-width="8" stroke-linecap="round" transform="rotate(225 120 110)"/>
<circle cx="120" cy="110" r="7" class="f-ink"/>
<rect x="250" y="24" width="372" height="78" rx="16" class="f-soft"/>
<text x="270" y="62" class="tj b" font-size="30">しち<tspan class="f-acc">じ</tspan> はん</text>
<text x="270" y="88" class="t" font-size="14">shichi-ji han — 7:30 (7 o'clock and a half)</text>
<rect x="250" y="116" width="372" height="78" rx="16" class="f-soft"/>
<text x="270" y="152" class="tj" font-size="21">7<tspan class="f-acc b">時</tspan> 30<tspan class="f-acc2 b">分</tspan> = しちじ さんじゅっぷん</text>
<text x="270" y="178" class="t" font-size="14">hour 時 (ji) first, then minutes 分 (fun / pun)</text>
</svg>"""

def _cal(x, cls, big, small):
    return (f'<g><rect x="{x}" y="34" width="170" height="126" rx="14" class="f-paper"/><rect x="{x}" y="34" width="170" height="126" rx="14" fill="none" class="s-soft2" stroke-width="2"/>'
            f'<path d="M{x} 70 v-22 a14 14 0 0 1 14 -14 h142 a14 14 0 0 1 14 14 v22 z" class="{cls}"/>'
            f'<rect x="{x+38}" y="22" width="8" height="26" rx="4" class="f-ink"/><rect x="{x+124}" y="22" width="8" height="26" rx="4" class="f-ink"/>'
            f'<text x="{x+85}" y="62" class="t f-paper b" font-size="14">{small}</text>'
            f'<text x="{x+85}" y="128" class="tj b" font-size="36">{big}</text></g>')
FIGS["date"] = f"""<svg viewBox="0 0 640 200" role="img" aria-label="Dates go year, month, day">
<g text-anchor="middle">
{_cal(20, 'f-acc2', '2025年', 'year · nen')}{_cal(235, 'f-acc', '9月', 'month · gatsu')}{_cal(450, 'f-ink', '12日', 'day · nichi')}
<path d="M200 98 l14 0 m-6 -6 l6 6 l-6 6 M415 98 l14 0 m-6 -6 l6 6 l-6 6" class="s-ink" stroke-width="3" fill="none" stroke-linecap="round"/>
<text x="320" y="190" class="t" font-size="13">Biggest unit first — the opposite of "12 September 2025".</text>
</g></svg>"""

FIGS["position"] = f"""<svg viewBox="0 0 640 270" role="img" aria-label="Position words around a table">
<rect x="0" y="216" width="640" height="54" rx="14" class="f-soft"/>
<ellipse cx="320" cy="222" rx="170" ry="8" class="f-shadow"/>
<rect x="160" y="112" width="320" height="16" rx="6" class="f-gold"/>
<rect x="178" y="128" width="14" height="92" rx="3" class="f-gold"/><rect x="448" y="128" width="14" height="92" rx="3" class="f-gold"/>
<g><rect x="294" y="74" width="52" height="38" rx="4" class="f-acc"/><path d="M294 88 h52 M320 74 v38" class="s-white" stroke-width="3"/></g>
{cat(318, 218, 1)}
<g><ellipse cx="86" cy="222" rx="38" ry="6" class="f-shadow"/><circle cx="86" cy="190" r="30" class="f-acc2"/><path d="M60 178 q26 -20 52 0" class="s-white" stroke-width="3" fill="none"/></g>
<g><ellipse cx="560" cy="222" rx="44" ry="6" class="f-shadow"/><path d="M522 164 h76 v56 h-76 z" class="f-soft2"/><path d="M522 164 l-12 -16 h76 l12 16" class="f-soft2" opacity=".7"/>
<circle cx="560" cy="186" r="15" class="f-pink"/><path d="M522 190 h76 v30 h-76 z" class="f-soft2"/></g>
<g text-anchor="middle">
<rect x="262" y="26" width="116" height="34" rx="17" class="f-paper"/><text x="320" y="50" class="tj b" font-size="19">うえ <tspan class="t" font-size="12">on / above</tspan></text>
<rect x="250" y="232" width="140" height="34" rx="17" class="f-paper"/><text x="320" y="256" class="tj b" font-size="19">した <tspan class="t" font-size="12">under / below</tspan></text>
<text x="86" y="140" class="tj b" font-size="20">まえ</text><text x="86" y="252" class="t" font-size="12">in front of</text>
<text x="560" y="134" class="tj b" font-size="20">なか</text><text x="560" y="252" class="t" font-size="12">inside</text>
</g></svg>"""

FIGS["verbgroups"] = """<svg viewBox="0 0 640 262" role="img" aria-label="How to tell ichidan from godan verbs">
<g text-anchor="middle">
<rect x="190" y="8" width="260" height="52" rx="26" class="f-soft"/>
<text x="320" y="31" class="t b" font-size="15">Dictionary form ends in</text><text x="320" y="50" class="tj b" font-size="15">-いる / -える ?</text>
<path d="M250 60 Q150 70 150 104 M390 60 Q490 70 490 104" class="s-ink" stroke-width="2.5" fill="none"/>
<rect x="158" y="68" width="44" height="22" rx="11" class="f-leaf"/><text x="180" y="84" class="t b f-paper" font-size="12">yes</text>
<rect x="438" y="68" width="44" height="22" rx="11" class="f-ink"/><text x="460" y="84" class="t b f-paper" font-size="12">no</text>
<rect x="36" y="104" width="228" height="62" rx="16" class="f-acc2"/>
<text x="150" y="130" class="t b f-paper" font-size="15">Probably ICHIDAN</text><text x="150" y="152" class="tj f-paper" font-size="15">食べる・見る・寝る</text>
<rect x="376" y="104" width="228" height="62" rx="16" class="f-acc"/>
<text x="490" y="130" class="t b f-paper" font-size="15">GODAN</text><text x="490" y="152" class="tj f-paper" font-size="15">飲む・待つ・話す</text>
<path d="M150 166 V194" class="s-ink" stroke-width="2.5"/>
<rect x="16" y="194" width="268" height="60" rx="16" class="f-accbg"/><rect x="16" y="194" width="268" height="60" rx="16" fill="none" class="s-acc" stroke-width="2" stroke-dasharray="6 5"/>
<text x="150" y="218" class="t b" font-size="13">…unless it is a "fake ichidan"</text><text x="150" y="240" class="tj" font-size="14">帰る・入る・走る・知る → godan</text>
<rect x="366" y="194" width="248" height="60" rx="16" class="f-ink"/>
<text x="490" y="214" class="t b f-paper" font-size="13">Only 2 irregular verbs</text><text x="490" y="245" class="tj f-paper b" font-size="17">する ・ 来る</text><text x="510" y="229" text-anchor="middle" class="tj f-paper" font-size="9">く</text>
</g></svg>"""

FIGS["giving"] = f"""<svg viewBox="0 0 640 262" role="img" aria-label="あげる, くれる and もらう">
<defs><marker id="ah2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="f-acc"/></marker></defs>
{person(96, 176, 'f-acc2')}{person(544, 176, 'f-leaf', 'f-soft2')}
<path d="M150 92 H486" class="s-acc" stroke-width="3.5" marker-end="url(#ah2)" fill="none"/>
<path d="M490 150 H154" class="s-acc" stroke-width="3.5" marker-end="url(#ah2)" fill="none"/>
<g><rect x="304" y="100" width="32" height="26" rx="4" class="f-gold"/><rect x="317" y="100" width="6" height="26" class="f-acc"/><rect x="304" y="110" width="32" height="5" class="f-acc"/>
<path d="M320 100 q-12 -14 -14 -2 q2 6 14 2 q12 4 14 -2 q-2 -12 -14 2" class="f-acc"/></g>
<g text-anchor="middle">
<text x="96" y="206" class="t b" font-size="14">me / my group</text><text x="544" y="206" class="t b" font-size="14">someone else</text>
<text x="320" y="80" class="tj" font-size="18"><tspan class="b">あげる</tspan> (I give / do for)</text>
<text x="320" y="174" class="tj" font-size="18"><tspan class="b">くれる</tspan> (they give / do for me)</text>
<rect x="110" y="222" width="420" height="34" rx="17" class="f-soft"/>
<text x="320" y="245" class="tj" font-size="15"><tspan class="b">もらう</tspan> = same arrow, seen from me: "I receive"</text>
</g></svg>"""

FIGS["keigo"] = f"""<svg viewBox="0 0 640 250" role="img" aria-label="Honorific and humble language">
<rect x="0" y="204" width="640" height="46" rx="14" class="f-soft"/>
<rect x="56" y="150" width="104" height="60" rx="8" class="f-gold"/><rect x="48" y="142" width="120" height="12" rx="4" class="f-gold"/>
{person(108, 142, 'f-acc', 'f-soft2')}
<path d="M196 176 V112" class="s-acc" stroke-width="4" stroke-linecap="round"/><path d="M184 126 L196 110 L208 126" class="s-acc" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
{person(520, 206, 'f-acc2', 'f-black', bow=-14)}
<path d="M596 104 V168" class="s-acc2" stroke-width="4" stroke-linecap="round"/><path d="M584 154 L596 170 L608 154" class="s-acc2" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<g>
<text x="224" y="44" class="tj b" font-size="20">尊敬語 sonkeigo</text>
<text x="224" y="68" class="t" font-size="13">raise the OTHER person's actions</text>
<text x="224" y="90" class="tj" font-size="14">いらっしゃる・召し上がる</text>
<text x="224" y="146" class="tj b" font-size="20">謙譲語 kenjōgo</text>
<text x="224" y="170" class="t" font-size="13">lower MY OWN actions</text>
<text x="224" y="192" class="tj" font-size="14">申す・いたす・いただく</text>
</g></svg>"""

FIGS["ballfall"] = """<svg viewBox="0 0 640 170" role="img" aria-label="Conditional と: drop the ball and it falls">
<rect x="0" y="146" width="150" height="24" rx="10" class="f-soft"/>
<rect x="6" y="14" width="40" height="26" rx="8" class="f-acc2"/><rect x="38" y="12" width="74" height="30" rx="15" class="f-skin"/><rect x="92" y="34" width="16" height="26" rx="8" class="f-skin"/><rect x="52" y="34" width="16" height="22" rx="8" class="f-skin"/>
<circle cx="78" cy="80" r="15" class="f-acc" opacity=".35"/><circle cx="78" cy="132" r="15" class="f-acc"/><circle cx="73" cy="127" r="4" class="f-white" opacity=".5"/>
<path d="M78 60 V112" class="s-acc" stroke-width="3" stroke-dasharray="3 7" stroke-linecap="round"/>
<path d="M56 96 v20 M100 96 v20" class="s-soft" stroke-width="2.5" stroke-linecap="round"/>
<text x="176" y="62" class="tj b" font-size="23">ボールを落とす<tspan class="f-acc">と</tspan>、落ちる。</text>
<text x="176" y="96" class="t" font-size="14">A happens → B always/automatically follows.</text>
<text x="176" y="120" class="t" font-size="14">Use と for natural consequences, habits, machines, directions.</text>
</svg>"""

# ---------------- new illustrations (Japanese labels only, nothing to translate) ----------------
def _tile(x, cls, kana, romaji, art, dx=0):
    return (f'<g><rect x="{x}" y="8" width="146" height="170" rx="18" class="{cls}"/><g transform="translate({dx} -8)">{art}</g>'
            + rb(x+73, 144, kana.split(' ')[0], kana.split(' ')[1], 28, 13) +
            f'<text x="{x+73}" y="164" text-anchor="middle" class="t" font-size="13">{romaji}</text></g>')
_petals = ''.join(f'<ellipse cx="85" cy="42" rx="10" ry="17" class="f-pink" transform="rotate({a} 85 62)"/>' for a in range(0, 360, 72))
_rays = ''.join(f'<rect x="245" y="24" width="6" height="14" rx="3" class="f-gold" transform="rotate({a} 248 64)"/>' for a in range(0, 360, 45))
_flake = ''.join(f'<g transform="rotate({a} 574 64)"><path d="M574 64 V28 M574 40 l-8 -8 M574 40 l8 -8" class="s-acc2" stroke-width="4" fill="none" stroke-linecap="round"/></g>' for a in range(0, 360, 60))
FIGS["seasons"] = f"""<svg viewBox="0 0 640 186" role="img" aria-label="The four seasons: haru, natsu, aki, fuyu">
{_tile(11, 'f-soft', '春 はる', 'haru', _petals + '<circle cx="85" cy="62" r="7" class="f-gold"/>', -1)}
{_tile(168, 'f-soft', '夏 なつ', 'natsu', _rays + '<circle cx="248" cy="64" r="22" class="f-gold"/>', -7)}
{_tile(325, 'f-soft', '秋 あき', 'aki', '<path d="M411 26 l8 16 l16 -6 l-6 16 l16 8 l-18 6 l2 18 l-14 -10 l-4 18 l-4 -18 l-14 10 l2 -18 l-18 -6 l16 -8 l-6 -16 l16 6 z" class="f-acc"/>', -13)}
{_tile(482, 'f-soft', '冬 ふゆ', 'fuyu', _flake, -19)}
</svg>"""

_COL = [('あか', 'aka', '#d6453a'), ('あお', 'ao', '#2f6fd0'), ('きいろ', 'kiiro', '#f2c12e'), ('みどり', 'midori', '#3f9a5a'), ('オレンジ', 'orenji', '#f08a2c'),
        ('むらさき', 'murasaki', '#8a55c2'), ('ちゃいろ', 'chairo', '#8a5a3a'), ('しろ', 'shiro', '#ffffff'), ('くろ', 'kuro', '#1c1c1e')]
FIGS["colors"] = '<svg viewBox="0 0 640 132" role="img" aria-label="Colour names in Japanese">' + ''.join(
    f'<g text-anchor="middle"><circle cx="{38+i*70.5}" cy="44" r="28" fill="{c}" class="s-soft" stroke-width="1.5"/>'
    f'<text x="{38+i*70.5}" y="96" class="tj b" font-size="{13 if len(k) > 3 else 15}">{k}</text><text x="{38+i*70.5}" y="116" class="t" font-size="11.5">{r}</text></g>'
    for i, (k, r, c) in enumerate(_COL)) + '</svg>'

FIGS["daytime"] = f"""<svg viewBox="0 0 640 218" role="img" aria-label="Times of day: asa, hiru, yūgata, yoru">
<defs><linearGradient id="dsky" x1="0" x2="1"><stop offset="0" stop-color="#ffd9a8"/><stop offset=".32" stop-color="#bfe0fb"/><stop offset=".62" stop-color="#ffb37a"/><stop offset="1" stop-color="#27335e"/></linearGradient></defs>
<rect x="8" y="8" width="624" height="112" rx="18" fill="url(#dsky)"/>
<path d="M40 120 Q320 -70 600 120" fill="none" stroke="#ffffff" stroke-width="2" stroke-dasharray="3 8" opacity=".8"/>
<circle cx="92" cy="86" r="17" fill="#f6b73c"/><circle cx="250" cy="36" r="20" fill="#f6c63c"/><circle cx="412" cy="52" r="18" fill="#f08a2c"/>
<g><circle cx="548" cy="56" r="17" fill="#f4efd8"/><circle cx="556" cy="50" r="15" fill="#27335e"/><g fill="#f4efd8"><circle cx="590" cy="34" r="2"/><circle cx="512" cy="30" r="1.6"/><circle cx="606" cy="72" r="1.6"/></g></g>
<g text-anchor="middle">
<text x="92" y="150" class="tj b" font-size="21">あさ</text><text x="92" y="172" class="t" font-size="13">asa</text>
<text x="250" y="150" class="tj b" font-size="21">ひる</text><text x="250" y="172" class="t" font-size="13">hiru</text>
<text x="412" y="150" class="tj b" font-size="21">ゆうがた</text><text x="412" y="172" class="t" font-size="13">yūgata</text>
<text x="548" y="150" class="tj b" font-size="21">よる</text><text x="548" y="172" class="t" font-size="13">yoru</text>
{rb(170, 208, '午前', 'ごぜん', 15, 9, False)}{rb(480, 208, '午後', 'ごご', 15, 9, False)}
</g></svg>"""

FIGS["compass"] = f"""<svg viewBox="0 -18 640 284" role="img" aria-label="Directions: north, south, east, west, left and right">
<circle cx="170" cy="118" r="92" class="f-acc2"/><circle cx="170" cy="118" r="78" class="f-paper"/>
<path d="M170 52 L186 118 L154 118 Z" class="f-acc"/><path d="M170 184 L186 118 L154 118 Z" class="f-soft2"/><circle cx="170" cy="118" r="8" class="f-ink"/>
<g text-anchor="middle">
{rb(170, 18, '北', 'きた', 20, 11, False)}{rb(170, 256, '南', 'みなみ', 20, 11, False)}
{rb(46, 128, '西', 'にし', 20, 11, False)}
{rb(296, 128, '東', 'ひがし', 20, 11, False)}
</g>
<ellipse cx="480" cy="186" rx="34" ry="6" class="f-shadow"/><circle cx="480" cy="128" r="30" class="f-leaf"/><path d="M480 84 l12 18 h-24 z" class="f-leaf"/><circle cx="480" cy="128" r="14" class="f-black"/>
<path d="M440 120 H376 M392 106 L374 120 L392 134" class="s-acc" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M520 120 H584 M568 106 L586 120 L568 134" class="s-acc2" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<g text-anchor="middle">
{rb(392, 86, '左', 'ひだり', 22, 11, False)}<text x="392" y="160" class="t" font-size="13">hidari</text>
{rb(570, 86, '右', 'みぎ', 22, 11, False)}<text x="570" y="160" class="t" font-size="13">migi</text>
</g></svg>"""
