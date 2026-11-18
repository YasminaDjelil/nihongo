# Nihongo

My Japanese study notes for JLPT N5 and N4, turned into a little web app I can keep on my phone.

I made this for my own study. Anyone is welcome to use it.

## How it was made

The lessons come from a French Japanese course written by people. That part is human work, and I use it with permission.

Everything around the lessons was built with the help of an AI assistant (Claude): the interface and its code, the illustrations, and the flashcard drawings. The AI also translated the course into English, Portuguese and Arabic, corrected the mistakes it found in the original, and wrote the short word meanings, the kanji list, the JLPT word lists and the Japanese button labels.

No native speaker or teacher has checked the result, so expect the odd mistake. If you spot one, open an issue.

## What's in it

- 25 lessons, from hiragana up to basic keigo
- vocab lists you can flip into flashcards
- exercises with the answers hidden until you want them
- tap any Japanese text to hear it
- search across vocabulary, grammar points and example sentences
- the full JLPT N5 and N4 word lists (about 1,300 words), each one tap away from a deck
- a grammar index listing every pattern with a link to its lesson
- flashcard decks with spaced repetition, with a small drawing on the card for almost every word
- at the end of each lesson, the list of kanji to learn with it. Kanji study itself (stroke order, practice sheets, tracking) lives in a separate app, [Kanji](https://github.com/YasminaDjelil/kanji)
- listening practice: hear a sentence, write it in your notebook, then check
- furigana over the kanji in example sentences, with a switch to turn it off
- an optional mode where the app's own buttons turn Japanese little by little as lessons are finished
- one-file backup of all progress (decks, reviews, finished lessons), with a reminder in Today

It's built to be used next to a paper notebook. There are no points, streaks or levels.

## Using it on a phone

Open the site in Safari, give it half a minute to pull down the audio, then Share → Add to Home Screen. After that it works offline.

On Android, Chrome shows an "Install app" option in its menu.

Progress is stored in the browser on that one device. Use Back up now in the Today tab every so often.

## Changing something and rebuilding

The site is generated. Don't edit `index.html` by hand; edit the files in `src/` and rebuild. You only need Python 3.

```
./build.sh
```

That rewrites `index.html`, copies the service worker, manifest and icons into place, and also makes `japanese-course-n5-n4.html`, the whole course as a single offline file (not committed, it's 18 MB).

Where things are in `src/`:

| What you want to change | File |
|---|---|
| Lesson text, examples, vocabulary, exercises | `intro.txt`, `n5a.txt`, `n5b.txt`, `n4a.txt`, `n4b.txt`, `n4c.txt` |
| French, Portuguese, Arabic translations of the lessons | `tr_fr.json`, `tr_pt.json`, `tr_ar.json` |
| Button and label text in all four languages | `ui.json` |
| Layout, styles and all the app's behaviour | `template.html` |
| Lesson illustrations | `figs.py` |
| Flashcard drawings | `icons.py`, `icons2.py`, `icons3.py` |
| Which kanji are listed with the lessons, and their meanings | `kanji.tsv`, `kanji_x.tsv` |
| JLPT word lists (word, reading, English, French) | `words_n5.txt`, `words_n4.txt` |
| Extra word meanings shown when you tap a word | `gloss_extra.json` |
| Furigana rules | `furi.py` |
| Service worker, manifest, icons | `static/` |

The lesson files use a small line-based format: `=lesson` starts a lesson, `ex:` is an example (Japanese | reading | translation), `vocab:` starts a word list, `q:` and `ans:` are exercises. Looking at any lesson file makes it clear.

If you change a lesson line in English, its translations are matched by the English text, so the same line in the `tr_*.json` files needs updating too, or that line will show in English.

Before publishing, raise the version at the top of `src/static/sw.js` (`nihongo-v34` → `nihongo-v35`) and run `./build.sh` again. Phones hang on to the old copy otherwise, which confused me the first time.

The audio in `audio.json` was recorded with Google Cloud Text-to-Speech. Anything without a clip falls back to the device's own Japanese voice.

To record what's missing (new sentences, or words added to the lists): run `./build.sh`, open `japanese-course-n5-n4.html` on a computer, go to Settings → Cloud voice, paste a Google Cloud Text-to-Speech API key, pick the same voice in the Voice menu, and press Download all sounds. It only records the missing clips. When it finishes, press Save audio.json and put that file in the repo in place of the old one. The key stays in the browser tab and is never saved.

## Files

- `index.html` is the whole course
- `audio.json` is the recorded audio, about 20 MB
- `sw.js` and `manifest.webmanifest` are what make it installable and offline
- the `icon-*.png` files are the home screen icon
- `src/` is everything the site is built from
- `build.sh` rebuilds it

## Licence

Free to use, share and adapt, with credit, for non-commercial purposes, as long as adaptations keep the same licence: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). The full text is in `LICENSE`.

Audio made with Google Cloud Text-to-Speech.
