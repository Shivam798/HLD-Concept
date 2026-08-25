# -*- coding: utf-8 -*-
"""Did every character in the HTML actually get painted into the PDF?

The recovered subsets paint blank for glyphs they never carried, so a page can
look complete to the layout engine and still be missing words. Compare the
visible characters of each source page against the text extracted from the
rendered page.
"""
import collections
import io
import re
import sys
import html as htmllib

import fitz

htmlfile, pdffile = sys.argv[1], sys.argv[2]
src = io.open(htmlfile, encoding='utf-8').read()
pages = re.split(r'<div class="page', src)[1:]
doc = fitz.open(pdffile)
bad = 0
for i, chunk in enumerate(pages):
    chunk = chunk.split('>', 1)[1] if '>' in chunk else chunk
    txt = re.sub(r'<[^>]+>', ' ', chunk)
    txt = htmllib.unescape(txt)
    want = collections.Counter(c for c in txt if not c.isspace())
    got = collections.Counter(c for c in doc[i].get_text() if not c.isspace())
    miss = {k: want[k] - got.get(k, 0) for k in want if want[k] > got.get(k, 0)}
    if miss:
        bad += 1
        print('page %d missing: %s' % (i + 1, ', '.join(
            '%r x%d' % (k, v) for k, v in sorted(miss.items()))))
print('pages=%d  html_pages=%d  %s' % (len(doc), len(pages),
                                       'ALL GLYPHS PRESENT' if not bad else 'MISSING GLYPHS'))
