# -*- coding: utf-8 -*-
"""Surgical text edits on the already-typeset guide pages.

The pages come out of Chrome/Skia with one Tj per glyph, so the only safe way to
change a word is to lift the whole span, redact its box and re-lay the new text
at the original per-character origins. Digits in Segoe UI are tabular, so a
digit-for-digit swap is pixel-identical; deletions shift the tail of the span
left by exactly the advance of what was removed.
"""
import os
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = {
    'SegoeUI': 'CAAAAA_SegoeUI.ttf',
    'SegoeUI-Bold': 'DAAAAA_SegoeUI-Bold.ttf',
    'SegoeUI-Italic': 'IAAAAA_SegoeUI-Italic.ttf',
    'SegoeUI-Semibold': 'AAAAAA_SegoeUI-Semibold.ttf',
    'SegoeUIBlack': 'BAAAAA_SegoeUIBlack.ttf',
    'SegoeUISymbol': 'QAAAAA_SegoeUISymbol.ttf',
    'SegoeUI-BoldItalic': 'TAAAAA_SegoeUI-BoldItalic.ttf',
    'SegoeUI-SemiboldItalic': 'XAAAAA_SegoeUI-SemiboldItalic.ttf',
}
# faces whose subset is too thin for arbitrary text: fall back to a full cut of
# the same weight (identical outlines, only the subset differs)
FALLBACK = {
    'SegoeUI-Semibold': 'DAAAAA_SegoeUI-Bold.ttf',
}
MENLO = '/System/Library/Fonts/Menlo.ttc'   # the code spans are Type3 cuts of Menlo
_cache = {}


def font_for(name):
    if name in _cache:
        return _cache[name]
    f = FONTS.get(name)
    if f is None:
        if 'T3' in name or 'Menlo' in name or 'mono' in name.lower():
            fo = fitz.Font(fontfile=MENLO)
            _cache[name] = fo
            return fo
        raise KeyError('no ttf for font %r' % name)
    fo = fitz.Font(fontfile=os.path.join(HERE, 'fonts', f))
    _cache[name] = fo
    return fo


def _usable(name, text):
    """pick a font file that actually carries every glyph in `text`"""
    fo = font_for(name)
    if name not in FONTS:          # Type3 code span: Menlo, nothing to swap for
        return fo
    missing = [c for c in text if not fo.has_glyph(ord(c))]
    if not missing and name not in FALLBACK:
        return fo
    for cand in [FALLBACK.get(name)] + list(FONTS.values()):
        if not cand:
            continue
        fo2 = fitz.Font(fontfile=os.path.join(HERE, 'fonts', cand))
        if all(fo2.has_glyph(ord(c)) for c in text):
            return fo2
    if missing:
        raise ValueError('no font carries %r for face %s' % (missing, name))
    return fo


def rgb(color):
    return ((color >> 16) & 255) / 255.0, ((color >> 8) & 255) / 255.0, (color & 255) / 255.0


def find_spans(page, needle):
    """every span on the page whose text contains `needle`"""
    out = []
    for b in page.get_text('rawdict')['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            for s in l['spans']:
                txt = ''.join(c['c'] for c in s['chars'])
                if needle in txt:
                    s['_text'] = txt
                    out.append(s)
    return out


def plan_edit(page, needle, replacement, occurrence=0, must=True, in_span=None):
    """Return an edit descriptor replacing `needle` with `replacement` inside a span."""
    spans = find_spans(page, in_span or needle)
    if in_span is not None:
        spans = [s for s in spans if needle in s['_text']]
    if not spans:
        if must:
            raise LookupError('%r not found on page %d' % (needle, page.number + 1))
        return None
    s = spans[occurrence]
    txt = s['_text']
    i = txt.index(needle)
    chars = s['chars']
    fo = _usable(s['font'], replacement + txt)
    size = s['size']
    # rebuild the character list: prefix, replacement, shifted tail
    items = []
    for c in chars[:i]:
        items.append((c['origin'][0], c['origin'][1], c['c']))
    x = chars[i]['origin'][0]
    y = chars[i]['origin'][1]
    for ch in replacement:
        items.append((x, y, ch))
        x += fo.glyph_advance(ord(ch)) * size
    tail = chars[i + len(needle):]
    if tail:
        shift = x - tail[0]['origin'][0]
        for c in tail:
            items.append((c['origin'][0] + shift, c['origin'][1], c['c']))
    return dict(span=s, items=items, font=s['font'], size=size, color=s['color'],
                bbox=fitz.Rect(s['bbox']), label='%r -> %r' % (needle, replacement))


def apply_edits(page, edits):
    """redact the touched spans, then re-lay their text"""
    edits = [e for e in edits if e]
    if not edits:
        return
    for e in edits:
        r = fitz.Rect(e['bbox'])
        r.y0 -= 0.6
        r.y1 += 0.6
        page.add_redact_annot(r)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                          graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                          text=fitz.PDF_REDACT_TEXT_REMOVE)
    for e in edits:
        tw = fitz.TextWriter(page.rect)
        fo = _usable(e['font'], ''.join(c for _, _, c in e['items']))
        for x, y, ch in e['items']:
            if ch.strip():
                tw.append((x, y), ch, font=fo, fontsize=e['size'])
        tw.write_text(page, color=rgb(e['color']))
