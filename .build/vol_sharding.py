# -*- coding: utf-8 -*-
"""Volume: Sharding, Partitioning & Consistent Hashing."""
from kit import (Book, cover, toc, qa, facts, table, cards, callout, formula, closing,
                 part, fig, kv, bullets, strip, codebox, codes, p, h2, h3, cd, STAR)
import figs_shard as F

THEME = dict(
    bgimg=(u'radial-gradient(52% 37% at 90% 7%, rgba(150,225,245,.28) 0%, '
           u'rgba(150,225,245,.07) 58%, rgba(150,225,245,0) 72%),'
           u'radial-gradient(34% 24% at 2% 99%, rgba(120,215,225,.30) 0%, '
           u'rgba(120,215,225,.06) 62%, rgba(120,215,225,0) 74%),'
           u'linear-gradient(157deg,#06141f 0%,#08202f 20%,#0b3147 38%,#0e4360 56%,'
           u'#12587a 72%,#186f91 88%,#2790a8 100%)'),
    hi=u'#8fe3f5', eye=u'#89cfe4', ledec=u'#c9e2ec', cardp=u'#bfd8e4', metac=u'#9dbccb',
    barg=u'linear-gradient(90deg,#8fe3f5 0%,#5ec9a8 100%)',
    acc=u'#0f6f92', acctint=u'#e6f2f8', qn=u'#6fc7e0',
)
EYEBROW = (u'S Y S T E M &nbsp;D E S I G N &nbsp; / &nbsp; '
           u'I N T E R V I E W &nbsp;P L A Y B O O K')

book = Book(u'The Complete Guide to Sharding', THEME)

# ═════════════════════════════════════════════════════════ front matter
book.raw(cover(
    THEME, EYEBROW,
    u'The Complete Guide<br>to <span class="hi">Sharding</span>',
    u'When to split a data set across machines, how to choose the key, how consistent hashing '
    u'actually works, how to reshard a live system — and everything you permanently give up the '
    u'moment you do.',
    [(u'Earn it before you do it',
      u'The five cheaper moves first, and the signals that genuinely force a split.'),
     (u'The shard key is the design',
      u'Hash, range, directory, geo — cardinality, skew and whether your queries survive.'),
     (u'Consistent hashing, properly',
      u'The ring, virtual nodes, replica placement, and why modulo hashing is an outage.'),
     (u'Resharding without downtime',
      u'Dual-write, backfill, verify, flip — plus logical buckets so you never do it again.')],
    u'7 parts · 3 diagrams · 14 interview Q&amp;A · one-page cheat sheet',
    u'Revised August 2026'))

book.page(toc(
    u'C O N T E N T S',
    u'What’s inside',
    u'Read it front to back once. Part 2 (the key) and Part 6 (what you lost) are where '
    u'interviews are won; Part 5 is the one candidates have never thought about.',
    [(u'1', u'', u'Before you shard',
      u'The five cheaper moves, the three signals that actually force a split, and what '
      u'sharding permanently costs you.'),
     (u'2', u'', u'Choosing the shard key',
      u'Hash, range, directory and geo partitioning; cardinality, skew, query alignment, '
      u'tenants and the celebrity problem.'),
     (u'3', u'', u'Consistent hashing',
      u'The ring, virtual nodes, replica placement, rebalancing maths, and the alternatives '
      u'worth naming.'),
     (u'4', u'', u'Routing and topology',
      u'Client-side vs proxy vs coordinator, slot maps, redirects, the metadata service, and '
      u'connection fan-out.'),
     (u'5', u'', u'Resharding a live system',
      u'Split and merge, dual-write, backfill, verification, cutover — and the logical-bucket '
      u'trick that makes it routine.'),
     (u'6', u'', u'Living with shards',
      u'Cross-shard queries and transactions, secondary indexes, uniqueness, aggregation, hot '
      u'shards, noisy tenants, backups.'),
     (u'7', u'', u'The interview itself',
      u'How to answer a sharding question, 14 asked-in-real-interviews Q&amp;A, and the red '
      u'flags to avoid.'),
     (STAR, u'star', u'One-page cheat sheet',
      u'The night-before page: the decision table, the numbers, sharding in eight facts.')],
    u'<b>Part of the HLD concept series.</b> Replication and quorums, caching, and the '
    u'messaging layer are separate volumes; this one is only about splitting the data.'))

book.page(
    h2(u'How to use this guide', 'qhead'),
    cards(
        ('', u'Understand',
         [u'Every section opens in plain English before any jargon. If a sentence needs a '
          u'diagram, there is one.']),
        ('', u'Say out loud',
         [u'The grey “interview line” boxes are the exact sentences that earn the point.']),
        ('', u'Defend',
         [u'Every choice lists its cost. Interviewers score the trade-off, not the choice.']),
    ),
    callout(u'PARTITIONING VS SHARDING — THE WORDS',
            [u'<b>Partitioning</b> splits one table inside one database: the engine prunes '
             u'partitions per query, retention becomes a <b>DROP</b>, and you still have one '
             u'write primary. <b>Sharding</b> splits the data set across independent databases '
             u'with routing above them: you gain write capacity and you lose cross-shard joins, '
             u'transactions and easy uniqueness. Interviewers use the words loosely; you should '
             u'not.'],
            'blue'),
    callout(u'THE ONE THING TO INTERNALISE',
            [u'Sharding buys exactly one thing — <b>capacity beyond one machine</b> — and it '
             u'charges you in every query that does not name the shard key. So the design work '
             u'is not the split; it is choosing a key that keeps almost every request on one '
             u'shard, and knowing what to do about the requests that cannot.'],
            'teal'),
)

# ═════════════════════════════════════════════════════════ Part 1
book.page(
    part(u'Before you shard', u'PART 1',
         u'Reaching for shards early is the most common way to fail a system design interview '
         u'while sounding advanced. The senior move is to name the cheaper options first, then '
         u'the number that rules them out.'),
    h2(u'1.1 The ladder, in order'),
    strip([(u'1', u'Index & query', u'Most “scale” problems are one missing composite index'),
           (u'2', u'Cache', u'Read-heavy? A cache removes the load you were about to shard for'),
           (u'3', u'Replicas', u'Reads scale out. Writes do not — say this explicitly'),
           (u'4', u'Bigger box', u'Vertical scaling is boring, instant and often enough'),
           (u'5', u'Partition', u'One node, many partitions: pruning and cheap retention')]),
    p(u'Only when all five are exhausted does the sixth step — splitting across machines — earn '
      u'its complexity. Saying that ladder out loud takes fifteen seconds and immediately '
      u'separates you from the candidate whose first move is “I’ll shard by user id”.'),
    h2(u'1.2 The three signals that actually force a shard'),
    kv([(u'Write throughput',
         u'One primary tops out around 5–10k writes/s. If the workload needs 50k, no cache or '
         u'replica helps — writes must be split.'),
        (u'Working set vs RAM',
         u'When the hot data no longer fits in memory, every read becomes disk I/O and p99 '
         u'falls off a cliff.'),
        (u'Operational size',
         u'A 20 TB table is not just slow: backups take a day, restores take longer, and '
         u'schema changes stop being feasible.'),
        (u'Blast radius / residency',
         u'One tenant must not be able to take down the rest, and EU data may have to stay in '
         u'the EU. Both are sharding arguments that have nothing to do with load.')]),
    callout(u'INTERVIEW LINE',
            [u'“Before I shard I would check whether one primary can carry this: the estimate '
             u'says roughly 8,000 writes a second at peak, which is right at the edge, so yes — '
             u'this one needs splitting. If it were 800 I would use a cache, read replicas and a '
             u'bigger box, and I would say so rather than sharding for the sake of it.”'],
            'teal'),
)

book.page(
    h2(u'1.3 What sharding permanently costs you', 'qhead'),
    table([u'What you lose', u'Why', u'What you do instead'],
          [(u'Cross-shard joins',
            u'The rows live in different databases; no engine can join them for you',
            u'Denormalise so the read is one shard, or join in the service layer for small '
            u'result sets'),
           (u'Single-node transactions',
            u'ACID stops at the shard boundary',
            u'Keep the transaction inside one shard by design; across shards use a saga with '
            u'compensations'),
           (u'Global uniqueness',
            u'A unique index is per shard, so two shards can both accept “alice@example.com”',
            u'A separate claim table or a uniqueness service, keyed so the claim lands on one '
            u'shard'),
           (u'Cheap aggregates',
            u'COUNT(*) now means scatter-gather over every shard',
            u'Maintain counters as you write, or answer from a warehouse and say how stale it '
            u'is'),
           (u'Simple operations',
            u'Backups, migrations, upgrades and on-call all multiply by the shard count',
            u'Automate per-shard operations from day one; never treat shard #7 as special'),
           (u'ORDER BY / LIMIT across shards',
            u'The global top-N needs N from every shard, merged',
            u'Fan out with a per-shard limit and merge, or precompute the ranking')],
          [126.0, 190.0, 206.0]),
    p(u'Every one of those lines is an interview answer waiting to be asked. Volunteering two of '
      u'them, unprompted, is what a senior candidate sounds like.', 'note'),
)

# ═════════════════════════════════════════════════════════ Part 2
book.page(
    part(u'Choosing the shard key', u'PART 2 · THE WHOLE DESIGN',
         u'Everything else in this volume is mechanics. The shard key is the decision, and it is '
         u'almost impossible to change later without a migration — which is why interviewers '
         u'spend most of their time here.'),
    h2(u'2.1 Four ways to partition, and what each one does to you'),
    table([u'Strategy', u'Good at', u'Fails at'],
          [(u'Hash of the key',
            u'Even distribution, no hotspots, trivial routing',
            u'Range queries are gone — “orders between two dates” hits every shard'),
           (u'Range of the key',
            u'Range scans and time windows stay on one shard; retention is a shard drop',
            u'Monotonic keys put every new write on the last shard — the classic hotspot'),
           (u'Directory / lookup',
            u'Maximum flexibility: move any key anywhere, rebalance per tenant',
            u'The lookup service is now on every request path — cache it, replicate it, or it '
            u'is your SPOF'),
           (u'Geo / tenant',
            u'Locality, data residency, and blast-radius isolation',
            u'Load is uneven by definition, and a big tenant needs its own treatment')],
          [116.0, 196.0, 210.0]),
    fig(u'2.1', F.fig_keys(),
        u'Four shards, three keys, three futures. The distribution is a property of the key, '
        u'not of the database.'),
)

book.page(
    h2(u'2.2 The four tests a candidate key must pass', 'qhead'),
    kv([(u'1 · High cardinality',
         u'Enough distinct values to spread over your shard count and the next one. '
         u'“Country” has 200 values and half your traffic in three of them.'),
        (u'2 · Even distribution',
         u'No value carries a disproportionate share — and check the tail, not the mean. '
         u'One key at 5% of traffic is a hot shard.'),
        (u'3 · Query alignment',
         u'Your top three queries must be answerable with the key in hand, or they become '
         u'scatter-gather.'),
        (u'4 · Stability',
         u'The value must not change. Sharding on something mutable means moving rows '
         u'between shards on update.')]),
    h2(u'2.3 The keys that keep appearing in interviews'),
    table([u'System', u'Key', u'Why it works'],
          [(u'Chat / messaging', u'hash(conversation_id)',
            u'Every read is “this conversation’s recent messages” — one shard, ordered'),
           (u'Social feed', u'hash(user_id)',
            u'The timeline belongs to one user; fan-out writes go to many shards, reads to one'),
           (u'E-commerce orders', u'hash(customer_id)',
            u'A customer’s orders and their history stay together; reporting goes to the '
            u'warehouse'),
           (u'Metrics / logs', u'range(time) + hash(series)',
            u'Composite: recent data on one set of shards for retention, series hashing for '
            u'spread'),
           (u'Multi-tenant SaaS', u'tenant_id (directory)',
            u'Isolation, residency and per-tenant migration; big tenants get dedicated shards'),
           (u'Ride-hailing / maps', u'geohash / S2 cell',
            u'Proximity queries need spatial locality, so the key <i>is</i> the geography')],
          [124.0, 156.0, 242.0]),
)

book.page(
    h2(u'2.4 The hot shard, and the four honest fixes', 'qhead'),
    p(u'One key, one shard. That is the whole mechanism behind every celebrity problem: adding '
      u'shards cannot help, because the traffic is not spread across keys — it is one key. Say '
      u'the mechanism first, then the fixes in order of how much they cost you.'),
    cards(
        ('good', u'Reads: cache in front',
         [u'A short-TTL in-process cache absorbs a viral key: 200 servers make 200 requests per '
          u'TTL instead of a million per second. Cheapest fix, and it changes nothing about the '
          u'data model.']),
        ('good', u'Writes: salt the key',
         [u'Write to <b>key#0 … key#15</b> at random and have a worker fold them into a total. '
          u'The write spreads over 16 shards; reads either read the total or sum 16 values.']),
    ),
    cards(
        ('', u'Give it its own shard',
         [u'For a known-large tenant, dedicate a shard (or a whole cluster). The directory '
          u'strategy exists precisely so you can do this without changing anything else.']),
        ('bad', u'Composite key',
         [u'Add a second dimension to the key — <b>(video_id, hour)</b> or '
          u'<b>(sensor_id, day)</b> — so a hot entity is spread across many partitions. Cheap, '
          u'but it changes every query you have already written.']),
    ),
    callout(u'THE SENTENCE THAT SCORES',
            [u'“Adding shards does not fix a hot key, because a single key hashes to a single '
             u'shard. I would absorb the reads in a local cache with a few seconds of TTL, and '
             u'if the writes are hot I would split the key into sixteen sub-keys and fold them '
             u'together asynchronously — and I would make sure those sub-keys land on '
             u'<i>different</i> shards, which means no shared hash tag or prefix.”'],
            'purple'),
)

# ═════════════════════════════════════════════════════════ Part 3
book.page(
    part(u'Consistent hashing', u'PART 3',
         u'The algorithm interviewers ask you to explain by name. It answers one question: how '
         u'do I add or remove a node without moving all the data?'),
    h2(u'3.1 The problem with the obvious answer'),
    p(u'<b>hash(key) % N</b> is even, fast and catastrophic to change: when N goes from 4 to 5, '
      u'about 80% of keys map somewhere new. For a cache that is a stampede against your '
      u'database; for a data store it is a full reshuffle of every byte you own.'),
    h2(u'3.2 The ring, and virtual nodes'),
    p(u'Hash both the keys <i>and</i> the nodes into the same space, arrange it as a ring, and '
      u'a key belongs to the first node clockwise from it. Adding a node claims one arc, so only '
      u'the keys in that arc move — roughly 1/N of them. Virtual nodes (each physical node '
      u'appearing at many points) fix two remaining problems: uneven arc sizes, and the fact '
      u'that without them a new node only relieves its single clockwise neighbour.'),
    fig(u'3.1', F.fig_ring(),
        u'One ring, four nodes, three virtual nodes each. Replication is “the next R distinct '
        u'physical nodes clockwise”, which is also how Dynamo-style stores place replicas.'),
)

book.page(
    h2(u'3.3 The numbers to quote', 'qhead'),
    formula(u'keys moved when adding one node = about 1 / (N + 1)',
            u'Going from 9 to 10 nodes moves about 10% of the keys, not 90%. With 100–256 '
            u'virtual nodes per physical node, the load spread stays within a few percent of '
            u'even — that is the number to say when asked “how many vnodes?”.'),
    h2(u'3.4 Where you have already met it'),
    kv([(u'Redis Cluster', u'16,384 fixed hash slots rather than a ring — the same idea with '
                           u'integer arithmetic, and rebalancing moves whole slots.'),
        (u'Cassandra / Scylla', u'A token ring with 256 vnodes per node by default; replicas '
                                u'are the next nodes clockwise, skipping racks.'),
        (u'Memcached clients', u'Ketama, the original client-side consistent hashing '
                               u'implementation — the reason a node failure is not a total '
                               u'cache flush.'),
        (u'Load balancers / CDNs', u'Consistent hashing on a request key to keep a user or an '
                                   u'object pinned to one backend, so its cache stays warm.')]),
    h2(u'3.5 The two alternatives worth naming'),
    bullets([
        u'<b>Rendezvous (highest random weight) hashing:</b> for each key, compute '
        u'<b>hash(key, node)</b> for every node and take the maximum. No ring, no vnodes, same '
        u'minimal movement, and weights are easy. O(N) per lookup, which is fine for tens of '
        u'nodes.',
        u'<b>Jump consistent hash:</b> a handful of lines, no memory, perfectly balanced — but '
        u'buckets are numbered 0…N-1, so you can only add or remove at the end. Excellent for '
        u'stateless sharding of work, wrong when specific nodes must be removed.',
        u'<b>Fixed logical buckets:</b> not an algorithm so much as a design — hash into 1,024 '
        u'buckets forever and map buckets to nodes in a table you can edit. Most production '
        u'systems end up here, because it makes migration a routing change (Part 5).']),
)

# ═════════════════════════════════════════════════════════ Part 4
book.page(
    part(u'Routing and topology', u'PART 4',
         u'Something has to turn a key into a connection. Where that logic lives is a real '
         u'architectural choice, and each option has a failure mode interviewers like to probe.'),
    h2(u'4.1 Three places to put the routing'),
    table([u'Where', u'How it works', u'Cost / failure mode'],
          [(u'In the client',
            u'The library holds the topology and connects straight to the right shard — '
            u'Cassandra and Redis Cluster drivers work this way',
            u'One extra hop saved, but every service embeds the map: rolling out a topology '
            u'change means redeploying clients, and every client needs connections to every '
            u'shard'),
           (u'In a proxy',
            u'A stateless layer (Vitess, ProxySQL, Twemproxy, Envoy) parses or hashes and '
            u'forwards',
            u'One deploy point and connection pooling for free; adds a hop of latency and a '
            u'tier to scale and page for'),
           (u'In a coordinator',
            u'Any node accepts any request and forwards internally — Dynamo-style',
            u'Simplest client in the world; the internal hop is on every request and a slow '
            u'node slows requests it does not own')],
          [116.0, 210.0, 196.0]),
    h2(u'4.2 The metadata problem'),
    p(u'Whoever routes needs the current map: which shard owns which range, and where that shard '
      u'lives. That map is small, read constantly and must survive failover — so it lives in a '
      u'consensus store (ZooKeeper, etcd, Consul), is cached everywhere, and carries a version '
      u'number. When a client is stale it must find out cheaply: Redis Cluster answers with '
      u'<b>MOVED</b> (permanent, update your map) or <b>ASK</b> (temporary, this key only), and '
      u'every well-designed router has an equivalent.'),
)

book.page(
    h2(u'4.3 The queries you must design for', 'qhead'),
    cards(
        ('good', u'Single-shard (the target)',
         [u'The key is in the request, so one lookup answers it. This is the shape you '
          u'denormalise <i>towards</i>. Latency is one hop and capacity scales linearly.']),
        ('bad', u'Scatter-gather (the tax)',
         [u'No key, so every shard is asked and the results merged. Latency becomes the '
          u'<i>slowest</i> shard — a p99 on one node becomes the p50 of the whole query at '
          u'enough fan-out.']),
    ),
    p(u'Three ways to make scatter-gather survivable, all worth naming: bound the fan-out (never '
      u'query 200 shards for one page of results); set a per-shard deadline and return partial '
      u'results marked as partial; and cache the merged answer, because the query that needed '
      u'the fan-out is usually not personalised.'),
    h2(u'4.4 Connections, the thing that actually breaks'),
    p(u'A fleet of 200 services × 20 pods × a pool of 10 connections × 32 shards is 1.28 million '
      u'connections. That number is why proxies exist. Say it: <b>“client-side routing means '
      u'every client holds a pool to every shard, so connection count grows with '
      u'fleet × shards — past a certain size you need a proxy tier or transaction-mode '
      u'pooling.”</b>'),
    h2(u'4.5 Secondary indexes across shards'),
    kv([(u'Local index',
         u'Each shard indexes its own rows. Cheap and consistent — but a query without the '
         u'shard key must ask every shard.'),
        (u'Global index',
         u'A separate structure sharded by the index key. One lookup, but it is a second '
         u'write on every change and it is eventually consistent.'),
        (u'The honest framing',
         u'“Local index, scatter-gather read” or “global index, asynchronous write” — those '
         u'are the only two options and I would pick per query.'),
        (u'What DynamoDB calls them',
         u'LSI is local (same partition key, extra sort key); GSI is global, with its own '
         u'partitioning and its own capacity.')]),
)

# ═════════════════════════════════════════════════════════ Part 5
book.page(
    part(u'Resharding a live system', u'PART 5 · THE QUESTION NOBODY PREPARES',
         u'“You picked user_id and now one tenant is 40% of the data. Reshard it, with the site '
         u'up.” This is the follow-up that separates people who have done it from people who '
         u'have read about it.'),
    h2(u'5.1 The four mechanisms'),
    kv([(u'Split a range',
         u'Range-partitioned stores (HBase, Bigtable, CockroachDB, MongoDB) split a hot range '
         u'in two and move half. Automatic in some, a command in others.'),
        (u'Move logical buckets',
         u'If keys map to 1,024 buckets and buckets map to nodes, you move buckets. This is '
         u'the design that makes resharding boring.'),
        (u'Add vnodes / slots',
         u'Consistent-hashing clusters stream the arcs or slots the new node claims. Redis '
         u'Cluster and Cassandra both do this online.'),
        (u'Copy and cut over',
         u'The general answer when the store gives you nothing: dual-write, backfill, verify, '
         u'flip — described below.')]),
    fig(u'5.1', F.fig_reshard(),
        u'The migration order. The only irreversible step is the last one, and it happens days '
        u'after the flip.'),
)

book.page(
    h2(u'5.2 Saying the migration out loud', 'qhead'),
    p(u'The interviewer is listening for reversibility and verification, not for the copy '
      u'itself. Five sentences:'),
    bullets([
        u'<b>Dual-write</b> every mutation to the old and the new shard, behind a flag, from the '
        u'same code path — so there is one place to turn it off.',
        u'<b>Backfill</b> history in batches, throttled and resumable, keyed by primary key '
        u'ranges so a restart continues rather than starts over.',
        u'<b>Verify</b> before trusting: row counts per range, checksums over key ranges, and a '
        u'shadow-read comparison that logs mismatches without serving them.',
        u'<b>Flip reads</b> gradually — per tenant, per key range, or by percentage — with an '
        u'instant rollback, and watch error rate and latency per shard, not globally.',
        u'<b>Stop writing the old shard days later</b>, and only drop it when you would no '
        u'longer want it back.']),
    callout(u'THE TRAP TO NAME FIRST',
            [u'Dual-writing from application code is <i>not</i> atomic: the old write can '
             u'succeed and the new one fail, and now the copies disagree in a way no retry will '
             u'notice. Either drive the copy from the database’s own log (CDC) or from an '
             u'outbox table written in the same transaction — and reconcile with the checksum '
             u'job either way. Volunteering this is a strong senior signal.'],
            ''),
    h2(u'5.3 Choosing the shard count'),
    p(u'Pick a number you can divide, not a number you will outgrow: powers of two make '
      u'splitting a shard into two clean, and hashing into a large fixed bucket space (1,024 or '
      u'4,096) decouples “how many buckets” from “how many machines” forever. The cost is a '
      u'bucket-to-node table you must keep authoritative — a small price for turning every '
      u'future reshard into a routing change.'),
)

# ═════════════════════════════════════════════════════════ Part 6
book.page(
    part(u'Living with shards', u'PART 6',
         u'A sharded system is not a bigger database; it is a distributed system with different '
         u'rules. These are the six places that surprise teams after the migration is over.'),
    h2(u'6.1 Transactions that span shards'),
    p(u'There is no single-node ACID across shards, so you have three honest options: <b>keep '
      u'the transaction inside one shard</b> by choosing the key so related rows co-locate (best '
      u'answer, and it is a modelling decision); a <b>saga</b> — a sequence of local '
      u'transactions with compensating actions and an idempotency key on every step; or '
      u'<b>two-phase commit</b>, which is correct, blocking, and slow enough that most systems '
      u'refuse it. Distributed SQL engines (Spanner, CockroachDB, TiDB, Vitess with 2PC) will do '
      u'it for you, and the price is latency and coordination.'),
    h2(u'6.2 Uniqueness and IDs'),
    kv([(u'Global uniqueness',
         u'A unique index is per shard. Use a dedicated claim table sharded <i>by the unique '
         u'value</i>, so “claim this email” lands on exactly one shard and is atomic there.'),
        (u'ID generation',
         u'No auto-increment. Snowflake, UUIDv7 or a KGS (key-generation service handing out '
         u'blocks) — ordered, compact, coordination-free.'),
        (u'Never shard on a monotonic key',
         u'Time or auto-increment sends every insert to the newest shard. Hash it, or prefix '
         u'it with something high-cardinality.'),
        (u'Carry the shard hint',
         u'Encoding the shard or bucket in the public id (or the URL) means routing needs no '
         u'lookup at all — a trick worth mentioning.')]),
    h2(u'6.3 Aggregates, reports and the warehouse'),
    p(u'The first “how many users signed up today?” after sharding is a scatter-gather over '
      u'every shard, and the second one is a nightly job. Maintain counters as you write for the '
      u'numbers users see, stream changes into a columnar warehouse for the numbers analysts '
      u'ask for, and say the staleness out loud (“the dashboard is five minutes behind”).'),
)

book.page(
    h2(u'6.4 Operating N of everything', 'qhead'),
    table([u'Concern', u'What changes', u'What you do'],
          [(u'Monitoring',
            u'A healthy average hides one dying shard',
            u'Every metric per shard, plus a “worst shard” panel and alerts on skew'),
           (u'Backups & restore',
            u'N backups, and a restore is only consistent per shard',
            u'Automate per shard; for cross-shard consistency, restore to a timestamp and '
            u'replay'),
           (u'Schema changes',
            u'A migration is now N migrations that can partially fail',
            u'Expand–contract, driven by a tool that tracks per-shard state and can resume'),
           (u'Noisy tenants',
            u'One tenant’s traffic degrades everyone on its shard',
            u'Per-tenant quotas, and move the big ones to their own shard — the directory '
            u'strategy earning its keep'),
           (u'Rebalancing',
            u'Growth is uneven, so the layout drifts',
            u'Track bytes and QPS per shard; move buckets on a schedule rather than in an '
            u'incident'),
           (u'Capacity',
            u'“Add a node” is now a data movement, not a deploy',
            u'Keep headroom (60–70% target), because rebalancing needs spare I/O to finish')],
          [104.0, 190.0, 228.0]),
    p(u'The one-liner for this whole page: <b>“sharding turns a database problem into a fleet '
      u'problem, so everything I do to one shard has to be automated for all of them from day '
      u'one.”</b>', 'note'),
)

# ═════════════════════════════════════════════════════════ Part 7
book.page(
    part(u'The interview itself', u'PART 7',
         u'Sharding questions arrive as “how would you scale this?” or as a trap: a key that '
         u'looks reasonable and skews horribly. Both want the same four-step answer.'),
    h2(u'7.1 The four-step answer'),
    strip([(u'1', u'Justify', u'The number that rules out cache, replicas and a bigger box'),
           (u'2', u'Pick the key', u'Cardinality, distribution, query alignment, stability'),
           (u'3', u'Route it', u'Client, proxy or coordinator — and where the map lives'),
           (u'4', u'Name the tax', u'The queries that now fan out, and how you handle them')]),
    h2(u'7.2 The five sentences that earn points'),
    bullets([
        u'“One primary handles roughly 5–10k writes a second; we need 40k, so this has to '
        u'split.”',
        u'“I would shard on conversation_id, because every read in this product is scoped to a '
        u'conversation.”',
        u'“Consistent hashing with virtual nodes, so adding a node moves about 1/N of the keys '
        u'and not the whole keyspace.”',
        u'“That query has no shard key, so it becomes scatter-gather — I would bound the '
        u'fan-out and cache the merged result.”',
        u'“I would hash into 1,024 logical buckets and map buckets to nodes, so the next '
        u'reshard is a routing change instead of a migration.”']),
    callout(u'INTERVIEW LINE',
            [u'“I want to be explicit that sharding is the expensive option: I lose cross-shard '
             u'joins, single-node transactions and easy uniqueness, and I gain write capacity. I '
             u'am choosing it because the write rate is above what one primary can take, and I '
             u'will design the key so that the three hot queries all stay on one shard.”'],
            'teal'),
)

book.page(
    h2(u'7.3 Fourteen questions with model answers', 'qhead'),
    qa(u'1', u'When would you shard, and when would you refuse?',
       [u'When one machine cannot hold the writes, the hot data no longer fits in memory, or the '
        u'data set has grown past what you can back up and migrate — or when isolation and data '
        u'residency demand it. I refuse while a composite index, a cache, read replicas or a '
        u'bigger instance would do, because sharding costs joins, transactions, uniqueness and '
        u'operational simplicity, permanently.']),
    qa(u'2', u'Explain consistent hashing as if I have not heard of it.',
       [u'Hash the keys and the nodes into the same circular space. A key belongs to the first '
        u'node clockwise from it. Adding a node claims one arc of the circle, so only the keys '
        u'in that arc move — about 1/N of them — instead of the near-total reshuffle you get '
        u'from <b>hash % N</b>. Each physical node is placed at a hundred or more points '
        u'(virtual nodes) so the arcs are even and a new node takes a slice from everyone, not '
        u'just from its neighbour.']),
    qa(u'3', u'What is wrong with hash(key) % N?',
       [u'N is in the formula, so changing the node count changes almost every mapping. For a '
        u'cache that means a near-total miss storm against the database at the worst possible '
        u'moment; for a store it means moving nearly all the data. Consistent hashing, '
        u'rendezvous hashing, or a fixed bucket space all exist to take N out of the key’s '
        u'identity.']),
    qa(u'4', u'How do you pick a shard key for a chat app?',
       [u'<b>hash(conversation_id)</b>, because every read is “the recent messages in this '
        u'conversation” and every write appends to one. That keeps reads and writes on one shard '
        u'and lets the shard hold them clustered by time. Sharding by user_id instead would put '
        u'a two-person conversation on two shards and make every read a merge.'],
       [('', u'Follow-up:', u'a very large group chat is a hot partition — bucket it by '
                            u'<b>(conversation_id, time window)</b> so history spreads while '
                            u'recent messages stay together.')]),
)

book.page(
    qa(u'5', u'One tenant is 40% of the data. What now?',
       [u'That is the directory strategy’s reason to exist: give the whale its own shard, or its '
        u'own cluster, and leave everyone else on hash-based placement. Concretely — mark the '
        u'tenant in the routing table, dual-write and backfill it to the new shard, verify with '
        u'checksums, flip its reads, then stop writing the old copy. Nothing about the other '
        u'tenants has to change, which is exactly why I would keep a routing table rather than '
        u'pure hashing for multi-tenant data.']),
    qa(u'6', u'A single celebrity key is saturating one shard. Fix it.',
       [u'Name the mechanism first: one key hashes to one shard, so more shards cannot help. For '
        u'reads, put a short-TTL local cache in front so each app server fetches it once per TTL. '
        u'For writes, split the key — <b>likes:{post}:{0..15}</b> written at random and folded '
        u'into a total by a worker — and make sure those sub-keys hash to different shards, '
        u'which means no shared hash tag.']),
    qa(u'7', u'How do you run a transaction across two shards?',
       [u'First I try not to: choose the key so the rows that must change together live on one '
        u'shard — that is a modelling decision and it is the right answer most of the time. When '
        u'it genuinely spans shards, a saga: local transactions plus compensating actions, an '
        u'idempotency key per step, and a state machine that can resume. Two-phase commit is '
        u'available and correct, and it blocks on the coordinator, so I would only reach for it '
        u'with a distributed SQL engine doing the work.']),
    qa(u'8', u'How do you keep an email address unique across 32 shards?',
       [u'A unique index only covers its own shard, so I add a claim table sharded <b>by the '
        u'email</b> itself: insert the claim first, and the insert either succeeds on that one '
        u'shard or fails. The user row can then live on its own shard keyed by user_id. The '
        u'general pattern is “route the uniqueness check by the unique value”, and it applies to '
        u'usernames, slugs and idempotency keys alike.']),
    qa(u'9', u'Your query has no shard key. What happens and what do you do?',
       [u'It becomes scatter-gather: every shard is asked, results are merged, and the latency '
        u'is the slowest shard — so tail latency becomes typical latency as fan-out grows. '
        u'Options: add a global secondary index sharded by that query’s key and accept it being '
        u'eventually consistent; bound the fan-out and cache the merged result; or answer it '
        u'from a warehouse if it is analytical rather than user-facing.']),
)

book.page(
    qa(u'10', u'How many shards would you start with?',
       [u'Enough that each shard is comfortable at projected peak with 40% headroom, in a count '
        u'I can split cleanly — so a power of two. Better still, decouple the two numbers: hash '
        u'into 1,024 logical buckets on day one and map buckets to however many nodes I '
        u'actually run. Adding capacity then means moving buckets, which is a routing change '
        u'rather than a rehash.']),
    qa(u'11', u'How do you reshard without downtime?',
       [u'Dual-write to old and new behind a flag — driven by CDC or an outbox, not a '
        u'best-effort double write in app code. Backfill history in throttled, resumable '
        u'batches. Verify with per-range checksums and shadow reads. Flip reads gradually with '
        u'instant rollback. Keep writing the old shard for days, then drop it. The point I '
        u'would stress is that every step before the last is reversible.']),
    qa(u'12', u'Where should the routing logic live?',
       [u'In a proxy if I have many services or many languages: one deploy point for topology '
        u'changes and connection pooling for free, at the cost of a hop. In the client if I '
        u'have few services and latency matters, accepting that a topology change means '
        u'redeploying clients and that connection count is fleet × shards. Either way the map '
        u'lives in a consensus store, is versioned, and clients can be told they are stale.']),
    qa(u'13', u'What breaks operationally after you shard?',
       [u'Averages stop being informative — one dying shard hides behind 31 healthy ones, so '
        u'every metric has to be per shard with an alert on skew. Backups and restores are per '
        u'shard and only consistent per shard. Migrations become N migrations that can partially '
        u'fail, so they need per-shard state and resumability. And capacity planning becomes '
        u'data movement, which needs spare I/O to complete.']),
    qa(u'14', u'Partitioning or sharding — what is the difference, and which do you need here?',
       [u'Partitioning splits one table inside one database: the engine prunes partitions, '
        u'retention becomes a partition drop, and I still have one write primary and real '
        u'transactions. Sharding splits across independent databases and buys write capacity at '
        u'the cost of joins, transactions and uniqueness. If the pain is query time on a huge '
        u'time-series table, partition. If the pain is write throughput or total size, shard.']),
)

book.page(
    h2(u'7.4 Red flags interviewers listen for', 'qhead'),
    table([u'Saying this', u'Says this about you'],
          [(u'Sharding as the first scaling move',
            u'Has not priced the cheaper options'),
           (u'“Shard by user_id” with no access-pattern argument',
            u'Guessing, not designing'),
           (u'Sharding on a timestamp or auto-increment id',
            u'Has built a write hotspot on the newest shard'),
           (u'“Add more shards” for a hot key',
            u'Does not know that one key maps to one shard'),
           (u'Using hash % N in a design',
            u'Has never resized a cluster'),
           (u'No answer for cross-shard joins',
            u'Has not thought past the happy path'),
           (u'Auto-increment IDs after sharding',
            u'Collisions, or a single sequence that is now a bottleneck'),
           (u'“We’ll just reshard later”',
            u'Has never done it; there is no “just”'),
           (u'Dual-writing from app code with no reconciliation',
            u'Silent divergence, and no way to detect it'),
           (u'Global aggregates as if nothing changed',
            u'Every COUNT(*) is now a fan-out')],
          [232.0, 290.0]),
    h2(u'7.5 Real systems worth name-dropping'),
    cards(
        ('', u'Amazon Dynamo (2007)',
         [u'Consistent hashing with virtual nodes, replica placement clockwise, quorums and '
          u'hinted handoff. The paper everything else in this volume descends from.']),
        ('', u'Vitess (YouTube → CNCF)',
         [u'MySQL sharding as a proxy layer: vschema, keyspaces, resharding by splitting '
          u'keyspace ranges online. Cite it as the industrial answer to “reshard MySQL live”.']),
    ),
    cards(
        ('', u'Redis Cluster’s 16,384 slots',
         [u'Fixed logical buckets instead of a ring, with MOVED/ASK redirects. The clearest '
          u'production example of decoupling bucket count from node count.']),
        ('', u'Figma’s Postgres sharding (2024)',
         [u'A widely read account of picking shard keys per table group, logical sharding '
          u'first and physical later. Good evidence you read post-mortems, not just papers.']),
    ),
)

# ---- cheat sheet ----
book.page(
    u'<span class="chip rev">R E V I S I O N</span>'
    u'<h1 class="big">One-page cheat sheet</h1>'
    + p(u'The night-before page. If you remember only this, you can still hold a good '
        u'conversation about splitting data.', 'sub')
    + u'<hr class="thin">',
    h2(u'The numbers'),
    formula(u'one primary ~ 5–10k writes/s &nbsp;·&nbsp; adding a node moves ~1/(N+1) of keys '
            u'&nbsp;·&nbsp; 100–256 vnodes per node',
            u'Target 60–70% utilisation per shard so rebalancing has room to finish, and keep '
            u'the logical bucket count (1,024 or 4,096) far larger than the node count.'),
    h2(u'The decisions'),
    table([u'Question', u'Default answer'],
          [(u'Shard yet?', u'No — until write rate, working set or total size proves it'),
           (u'Which strategy?', u'Hash for even spread; directory when tenants differ wildly; '
                                u'range only for time-shaped data you will drop'),
           (u'Which key?', u'The one that appears in your top three queries and has high '
                           u'cardinality'),
           (u'How many shards?', u'A power of two — and hash into 1,024 logical buckets '
                                 u'regardless'),
           (u'Rebalancing?', u'Consistent hashing with virtual nodes, or move logical buckets'),
           (u'Routing?', u'Proxy for many services; client-side for few and latency-critical'),
           (u'Cross-shard write?', u'Redesign the key first; then a saga; 2PC last'),
           (u'Unique constraint?', u'A claim table sharded by the unique value'),
           (u'IDs?', u'Snowflake or UUIDv7 — never a global auto-increment'),
           (u'Reshard?', u'Dual-write → backfill → verify → flip → drop, days apart')],
          [148.0, 374.0]),
)

book.page(
    h2(u'Sharding in eight facts', 'qhead'),
    facts([
        (u'It buys one thing',
         u'Capacity past one machine. Everything else on the invoice is a cost.'),
        (u'The key is the design',
         u'Cardinality, distribution, query alignment, stability — in that order.'),
        (u'One key lives on one shard',
         u'So a hot key is never fixed by adding shards. Cache it or split it.'),
        (u'Monotonic keys are hotspots',
         u'Time and auto-increment send every insert to the newest shard.'),
        (u'hash % N is an outage',
         u'Changing N remaps almost everything. Ring, rendezvous, or fixed buckets instead.'),
        (u'Virtual nodes make it even',
         u'Many small arcs per node: even load, and a new node relieves everybody.'),
        (u'No shard key means fan-out',
         u'Scatter-gather latency is the slowest shard’s latency. Bound it and cache it.'),
        (u'Resharding is reversible until the flip',
         u'Dual-write, backfill, verify, then flip — and keep the old copy for days.'),
    ], tone='acc'),
    h2(u'The five failure modes'),
    table([u'Name', u'Mechanism', u'Primary fix'],
          [(u'Hot shard', u'One key or tenant takes a disproportionate share',
            u'Local cache, key salting, or a dedicated shard'),
           (u'Newest-shard hotspot', u'Monotonic shard key',
            u'Hash the key, or prefix with high-cardinality data'),
           (u'Fan-out tail', u'Query without the shard key touches every shard',
            u'Global index, bounded fan-out, cached merge'),
           (u'Rebalance storm', u'Migration competes with production I/O',
            u'Throttle, run off-peak, keep 30–40% headroom'),
           (u'Split brain in the map', u'Two routers disagree about ownership',
            u'Versioned topology in a consensus store, redirect on stale')],
          [112.0, 204.0, 206.0]),
)

book.page(
    closing(u'IF YOU SAY NOTHING ELSE, SAY THIS',
            u'“Sharding is the expensive answer, so I only reach for it when one machine cannot '
            u'take the writes, hold the working set, or be operated at that size. Then the whole '
            u'design is the key: high cardinality, even distribution, and present in my top '
            u'three queries — so almost every request stays on one shard. I would place it with '
            u'consistent hashing over virtual nodes, or better, hash into a fixed set of logical '
            u'buckets so future rebalancing is a routing change. And I would say out loud what I '
            u'gave up: cross-shard joins, single-node transactions and cheap global '
            u'uniqueness.”'),
    p(u'<b>Sources &amp; further reading</b> — DeCandia et al., <i>Dynamo: Amazon’s Highly '
      u'Available Key-value Store</i> (SOSP 2007); Karger et al., <i>Consistent Hashing and '
      u'Random Trees</i> (1997); Thaler &amp; Ravishankar on rendezvous hashing; Lamping &amp; '
      u'Veach, <i>A Fast, Minimal Memory, Consistent Hash Algorithm</i> (jump hash); Martin '
      u'Kleppmann, <i>Designing Data-Intensive Applications</i>, chapter 6; the Redis Cluster '
      u'specification; Cassandra documentation on token ranges and virtual nodes; the Vitess '
      u'documentation on resharding; Figma’s engineering blog on sharding Postgres; Notion’s '
      u'write-up on sharding its Postgres monolith; MongoDB documentation on chunk splitting '
      u'and balancing.', 'src'),
)

book.write('v_sharding.html')
