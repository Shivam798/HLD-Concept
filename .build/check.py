# -*- coding: utf-8 -*-
"""Verify the regenerated pages: no font fallback, nothing off-page, no clipping."""
import sys
import fitz

OK_FONTS = ('SegoeUI', 'SegoeUI-Bold', 'SegoeUI-Italic', 'SegoeUI-Semibold',
            'SegoeUIBlack', 'SegoeUISymbol', 'Menlo-Regular',
            'Selawik-Regular', 'Selawik-Bold', 'Selawik-Semibold')
LEFT, RIGHT, TOP, BOTTOM = 36.0, 559.5, 30.0, 812.0

doc = fitz.open(sys.argv[1] if len(sys.argv) > 1 else 'part2.pdf')
bad_font, oob, empty = [], [], []
for i, page in enumerate(doc):
    spans = []
    for b in page.get_text('dict')['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            for s in l['spans']:
                if not s['text'].strip():
                    continue
                spans.append(s)
                if s['font'] not in OK_FONTS:
                    bad_font.append((i + 1, s['font'], s['text'][:40]))
                x0, y0, x1, y1 = s['bbox']
                if x0 < LEFT - 0.6 or x1 > RIGHT + 0.6 or y0 < TOP or y1 > BOTTOM:
                    oob.append((i + 1, round(x0, 1), round(y0, 1), round(x1, 1),
                                round(y1, 1), s['text'][:40]))
    if not spans:
        empty.append(i + 1)
    # deepest painted content, to judge how full each page is
    ymax = max([s['bbox'][3] for s in spans] or [0])
    for d in page.get_drawings():
        r = d['rect']
        if r.height > 800:      # the page background, not content
            continue
        ymax = max(ymax, r.y1)
    print('page %2d  spans=%3d  content ends at y=%6.1f  (%.0f%% of the text block)'
          % (i + 1, len(spans), ymax, 100.0 * (ymax - 36) / (808 - 36)))

print('\n--- fallback fonts (must be empty) ---')
for r in bad_font:
    print('  p%-3d %-16s %s' % r)
print('--- out of bounds (must be empty) ---')
for r in oob:
    print('  p%-3d (%.1f,%.1f)-(%.1f,%.1f) %s' % r)
print('--- blank pages (must be empty) ---', empty)
print('\nRESULT:', 'FAIL' if (bad_font or oob or empty) else 'PASS')
