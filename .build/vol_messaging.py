# -*- coding: utf-8 -*-
"""Volume: Messaging, Queues, Kafka & Event-Driven Architecture."""
from kit import (Book, cover, toc, qa, facts, table, cards, callout, formula, closing,
                 part, fig, kv, bullets, strip, codebox, codes, p, h2, h3, cd, STAR)
import figs_msg as F

THEME = dict(
    bgimg=(u'radial-gradient(52% 37% at 90% 7%, rgba(160,235,205,.26) 0%, '
           u'rgba(160,235,205,.06) 58%, rgba(160,235,205,0) 72%),'
           u'radial-gradient(34% 24% at 2% 99%, rgba(120,200,255,.26) 0%, '
           u'rgba(120,200,255,.06) 62%, rgba(120,200,255,0) 74%),'
           u'linear-gradient(157deg,#07171a 0%,#0a2426 20%,#0d3630 38%,#114838 56%,'
           u'#175c3f 72%,#1f7350 88%,#2c8f77 100%)'),
    hi=u'#8ff0c8', eye=u'#88d9bd', ledec=u'#c9e7dc', cardp=u'#bfded2', metac=u'#9cc3b6',
    barg=u'linear-gradient(90deg,#8ff0c8 0%,#63b8e8 100%)',
    acc=u'#0d7a5f', acctint=u'#e4f5ef', qn=u'#66d8b0',
)
EYEBROW = (u'S Y S T E M &nbsp;D E S I G N &nbsp; / &nbsp; '
           u'I N T E R V I E W &nbsp;P L A Y B O O K')

book = Book(u'The Complete Guide to Messaging & Streams', THEME)

# ═════════════════════════════════════════════════════════ front matter
book.raw(cover(
    THEME, EYEBROW,
    u'The Complete Guide<br>to <span class="hi">Messaging</span>',
    u'Queues, logs and event-driven design: partitions and consumer groups, delivery semantics, '
    u'the outbox pattern, idempotent consumers, dead-letter queues, backpressure and stream '
    u'processing.',
    [(u'Queue or log — decide it',
      u'Work to be executed once, or events other teams will read later. One question settles '
      u'it.'),
     (u'Kafka where it counts',
      u'Partitions, offsets, consumer groups, ISR and retention — the parts interviews probe.'),
     (u'Exactly-once, honestly',
      u'What at-least-once really means, the outbox, idempotency keys, and where duplicates '
      u'come from.'),
     (u'When it goes wrong',
      u'Consumer lag, poison messages, DLQs, rebalance storms, backpressure and replay.')],
    u'7 parts · 4 diagrams · 14 interview Q&amp;A · one-page cheat sheet',
    u'Revised August 2026'))

book.page(toc(
    u'C O N T E N T S',
    u'What’s inside',
    u'Read it front to back once. Part 3 (the outbox and idempotency) is the part that most '
    u'often separates a senior answer from a plausible one, and Part 6 is what on-call feels '
    u'like.',
    [(u'1', u'', u'Queues, logs and why async at all',
      u'What asynchrony actually buys, queue versus log, the four patterns, and the coupling '
      u'you trade away.'),
     (u'2', u'', u'Inside a log: Kafka mechanics',
      u'Topics, partitions and keys, offsets and consumer groups, replication and ISR, '
      u'retention, compaction, rebalancing.'),
     (u'3', u'', u'Getting events out of your database',
      u'Dual writes and why they break, the outbox pattern, CDC, ordering, and schema '
      u'evolution with a registry.'),
     (u'4', u'', u'Delivery semantics and idempotency',
      u'At most once, at least once, effectively once; idempotency keys, dedupe windows, and '
      u'Kafka transactions.'),
     (u'5', u'', u'Designing event flows',
      u'Event notification vs event-carried state vs event sourcing, choreography vs '
      u'orchestration, sagas, fan-out.'),
     (u'6', u'', u'Operating it',
      u'Consumer lag as the SLI, poison messages and DLQs, retries with backoff, backpressure, '
      u'rebalance storms, replay.'),
     (u'7', u'', u'The interview itself',
      u'How to introduce a queue without hand-waving, 14 asked-in-real-interviews Q&amp;A, and '
      u'the red flags to avoid.'),
     (STAR, u'star', u'One-page cheat sheet',
      u'The night-before page: the decision table, the numbers, messaging in eight facts.')],
    u'<b>Part of the HLD concept series.</b> Caching, databases, sharding and replication are '
    u'separate volumes; Redis Streams and Pub/Sub live in the Redis volume.'))

book.page(
    h2(u'How to use this guide', 'qhead'),
    cards(
        ('', u'Understand',
         [u'Each mechanism gets the plain-English version before the vocabulary, and the '
          u'failure it exists to survive.']),
        ('', u'Say out loud',
         [u'The grey “interview line” boxes are the sentences that show you have run one of '
          u'these systems.']),
        ('', u'Defend',
         [u'Async buys decoupling and costs you ordering, debuggability and exactly-once. Name '
          u'the cost.']),
    ),
    callout(u'THE WORDS, PRECISELY',
            [u'A <b>queue</b> distributes work: one consumer wins each message and it is then '
             u'gone. A <b>log</b> (Kafka, Kinesis, Pulsar) is an ordered, retained sequence '
             u'many independent consumers read at their own offsets. <b>Pub/Sub</b> is a '
             u'delivery style — fan-out to whoever is listening — and it can be built on '
             u'either. Using “queue” for all three is the most common vocabulary slip in these '
             u'interviews.'],
            'blue'),
    callout(u'THE ONE THING TO INTERNALISE',
            [u'Going asynchronous buys <b>availability and smoothing</b>: the producer stops '
             u'depending on the consumer being up or fast. It charges you in <b>ordering, '
             u'duplicates, debuggability and end-to-end latency you can no longer see in one '
             u'trace</b>. <b>Every message you add is a distributed system you now own.</b>'],
            'teal'),
)

# ═════════════════════════════════════════════════════════ Part 1
book.page(
    part(u'Queues, logs and why async at all', u'PART 1',
         u'“I’d put a queue there” is the most casually thrown phrase in system design '
         u'interviews. Earning the point means saying what it buys and what it breaks.'),
    h2(u'1.1 What asynchrony actually buys'),
    kv([(u'Decoupling in time',
         u'The producer completes even if the consumer is down, deploying or slow. This is the '
         u'availability argument and it is the main one.'),
        (u'Smoothing bursts',
         u'A 10× traffic spike becomes a longer queue instead of a wall of 503s — as long as '
         u'the work is genuinely deferrable.'),
        (u'Fan-out',
         u'One event, many consumers, none of which the producer needs to know about. This is '
         u'the argument for a log rather than a queue.'),
        (u'Slow work off the request path',
         u'Encoding video, sending email, building a thumbnail. The user gets 202 Accepted and '
         u'a way to check status.')]),
    h2(u'1.2 Queue or log?'),
    fig(u'1.1', F.fig_queue_vs_log(),
        u'A queue deletes what has been handled; a log remembers and lets each consumer track '
        u'its own position.'),
)

book.page(
    h2(u'1.3 The four things people actually build', 'qhead'),
    table([u'Pattern', u'Shape', u'Use it for'],
          [(u'Work queue',
            u'Producer → queue → competing workers, message deleted on ack',
            u'Thumbnails, emails, exports, retries — anything that must happen once'),
           (u'Publish/subscribe',
            u'One event delivered to every interested subscriber',
            u'Notifying other services that something happened, without knowing who they are'),
           (u'Event log / stream',
            u'Retained, ordered, replayable; each consumer holds an offset',
            u'Feeding search indexes, analytics, audit, ML features, and rebuilding state'),
           (u'Request/reply over a broker',
            u'Correlation id and a reply queue',
            u'Rare and usually a mistake — if you need an answer now, call the service')],
          [128.0, 200.0, 194.0]),
    h2(u'1.4 The costs, said out loud'),
    bullets([
        u'<b>Ordering is only per partition or per key</b> — a topic has no global order, and '
        u'assuming one is the classic bug.',
        u'<b>Duplicates are normal</b>, because at-least-once delivery is what durable brokers '
        u'give you. Consumers must be idempotent.',
        u'<b>Latency becomes invisible</b> unless you trace it: “the write returned in 20 ms” '
        u'says nothing about when the effect happened.',
        u'<b>Failure moves</b>: instead of a 500 the user sees nothing happen, which is harder '
        u'to notice and harder to explain.',
        u'<b>You now operate a broker</b>: partitions, retention, lag, rebalances and a '
        u'dead-letter policy are yours.']),
    callout(u'INTERVIEW LINE',
            [u'“I would put this behind a queue because the user does not need the result to '
             u'commit, and because the downstream system being slow should not fail the request. '
             u'The costs I am accepting are eventual consistency of the effect, duplicate '
             u'deliveries — so the consumer is idempotent — and the fact that I now need lag '
             u'monitoring and a dead-letter path.”'],
            'teal'),
)

# ═════════════════════════════════════════════════════════ Part 2
book.page(
    part(u'Inside a log: Kafka mechanics', u'PART 2',
         u'You do not need Kafka internals to design a system, and you do need enough of them '
         u'to answer “how does ordering work?” and “what happens when a consumer dies?”.'),
    h2(u'2.1 Topics, partitions, keys'),
    p(u'A topic is split into <b>partitions</b>, each an append-only file with monotonically '
      u'increasing <b>offsets</b>. The producer picks a partition — by hash of the message key, '
      u'or round-robin when there is no key. Two consequences carry most interview answers: '
      u'<b>order is guaranteed inside a partition only</b>, and <b>the partition count is your '
      u'maximum consumer parallelism</b>.'),
    fig(u'2.1', F.fig_partitions(),
        u'Partitions are the unit of ordering, of parallelism and of assignment. Everything '
        u'else about a consumer group follows from that.'),
)

book.page(
    h2(u'2.2 Consumer groups and offsets', 'qhead'),
    kv([(u'A group is a scaling unit',
         u'Each partition is assigned to exactly one consumer in the group, so adding '
         u'consumers past the partition count does nothing.'),
        (u'Offsets are committed, not deleted',
         u'The consumer records “I have processed up to 4,201”. Restarting resumes there — and '
         u'committing before processing is how you lose messages.'),
        (u'Several groups, same data',
         u'Search indexing, analytics and audit each read the whole topic independently. This '
         u'is the property a queue cannot give you.'),
        (u'Rebalancing',
         u'When a member joins or dies, partitions are reassigned — and processing pauses '
         u'briefly. Frequent rebalances are usually a too-short session timeout or a slow '
         u'poll loop.')]),
    h2(u'2.3 Durability: replication and ISR'),
    p(u'Each partition has a leader and followers. The <b>in-sync replica</b> set is those '
      u'followers that are caught up; a producer with <b>acks=all</b> waits for all of them, so '
      u'the write survives any single broker loss. <b>min.insync.replicas=2</b> with replication '
      u'factor 3 is the standard production setting: it tolerates one broker down and refuses '
      u'writes rather than accepting one it cannot keep.'),
    table([u'Setting', u'Meaning', u'When you would use it'],
          [(u'acks=0', u'Fire and forget', u'Never, for anything that matters'),
           (u'acks=1', u'Leader has it', u'High-throughput telemetry where a broker failure may '
                                         u'lose the tail'),
           (u'acks=all + min.insync=2', u'Leader plus a caught-up follower',
            u'The default for business events'),
           (u'unclean.leader.election=true', u'A lagging replica may become leader',
            u'Availability over durability — say it out loud if you enable it')],
          [148.0, 176.0, 198.0]),
    h2(u'2.4 Retention and compaction'),
    p(u'Time or size retention (“keep seven days”) is what makes replay possible — the single '
      u'most useful operational property of a log. <b>Log compaction</b> is the other mode: keep '
      u'the latest value per key forever, so the topic becomes a rebuildable snapshot of current '
      u'state. That is how a service bootstraps a cache or a materialised view from the '
      u'beginning of time without a database dump.'),
)

# ═════════════════════════════════════════════════════════ Part 3
book.page(
    part(u'Getting events out of your database', u'PART 3 · THE SENIOR SIGNAL',
         u'“Save the row and publish the event” looks like one line of code and is actually a '
         u'distributed transaction. How you answer this is the clearest read on whether you have '
         u'operated an event-driven system.'),
    h2(u'3.1 Why the dual write is broken'),
    p(u'Two independent systems, two writes, no atomicity: the database commit can succeed and '
      u'the publish fail (a row nobody hears about), or the publish can succeed and the '
      u'transaction roll back (an event for something that never happened). Retries do not fix '
      u'it, because the process can die between them.'),
    fig(u'3.1', F.fig_outbox(),
        u'The outbox: one transaction writes both the state and the intent to publish, and a '
        u'relay ships it afterwards.'),
)

book.page(
    h2(u'3.2 The two correct mechanisms', 'qhead'),
    cards(
        ('good', u'Transactional outbox',
         [u'Write the domain row and an <b>outbox</b> row in the same transaction. A relay '
          u'polls the outbox (or tails the log) and publishes, marking rows sent. Explicit, '
          u'testable, and it works on any database.']),
        ('good', u'Change data capture',
         [u'Read the database’s own replication log — Debezium on MySQL binlog or Postgres '
          u'logical decoding — and turn committed changes into events. Nothing to write in the '
          u'application, and the log is the source of truth by construction.']),
    ),
    table([u'Concern', u'Outbox', u'CDC'],
          [(u'What you publish', u'Exactly the event you designed',
            u'Row changes; you map them to events downstream'),
           (u'Coupling', u'Application owns the contract',
            u'Consumers see your schema — a real coupling risk'),
           (u'Ordering', u'Per aggregate, if you key it that way',
            u'Per table and transaction, in commit order'),
           (u'Operational load', u'A relay to run and monitor',
            u'A connector, slot/binlog retention, and schema-change handling'),
           (u'Failure mode', u'Outbox grows if the relay stalls',
            u'Replication slot grows and can threaten the database')],
          [116.0, 200.0, 206.0]),
    h2(u'3.3 Schema evolution'),
    p(u'Events outlive the code that wrote them, so the contract needs rules: add fields as '
      u'optional, never repurpose a field, version the schema, and register it '
      u'(Avro/Protobuf/JSON Schema in a registry) so producers cannot ship a breaking change. '
      u'The one-liner: <b>“consumers must tolerate unknown fields and missing optional ones — '
      u'that is what makes independent deploys possible.”</b>'),
)

# ═════════════════════════════════════════════════════════ Part 4
book.page(
    part(u'Delivery semantics and idempotency', u'PART 4',
         u'The three-word answers — at most once, at least once, exactly once — are easy. The '
         u'points come from knowing which one you actually get, and what you must build because '
         u'of it.'),
    h2(u'4.1 The three semantics'),
    fig(u'4.1', F.fig_delivery(),
        u'Ack before processing loses; ack after processing duplicates. There is no third '
        u'option without dedupe.'),
    h2(u'4.2 Making a consumer idempotent'),
    kv([(u'Natural idempotence',
         u'“Set status to SHIPPED” is safe to apply twice. Prefer designing operations this way '
         u'over adding machinery.'),
        (u'Dedupe table',
         u'Store the event id (or a hash) with a unique index and insert it in the same '
         u'transaction as the effect. A duplicate hits the constraint and is dropped.'),
        (u'Idempotency key at the API edge',
         u'The client sends a key; you store the first response against it and replay that '
         u'response for retries. This is the Stripe pattern.'),
        (u'Conditional writes',
         u'Version numbers, sequence numbers, or “update where status = PENDING” — the effect '
         u'applies once because the condition only matches once.')]),
)

book.page(
    h2(u'4.3 “Exactly once” — what is really on offer', 'qhead'),
    p(u'Kafka’s transactions give exactly-once <b>within Kafka</b>: a consume-transform-produce '
      u'loop can commit offsets and output atomically. The moment the effect leaves the broker — '
      u'a database row, an email, a card charge — you are back to at-least-once delivery with an '
      u'idempotent consumer. The honest phrase is <b>effectively once</b>, and using it is a '
      u'senior tell.'),
    callout(u'INTERVIEW LINE',
            [u'“I would design for at-least-once, because that is what a durable broker gives '
             u'me, and make the consumer idempotent: the event id goes into a dedupe table in '
             u'the same transaction as the effect, so a redelivery is a constraint violation and '
             u'not a double charge. If both ends were Kafka topics I could use transactions for '
             u'true exactly-once, but the moment I write to an external system that guarantee '
             u'ends.”'],
            'teal'),
    h2(u'4.4 Ordering, when you genuinely need it'),
    bullets([
        u'<b>Key by the entity</b> — order id, account id, conversation id — so all events for '
        u'that entity land in one partition and are processed in order.',
        u'<b>Sequence numbers</b> in the payload, so a consumer can detect a gap or an '
        u'out-of-order arrival rather than trusting the transport.',
        u'<b>Single-threaded per key</b> inside the consumer: parallelise across keys, never '
        u'within one.',
        u'<b>Accept that retries reorder.</b> A failed message sent to a retry topic will '
        u'arrive after later messages for the same key — which is exactly why the handler should '
        u'be commutative or version-checked.']),
    h2(u'4.5 The idempotency table, concretely'),
    codes(
        codebox(u'consumer, one transaction',
                u'BEGIN;\n'
                u'  INSERT INTO processed_events(event_id)\n'
                u'       VALUES ($1);          -- unique index\n'
                u'  UPDATE orders SET status = \'PAID\'\n'
                u'   WHERE id = $2 AND status = \'PENDING\';\n'
                u'COMMIT;',
                u'A duplicate delivery fails the insert, the transaction aborts, and nothing '
                u'happens twice. The condition on status makes it safe even if the row was '
                u'already advanced.'),
        codebox(u'what to keep, and for how long',
                u'event_id      uuid primary key\n'
                u'processed_at  timestamptz\n'
                u'-- retention: longer than the broker’s\n'
                u'-- redelivery window, then partition\n'
                u'-- by day and drop old partitions',
                u'Bound the table or it becomes the next scaling problem. A dedupe window '
                u'wider than the broker’s retention is wasted; narrower is a hole.'),
    ),
)

# ═════════════════════════════════════════════════════════ Part 5
book.page(
    part(u'Designing event flows', u'PART 5',
         u'Once you have a broker, the design question becomes what goes in the message and who '
         u'is in charge — and those two choices determine how coupled your services really are.'),
    h2(u'5.1 What goes in the event'),
    table([u'Style', u'Payload', u'Trade-off'],
          [(u'Event notification', u'“Order 1183 changed” plus an id',
            u'Tiny and loosely coupled; every consumer must call back for details, so you have '
            u'moved the load rather than removed it'),
           (u'Event-carried state', u'The fields consumers need, denormalised',
            u'No callback, so consumers work while the producer is down; the schema is now a '
            u'contract and payloads get big'),
           (u'Event sourcing', u'Every state change, as the system of record',
            u'Perfect audit and time travel; you now own snapshots, replay performance and '
            u'schema versioning forever')],
          [128.0, 176.0, 218.0]),
    h2(u'5.2 Who is in charge: choreography or orchestration'),
    cards(
        ('', u'Choreography',
         [u'Each service reacts to events and emits its own. No central brain, easy to extend '
          u'— and no single place to see “where is order 1183?”, which makes debugging a '
          u'log-joining exercise.']),
        ('', u'Orchestration',
         [u'A saga orchestrator owns the state machine and calls each step. One place to see '
          u'progress, retry and compensate; that component is now critical and must itself be '
          u'durable.']),
    ),
    p(u'The rule of thumb worth saying: <b>choreography for notifications and fan-out, '
      u'orchestration for business transactions with compensation</b> — anything where a partial '
      u'failure needs a defined reversal.'),
    h2(u'5.3 Sagas in three sentences'),
    p(u'A saga is a sequence of local transactions where each step has a compensating action, '
      u'used because a transaction cannot span services. Every step needs an idempotency key, '
      u'the state machine must be persisted so it can resume after a crash, and compensation is '
      u'business logic — “refund the payment”, not “roll back the transaction”. Interviewers '
      u'listen for that third sentence.'),
)

# ═════════════════════════════════════════════════════════ Part 6
book.page(
    part(u'Operating it', u'PART 6',
         u'Everything in this part is what being on call for an event-driven system feels like. '
         u'Volunteering two of these is worth more than naming three brokers.'),
    h2(u'6.1 Consumer lag is the SLI'),
    p(u'Lag — the difference between the newest offset and the committed one — is the number '
      u'that tells you whether the system is keeping up, and it is the one to alert on. Watch '
      u'the <i>derivative</i> too: flat lag at 50,000 is a system in balance, while steadily '
      u'growing lag is a system that will not recover without more consumers or fewer events. '
      u'Alert on lag in <b>time</b> (“more than two minutes behind”), because that is what the '
      u'product cares about.'),
    h2(u'6.2 Poison messages and dead letters'),
    strip([(u'1', u'Retry in place', u'A few attempts with exponential backoff and jitter'),
           (u'2', u'Retry topic', u'Move it aside so the partition keeps flowing'),
           (u'3', u'Dead letter', u'Park it with the error and full context'),
           (u'4', u'Alert & replay', u'Someone looks, fixes, and replays from the DLQ')]),
    p(u'The failure to name: <b>a poison message with in-place infinite retry blocks its whole '
      u'partition</b>, so one malformed event stops every key that hashes to it. That is the '
      u'outage a DLQ prevents, and “what happens to a message you can never process?” is a '
      u'standard follow-up.'),
    h2(u'6.3 Backpressure'),
    kv([(u'The broker absorbs, until it does not',
         u'Retention is finite. A consumer down longer than retention loses data — a real '
         u'incident, not a theoretical one.'),
        (u'Bound everything',
         u'Prefetch limits, in-flight caps, and a bounded internal work queue. Unbounded '
         u'buffering converts a slow consumer into an OOM.'),
        (u'Shed or degrade',
         u'Drop low-value events (telemetry sampling) rather than falling behind on the ones '
         u'that matter. Separate topics make that possible.'),
        (u'Scale the unit that matters',
         u'More consumers only help up to the partition count — so partition count is a '
         u'capacity decision made in advance.')]),
    h2(u'6.4 Replay, the superpower and the footgun'),
    p(u'Replaying a retained log rebuilds a search index, backfills a new service, or recovers '
      u'from a bad deploy — and it re-emits side effects unless consumers are idempotent and '
      u'external calls are guarded. Design for it explicitly: a replay flag, a dedupe window '
      u'wide enough to cover the replay, and a way to throttle so the replay does not take the '
      u'database down.'),
)

# ═════════════════════════════════════════════════════════ Part 7
book.page(
    part(u'The interview itself', u'PART 7',
         u'The queue is usually the easiest box to draw and the easiest place to lose points. '
         u'These four beats keep it credible.'),
    h2(u'7.1 The four-beat answer'),
    strip([(u'1', u'Why async', u'The user does not need the result to commit'),
           (u'2', u'Queue or log', u'Will another consumer need these events later?'),
           (u'3', u'Semantics', u'At-least-once, keyed by entity, idempotent consumer'),
           (u'4', u'Failure', u'Retries with backoff, a DLQ, and lag alerting')]),
    h2(u'7.2 The five sentences that earn points'),
    bullets([
        u'“Ordering is per partition, so I key by order id and process one key at a time.”',
        u'“I would not dual-write; the event goes in an outbox row in the same transaction, and '
        u'a relay publishes it.”',
        u'“At-least-once is what I get, so the consumer dedupes on event id inside the same '
        u'transaction as the effect.”',
        u'“A poison message with infinite retry blocks the partition, so failures go to a retry '
        u'topic and then a DLQ.”',
        u'“Consumer lag in seconds is the SLI, and partition count is my parallelism ceiling.”']),
    callout(u'INTERVIEW LINE',
            [u'“I would use a log rather than a queue here, because the notification service is '
             u'not the only future consumer — search indexing, analytics and audit will all want '
             u'the same events, and a log lets them read independently and replay. The costs are '
             u'retention capacity and the fact that consumers must be idempotent, which they '
             u'have to be anyway.”'],
            'teal'),
)

book.page(
    h2(u'7.3 Fourteen questions with model answers', 'qhead'),
    qa(u'1', u'Queue or Kafka — how do you choose?',
       [u'One question: will anyone other than this consumer, now or later, need these events? '
        u'If yes, a log — retained, ordered per partition, with independent offsets — so search, '
        u'analytics and audit can each read the whole stream and replay it. If it is work to be '
        u'executed exactly once by whichever worker is free, a queue is simpler and the '
        u'operational surface is smaller.']),
    qa(u'2', u'How does Kafka guarantee ordering?',
       [u'Only inside a partition. A partition is an append-only sequence with monotonic '
        u'offsets, and one consumer per group owns it — so events with the same key, hashed to '
        u'the same partition, are processed in order. A topic has no global order, so if I need '
        u'per-entity ordering I key by that entity, and if I need global ordering I have a '
        u'single-partition topic and no parallelism.']),
    qa(u'3', u'Save an order and publish an event. How do you do it atomically?',
       [u'Not with a dual write — the commit can succeed and the publish fail, or the reverse. '
        u'I write the order and an outbox row in the same transaction, and a relay reads the '
        u'outbox and publishes, marking rows sent; or I skip the outbox and use CDC on the '
        u'database log. Either way the event cannot exist without the row. It is still '
        u'at-least-once, so consumers dedupe.']),
    qa(u'4', u'Is exactly-once delivery possible?',
       [u'Not end-to-end, in general. Kafka transactions give exactly-once between Kafka topics '
        u'by committing offsets and output atomically. As soon as the effect is external — a '
        u'row, an email, a charge — you get at-least-once delivery plus idempotent processing, '
        u'which is what people mean when they say effectively once. The mechanism is a dedupe '
        u'key stored transactionally with the effect.']),
)

book.page(
    qa(u'5', u'A consumer keeps crashing on one message. What happens and what do you do?',
       [u'With in-place retry it blocks the partition: every message behind it stops, including '
        u'other keys that hash there. So: a few retries with exponential backoff and jitter, '
        u'then move the message to a retry topic so the main partition flows, then to a '
        u'dead-letter queue with the error and enough context to reproduce. Alert on DLQ depth, '
        u'and make replay from the DLQ a normal operation rather than a script someone writes '
        u'during an incident.']),
    qa(u'6', u'How do you scale consumers?',
       [u'Add consumers up to the partition count and no further — partitions are the unit of '
        u'assignment, so extra consumers idle. That means partition count is a capacity decision '
        u'you make in advance, with headroom, because increasing it later changes key-to-'
        u'partition mapping and therefore breaks per-key ordering for in-flight data. Inside a '
        u'consumer, parallelise across keys, never within a key.']),
    qa(u'7', u'What is consumer lag and what do you alert on?',
       [u'The gap between the newest offset and the one the group has committed. I alert on lag '
        u'expressed in time — “more than two minutes behind” — because that is what the product '
        u'notices, and I watch whether it is flat or growing: flat lag is balance, growing lag is '
        u'a system that will not recover on its own. I would also alert on a group that stops '
        u'committing at all, which flat lag can hide.']),
    qa(u'8', u'The consumer was down for six hours. What now?',
       [u'First check retention: if the topic keeps seven days I have simply got a backlog, and '
        u'the questions are how fast I can drain it and whether processing it late is harmful. I '
        u'would scale consumers to the partition ceiling, consider a temporary separate group '
        u'for the backlog, and throttle so the downstream database survives. If the outage '
        u'exceeded retention, data is genuinely gone and I need a backfill from the source of '
        u'truth — which is the argument for retention longer than your worst realistic outage.']),
    qa(u'9', u'Event notification or event-carried state?',
       [u'Notification — an id and a change type — keeps payloads small and coupling low, but '
        u'every consumer calls back for details, so I have moved load rather than removed it, '
        u'and consumers cannot work while the producer is down. Carried state makes consumers '
        u'independent at the price of a schema contract and bigger messages. I would carry state '
        u'for cross-team consumption and notify inside a team that owns both sides.']),
)

book.page(
    qa(u'10', u'Design the notification fan-out for a social app.',
       [u'Producers publish one <b>PostCreated</b> event to a log, keyed by author. A fan-out '
        u'consumer group expands it to followers and writes per-channel jobs to separate topics '
        u'— push, email, in-app — because their rate limits and failure modes differ. Each '
        u'channel worker is idempotent on (user, post, channel), retries with backoff, and '
        u'dead-letters after a bounded number of attempts. Celebrity authors get the hybrid '
        u'treatment: no fan-out on write, merged on read.']),
    qa(u'11', u'Do you need a broker, or would a database table do?',
       [u'A table with <b>SELECT … FOR UPDATE SKIP LOCKED</b> is a genuinely good queue at low '
        u'rates: transactional with your data, no new infrastructure, easy to inspect. It stops '
        u'being good at high throughput, with many consumers, when you need fan-out or replay, '
        u'or when the dead tuples start hurting. Saying this out loud is a strong signal — '
        u'reaching for Kafka to send a thousand emails a day is over-engineering.']),
    qa(u'12', u'How do you evolve an event schema without breaking consumers?',
       [u'Additive changes only: new fields optional, never repurpose or remove a field in '
        u'place, and version the event type when the meaning changes. Enforce it with a schema '
        u'registry and compatibility checks in CI, so a producer physically cannot ship a '
        u'breaking change. Consumers ignore unknown fields, which is what lets both sides deploy '
        u'independently.']),
    qa(u'13', u'When does a retry make things worse?',
       [u'When it is immediate, unbounded, or synchronised. Immediate retries hit a struggling '
        u'dependency hardest; unbounded retries turn a transient error into an infinite loop; '
        u'and retries across a whole fleet at the same interval produce a thundering herd. So: '
        u'exponential backoff with jitter, a retry budget or circuit breaker, and idempotency so '
        u'the retry is safe at all. Also worth naming: retries reorder events for a key.']),
    qa(u'14', u'What would make you not use async here?',
       [u'When the user needs the answer to proceed — a payment authorisation, a login, a seat '
        u'reservation. Making that asynchronous does not remove the wait, it just hides it and '
        u'adds a status-polling problem. Also when the operation is genuinely simple and '
        u'synchronous is easier to reason about: a queue adds a broker, duplicates, ordering '
        u'rules and lag monitoring, and it should earn that.']),
)

book.page(
    h2(u'7.4 Red flags interviewers listen for', 'qhead'),
    table([u'Saying this', u'Says this about you'],
          [(u'“Kafka guarantees ordering”',
            u'Only per partition — and that distinction is the whole design'),
           (u'“Exactly-once, so no dedupe needed”',
            u'Has not read the small print at the system boundary'),
           (u'Dual-writing DB and broker in application code',
            u'The two will disagree, and nothing will notice'),
           (u'No answer for a message that always fails',
            u'One poison message can stall a partition'),
           (u'Unbounded in-place retries',
            u'Turns a transient error into a permanent outage'),
           (u'More consumers than partitions',
            u'The extras idle; parallelism is capped by partitions'),
           (u'No retention or lag numbers',
            u'Has not operated a broker'),
           (u'“We’ll use a queue” for a synchronous user need',
            u'Hides the wait instead of removing it'),
           (u'Event payload = the whole database row, versioned by nothing',
            u'Consumers break on the next migration'),
           (u'Kafka for a thousand jobs a day',
            u'Over-engineering; a table with SKIP LOCKED was the answer')],
          [232.0, 290.0]),
    h2(u'7.5 Real systems worth name-dropping'),
    cards(
        ('', u'LinkedIn → Kafka',
         [u'Jay Kreps’ <i>The Log</i> is still the clearest argument for a replayable log as '
          u'the backbone of data integration. Cite it for “why a log, not a queue”.']),
        ('', u'Debezium & the outbox',
         [u'The industry-standard CDC connector, and the pattern write-up that made “outbox” '
          u'common vocabulary. Cite it for atomic state-plus-event.']),
    ),
    cards(
        ('', u'Stripe idempotency keys',
         [u'A public API contract built entirely on “retry safely”. The canonical reference for '
          u'idempotency at the edge rather than deep in a consumer.']),
        ('', u'Uber & DoorDash event platforms',
         [u'Public write-ups on Kafka at scale: tiered storage, consumer-lag SLOs, DLQ tooling. '
          u'Good for showing you have read operational accounts, not just docs.']),
    ),
)

# ---- cheat sheet ----
book.page(
    u'<span class="chip rev">R E V I S I O N</span>'
    u'<h1 class="big">One-page cheat sheet</h1>'
    + p(u'The night-before page. If you remember only this, you can still hold a good '
        u'conversation about async.', 'sub')
    + u'<hr class="thin">',
    h2(u'The numbers'),
    formula(u'one Kafka broker ~ 100 MB/s  ·  partitions = your consumer parallelism  ·  '
            u'retention beyond your worst outage',
            u'Alert on lag in time, not messages. Keep 30–40% partition headroom, because '
            u'repartitioning later breaks per-key ordering. A dedupe window must be wider than '
            u'the broker’s redelivery window.'),
    h2(u'The decisions'),
    table([u'Question', u'Default answer'],
          [(u'Async at all?', u'Only if the user does not need the result to commit'),
           (u'Queue or log?', u'Log if anyone else will ever want these events'),
           (u'Partition key?', u'The entity whose order matters: order id, account, '
                               u'conversation'),
           (u'Delivery?', u'At-least-once, with an idempotent consumer'),
           (u'Dedupe?', u'Event id in a unique index, inserted in the effect’s transaction'),
           (u'DB + event?', u'Outbox in one transaction, or CDC. Never a dual write'),
           (u'Retries?', u'Bounded, exponential, jittered → retry topic → DLQ'),
           (u'Payload?', u'Carry state across teams; notify inside one'),
           (u'Saga?', u'Orchestration for business transactions, choreography for fan-out'),
           (u'Alerting?', u'Consumer lag in seconds, DLQ depth, and commit staleness')],
          [148.0, 374.0]),
)

book.page(
    h2(u'Messaging in eight facts', 'qhead'),
    facts([
        (u'Async buys availability',
         u'The producer stops depending on the consumer being up. That is the whole argument.'),
        (u'Ordering is per partition',
         u'Key by the entity that needs order, and process one key at a time.'),
        (u'Partitions cap parallelism',
         u'More consumers than partitions do nothing. Decide the count with headroom.'),
        (u'At-least-once is what you get',
         u'So idempotency is not optional. Dedupe transactionally with the effect.'),
        (u'Dual writes always diverge',
         u'Outbox or CDC. One transaction must cover the state and the intent.'),
        (u'A poison message blocks a partition',
         u'Bounded retries, then a retry topic, then a DLQ someone actually watches.'),
        (u'Lag is the SLI',
         u'In seconds. Flat lag is balance; growing lag never recovers by itself.'),
        (u'Retention is a data-loss boundary',
         u'A consumer down longer than retention has lost data. Size it for your worst '
         u'outage.'),
    ], tone='acc'),
    h2(u'The failure modes'),
    table([u'Name', u'Mechanism', u'Primary fix'],
          [(u'Poison message', u'A message that always fails, retried in place',
            u'Bounded retry → retry topic → DLQ'),
           (u'Duplicate effects', u'Redelivery after a partial success',
            u'Idempotency key in the same transaction as the effect'),
           (u'Lost event', u'Dual write, or offset committed before processing',
            u'Outbox/CDC; commit offsets only after the effect'),
           (u'Rebalance storm', u'Slow poll loop or short session timeout',
            u'Tune timeouts, shorten processing, use cooperative rebalancing'),
           (u'Backlog past retention', u'Consumer down longer than the retention window',
            u'Longer retention, lag alerts, and a backfill path from the source'),
           (u'Reordering by retry', u'A retried message arrives after later ones',
            u'Version checks or commutative handlers; never assume transport order')],
          [124.0, 194.0, 204.0]),
)

book.page(
    closing(u'IF YOU SAY NOTHING ELSE, SAY THIS',
            u'“I would go asynchronous where the user does not need the result to commit, and I '
            u'would use a log rather than a queue whenever a second consumer will ever want the '
            u'same events. Ordering is per partition, so I key by the entity that needs it. '
            u'Delivery is at-least-once, so the consumer dedupes on event id in the same '
            u'transaction as the effect, and the event itself comes out of an outbox rather than '
            u'a dual write. Failures retry with backoff and end in a dead-letter queue, and '
            u'consumer lag in seconds is the number I would put on a dashboard and alert on.”'),
    p(u'<b>Sources &amp; further reading</b> — Jay Kreps, <i>The Log: What every software '
      u'engineer should know about real-time data’s unifying abstraction</i>; the Apache Kafka '
      u'documentation on partitions, consumer groups, ISR, transactions and log compaction; '
      u'Debezium documentation and the transactional-outbox pattern write-up; Chris Richardson’s '
      u'microservices patterns (saga, outbox, CQRS); Martin Kleppmann, <i>Designing '
      u'Data-Intensive Applications</i>, chapters 11 and 12; Stripe’s API documentation on '
      u'idempotency keys; Confluent’s articles on exactly-once semantics; AWS documentation on '
      u'SQS visibility timeouts, FIFO queues and DLQs; Uber and DoorDash engineering blogs on '
      u'operating Kafka at scale.', 'src'),
)

book.write('v_messaging.html')
