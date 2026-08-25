#!/bin/zsh
# Chrome needs the virtual time budget: with 13 local @font-face files it will
# otherwise snapshot the page while faces are still loading and paint nothing.
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for f in "$@"; do
  "$CH" --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=20000 \
        --run-all-compositor-stages-before-draw --print-to-pdf="${f%.html}.pdf" "$f" 2>/dev/null
  echo "rendered ${f%.html}.pdf"
done
