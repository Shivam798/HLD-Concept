# -*- coding: utf-8 -*-
"""Page helpers shared by the two split volumes."""
import io

D = u'—'   # em dash
EN = u'–'  # en dash
LQ, RQ = u'“', u'”'
AP = u'’'
AR = u'→'
S = u'§'
NE = u'≠'
LE = u'≤'
TIMES = u'×'
STAR = u'★'
NBSP = u' '


class Book(object):
    def __init__(self, title, theme=None):
        self.title = title
        self.theme = theme or {}
        self.pages = []

    def _vars(self, keys):
        css = u';'.join(u'--%s:%s' % (k, self.theme[k]) for k in keys if k in self.theme)
        return u' style="%s"' % css if css else u''

    def page(self, *blocks):
        self.pages.append(u'<div class="page"%s><div class="inner">%s</div></div>'
                          % (self._vars(('acc', 'acctint', 'qn')), u''.join(blocks)))

    def raw(self, html):
        self.pages.append(html)

    def write(self, path):
        html = (u'<meta charset="utf-8"><title>%s</title>'
                u'<link rel="stylesheet" href="style.css">'
                u'<link rel="stylesheet" href="fonts.css">'
                u'<link rel="stylesheet" href="extra.css">' % self.title
                + u''.join(self.pages))
        io.open(path, 'w', encoding='utf-8').write(html)
        print('wrote %s  pages=%d' % (path, len(self.pages)))


# ---------------------------------------------------------------- primitives
def p(t, cls=None):
    return u'<p%s>%s</p>' % (u' class="%s"' % cls if cls else u'', t)


def h2(t, cls=None):
    return u'<h2%s>%s</h2>' % (u' class="%s"' % cls if cls else u'', t)


def h3(t):
    return u'<h3>%s</h3>' % t


def cd(t):
    return u'<span class="mono">%s</span>' % t


def callout(label, body, kind=''):
    return (u'<div class="callout %s"><span class="lbl">%s</span>%s</div>'
            % (kind, label, u''.join(p(b) for b in body)))


def cards(*items):
    out = []
    for cls, title, lines in items:
        body = u''.join(p(x) for x in lines)
        out.append(u'<div class="card %s"><h4>%s</h4>%s</div>' % (cls, title, body))
    return u'<div class="cards">%s</div>' % u''.join(out)


def table(head, rows, widths=None):
    w = u''
    if widths:
        w = u'<colgroup>%s</colgroup>' % u''.join(u'<col style="width:%.1fpt">' % x
                                                 for x in widths)
    th = u''.join(u'<th>%s</th>' % x for x in head)
    tr = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            tds.append(u'<td%s>%s</td>' % (u' class="k"' if i == 0 else u'', c))
        tr.append(u'<tr>%s</tr>' % u''.join(tds))
    return (u'<table>%s<thead><tr>%s</tr></thead><tbody>%s</tbody></table>'
            % (w, th, u''.join(tr)))


# ---------------------------------------------------------------- components
COVER_VARS = ('bgimg', 'hi', 'eye', 'ledec', 'cardp', 'metac', 'barg')


def cover(theme, eyebrow, title_html, lede, boxes, meta_left, meta_right):
    """theme: dict of cover CSS variables (see COVER_VARS) - one per volume."""
    cc = []
    for cls, (h, txt) in zip('abcd', boxes):
        cc.append(u'<div class="cc %s"><h4>%s</h4><p>%s</p></div>' % (cls, h, txt))
    style = u';'.join(u'--%s:%s' % (k, theme[k]) for k in COVER_VARS if k in theme)
    return (u'<div class="page cover" style="%s"><div class="bg"></div><div class="cin">'
            u'<div class="eyebrow">%s</div><h1>%s</h1><div class="bar"></div>'
            u'<p class="lede">%s</p><div class="grid">%s</div>'
            u'<div class="rule"></div><div class="meta"><span>%s</span><span>%s</span></div>'
            u'</div></div>'
            % (style, eyebrow, title_html, lede, u''.join(cc), meta_left, meta_right))


def toc(chip, heading, sub, rows, foot=None):
    out = []
    for num, cls, title, desc in rows:
        out.append(u'<div class="row"><span class="n %s">%s</span><h4>%s</h4><p>%s</p></div>'
                   % (cls, num, title, desc))
    return (u'<span class="chip">%s</span><h1 class="big">%s</h1>%s<hr class="thin">'
            u'<div class="toc">%s</div>%s'
            % (chip, heading, p(sub, 'sub'), u''.join(out),
               p(foot, 'foot') if foot else u''))


def qa(num, question, paras, tails=()):
    body = u''.join(p(x) for x in paras)
    for cls, label, txt in tails:
        body += (u'<div class="tail %s"><b>%s</b> %s</div>' % (cls, label, txt))
    return (u'<div class="qa"><span class="qh"><span class="qn">Q%s</span>'
            u'<span class="qt">%s</span></span><div class="qb">%s</div></div>'
            % (num, question, body))


def facts(items, tone='red'):
    out = []
    for h, t in items:
        out.append(u'<div class="f"><h4>%s</h4><p>%s</p></div>' % (h, t))
    return u'<div class="facts%s">%s</div>' % (u' blue' if tone == 'blue' else u'',
                                              u''.join(out))


def formula(f1, f2):
    return (u'<div class="formula"><div class="f1">%s</div><div class="f2">%s</div></div>'
            % (f1, f2))


def closing(label, text):
    return (u'<div class="closing"><span class="lbl">%s</span>%s</div>' % (label, p(text)))


def part(title, badge, lede):
    """the opening block of a part: title, PART n chip, lede, rule"""
    return (u'<h1>%s</h1><span class="badge">%s</span>%s<hr class="rule">'
            % (title, badge, p(lede, 'lede')))


def fig(num, svg, caption, note=None, title=None):
    """a figure with the guide's caption style"""
    head = u'<p class="figtitle">%s</p>' % title if title else u''
    cap = (u'<figcaption><b>Figure %s</b> %s %s</figcaption>'
           % (num, u'\u2014', caption))
    extra = u''
    if note:
        extra = (u'<div class="fignote"><div class="t">%s</div><div class="d">%s</div></div>'
                 % (note[0], note[1]))
    return u'<figure>%s%s%s%s</figure>' % (head, svg, extra, cap)


def kv(items):
    """small two-per-row info tiles"""
    out = [u'<div class="i"><h5>%s</h5><p>%s</p></div>' % (h, t) for h, t in items]
    return u'<div class="kv">%s</div>' % u''.join(out)


def bullets(items):
    return u'<ul class="bul">%s</ul>' % u''.join(u'<li>%s</li>' % x for x in items)


def strip(items):
    """the numbered progression strip"""
    cells = []
    for n, t, d in items:
        cells.append(u'<div class="s"><span class="n">%s</span><span class="t2">%s</span>'
                     u'<span class="d">%s</span></div>' % (n, t, d))
    return u'<div class="strip">%s</div>' % (u'<span class="ar">\u2192</span>'.join(cells))


def codebox(title, lines, foot=None):
    return (u'<div class="codebox"><span class="h">%s</span><pre>%s</pre>%s</div>'
            % (title, lines, u'<div class="foot">%s</div>' % foot if foot else u''))


def codes(*boxes):
    return u'<div class="codes">%s</div>' % u''.join(boxes)
