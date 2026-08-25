# -*- coding: utf-8 -*-
"""Figures for the Databases volume, drawn in the guide's existing visual language."""
from svgkit import Fig, C


def fig_choose():
    """1.1 - the access pattern decides the store, not the brand"""
    f = Fig(522, 250)
    # the question column
    qs = [(u'Does one query need', u'several entities joined?', 30),
          (u'Is the write rate above', u'~10k/s on one key space?', 78),
          (u'Is the query "find me', u'documents like this"?', 126),
          (u'Are you aggregating', u'billions of rows?', 174)]
    for t1, t2, y in qs:
        f.rect(0, y, 176, 38, C['panel'], C['border'], 0.75, 3.5)
        f.text(88, y + 15, t1, C['ink'], 7.2)
        f.text(88, y + 25, t2, C['ink'], 7.2)
    answers = [(u'Relational', u'Postgres / MySQL', 'blue', 30),
               (u'Wide-column / KV', u'Cassandra · DynamoDB', 'green', 78),
               (u'Search index', u'Elasticsearch', 'amber', 126),
               (u'Columnar / OLAP', u'ClickHouse · BigQuery', 'teal', 174)]
    for label, sub, kind, y in answers:
        f.node(300, y, label, kind, w=150, h=38, sub=sub, size=7.8)
        f.arrow([(184, y + 19), (296, y + 19)], C['slate'], sw=0.9)
        f.text(240, y + 14, u'yes', C['muted'], 6.1)
    f.rect(0, 216, 450, 26, C['bluetint'], C['blue'], 0.75, 3.5)
    f.text(225, 232, u'All four can be true at once — that is polyglot persistence, not indecision.',
           C['blue'], 7.2)
    return f.render()


def fig_engines():
    """2.1 - B-tree vs LSM write path"""
    f = Fig(522, 258)
    f.text(120, 10, u'B-tree — update in place', C['blue'], 8.2)
    f.text(400, 10, u'LSM tree — append, then merge', C['green'], 8.2)
    f.line([(261, 4), (261, 250)], C['border'], 0.75, dash='3 3')

    # ---- B-tree side ----
    f.node(78, 22, u'write', 'app', w=84, h=24, size=7.4)
    f.node(78, 60, u'WAL append', 'plain', w=84, h=24, size=7.4)
    f.arrow([(120, 46), (120, 58)], C['slate'])
    f.rect(20, 100, 200, 62, C['bluetint'], C['blue'], 0.75, 3.5)
    f.text(120, 114, u'find the leaf page, modify it in place', C['blue'], 7.0)
    for i in range(4):
        f.rect(34 + i * 46, 122, 40, 14, C['white'], C['blue'], 0.7, 2)
        f.text(54 + i * 46, 132, u'page %d' % (i + 1), C['blue'], 6.0)
    f.text(120, 152, u'page full → split (write amplification)', C['red'], 6.6)
    f.arrow([(120, 84), (120, 98)], C['slate'])
    f.node(78, 176, u'one random write per page', 'plain', w=84, h=30, size=6.6)
    f.arrow([(120, 162), (120, 174)], C['slate'])
    f.text(120, 220, u'Reads: one page walk, ~3–4 levels.', C['slate'], 7.0)
    f.text(120, 232, u'Writes: random I/O, in-place.', C['slate'], 7.0)

    # ---- LSM side ----
    f.node(360, 22, u'write', 'app', w=84, h=24, size=7.4)
    f.node(360, 60, u'WAL append', 'plain', w=84, h=24, size=7.4)
    f.arrow([(402, 46), (402, 58)], C['slate'])
    f.node(360, 98, u'memtable (RAM, sorted)', 'green', w=84, h=26, size=6.6)
    f.arrow([(402, 84), (402, 96)], C['slate'])
    f.text(470, 111, u'flush when full', C['muted'], 6.1, anchor='start')
    f.rect(292, 136, 220, 60, C['greentint'], C['green'], 0.75, 3.5)
    f.text(402, 149, u'immutable SSTables on disk, newest first', C['green'], 7.0)
    for i, w in enumerate((44, 62, 88)):
        f.rect(302, 156 + i * 12, w, 9, C['white'], C['green'], 0.6, 1.5)
        f.text(306, 163 + i * 12, u'L%d' % i, C['green'], 5.6, anchor='start')
    f.text(430, 168, u'compaction merges levels', C['green'], 6.4, anchor='start')
    f.text(430, 180, u'and drops tombstones', C['green'], 6.4, anchor='start')
    f.arrow([(402, 122), (402, 134)], C['slate'])
    f.text(402, 220, u'Reads: check memtable, then every level —', C['slate'], 7.0)
    f.text(402, 232, u'Bloom filters make the misses cheap.', C['slate'], 7.0)
    return f.render()


def fig_index():
    """3.1 - the leftmost-prefix rule on a composite index"""
    f = Fig(522, 196)
    f.text(261, 10, u'INDEX (tenant_id, created_at, status)', C['ink'], 8.2)
    xs = [70, 200, 330]
    labels = [u'tenant_id', u'created_at', u'status']
    for x, lab in zip(xs, labels):
        f.rect(x - 56, 22, 112, 24, C['bluetint'], C['blue'], 0.75, 3)
        f.text(x, 38, lab, C['blue'], 7.4)
    for x in xs[:-1]:
        f.arrow([(x + 58, 34), (x + 70, 34)], C['slate'], sw=0.8, hsize=5)

    rows = [
        (u'WHERE tenant_id = ?', u'full index seek', 'good'),
        (u'WHERE tenant_id = ? AND created_at > ?', u'seek + range scan', 'good'),
        (u'WHERE tenant_id = ? ORDER BY created_at', u'seek, no sort needed', 'good'),
        (u'WHERE created_at > ?', u'index unusable — scan', 'bad'),
        (u'WHERE tenant_id = ? AND status = ?', u'seek, then filter every row', 'warn'),
    ]
    y = 62
    for q, verdict, kind in rows:
        col = {'good': C['green'], 'bad': C['red'], 'warn': C['amber']}[kind]
        tint = {'good': C['greentint'], 'bad': C['pink'], 'warn': C['ambertint']}[kind]
        f.rect(0, y, 300, 21, tint, col, 0.7, 2.5)
        f.text(8, y + 14, q, C['ink'], 7.0, anchor='start', font='var(--mono)')
        f.text(312, y + 14, verdict, col, 7.0, anchor='start')
        y += 26
    return f.render()


def fig_skew():
    """5.1 - write skew: both transactions read a valid state and both commit"""
    f = Fig(522, 190)
    f.text(261, 10, u'Two on-call engineers, rule: at least one must stay on call', C['ink'], 8.2)
    # lanes
    for i, (name, col) in enumerate(((u'TX A — Alice goes off call', C['blue']),
                                     (u'TX B — Bob goes off call', C['purple']))):
        y = 26 + i * 78
        f.rect(0, y, 522, 66, C['panel'], C['border'], 0.75, 3.5)
        f.text(10, y + 14, name, col, 7.4, anchor='start')
        who = u'alice' if i == 0 else u'bob'
        steps = [(u'SELECT count(*) WHERE on_call', u'→ 2, so it is safe to leave'),
                 (u'UPDATE %s SET on_call = false' % who, u'one row, no conflict'),
                 (u'COMMIT', u'succeeds')]
        x = 12
        for s, note in steps:
            w = 176 if len(s) > 12 else 100
            f.rect(x, y + 22, w, 32, C['white'], col, 0.7, 2.5)
            f.text(x + 6, y + 36, s, C['ink'], 6.2, anchor='start', font='var(--mono)')
            f.text(x + 6, y + 47, note, C['muted'], 6.2, anchor='start')
            x += w + 8
    f.rect(0, 168, 522, 20, C['pink'], C['red'], 0.75, 3)
    f.text(261, 182, u'Both snapshots were valid. Nobody is on call. Snapshot isolation '
                     u'permits this; SERIALIZABLE or SELECT … FOR UPDATE does not.',
           C['red'], 7.0)
    return f.render()
