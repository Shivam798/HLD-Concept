# -*- coding: utf-8 -*-
"""Minimal SVG diagram kit that matches the guide's existing figure style."""

C = dict(ink='#141824', navy='#20243c', slate='#3c4356', muted='#6b7284',
         border='#dfe3ec', panel='#f6f7fb', blue='#3538a8', green='#15713f',
         red='#d3372a', amber='#a85a06', teal='#0d7a84', purple='#7a2f8f',
         pink='#fdecea', bluetint='#eef0fa', greentint='#e8f3ec',
         ambertint='#fdf1de', tealtint='#e4f4f5', white='#ffffff')

NW, NH, RAD = 64.1, 32.8, 4.2
BOLD = 'var(--bold)'
REG = 'var(--reg)'

KINDS = {
    'app':   (C['white'], C['slate'], C['ink']),
    'cache': (C['pink'], C['red'], C['red']),
    'db':    (C['navy'], None, C['white']),
    'blue':  (C['bluetint'], C['blue'], C['blue']),
    'green': (C['greentint'], C['green'], C['green']),
    'amber': (C['ambertint'], C['amber'], C['amber']),
    'teal':  (C['tealtint'], C['teal'], C['teal']),
    'plain': (C['panel'], C['border'], C['slate']),
}


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


class Fig(object):
    def __init__(self, w=522.0, h=200.0):
        self.w, self.h, self.b = w, h, []

    # ---------- primitives ----------
    def text(self, x, y, s, color=None, size=6.11, anchor='middle', font=BOLD,
             ls=None, op=None):
        # NB: font-size must be a presentation attribute in user units. A CSS
        # "pt" value inside an SVG whose user unit is already 1pt is converted
        # twice and comes out 4/3 too large.
        st = 'font-family:%s' % font
        if ls:
            st += ';letter-spacing:%.3fem' % ls
        if op:
            st += ';opacity:%.2f' % op
        self.b.append('<text x="%.2f" y="%.2f" font-size="%.2f" text-anchor="%s" fill="%s" '
                      'style="%s">%s</text>'
                      % (x, y, size, anchor, color or C['ink'], st, esc(s)))
        return self

    def rect(self, x, y, w, h, fill=None, stroke=None, sw=0.82, r=0.0, dash=None):
        a = ['<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"' % (x, y, w, h)]
        if r:
            a.append('rx="%.2f"' % r)
        a.append('fill="%s"' % (fill or 'none'))
        if stroke:
            a.append('stroke="%s" stroke-width="%.2f"' % (stroke, sw))
            if dash:
                a.append('stroke-dasharray="%s"' % dash)
        self.b.append(' '.join(a) + '/>')
        return self

    def line(self, pts, color, sw=0.97, dash=None):
        d = 'M' + ' L'.join('%.2f %.2f' % p for p in pts)
        a = ['<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-linejoin="round"'
             % (d, color, sw)]
        if dash:
            a.append('stroke-dasharray="%s"' % dash)
        self.b.append(' '.join(a) + '/>')
        return self

    # ---------- composites ----------
    def node(self, x, y, label, kind='app', w=NW, h=NH, sub=None, size=7.45, sw=0.82):
        fill, stroke, tc = KINDS[kind]
        self.rect(x, y, w, h, fill, stroke, sw, RAD)
        cy = y + h / 2.0
        if sub:
            self.text(x + w / 2.0, cy - 0.6, label, tc, size)
            self.text(x + w / 2.0, cy + 7.4, sub, tc, 5.7, op=0.85)
        else:
            self.text(x + w / 2.0, cy + size * 0.35, label, tc, size)
        return self

    def head(self, x, y, dx, dy, color, size=6.3):
        """filled triangular arrowhead at (x,y) pointing along (dx,dy)"""
        import math
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        px, py = -uy, ux
        hw = size / 2.0
        p = [(x, y), (x - ux * size + px * hw, y - uy * size + py * hw),
             (x - ux * size - px * hw, y - uy * size - py * hw)]
        self.b.append('<path d="M%.2f %.2f L%.2f %.2f L%.2f %.2f Z" fill="%s"/>'
                      % (p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1], color))
        return self

    def arrow(self, pts, color, dash=None, sw=0.97, hsize=6.3):
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        import math
        n = math.hypot(x1 - x0, y1 - y0) or 1.0
        ux, uy = (x1 - x0) / n, (y1 - y0) / n
        self.line(pts[:-1] + [(x1 - ux * hsize * 0.75, y1 - uy * hsize * 0.75)], color, sw, dash)
        self.head(x1, y1, x1 - x0, y1 - y0, color, hsize)
        return self

    def hlabel(self, x1, x2, y, s, color, above=True, size=6.11, gap=4.2, anchor=None):
        xm = (x1 + x2) / 2.0
        self.text(xm if anchor is None else x1, y - gap if above else y + gap + 4.0, s,
                  color, size, anchor='middle' if anchor is None else anchor)
        return self

    def band(self, x, y, w, h, fill, stroke=None, r=3.5, dash=None):
        return self.rect(x, y, w, h, fill, stroke, 0.75, r, dash)

    def caption(self, x, y, s, color=None, size=6.9, anchor='start', font=BOLD):
        return self.text(x, y, s, color or C['slate'], size, anchor, font)

    def cross(self, x, y, size, color, sw=1.0):
        """a small drawn multiplication sign - no symbol font needed"""
        h = size / 2.0
        self.line([(x - h, y - h), (x + h, y + h)], color, sw)
        self.line([(x - h, y + h), (x + h, y - h)], color, sw)
        return self

    def render(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="%.2fpt" height="%.2fpt" '
                'viewBox="0 0 %.2f %.2f">%s</svg>'
                % (self.w, self.h, self.w, self.h, ''.join(self.b)))
