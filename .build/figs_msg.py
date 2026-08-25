# -*- coding: utf-8 -*-
"""Figures for the Messaging & Streams volume."""
from svgkit import Fig, C


def fig_queue_vs_log():
    """1.1 - a queue deletes, a log remembers"""
    f = Fig(522, 226)
    # queue
    f.text(120, 12, u'Queue — work to be done', C['blue'], 8.2)
    f.rect(0, 22, 250, 88, C['bluetint'], C['blue'], 0.8, 3.5)
    for i in range(4):
        f.rect(14 + i * 56, 40, 46, 22, C['white'], C['blue'], 0.7, 2.5)
        f.text(37 + i * 56, 55, u'job %d' % (i + 1), C['blue'], 6.4)
    f.text(125, 78, u'one consumer takes a message and it is gone', C['ink'], 6.8)
    f.text(125, 92, u'competing consumers · scale by adding workers', C['slate'], 6.8)
    f.node(14, 122, u'worker A', 'plain', w=70, h=22, size=6.6)
    f.node(96, 122, u'worker B', 'plain', w=70, h=22, size=6.6)
    f.node(178, 122, u'worker C', 'plain', w=70, h=22, size=6.6)
    f.text(125, 160, u'SQS · RabbitMQ · Celery', C['muted'], 7.0)

    # log
    f.text(400, 12, u'Log — events that happened', C['green'], 8.2)
    f.rect(272, 22, 250, 88, C['greentint'], C['green'], 0.8, 3.5)
    for i in range(6):
        f.rect(284 + i * 38, 40, 32, 22, C['white'], C['green'], 0.7, 2.5)
        f.text(300 + i * 38, 55, u'e%d' % (i + 1), C['green'], 6.4)
    f.text(397, 78, u'nothing is removed; each consumer keeps an offset', C['ink'], 6.8)
    f.text(397, 92, u'replay from any point · many independent readers', C['slate'], 6.8)
    f.node(286, 122, u'search idx', 'plain', w=70, h=22, size=6.6)
    f.node(368, 122, u'analytics', 'plain', w=70, h=22, size=6.6)
    f.node(450, 122, u'audit', 'plain', w=64, h=22, size=6.6)
    f.text(397, 160, u'Kafka · Pulsar · Kinesis · Redis Streams', C['muted'], 7.0)

    f.rect(0, 176, 522, 44, C['panel'], C['border'], 0.75, 3.5)
    f.text(261, 194, u'Ask one question to choose: does a second team, later, need to read '
                     u'these same events?', C['ink'], 7.4)
    f.text(261, 209, u'Yes → log. No, it is work to be executed once → queue.', C['slate'], 7.0)
    return f.render()


def fig_partitions():
    """2.1 - partitions, keys, consumer groups and where ordering lives"""
    f = Fig(522, 236)
    f.text(261, 12, u'One topic, three partitions: ordering is per partition, never per topic',
           C['ink'], 8.2)
    cols = [C['blue'], C['purple'], C['teal']]
    for pnum in range(3):
        y = 26 + pnum * 56
        col = cols[pnum]
        f.text(0, y + 20, u'P%d' % pnum, col, 7.6, anchor='start')
        for i in range(7):
            f.rect(24 + i * 44, y, 38, 24, C['white'], col, 0.75, 2.5)
            f.text(43 + i * 44, y + 16, u'%d' % i, col, 6.6)
        f.text(340, y + 16, u'offset →', C['muted'], 6.4, anchor='start')
        f.node(392, y - 1, u'consumer %d' % (pnum + 1), 'plain', w=94, h=26, size=6.8)
        f.arrow([(336, y + 12), (388, y + 12)], C['slate'], sw=0.8, hsize=5)
    f.rect(0, 196, 254, 34, C['greentint'], C['green'], 0.75, 3.5)
    f.text(12, 210, u'key → partition', C['green'], 7.2, anchor='start')
    f.text(12, 223, u'same key, same partition, so per-key order holds', C['ink'], 6.7,
           anchor='start')
    f.rect(268, 196, 254, 34, C['pink'], C['red'], 0.75, 3.5)
    f.text(280, 210, u'more consumers than partitions', C['red'], 7.2, anchor='start')
    f.text(280, 223, u'the extras idle — partitions are the unit of parallelism', C['ink'], 6.7,
           anchor='start')
    return f.render()


def fig_outbox():
    """3.1 - the only safe way to write a row and publish an event"""
    f = Fig(522, 214)
    f.text(261, 12, u'“Save the order and publish OrderCreated” — atomically', C['ink'], 8.2)

    # wrong
    f.rect(0, 26, 250, 96, C['pink'], C['red'], 0.8, 3.5)
    f.text(125, 42, u'Dual write (broken)', C['red'], 7.6)
    f.node(14, 54, u'service', 'app', w=64, h=24, size=6.8)
    f.node(160, 54, u'database', 'db', w=64, h=24, size=6.8)
    f.node(160, 90, u'broker', 'plain', w=64, h=24, size=6.8)
    f.arrow([(80, 66), (156, 66)], C['slate'], sw=0.85, hsize=5)
    f.arrow([(46, 78), (46, 102), (156, 102)], C['red'], sw=0.85, hsize=5)
    f.text(112, 118, u'second write can fail: row exists, event never sent', C['red'], 6.5)

    # right
    f.rect(272, 26, 250, 96, C['greentint'], C['green'], 0.8, 3.5)
    f.text(397, 42, u'Outbox (correct)', C['green'], 7.6)
    f.node(284, 54, u'service', 'app', w=64, h=24, size=6.8)
    f.node(392, 54, u'orders +', 'db', w=70, h=24, sub=u'outbox row', size=6.6)
    f.node(392, 92, u'relay / CDC', 'green', w=70, h=22, size=6.6)
    f.node(478, 92, u'broker', 'plain', w=40, h=22, size=6.2)
    f.arrow([(350, 66), (388, 66)], C['slate'], sw=0.85, hsize=5)
    f.arrow([(427, 80), (427, 90)], C['green'], sw=0.85, hsize=5)
    f.arrow([(462, 103), (474, 103)], C['green'], sw=0.85, hsize=5)
    f.text(397, 118, u'one transaction writes both; the relay publishes later', C['green'], 6.5)

    f.rect(0, 136, 522, 70, C['panel'], C['border'], 0.75, 3.5)
    f.text(12, 154, u'What this buys, and what it still costs', C['ink'], 7.4, anchor='start')
    for i, t in enumerate([
            u'Buys: the row and the event cannot disagree — they commit or fail together.',
            u'Costs: the event is published after the commit, so consumers are eventually '
            u'consistent (milliseconds).',
            u'Still at-least-once: the relay can publish twice, so every consumer must be '
            u'idempotent.']):
        f.text(12, 170 + i * 12, t, C['slate'], 6.9, anchor='start')
    return f.render()


def fig_delivery():
    """4.1 - the three delivery semantics, and where the duplicate comes from"""
    f = Fig(522, 190)
    f.text(261, 12, u'Where the duplicate and the loss actually come from', C['ink'], 8.2)
    boxes = [
        (0, u'At most once', C['red'],
         [u'ack before processing', u'crash → message lost', u'metrics, fire-and-forget logs']),
        (178, u'At least once', C['green'],
         [u'ack after processing', u'crash → redelivered', u'the default everywhere']),
        (356, u'Effectively once', C['blue'],
         [u'at-least-once + dedupe', u'idempotency key or txn', u'payments, orders, ledgers']),
    ]
    for x0, title, col, lines in boxes:
        f.rect(x0, 24, 166, 96, C['white'], col, 0.9, 3.5)
        f.rect(x0, 24, 166, 20, col)
        f.text(x0 + 83, 38, title, C['white'], 7.4)
        for i, t in enumerate(lines):
            f.text(x0 + 83, 60 + i * 18, t, C['slate'] if i < 2 else C['ink'], 6.7)
    f.rect(0, 132, 522, 52, C['ambertint'], C['amber'], 0.75, 3.5)
    f.text(12, 150, u'“Exactly once” in the wild', C['amber'], 7.4, anchor='start')
    f.text(12, 165, u'Kafka transactions give exactly-once between Kafka topics. The moment an '
                    u'external system is involved —', C['ink'], 6.9, anchor='start')
    f.text(12, 177, u'a database, an email, a payment API — you are back to at-least-once plus '
                    u'an idempotent consumer.', C['ink'], 6.9, anchor='start')
    return f.render()
