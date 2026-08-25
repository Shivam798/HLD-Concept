# -*- coding: utf-8 -*-
"""Volume: Replication, Consistency & Consensus."""
from kit import (Book, cover, toc, qa, facts, table, cards, callout, formula, closing,
                 part, fig, kv, bullets, strip, codebox, codes, p, h2, h3, cd, STAR)
import figs_repl as F

THEME = dict(
    bgimg=(u'radial-gradient(52% 37% at 90% 7%, rgba(255,205,150,.26) 0%, '
           u'rgba(255,205,150,.06) 58%, rgba(255,205,150,0) 72%),'
           u'radial-gradient(34% 24% at 2% 99%, rgba(255,170,110,.28) 0%, '
           u'rgba(255,170,110,.06) 62%, rgba(255,170,110,0) 74%),'
           u'linear-gradient(157deg,#14100e 0%,#1f1813 20%,#33241a 38%,#4a3222 56%,'
           u'#64432a 72%,#8a5a32 88%,#b8793a 100%)'),
    hi=u'#ffc98a', eye=u'#e8bd93', ledec=u'#e8ddd0', cardp=u'#ddd0c2', metac=u'#bfae9c',
    barg=u'linear-gradient(90deg,#ffc98a 0%,#d9705a 100%)',
    acc=u'#a85a06', acctint=u'#fdf1de', qn=u'#f0b071',
)
EYEBROW = (u'S Y S T E M &nbsp;D E S I G N &nbsp; / &nbsp; '
           u'I N T E R V I E W &nbsp;P L A Y B O O K')

book = Book(u'The Complete Guide to Replication & Consistency', THEME)

# ═════════════════════════════════════════════════════════ front matter
book.raw(cover(
    THEME, EYEBROW,
    u'The Complete Guide<br>to <span class="hi">Replication</span>',
    u'Copies of data, and the honest cost of each one: CAP and PACELC without the folklore, '
    u'replication topologies, quorums, consensus, clocks, and what multi-region actually '
    u'promises.',
    [(u'Consistency, per operation',
      u'Linearizable to eventual as a ladder — and the sentence that stops the CAP argument.'),
     (u'Topologies and their failures',
      u'Single-leader, multi-leader, leaderless; lag, failover, split brain and fencing.'),
     (u'Quorums and repair',
      u'W + R > N, sloppy quorums, hinted handoff, read repair, Merkle anti-entropy.'),
     (u'Consensus and clocks',
      u'Raft in one page, 2f+1, what a majority costs, and why timestamps are not order.')],
    u'7 parts · 4 diagrams · 14 interview Q&amp;A · one-page cheat sheet',
    u'Revised August 2026'))

book.page(toc(
    u'C O N T E N T S',
    u'What’s inside',
    u'Read it front to back once. Part 1 gives you the language, Part 3 the arithmetic and '
    u'Part 6 the multi-region answer interviewers now expect from senior candidates.',
    [(u'1', u'', u'Consistency, said precisely',
      u'CAP and PACELC properly, the consistency ladder from linearizable to eventual, and '
      u'per-operation guarantees.'),
     (u'2', u'', u'Replication topologies',
      u'Single-leader, multi-leader and leaderless; what gets shipped; sync vs async; lag, '
      u'failover, split brain and fencing.'),
     (u'3', u'', u'Quorums and tunable consistency',
      u'W + R > N, sloppy quorums and hinted handoff, read repair, anti-entropy, and conflict '
      u'resolution when writes collide.'),
     (u'4', u'', u'Consensus',
      u'Why you need it, Raft in one page, 2f+1, what a majority costs, and the systems that '
      u'give it to you.'),
     (u'5', u'', u'Time, order and clocks',
      u'Clock skew, wall vs monotonic, Lamport and hybrid logical clocks, TrueTime, and why a '
      u'timestamp is not an ordering.'),
     (u'6', u'', u'Multi-region',
      u'Active–passive vs active–active, the 80 ms tax, data residency, RPO and RTO, and '
      u'failover you have actually rehearsed.'),
     (u'7', u'', u'The interview itself',
      u'How to answer a consistency question, 14 asked-in-real-interviews Q&amp;A, and the red '
      u'flags to avoid.'),
     (STAR, u'star', u'One-page cheat sheet',
      u'The night-before page: the ladder, the quorum arithmetic, the numbers, eight facts.')],
    u'<b>Part of the HLD concept series.</b> Sharding (splitting data), databases (the engine) '
    u'and messaging (moving events) are separate volumes; this one is only about copies and '
    u'agreement.'))

book.page(
    h2(u'How to use this guide', 'qhead'),
    cards(
        ('', u'Understand',
         [u'Each mechanism gets the plain-English version, then the failure it exists to '
          u'survive.']),
        ('', u'Say out loud',
         [u'The grey “interview line” boxes are the sentences that end a CAP argument instead '
          u'of starting one.']),
        ('', u'Defend',
         [u'Every guarantee has a latency price. Interviewers score whether you named it.']),
    ),
    callout(u'THE WORDS PEOPLE MISUSE',
            [u'<b>Replication</b> makes copies for availability and read capacity. '
             u'<b>Sharding</b> splits data for write capacity. <b>Consensus</b> gets several '
             u'machines to agree on one value. <b>Consistency</b> in CAP means linearizability, '
             u'and consistency in ACID means “your invariants hold” — they are different words '
             u'wearing the same clothes, and saying so is worth a point on its own.'],
            'blue'),
    callout(u'THE ONE THING TO INTERNALISE',
            [u'Every consistency guarantee is bought with <b>coordination</b>, and coordination '
             u'is paid for in <b>latency and availability</b>. So the design question is never '
             u'“strong or eventual?” — it is <b>“which operations are worth a round trip, and '
             u'which are not?”</b>'],
            'teal'),
)

# ═════════════════════════════════════════════════════════ Part 1
book.page(
    part(u'Consistency, said precisely', u'PART 1',
         u'Most candidates can recite CAP and almost none can use it. The fix is to stop '
         u'treating consistency as a system-wide setting and start treating it as a property of '
         u'each operation.'),
    h2(u'1.1 CAP, said correctly'),
    p(u'CAP is about behaviour <b>during a network partition</b>: when nodes cannot talk, you '
      u'either refuse the request (choose consistency) or answer possibly-stale (choose '
      u'availability). It is not a general classification of databases, and “we are a CP '
      u'system” as a blanket statement is the tell that someone learned it from a slide.'),
    p(u'<b>PACELC is the better frame:</b> <i>if there is a Partition, choose A or C; Else, '
      u'choose Latency or Consistency.</i> That second half is the everyday trade-off — '
      u'partitions are rare, but the choice between waiting for a quorum and answering from the '
      u'nearest replica is made on every single request.'),
    h2(u'1.2 The ladder'),
    fig(u'1.1', F.fig_ladder(),
        u'The consistency ladder. Every step down removes a round trip and adds a class of '
        u'surprise you must design around.'),
)

book.page(
    h2(u'1.3 The session guarantees that users actually notice', 'qhead'),
    p(u'Users do not experience linearizability; they experience their own edit disappearing. '
      u'Three cheap guarantees fix almost every user-visible anomaly without global '
      u'coordination:'),
    kv([(u'Read-your-writes',
         u'After I write, I see it. Pin my reads to the primary for a few seconds, or require '
         u'a replica at least as fresh as my write’s log position.'),
        (u'Monotonic reads',
         u'Time never runs backwards for me. Stick a session to one replica so a second read '
         u'cannot land on a staler one.'),
        (u'Consistent prefix',
         u'I never see an answer before its question. Replicate related writes in order, which '
         u'usually means same partition or same stream.'),
        (u'Causal consistency',
         u'The general version of the above: writes that depend on each other are seen in '
         u'order. Implemented with logical clocks or dependency tracking.')]),
    callout(u'INTERVIEW LINE',
            [u'“Different operations in this system deserve different guarantees. The payment '
             u'and the inventory decrement are linearizable, because getting those wrong costs '
             u'money. The order history is read-your-writes, so a user always sees what they '
             u'just did. The view counter is eventual and I would not spend a round trip on '
             u'it.”'],
            'teal'),
    h2(u'1.4 What “strong consistency” costs, in numbers'),
    formula(u'same-datacenter quorum ~ 1–2 ms  ·  cross-AZ ~ 1–3 ms  ·  cross-region '
            u'~ 80–100 ms',
            u'A linearizable write inside one region is affordable. The same write coordinated '
            u'across continents turns a 5 ms API into a 200 ms API — which is why global '
            u'systems keep writes regional and replicate asynchronously.'),
)

# ═════════════════════════════════════════════════════════ Part 2
book.page(
    part(u'Replication topologies', u'PART 2',
         u'Three shapes, and each one is a different answer to “who is allowed to accept a '
         u'write?”. Everything else — lag, conflicts, failover — follows from that.'),
    h2(u'2.1 The three shapes'),
    table([u'Topology', u'How writes work', u'What it buys · what it costs'],
          [(u'Single-leader',
            u'All writes to one node, which ships the change to followers',
            u'No write conflicts, simple reasoning · one write bottleneck, and a failover '
            u'window when the leader dies'),
           (u'Multi-leader',
            u'Several nodes accept writes and replicate to each other',
            u'Local writes in every region, survives a region · conflicts are guaranteed and '
            u'you must resolve them'),
           (u'Leaderless (Dynamo-style)',
            u'The client (or a coordinator) writes to W replicas and reads from R',
            u'No failover at all, tunable per request · read repair, anti-entropy and version '
            u'conflicts become your problem')],
          [116.0, 186.0, 220.0]),
    h2(u'2.2 What actually gets shipped'),
    kv([(u'Statement replication',
         u'Ship the SQL. Cheap and dangerous: NOW(), RAND() and triggers diverge. Largely '
         u'abandoned.'),
        (u'Write-ahead-log / physical',
         u'Ship the byte-level changes. Exact and fast, but the replica must run the same '
         u'engine version — this is Postgres streaming replication.'),
        (u'Logical / row-based',
         u'Ship “row X changed to Y”. Version-tolerant, works across engines, and it is what '
         u'CDC pipelines consume.'),
        (u'Trigger-based',
         u'Application-level, flexible, slow. Only when nothing else can see the change.')]),
    h2(u'2.3 Sync, async, and the honest middle'),
    p(u'<b>Synchronous</b> means the write is not acknowledged until a replica has it: zero '
      u'data loss, and your write latency now includes the slowest replica — plus writes stop '
      u'entirely if that replica is down. <b>Asynchronous</b> acknowledges immediately: fast, '
      u'and a failover can lose the tail. <b>Semi-synchronous</b> is what most production '
      u'systems actually run: one replica synchronous, the rest async, so you can lose a node '
      u'without losing data and without waiting for everybody.'),
)

book.page(
    h2(u'2.4 Replication lag and the three anomalies it causes', 'qhead'),
    cards(
        ('bad', u'“Where did my edit go?”',
         [u'The write went to the leader, the read to a follower. Fix: read-your-writes — pin '
          u'to the leader briefly, or require a replica fresh enough by log position.']),
        ('bad', u'“Time went backwards.”',
         [u'Two reads hit two followers with different lag. Fix: monotonic reads — stick a '
          u'session to one replica.']),
    ),
    p(u'The third is the one people forget: <b>an answer arriving before its question</b>, when '
      u'two related writes replicate through different paths. Keep causally related writes on '
      u'one partition or one stream, and you have consistent prefix reads for free.'),
    h2(u'2.5 Failover, split brain and fencing'),
    p(u'Failover is a sequence, and every step can hurt: detect the leader is gone (too eager '
      u'and you flap, too slow and you are down), choose a new leader (ideally the most '
      u'up-to-date replica), redirect clients, and decide what to do about writes the old '
      u'leader accepted but never replicated.'),
    bullets([
        u'<b>Split brain</b> is two nodes both believing they are the leader — the failure that '
        u'produces silent, permanent divergence.',
        u'<b>Fencing</b> is the fix: a monotonically increasing epoch or term number that '
        u'storage refuses to accept writes below, so a resurrected old leader is rejected '
        u'rather than trusted.',
        u'<b>STONITH / lease-based leadership</b> — the leader holds a time-bounded lease and '
        u'must stop serving when it cannot renew it.',
        u'<b>The data question:</b> under async replication, promoting a replica means '
        u'discarding the old leader’s unreplicated tail. Someone has to decide that '
        u'deliberately; say so.']),
    callout(u'INTERVIEW LINE',
            [u'“Automatic failover with async replication means I am choosing availability over '
             u'those last few writes. I would make that explicit: fence with an epoch number so '
             u'the old primary cannot come back and write, quote an RPO of a few seconds, and '
             u'have a reconciliation path for anything the application cannot lose.”'],
            'teal'),
)

# ═════════════════════════════════════════════════════════ Part 3
book.page(
    part(u'Quorums and tunable consistency', u'PART 3',
         u'The leaderless model turns consistency into arithmetic you can do on a whiteboard, '
         u'which is exactly why interviewers like it.'),
    h2(u'3.1 W + R > N'),
    p(u'With <b>N</b> replicas, a write acknowledged by <b>W</b> of them and a read answered by '
      u'<b>R</b> of them are guaranteed to overlap when <b>W + R > N</b> — so the read sees the '
      u'latest write. Everything else in Dynamo-style tuning is a consequence of choosing '
      u'those three numbers.'),
    fig(u'3.1', F.fig_quorum(),
        u'Quorum overlap with N = 3. The arithmetic is the guarantee; the settings are the '
        u'dial.'),
)

book.page(
    h2(u'3.2 What breaks quorums, and the repairs', 'qhead'),
    kv([(u'Sloppy quorum',
         u'When the “right” replicas are unreachable, write to any W healthy nodes instead. '
         u'Availability up, and the data is now in the wrong place.'),
        (u'Hinted handoff',
         u'Those stand-in nodes hold a hint and forward the data when the real owner returns. '
         u'This is what makes sloppy quorums safe rather than lossy.'),
        (u'Read repair',
         u'A read that sees disagreement writes the newest value back to the stale replica. '
         u'Repair paid for by traffic — so cold data never gets fixed this way.'),
        (u'Anti-entropy',
         u'A background job compares Merkle trees of key ranges and syncs the differences. '
         u'This is what repairs the data nobody reads.')]),
    h2(u'3.3 When writes collide'),
    table([u'Resolution', u'How it decides', u'When it is acceptable'],
          [(u'Last write wins (LWW)',
            u'Highest timestamp survives; the other is discarded',
            u'Only when losing a write is genuinely fine — and remember clock skew decides the '
            u'winner'),
           (u'Vector clocks / version vectors',
            u'Detects that two versions are siblings rather than ordered',
            u'When the application can merge, or ask the user (the shopping-cart answer)'),
           (u'CRDTs',
            u'A merge function that is commutative, associative and idempotent',
            u'Counters, sets, collaborative text — anything whose merge rule can be fixed in '
            u'advance'),
           (u'Application merge',
            u'Your code reconciles siblings on read',
            u'The general escape hatch: correct, and it is code you must actually write')],
          [138.0, 184.0, 200.0]),
    p(u'The senior framing: <b>“last-write-wins is not conflict resolution, it is conflict '
      u'deletion — so I would only use it where I can name the write I am willing to lose.”</b>',
      'note'),
)

# ═════════════════════════════════════════════════════════ Part 4
book.page(
    part(u'Consensus', u'PART 4',
         u'Consensus is how a group of machines agrees on one value despite failures. You will '
         u'rarely implement it and you are frequently asked to explain it, because everything '
         u'that has a single leader depends on it.'),
    h2(u'4.1 What it is for'),
    bullets([
        u'<b>Electing a leader</b> — and making sure there is only ever one per term.',
        u'<b>Agreeing on a log</b> — an ordered sequence every node replays to reach the same '
        u'state (this is state-machine replication).',
        u'<b>Holding configuration and locks</b> — topology, shard maps, leases; the job etcd, '
        u'ZooKeeper and Consul exist to do.',
        u'<b>Committing transactions across partitions</b> — Spanner, CockroachDB and TiDB run '
        u'a consensus group per shard.']),
    fig(u'4.1', F.fig_raft(),
        u'Raft in one picture: a leader per term, entries committed once a majority has them, '
        u'and a minority that cannot make progress on purpose.'),
)

book.page(
    h2(u'4.2 Raft in one page', 'qhead'),
    strip([(u'1', u'Terms', u'Logical time; every election starts a new one'),
           (u'2', u'Election', u'A candidate needs votes from a majority'),
           (u'3', u'Replication', u'The leader appends and ships entries'),
           (u'4', u'Commit', u'An entry is committed once a majority stores it'),
           (u'5', u'Apply', u'Each node applies committed entries in order')]),
    p(u'Two properties make it safe: a candidate can only win with a majority (so two leaders '
      u'in one term are impossible), and a voter refuses a candidate whose log is behind its own '
      u'(so a committed entry can never be overwritten). Membership changes go through the same '
      u'log — joint consensus — which is why adding a node is a committed entry, not a config '
      u'file edit.'),
    h2(u'4.3 The arithmetic and the cost'),
    formula(u'survive f failures with 2f + 1 nodes  ·  3 nodes tolerate 1  ·  5 tolerate 2',
            u'Every commit costs a round trip to a majority, so latency is the median replica, '
            u'not the fastest. Bigger groups survive more and commit slower — which is why '
            u'production clusters are three or five, never nine.'),
    kv([(u'Paxos / Multi-Paxos',
         u'The original. Same guarantees, famously harder to describe — say “Raft is Paxos made '
         u'teachable” and move on.'),
        (u'ZAB',
         u'ZooKeeper’s protocol: atomic broadcast with a leader, tuned for configuration '
         u'workloads.'),
        (u'Kafka KRaft',
         u'Kafka’s own Raft implementation for metadata, which is why it no longer needs '
         u'ZooKeeper.'),
        (u'The honest limitation',
         u'Consensus gives you agreement, not throughput. It is for metadata and leadership — '
         u'do not put every user write through one Raft group.')]),
)

# ═════════════════════════════════════════════════════════ Part 5
book.page(
    part(u'Time, order and clocks', u'PART 5',
         u'Half of the hard bugs in replicated systems are someone trusting a timestamp. This '
         u'part is the vocabulary to avoid that, and it is a reliable senior differentiator.'),
    h2(u'5.1 Why wall-clock time lies'),
    bullets([
        u'<b>Skew:</b> NTP-synced machines are typically within a few milliseconds, but '
        u'hundreds of milliseconds happen — and a virtual machine can pause for seconds.',
        u'<b>Steps:</b> a clock can jump backwards when it is corrected, so “later” timestamps '
        u'can be produced before earlier ones. Use a monotonic clock for durations, never the '
        u'wall clock.',
        u'<b>Leap seconds and VM pauses:</b> the classic sources of a lease you think you hold '
        u'and no longer do.',
        u'<b>The consequence:</b> ordering by timestamp is a heuristic. Under LWW conflict '
        u'resolution, clock skew silently decides which write survives.']),
    h2(u'5.2 Logical clocks'),
    table([u'Clock', u'What it tells you', u'Cost'],
          [(u'Lamport clock', u'A total order consistent with causality',
            u'Cannot distinguish concurrent from ordered'),
           (u'Vector clock', u'Whether two events are causally ordered or concurrent',
            u'Size grows with the number of writers'),
           (u'Hybrid logical clock (HLC)',
            u'Causality plus a timestamp close to real time — the modern default in '
            u'CockroachDB and YugabyteDB',
            u'Still bounded by clock skew, but degrades safely'),
           (u'TrueTime (Spanner)',
            u'An interval with a bounded error, backed by GPS and atomic clocks',
            u'Commit waits out the uncertainty window — correctness bought with hardware')],
          [136.0, 216.0, 170.0]),
    callout(u'THE SENTENCE THAT SCORES',
            [u'“I would not order events by wall-clock timestamp across machines. For causality '
             u'I would use a logical clock, and if I need last-write-wins I would say out loud '
             u'that clock skew is choosing the winner — which is only acceptable where losing '
             u'that write is acceptable.”'],
            'purple'),
)

# ═════════════════════════════════════════════════════════ Part 6
book.page(
    part(u'Multi-region', u'PART 6 · THE 2026 EXPECTATION',
         u'Interviewers now expect a senior candidate to reason about regions unprompted: where '
         u'writes land, what replicates, what a failover loses, and where the data is legally '
         u'allowed to live.'),
    h2(u'6.1 The three shapes'),
    fig(u'6.1', F.fig_region(),
        u'Three multi-region shapes. The cross-region round trip is the number that decides '
        u'between them.'),
    h2(u'6.2 Say it as a table, per data class'),
    table([u'Data', u'Where it is written', u'How it replicates'],
          [(u'Payments, ledger', u'One home region per account',
            u'Synchronous within the region, async across — never a cross-region write on the '
            u'hot path'),
           (u'User profile, settings', u'Home region of the user',
            u'Async global copies; read locally, accept seconds of staleness'),
           (u'Session, cache', u'Local region only',
            u'Not replicated at all. Rebuild on failover; that is what a cache is for'),
           (u'Catalogue, config', u'One writer, global read',
            u'Async fan-out to every region; it changes rarely and is read constantly')],
          [130.0, 156.0, 236.0]),
)

book.page(
    h2(u'6.3 RPO, RTO, and rehearsing the failover', 'qhead'),
    kv([(u'RPO — recovery point',
         u'How much data you accept losing. Async cross-region replication makes this “the '
         u'unreplicated tail”, usually seconds.'),
        (u'RTO — recovery time',
         u'How long until you serve again. DNS or global load-balancer switching plus a '
         u'promotion: minutes if rehearsed, hours if not.'),
        (u'The drill',
         u'A failover plan that has never been executed is a document, not a capability. '
         u'Saying you would run game days is a cheap, credible point.'),
        (u'The asymmetry',
         u'Failing over is the easy half. Failing <i>back</i> — reconciling writes taken while '
         u'the primary was away — is the part teams forget.')]),
    h2(u'6.4 Data residency, in one paragraph'),
    p(u'Some data may not leave a jurisdiction. That turns into a sharding-and-replication rule: '
      u'the user’s home region is part of their identity, personal fields never replicate out, '
      u'and derived or anonymised data is what travels. It is worth one sentence in any design '
      u'with European or Indian users, and it is often the real reason a system is '
      u'geo-partitioned rather than globally replicated.'),
    h2(u'6.5 What “eventually consistent” must mean in practice'),
    bullets([
        u'<b>A bound:</b> “replicas converge within a second under normal conditions” — and an '
        u'alert when lag exceeds it.',
        u'<b>A user-visible story:</b> which screens can be stale, and what the product does '
        u'about it (optimistic UI, “syncing…”, or hiding the operation entirely).',
        u'<b>A repair path:</b> read repair plus anti-entropy, so divergence is corrected '
        u'rather than accumulated.',
        u'<b>A measurement:</b> replication lag as a first-class SLI, per region and per '
        u'partition, because it is the number your failover decision depends on.']),
)

# ═════════════════════════════════════════════════════════ Part 7
book.page(
    part(u'The interview itself', u'PART 7',
         u'Consistency questions are traps for the unprepared because the honest answer is '
         u'always “it depends” — and the score comes from what it depends on.'),
    h2(u'7.1 The four-step answer'),
    strip([(u'1', u'Classify', u'Which operations are money-critical, which are cosmetic'),
           (u'2', u'Choose', u'A guarantee per class, named precisely'),
           (u'3', u'Place', u'Where writes land, what replicates, and how fast'),
           (u'4', u'Fail', u'What a partition or a failover loses, in RPO and RTO')]),
    h2(u'7.2 The five sentences that earn points'),
    bullets([
        u'“CAP only bites during a partition; the everyday trade is PACELC’s second half — '
        u'latency versus consistency.”',
        u'“Different operations deserve different guarantees, so here is my per-operation '
        u'table.”',
        u'“W plus R greater than N gives me overlap; with N=3 I would run W=2, R=2 and survive '
        u'one node.”',
        u'“Last-write-wins deletes a write and lets clock skew choose which one — I would only '
        u'accept that for this field.”',
        u'“Cross-region consensus costs 80 to 100 milliseconds per write, so writes stay '
        u'regional and replicate asynchronously.”']),
    callout(u'INTERVIEW LINE',
            [u'“I would keep the strong guarantees inside one region and one partition, because '
             u'that is where coordination is cheap: a quorum inside a datacentre is a couple of '
             u'milliseconds. Everything global gets asynchronous replication with an explicit '
             u'staleness budget, and the operations that cannot tolerate that are exactly the '
             u'ones I would keep pinned to the user’s home region.”'],
            'teal'),
)

book.page(
    h2(u'7.3 Fourteen questions with model answers', 'qhead'),
    qa(u'1', u'Explain CAP, and then tell me what is wrong with how people use it.',
       [u'During a network partition you can either refuse requests to stay consistent or serve '
        u'possibly-stale data to stay available. What is wrong is treating it as a permanent '
        u'label: partitions are rare, so most of the time you are choosing between latency and '
        u'consistency instead — that is PACELC, and it is the trade you make on every request.']),
    qa(u'2', u'What does W + R > N actually guarantee?',
       [u'That the set of replicas you wrote to and the set you read from must overlap in at '
        u'least one node, so the read sees the latest acknowledged write. With N=3 and W=R=2 you '
        u'get that overlap and you survive one replica being down. It does not give you '
        u'linearizability in general — concurrent writes, sloppy quorums and read repair all '
        u'complicate it — which is a good nuance to volunteer.']),
    qa(u'3', u'A user updates their profile and sees the old value. Diagnose and fix.',
       [u'Replication lag: the write went to the leader and the read to a follower that has not '
        u'applied it. The fix is read-your-writes — route that user’s reads to the leader for a '
        u'few seconds, or carry the write’s log position and require a replica at least that '
        u'fresh. Add sticky routing for monotonic reads so the value cannot flip back and '
        u'forth.']),
    qa(u'4', u'Sync or async replication — which do you choose?',
       [u'Semi-synchronous in almost every case: one replica acknowledges synchronously so a '
        u'single node failure loses nothing, and the rest follow asynchronously so the write '
        u'does not wait for the slowest. Fully synchronous means a slow replica becomes your '
        u'write latency and a dead replica blocks writes; fully async means a failover discards '
        u'the tail. I would state the RPO either way.']),
)

book.page(
    qa(u'5', u'How does leader election work, and what is split brain?',
       [u'A consensus protocol — Raft or similar — has candidates request votes for a new term '
        u'and requires a majority, which makes two leaders in one term impossible. Split brain '
        u'is when that guarantee is missing or ignored and two nodes both act as leader, so '
        u'writes diverge permanently. The defence is fencing: a monotonic epoch or term number '
        u'that storage checks, so a returning old leader is rejected instead of trusted.']),
    qa(u'6', u'Why not use consensus for everything?',
       [u'Because every committed write pays a round trip to a majority, and a minority '
        u'partition cannot make progress at all. That is the right trade for metadata, '
        u'leadership and configuration, and the wrong one for a high-volume data path. Systems '
        u'that do use it for data — Spanner, CockroachDB — run one consensus group per shard, '
        u'and they still keep the group inside a region wherever possible.']),
    qa(u'7', u'Two regions accepted conflicting writes. What now?',
       [u'First, note that active–active everywhere makes this inevitable, so it must be a '
        u'design decision rather than a surprise. Then pick the resolution honestly: '
        u'last-write-wins if I can name the write I am willing to lose; version vectors if the '
        u'application can merge or ask the user; a CRDT if the merge rule can be fixed in '
        u'advance. Or avoid it entirely by partitioning ownership so each key has exactly one '
        u'writing region.']),
    qa(u'8', u'Is “eventually consistent” an acceptable answer?',
       [u'Only with three things attached: a bound (“converges within a second, alerting above '
        u'five”), a user-visible story for what can be stale, and a repair path — read repair '
        u'plus anti-entropy — so divergence is corrected rather than accumulated. Without those '
        u'it is a way of saying “I have not thought about it”.']),
    qa(u'9', u'How do you detect and repair divergence between replicas?',
       [u'Two mechanisms working together. Read repair fixes what traffic touches: a read that '
        u'sees disagreement writes the newest value back. Anti-entropy fixes what nobody reads: '
        u'a background job compares Merkle trees of key ranges and syncs only the ranges whose '
        u'hashes differ, which is log(n) messages rather than a full comparison.']),
)

book.page(
    qa(u'10', u'Design the consistency model for a payment system.',
       [u'Linearizable where money moves: the ledger write and the balance check go through one '
        u'partition with a real transaction, and idempotency keys make retries safe. '
        u'Read-your-writes for the user’s own transaction list. Eventual for aggregates and '
        u'dashboards. Cross-region, the account has a home region and writes never leave it — I '
        u'would rather fail a write over than take an 80 ms coordination penalty or risk a '
        u'conflicting balance.']),
    qa(u'11', u'Why can’t you order events by timestamp across machines?',
       [u'Because clocks disagree — a few milliseconds normally, far more after a VM pause or a '
        u'correction — and they can even step backwards, so a “later” event can carry an earlier '
        u'timestamp. For causality use logical clocks: Lamport for a consistent total order, '
        u'vector clocks to detect concurrency, hybrid logical clocks if you also want the value '
        u'to look like a real time. Spanner solves it with TrueTime and pays for it in '
        u'hardware.']),
    qa(u'12', u'How many nodes in a consensus cluster, and why?',
       [u'Three or five. You need 2f+1 to survive f failures, so three tolerates one and five '
        u'tolerates two. Beyond that every commit gets slower because a majority is larger, '
        u'while the marginal availability gain is tiny. Even numbers buy nothing — four nodes '
        u'still only tolerate one failure and make quorums bigger.']),
    qa(u'13', u'Walk me through a region failover.',
       [u'Detect with a health signal that is not the failing region’s own; shift traffic at DNS '
        u'or the global load balancer; promote the replica database with a fence so the old '
        u'primary cannot write; accept and record the RPO — the writes that never replicated; '
        u'and expect a cold cache, so ramp traffic rather than shifting all of it at once. Then '
        u'the hard part, which is failing back and reconciling what happened while the primary '
        u'was away.']),
    qa(u'14', u'What is the difference between ACID consistency and CAP consistency?',
       [u'ACID’s C means your declared invariants hold after a transaction — it is about '
        u'constraints. CAP’s C means linearizability: every read sees the latest write, as if '
        u'there were one copy. A single Postgres node gives you ACID consistency and, being one '
        u'copy, trivially the CAP kind too; a replicated eventually-consistent store can be '
        u'fully ACID per node and not linearizable across the cluster.']),
)

book.page(
    h2(u'7.4 Red flags interviewers listen for', 'qhead'),
    table([u'Saying this', u'Says this about you'],
          [(u'“We’re a CP system” as a general property',
            u'Learned CAP from a slide; it only applies during a partition'),
           (u'“Strong consistency everywhere”',
            u'Has not priced a cross-region round trip'),
           (u'“Eventually consistent” with no bound or repair path',
            u'A way of saying “I have not thought about it”'),
           (u'Last-write-wins presented as conflict resolution',
            u'It deletes a write, and clock skew picks the loser'),
           (u'Ordering distributed events by wall-clock timestamp',
            u'Has not met clock skew'),
           (u'Automatic failover with no fencing',
            u'Split brain and permanent divergence'),
           (u'“Add a replica” to fix a write bottleneck',
            u'Replicas do not take writes'),
           (u'A consensus group on the user write path',
            u'Correct and slow; consensus is for metadata and leadership'),
           (u'Active–active without naming conflict resolution',
            u'Conflicts are guaranteed, not possible'),
           (u'No RPO/RTO numbers in a failover answer',
            u'Has never been on call for one')],
          [232.0, 290.0]),
    h2(u'7.5 Real systems worth name-dropping'),
    cards(
        ('', u'Amazon Dynamo (2007)',
         [u'Leaderless replication, W/R/N tuning, sloppy quorums, hinted handoff, vector clocks '
          u'and Merkle repair. Every quorum answer traces back to this paper.']),
        ('', u'Google Spanner (2012)',
         [u'External consistency at global scale with TrueTime and Paxos groups. The honest '
          u'counterexample to “you cannot have both” — paid for in hardware and commit waits.']),
    ),
    cards(
        ('', u'Raft (Ongaro & Ousterhout, 2014)',
         [u'Consensus written to be understandable, and now the implementation in etcd, Consul, '
          u'TiKV, CockroachDB and Kafka’s KRaft.']),
        ('', u'Jepsen',
         [u'Kyle Kingsbury’s test reports showing real databases violating the guarantees they '
          u'advertised. Citing it signals you distrust marketing claims.']),
    ),
)

# ---- cheat sheet ----
book.page(
    u'<span class="chip rev">R E V I S I O N</span>'
    u'<h1 class="big">One-page cheat sheet</h1>'
    + p(u'The night-before page. The arithmetic and the latencies are what make the answer '
        u'concrete.', 'sub')
    + u'<hr class="thin">',
    h2(u'The numbers'),
    formula(u'quorum in one DC ~ 1–2 ms  ·  cross-AZ ~ 1–3 ms  ·  cross-region ~ 80–100 ms  '
            u'·  2f + 1 to survive f',
            u'W + R > N gives read/write overlap. Three or five nodes in a consensus group. '
            u'Async replication makes RPO “the unreplicated tail”; synchronous makes it zero '
            u'and adds the slowest replica to every write.'),
    h2(u'The decisions'),
    table([u'Question', u'Default answer'],
          [(u'Consistency level?', u'Per operation. Linearizable for money, read-your-writes '
                                   u'for user edits, eventual for counters'),
           (u'Topology?', u'Single-leader inside a region; partitioned ownership across '
                          u'regions'),
           (u'Sync or async?', u'Semi-sync: one synchronous replica, the rest async'),
           (u'N, W, R?', u'N=3, W=2, R=2 — overlap plus one-node tolerance'),
           (u'Conflicts?', u'Avoid by ownership; then CRDT or version vectors; LWW only where '
                           u'a lost write is acceptable'),
           (u'Consensus for what?', u'Leadership, membership, configuration, locks — not the '
                                    u'data path'),
           (u'Cluster size?', u'3 or 5. Never even, never nine'),
           (u'Ordering?', u'Logical clocks, not wall clocks'),
           (u'Failover?', u'Fenced by epoch, rehearsed, with RPO and RTO written down'),
           (u'Multi-region?', u'Writes local, replication async, staleness budget stated')],
          [148.0, 374.0]),
)

book.page(
    h2(u'Replication in eight facts', 'qhead'),
    facts([
        (u'CAP is about partitions only',
         u'The everyday trade is latency versus consistency — PACELC’s second half.'),
        (u'Coordination is the price',
         u'Every guarantee costs a round trip. Keep the expensive ones inside one region.'),
        (u'Replicas add reads, not writes',
         u'A write bottleneck is a sharding problem, never a replica problem.'),
        (u'Lag is a feature you must design for',
         u'Read-your-writes and monotonic reads fix the anomalies users actually notice.'),
        (u'W + R > N is the whole quorum idea',
         u'N=3, W=2, R=2 by default. Anything less is a deliberate weakening.'),
        (u'Failover without fencing is divergence',
         u'An epoch number storage enforces is what stops a returning old leader.'),
        (u'2f + 1 survives f',
         u'Three or five nodes. Consensus is for metadata, not for every write.'),
        (u'Timestamps are not order',
         u'Clock skew decides LWW winners. Use logical clocks for causality.'),
    ], tone='acc'),
    h2(u'The failure modes'),
    table([u'Name', u'Mechanism', u'Primary fix'],
          [(u'Stale read', u'Read hit a lagging replica',
            u'Read-your-writes; freshness requirement by log position'),
           (u'Time travel', u'Two reads, two replicas, different lag',
            u'Sticky session to one replica (monotonic reads)'),
           (u'Split brain', u'Two nodes both believe they lead',
            u'Fencing epoch enforced at the storage layer'),
           (u'Lost tail', u'Async failover discards unreplicated writes',
            u'Semi-sync, or accept and state the RPO'),
           (u'Silent divergence', u'Conflicting writes resolved by LWW',
            u'Version vectors or CRDTs; ownership per key'),
           (u'Repair never runs', u'Read repair only fixes what is read',
            u'Merkle-tree anti-entropy on a schedule')],
          [112.0, 200.0, 210.0]),
)

book.page(
    closing(u'IF YOU SAY NOTHING ELSE, SAY THIS',
            u'“Consistency is bought with coordination, and coordination is paid for in latency '
            u'and availability — so I choose it per operation rather than per system. Money is '
            u'linearizable inside one region and one partition; a user’s own edits are '
            u'read-your-writes; counters are eventual with a stated bound and a repair path. '
            u'Across regions writes stay local and replicate asynchronously, because a '
            u'cross-region round trip is eighty milliseconds I refuse to put on the hot path. '
            u'And failover is fenced, rehearsed, and quoted with an RPO and an RTO.”'),
    p(u'<b>Sources &amp; further reading</b> — Martin Kleppmann, <i>Designing Data-Intensive '
      u'Applications</i>, chapters 5, 7 and 9; DeCandia et al., <i>Dynamo</i> (SOSP 2007); '
      u'Ongaro &amp; Ousterhout, <i>In Search of an Understandable Consensus Algorithm</i> '
      u'(Raft, 2014); Corbett et al., <i>Spanner</i> (OSDI 2012); Daniel Abadi on PACELC; '
      u'Gilbert &amp; Lynch’s CAP proof and Eric Brewer’s <i>CAP Twelve Years Later</i>; Kyle '
      u'Kingsbury’s Jepsen analyses; Kulkarni et al. on hybrid logical clocks; Shapiro et al. on '
      u'CRDTs; the etcd, ZooKeeper and Cassandra documentation on quorums, leases and repair.',
      'src'),
)

book.write('v_replication.html')
