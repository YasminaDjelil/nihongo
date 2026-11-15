# Small flat illustrations for practice cards (96x96). Colours come from the same CSS classes as the lesson figures.
import json, math
W = 'class="f-white s-soft" stroke-width="2"'
BR = '#8a5a3a'

def mp(cx, by, cls, s=1.0, hair='f-black'):
    """Mini person standing on baseline by."""
    return (f'<g transform="translate({cx} {by}) scale({s})"><path d="M-15 0 v-22 a15 15 0 0 1 30 0 v22z" class="{cls}"/>'
            f'<circle cx="0" cy="-48" r="13" class="f-skin"/><path d="M-13.5 -50 a13.5 13.5 0 0 1 27 0 q-4 -6 -13.5 -5.5 q-9.5 -.5 -13.5 5.5z" class="{hair}"/>'
            '<circle cx="-4.5" cy="-47" r="1.6" class="f-black"/><circle cx="4.5" cy="-47" r="1.6" class="f-black"/></g>')

def face(mouth, extra=''):
    return ('<circle cx="48" cy="48" r="36" class="f-gold"/><circle cx="35" cy="42" r="4" class="f-black"/><circle cx="61" cy="42" r="4" class="f-black"/>' + mouth + extra)

def sun(cx=48, cy=48, r=17, rr=30):
    rays = ''.join(f'<rect x="{cx-2.5}" y="{cy-rr-6}" width="5" height="11" rx="2.5" class="f-gold" transform="rotate({a} {cx} {cy})"/>' for a in range(0, 360, 45))
    return rays + f'<circle cx="{cx}" cy="{cy}" r="{r}" class="f-gold"/>'

def cloud(cx, cy, s=1):
    return (f'<g transform="translate({cx} {cy}) scale({s})"><path d="M-26 10 a12 12 0 0 1 2 -24 a16 16 0 0 1 30 -4 a13 13 0 0 1 18 28z" {W}/></g>')

def swatch(c):
    return f'<circle cx="48" cy="48" r="32" fill="{c}" class="s-soft" stroke-width="2"/>'

def arrow(rot):
    return f'<g transform="rotate({rot} 48 48)"><path d="M48 12 L74 44 H58 V84 H38 V44 H22Z" class="f-acc2"/></g>'

def compass(rot, label):
    return ('<circle cx="48" cy="48" r="38" class="f-acc2"/><circle cx="48" cy="48" r="31" class="f-paper"/>'
            f'<g transform="rotate({rot} 48 48)"><path d="M48 20 L56 48 H40Z" class="f-acc"/><path d="M48 76 L56 48 H40Z" class="f-soft2"/></g><circle cx="48" cy="48" r="4" class="f-ink"/>')

def thermo(cls, y):
    return (f'<rect x="39" y="8" width="18" height="60" rx="9" {W}/><circle cx="48" cy="74" r="15" class="{cls}"/><rect x="44" y="{y}" width="8" height="{74-y}" rx="3" class="{cls}"/>')

def pine(cx, by, s=1):
    return (f'<g transform="translate({cx} {by}) scale({s})"><rect x="-4" y="-12" width="8" height="12" fill="{BR}"/><path d="M0 -66 l15 24 h-7 l12 20 h-8 l12 12 h-48 l12 -12 h-8 l12 -20 h-7z" class="f-leaf"/></g>')

PETALS = ''.join(f'<ellipse cx="48" cy="24" rx="12" ry="19" class="f-pink" transform="rotate({a} 48 48)"/>' for a in range(0, 360, 72))
FLAKE = ''.join(f'<g transform="rotate({a} 48 48)"><path d="M48 48 V10 M48 22 l-9 -9 M48 22 l9 -9" class="s-acc2" stroke-width="5" fill="none" stroke-linecap="round"/></g>' for a in range(0, 360, 60))
PENCIL = '<g transform="rotate(38 66 46)"><rect x="60" y="14" width="12" height="50" class="f-gold"/><path d="M60 64 h12 l-6 14z" class="f-skin"/><rect x="60" y="7" width="12" height="9" rx="2" class="f-pink"/></g>'
BOWL = ('<path d="M34 10 q-5 7 0 14 M48 8 q-5 7 0 14 M62 10 q-5 7 0 14" class="s-soft" stroke-width="3" fill="none" stroke-linecap="round"/>'
        f'<path d="M24 46 a24 17 0 0 1 48 0z" {W}/><path d="M12 48 h72 a36 32 0 0 1 -72 0z" class="f-acc"/><rect x="8" y="44" width="80" height="7" rx="3.5" class="f-ink"/>')

I = {
 'book': '<rect x="18" y="12" width="60" height="72" rx="6" class="f-acc2"/><rect x="26" y="12" width="6" height="72" class="f-black" opacity=".25"/><rect x="40" y="28" width="28" height="7" rx="3.5" class="f-white"/><rect x="40" y="42" width="20" height="5" rx="2.5" class="f-white" opacity=".7"/>',
 'openbook': f'<path d="M48 26 Q30 14 10 20 V74 Q30 68 48 80Z" {W}/><path d="M48 26 Q66 14 86 20 V74 Q66 68 48 80Z" {W}/><path d="M18 34 q12 -3 22 3 M18 46 q12 -3 22 3 M18 58 q12 -3 22 3 M56 37 q10 -6 22 -3 M56 49 q10 -6 22 -3 M56 61 q10 -6 22 -3" class="s-soft" stroke-width="2.5" fill="none"/>',
 'apple': '<path d="M48 34 C30 20 12 36 18 58 C22 76 36 88 48 82 C60 88 74 76 78 58 C84 36 66 20 48 34Z" class="f-acc"/><path d="M48 34 q2 -12 10 -16" class="s-black" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M52 26 q14 -12 22 0 q-12 8 -22 0z" class="f-leaf"/><circle cx="33" cy="50" r="5" class="f-white" opacity=".5"/>',
 'dog': f'<path d="M24 38 q-12 -4 -9 24 q11 2 13 -10z M72 38 q12 -4 9 24 q-11 2 -13 -10z" fill="{BR}"/><ellipse cx="48" cy="50" rx="27" ry="26" fill="#c98b4e"/><ellipse cx="48" cy="62" rx="14" ry="11" class="f-white"/><ellipse cx="48" cy="57" rx="5.5" ry="4" class="f-black"/><circle cx="37" cy="44" r="3.4" class="f-black"/><circle cx="59" cy="44" r="3.4" class="f-black"/><path d="M43 66 q5 9 10 0z" class="f-pink"/>',
 'cat': '<path d="M23 46 L25 14 L45 30Z M73 46 L71 14 L51 30Z" fill="#e79a45"/><circle cx="48" cy="54" r="28" fill="#e79a45"/><circle cx="37" cy="50" r="4" class="f-black"/><circle cx="59" cy="50" r="4" class="f-black"/><path d="M44 60 l4 4 l4 -4z" class="f-pink"/><path d="M48 64 v4 M30 60 l-14 -3 M30 66 l-14 3 M66 60 l14 -3 M66 66 l14 3" class="s-black" stroke-width="2" stroke-linecap="round"/>',
 'house': f'<rect x="20" y="42" width="56" height="42" {W}/><path d="M8 46 L48 12 L88 46Z" class="f-acc"/><rect x="42" y="58" width="15" height="26" rx="2" class="f-acc2"/><rect x="26" y="52" width="11" height="11" class="f-sky"/><rect x="62" y="52" width="9" height="11" class="f-sky"/>',
 'bank': '<path d="M8 36 L48 12 L88 36Z" class="f-ink"/><circle cx="48" cy="27" r="5" class="f-gold"/><rect x="12" y="36" width="72" height="7" class="f-ink"/><rect x="19" y="46" width="9" height="28" class="f-acc2"/><rect x="35" y="46" width="9" height="28" class="f-acc2"/><rect x="52" y="46" width="9" height="28" class="f-acc2"/><rect x="68" y="46" width="9" height="28" class="f-acc2"/><rect x="10" y="76" width="76" height="8" class="f-ink"/>',
 'museum': '<path d="M8 36 L48 12 L88 36Z" class="f-acc"/><rect x="12" y="36" width="72" height="7" class="f-soft2"/><rect x="19" y="46" width="9" height="28" class="f-gold"/><rect x="35" y="46" width="9" height="28" class="f-gold"/><rect x="52" y="46" width="9" height="28" class="f-gold"/><rect x="68" y="46" width="9" height="28" class="f-gold"/><rect x="10" y="76" width="76" height="8" class="f-soft2"/>',
 'hospital': f'<rect x="14" y="18" width="68" height="66" rx="6" {W}/><path d="M42 28 h12 v10 h10 v12 h-10 v10 h-12 v-10 h-10 v-12 h10z" class="f-acc"/><rect x="41" y="68" width="14" height="16" class="f-acc2"/>',
 'hotel': '<rect x="22" y="10" width="52" height="74" rx="4" class="f-acc2"/>' + ''.join(f'<rect x="{x}" y="{y}" width="9" height="9" class="f-gold"/>' for y in (18, 32, 46) for x in (29, 43.5, 58)) + '<rect x="41" y="66" width="14" height="18" class="f-white"/>',
 'letter': f'<rect x="10" y="24" width="76" height="50" rx="6" {W}/><path d="M12 28 L48 54 L84 28" class="s-acc" stroke-width="4" fill="none" stroke-linejoin="round"/>',
 'library': '<rect x="12" y="12" width="72" height="72" rx="4" class="f-soft2"/>' + ''.join(f'<rect x="{18+i*10.5}" y="18" width="8" height="26" class="{c}"/>' for i, c in enumerate(['f-acc', 'f-acc2', 'f-gold', 'f-leaf', 'f-acc', 'f-acc2'])) + ''.join(f'<rect x="{18+i*10.5}" y="52" width="8" height="26" class="{c}"/>' for i, c in enumerate(['f-leaf', 'f-gold', 'f-acc2', 'f-acc', 'f-pink', 'f-leaf'])) + '<rect x="12" y="45" width="72" height="5" class="f-black" opacity=".25"/>',
 'film': '<rect x="12" y="38" width="72" height="44" rx="5" class="f-ink"/><rect x="12" y="20" width="72" height="14" rx="3" class="f-ink"/><path d="M22 20 l8 14 M40 20 l8 14 M58 20 l8 14 M76 20 l6 10" class="s-paper" stroke-width="6"/><path d="M41 50 l17 10 l-17 10z" class="f-acc"/>',
 'umbrella': '<path d="M10 50 A38 36 0 0 1 86 50 Q76 42 67 50 Q57 42 48 50 Q39 42 29 50 Q20 42 10 50Z" class="f-acc"/><path d="M48 50 V78 q0 8 -9 8" class="s-ink" stroke-width="4" fill="none" stroke-linecap="round"/>',
 'train': '<path d="M30 72 l-10 14 M66 72 l10 14" class="s-ink" stroke-width="4" stroke-linecap="round"/><rect x="18" y="12" width="60" height="62" rx="13" class="f-acc2"/><rect x="26" y="21" width="44" height="23" rx="5" class="f-sky"/><circle cx="32" cy="59" r="5" class="f-gold"/><circle cx="64" cy="59" r="5" class="f-gold"/>',
 'station': f'<rect x="22" y="56" width="5" height="28" class="f-ink"/><rect x="69" y="56" width="5" height="28" class="f-ink"/><rect x="10" y="24" width="76" height="34" rx="4" {W}/><rect x="11" y="46" width="74" height="6" class="f-leaf"/><text x="48" y="42" text-anchor="middle" class="tj b f-black" font-size="14">えき</text>',
 'head': '<circle cx="48" cy="52" r="28" class="f-skin"/><path d="M19 50 a29 29 0 0 1 58 0 q-9 -13 -29 -12 q-20 -1 -29 12z" class="f-black"/><circle cx="38" cy="54" r="3" class="f-black"/><circle cx="58" cy="54" r="3" class="f-black"/><path d="M40 65 q8 7 16 0" class="s-black" stroke-width="2.5" fill="none" stroke-linecap="round"/>',
 'hand': '<rect x="30" y="42" width="38" height="42" rx="13" class="f-skin"/><rect x="31" y="20" width="8.5" height="34" rx="4.2" class="f-skin"/><rect x="40.5" y="12" width="8.5" height="40" rx="4.2" class="f-skin"/><rect x="50" y="14" width="8.5" height="40" rx="4.2" class="f-skin"/><rect x="59.5" y="22" width="8.5" height="34" rx="4.2" class="f-skin"/><rect x="12" y="50" width="26" height="10" rx="5" class="f-skin" transform="rotate(32 25 55)"/>',
 'foot': '<path d="M32 10 h22 v40 q28 8 32 22 q2 10 -9 10 H34 q-9 0 -9 -11z" class="f-skin"/>',
 'magazine': '<rect x="20" y="10" width="56" height="76" rx="4" class="f-pink"/><rect x="28" y="18" width="40" height="9" rx="2" class="f-white"/><rect x="28" y="33" width="40" height="32" rx="2" class="f-acc2"/><rect x="28" y="71" width="24" height="5" rx="2.5" class="f-white"/>',
 'newspaper': f'<rect x="12" y="16" width="72" height="66" rx="3" {W}/><rect x="20" y="24" width="56" height="9" class="f-ink"/><rect x="20" y="39" width="24" height="20" class="f-soft2"/><path d="M50 41 h26 M50 49 h26 M50 57 h26 M20 66 h56 M20 74 h40" class="s-soft" stroke-width="3"/>',
 'camera': '<rect x="30" y="18" width="24" height="14" rx="3" class="f-ink"/><rect x="10" y="28" width="76" height="52" rx="9" class="f-ink"/><circle cx="48" cy="54" r="18" class="f-white"/><circle cx="48" cy="54" r="12" class="f-acc2"/><circle cx="73" cy="39" r="4" class="f-gold"/>',
 'bed': f'<rect x="8" y="28" width="7" height="56" rx="2" class="f-soft2"/><rect x="81" y="46" width="7" height="38" rx="2" class="f-soft2"/><rect x="12" y="52" width="72" height="22" rx="4" class="f-acc2"/><rect x="17" y="40" width="26" height="15" rx="6" {W}/>',
 'phone': '<rect x="27" y="6" width="42" height="84" rx="8" class="f-ink"/><rect x="32" y="16" width="32" height="58" rx="2" class="f-sky"/><circle cx="48" cy="82" r="3.5" class="f-paper"/>',
 'doctor': f'<path d="M20 88 v-20 a28 24 0 0 1 56 0 v20z" {W}/><circle cx="48" cy="30" r="16" class="f-skin"/><path d="M31.500 28 a16.500 16.500 0 0 1 33 0 q-5 -7 -16.500 -6.500 q-11.500 -.5 -16.500 6.500z" class="f-black"/><circle cx="42" cy="32" r="2" class="f-black"/><circle cx="54" cy="32" r="2" class="f-black"/><path d="M57 60 h6 v5 h5 v6 h-5 v5 h-6 v-5 h-5 v-6 h5z" class="f-acc"/>',
 'teacher': '<rect x="42" y="10" width="48" height="36" rx="3" class="f-leaf"/><text x="66" y="36" text-anchor="middle" class="tj b f-white" font-size="20">あ</text><path d="M38 52 L52 38" class="s-ink" stroke-width="3" stroke-linecap="round"/>' + mp(28, 88, 'f-acc2', 1.05),
 'pill': f'<g transform="rotate(-35 48 48)"><rect x="14" y="32" width="68" height="32" rx="16" {W}/><path d="M48 32 h18 a16 16 0 0 1 0 32 h-18z" class="f-acc"/></g>',
 'tree': f'<rect x="43" y="54" width="10" height="32" rx="2" fill="{BR}"/><circle cx="48" cy="34" r="24" class="f-leaf"/><circle cx="29" cy="48" r="15" class="f-leaf"/><circle cx="67" cy="48" r="15" class="f-leaf"/>',
 'park': f'<ellipse cx="48" cy="84" rx="42" ry="6" class="f-leaf" opacity=".5"/><rect x="24" y="52" width="8" height="32" rx="2" fill="{BR}"/><circle cx="28" cy="36" r="20" class="f-leaf"/><circle cx="14" cy="48" r="11" class="f-leaf"/><circle cx="42" cy="48" r="11" class="f-leaf"/><rect x="50" y="54" width="38" height="6" rx="2" class="f-gold"/><rect x="50" y="66" width="38" height="6" rx="2" class="f-gold"/><path d="M56 60 v24 M82 60 v24" class="s-ink" stroke-width="4" stroke-linecap="round"/>',
 'forest': pine(74, 80, .8) + pine(24, 82, .9) + pine(48, 88, 1.1),
 'leaf': '<path d="M18 78 C12 40 38 14 80 16 C82 58 56 84 18 78Z" class="f-leaf"/><path d="M20 76 L64 32" class="s-white" stroke-width="3" stroke-linecap="round" opacity=".7"/>',
 'flower': PETALS + '<circle cx="48" cy="48" r="9" class="f-gold"/>',
 'sun': sun(),
 'maple': '<path d="M48 8 l9 18 l18 -7 l-7 18 l18 9 l-20 7 l2 20 l-16 -11 l-4 22 l-4 -22 l-16 11 l2 -20 l-20 -7 l18 -9 l-7 -18 l18 7z" class="f-acc"/>',
 'snow': FLAKE,
 'friends': mp(31, 86, 'f-acc2', 1.1) + mp(66, 86, 'f-acc', 1.1),
 'family': mp(24, 86, 'f-acc2', 1.05) + mp(72, 86, 'f-acc', 1.05) + mp(48, 88, 'f-gold', .72),
 'child': mp(48, 86, 'f-gold', 1.25),
 'bag': '<path d="M36 34 v-8 a12 12 0 0 1 24 0 v8" class="s-ink" stroke-width="4" fill="none"/><path d="M20 32 h56 l6 54 h-68z" class="f-acc"/><circle cx="36" cy="42" r="3" class="f-white"/><circle cx="60" cy="42" r="3" class="f-white"/>',
 'mountain': '<path d="M4 82 L40 20 L60 56 L70 42 L92 82Z" class="f-mount"/><path d="M40 20 L52 41 L45 37 L39 46 L33 36 L28.500 40Z" class="f-white"/>',
 'dict': f'<rect x="14" y="10" width="68" height="76" rx="7" class="f-leaf"/><rect x="18" y="72" width="64" height="10" rx="3" {W}/><text x="48" y="50" text-anchor="middle" class="tj b f-white" font-size="24">あA</text>',
 'music': '<ellipse cx="30" cy="72" rx="13" ry="10" class="f-acc2"/><ellipse cx="68" cy="64" rx="13" ry="10" class="f-acc2"/><path d="M40 72 V22 L78 12 V64" class="s-acc2" stroke-width="6" fill="none" stroke-linejoin="round"/><path d="M40 22 L78 12 V26 L40 36Z" class="f-acc2"/>',
 'earth': '<circle cx="48" cy="48" r="37" fill="#3f7fd0"/><path d="M28 24 q16 -10 26 2 q-2 14 -13 14 q-5 12 -14 5 q-8 -11 1 -21z" class="f-leaf"/><path d="M56 52 q16 -5 20 9 q-5 16 -16 16 q-9 -9 -4 -25z" class="f-leaf"/>',
 'bulb': '<path d="M48 8 a26 26 0 0 1 15 47 v9 h-30 v-9 a26 26 0 0 1 15 -47z" class="f-gold"/><rect x="35" y="68" width="26" height="7" rx="3.5" class="f-soft2"/><rect x="39" y="78" width="18" height="7" rx="3.5" class="f-soft2"/>',
 'flame': '<path d="M48 6 C60 26 78 38 74 62 A26 26 0 0 1 22 62 C20 46 31 40 33 26 C42 33 44 22 48 6Z" class="f-acc"/><path d="M48 44 C57 55 61 60 59 70 A11 11 0 0 1 37 70 C37 60 46 55 48 44Z" class="f-gold"/>',
 'ship': f'<rect x="42" y="14" width="13" height="22" class="f-acc"/><rect x="28" y="36" width="40" height="22" {W}/><path d="M8 56 h80 l-11 22 h-58z" class="f-acc2"/><path d="M4 88 q8 -7 16 0 t16 0 t16 0 t16 0 t16 0" class="s-acc2" stroke-width="3" fill="none"/>',
 'shop': f'<rect x="16" y="38" width="64" height="46" {W}/><path d="M12 16 h72 l5 24 h-82z" class="f-acc"/><path d="M30 16 h12 v24 h-14z M54 16 h12 l2 24 h-14z" class="f-white"/><rect x="44" y="56" width="16" height="28" class="f-acc2"/><rect x="22" y="52" width="15" height="15" class="f-sky"/>',
 'egg': f'<path d="M48 8 C68 8 80 42 80 58 A32 30 0 0 1 16 58 C16 42 28 8 48 8Z" {W}/>',
 'carrot': '<g transform="rotate(32 48 48)"><path d="M34 30 h28 l-14 60z" fill="#f08a2c"/><path d="M48 30 q-16 -12 -9 -24 q9 7 9 24 q0 -17 9 -24 q7 12 -9 24z" class="f-leaf"/></g>',
 'window': '<rect x="14" y="12" width="68" height="72" rx="4" class="f-soft2"/><rect x="21" y="19" width="25" height="28" class="f-sky"/><rect x="50" y="19" width="25" height="28" class="f-sky"/><rect x="21" y="51" width="25" height="26" class="f-sky"/><rect x="50" y="51" width="25" height="26" class="f-sky"/>',
 'clock': '<circle cx="48" cy="48" r="38" class="f-acc2"/><circle cx="48" cy="48" r="31" class="f-paper"/><path d="M48 48 V26 M48 48 L64 56" class="s-ink" stroke-width="5" stroke-linecap="round"/><circle cx="48" cy="48" r="4" class="f-acc"/>',
 'shoe': f'<path d="M8 60 v-24 h24 q4 17 24 21 q30 4 32 14 v3 h-80z" class="f-acc"/><rect x="8" y="72" width="80" height="9" rx="3" {W}/>',
 'sock': '<path d="M32 8 h28 v46 l22 14 q9 6 3 15 q-5 6 -13 4 l-32 -12 q-8 -4 -8 -13z" class="f-acc2"/><rect x="32" y="8" width="28" height="11" class="f-white" opacity=".85"/>',
 'picture': '<rect x="10" y="16" width="76" height="64" rx="4" class="f-gold"/><rect x="18" y="24" width="60" height="48" class="f-sky"/><circle cx="64" cy="38" r="7" class="f-acc"/><path d="M18 72 L40 40 L54 60 L62 50 L78 72Z" class="f-mount"/>',
 'dish': BOWL,
 'coin': '<circle cx="48" cy="48" r="36" class="f-gold"/><circle cx="48" cy="48" r="28" fill="none" class="s-white" stroke-width="2" opacity=".6"/><text x="48" y="61" text-anchor="middle" class="t b f-black" font-size="38">¥</text>',
 'fruit': '<circle cx="34" cy="58" r="22" fill="#f08a2c"/><circle cx="64" cy="54" r="22" class="f-acc"/><path d="M64 34 q1 -10 8 -13" class="s-black" stroke-width="3.5" fill="none" stroke-linecap="round"/><path d="M34 37 q10 -10 18 -2 q-9 8 -18 2z" class="f-leaf"/>',
 'laptop': '<rect x="16" y="16" width="64" height="46" rx="5" class="f-ink"/><rect x="22" y="22" width="52" height="34" class="f-sky"/><path d="M6 66 h84 l-7 13 h-70z" class="f-soft2"/>',
 'rain': cloud(48, 34, 1.1) + '<path d="M30 60 l-6 16 M48 60 l-6 16 M66 60 l-6 16" class="s-acc2" stroke-width="5" stroke-linecap="round"/>',
 'sunny': sun(38, 40, 15, 26) + cloud(60, 64, .95),
 'cap': '<path d="M26 48 v18 q22 15 44 0 v-18 l-22 11z" class="f-acc2"/><path d="M4 40 L48 20 L92 40 L48 60Z" class="f-ink"/><rect x="83" y="40" width="3.5" height="24" class="f-gold"/><circle cx="84.700" cy="66" r="5" class="f-gold"/>',
 'toy': '<rect x="14" y="48" width="34" height="34" rx="4" class="f-acc"/><rect x="50" y="48" width="34" height="34" rx="4" class="f-acc2"/><path d="M48 12 L68 46 H28Z" class="f-gold"/>',
 'paper': f'<rect x="16" y="10" width="54" height="76" rx="4" {W}/><path d="M26 26 h34 M26 38 h34 M26 50 h34 M26 62 h20" class="s-soft" stroke-width="3" stroke-linecap="round"/>' + PENCIL,
 'moon': '<circle cx="48" cy="48" r="39" fill="#27335e"/><path d="M58 22 a27 27 0 1 0 15 42 a23 23 0 0 1 -15 -42z" fill="#f4efd8"/><circle cx="70" cy="30" r="2" fill="#f4efd8"/><circle cx="28" cy="26" r="1.600" fill="#f4efd8"/>',
 'sunrise': ''.join(f'<rect x="45.500" y="18" width="5" height="12" rx="2.500" class="f-gold" transform="rotate({a} 48 66)"/>' for a in (-60, -30, 0, 30, 60)) + '<path d="M20 66 a28 28 0 0 1 56 0z" class="f-gold"/><rect x="6" y="66" width="84" height="7" rx="3.500" class="f-acc2"/><rect x="22" y="78" width="52" height="5" rx="2.500" class="f-acc2" opacity=".5"/>',
 'coffee': f'<path d="M34 8 q-5 7 0 14 M50 6 q-5 7 0 14" class="s-soft" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M68 40 h6 a10 10 0 0 1 0 20 h-9" class="s-soft" stroke-width="5" fill="none"/><path d="M16 32 h54 v22 a27 24 0 0 1 -54 0z" {W}/><ellipse cx="43" cy="34" rx="24" ry="4.500" fill="{BR}"/><rect x="14" y="80" width="58" height="6" rx="3" class="f-soft2"/>',
 'police': '<path d="M48 8 L82 20 V46 C82 68 65 82 48 88 C31 82 14 68 14 46 V20Z" class="f-acc2"/><path d="M48 26 l6.500 13 l14.500 2 l-10.500 10 l2.500 14 l-13 -7 l-13 7 l2.500 -14 l-10.500 -10 l14.500 -2z" class="f-gold"/>',
 'city': '<rect x="8" y="40" width="24" height="46" class="f-acc2"/><rect x="34" y="14" width="28" height="72" class="f-ink"/><rect x="64" y="32" width="24" height="54" class="f-acc"/>' + ''.join(f'<rect x="{x}" y="{y}" width="6" height="7" class="f-gold"/>' for x, y in [(13, 48), (22, 48), (13, 62), (22, 62), (40, 22), (50, 22), (40, 36), (50, 36), (40, 50), (50, 50), (69, 40), (78, 40), (69, 54), (78, 54)]),
 'road': '<path d="M32 8 h32 l24 80 h-80z" class="f-soft2"/><path d="M48 14 v12 M48 36 v14 M48 62 v18" class="s-white" stroke-width="4" stroke-linecap="round"/>',
 'happy': face('<path d="M32 56 q16 16 32 0" class="s-black" stroke-width="4" fill="none" stroke-linecap="round"/>'),
 'laugh': face('<path d="M30 54 h36 a18 18 0 0 1 -36 0z" class="f-black"/><path d="M38 66 q10 -7 20 0 a18 18 0 0 1 -20 0z" class="f-pink"/>'),
 'sad': face('<path d="M33 66 q15 -13 30 0" class="s-black" stroke-width="4" fill="none" stroke-linecap="round"/>'),
 'cry': face('<path d="M33 66 q15 -13 30 0" class="s-black" stroke-width="4" fill="none" stroke-linecap="round"/>', '<path d="M64 50 q7 11 0 16 q-7 -5 0 -16z" fill="#4f9be8"/>'),
 'sleep': face('<path d="M40 62 q8 5 16 0" class="s-black" stroke-width="3.500" fill="none" stroke-linecap="round"/>').replace('<circle cx="35" cy="42" r="4" class="f-black"/><circle cx="61" cy="42" r="4" class="f-black"/>', '<path d="M29 44 q6 5 12 0 M55 44 q6 5 12 0" class="s-black" stroke-width="3.500" fill="none" stroke-linecap="round"/>') + '<text x="74" y="24" class="t b f-acc2" font-size="20">z</text><text x="84" y="12" class="t b f-acc2" font-size="13">z</text>',
 'palette': '<path d="M48 10 C22 10 8 28 8 48 C8 70 26 86 46 86 C56 86 56 76 52 70 C48 62 56 56 66 58 C80 60 88 52 88 42 C88 24 72 10 48 10Z" class="f-skin"/><circle cx="30" cy="36" r="7" fill="#d6453a"/><circle cx="50" cy="26" r="7" fill="#f2c12e"/><circle cx="70" cy="36" r="7" fill="#2f6fd0"/><circle cx="26" cy="58" r="7" fill="#3f9a5a"/>',
 'chair': '<path d="M32 60 v26 M72 60 v26" class="s-ink" stroke-width="5" stroke-linecap="round"/><rect x="24" y="10" width="14" height="54" rx="6" class="f-acc2"/><rect x="24" y="50" width="56" height="14" rx="6" class="f-acc2"/>',
 'cold': thermo('f-acc2', 56), 'hot': thermo('f-acc', 20),
 'up': arrow(0), 'right': arrow(90), 'down': arrow(180), 'left': arrow(270),
 'north': compass(0, 'N'), 'east': compass(90, 'E'), 'south': compass(180, 'S'), 'west': compass(270, 'W'),
 'red': swatch('#d6453a'), 'blue': swatch('#2f6fd0'), 'yellow': swatch('#f2c12e'), 'white': swatch('#ffffff'), 'black': swatch('#1c1c1e'),
 'green': swatch('#3f9a5a'), 'purple': swatch('#8a55c2'), 'orange': swatch('#f08a2c'), 'brown': swatch('#8a5a3a'),
}

WORDS = {
 'book': '本 教科書 小説', 'openbook': '読みます', 'apple': '林檎', 'dog': '犬', 'cat': '猫', 'house': '家', 'bank': '銀行', 'museum': '博物館 美術館',
 'hospital': '病院', 'hotel': 'ホテル', 'letter': '郵便局', 'library': '図書館', 'film': '映画館 映画', 'umbrella': '傘', 'train': '電車 列車 地下鉄', 'station': '駅',
 'head': '頭', 'hand': '手', 'foot': '足 脚', 'magazine': '雑誌', 'newspaper': '新聞', 'camera': '写真 写真を撮る', 'bed': '部屋', 'phone': '電話', 'doctor': '医者',
 'teacher': '先生', 'pill': '薬', 'tree': '木', 'park': '公園', 'forest': '森', 'leaf': '葉', 'flower': '春 桜 咲く', 'sun': '夏 太陽 昼', 'maple': '秋', 'snow': '冬',
 'friends': '友達', 'family': '家族 両親', 'child': '子供', 'bag': '買い物', 'mountain': '山', 'dict': '辞書', 'music': '音楽', 'earth': '地球 世界', 'bulb': '電気',
 'flame': '火事', 'ship': '船', 'shop': '店 コンビニ スーパー デパート', 'egg': '卵', 'carrot': '野菜', 'window': '窓', 'clock': '時計 時間', 'shoe': '靴', 'sock': '靴下',
 'picture': '絵', 'dish': '食事 料理 食べます', 'coin': 'お金 円', 'fruit': '果物', 'laptop': 'パソコン', 'rain': '雨が降る', 'sunny': '晴れ 天気予報', 'cap': '大学',
 'toy': '玩具', 'paper': '宿題 試験 書きます', 'moon': '夜 今夜 晩 月明かり', 'sunrise': '朝 毎朝 早起き', 'coffee': '喫茶店 漫画喫茶', 'police': '警察署', 'city': '街',
 'road': '通り', 'happy': '嬉しい 幸せな 楽しい', 'laugh': '笑う', 'sad': '悲しい', 'cry': '泣く', 'sleep': '昼寝', 'palette': '色', 'chair': '座席',
 'cold': '寒い 冷たい', 'hot': '暑い', 'up': '上', 'down': '下', 'left': '左', 'right': '右', 'north': '北', 'south': '南', 'east': '東', 'west': '西',
 'red': '赤い', 'blue': '青い', 'yellow': '黄色い', 'white': '白い', 'black': '黒い', 'green': '緑', 'purple': '紫', 'orange': 'オレンジ', 'brown': '茶色',
}

def build_icons():
    w = {}
    for name, ws in WORDS.items():
        assert name in I, name
        for x in (ws.split('|') if '|' in ws else ws.split()): w[x] = name
    return json.dumps({'i': I, 'w': w}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'), w
