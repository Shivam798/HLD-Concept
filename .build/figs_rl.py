# -*- coding: utf-8 -*-
"""Figures for the Rate Limiting volume.

The comparison figure is not drawn by hand: the five algorithms are
re-implemented here exactly as they appear in the Java reference and run
against one shared arrival trace, so every green and red cell in Figure 4.1
is a real verdict rather than an illustration.
"""
from collections import deque

from svgkit import Fig, C

GREY = '#eef0f4'
PLUM = '#f6e9f9'


# ══════════════════════════════════════════════════ the reference simulators
def sim_fixed(trace, limit, window):
    start, count, out = 0, 0, []
    for t in trace:
        if t - start >= window:
            start += ((t - start) // window) * window
            count = 0
        if count < limit:
            count += 1
            out.append(True)
        else:
            out.append(False)
    return out


def sim_log(trace, limit, window):
    dq, out = deque(), []
    for t in trace:
        cutoff = t - window
        while dq and dq[0] <= cutoff:
            dq.popleft()
        if len(dq) >= limit:
            out.append(False)
        else:
            dq.append(t)
            out.append(True)
    return out


def sim_swc(trace, limit, window):
    cur, cc, pc, out = 0, 0, 0, []
    for t in trace:
        b = t // window
        if b == cur + 1:
            pc, cc, cur = cc, 0, b
        elif b > cur + 1:
            pc, cc, cur = 0, 0, b
        overlap = 1.0 - float(t - cur * window) / window
        if cc + pc * overlap < limit:
            cc += 1
            out.append(True)
        else:
            out.append(False)
    return out


def sim_token(trace, cap, rate):
    tokens, last, out = float(cap), 0, []
    for t in trace:
        if t > last:
            tokens = min(float(cap), tokens + (t - last) / 1000.0 * rate)
            last = t
        if tokens >= 1.0:
            tokens -= 1.0
            out.append(True)
        else:
            out.append(False)
    return out


def sim_leaky(trace, cap, rate):
    water, last, out = 0.0, 0, []
    for t in trace:
        if t > last:
            water = max(0.0, water - (t - last) / 1000.0 * rate)
            last = t
        if water + 1.0 <= cap:
            water += 1.0
            out.append(True)
        else:
            out.append(False)
    return out


TRACE = [100, 300, 500,
         900, 920, 940, 960, 980,
         1000, 1020, 1040, 1060, 1080,
         1600, 1700, 1800,
         2500, 2510, 2520, 2530, 2540, 2550, 2560]
LIMIT, WINDOW = 5, 1000


def results():
    return [
        (u'Fixed window',    sim_fixed(TRACE, LIMIT, WINDOW),  C['red']),
        (u'Sliding log',     sim_log(TRACE, LIMIT, WINDOW),    C['green']),
        (u'Sliding counter', sim_swc(TRACE, LIMIT, WINDOW),    C['blue']),
        (u'Token bucket',    sim_token(TRACE, LIMIT, LIMIT),   C['amber']),
        (u'Leaky (meter)',   sim_leaky(TRACE, LIMIT, LIMIT),   C['teal']),
    ]


# ══════════════════════════════════════════════════════════════════ figures
def fig_where():
    """1.1 - where a limiter sits on the request path"""
    f = Fig(522, 196)
    f.text(261, 10, u'Put the limit at the outermost layer that knows enough to apply it',
           C['ink'], 8.4)
    stages = [(0, u'Client', u'retry + backoff', 'plain'),
              (108, u'Edge / CDN', u'IP, bots, WAF', 'blue'),
              (216, u'API gateway', u'per API key', 'green'),
              (324, u'Service', u'per tenant, per cost', 'amber'),
              (432, u'Datastore', u'what you protect', 'db')]
    for x, t, s, k in stages:
        f.node(x, 58, t, k, w=90, h=40, sub=s, size=7.8)
    for i in range(4):
        x = i * 108 + 90
        f.arrow([(x + 2, 78), (x + 16, 78)], C['slate'], sw=1.0, hsize=5.5)
    for x, lab in [(108, u'coarse and cheap'), (216, u'the usual answer'),
                   (324, u'fine and expensive')]:
        f.rect(x + 16, 26, 58, 14, C['pink'], C['red'], 0.8, 3.0)
        f.text(x + 45, 36, u'L I M I T', C['red'], 6.4)
        f.arrow([(x + 45, 42), (x + 45, 55)], C['red'], sw=0.9, hsize=5)
        f.text(x + 45, 112, lab, C['muted'], 6.5)
    f.rect(0, 124, 256, 40, C['greentint'], C['green'], 0.75, 3.5)
    f.text(10, 138, u'Reject early', C['green'], 7.6, anchor='start')
    f.text(10, 150, u'A request refused at the edge costs one handshake.',
           C['slate'], 6.7, anchor='start')
    f.text(10, 159, u'Refused at the database, it already cost you the database.',
           C['slate'], 6.7, anchor='start')
    f.rect(266, 124, 256, 40, C['bluetint'], C['blue'], 0.75, 3.5)
    f.text(276, 138, u'But only the inner layer knows the price', C['blue'], 7.6, anchor='start')
    f.text(276, 150, u'The edge sees an IP. The service knows this call is a',
           C['slate'], 6.7, anchor='start')
    f.text(276, 159, u'report that runs for 40 seconds. So you limit at both.',
           C['slate'], 6.7, anchor='start')
    f.text(261, 182, u'Rate limiting protects the system. Quotas bill the customer. '
                     u'Load shedding saves you when both have already failed.',
           C['slate'], 7.2)
    return f.render()


def fig_fixed():
    """2.1 - fixed window counter: the count climbs, then the boundary resets it"""
    f = Fig(522, 244)
    x0, wpx = 12.0, 160.0
    top, zero, unit = 40.0, 132.0, 15.0
    limy = zero - 5 * unit
    axis = 152.0
    hits = [[16, 34, 56, 78, 100, 118, 136],
            [18, 40, 62, 88, 110, 130],
            [12, 26, 40, 54, 70, 90, 112, 132]]
    for w in range(3):
        wx = x0 + w * wpx
        f.rect(wx, top, wpx - 6, zero - top + 10, GREY, C['border'], 0.75, 3.0)
        f.text(wx + (wpx - 6) / 2.0, top - 8, u'window %d' % (w + 1), C['slate'], 7.2)
    f.line([(x0 - 2, limy), (x0 + 3 * wpx - 6, limy)], C['amber'], 0.9, dash='3,2.2')
    f.text(x0 + 3 * wpx - 2, limy + 2.4, u'limit 5', C['amber'], 6.4, anchor='start')
    f.line([(x0 - 2, axis), (508, axis)], C['slate'], 1.0)
    f.text(x0 - 5, limy + 2.4, u'5', C['muted'], 6.0, anchor='end')
    f.text(x0 - 5, zero + 2.4, u'0', C['muted'], 6.0, anchor='end')
    for w in range(3):
        wx = x0 + w * wpx
        pts, cnt = [(wx + 4, zero)], 0
        for h in hits[w]:
            hx = wx + h
            pts.append((hx, zero - min(cnt, 5) * unit))
            cnt += 1
            pts.append((hx, zero - min(cnt, 5) * unit))
        pts.append((wx + wpx - 10, zero - min(cnt, 5) * unit))
        f.line(pts, C['blue'], 1.5)
        cnt = 0
        for h in hits[w]:
            cnt += 1
            col = C['green'] if cnt <= 5 else C['red']
            f.b.append('<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s"/>' % (wx + h, axis, col))
        n = len(hits[w])
        f.text(wx + (wpx - 6) / 2.0, axis + 17, u'%d allowed, %d rejected'
               % (min(5, n), max(0, n - 5)), C['muted'], 6.6)
        if w:
            f.line([(wx - 3, top - 18), (wx - 3, axis + 5)], C['red'], 1.0, dash='3,2.2')
            f.text(wx - 3, top - 22, u'RESET', C['red'], 6.2)
    f.line([(151, 181), (169, 181)], C['blue'], 1.5)
    f.text(173, 183.4, u'the counter, flat-lining at the limit', C['slate'], 6.6,
           anchor='start')
    f.b.append('<circle cx="292" cy="181" r="3.6" fill="%s"/>' % C['green'])
    f.text(299, 183.4, u'allowed', C['slate'], 6.6, anchor='start')
    f.b.append('<circle cx="345" cy="181" r="3.6" fill="%s"/>' % C['red'])
    f.text(352, 183.4, u'rejected', C['slate'], 6.6, anchor='start')
    f.rect(0, 198, 522, 40, C['ambertint'], C['amber'], 0.75, 3.5)
    f.text(261, 213, u'One counter, one timestamp. INCR + EXPIRE in Redis is the whole '
                     u'implementation.', C['amber'], 7.4)
    f.text(261, 226, u'That cheapness is the only reason anyone accepts the bug on the '
                     u'next page.', C['slate'], 7.0)
    return f.render()

def fig_boundary():
    """2.2 - the boundary burst: 2x the limit in one wall-clock second"""
    f = Fig(522, 196)
    base, mid = 96.0, 261.0
    f.line([(10, base), (512, base)], C['slate'], 1.0)
    f.line([(mid, 26), (mid, base + 10)], C['red'], 1.1, dash='3,2.2')
    f.text(mid, 20, u'window boundary  (12:00:00)', C['red'], 7.0)
    f.rect(10, 34, 251, base - 34, C['bluetint'], None, 0, 3.0)
    f.rect(261, 34, 251, base - 34, C['greentint'], None, 0, 3.0)
    f.text(80, 46, u'window 1   counter 0 .. 100', C['blue'], 7.0)
    f.text(442, 46, u'window 2   counter 0 .. 100', C['green'], 7.0)
    for i in range(20):
        f.line([(200 + i * 3, 62), (200 + i * 3, base - 4)], C['blue'], 1.0)
    for i in range(20):
        f.line([(264 + i * 3, 62), (264 + i * 3, base - 4)], C['green'], 1.0)
    f.text(200, 56, u'100 requests', C['blue'], 6.4, anchor='start')
    f.text(324, 56, u'100 requests', C['green'], 6.4, anchor='start')
    f.line([(198, base + 12), (326, base + 12)], C['red'], 1.2)
    f.line([(198, base + 8), (198, base + 16)], C['red'], 1.2)
    f.line([(326, base + 8), (326, base + 16)], C['red'], 1.2)
    f.text(262, base + 27, u'200 requests inside two seconds of wall clock',
           C['red'], 8.4)
    f.text(262, base + 39, u'Every window obeyed the limit. The client got twice the rate.',
           C['red'], 7.0)
    f.rect(0, 152, 522, 36, C['pink'], C['red'], 0.75, 3.5)
    f.text(261, 166, u'This single defect is the reason the other four algorithms exist.',
           C['red'], 7.6)
    f.text(261, 179, u'Sliding window anchors the window to "now" instead of to the clock. '
                     u'Buckets never reset at all.', C['slate'], 7.0)
    return f.render()


def fig_log():
    """2.3 - sliding window log: the deque and the cutoff"""
    f = Fig(522, 226)
    f.text(261, 11, u'The window is anchored to now, so there is no boundary to exploit',
           C['ink'], 8.4)
    y = 40.0
    ts = [u'0.10', u'0.30', u'0.50', u'0.90', u'0.92', u'1.60', u'1.70', u'1.80', u'2.50']
    cw, x0 = 46.0, 24.0
    keep = 5
    for i, t in enumerate(ts):
        x = x0 + i * (cw + 6)
        old = i < len(ts) - keep
        fill = GREY if old else C['greentint']
        stroke = C['border'] if old else C['green']
        f.rect(x, y, cw, 26, fill, stroke, 0.85, 3.0)
        f.text(x + cw / 2.0, y + 16.5, t, C['muted'] if old else C['green'], 7.4)
        if old:
            f.cross(x + cw / 2.0, y + 38, 6.0, C['red'], 1.1)
    f.text(x0 - 6, y + 16.5, u'head', C['muted'], 6.2, anchor='end')
    f.text(x0 + 9 * (cw + 6) + 2, y + 16.5, u'tail', C['muted'], 6.2, anchor='start')
    f.text(x0 + 2 * (cw + 6), y + 52, u'evicted: older than now minus the window',
           C['red'], 6.8, anchor='start')
    ly = 96.0
    lx0 = x0 + 4 * (cw + 6) - 3
    lx1 = x0 + 9 * (cw + 6) - 6
    f.rect(lx0, ly, lx1 - lx0, 22, C['bluetint'], C['blue'], 0.85, 3.0)
    f.text((lx0 + lx1) / 2.0, ly + 14.5, u'the live window:  [ now - 1.00s , now ]',
           C['blue'], 7.2)
    f.arrow([(lx0 - 26, ly + 11), (lx0 - 6, ly + 11)], C['blue'], sw=1.0, hsize=5.5)
    f.text(lx0 - 30, ly + 13.5, u'slides', C['blue'], 6.4, anchor='end')
    f.rect(0, 136, 256, 76, C['white'], C['green'], 0.9, 3.5)
    f.text(10, 151, u'What you get', C['green'], 7.8, anchor='start')
    for j, t in enumerate([u'Exactly N per window. No approximation, no',
                           u'boundary case, no argument with the customer',
                           u'about what the number means.',
                           u'Rejected requests are not recorded, so a client',
                           u'being throttled cannot deepen its own hole.']):
        f.text(10, 165 + j * 9.6, t, C['slate'], 6.7, anchor='start')
    f.rect(266, 136, 256, 76, C['white'], C['red'], 0.9, 3.5)
    f.text(276, 151, u'What it costs', C['red'], 7.8, anchor='start')
    for j, t in enumerate([u'One timestamp per allowed request, per client.',
                           u'1M clients x 1,000 req/window x 8 bytes = 8 GB',
                           u'of RAM that does nothing but remember.',
                           u'Eviction is amortised O(1), but the memory is',
                           u'the reason this rarely ships as-is at scale.']):
        f.text(276, 165 + j * 9.6, t, C['slate'], 6.7, anchor='start')
    return f.render()


def fig_counter():
    """2.4 - sliding window counter: the weighted blend"""
    f = Fig(522, 230)
    y, h = 44.0, 56.0
    pw = 208.0
    f.rect(24, y, pw, h, C['bluetint'], C['blue'], 0.9, 3.5)
    f.rect(24 + pw + 6, y, pw, h, C['greentint'], C['green'], 0.9, 3.5)
    f.text(24 + pw / 2.0, y - 8, u'previous window', C['blue'], 7.4)
    f.text(24 + pw + 6 + pw / 2.0, y - 8, u'current window', C['green'], 7.4)
    f.text(24 + pw / 2.0, y + 24, u'80', C['blue'], 15.0)
    f.text(24 + pw / 2.0, y + 40, u'requests counted', C['blue'], 6.4)
    f.text(24 + pw + 6 + pw / 2.0, y + 24, u'20', C['green'], 15.0)
    f.text(24 + pw + 6 + pw / 2.0, y + 40, u'requests so far', C['green'], 6.4)
    nowx = 24 + pw + 6 + pw * 0.30
    f.line([(nowx, y - 20), (nowx, y + h + 22)], C['red'], 1.1, dash='3,2.2')
    f.text(nowx, y - 25, u'now  (30% into the current window)', C['red'], 7.0)
    sx = 24 + pw * 0.30
    f.rect(sx, y + h + 6, nowx - sx, 14, C['ambertint'], C['amber'], 0.85, 2.5)
    f.text((sx + nowx) / 2.0, y + h + 16, u'the rolling window the client actually feels',
           C['amber'], 6.8)
    f.line([(24, y + h + 30), (sx, y + h + 30)], C['muted'], 0.9, dash='2,2')
    f.text((24 + sx) / 2.0, y + h + 42, u'already slid out', C['muted'], 6.4)
    f.rect(0, 148, 522, 40, C['panel'], C['border'], 0.75, 3.5)
    f.text(261, 166, u'estimate  =  current  +  previous x overlap  =  20 + 80 x 0.70  =  76',
           C['ink'], 10.6)
    f.text(261, 180, u'76 is under the limit of 100, so this request is allowed. '
                     u'Two integers and one long, per client.', C['slate'], 7.0)
    f.rect(0, 196, 522, 30, C['ambertint'], C['amber'], 0.75, 3.5)
    f.text(261, 209, u'The one assumption: the previous window’s traffic was spread '
                     u'evenly across it.', C['amber'], 7.2)
    f.text(261, 220, u'Bursty traffic inside that window makes the estimate drift '
                     u'— low single-digit percent in practice.', C['slate'], 7.0)
    return f.render()


def fig_token():
    """3.1 - token bucket: the bucket and the level over time"""
    f = Fig(522, 268)
    bx, by, bw, bh = 32.0, 56.0, 104.0, 128.0
    f.text(bx + bw / 2.0, 14, u'refill: + r tokens / second', C['amber'], 7.6)
    for i in range(5):
        f.arrow([(bx + 16 + i * 18, 24), (bx + 16 + i * 18, 50)], C['amber'], sw=0.9, hsize=4.6)
    f.rect(bx, by, bw, bh, C['white'], C['slate'], 1.1, 3.0)
    f.line([(bx - 5, by), (bx + bw + 5, by)], C['amber'], 1.0, dash='3,2')
    f.text(bx + bw / 2.0, by + 12, u'capacity = the biggest burst', C['amber'], 6.4)
    for r in range(4):
        for c in range(3):
            f.b.append('<circle cx="%.1f" cy="%.1f" r="6.6" fill="%s"/>'
                       % (bx + 26 + c * 26, by + 42 + r * 24, C['amber']))
    f.text(bx + bw / 2.0, by + bh + 14, u'one request spends one token', C['ink'], 7.0)
    f.text(bx + bw / 2.0, by + bh + 25, u'refill computed on read, never by a timer',
           C['muted'], 6.4)
    ox, oy, ow, oh = 176.0, 56.0, 346.0, 128.0
    f.rect(ox, oy, ow, oh, '#fafbfd', C['border'], 0.75, 3.5)
    ax, ay0, ay1 = ox + 34, oy + 16, oy + 96
    f.line([(ax, ay0), (ax, ay1), (ox + ow - 16, ay1)], C['slate'], 0.9)
    f.text(ax - 5, ay0 + 3, u'full', C['muted'], 6.0, anchor='end')
    f.text(ax - 5, ay1 + 2, u'empty', C['muted'], 6.0, anchor='end')
    f.text(ax + 2, oy + 10, u'tokens in the bucket', C['muted'], 6.2, anchor='start')
    f.text(ox + ow / 2.0, oy - 8, u'A request costs one token. No token, no request.',
           C['ink'], 7.6)
    pts = [(ax, ay0 + 2), (ax + 52, ay0 + 2), (ax + 88, ay1 - 18),
           (ax + 126, ay1 - 44), (ax + 160, ay1 - 6), (ax + 188, ay1 - 4),
           (ax + 228, ay0 + 6), (ax + 258, ay1 - 4), (ax + 286, ay0 + 4)]
    f.line(pts, C['amber'], 1.5)
    notes = [(ox + 56, C['red'], u'a burst drains it'),
             (ox + 172, C['green'], u'idle time refills it'),
             (ox + 274, C['red'], u'empty means deny')]
    for nx, col, t in notes:
        f.b.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s"/>' % (nx, oy + 114, col))
        f.text(nx + 6, oy + 116.5, t, C['slate'], 6.6, anchor='start')
    f.rect(0, 218, 256, 44, C['greentint'], C['green'], 0.75, 3.5)
    f.text(10, 233, u'Why it is the default answer', C['green'], 7.6, anchor='start')
    f.text(10, 246, u'Two numbers per client, O(1) per call, and it lets a quiet',
           C['slate'], 6.8, anchor='start')
    f.text(10, 256, u'client spend a saved-up burst — which real traffic does.',
           C['slate'], 6.8, anchor='start')
    f.rect(266, 218, 256, 44, C['bluetint'], C['blue'], 0.75, 3.5)
    f.text(276, 233, u'The two dials, said correctly', C['blue'], 7.6, anchor='start')
    f.text(276, 246, u'capacity sets how big a burst you tolerate; refill rate',
           C['slate'], 6.8, anchor='start')
    f.text(276, 256, u'sets the sustained rate. They are independent knobs.',
           C['slate'], 6.8, anchor='start')
    return f.render()

def fig_leaky():
    """3.2 - leaky bucket: meter form vs queue form"""
    f = Fig(522, 252)
    for x0, title, col in [(0, u'Meter form  —  the one in the code', C['teal']),
                           (266, u'Queue form  —  the one that shapes traffic', C['purple'])]:
        f.rect(x0, 24, 256, 182, C['white'], C['border'], 0.75, 3.5)
        f.text(x0 + 128, 16, title, col, 8.0)
    bx, by, bw, bh = 78.0, 64.0, 100.0, 84.0
    f.text(bx + bw / 2.0, 38, u'spiky arrivals pour in', C['slate'], 6.9)
    for dx in (12, 34, 56, 78, 88):
        f.arrow([(bx + dx, 44), (bx + dx, 60)], C['slate'], sw=0.9, hsize=4.4)
    f.rect(bx, by, bw, bh, C['white'], C['slate'], 1.1, 3.0)
    f.rect(bx + 1.5, by + 30, bw - 3, bh - 31.5, C['tealtint'], None, 0, 2.0)
    f.line([(bx + 1.5, by + 30), (bx + bw - 1.5, by + 30)], C['teal'], 1.0)
    f.text(bx + bw / 2.0, by + 20, u'room left', C['muted'], 6.4)
    f.text(bx + bw / 2.0, by + 56, u'water level', C['teal'], 7.4)
    f.line([(bx - 5, by), (bx + bw + 5, by)], C['red'], 1.0, dash='3,2')
    f.text(bx + bw + 9, by + 3, u'full = deny', C['red'], 6.4, anchor='start')
    f.arrow([(bx + bw / 2.0, by + bh + 2), (bx + bw / 2.0, by + bh + 18)], C['teal'],
            sw=1.1, hsize=5.5)
    f.text(128, 178, u'leaks at a constant rate', C['teal'], 6.9)
    f.text(128, 194, u'Allow or deny only. The output is never reshaped.', C['slate'], 6.9)
    qx = 300.0
    f.text(qx + 82, 38, u'spiky in', C['slate'], 6.9)
    for dx in (0, 14, 28, 34, 60, 66, 72):
        f.line([(qx + dx, 44), (qx + dx, 58)], C['slate'], 1.4)
    f.rect(qx - 6, 68, 176, 26, PLUM, C['purple'], 0.9, 3.0)
    for i in range(7):
        f.rect(qx + 2 + i * 23, 73, 17, 16, C['white'], C['purple'], 0.7, 2.0)
    f.text(qx + 82, 106, u'FIFO queue, drained by a worker', C['purple'], 6.9)
    for i in range(7):
        f.line([(qx + 10 + i * 23, 116), (qx + 10 + i * 23, 130)], C['purple'], 1.4)
    f.text(qx + 82, 142, u'perfectly uniform out', C['purple'], 6.9)
    f.text(qx + 82, 158, u'The queue costs memory and latency: a request', C['slate'], 6.9)
    f.text(qx + 82, 168, u'may wait instead of being told no.', C['slate'], 6.9)
    f.text(qx + 82, 184, u'A full queue drops, and now you have a queueing-', C['red'], 6.9)
    f.text(qx + 82, 194, u'delay problem as well as a rate problem.', C['red'], 6.9)
    f.rect(0, 216, 522, 32, C['ambertint'], C['amber'], 0.75, 3.5)
    f.text(261, 230, u'Say this when asked: the meter form of leaky bucket and the token '
                     u'bucket are the same algorithm inside out.', C['amber'], 7.2)
    f.text(261, 242, u'“Is there room?” and “do I have a token?” are the same comparison. '
                     u'Only the queue form behaves differently.', C['slate'], 7.0)
    return f.render()

def fig_compare():
    """4.1 - the five algorithms on one real trace"""
    rows = results()
    f = Fig(522, 214)
    lx, gx, cw, ch, pitch = 0.0, 92.0, 17.4, 15.0, 19.0
    groups = [(0, 3, u'0.1 - 0.5s'), (3, 8, u'0.9s burst'), (8, 13, u'1.0s burst'),
              (13, 16, u'1.6 - 1.8s'), (16, 23, u'2.5s burst')]
    f.text(0, 10, u'One arrival trace, 23 requests, limit = 5 per second',
           C['ink'], 8.4, anchor='start')
    for a, b, lab in groups:
        x = gx + a * cw
        w = (b - a) * cw - 3
        f.rect(x, 18, w, 13, GREY, C['border'], 0.7, 2.0)
        f.text(x + w / 2.0, 27.4, lab, C['slate'], 6.2)
    top = 38.0
    for r, (name, verdicts, col) in enumerate(rows):
        y = top + r * pitch
        f.rect(lx, y, 86, ch, C['white'], col, 0.9, 2.5)
        f.text(lx + 6, y + 10.2, name, col, 7.0, anchor='start')
        for i, ok in enumerate(verdicts):
            x = gx + i * cw
            fill = C['greentint'] if ok else C['pink']
            stroke = C['green'] if ok else C['red']
            f.rect(x, y, cw - 2.4, ch, fill, stroke, 0.7, 2.0)
            if ok:
                f.line([(x + 4.6, y + 7.8), (x + 6.8, y + 10.4), (x + 10.6, y + 4.6)],
                       C['green'], 1.2)
            else:
                f.cross(x + 7.5, y + 7.5, 5.4, C['red'], 1.1)
        f.text(516, y + 10.2, u'%d' % sum(verdicts), col, 7.6, anchor='end')
    f.text(516, top - 8, u'allowed', C['muted'], 6.2, anchor='end')
    f.rect(0, 140, 256, 42, C['pink'], C['red'], 0.75, 3.5)
    f.text(10, 154, u'Read the fixed-window row', C['red'], 7.4, anchor='start')
    f.text(10, 166, u'It passes seven requests across the 1.0s boundary in',
           C['slate'], 6.7, anchor='start')
    f.text(10, 175, u'180 ms. Every window obeyed the limit; the client did not.',
           C['slate'], 6.7, anchor='start')
    f.rect(266, 140, 256, 42, C['bluetint'], C['blue'], 0.75, 3.5)
    f.text(276, 154, u'Read the last two rows', C['blue'], 7.4, anchor='start')
    f.text(276, 166, u'Token bucket and the leaky-bucket meter are byte-for-byte',
           C['slate'], 6.7, anchor='start')
    f.text(276, 175, u'identical here. That is not a coincidence — see Figure 3.2.',
           C['slate'], 6.7, anchor='start')
    f.rect(0, 188, 522, 24, C['greentint'], C['green'], 0.75, 3.5)
    f.text(261, 203, u'Sliding log is the truth. Sliding counter tracks it closely for '
                     u'a fraction of the memory. That trade is the whole chapter.',
           C['green'], 7.2)
    return f.render()


def fig_choose():
    """4.2 - the decision, as a flow"""
    f = Fig(522, 200)
    f.text(261, 12, u'Pick from the requirement, not from the algorithm', C['ink'], 8.4)
    qs = [(0, u'Bursts are\nnormal traffic?', u'Token bucket', C['amber'],
           u'API keys, user actions,\nanything human-paced'),
          (134, u'The count must be\nexact and billable?', u'Sliding window log', C['green'],
           u'quotas, paid tiers,\nlow client count'),
          (268, u'Millions of clients,\nno room for logs?', u'Sliding window counter',
           C['blue'], u'the production default\nfor public APIs'),
          (402, u'Downstream needs a\nsteady feed?', u'Leaky bucket (queue)', C['purple'],
           u'a third-party API that\nallows 10 calls/second')]
    for x, q, ans, col, note in qs:
        f.rect(x, 28, 118, 40, C['white'], C['slate'], 0.85, 3.5)
        for i, ln in enumerate(q.split('\n')):
            f.text(x + 59, 44 + i * 11, ln, C['ink'], 7.2)
        f.arrow([(x + 59, 70), (x + 59, 86)], col, sw=1.0, hsize=5.5)
        f.rect(x, 88, 118, 30, C['white'], col, 1.2, 3.5)
        f.text(x + 59, 106, ans, col, 7.8)
        for i, ln in enumerate(note.split('\n')):
            f.text(x + 59, 132 + i * 10, ln, C['muted'], 6.4)
    f.rect(0, 158, 522, 36, C['ambertint'], C['amber'], 0.75, 3.5)
    f.text(261, 172, u'If you only remember one: token bucket for the limit itself, '
                     u'sliding window counter when memory is the constraint.',
           C['amber'], 7.4)
    f.text(261, 185, u'Fixed window is the thing you implement first and then criticise. '
                     u'Never present it as the final answer.', C['slate'], 7.0)
    return f.render()


def fig_dist():
    """5.1 - three ways to run a limiter across N nodes"""
    f = Fig(522, 224)
    panels = [
        (0, u'Local only', C['red'], u'N nodes x limit',
         [u'Each node counts on its own.', u'Three nodes, limit 100 = 300 allowed.',
          u'Zero latency, zero coordination,', u'and the wrong answer.']),
        (178, u'Central store', C['green'], u'exact, + 1 RTT',
         [u'One Redis holds the counter.', u'INCR or a Lua script per request.',
          u'Correct everywhere; now Redis is', u'on the hot path and can fail.']),
        (356, u'Local + async sync', C['blue'], u'approximate, fast',
         [u'Count locally, gossip totals every', u'few hundred ms, deduct a shared',
          u'budget. Small overshoot in return', u'for no per-request network hop.']),
    ]
    for x0, title, col, tag, lines in panels:
        f.rect(x0, 22, 166, 178, C['white'], C['border'], 0.75, 3.5)
        f.rect(x0, 22, 166, 22, col, None, 0, 3.5)
        f.rect(x0, 36, 166, 8, col, None, 0, 0)
        f.text(x0 + 83, 36, title, C['white'], 8.0)
        f.text(x0 + 83, 60, tag, col, 7.2)
        for i in range(3):
            f.rect(x0 + 20 + i * 44, 70, 34, 20, C['panel'], C['border'], 0.75, 2.5)
            f.text(x0 + 37 + i * 44, 83, u'node', C['slate'], 6.2)
        if x0 == 178:
            f.rect(x0 + 53, 104, 60, 18, C['pink'], C['red'], 0.85, 2.5)
            f.text(x0 + 83, 116, u'Redis', C['red'], 7.0)
            for i, tx in enumerate((63, 83, 103)):
                f.arrow([(x0 + 37 + i * 44, 92), (x0 + tx, 102)], C['red'], sw=0.8, hsize=4.2)
        elif x0 == 356:
            f.line([(x0 + 37, 96), (x0 + 125, 96)], C['blue'], 0.9, dash='3,2')
            f.text(x0 + 83, 114, u'gossip every ~200 ms', C['blue'], 6.6)
        else:
            for i in range(3):
                f.text(x0 + 37 + i * 44, 102, u'100', C['red'], 7.0)
            f.text(x0 + 83, 116, u'total allowed: 300', C['red'], 7.0)
        f.line([(x0 + 10, 126), (x0 + 156, 126)], C['border'], 0.75)
        for j, ln in enumerate(lines):
            f.text(x0 + 10, 140 + j * 10.5, ln, C['slate'], 6.7, anchor='start')
    f.rect(0, 206, 522, 18, C['bluetint'], C['blue'], 0.75, 3.5)
    f.text(261, 218, u'Say the trade explicitly: exactness costs a network round trip on '
                     u'every request. Most APIs buy approximate and fast.', C['blue'], 7.2)
    return f.render()

def fig_race():
    """5.2 - the read-modify-write race, and the two fixes"""
    f = Fig(522, 216)
    f.text(261, 12, u'Two nodes, one counter at 99, limit 100', C['ink'], 8.4)
    ty = [40.0, 74.0]
    for i, lab in enumerate([u'node A', u'node B']):
        f.text(4, ty[i] + 12, lab, C['slate'], 7.0, anchor='start')
        f.line([(46, ty[i] + 9), (300, ty[i] + 9)], C['border'], 0.9)
    steps = [(60, 0, u'GET → 99', C['blue']), (108, 1, u'GET → 99', C['blue']),
             (168, 0, u'99 < 100, allow', C['red']), (232, 1, u'99 < 100, allow', C['red'])]
    for x, row, lab, col in steps:
        f.rect(x, ty[row], 60, 18, C['white'], col, 0.9, 2.5)
        f.text(x + 30, ty[row] + 12, lab, col, 6.4)
    f.text(174, 112, u'counter ends at 101. One request over the limit, silently.',
           C['red'], 7.2)
    f.rect(310, 30, 212, 82, C['greentint'], C['green'], 0.85, 3.5)
    f.text(320, 45, u'Fix 1  —  one atomic op', C['green'], 7.6, anchor='start')
    f.text(320, 59, u'INCR key ; EXPIRE key 60', C['navy'], 7.0, anchor='start',
           font='var(--mono)')
    f.text(320, 73, u'The read and the write are the same command,', C['slate'], 6.7,
           anchor='start')
    f.text(320, 82, u'so there is no window to interleave into.', C['slate'], 6.7,
           anchor='start')
    f.text(320, 98, u'Works for fixed window. Not enough for the rest.', C['green'], 6.7,
           anchor='start')
    f.rect(0, 126, 522, 54, C['bluetint'], C['blue'], 0.85, 3.5)
    f.text(10, 141, u'Fix 2  —  a Lua script, for every other algorithm', C['blue'], 7.8,
           anchor='start')
    f.text(10, 156, u'Token bucket needs read tokens → compute refill → compare '
                    u'→ write back. Four steps, one client, no lock.',
           C['slate'], 7.0, anchor='start')
    f.text(10, 169, u'Redis runs a Lua script atomically on one shard, so the whole '
                    u'decision is one round trip and one critical section.',
           C['slate'], 7.0, anchor='start')
    f.rect(0, 186, 522, 30, C['ambertint'], C['amber'], 0.75, 3.5)
    f.text(261, 199, u'Keep every key for one client on one shard — a hash tag, or the '
                     u'client id as the whole key.', C['amber'], 7.2)
    f.text(261, 210, u'A script that touches two shards will not run, and a counter '
                     u'split across shards is not a counter.', C['slate'], 7.0)
    return f.render()


def fig_response():
    """6.1 - the 429 contract and client backoff"""
    f = Fig(522, 220)
    f.rect(0, 20, 250, 122, C['white'], C['border'], 0.9, 3.5)
    f.rect(0, 20, 250, 20, C['navy'], None, 0, 3.5)
    f.rect(0, 34, 250, 8, C['navy'], None, 0, 0)
    f.text(125, 34, u'HTTP 429  Too Many Requests', C['white'], 7.8)
    hdrs = [(u'Retry-After: 12', u'when to come back. Seconds or a date.'),
            (u'RateLimit-Limit: 100', u'the ceiling for this window'),
            (u'RateLimit-Remaining: 0', u'what is left right now'),
            (u'RateLimit-Reset: 12', u'seconds until the window refills')]
    for i, (h, d) in enumerate(hdrs):
        f.text(10, 56 + i * 21, h, C['navy'], 7.0, anchor='start', font='var(--mono)')
        f.text(10, 66 + i * 21, d, C['muted'], 6.3, anchor='start')
    f.text(125, 152, u'Send the headers on success too, not only on 429.', C['slate'], 6.9)
    f.text(125, 162, u'A client that can see it is at 3 of 100 never has to guess.',
           C['slate'], 6.9)
    ox = 268.0
    f.text(ox + 127, 14, u'And what the client must do with it', C['ink'], 8.0)
    f.line([(ox + 10, 92), (ox + 244, 92)], C['border'], 0.9)
    f.text(ox + 10, 34, u'No jitter: everyone retries together', C['red'], 7.0, anchor='start')
    for i in range(6):
        f.line([(ox + 40 + i * 1.6, 44), (ox + 40 + i * 1.6, 60)], C['red'], 1.3)
        f.line([(ox + 120 + i * 1.6, 44), (ox + 120 + i * 1.6, 60)], C['red'], 1.3)
        f.line([(ox + 200 + i * 1.6, 44), (ox + 200 + i * 1.6, 60)], C['red'], 1.3)
    f.text(ox + 127, 72, u'the retry storm rebuilds the spike you just shed', C['red'], 6.6)
    f.text(ox + 10, 108, u'Full jitter: sleep = random(0, backoff)', C['green'], 7.0,
           anchor='start')
    import random
    random.seed(7)
    for i in range(18):
        x = ox + 24 + random.random() * 214
        f.line([(x, 118), (x, 134)], C['green'], 1.3)
    f.text(ox + 127, 146, u'same load, spread out — the server drains instead of '
                          u'oscillating', C['green'], 6.6)
    f.rect(0, 176, 256, 40, C['greentint'], C['green'], 0.75, 3.5)
    f.text(10, 190, u'429 vs 503', C['green'], 7.4, anchor='start')
    f.text(10, 202, u'429 means "you, specifically, are over your limit".',
           C['slate'], 6.7, anchor='start')
    f.text(10, 211, u'503 means "we are overloaded". Do not confuse them.',
           C['slate'], 6.7, anchor='start')
    f.rect(266, 176, 256, 40, C['pink'], C['red'], 0.75, 3.5)
    f.text(276, 190, u'Never silently drop', C['red'], 7.4, anchor='start')
    f.text(276, 202, u'A timeout teaches the client to retry harder. An explicit',
           C['slate'], 6.7, anchor='start')
    f.text(276, 211, u'429 with Retry-After teaches it to wait. Cheaper for both.',
           C['slate'], 6.7, anchor='start')
    return f.render()


def fig_keys():
    """6.2 - layered limits, and what to key on"""
    f = Fig(522, 202)
    f.text(0, 10, u'Real APIs run several limits at once. The first one to say no wins.',
           C['ink'], 8.4, anchor='start')
    layers = [(u'Global', u'the whole service', u'protects total capacity', C['navy']),
              (u'Per IP / subnet', u'anonymous traffic', u'blunt: NAT and mobile share IPs',
               C['red']),
              (u'Per API key / user', u'the real identity', u'the limit customers see',
               C['blue']),
              (u'Per key + endpoint', u'search vs. a static GET',
               u'one costly route cannot eat the quota', C['green']),
              (u'Per cost unit', u'tokens, rows, CPU seconds',
               u'charge by work, not by request', C['amber'])]
    for i, (name, sub, note, col) in enumerate(layers):
        y = 22 + i * 31
        x = i * 18
        f.rect(x, y, 280, 27, C['white'], col, 1.0, 3.0)
        f.text(x + 10, y + 12, name, col, 7.6, anchor='start')
        f.text(x + 10, y + 21.5, sub, C['muted'], 6.3, anchor='start')
        f.text(364, y + 16.5, note, C['slate'], 6.8, anchor='start')
        if i:
            f.arrow([(x - 13, y + 13), (x - 3, y + 13)], col, sw=0.8, hsize=4.2)
    f.rect(0, 182, 256, 18, C['bluetint'], C['blue'], 0.75, 3.0)
    f.text(128, 194, u'Unauthenticated: key on IP, and keep the limit low.', C['blue'], 6.8)
    f.rect(266, 182, 256, 18, C['greentint'], C['green'], 0.75, 3.0)
    f.text(394, 194, u'Authenticated: key on the account, never the IP.', C['green'], 6.8)
    return f.render()

def fig_failures():
    """7.1 - the four ways a rate limiter hurts you"""
    f = Fig(522, 176)
    items = [(0, u'Limiter is down', u'Fail open or fail closed?',
              u'Fail open for availability, but cap it: a local',
              u'in-process limiter as the backstop.', C['red']),
             (266, u'Retry storm', u'Every client retries at the same second',
              u'Full jitter plus Retry-After. Without it the 429s',
              u'themselves become the load.', C['amber']),
             (0, u'One noisy tenant', u'Shared pool, one customer eats it',
              u'Per-tenant limits under the global one, and a',
              u'reserved slice for everybody else.', C['blue']),
             (266, u'Limit is a mystery', u'Clients cannot see where they are',
              u'RateLimit-* headers on every response, and the',
              u'limit documented in numbers, not adjectives.', C['green'])]
    for i, (x, title, prob, l1, l2, col) in enumerate(items):
        y = 0 if i < 2 else 90
        f.rect(x, y, 256, 78, C['white'], C['border'], 0.75, 3.5)
        f.rect(x, y, 3.2, 78, col, None, 0, 0)
        f.text(x + 12, y + 17, title, col, 8.2, anchor='start')
        f.text(x + 12, y + 31, prob, C['muted'], 6.8, anchor='start')
        f.line([(x + 12, y + 40), (x + 244, y + 40)], C['border'], 0.75)
        f.text(x + 12, y + 54, l1, C['slate'], 6.9, anchor='start')
        f.text(x + 12, y + 65, l2, C['slate'], 6.9, anchor='start')
    return f.render()


def fig_family():
    """0.1 - the five algorithms at a glance"""
    f = Fig(522, 178)
    panels = [(0, u'Fixed window', C['red'], u'count, reset on the clock'),
              (105.5, u'Sliding log', C['green'], u'remember every timestamp'),
              (211, u'Sliding counter', C['blue'], u'blend two counts'),
              (316.5, u'Token bucket', C['amber'], u'spend a token'),
              (422, u'Leaky bucket', C['teal'], u'is there room?')]
    for x, name, col, sub in panels:
        f.rect(x, 0, 100, 152, C['white'], C['border'], 0.75, 3.5)
        f.rect(x, 0, 100, 3.0, col, None, 0, 0)
        f.text(x + 50, 22, name, col, 8.0)
        f.text(x + 50, 33, sub, C['muted'], 6.3)
    gy = 48.0
    # 1 fixed window: three boxes, bars inside, a red reset line
    for i in range(3):
        bx = 8 + i * 29
        f.rect(bx, gy, 25, 40, GREY, C['border'], 0.7, 2.0)
        for j in range(3):
            f.rect(bx + 4 + j * 6, gy + 32 - j * 8, 4, 8 + j * 8, C['red'], None, 0, 0.8)
        if i:
            f.line([(bx - 2, gy - 5), (bx - 2, gy + 45)], C['red'], 0.9, dash='2,1.8')
    f.text(50, gy + 58, u'2x across', C['red'], 6.4)
    f.text(50, gy + 68, u'the boundary', C['red'], 6.4)
    # 2 sliding log: ticks + bracket
    x0 = 105.5
    for i, dx in enumerate([12, 22, 30, 44, 52, 66, 78, 86]):
        col = C['muted'] if dx < 40 else C['green']
        f.line([(x0 + dx, gy + 12), (x0 + dx, gy + 34)], col, 1.4)
    f.line([(x0 + 40, gy + 42), (x0 + 92, gy + 42)], C['green'], 1.1)
    f.line([(x0 + 40, gy + 38), (x0 + 40, gy + 46)], C['green'], 1.1)
    f.line([(x0 + 92, gy + 38), (x0 + 92, gy + 46)], C['green'], 1.1)
    f.text(x0 + 50, gy + 58, u'exact,', C['green'], 6.4)
    f.text(x0 + 50, gy + 68, u'and expensive', C['green'], 6.4)
    # 3 sliding counter: two boxes + blend
    x0 = 211
    f.rect(x0 + 10, gy + 8, 38, 28, C['bluetint'], C['blue'], 0.8, 2.5)
    f.rect(x0 + 52, gy + 8, 38, 28, C['greentint'], C['green'], 0.8, 2.5)
    f.text(x0 + 29, gy + 26, u'80', C['blue'], 9.0)
    f.text(x0 + 71, gy + 26, u'20', C['green'], 9.0)
    f.text(x0 + 50, gy + 47, u'20 + 80 x 0.7 = 76', C['ink'], 6.6)
    f.text(x0 + 50, gy + 58, u'two ints,', C['blue'], 6.4)
    f.text(x0 + 50, gy + 68, u'~99.9% right', C['blue'], 6.4)
    # 4 token bucket
    x0 = 316.5
    f.arrow([(x0 + 50, gy + 2), (x0 + 50, gy + 12)], C['amber'], sw=0.9, hsize=4.4)
    f.rect(x0 + 32, gy + 14, 36, 30, C['white'], C['slate'], 1.0, 2.5)
    for r in range(2):
        for c in range(3):
            f.b.append('<circle cx="%.1f" cy="%.1f" r="4.2" fill="%s"/>'
                       % (x0 + 40 + c * 10, gy + 24 + r * 12, C['amber']))
    f.text(x0 + 50, gy + 58, u'bursts up to', C['amber'], 6.4)
    f.text(x0 + 50, gy + 68, u'capacity', C['amber'], 6.4)
    # 5 leaky bucket
    x0 = 422
    for dx in (38, 50, 62):
        f.line([(x0 + dx, gy + 2), (x0 + dx, gy + 11)], C['slate'], 1.3)
    f.rect(x0 + 32, gy + 14, 36, 30, C['white'], C['slate'], 1.0, 2.5)
    f.rect(x0 + 33.5, gy + 26, 33, 16.5, C['tealtint'], None, 0, 1.5)
    f.line([(x0 + 33.5, gy + 26), (x0 + 66.5, gy + 26)], C['teal'], 0.9)
    f.arrow([(x0 + 50, gy + 45), (x0 + 50, gy + 54)], C['teal'], sw=0.9, hsize=4.4)
    f.text(x0 + 50, gy + 68, u'the same thing', C['teal'], 6.4)
    f.text(261, 168, u'Two of these five are the same algorithm. One of them is broken. '
                     u'Knowing which is the whole topic.', C['slate'], 7.2)
    return f.render()


def fig_why():
    """1.2 - what a limit actually buys everybody else"""
    f = Fig(522, 186)
    for x0, title, sub, col in [
            (0, u'No limit', u'one caller, everybody\u2019s outage', C['red']),
            (266, u'With a limit', u'one caller gets 429s, nobody else notices', C['green'])]:
        f.rect(x0, 22, 256, 128, C['white'], C['border'], 0.75, 3.5)
        f.text(x0 + 128, 10, title, col, 8.4)
        f.text(x0 + 128, 19, sub, C['muted'], 6.6)
        f.line([(x0 + 40, 38), (x0 + 40, 138), (x0 + 244, 138)], C['slate'], 0.9)
        f.text(x0 + 36, 41, u'high', C['muted'], 6.0, anchor='end')
        f.text(x0 + 36, 138, u'0', C['muted'], 6.0, anchor='end')
        f.text(x0 + 142, 147, u'time', C['muted'], 6.2)
        f.line([(x0 + 50, 46), (x0 + 64, 46)], C['amber'], 1.6)
        f.text(x0 + 68, 48.4, u'the noisy client\u2019s request rate', C['slate'], 6.3,
               anchor='start')
        f.line([(x0 + 50, 58), (x0 + 64, 58)], col, 1.6)
        f.text(x0 + 68, 60.4, u'everybody else\u2019s p99 latency', C['slate'], 6.3,
               anchor='start')
    f.line([(40, 132), (100, 126), (150, 110), (190, 84), (215, 52), (234, 44)],
           C['amber'], 1.6)
    f.line([(40, 136), (110, 135), (160, 131), (196, 108), (220, 60), (234, 46)],
           C['red'], 1.6)
    f.line([(306, 132), (356, 126), (400, 110), (430, 98), (470, 98), (508, 98)],
           C['amber'], 1.6)
    f.line([(306, 136), (360, 136), (420, 135), (470, 135), (508, 135)], C['green'], 1.6)
    f.line([(430, 78), (430, 142)], C['green'], 1.0, dash='3,2.2')
    f.text(430, 74, u'limit', C['green'], 6.6)
    f.text(478, 92, u'429s from here on', C['amber'], 6.4)
    f.text(261, 176, u'The limit does not make the noisy client fast. It makes everybody '
                     u'else unaffected \u2014 and turns a mystery into a 429.', C['slate'], 7.2)
    return f.render()
