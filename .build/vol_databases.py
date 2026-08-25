# -*- coding: utf-8 -*-
"""Volume: Databases & Data Modelling for system design interviews."""
from kit import (Book, cover, toc, qa, facts, table, cards, callout, formula, closing,
                 part, fig, kv, bullets, strip, codebox, codes, p, h2, h3, cd, STAR)
import figs_db as F

THEME = dict(
    bgimg=(u'radial-gradient(52% 37% at 90% 7%, rgba(150,235,205,.30) 0%, '
           u'rgba(150,235,205,.08) 58%, rgba(150,235,205,0) 72%),'
           u'radial-gradient(34% 24% at 2% 99%, rgba(214,196,90,.34) 0%, '
           u'rgba(214,196,90,.07) 62%, rgba(214,196,90,0) 74%),'
           u'linear-gradient(157deg,#08171f 0%,#0b2830 20%,#0f3a3c 38%,#134b44 56%,'
           u'#1a5c44 72%,#2a6f3f 88%,#48843a 100%)'),
    hi=u'#8ee6bd', eye=u'#8fd8c8', ledec=u'#cfe6dd', cardp=u'#c6ddd4', metac=u'#a4c3ba',
    barg=u'linear-gradient(90deg,#8ee6bd 0%,#d6c45a 100%)',
    acc=u'#0d7a84', acctint=u'#e4f4f5', qn=u'#6fd0c0',
)
EYEBROW = (u'S Y S T E M &nbsp;D E S I G N &nbsp; / &nbsp; '
           u'I N T E R V I E W &nbsp;P L A Y B O O K')

book = Book(u'The Complete Guide to Databases', THEME)

# ═════════════════════════════════════════════════════════ front matter
book.raw(cover(
    THEME, EYEBROW,
    u'The Complete Guide<br>to <span class="hi">Databases</span>',
    u'Choosing a store, the engine underneath it, indexes, data models, isolation levels and '
    u'the operational failure modes — everything an HLD interview can ask about the layer your '
    u'design actually depends on.',
    [(u'Pick a store on evidence',
      u'Access pattern first, brand second. Nine store families and what each one charges you.'),
     (u'B-tree vs LSM, properly',
      u'Pages, WAL, memtables, compaction, write and read amplification — and which wins when.'),
     (u'Indexes and models that scale',
      u'Leftmost prefix, covering indexes, keyset pagination, single-table design, ID choices.'),
     (u'Isolation and the real bugs',
      u'Lost update, write skew, MVCC, optimistic locking, deadlocks, replica lag, migrations.')],
    u'7 parts · 4 diagrams · 14 interview Q&amp;A · one-page cheat sheet',
    u'Revised August 2026'))

book.page(toc(
    u'C O N T E N T S',
    u'What’s inside',
    u'Read it front to back once. After that, Part 2 (engines), Part 5 (isolation) and Part 7 '
    u'(interview answers) are the pages that earn the most points per minute of revision.',
    [(u'1', u'', u'Choosing a datastore',
      u'Access patterns before products, the nine store families, SQL vs NoSQL without the '
      u'marketing, and the real cost of a second store.'),
     (u'2', u'', u'Storage engines under the hood',
      u'Pages and the write-ahead log, B-tree vs LSM tree, amplification, row vs columnar, '
      u'what an fsync actually costs.'),
     (u'3', u'', u'Indexing and query performance',
      u'What an index is, composite indexes and the leftmost-prefix rule, covering indexes, '
      u'selectivity, the write cost, keyset pagination.'),
     (u'4', u'', u'Data modelling for scale',
      u'Query-first modelling, denormalisation, single-table design, ID schemes, TTL and '
      u'time-series tables, schema evolution.'),
     (u'5', u'', u'Transactions and isolation',
      u'ACID honestly, the four isolation levels and the anomalies each one still allows, '
      u'MVCC, write skew, optimistic vs pessimistic locking.'),
     (u'6', u'', u'Running it in production',
      u'Connection pools, read replicas and lag, failover with RPO/RTO, online schema change, '
      u'bloat, table partitioning.'),
     (u'7', u'', u'The interview itself',
      u'How to answer a data-layer question, 14 asked-in-real-interviews Q&amp;A, and the red '
      u'flags to avoid.'),
     (STAR, u'star', u'One-page cheat sheet',
      u'The night-before page: the decision table, the numbers, the isolation grid, databases '
      u'in eight facts.')],
    u'<b>Part of the HLD concept series.</b> Caching, Redis, sharding, replication and the '
    u'messaging layer are separate volumes — this one stops where the shard key begins.'))

book.page(
    h2(u'How to use this guide', 'qhead'),
    cards(
        ('', u'Understand',
         [u'Every section opens in plain English before any jargon. If a sentence needs a '
          u'diagram, there is one.']),
        ('', u'Say out loud',
         [u'The grey “interview line” boxes are the exact sentences that earn the point. '
          u'Practise saying them.']),
        ('', u'Defend',
         [u'Every choice lists its cost. Interviewers score the trade-off, not the choice.']),
    ),
    callout(u'A NOTE ON SQL',
            [u'The SQL in this volume is there because the query <i>is</i> the argument — an '
             u'index that does or does not get used, a lock that is or is not taken. You are '
             u'never asked to write production SQL on a whiteboard, but you are absolutely '
             u'asked why a query is slow, and that answer is a sentence about pages, indexes '
             u'and locks.'],
            'blue'),
    callout(u'THE ONE THING TO INTERNALISE',
            [u'A database is a set of trade-offs frozen into a product: how it writes to disk, '
             u'what it locks, what it replicates and what it refuses to do. <b>Every data-layer '
             u'question in an interview is asking whether you can name the trade-off you just '
             u'accepted</b> — not whether you can name a product.'],
            'teal'),
)

# ═════════════════════════════════════════════════════════ Part 1
book.page(
    part(u'Choosing a datastore', u'PART 1',
         u'“Which database would you use?” is never really a question about databases. It is a '
         u'question about your access patterns, and whether you derived the store from them or '
         u'guessed.'),
    h2(u'1.1 Start from the access pattern, always'),
    p(u'Before naming anything, say out loud what the workload does. Four numbers and two '
      u'sentences are enough, and they eliminate most of the menu by themselves:'),
    kv([(u'Read:write ratio',
         u'100:1 says cache and replicas. 1:1 says the write path is the design.'),
        (u'Access shape',
         u'Point lookups by key? Ranges by time? Multi-entity joins? Full-text? Aggregates?'),
        (u'Size and growth',
         u'Rows/day × bytes/row × retention. Say whether it fits one node — most designs do.'),
        (u'Consistency need',
         u'Per operation, not per system: money is strict, a like count is eventual.')]),
    fig(u'1.1', F.fig_choose(),
        u'The four questions that pick the store. Ask them in this order and '
                           u'the answer stops being a matter of taste.'),
)

book.page(
    h2(u'1.2 The nine families, and what each one charges you', 'qhead'),
    p(u'Products change; families do not. Name the family, then one product in it, then the '
      u'bill it hands you.'),
    table([u'Family', u'Reach for it when', u'What it charges you'],
          [(u'Relational<br>Postgres · MySQL',
            u'Joins, transactions across rows, ad-hoc queries, anything money touches',
            u'One primary for writes (~5–10k/s); schema changes need care; sharding is manual'),
           (u'Wide-column<br>Cassandra · Scylla',
            u'Huge write rates, time-series by partition key, linear scale-out, multi-region '
            u'writes',
            u'No joins; you model per query; eventual consistency unless you pay quorum '
            u'latency'),
           (u'Managed KV<br>DynamoDB',
            u'Predictable point access at any scale with no servers to run',
            u'Item and partition limits, GSI cost, and the bill tracks your access pattern'),
           (u'Document<br>MongoDB',
            u'One aggregate read per request, flexible fields, per-document atomicity',
            u'Cross-document transactions are possible but not the design’s strength'),
           (u'In-memory<br>Redis · Memcached',
            u'Sub-millisecond reads, counters, leaderboards, sessions, locks',
            u'RAM cost, and it is a dependency the moment your DB is sized for a hit ratio'),
           (u'Search<br>Elasticsearch',
            u'Free-text, relevance ranking, facets, typo tolerance',
            u'Near-real-time only (refresh interval); a second copy of the data to keep in step'),
           (u'Columnar / OLAP<br>ClickHouse · BigQuery',
            u'Aggregates over billions of rows, dashboards, funnels',
            u'Not for point updates; batch or streaming ingest, not per-request writes'),
           (u'Time-series<br>Prometheus · Timescale',
            u'Metrics, retention windows, downsampling, time-bucketed queries',
            u'Cardinality is the enemy — every label combination is a new series'),
           (u'Object store<br>S3 · GCS',
            u'Blobs: images, video, backups, data-lake files',
            u'No queries. Store the key in your database, never the bytes')],
          [128.0, 205.0, 189.0]),
    callout(u'INTERVIEW LINE',
            [u'“Before I pick a store I want the read:write ratio and the access shape, because '
             u'those two decide it. If reads are point lookups by a known key and writes are '
             u'heavy and append-shaped, I want an LSM-backed wide-column store. If the same '
             u'request needs three entities joined and a transaction across them, I want '
             u'Postgres — and I would rather add a cache than give that up.”'],
            'teal'),
)

book.page(
    h2(u'1.3 SQL vs NoSQL, without the marketing', 'qhead'),
    p(u'The honest framing is not “relational versus not”. It is <b>which guarantees am I '
      u'willing to give up to get horizontal write scale</b> — because that is the actual trade.'),
    cards(
        ('good', u'What relational still wins',
         [u'Joins you did not anticipate, transactions across entities, unique constraints '
          u'the database enforces for you, and an ecosystem of tooling. A single Postgres '
          u'node with an index and a cache handles more than most candidates assume: tens of '
          u'thousands of reads/s and thousands of writes/s.']),
        ('bad', u'What it costs you',
         [u'Writes funnel through one primary, so past roughly 10k writes/s on one table you '
          u'are into partitioning, sharding or a different family. Schema change on a large '
          u'table needs an online-migration tool, not an <b>ALTER</b> in a deploy.']),
    ),
    p(u'Three claims to correct if the interviewer offers them:', 'note'),
    bullets([
        u'<b>“NoSQL is schemaless.”</b> The schema moved into your application code, where '
        u'nothing enforces it. You still have one — you just cannot see it.',
        u'<b>“NoSQL is faster.”</b> Per operation it is often the same order of magnitude. '
        u'What it buys is <i>scale-out</i> of writes and predictable latency at size.',
        u'<b>“Postgres does not scale.”</b> It scales vertically a long way, and reads scale '
        u'with replicas. What does not scale is a single write primary — say that instead.'])
    ,
    h2(u'1.4 Polyglot persistence and its real bill'),
    p(u'Serious systems run more than one store: Postgres for orders, Redis for sessions, '
      u'Elasticsearch for search, S3 for files, a warehouse for analytics. That is normal. What '
      u'a senior answer adds is the cost of the second copy:'),
    kv([(u'Two truths', u'Which store is authoritative? Everything else is a projection, and '
                        u'projections need rebuilding.'),
        (u'A sync path', u'CDC, an outbox, or a dual write you will regret. Name it and its '
                         u'lag.'),
        (u'Twice the operations', u'Backups, upgrades, on-call, capacity, access control — per '
                                  u'store.'),
        (u'A consistency story', u'“Search may be 2 s behind the order table, and here is why '
                                 u'that is acceptable.”')]),
)

# ═════════════════════════════════════════════════════════ Part 2
book.page(
    part(u'Storage engines under the hood', u'PART 2',
         u'Two designs cover almost every store you will name in an interview: the B-tree that '
         u'updates a page in place, and the log-structured merge tree that only ever appends. '
         u'Knowing which one you chose explains your write path, your latency spikes and your '
         u'disk bill.'),
    h2(u'2.1 The two things every engine does first'),
    p(u'<b>Pages.</b> Storage is read and written in fixed blocks — 8 KB in Postgres, 16 KB in '
      u'InnoDB. A row lives inside a page; a “random read” means fetching one page. The buffer '
      u'pool (or page cache) keeps hot pages in RAM, which is why the same query is 100× faster '
      u'the second time and why RAM sizing is a database decision, not an ops afterthought.'),
    p(u'<b>The write-ahead log.</b> Before a change touches the data files it is appended to a '
      u'log and flushed. Crash recovery replays the log. This is why a durable write costs a '
      u'sequential disk flush, why <b>fsync</b> is the unit of write cost, and why group commit '
      u'(batching many transactions into one flush) is the single biggest write-throughput knob '
      u'in every relational engine.'),
    fig(u'2.1', F.fig_engines(),
        u'The same write, two engines. The B-tree pays random I/O now; the LSM pays merge work '
        u'later and read work on every lookup.'),
)

book.page(
    h2(u'2.2 B-tree: sorted, balanced, updated in place', 'qhead'),
    p(u'A B-tree keeps keys sorted in a shallow tree of pages — typically three or four levels '
      u'for hundreds of millions of rows, so any lookup is a handful of page reads. A write '
      u'finds the leaf page and modifies it. When a leaf is full it <b>splits</b>, which is '
      u'where the write amplification and the occasional latency spike come from.'),
    bullets([
        u'<b>Reads are predictable.</b> Point lookups and range scans both walk the same '
        u'structure, so <i>ORDER BY</i> on the index columns is free.',
        u'<b>Writes are random I/O.</b> Two rows written together may live in pages far apart. '
        u'On SSDs this is survivable; on spinning disks it was the whole story.',
        u'<b>Fill factor matters.</b> Pages packed to 100% split on the next insert; leaving '
        u'headroom trades space for fewer splits.',
        u'<b>Monotonic keys are a mixed blessing.</b> Appending to the right edge avoids random '
        u'I/O, but in a sharded world it puts every insert on one shard (Part 4.4).']),
    h2(u'2.3 LSM tree: append now, sort later'),
    p(u'Writes land in an in-memory sorted structure (the <b>memtable</b>) plus the log. When it '
      u'fills, it is flushed to an immutable <b>SSTable</b> on disk. Background <b>compaction</b> '
      u'merges SSTables, drops overwritten values and removes <b>tombstones</b> — the markers '
      u'that record a delete.'),
    table([u'Property', u'What it means', u'Consequence you should name'],
          [(u'Write amplification',
            u'Each byte is rewritten several times as it moves down the levels',
            u'Disk writes are 10–30× the logical write rate; SSD wear is real'),
           (u'Read amplification',
            u'A lookup may touch the memtable and one file per level',
            u'Bloom filters per SSTable make the misses ~free — say this'),
           (u'Space amplification',
            u'Old versions live until compaction reclaims them',
            u'Size-tiered compaction can transiently double disk; levelled trades write I/O '
            u'for space'),
           (u'Tombstones',
            u'Deletes are writes, and they linger until compaction',
            u'Delete-heavy workloads read <i>slower</i>, the classic Cassandra trap')],
          [116.0, 196.0, 210.0]),
)

book.page(
    h2(u'2.4 Which one wins, in one sentence', 'qhead'),
    callout(u'THE ONE-LINER THAT LANDS',
            [u'“B-trees give me fast, predictable reads and in-place updates; LSM trees give me '
             u'sequential writes and cheap ingest, and they claw the read cost back with Bloom '
             u'filters and compaction. Write-heavy and append-shaped goes LSM; read-heavy with '
             u'ranges and transactions goes B-tree.”'],
            'purple'),
    p(u'Where the engines actually live: B-tree in Postgres, MySQL/InnoDB, Oracle and most '
      u'index structures; LSM in Cassandra, ScyllaDB, RocksDB (and therefore in TiKV, CockroachDB '
      u'storage, Kafka Streams state stores), LevelDB, HBase and DynamoDB’s internals. '
      u'MyRocks and Postgres extensions blur the line, which is a good aside if pushed.'),
    h2(u'2.5 Row store vs column store'),
    cards(
        ('', u'Row-oriented (OLTP)',
         [u'All columns of a row sit together, so “give me this order” is one page read. '
          u'Aggregating one column across a billion rows means reading every row.']),
        ('', u'Column-oriented (OLAP)',
         [u'Each column is stored and compressed separately, so <b>SUM(amount)</b> over a '
          u'billion rows reads one column and nothing else — often 10–100× less I/O, with '
          u'compression ratios that row stores cannot reach.']),
    ),
    p(u'This is why analytics does not belong on your OLTP primary: it is not just load, it is '
      u'the wrong physical layout. The standard answer is CDC or a nightly load into a columnar '
      u'store, and the interview point is naming the freshness you accepted (“dashboards are '
      u'five minutes behind”).', 'note'),
    h2(u'2.6 What durability costs, numerically'),
    kv([(u'fsync on NVMe', u'~0.1–1 ms. It is the floor under every committed write.'),
        (u'Group commit', u'Batches N transactions into one flush — throughput scales, latency '
                          u'stays.'),
        (u'Sync replication', u'Adds a network round trip (0.5 ms local, 80 ms cross-region) '
                              u'to every commit.'),
        (u'Async replication', u'Commit returns before the replica has it: fast, and it can '
                               u'lose the tail on failover.')]),
)

# ═════════════════════════════════════════════════════════ Part 3
book.page(
    part(u'Indexing and query performance', u'PART 3',
         u'Most “the database is slow” stories are one missing or unusable index. This part is '
         u'the vocabulary to diagnose that out loud: what an index costs, when the planner can '
         u'use it, and when it silently cannot.'),
    h2(u'3.1 What an index actually is'),
    p(u'A second, sorted copy of some columns plus a pointer to the row. It turns a full scan '
      u'(O(N) pages) into a tree walk (three or four page reads). Everything else about indexing '
      u'follows from that one sentence: it is a copy, so writes maintain it; it is sorted, so '
      u'only prefixes of that sort order can be searched.'),
    h2(u'3.2 Composite indexes and the leftmost-prefix rule'),
    p(u'An index on (A, B, C) is sorted by A, then B within A, then C. You can seek on A, on '
      u'A+B, or on A+B+C — never on B alone, because B is only sorted <i>inside</i> a value of '
      u'A. Getting this right is the difference between a 2 ms query and a table scan.'),
    fig(u'3.1', F.fig_index(),
        u'One index, five queries. The rule is mechanical: equality columns first, then the '
        u'range or sort column.'),
    p(u'Ordering rule for a composite index: <b>equality predicates first, then the range or '
      u'ORDER BY column, then anything you only want to avoid a row fetch for.</b> A range '
      u'column placed before an equality column ends the useful part of the seek right there.',
      'note'),
)

book.page(
    h2(u'3.3 Covering indexes, selectivity, and why the planner ignores you', 'qhead'),
    kv([(u'Covering / index-only scan',
         u'If the index carries every column the query needs, the row is never fetched. '
         u'This is the cheapest big win in a read-heavy table.'),
        (u'Selectivity',
         u'How much of the table a predicate eliminates. An index on a boolean “is_active”, '
         u'90% true, is nearly useless on its own.'),
        (u'Cardinality',
         u'Distinct values. High cardinality (user_id) indexes well; low cardinality (status) '
         u'belongs later in a composite.'),
        (u'Statistics',
         u'The planner uses sampled histograms. Stale statistics after a bulk load is a real '
         u'and common cause of a sudden plan change.')]),
    p(u'Reasons an index exists and still is not used — worth reciting, because interviewers '
      u'ask “the index is there, why is it slow?”:'),
    bullets([
        u'A function or cast wraps the column: <b>WHERE lower(email) = ?</b> cannot use an '
        u'index on <b>email</b> — you need an expression index on <b>lower(email)</b>.',
        u'The predicate is a leading wildcard (<b>LIKE \'%foo\'</b>): no sorted structure can '
        u'help; that is what a search index or a trigram index is for.',
        u'The predicate matches most of the table, so a sequential scan is genuinely cheaper '
        u'than random row fetches. The planner is right and your query needs rethinking.',
        u'Type mismatch between the column and the parameter, so the comparison is not '
        u'index-sargable.',
        u'<b>OR</b> across different columns, which often needs two indexes and a bitmap '
        u'combination rather than one.']),
    h2(u'3.4 The write cost nobody mentions'),
    p(u'Every index multiplies write work: one row insert with five indexes is six structures '
      u'to maintain, six sets of pages to dirty, and six things to replicate. On a write-heavy '
      u'table, deleting an unused index is a performance <i>improvement</i>. Say it — it shows '
      u'you have run one of these systems, not just queried it.'),
)

book.page(
    h2(u'3.5 Pagination: the offset trap', 'qhead'),
    codes(
        codebox(u'OFFSET — degrades with depth',
                u'SELECT * FROM posts\n'
                u'ORDER BY created_at DESC\n'
                u'LIMIT 20 OFFSET 100000;',
                u'The engine still produces and discards 100,000 rows. Page 5,000 is '
                u'thousands of times more expensive than page 1 — and rows shift under the '
                u'user as new posts arrive.'),
        codebox(u'Keyset / cursor — flat cost',
                u'SELECT * FROM posts\n'
                u'WHERE (created_at, id) < (?, ?)\n'
                u'ORDER BY created_at DESC, id DESC\n'
                u'LIMIT 20;',
                u'Seeks straight to the cursor and reads 20 rows. Constant cost at any depth, '
                u'stable under concurrent inserts. This is what every infinite feed uses.'),
    ),
    p(u'Interview framing: “I would expose an opaque cursor, not a page number. Deep OFFSET is '
      u'O(offset) and it double-shows rows when the list is changing underneath — a feed cannot '
      u'use it.”', 'note'),
    h2(u'3.6 Reading a query plan out loud'),
    p(u'You will not be handed an <b>EXPLAIN ANALYZE</b> output on a whiteboard, but naming what '
      u'you would look for is a strong signal. Four things, in order:'),
    strip([(u'1', u'Scan type', u'Index seek, index-only, bitmap, or a sequential scan'),
           (u'2', u'Rows', u'Estimated vs actual — a 100× gap means bad statistics'),
           (u'3', u'Join', u'Nested loop is fine for few rows, hash for many'),
           (u'4', u'Sort', u'A sort or a spill to disk means the index order is wrong')]),
    callout(u'INTERVIEW LINE',
            [u'“I would confirm it with the plan before adding anything: if the estimate and '
             u'the actual row count disagree by orders of magnitude, the fix is statistics, not '
             u'another index. If it is a sequential scan on a selective predicate, the fix is a '
             u'composite index with the equality column first.”'],
            'teal'),
)

# ═════════════════════════════════════════════════════════ Part 4
book.page(
    part(u'Data modelling for scale', u'PART 4',
         u'Relational modelling starts from the entities. Modelling for scale starts from the '
         u'queries. Both are correct in their place, and being explicit about which one you are '
         u'doing is what separates a considered design from a guess.'),
    h2(u'4.1 Query-first modelling'),
    p(u'Write the three or four access patterns down before any table: “timeline for user X, '
      u'newest first”, “order by id”, “all orders for a customer in the last 90 days”. In a '
      u'relational design those become indexes. In a wide-column or KV design they become '
      u'<i>tables</i> — one per access pattern, each denormalised, each written to on the same '
      u'event.'),
    h2(u'4.2 Normalise, then denormalise deliberately'),
    cards(
        ('good', u'Normalised',
         [u'One fact in one place, so updates are cheap and cannot disagree with themselves. '
          u'Reads pay with joins.']),
        ('bad', u'Denormalised',
         [u'The read is one lookup, so it scales and it shards. Writes pay: the same fact now '
          u'lives in several rows, and keeping them in step is your job.']),
    ),
    p(u'The senior sentence is the second half: <b>“I denormalise the read path and accept a '
      u'fan-out write, and I make that write idempotent and replayable so a partial failure is '
      u'recoverable.”</b> Denormalisation without saying how you repair drift is the junior '
      u'version of the same answer.'),
    h2(u'4.3 One row per question: the counter example'),
    p(u'A like count read a million times a second and written a thousand times a second is not '
      u'a column on the post row — that row becomes a lock convoy. Split it: an append-only '
      u'events table or a sharded counter for the writes, and a periodically materialised total '
      u'for the reads. Same data, two shapes, because the two access patterns have nothing in '
      u'common.'),
)

book.page(
    h2(u'4.4 Choosing a primary key', 'qhead'),
    table([u'Scheme', u'Shape', u'Use it when · watch out for'],
          [(u'Auto-increment', u'Dense, monotonic, 8 bytes',
            u'Single-node relational. Leaks volume, needs the DB to mint it, and every insert '
            u'hits the same page or shard'),
           (u'UUIDv4', u'Random, 16 bytes',
            u'Client can mint it offline. Random order destroys B-tree locality and bloats '
            u'indexes — measurable on large tables'),
           (u'UUIDv7 / ULID', u'Time-ordered prefix + random',
            u'The modern default: client-generated, index-friendly, sortable by creation. '
            u'Still 16 bytes'),
           (u'Snowflake', u'timestamp | machine | sequence, 8 bytes',
            u'When you need ordered, compact, coordination-free IDs at high rate — Twitter, '
            u'Discord. Needs machine-ID assignment and clock discipline'),
           (u'Natural key', u'Email, ISBN, tenant slug',
            u'Only when it is genuinely immutable. People change emails; countries rename '
            u'themselves')],
          [104.0, 132.0, 286.0]),
    callout(u'THE TRAP TO NAME',
            [u'A monotonically increasing key is the best thing for a single B-tree (append at '
             u'the right edge) and the worst thing for a sharded cluster (every write lands on '
             u'the newest partition). If you shard on time or on an auto-increment id, you have '
             u'built a hotspot — prefix with something high-cardinality, or hash the key.'],
            ''),
    h2(u'4.5 Time-series and TTL tables'),
    bullets([
        u'<b>Partition by time</b> (daily or monthly) so retention is a <b>DROP PARTITION</b>, '
        u'not a <b>DELETE</b> of a billion rows that bloats the table and floods replication.',
        u'<b>Bucket the partition key</b> in wide-column stores: <b>(sensor_id, day)</b> keeps '
        u'partitions bounded — an unbounded partition is the number-one Cassandra design '
        u'mistake.',
        u'<b>Let the store expire rows</b> where it can (DynamoDB TTL, Cassandra TTL, '
        u'Timescale retention policies) instead of writing your own reaper.']),
)

book.page(
    h2(u'4.6 Single-table design, when the store is DynamoDB', 'qhead'),
    p(u'In a KV/wide-column store you cannot join, so the join is done at write time by putting '
      u'related items under one partition key with sortable prefixes. One query then returns a '
      u'whole aggregate — user, their orders, their addresses — with a single round trip.'),
    table([u'PK', u'SK', u'Item'],
          [(u'USER#42', u'PROFILE', u'name, email, created_at'),
           (u'USER#42', u'ORDER#2026-08-01#1183', u'total, status'),
           (u'USER#42', u'ORDER#2026-08-14#1204', u'total, status'),
           (u'USER#42', u'ADDR#home', u'line1, city, postcode'),
           (u'ORDER#1204', u'ITEM#7', u'sku, qty, price')],
          [110.0, 190.0, 222.0]),
    p(u'“Give me user 42 and their last 10 orders” is one query with <b>PK = USER#42 AND '
      u'begins_with(SK, \'ORDER#\')</b>, newest first. Access patterns you did not model need a '
      u'<b>global secondary index</b> — which is a second copy, updated asynchronously, and '
      u'therefore eventually consistent. Say that when you add one.'),
    h2(u'4.7 Schema evolution without downtime'),
    strip([(u'1', u'Expand', u'Add the new nullable column or table. Nothing reads it yet'),
           (u'2', u'Dual-write', u'Write both shapes. Deploy readers that tolerate either'),
           (u'3', u'Backfill', u'Migrate old rows in batches, throttled, resumable'),
           (u'4', u'Contract', u'Flip reads to the new shape, then drop the old one')]),
    p(u'This expand–contract sequence is the answer to “how do you change a schema on a live '
      u'table?” — plus the tooling: <b>gh-ost</b> or <b>pt-online-schema-change</b> for MySQL, '
      u'a concurrent index build and a <b>NOT VALID</b> constraint promoted later for Postgres. '
      u'The failure to avoid is the migration that takes an <b>ACCESS EXCLUSIVE</b> lock on a '
      u'hot table during peak traffic.', 'note'),
)

# ═════════════════════════════════════════════════════════ Part 5
book.page(
    part(u'Transactions and isolation', u'PART 5 · THE DEEP-DIVE MAGNET',
         u'Nothing separates candidates faster than this part. Everyone can say “ACID”. Very '
         u'few can name what READ COMMITTED still allows, and that is exactly the question '
         u'interviewers reach for when they want to find your ceiling.'),
    h2(u'5.1 ACID, honestly'),
    kv([(u'Atomicity', u'All of the statements or none. Implemented by the log, not by hope.'),
        (u'Consistency', u'Your invariants hold — the database only enforces the ones you '
                         u'declared as constraints.'),
        (u'Isolation', u'How much concurrent transactions can see of each other. This is the '
                       u'dial, and the default is not the top.'),
        (u'Durability', u'Committed means flushed. Note that “flushed on the primary” is not '
                        u'“present on a replica”.')]),
    h2(u'5.2 The levels, and the anomaly each one still permits'),
    table([u'Level', u'Still allows', u'Cost / where you meet it'],
          [(u'READ UNCOMMITTED', u'Dirty reads — you see uncommitted data',
            u'Effectively unused; MySQL only'),
           (u'READ COMMITTED', u'Non-repeatable reads, phantoms, lost updates',
            u'<b>The Postgres and Oracle default.</b> Cheap, and the level most production bugs '
            u'live at'),
           (u'REPEATABLE READ', u'Phantoms (classically) and write skew',
            u'The MySQL/InnoDB default; in Postgres this is snapshot isolation'),
           (u'SERIALIZABLE', u'Nothing — equivalent to some serial order',
            u'Retries and aborts under contention (SSI), or real locking. Correct, and you pay '
            u'for it')],
          [124.0, 174.0, 224.0]),
    p(u'The four anomalies in one line each: <b>dirty read</b> — seeing uncommitted data; '
      u'<b>non-repeatable read</b> — the same row changes inside your transaction; '
      u'<b>phantom</b> — a new row appears in a range you already queried; <b>lost update</b> — '
      u'two read-modify-writes and one overwrites the other.', 'note'),
)

book.page(
    h2(u'5.3 MVCC and snapshot isolation', 'qhead'),
    p(u'Modern engines do not block readers. Each transaction sees a <b>snapshot</b>: rows carry '
      u'version metadata, and a reader ignores versions committed after it started. Readers '
      u'never block writers and writers never block readers — the property that made Postgres '
      u'and InnoDB usable under load.'),
    p(u'The costs are worth naming, because they are the operational failure modes of Part 6: '
      u'old row versions must be reclaimed (<b>VACUUM</b>, purge threads), so a long-running '
      u'transaction pins garbage and bloats tables; and a snapshot that is minutes old is a '
      u'snapshot of minutes-old truth.'),
    h2(u'5.4 Write skew — the anomaly that survives snapshot isolation'),
    fig(u'5.1', F.fig_skew(),
        u'Write skew: two transactions read overlapping data, write disjoint rows, and together '
        u'break an invariant that each of them individually preserved.'),
    callout(u'THE FIXES, IN ORDER OF PREFERENCE',
            [u'<b>1.</b> Put the invariant in the database: a unique index, a check constraint, '
             u'an exclusion constraint. Nothing beats a constraint. <b>2.</b> Take the conflict '
             u'explicitly: <b>SELECT … FOR UPDATE</b> on the rows the invariant spans, or a '
             u'materialised “lock row” when the invariant spans a set. <b>3.</b> Run that '
             u'transaction at <b>SERIALIZABLE</b> and be ready to retry on abort. '
             u'<b>4.</b> Last resort: a distributed lock — which is an efficiency lock, not a '
             u'correctness one.'],
            'purple'),
)

book.page(
    h2(u'5.5 Optimistic vs pessimistic, and the last item in stock', 'qhead'),
    codes(
        codebox(u'Optimistic — version check',
                u'-- read\nSELECT qty, version FROM stock WHERE id = 9;\n\n'
                u'-- write only if nobody moved\nUPDATE stock SET qty = qty - 1,\n'
                u'       version = version + 1\n'
                u' WHERE id = 9 AND version = 41;\n-- 0 rows updated → retry',
                u'No locks held while the user thinks. Best when conflicts are rare — and the '
                u'retry path must exist, or you have just built a silent data-loss bug.'),
        codebox(u'Pessimistic — lock the row',
                u'BEGIN;\nSELECT qty FROM stock\n WHERE id = 9\n FOR UPDATE;   -- others wait\n\n'
                u'UPDATE stock SET qty = qty - 1\n WHERE id = 9;\nCOMMIT;',
                u'Correct under heavy contention and simple to reason about. Costs held locks, '
                u'so it needs short transactions, a lock timeout, and an eye on deadlocks.'),
    ),
    p(u'Best answer of all for a decrement: let the database do it in one statement — '
      u'<b>UPDATE stock SET qty = qty - 1 WHERE id = 9 AND qty > 0</b> — and treat “0 rows '
      u'affected” as out of stock. One statement, no read-modify-write, no lost update, and the '
      u'invariant is enforced by the predicate.', 'note'),
    h2(u'5.6 Deadlocks, in one paragraph'),
    p(u'Two transactions hold what the other needs. The engine detects the cycle and kills one, '
      u'so your application must retry — that is not an error condition, it is normal operation '
      u'under contention. You reduce them by touching rows in a consistent order, keeping '
      u'transactions short, avoiding user think-time inside a transaction, and taking the '
      u'strongest lock you will need up front rather than upgrading later.'),
)

# ═════════════════════════════════════════════════════════ Part 6
book.page(
    part(u'Running it in production', u'PART 6',
         u'The failure modes that actually page you are rarely exotic. They are connection '
         u'pools, replica lag, a migration at the wrong time, and a table that grew a hundred '
         u'times without anyone re-reading its access pattern.'),
    h2(u'6.1 Connection pooling and the cliff'),
    p(u'Every Postgres connection is a process with its own memory; every MySQL connection a '
      u'thread. A few hundred is healthy, a few thousand is a queue. Serverless functions and '
      u'large fleets hit that ceiling long before they hit CPU, which is why a pooler '
      u'(<b>pgbouncer</b>, RDS Proxy, ProxySQL) sits in front and multiplexes thousands of '
      u'client connections onto tens of server ones.'),
    kv([(u'Size it, do not guess', u'Little’s law: pool = throughput × latency. 500 qps × 4 ms '
                                   u'is ~2 connections busy, plus headroom.'),
        (u'Transaction pooling', u'The mode that actually saves connections — and it forbids '
                                 u'session state and prepared statements across queries.'),
        (u'Bound the queue', u'A pool with no timeout converts a slow database into a hung '
                             u'application. Fail fast and shed.'),
        (u'Per-service pools', u'One noisy service should not be able to consume every '
                               u'connection the primary has.')]),
    h2(u'6.2 Read replicas and the lag you must design for'),
    p(u'Replicas scale reads, not writes, and they are behind — milliseconds normally, seconds '
      u'under load, minutes during a bulk import. That produces the single most common '
      u'user-visible bug in a replicated system: the user writes, is routed to a replica, and '
      u'their own change is missing.'),
    bullets([
        u'<b>Read-your-writes:</b> pin that user’s reads to the primary for a few seconds, or '
        u'carry the write’s log position and require a replica at least that fresh.',
        u'<b>Monotonic reads:</b> route a session to one replica (sticky) so time never appears '
        u'to run backwards.',
        u'<b>Monitor the lag, not the replica count.</b> Lag is a first-class SLI, and it is '
        u'what your failover decision depends on.']),
)

book.page(
    h2(u'6.3 Failover, backups, and the two numbers to quote', 'qhead'),
    kv([(u'RPO — recovery point', u'How much data you accept losing. Async replication makes '
                                  u'this “the unreplicated tail”; sync makes it zero and costs '
                                  u'latency.'),
        (u'RTO — recovery time', u'How long until you are serving again. Automated failover '
                                 u'means seconds to a minute; a restore from backup means '
                                 u'hours.'),
        (u'PITR', u'Continuous log archiving lets you restore to a timestamp — the only real '
                  u'answer to “someone ran a bad UPDATE”.'),
        (u'Restore drills', u'A backup you have never restored is not a backup. Saying this '
                            u'costs nothing and reads as experience.')]),
    p(u'Failover is not free even when it works: connections drop, the new primary has a cold '
      u'cache, and any client caching the old topology needs to re-resolve. And a promotion '
      u'under async replication is a deliberate decision to lose the tail — the interview point '
      u'is that <i>someone</i> must choose availability over that data, explicitly.'),
    h2(u'6.4 Table partitioning is not sharding'),
    cards(
        ('', u'Partitioning (one node)',
         [u'One logical table split into physical partitions by range or hash. The engine '
          u'prunes partitions per query and retention becomes a DROP. Still one primary, still '
          u'one machine’s write capacity.']),
        ('', u'Sharding (many nodes)',
         [u'The data set split across independent nodes with a routing layer above. Adds write '
          u'capacity, and takes away cross-shard joins and single-node transactions. That '
          u'trade-off gets its own volume.']),
    ),
    h2(u'6.5 The four operational smells'),
    table([u'Smell', u'What is really happening', u'Move'],
          [(u'Table bloat', u'Long transactions or heavy updates leave dead versions VACUUM '
                            u'cannot reclaim',
            u'Kill long idle-in-transaction sessions; autovacuum tuning; pg_repack'),
           (u'Sudden plan flip', u'Statistics went stale after a bulk load, or a parameter '
                                 u'sniffed badly',
            u'ANALYZE after loads; check estimate vs actual; pin the plan only as a last '
            u'resort'),
           (u'Hot row', u'Every transaction updates the same counter or state row',
            u'Shard the counter, batch the updates, or move it to Redis with periodic '
            u'materialisation'),
           (u'Queue in a table', u'Polling <b>SELECT … FOR UPDATE SKIP LOCKED</b> at scale, '
                                 u'plus dead tuples',
            u'Fine at low rate and honest about it; past that, a real broker')],
          [104.0, 214.0, 204.0]),
)

# ═════════════════════════════════════════════════════════ Part 7
book.page(
    part(u'The interview itself', u'PART 7',
         u'Data-layer questions arrive in two shapes: “which database?” and “why is this slow / '
         u'wrong?”. The first wants a derivation, the second wants a mechanism. Both want you '
         u'to name the cost of your answer.'),
    h2(u'7.1 A four-step answer that always works'),
    strip([(u'1', u'Access patterns', u'List the 3–4 queries and the read:write ratio'),
           (u'2', u'Shape and size', u'Rows/day × bytes, and whether it fits one node'),
           (u'3', u'Pick and justify', u'Family → product → the guarantee you are buying'),
           (u'4', u'Name the cost', u'What you gave up, and the failure mode you accept')]),
    h2(u'7.2 The five sentences that earn points'),
    bullets([
        u'“Different operations in this system deserve different consistency — the payment is '
        u'strict, the view count is eventual.”',
        u'“This fits on one Postgres primary with a cache and replicas; I would not shard until '
        u'the write rate or the data size forces it.”',
        u'“I would model this per access pattern, so the read is one lookup and the write is a '
        u'fan-out I make idempotent.”',
        u'“That is a lost update, so I need either one atomic statement, a version check, or a '
        u'row lock — and here is which I would choose.”',
        u'“The migration is expand, dual-write, backfill, contract, and every step is '
        u'reversible.”']),
    callout(u'THE QUESTION BEHIND THE QUESTION',
            [u'When an interviewer asks “SQL or NoSQL?”, they are testing whether you '
             u'understand what you lose. Answer with the loss: “Cassandra gives me linear write '
             u'scale and I give up joins, ad-hoc queries and multi-row transactions — so I model '
             u'every read up front and accept that a new query means a new table.”'],
            'teal'),
)

# ---- Q&A ----
book.page(
    h2(u'7.3 Fourteen questions with model answers', 'qhead'),
    qa(u'1', u'How would you choose between Postgres and Cassandra for this feature?',
       [u'Derive it. If the request needs several entities together, needs a transaction across '
        u'them, or the query set will keep changing, Postgres — and I would scale reads with '
        u'replicas and a cache before considering anything else. If writes are tens of '
        u'thousands per second, partitioned naturally by an entity id, and every read is a point '
        u'or range lookup inside one partition, Cassandra.'],
       [('', u'Signal:', u'volunteering the ceiling of the simpler option: “one primary gives '
                         u'me roughly 5–10k writes/s; below that, sharding is complexity I '
                         u'have not earned.”')]),
    qa(u'2', u'B-tree or LSM — what is the difference and when does it matter?',
       [u'B-trees update a page in place: predictable reads, random write I/O, page splits. LSM '
        u'trees append to a memtable and flush immutable SSTables that compaction merges later: '
        u'sequential writes, cheap ingest, and reads that may touch several levels, which Bloom '
        u'filters make survivable. It matters when the workload is write-heavy — that is when '
        u'you pick LSM and accept write amplification and delete-heavy read slowdowns from '
        u'tombstones.']),
    qa(u'3', u'This query is slow and the index exists. What do you check?',
       [u'Whether the index can actually be used. A function or cast around the column, a '
        u'leading wildcard, a type mismatch, or a predicate on the second column of a composite '
        u'index all make it unusable. Then whether it <i>should</i> be used: if the predicate '
        u'matches most of the table, a sequential scan is cheaper and the planner is right. '
        u'Then statistics — an estimate that is 100× off after a bulk load explains a sudden '
        u'plan change.'],
       [('b', u'Bonus:', u'suggest a covering index so the query never fetches the row at all.')]),
    qa(u'4', u'Design the indexes for “orders for a tenant in a date range, newest first”.',
       [u'One composite index on <b>(tenant_id, created_at DESC)</b>: equality column first, '
        u'then the range and sort column, so the seek lands on the tenant and reads the range in '
        u'order with no sort step. If the list view needs status and total, I would include them '
        u'so the scan is index-only. I would not add a separate index per column — that gives '
        u'the planner three weak options instead of one good one.']),
)

book.page(
    qa(u'5', u'Two users buy the last item at the same time. Walk me through it.',
       [u'The bug is a lost update: both read qty = 1, both write 0, both ship. Three fixes, '
        u'best first. <b>One atomic statement:</b> <b>UPDATE stock SET qty = qty - 1 WHERE id = '
        u'? AND qty > 0</b> and treat zero rows affected as sold out. <b>Optimistic:</b> a '
        u'version column and a retry loop. <b>Pessimistic:</b> <b>SELECT … FOR UPDATE</b> and a '
        u'short transaction. Which I pick depends on contention: for one hot SKU in a flash sale '
        u'I would serialise per item rather than let thousands of retries thrash.']),
    qa(u'6', u'What does READ COMMITTED still allow?',
       [u'Non-repeatable reads (the same row changes inside your transaction), phantoms (new '
        u'rows appear in a range you already read) and lost updates from read-modify-write '
        u'pairs. It is the Postgres default, so those anomalies are the normal state of most '
        u'production systems — you handle them per operation with atomic statements, version '
        u'checks, row locks or a stronger level on the transactions that need it.'],
       [('', u'Follow-up trap:', u'“so use SERIALIZABLE everywhere?” — no. It converts '
                                 u'contention into aborts, so it needs a retry path and it '
                                 u'costs throughput. Use it where the invariant is worth it.')]),
    qa(u'7', u'What is write skew and how is it different from a lost update?',
       [u'A lost update is two transactions writing the <i>same</i> row. Write skew is two '
        u'transactions reading an overlapping set, writing <i>different</i> rows, and together '
        u'breaking an invariant over that set — the classic being two doctors both going off '
        u'call because each saw the other still on. Snapshot isolation does not prevent it, '
        u'because neither transaction touched a row the other wrote. Fix it with a constraint, '
        u'an explicit <b>FOR UPDATE</b> over the set, or SERIALIZABLE.']),
    qa(u'8', u'A user updates their profile and immediately sees the old value. Why?',
       [u'Replica lag: the write went to the primary, the read was routed to a replica that has '
        u'not applied it. Fix with read-your-writes — pin that user’s reads to the primary for a '
        u'few seconds after a write, or pass the write’s log position and require a replica at '
        u'least that fresh. Sticky routing to one replica also gives monotonic reads so the '
        u'value does not flip back and forth.']),
    qa(u'9', u'How do you add a NOT NULL column to a 500-million-row table with no downtime?',
       [u'Expand, dual-write, backfill, contract. Add the column nullable with no default '
        u'rewrite; deploy code that writes both and tolerates either; backfill in throttled, '
        u'resumable batches; then flip reads and add the constraint — in Postgres as <b>NOT '
        u'VALID</b> first and validated afterwards so the table is never exclusively locked, or '
        u'with gh-ost on MySQL. The thing to avoid is a single DDL statement that takes an '
        u'exclusive lock on a hot table at peak.']),
)

book.page(
    qa(u'10', u'How do you paginate a feed of 10 million rows?',
       [u'Keyset pagination on the sort key, not OFFSET. <b>WHERE (created_at, id) < (?, ?) '
        u'ORDER BY created_at DESC, id DESC LIMIT 20</b>, with the cursor returned to the '
        u'client as an opaque token. Constant cost at any depth, and stable when rows are being '
        u'inserted — OFFSET is O(offset) and shows duplicates in a moving list.']),
    qa(u'11', u'What primary key would you use, and why does it matter?',
       [u'UUIDv7 or a Snowflake id for anything distributed: client-generatable, time-ordered so '
        u'B-tree inserts stay local, and sortable by creation. UUIDv4 is fine for low volume but '
        u'its randomness hurts index locality on big tables. Auto-increment is fine on one node '
        u'and bad in a sharded world, because a monotonic key sends every insert to the newest '
        u'shard.']),
    qa(u'12', u'Your app runs out of database connections under load. What is happening?',
       [u'Each connection is a process or thread, so a few thousand of them is a queue, not '
        u'capacity. Usually it is a fleet that grew, a pool with no upper bound or timeout, or '
        u'transactions held open across a slow external call. Put a pooler in front in '
        u'transaction mode, size pools from throughput × latency rather than by hope, give '
        u'checkout a timeout so the app sheds instead of hanging, and stop doing network I/O '
        u'inside a transaction.']),
    qa(u'13', u'When would you deliberately keep two copies of the same data?',
       [u'Whenever the two access patterns are physically incompatible: the transactional row '
        u'store plus a search index, plus a columnar store for analytics. The rules I would '
        u'state are which copy is authoritative, how the others are fed — CDC or an outbox, '
        u'never a best-effort dual write — and what staleness the product accepts. The cost is '
        u'operational: two systems to back up, upgrade and be paged for.']),
    qa(u'14', u'How do you delete a billion rows?',
       [u'Not with one <b>DELETE</b> — that builds a huge transaction, bloats the table, floods '
        u'replication and may lock. If the data is time-shaped, partition by time and '
        u'<b>DROP PARTITION</b>, which is a metadata operation. Otherwise batch it: delete by '
        u'key range in chunks of a few thousand with a pause, watching replica lag, and let the '
        u'reclaim run afterwards. If the table is mostly going away, copy the survivors into a '
        u'new table and swap.']),
)

book.page(
    h2(u'7.4 Red flags interviewers listen for', 'qhead'),
    table([u'Saying this', u'Says this about you'],
          [(u'“I’d use MongoDB because it’s schemaless”',
            u'The schema moved to your code, unenforced'),
           (u'Naming a product before naming the access pattern',
            u'Pattern-matching rather than designing'),
           (u'“Postgres doesn’t scale”',
            u'Has never measured one; conflates read scale with write scale'),
           (u'Adding an index per column',
            u'Has not thought about composite order or write cost'),
           (u'OFFSET pagination on a feed',
            u'Has not run a deep page in production'),
           (u'“Transactions handle that” with no isolation level',
            u'Does not know what the default still allows'),
           (u'Sharding on an auto-increment id or a timestamp',
            u'Has built a write hotspot'),
           (u'Dual-writing to two stores in application code',
            u'No idea how the two diverge, and no repair path'),
           (u'“We’ll add a read replica” for a write bottleneck',
            u'Replicas do not take writes'),
           (u'Analytics queries on the OLTP primary',
            u'Wrong physical layout, and one report can take the site down')],
          [232.0, 290.0]),
    h2(u'7.5 Real systems worth name-dropping'),
    cards(
        ('', u'Amazon Dynamo (2007)',
         [u'Where consistent hashing, quorums, vector clocks and hinted handoff entered '
          u'mainstream design. Cite it for leaderless replication and tunable consistency.']),
        ('', u'Google Spanner',
         [u'External consistency at global scale using TrueTime and Paxos groups. The honest '
          u'counterexample to “CAP means you cannot have both” — you pay in hardware and '
          u'latency.']),
    ),
    cards(
        ('', u'Facebook TAO / MyRocks',
         [u'A graph-shaped cache over MySQL, and later an LSM engine under it. Cite it for '
          u'“the access pattern chose the engine”.']),
        ('', u'Uber’s Postgres → MySQL write-up',
         [u'A widely read account of write amplification, replication and connection handling '
          u'deciding an engine choice. Good for showing you read post-mortems, not just docs.']),
    ),
)

# ---- cheat sheet ----
book.page(
    u'<span class="chip rev">R E V I S I O N</span>'
    u'<h1 class="big">One-page cheat sheet</h1>'
    + p(u'The night-before page. Numbers first, because they end arguments.', 'sub')
    + u'<hr class="thin">',
    h2(u'The numbers'),
    formula(u'one primary ~ 5–10k writes/s &nbsp;·&nbsp; indexed read ~ 5–10 ms '
            u'&nbsp;·&nbsp; fsync ~ 0.1–1 ms',
            u'RAM is ~100,000× faster than disk, a local round trip is 0.5 ms and a '
            u'cross-region one is 80–100 ms. Those three facts explain caching, replicas and '
            u'why you do not call across regions on the hot path.'),
    h2(u'The decisions'),
    table([u'Question', u'Default answer'],
          [(u'Which store?', u'Start relational; move only when a named pattern forces it'),
           (u'Engine?', u'Read-heavy with ranges → B-tree. Write-heavy and append-shaped → LSM'),
           (u'Index?', u'One composite: equality columns first, then the range/sort column'),
           (u'Primary key?', u'UUIDv7 or Snowflake — time-ordered, client-generatable'),
           (u'Isolation?', u'READ COMMITTED plus per-operation protection; SERIALIZABLE where '
                           u'the invariant is worth the retries'),
           (u'Decrement a counter?', u'One conditional UPDATE, not read-modify-write'),
           (u'Pagination?', u'Keyset with an opaque cursor. Never deep OFFSET'),
           (u'Schema change?', u'Expand → dual-write → backfill → contract'),
           (u'Analytics?', u'Off the primary: CDC into a columnar store, and state the lag')],
          [148.0, 374.0]),
)

book.page(
    h2(u'The isolation grid', 'qhead'),
    table([u'Level', u'Dirty read', u'Non-repeatable', u'Phantom', u'Lost update / skew'],
          [(u'READ UNCOMMITTED', u'possible', u'possible', u'possible', u'possible'),
           (u'READ COMMITTED', u'no', u'possible', u'possible', u'possible'),
           (u'REPEATABLE READ / snapshot', u'no', u'no', u'engine-dependent',
            u'write skew possible'),
           (u'SERIALIZABLE', u'no', u'no', u'no', u'no — pay in aborts')],
          [156.0, 84.0, 96.0, 90.0, 96.0]),
    h2(u'Databases in eight facts'),
    facts([
        (u'Access pattern picks the store',
         u'Ratio, shape, size, consistency. Name those four and the product is nearly decided.'),
        (u'Writes go through one primary',
         u'Until you shard. Replicas add read capacity and lag, never write capacity.'),
        (u'An index is a sorted copy',
         u'So writes maintain it, and only prefixes of its sort order can be searched.'),
        (u'The default level is weak',
         u'READ COMMITTED allows lost updates. Protect the operation, not the whole system.'),
        (u'One statement beats read-modify-write',
         u'Conditional UPDATE, INSERT … ON CONFLICT, or a constraint — let the engine be atomic.'),
        (u'Monotonic keys are a hotspot',
         u'Great for a local B-tree, terrible for a sharded cluster. Hash or prefix them.'),
        (u'Deletes are writes',
         u'Tombstones and dead versions cost reads until compaction or VACUUM catches up.'),
        (u'Migrations are four steps',
         u'Expand, dual-write, backfill, contract — each one reversible on its own.'),
    ], tone='acc'),
)

book.page(
    closing(u'IF YOU SAY NOTHING ELSE, SAY THIS',
            u'“I choose a store from the access pattern, not the brand: the read:write ratio, '
            u'the query shape, the size and the consistency each operation actually needs. I '
            u'start relational because it enforces invariants for me, I scale reads with a '
            u'cache and replicas, and I only give up joins and single-node transactions when a '
            u'named write-rate or data-size limit forces me to. Whatever I pick, I can tell you '
            u'what it writes to disk, what it locks, and what it silently allows.”'),
    p(u'<b>Sources &amp; further reading</b> — Martin Kleppmann, <i>Designing Data-Intensive '
      u'Applications</i> (chapters 3, 5, 7 in particular); the PostgreSQL documentation on '
      u'MVCC, isolation levels and index types; <i>Use The Index, Luke!</i> by Markus Winand '
      u'for composite indexes and pagination; the Dynamo (SOSP 2007) and Spanner (OSDI 2012) '
      u'papers; Facebook’s TAO and MyRocks papers; RocksDB and Cassandra documentation on '
      u'compaction strategies and tombstones; gh-ost and pt-online-schema-change docs; '
      u'Brandur Leach’s writing on Postgres operations; AWS documentation on DynamoDB '
      u'single-table design and GSIs.', 'src'),
)

book.write('v_databases.html')
