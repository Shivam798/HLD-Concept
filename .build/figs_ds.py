# -*- coding: utf-8 -*-
"""Figures for the Data Structures volume."""
from svgkit import Fig, C


def fig_bloom():
    """2.1 - insert with k hashes, then the two possible answers"""
    f = Fig(522, 224)
    n = 20
    cellw = 20.0
    x0 = 66.0
    set_bits = {2, 5, 9, 11, 14, 17}
    # the bit array
    f.text(x0 - 8, 44, u'bit array', C['slate'], 6.8, anchor='end')
    f.text(x0 - 8, 54, u'm bits', C['muted'], 6.2, anchor='end')
    for i in range(n):
        x = x0 + i * cellw
        on = i in set_bits
        f.rect(x, 34, cellw - 2, 22, C['purple'] if on else C['white'],
               C['purple'] if on else C['border'], 0.7, 2)
        f.text(x + (cellw - 2) / 2, 49, u'1' if on else u'0',
               C['white'] if on else C['muted'], 6.6)
    # insert
    f.text(x0, 18, u'add("alice")  →  set the bits at h1, h2, h3', C['purple'], 7.4,
           anchor='start')
    for i, idx in enumerate((2, 9, 14)):
        x = x0 + idx * cellw + (cellw - 2) / 2
        f.arrow([(x, 26), (x, 32)], C['purple'], sw=0.9, hsize=4.6)
        f.text(x, 24, u'h%d' % (i + 1), C['purple'], 5.8)

    # query 1 - definitely absent
    f.rect(0, 78, 254, 62, C['greentint'], C['green'], 0.75, 3.5)
    f.text(12, 94, u'contains("carol")', C['green'], 7.4, anchor='start', font='var(--mono)')
    f.text(12, 108, u'one of its three bits is 0', C['ink'], 6.9, anchor='start')
    f.text(12, 122, u'DEFINITELY NOT PRESENT — no false negatives,', C['green'], 6.9,
           anchor='start')
    f.text(12, 133, u'which is why it is safe to reject on.', C['green'], 6.9, anchor='start')

    # query 2 - maybe present
    f.rect(268, 78, 254, 62, C['ambertint'], C['amber'], 0.75, 3.5)
    f.text(280, 94, u'contains("bob")', C['amber'], 7.4, anchor='start', font='var(--mono)')
    f.text(280, 108, u'all three bits are 1', C['ink'], 6.9, anchor='start')
    f.text(280, 122, u'PROBABLY PRESENT — or three other keys lit', C['amber'], 6.9,
           anchor='start')
    f.text(280, 133, u'those bits. That is the false positive.', C['amber'], 6.9, anchor='start')

    # sizing
    f.rect(0, 152, 522, 60, C['panel'], C['border'], 0.75, 3.5)
    f.text(12, 168, u'Sizing, the only formula worth memorising', C['ink'], 7.4, anchor='start')
    f.text(12, 184, u'm = -n ln(p) / (ln 2)^2', C['navy'], 7.6, anchor='start',
           font='var(--mono)')
    f.text(196, 184, u'k = (m/n) ln 2', C['navy'], 7.6, anchor='start', font='var(--mono)')
    f.text(12, 202, u'1% false positives cost ~9.6 bits per item, whatever the item is: '
                    u'1.2 GB for a billion keys.', C['slate'], 6.9, anchor='start')
    return f.render()


def fig_hll():
    """3.1 - counting distinct things by watching for improbable hashes"""
    f = Fig(522, 200)
    f.text(261, 12, u'Count distinct without storing anything', C['ink'], 8.2)
    # the intuition
    f.rect(0, 24, 250, 78, C['bluetint'], C['blue'], 0.75, 3.5)
    f.text(12, 40, u'The intuition', C['blue'], 7.4, anchor='start')
    for i, t in enumerate([
            u'Hash each item to a random bit string.',
            u'Track the longest run of leading zeros seen.',
            u'A run of 10 zeros appears about once in 2^10',
            u'items — so it implies ~1,000 distinct items.']):
        f.text(12, 54 + i * 12, t, C['ink'], 6.8, anchor='start')
    # the fix
    f.rect(272, 24, 250, 78, C['greentint'], C['green'], 0.75, 3.5)
    f.text(284, 40, u'Why it is accurate', C['green'], 7.4, anchor='start')
    for i, t in enumerate([
            u'One estimate has huge variance, so the hash is',
            u'split into 16,384 buckets (registers), each',
            u'keeping its own max. The harmonic mean of the',
            u'registers gives ~0.81% error in 12 KB, forever.']):
        f.text(284, 54 + i * 12, t, C['ink'], 6.8, anchor='start')
    # registers strip
    f.text(0, 126, u'registers', C['slate'], 6.8, anchor='start')
    vals = [3, 5, 2, 7, 4, 3, 6, 2, 5, 4, 8, 3, 4, 6, 2, 5]
    for i, v in enumerate(vals):
        x = 62 + i * 28
        h = 4.0 * v
        f.rect(x, 152 - h, 20, h, C['purple'], None, 0, 1.5)
        f.text(x + 10, 162, u'%d' % v, C['muted'], 5.8)
    f.line([(58, 152), (522, 152)], C['border'], 0.8)
    f.rect(0, 172, 522, 24, C['panel'], C['border'], 0.75, 3)
    f.text(261, 187, u'Mergeable: the union of two HLLs is the per-register maximum — which is '
                     u'why daily sketches roll up into a month.', C['slate'], 7.0)
    return f.render()


def fig_cms():
    """4.1 - count-min sketch: d rows, w counters, take the minimum"""
    f = Fig(522, 190)
    f.text(261, 12, u'Count-Min Sketch — frequency of anything, in fixed memory', C['ink'], 8.2)
    rows = [(u'h1', [4, 12, 3, 9, 6, 2, 11, 5]),
            (u'h2', [7, 5, 14, 3, 10, 8, 4, 6]),
            (u'h3', [2, 9, 6, 11, 5, 13, 3, 7])]
    hit = [(0, 3), (1, 6), (2, 1)]
    x0, y0, cw, ch = 70.0, 30.0, 40.0, 26.0
    for r, (label, counters) in enumerate(rows):
        f.text(x0 - 10, y0 + r * (ch + 6) + 17, label, C['slate'], 7.0, anchor='end',
               font='var(--mono)')
        for c, v in enumerate(counters):
            on = (r, c) in hit
            x = x0 + c * cw
            y = y0 + r * (ch + 6)
            f.rect(x, y, cw - 3, ch, C['ambertint'] if on else C['white'],
                   C['amber'] if on else C['border'], 0.9 if on else 0.7, 2.5)
            f.text(x + (cw - 3) / 2, y + 17, u'%d' % v, C['amber'] if on else C['slate'], 7.0)
    f.text(x0 + 8 * cw + 8, y0 + 17, u'query "GET /x" hits these', C['amber'], 6.9, anchor='start')
    f.text(x0 + 8 * cw + 8, y0 + 45, u'one cell per row', C['muted'], 6.4, anchor='start')
    f.text(x0 + 8 * cw + 8, y0 + 73, u'estimate = min(9, 4, 9) = 4', C['ink'], 6.9,
           anchor='start')
    f.rect(0, 128, 254, 54, C['greentint'], C['green'], 0.75, 3.5)
    f.text(12, 144, u'What it guarantees', C['green'], 7.4, anchor='start')
    f.text(12, 158, u'Never undercounts. Overcounts only when every', C['ink'], 6.8,
           anchor='start')
    f.text(12, 170, u'row collides — so take the minimum.', C['ink'], 6.8, anchor='start')
    f.rect(268, 128, 254, 54, C['bluetint'], C['blue'], 0.75, 3.5)
    f.text(280, 144, u'What it is for', C['blue'], 7.4, anchor='start')
    f.text(280, 158, u'Heavy hitters: hot keys, top URLs, abusive IPs,', C['ink'], 6.8,
           anchor='start')
    f.text(280, 170, u'trending terms — at millions of events a second.', C['ink'], 6.8,
           anchor='start')
    return f.render()


def fig_merkle():
    """6.1 - finding the one differing block without comparing everything"""
    f = Fig(522, 196)
    f.text(261, 12, u'Merkle tree — compare two replicas in log(n) messages', C['ink'], 8.2)

    def tree(x0, label, diff_leaf, col):
        f.text(x0 + 108, 32, label, col, 7.4)
        f.node(x0 + 78, 40, u'root', 'plain', w=60, h=20, size=6.6)
        for i in range(2):
            f.node(x0 + 24 + i * 108, 78, u'h%d' % (i + 1), 'plain', w=60, h=20, size=6.6)
            f.line([(x0 + 108, 60), (x0 + 54 + i * 108, 76)], C['slate'], 0.8)
        for i in range(4):
            leaf_col = 'cache' if i == diff_leaf else 'plain'
            f.node(x0 + i * 54, 118, u'b%d' % (i + 1), leaf_col, w=46, h=20, size=6.6)
            parent = x0 + 54 + (0 if i < 2 else 108)
            f.line([(parent, 98), (x0 + 23 + i * 54, 116)], C['slate'], 0.8)

    tree(0, u'replica A', None, C['blue'])
    tree(280, u'replica B', 2, C['purple'])
    f.line([(261, 26), (261, 146)], C['border'], 0.75, dash='3 3')
    f.rect(0, 152, 522, 40, C['panel'], C['border'], 0.75, 3.5)
    f.text(261, 168, u'Roots differ → compare the two children → only one subtree differs → '
                     u'descend. Four messages, not four million.', C['slate'], 7.0)
    f.text(261, 182, u'This is anti-entropy repair in Dynamo, Cassandra and Riak, and how Git '
                     u'and rsync avoid shipping whole files.', C['muted'], 6.8)
    return f.render()
