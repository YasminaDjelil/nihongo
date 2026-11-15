#!/bin/sh
# Rebuilds the site from the files in src/. Needs only Python 3.
set -e
cd "$(dirname "$0")"
python3 src/build.py . pwa                 # writes index.html (and rewrites audio.json unchanged)
cp src/static/* .                          # service worker, manifest and icons
python3 src/build.py japanese-course-n5-n4.html   # optional: the whole course as one offline file
echo "Done. Remember to raise the version at the top of src/static/sw.js before publishing."
