# -*- coding: utf-8 -*-
"""Figures for the Replication & Consistency volume."""
from svgkit import Fig, C


def fig_ladder():
    """1.1 - the consistency ladder, strongest at the top"""
    f = Fig(522, 232)
    rows = [
        (u'Linearizable', u'every read sees the latest committed write, globally',
         u'money, inventory, unique-name claims', C['red']),
        (u'Sequential / causal', u'related events keep their order; unrelated ones may not',
         u'chat messages, comment threads', C['amber']),
        (u'Read-your-writes', u'you always see your own updates',
         u'any user-facing write: profile, post', C['purple']),
        (u'Monotonic reads', u'time never runs backwards for one session',
         u'feeds, timelines, dashboards', C['blue']),
        (u'Eventual', u'replicas converge, eventually, with no ordering promise',
         u'counters, likes, view counts, analytics', C['green']),
    ]
    y = 26
    for name, meaning, use, col in rows:
        f.rect(0, y, 522, 34, C['white'], col, 0.9, 3.5)
        f.rect(0, y, 4.4, 34, col)
        f.text(14, y + 15, name, col, 8.0, anchor='start')
        f.text(14, y + 27, meaning, C['slate'], 6.8, anchor='start')
        f.text(514, y + 21, use, C['muted'], 6.8, anchor='end')
        y += 40
    f.text(0, 14, u'stronger — more coordination, more latency', C['red'], 7.0, anchor='start')
    f.text(522, 14, u'weaker — cheaper, faster, more surprises', C['green'], 7.0, anchor='end')
    f.text(261, 228, u'Pick per operation, not per system.', C['ink'], 7.4)
    return f.render()


def fig_quorum():
    """3.1 - why W + R > N is the whole idea"""
    f = Fig(522, 216)
    f.text(261, 12, u'N = 3 replicas: the write set and the read set must overlap', C['ink'],
           8.2)

    def cluster(x0, title, w_set, r_set, verdict, col):
        f.text(x0 + 111, 32, title, C['ink'], 7.6)
        for i in range(3):
            x = x0 + 12 + i * 70
            inw, inr = i in w_set, i in r_set
            fill = C['white']
            if inw and inr:
                fill = C['ambertint']
            elif inw:
                fill = C['bluetint']
            elif inr:
                fill = C['greentint']
            f.rect(x, 42, 58, 46, fill, C['border'], 0.8, 3.5)
            f.text(x + 29, 60, u'R%d' % (i + 1), C['slate'], 7.0)
            tag = u'W' if inw and not inr else (u'R' if inr and not inw else
                                               (u'W+R' if inw else u'—'))
            tcol = C['blue'] if inw and not inr else (C['green'] if inr and not inw else
                                                     (C['amber'] if inw else C['muted']))
            f.text(x + 29, 76, tag, tcol, 7.4)
        f.rect(x0, 98, 222, 28, C['greentint'] if col == 'ok' else C['pink'],
               C['green'] if col == 'ok' else C['red'], 0.8, 3)
        f.text(x0 + 111, 116, verdict, C['green'] if col == 'ok' else C['red'], 7.0)

    cluster(0, u'W = 2, R = 2  →  2 + 2 > 3', {0, 1}, {1, 2},
            u'the sets share R2, so the read sees the write', 'ok')
    cluster(300, u'W = 1, R = 1  →  1 + 1 < 3', {0}, {2},
            u'no overlap: the read can miss the write', 'bad')

    f.rect(0, 140, 522, 68, C['panel'], C['border'], 0.75, 3.5)
    f.text(12, 158, u'The three settings you should be able to justify', C['ink'], 7.4,
           anchor='start')
    for i, t in enumerate([
            u'W=N, R=1  — fast reads, slow and fragile writes: one replica down blocks writing.',
            u'W=1, R=1  — fastest and weakest: eventual, and the classic “I read stale data” bug.',
            u'W=2, R=2 (N=3) — the default. Survives one node down, and a read overlaps the '
            u'last write.']):
        f.text(12, 174 + i * 12, t, C['slate'], 6.9, anchor='start')
    return f.render()


def fig_raft():
    """4.1 - what a consensus round actually costs"""
    f = Fig(522, 208)
    f.text(261, 12, u'Raft: one leader, a replicated log, and a majority on every commit',
           C['ink'], 8.2)
    # nodes
    f.node(40, 30, u'leader', 'blue', w=96, h=30, sub=u'term 7', size=7.4)
    f.node(210, 30, u'follower', 'plain', w=96, h=30, sub=u'in sync', size=7.4)
    f.node(380, 30, u'follower', 'plain', w=96, h=30, sub=u'lagging', size=7.4)
    f.arrow([(140, 45), (206, 45)], C['blue'], sw=0.9, hsize=5)
    f.arrow([(310, 45), (376, 45)], C['blue'], sw=0.9, hsize=5)
    f.text(173, 40, u'AppendEntries', C['blue'], 6.2)
    f.text(343, 40, u'AppendEntries', C['blue'], 6.2)

    # the log
    f.text(0, 84, u'log', C['slate'], 6.8, anchor='start')
    for i in range(8):
        x = 30 + i * 58
        committed = i < 5
        f.rect(x, 74, 52, 22, C['greentint'] if committed else C['white'],
               C['green'] if committed else C['border'], 0.8, 2.5)
        f.text(x + 26, 89, u'e%d' % (i + 1), C['green'] if committed else C['muted'], 6.6)
    f.text(30 + 5 * 58 - 4, 108, u'commit index — a majority has it', C['green'], 6.6,
           anchor='middle')

    f.rect(0, 122, 254, 78, C['bluetint'], C['blue'], 0.75, 3.5)
    f.text(12, 138, u'What it guarantees', C['blue'], 7.4, anchor='start')
    for i, t in enumerate([
            u'One leader per term, elected by a majority.',
            u'A committed entry is on a majority of nodes,',
            u'so it survives any minority failing.',
            u'Followers never accept a stale leader’s log.']):
        f.text(12, 152 + i * 12, t, C['ink'], 6.8, anchor='start')

    f.rect(268, 122, 254, 78, C['ambertint'], C['amber'], 0.75, 3.5)
    f.text(280, 138, u'What it costs', C['amber'], 7.4, anchor='start')
    for i, t in enumerate([
            u'Every write pays a round trip to a majority.',
            u'2f+1 nodes to survive f failures — 5 for two.',
            u'A minority partition cannot make progress:',
            u'that is CAP choosing C over A, deliberately.']):
        f.text(280, 152 + i * 12, t, C['ink'], 6.8, anchor='start')
    return f.render()


def fig_region():
    """6.1 - three multi-region shapes and what each one really promises"""
    f = Fig(522, 214)
    shapes = [
        (0, u'Active–passive', C['blue'],
         [u'writes in one region, async copy',
          u'RPO: seconds of loss',
          u'RTO: minutes, needs a promotion',
          u'simple, and the default answer']),
        (178, u'Active–active, partitioned', C['green'],
         [u'each region owns a key range',
          u'no write conflicts by construction',
          u'cross-region reads are stale',
          u'the pattern most large systems use']),
        (356, u'Active–active, everywhere', C['amber'],
         [u'any region takes any write',
          u'conflicts are guaranteed: LWW or CRDT',
          u'or consensus per write, at 80–100 ms',
          u'only worth it if the product demands it']),
    ]
    for x0, title, col, lines in shapes:
        f.rect(x0, 22, 166, 132, C['white'], col, 0.9, 3.5)
        f.rect(x0, 22, 166, 22, col)
        f.text(x0 + 83, 37, title, C['white'], 7.4)
        for i, t in enumerate(lines):
            f.text(x0 + 10, 60 + i * 22, u'·', col, 7.4, anchor='start')
            f.text(x0 + 18, 60 + i * 22, t, C['slate'], 6.6, anchor='start')
    f.rect(0, 166, 522, 42, C['panel'], C['border'], 0.75, 3.5)
    f.text(261, 182, u'A cross-region round trip is 80–100 ms. That single number decides the '
                     u'shape: anything on the write path', C['slate'], 7.0)
    f.text(261, 196, u'that needs another region is a user-visible cost, so keep writes local '
                     u'and replicate asynchronously.', C['slate'], 7.0)
    return f.render()
