# -*- coding: utf-8 -*-
"""Figures for the Sharding volume."""
import math

from svgkit import Fig, C


def fig_keys():
    """2.1 - the same 4 nodes, three shard keys, three distributions"""
    f = Fig(522, 214)
    panels = [
        (0, u'hash(user_id)', C['green'], [26, 24, 25, 25],
         u'even, but no range scans'),
        (178, u'range(created_at)', C['red'], [4, 6, 12, 78],
         u'every new write on the last shard'),
        (356, u'range(tenant_id)', C['amber'], [58, 14, 18, 10],
         u'one big tenant dominates'),
    ]
    for x0, title, col, bars, note in panels:
        f.rect(x0, 0, 166, 196, C['white'], C['border'], 0.75, 3.5)
        f.text(x0 + 83, 15, title, col, 7.8)
        base = 150
        for i, v in enumerate(bars):
            h = 1.0 * v
            bx = x0 + 20 + i * 34
            f.rect(bx, base - h, 24, h, col, None, 0, 1.5)
            f.text(bx + 12, base + 11, u'S%d' % (i + 1), C['muted'], 6.1)
            f.text(bx + 12, base - h - 3, u'%d%%' % v, col, 5.8)
        f.line([(x0 + 14, base), (x0 + 152, base)], C['border'], 0.8)
        f.text(x0 + 83, 176, note, C['slate'], 6.6)
    f.rect(0, 204, 522, 0.8, C['border'])
    return f.render()


def fig_ring():
    """3.1 - consistent hashing with virtual nodes, and what a join actually moves"""
    f = Fig(522, 250)
    cx, cy, r = 108.0, 124.0, 82.0
    f.b.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" '
               'stroke-width="1.1"/>' % (cx, cy, r, C['border']))
    cols = [C['blue'], C['green'], C['purple'], C['amber']]
    names = [u'A', u'B', u'C', u'D']
    for i in range(12):
        ang = -math.pi / 2 + i * (2 * math.pi / 12) + 0.12
        node = i % 4
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        f.b.append('<circle cx="%.1f" cy="%.1f" r="6.2" fill="%s"/>' % (x, y, cols[node]))
        f.text(x, y + 2.3, names[node], C['white'], 5.8)
    # a key hashing onto the left of the ring, so its label has room
    ang = math.pi * 0.80
    kx, ky = cx + r * math.cos(ang), cy + r * math.sin(ang)
    f.b.append('<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (kx, ky, C['red']))
    f.text(kx + 9, ky - 2, u'hash(key)', C['red'], 6.4, anchor='start')
    f.text(kx + 9, ky + 9, u'walks clockwise', C['muted'], 6.1, anchor='start')
    f.text(cx, cy - 4, u'hash ring', C['slate'], 7.4)
    f.text(cx, cy + 8, u'0 .. 2^32-1', C['muted'], 6.4)

    lx, lw = 252, 270
    f.text(lx, 20, u'Why virtual nodes', C['ink'], 8.2, anchor='start')
    for j, t in enumerate([
            u'Each physical node owns many small arcs, not one big one.',
            u'Adding a node steals a slice from every other node, so it',
            u'moves ~1/N of the keys instead of rehashing everything.',
            u'Replicas = the next R distinct physical nodes clockwise.']):
        f.text(lx, 36 + j * 12, t, C['slate'], 6.9, anchor='start')
    f.rect(lx, 92, lw, 54, C['greentint'], C['green'], 0.75, 3.5)
    f.text(lx + 10, 108, u'modulo hashing:  hash(key) % N', C['green'], 7.0, anchor='start',
           font='var(--mono)')
    f.text(lx + 10, 123, u'N changes and almost every key moves.', C['red'], 6.9, anchor='start')
    f.text(lx + 10, 136, u'That is the outage nobody plans for.', C['red'], 6.9, anchor='start')
    f.rect(lx, 156, lw, 80, C['bluetint'], C['blue'], 0.75, 3.5)
    f.text(lx + 10, 172, u'Alternatives worth naming', C['blue'], 7.2, anchor='start')
    for j, t in enumerate([
            u'Rendezvous (HRW) hashing: no ring, same minimal',
            u'movement, and weights are easy to express.',
            u'Jump consistent hash: tiny and fast, but nodes can',
            u'only be added or removed at the end.']):
        f.text(lx + 10, 188 + j * 12, t, C['blue'], 6.6, anchor='start')
    return f.render()


def fig_reshard():
    """5.1 - a live resharding, in the order you must say it"""
    f = Fig(522, 176)
    steps = [
        (u'1 · Dual-write', u'writes go to old and new shard', C['blue']),
        (u'2 · Backfill', u'copy history in throttled batches', C['teal']),
        (u'3 · Verify', u'checksum ranges, compare counts', C['amber']),
        (u'4 · Flip reads', u'per-tenant or per-key, reversible', C['green']),
        (u'5 · Stop writing old', u'then drop it, days later', C['purple']),
    ]
    w = 96
    for i, (t, d, col) in enumerate(steps):
        x = i * 106
        f.rect(x, 24, w, 58, C['white'], col, 0.9, 3.5)
        f.text(x + w / 2, 42, t, col, 7.2)
        for j, line in enumerate(d.split(' ', 3)[:1] + [' '.join(d.split(' ')[1:])]):
            f.text(x + w / 2, 56 + j * 10, line, C['slate'], 6.2)
        if i < 4:
            f.arrow([(x + w + 1, 53), (x + w + 8, 53)], C['slate'], sw=0.9, hsize=5)
    f.text(261, 12, u'Every step is reversible until the last one', C['ink'], 8.2)
    f.rect(0, 96, 522, 30, C['pink'], C['red'], 0.75, 3.5)
    f.text(261, 108, u'The failure mode: flipping reads before verification, with no way back.',
           C['red'], 7.0)
    f.text(261, 119, u'Keep the old shard writable until you have served the new one for days.',
           C['red'], 7.0)
    f.rect(0, 136, 522, 32, C['bluetint'], C['blue'], 0.75, 3.5)
    f.text(261, 148, u'Shortcut worth naming: shard into 1,024 logical buckets on day one,',
           C['blue'], 7.0)
    f.text(261, 160, u'then move buckets between nodes. Resharding becomes a routing change.',
           C['blue'], 7.0)
    return f.render()
