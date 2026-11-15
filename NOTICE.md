# Third-party material

Not everything here is mine, and not everything is under the licence in `LICENSE`.

## KanjiVG (kanji stroke order)

The stroke-order drawings for the 247 kanji come from [KanjiVG](https://kanjivg.tagaini.net/),
copyright © Ulrich Apel, licensed under
[Creative Commons Attribution-Share Alike 3.0](https://creativecommons.org/licenses/by-sa/3.0/).

- The stroke paths are in `src/vendor/kanjivg/strokes.json`, copied unchanged from KanjiVG's SVG files and gathered into one file, next to the project's `COPYING` file.
- The same stroke data is embedded in `index.html` so the app works offline.

This data stays under CC BY-SA 3.0. The non-commercial condition in `LICENSE` does not apply to it.

## JLPT word lists

The JLPT publishes no official vocabulary list. The N5 and N4 lists in `src/words_n5.txt` and
`src/words_n4.txt` were compiled for this project with the help of AI, following the lists learners
commonly use, with meanings written in English and French. Every reading was checked against the
JMdict dictionary (EDRDG); no JMdict text is included.

## Audio

The clips in `audio.json` were generated with Google Cloud Text-to-Speech (voice `Chirp3-HD-Achernar`).

## The original course

The lessons are adapted from a French Japanese course written by people. It is used here with permission.
