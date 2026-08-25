# -*- coding: utf-8 -*-
"""Volume: the data structures and algorithms that HLD interviews name-drop."""
from kit import (Book, cover, toc, qa, facts, table, cards, callout, formula, closing,
                 part, fig, kv, bullets, strip, codebox, codes, p, h2, h3, cd, STAR)
import figs_ds as F

THEME = dict(
    bgimg=(u'radial-gradient(52% 37% at 90% 7%, rgba(216,180,254,.26) 0%, '
           u'rgba(216,180,254,.07) 58%, rgba(216,180,254,0) 72%),'
           u'radial-gradient(34% 24% at 2% 99%, rgba(240,160,120,.30) 0%, '
           u'rgba(240,160,120,.06) 62%, rgba(240,160,120,0) 74%),'
           u'linear-gradient(157deg,#150c26 0%,#1f1136 20%,#2e1750 38%,#432070 56%,'
           u'#5f2a80 72%,#8a3a7a 88%,#c05f52 100%)'),
    hi=u'#d9b6fe', eye=u'#c2a7ea', ledec=u'#ddd2ee', cardp=u'#d3c8e6', metac=u'#b0a3c6',
    barg=u'linear-gradient(90deg,#d9b6fe 0%,#f0a078 100%)',
    acc=u'#7a2f8f', acctint=u'#f6e9f9', qn=u'#c79bff',
)
EYEBROW = (u'S Y S T E M &nbsp;D E S I G N &nbsp; / &nbsp; '
           u'I N T E R V I E W &nbsp;P L A Y B O O K')

book = Book(u'The Complete Guide to System Design Data Structures', THEME)

# ═════════════════════════════════════════════════════════ front matter
book.raw(cover(
    THEME, EYEBROW,
    u'The Complete Guide<br>to <span class="hi">HLD Data Structures</span>',
    u'Bloom filters, HyperLogLog, count-min sketches, Merkle trees, tries, inverted indexes, '
    u'geohashes, vector clocks and CRDTs — the structures interviewers expect you to name, '
    u'size and defend.',
    [(u'Membership without the data',
      u'Bloom and cuckoo filters: the sizing formula, the false-positive trade, where they '
      u'already run.'),
     (u'Counting at scale',
      u'HyperLogLog for distincts, count-min for frequency, t-digest for the p99 you report.'),
     (u'Finding things fast',
      u'Skip lists, inverted indexes, tries for typeahead, geohash · S2 · quadtree for '
      u'proximity.'),
     (u'Agreeing without a leader',
      u'Merkle trees, vector clocks, CRDTs, SimHash — the structures distributed stores are '
      u'built from.')],
    u'7 parts · 4 diagrams · 14 interview Q&amp;A · one-page cheat sheet',
    u'Revised August 2026'))

book.page(toc(
    u'C O N T E N T S',
    u'What’s inside',
    u'Every structure here exists because exactness was too expensive. Learn each one as a '
    u'trade — what you gave up, what it costs in bytes — and you can pick one under pressure '
    u'rather than recite names.',
    [(u'1', u'', u'Why approximate structures win',
      u'The four questions to ask before choosing one, and the memory-versus-truth trade that '
      u'connects all of them.'),
     (u'2', u'', u'Membership: Bloom and cuckoo filters',
      u'How a Bloom filter works, the sizing formula, false positives, counting and cuckoo '
      u'variants, and the five systems that already use them.'),
     (u'3', u'', u'Cardinality: HyperLogLog and friends',
      u'Counting distinct users in 12 KB, mergeable sketches, MinHash for similarity, and when '
      u'to just use a set.'),
     (u'4', u'', u'Frequency, top-K and percentiles',
      u'Count-min sketch, heavy hitters, reservoir sampling, t-digest and HDR histograms — and '
      u'why you cannot average a p99.'),
     (u'5', u'', u'Finding things: indexes and ordering',
      u'Skip lists, inverted indexes and posting lists, tries and radix trees for autocomplete, '
      u'n-grams for typo tolerance.'),
     (u'6', u'', u'Distributed-systems structures',
      u'Merkle trees, Lamport and vector clocks, CRDTs, SimHash, geospatial indexing, and '
      u'coordination-free IDs.'),
     (u'7', u'', u'The interview itself',
      u'How to introduce a structure without sounding like a flashcard, 14 Q&amp;A, and the red '
      u'flags to avoid.'),
     (STAR, u'star', u'One-page cheat sheet',
      u'The night-before page: the sizing table, the pick-one decision list, eight facts.')],
    u'<b>Part of the HLD concept series.</b> Caching, Redis, databases and sharding are '
    u'separate volumes — the structures here are referenced from all of them.'))

book.page(
    h2(u'How to use this guide', 'qhead'),
    cards(
        ('', u'Understand',
         [u'Each structure gets the mechanism in plain English, then the number that makes it '
          u'worth using.']),
        ('', u'Size it',
         [u'Every entry carries bytes per item or total memory. Quoting the size is what makes '
          u'the mention credible.']),
        ('', u'Place it',
         [u'Each one ends with the real systems that use it, so you can cite rather than '
          u'speculate.']),
    ),
    callout(u'HOW TO INTRODUCE ONE IN AN INTERVIEW',
            [u'Never lead with the name. Lead with the problem, then the structure, then the '
             u'cost: <i>“most of these lookups are for IDs that do not exist, so I would gate '
             u'them with a Bloom filter — about 1.2 GB for a billion IDs at a 1% false-positive '
             u'rate, and false positives only cost me one wasted cache lookup.”</i> Name, '
             u'number, trade-off. In that order, every time.'],
            'blue'),
    callout(u'THE ONE THING TO INTERNALISE',
            [u'All of these structures buy <b>memory or latency</b> by giving up something '
             u'specific: exactness, deletability, or the ability to enumerate what is inside '
             u'them. <b>If you cannot say which of the three you gave up, you have not chosen '
             u'the structure — you have named it.</b>'],
            'teal'),
)

# ═════════════════════════════════════════════════════════ Part 1
book.page(
    part(u'Why approximate structures win', u'PART 1',
         u'A hash set of a billion 16-byte IDs is 16 GB before overhead, and roughly 50–90 GB '
         u'with it. The same question — “have I seen this?” — costs 1.2 GB with a Bloom filter. '
         u'That ratio is the whole reason this volume exists.'),
    h2(u'1.1 The four questions'),
    kv([(u'Can I tolerate a wrong answer, and in which direction?',
         u'A Bloom filter never says “absent” about something present. That asymmetry is '
         u'usually what makes it safe.'),
        (u'Do I need to enumerate, or only to ask?',
         u'Sketches answer questions about a set they cannot list. If you need the members '
         u'back, you need the real data.'),
        (u'Must it merge?',
         u'HLL and count-min merge cleanly, so per-shard sketches roll up. A plain set does '
         u'too, at full cost.'),
        (u'Does anything get deleted?',
         u'Classic Bloom filters cannot delete. Counting Bloom and cuckoo filters can, at '
         u'extra bytes per item.')]),
    h2(u'1.2 The trade-offs, side by side'),
    table([u'Structure', u'Answers', u'Memory', u'Error'],
          [(u'Hash set', u'exact membership, and enumerate', u'~16–90 bytes/item', u'none'),
           (u'Bloom filter', u'probably present / definitely absent', u'~1.2 bytes/item at 1%',
            u'false positives only'),
           (u'Cuckoo filter', u'same, plus delete', u'~1.5 bytes/item at 1%',
            u'false positives only'),
           (u'HyperLogLog', u'how many distinct', u'12 KB total', u'~0.81% standard error'),
           (u'Count-min sketch', u'how often did X occur', u'fixed grid, e.g. 1 MB',
            u'over-counts, never under'),
           (u't-digest', u'percentiles', u'a few KB per stream', u'accurate in the tails'),
           (u'Reservoir sample', u'a uniform sample of a stream', u'k items', u'sampling error')],
          [116.0, 194.0, 116.0, 96.0]),
    p(u'The sentence that ties it together: <b>“I do not need the data, I need an answer about '
      u'the data — so I will pay bytes for the answer instead of storing the set.”</b>', 'note'),
)

# ═════════════════════════════════════════════════════════ Part 2
book.page(
    part(u'Membership: Bloom and cuckoo filters', u'PART 2',
         u'The most name-dropped structure in system design, and the one candidates most often '
         u'get half right. The half that matters is which way the error goes.'),
    h2(u'2.1 The mechanism, in four lines'),
    bullets([
        u'A bit array of <b>m</b> bits, all zero, and <b>k</b> independent hash functions.',
        u'<b>Add:</b> hash the item k ways, set those k bits.',
        u'<b>Query:</b> hash the item k ways. If any bit is 0 it is <b>definitely absent</b>. '
        u'If all are 1 it is <b>probably present</b>.',
        u'<b>Never delete:</b> clearing a bit could erase another item that shares it — which '
        u'is why the classic filter is add-only.']),
    fig(u'2.1', F.fig_bloom(),
        u'One bit array, three hashes, two kinds of answer. The asymmetry — no false negatives '
        u'— is what makes it safe to reject on.'),
)

book.page(
    h2(u'2.2 Sizing it out loud', 'qhead'),
    formula(u'm = -n · ln(p) / (ln 2)<sup>2</sup>  &nbsp;&nbsp;·&nbsp;&nbsp;  k = (m/n) · ln 2',
            u'At a 1% false-positive rate that is ~9.6 bits per item and about 7 hash '
            u'functions, whatever the items are. Ten million items ≈ 12 MB. A billion ≈ 1.2 GB. '
            u'Halving p costs roughly one more byte per item, not double the memory.'),
    table([u'Items', u'p = 1%', u'p = 0.1%', u'Exact hash set (16-byte ids)'],
          [(u'1 million', u'1.2 MB', u'1.8 MB', u'~50–90 MB'),
           (u'100 million', u'120 MB', u'180 MB', u'~5–9 GB'),
           (u'1 billion', u'1.2 GB', u'1.8 GB', u'~50–90 GB')],
          [130.0, 116.0, 116.0, 160.0]),
    h2(u'2.3 The variants worth naming'),
    kv([(u'Counting Bloom filter',
         u'Replace each bit with a 4-bit counter so deletes decrement instead of clearing. '
         u'~4× the memory.'),
        (u'Cuckoo filter',
         u'Stores small fingerprints in a cuckoo hash table: supports delete, better cache '
         u'locality, and beats Bloom below ~3% error. Insertions can fail when it is nearly '
         u'full.'),
        (u'Scalable / layered Bloom',
         u'Chain filters of growing size when you do not know n in advance — the honest answer '
         u'to “what if the set grows?”.'),
        (u'Quotient filter',
         u'Mergeable and resizable, used in some LSM engines. Worth one sentence if the '
         u'interviewer digs.')]),
    h2(u'2.4 Where it already runs'),
    bullets([
        u'<b>Cache penetration gate:</b> hold every valid ID; reject lookups for IDs that '
        u'cannot exist before they touch cache or database.',
        u'<b>LSM storage engines:</b> one filter per SSTable, so a read skips files that '
        u'certainly do not hold the key — this is what makes LSM reads survivable.',
        u'<b>Web crawlers:</b> “have I fetched this URL?” over billions of URLs, where a rare '
        u'false positive means one page skipped.',
        u'<b>Chrome / Safe Browsing and Bigtable:</b> the canonical citations if you want one '
        u'name-drop rather than three.',
        u'<b>Redis:</b> <b>BF.ADD</b> / <b>BF.EXISTS</b> in the Bloom module, so you get it '
        u'without running new infrastructure.']),
)

# ═════════════════════════════════════════════════════════ Part 3
book.page(
    part(u'Cardinality: HyperLogLog and friends', u'PART 3',
         u'“How many unique users watched this video?” asked for every video, every hour, for '
         u'ten years. Exact answers need the set; you almost never need exact.'),
    h2(u'3.1 The mechanism'),
    p(u'Hash each item to a uniformly random bit string and watch for improbable patterns: a '
      u'hash with ten leading zeros turns up about once every 1,024 distinct items, so '
      u'seeing one implies roughly a thousand distinct items. One estimate is far too '
      u'noisy, so the hash is '
      u'split into 16,384 registers, each tracking its own maximum, and the harmonic mean of '
      u'the registers becomes the estimate.'),
    fig(u'3.1', F.fig_hll(),
        u'The two halves of HyperLogLog: an improbability counter, then averaging over thousands '
        u'of independent copies to kill the variance.'),
    p(u'The numbers to quote: <b>12 KB, ~0.81% standard error, unlimited cardinality, and '
      u'unions are free</b> — merging two sketches is the per-register maximum, so daily '
      u'sketches roll into a month and per-shard sketches roll into a global figure.', 'note'),
)

book.page(
    h2(u'3.2 When not to use it', 'qhead'),
    cards(
        ('bad', u'Small cardinalities',
         [u'Below a few thousand items a plain set is smaller <i>and</i> exact. Real '
          u'implementations know this and switch representation (HLL++ uses a sparse encoding '
          u'first) — worth mentioning that the library already handles it.']),
        ('bad', u'When the answer must be exact',
         [u'Billing, compliance, anything a regulator reads. An 0.8% error on a revenue number '
          u'is not a design trade-off, it is a bug.']),
    ),
    h2(u'3.3 MinHash and Jaccard similarity'),
    p(u'Different question, same trick. To estimate how much two sets overlap, keep only the '
      u'smallest k hash values of each set: the fraction of shared minima estimates the Jaccard '
      u'similarity. It is how near-duplicate detection, recommendation candidate generation and '
      u'plagiarism checks work at scale, and it composes with locality-sensitive hashing to find '
      u'similar pairs without comparing every pair.'),
    h2(u'3.4 The family, one line each'),
    table([u'Structure', u'Question it answers', u'The number'],
          [(u'HyperLogLog', u'How many distinct items?', u'12 KB, 0.81% error, mergeable'),
           (u'HLL++', u'Same, accurate on small sets too', u'Sparse below ~thousands, then '
                                                           u'dense'),
           (u'Linear counting', u'Distincts when cardinality is small', u'Simpler, worse at '
                                                                       u'scale'),
           (u'MinHash', u'How similar are two sets?', u'k hashes per set; error falls with k'),
           (u'SimHash', u'Are these two documents near-identical?', u'64-bit fingerprint, '
                                                                    u'Hamming distance'),
           (u'Theta sketch', u'Distincts with set operations (intersections too)',
            u'Bigger than HLL, does more')],
          [116.0, 234.0, 172.0]),
)

# ═════════════════════════════════════════════════════════ Part 4
book.page(
    part(u'Frequency, top-K and percentiles', u'PART 4',
         u'Three questions that look similar and need three different structures: how often did '
         u'this happen, what are the busiest keys, and what is my p99.'),
    h2(u'4.1 Count-min sketch'),
    p(u'A grid of <b>d</b> rows × <b>w</b> counters. To add an event, hash the key once per row '
      u'and increment that row’s counter. To query, take the <b>minimum</b> across the rows — '
      u'collisions can only inflate a counter, so the smallest of d readings is the closest to '
      u'the truth. It never undercounts, which is exactly the guarantee you want when hunting '
      u'abuse or hot keys.'),
    fig(u'4.1', F.fig_cms(),
        u'Count-min sketch: constant memory regardless of how many distinct keys arrive, and an '
        u'error bound you can state.'),
    p(u'Interview framing: <b>“I would find hot keys with a count-min sketch in the proxy — '
      u'fixed memory, no per-key allocation, never undercounts — and keep an exact top-K '
      u'alongside it with Space-Saving.”</b>', 'note'),
)

book.page(
    h2(u'4.2 Top-K without keeping every key', 'qhead'),
    kv([(u'Space-Saving / Misra-Gries',
         u'Keep k counters; a new key evicts the current minimum and inherits its count. '
         u'Finds heavy hitters in one pass, memory O(k).'),
        (u'Count-min + heap',
         u'Sketch for counts, small heap for the current leaders. The standard trending-topics '
         u'design.'),
        (u'Redis in practice',
         u'A sorted set with <b>ZINCRBY</b> when the key space is bounded; <b>TOPK</b> and '
         u'<b>CMS</b> commands from the Bloom module when it is not.'),
        (u'The honest caveat',
         u'Approximate top-K can miss a key that is just below the threshold. Say so — it is '
         u'usually fine for trending, never fine for billing.')]),
    h2(u'4.3 Percentiles, and the mistake everyone makes'),
    callout(u'YOU CANNOT AVERAGE PERCENTILES',
            [u'The mean of ten servers’ p99 values is not the fleet p99. To aggregate you need '
             u'a mergeable summary of the distribution — an HDR histogram (fixed buckets, exact '
             u'within bucket width) or a <b>t-digest</b> (adaptive, far more accurate in the '
             u'tails, and mergeable). Saying this out loud in an observability discussion is a '
             u'reliable senior signal.'],
            ''),
    h2(u'4.4 Reservoir sampling'),
    p(u'To keep k uniformly random items from a stream of unknown length: keep the first k, then '
      u'for item n replace a random one with probability k/n. One pass, O(k) memory, and every '
      u'item equally likely. It is how you sample traces for debugging, or logs for analysis, '
      u'without deciding the sample rate in advance.'),
)

# ═════════════════════════════════════════════════════════ Part 5
book.page(
    part(u'Finding things: indexes and ordering', u'PART 5',
         u'Search, autocomplete and leaderboards are three of the most common design prompts, '
         u'and each one is a structure question wearing a product costume.'),
    h2(u'5.1 Skip list — the sorted structure you already use'),
    p(u'A linked list with extra express lanes: each node appears in higher levels with '
      u'probability one half, so search skips ahead and lands in O(log n). No rebalancing, and range '
      u'scans are a walk along the bottom level. This is what backs a Redis sorted set, which is '
      u'why <b>ZREVRANK</b> can give an exact rank among fifty million players in O(log n) — the '
      u'query SQL cannot do without scanning.'),
    h2(u'5.2 Inverted index — how search actually works'),
    p(u'Documents are tokenised, normalised (lowercase, stem, strip stop words) and stored as a '
      u'map from term to a sorted <b>posting list</b> of document ids. A query intersects the '
      u'posting lists of its terms, then ranks the survivors — classically by BM25, now often '
      u'blended with vector similarity.'),
    kv([(u'Why it is fast', u'Posting lists are sorted and delta-compressed, so intersection is '
                            u'a merge, and skip pointers jump ahead.'),
        (u'Why writes are batched', u'Segments are immutable and merged in the background — '
                                    u'which is why Elasticsearch is near-real-time, not '
                                    u'real-time.'),
        (u'Typo tolerance', u'Character n-grams or edit-distance automata; “fuzzy” is a '
                            u'different index, not a flag on the same one.'),
        (u'The interview point', u'An inverted index is a second copy of your data, so it needs '
                                 u'a feed (CDC or an outbox) and a reindex plan.')]),
    h2(u'5.3 Trie and radix tree — autocomplete'),
    p(u'A prefix tree: each edge a character, so “find everything starting with tes” is a walk '
      u'to that node. A radix tree compresses single-child chains, which is what makes it '
      u'memory-viable. The trick that makes typeahead fast is <b>precomputing the top-K '
      u'completions at every node</b>, so a keystroke is a lookup rather than a subtree scan, '
      u'and the whole structure is rebuilt offline from query logs.'),
)

# ═════════════════════════════════════════════════════════ Part 6
book.page(
    part(u'Distributed-systems structures', u'PART 6',
         u'These are the structures that let independent machines agree, or at least reconcile, '
         u'without a coordinator on the hot path.'),
    h2(u'6.1 Merkle trees'),
    p(u'Hash each block of data, then hash pairs of hashes upward to a single root. Two replicas '
      u'compare roots: equal means identical, different means descend into the differing '
      u'subtree. You find the one bad block in log(n) comparisons instead of streaming '
      u'everything.'),
    fig(u'6.1', F.fig_merkle(),
        u'Anti-entropy repair in three steps. Dynamo-style stores, Git and rsync all lean on '
        u'exactly this property.'),
    h2(u'6.2 Clocks: Lamport, vector, and why timestamps lie'),
    table([u'Mechanism', u'What it gives you', u'What it costs'],
          [(u'Wall clock (LWW)', u'A simple “latest wins” rule',
            u'Clock skew silently discards writes — correct only when you accept losing one'),
           (u'Lamport clock', u'A total order consistent with causality',
            u'Cannot tell concurrent from ordered — one counter, no context'),
           (u'Vector clock', u'Detects concurrency: “these two writes are siblings”',
            u'Size grows with the number of writers; needs pruning'),
           (u'Version vector / dotted', u'The production form used by Dynamo-style stores',
            u'Conflicts are surfaced to the application to resolve')],
          [124.0, 194.0, 204.0]),
)

book.page(
    h2(u'6.3 CRDTs — merging without asking', 'qhead'),
    p(u'A conflict-free replicated data type is a structure whose merge function is '
      u'commutative, associative and idempotent, so replicas that receive the same updates in '
      u'any order converge to the same value. No coordination, no conflicts to resolve, and the '
      u'cost is that the merge rule must be decided in advance — and it is not always the rule '
      u'the product wants.'),
    table([u'Type', u'Merge rule', u'Used for'],
          [(u'G-counter', u'Per-replica counters, sum them', u'Increment-only metrics, likes'),
           (u'PN-counter', u'Two G-counters, subtract', u'Counters that go down too'),
           (u'LWW register', u'Highest timestamp wins', u'Profile fields, settings'),
           (u'OR-set', u'Adds and removes with unique tags', u'Shopping carts, tag sets'),
           (u'RGA / Yjs, Automerge', u'Ordered sequence with unique ids',
            u'Collaborative text editing')],
          [136.0, 190.0, 196.0]),
    h2(u'6.4 Geospatial indexing'),
    kv([(u'Geohash', u'Interleave latitude and longitude bits into a string, so a shared prefix '
                     u'means physical proximity. Simple, sortable, and it has edge cases at '
                     u'cell boundaries.'),
        (u'S2 / H3', u'Google’s spherical cells and Uber’s hexagons: uniform cell areas, '
                     u'hierarchical, and no boundary pathologies. The modern answer.'),
        (u'Quadtree', u'Recursively split space until each cell holds few points — good for '
                      u'skewed density, and it is the classic interview answer for “find '
                      u'nearby drivers”.'),
        (u'R-tree / PostGIS', u'Bounding-box index for shapes and polygons, not just points. '
                              u'What a real GIS database uses.')]),
    h2(u'6.5 Coordination-free IDs'),
    p(u'Snowflake: 41 bits of millisecond timestamp, 10 bits of machine id, 12 bits of '
      u'sequence — 4,096 ids per millisecond per machine, sortable by time, no coordination on '
      u'the write path. UUIDv7 is the same idea in the UUID format. Both exist because '
      u'auto-increment needs a single authority, and a single authority does not shard.'),
)

# ═════════════════════════════════════════════════════════ Part 7
book.page(
    part(u'The interview itself', u'PART 7',
         u'These structures are worth points only when they arrive as answers to a problem you '
         u'have already stated. Named unprompted, they read as flashcards.'),
    h2(u'7.1 The three-beat mention'),
    strip([(u'1', u'The problem', u'“Most of these lookups are for IDs that never existed”'),
           (u'2', u'The structure', u'“A Bloom filter in front of the cache”'),
           (u'3', u'The number', u'“1.2 GB for a billion IDs at 1%, and a false positive '
                                 u'costs one wasted lookup”')]),
    h2(u'7.2 Matching problem to structure'),
    table([u'When you hear', u'Reach for', u'Because'],
          [(u'“Has this URL been crawled?”', u'Bloom filter',
            u'Billions of items, and a rare false positive only skips one page'),
           (u'“How many unique viewers?”', u'HyperLogLog',
            u'12 KB per counter and the sketches merge across shards and days'),
           (u'“Which keys are hot right now?”', u'Count-min + Space-Saving',
            u'Fixed memory at millions of events a second, never undercounts'),
           (u'“Show the p99 across the fleet”', u't-digest / HDR histogram',
            u'Percentiles do not average; distributions merge'),
           (u'“Rank among 50 million players”', u'Skip list (sorted set)',
            u'O(log n) exact rank, which SQL cannot do without a scan'),
           (u'“Search these documents”', u'Inverted index',
            u'Term → posting list intersection, then ranking'),
           (u'“Autocomplete as I type”', u'Trie with precomputed top-K',
            u'A keystroke becomes a lookup instead of a scan'),
           (u'“Find drivers near me”', u'S2 / H3 / quadtree',
            u'Proximity needs spatial locality in the key itself'),
           (u'“Do these replicas match?”', u'Merkle tree',
            u'log(n) comparisons instead of streaming the data set'),
           (u'“Offline edits must merge”', u'CRDT',
            u'A merge rule that converges without coordination')],
          [148.0, 148.0, 226.0]),
)

book.page(
    h2(u'7.3 Fourteen questions with model answers', 'qhead'),
    qa(u'1', u'Explain a Bloom filter and its failure mode.',
       [u'A bit array plus k hash functions. Adding sets k bits; a query that finds any bit zero '
        u'proves absence, and all-ones means probably present. So the only error is a false '
        u'positive — never a false negative — which is why it is safe to <i>reject</i> on and '
        u'never safe to <i>confirm</i> on. About 9.6 bits per item gives 1%, and the classic '
        u'filter cannot delete because clearing a bit could erase another item.']),
    qa(u'2', u'How big a Bloom filter for a billion IDs, and what does the error cost you?',
       [u'~1.2 GB at 1% false positives, or ~1.8 GB at 0.1%, with about seven hash functions. '
        u'In a cache-penetration gate a false positive means one lookup that would have been '
        u'skipped still happens — a wasted read, not a wrong answer. Compare that with a hash '
        u'set of the same IDs at 50 GB or more.']),
    qa(u'3', u'Count the unique visitors to a billion pages, hourly.',
       [u'One HyperLogLog per page per hour: 12 KB each, ~0.8% error, and unions are the '
        u'per-register maximum so hours roll up into days and shards roll up into a global '
        u'number. I would say explicitly that this is an estimate, and keep an exact count only '
        u'for the handful of pages someone bills against.']),
    qa(u'4', u'Find the top 100 hottest keys in a 5-million-QPS stream.',
       [u'A count-min sketch for frequencies plus Space-Saving for the leaders: fixed memory, no '
        u'per-key allocation, and the sketch never undercounts so a hot key cannot hide. Per '
        u'shard, then merge the sketches. The caveat I would volunteer is that a key just below '
        u'the threshold can be missed, which is fine for hot-key mitigation and not fine for '
        u'billing.']),
)

book.page(
    qa(u'5', u'Why can’t you average p99 across servers?',
       [u'Because a percentile is a property of a distribution, not a number you can mean. Ten '
        u'servers each reporting p99 = 100 ms could have a fleet p99 far higher, depending on '
        u'traffic share and shape. You need mergeable summaries: HDR histograms with fixed '
        u'buckets, or t-digests, which stay accurate in the tails and merge exactly.']),
    qa(u'6', u'Design autocomplete for a search box.',
       [u'A trie or radix tree over the query corpus with the <b>top-K completions '
        u'precomputed at every node</b>, so a keystroke is one lookup. Build it offline from '
        u'query logs, ship it as an immutable artefact, and keep it in memory — it is small '
        u'enough. Add a personalisation pass on top of the shared candidates, cache the prefix '
        u'results, and debounce on the client. Typos are a separate n-gram or edit-distance '
        u'index, not a flag.']),
    qa(u'7', u'How would you detect near-duplicate documents at scale?',
       [u'SimHash or MinHash. SimHash gives each document a 64-bit fingerprint where similar '
        u'documents differ in only a few bits, so “near-duplicate” becomes a Hamming-distance '
        u'lookup. MinHash estimates Jaccard similarity from the smallest k hashes, and with '
        u'locality-sensitive hashing you only compare documents that land in the same bucket — '
        u'that is what makes it linear instead of quadratic.']),
    qa(u'8', u'Two replicas may have diverged. How do you find the difference cheaply?',
       [u'Merkle trees. Each replica hashes its key ranges into a tree; comparing roots is one '
        u'message, and if they differ you descend only into the subtrees that disagree — log(n) '
        u'messages to locate the bad range, then repair just that range. This is anti-entropy in '
        u'Dynamo-style stores, and the same trick Git and rsync use.']),
    qa(u'9', u'What is a vector clock and when would you use one?',
       [u'A per-replica counter set attached to a value, so two versions can be compared: one '
        u'dominates the other, or they are concurrent siblings. You use it when writes can '
        u'happen in more than one place and last-write-wins is not acceptable, because it lets '
        u'you <i>detect</i> the conflict instead of silently dropping a write. The cost is size '
        u'growth with the number of writers and the need to resolve siblings in application '
        u'code.']),
)

book.page(
    qa(u'10', u'When would you use a CRDT instead of a lock?',
       [u'When replicas must accept writes while partitioned and then converge — collaborative '
        u'editing, offline-capable apps, per-region counters. A CRDT’s merge is commutative, '
        u'associative and idempotent, so order does not matter and no coordination is needed. '
        u'The price is that the merge rule is fixed in advance: a G-counter cannot express '
        u'“reject if it would go negative”, so inventory still wants a transaction.']),
    qa(u'11', u'Find all drivers within 2 km. What is the index?',
       [u'Spatial cells: H3 or S2, or a quadtree if density is very uneven. Each driver’s '
        u'position becomes a cell id, drivers are stored by cell, and a proximity query reads '
        u'the covering cell plus its neighbours — because the target can sit near a boundary. '
        u'Geohash works the same way with a string prefix and is fine to name, as long as you '
        u'mention the boundary problem.']),
    qa(u'12', u'How does a Redis sorted set give exact ranks so fast?',
       [u'It is a skip list plus a hash map. The skip list keeps members ordered by score with '
        u'probabilistic express lanes, so insert, delete and rank are O(log n); the hash map '
        u'gives O(1) score lookup by member. That combination is why leaderboards, sliding-'
        u'window rate limiters and priority queues all end up on a sorted set.']),
    qa(u'13', u'Generate unique IDs across 100 servers without coordination.',
       [u'Snowflake: 41 bits of millisecond timestamp, 10 bits of machine id, 12 bits of '
        u'sequence — time-ordered, 8 bytes, and 4,096 per millisecond per machine. UUIDv7 is the '
        u'same shape in UUID clothing. The operational details worth naming are machine-id '
        u'assignment and what you do when the clock steps backwards: refuse to mint rather than '
        u'risk duplicates.']),
    qa(u'14', u'The interviewer asks “why not just use a hash set?”',
       [u'Sometimes that is the right answer, and saying so is a good signal: below a few '
        u'million items, exact and simple beats clever. The switch happens when the set no '
        u'longer fits in memory on one node, or when you need it in a hot path on every server, '
        u'or when it must merge across shards. Then I trade exactness for bytes — and I say '
        u'which direction the error goes.']),
)

book.page(
    h2(u'7.4 Red flags interviewers listen for', 'qhead'),
    table([u'Saying this', u'Says this about you'],
          [(u'“Bloom filter” with no size or error rate',
            u'Name-dropping; the number is the whole point'),
           (u'“Bloom filters can have false negatives”',
            u'Backwards — and it inverts where they are safe to use'),
           (u'Deleting from a classic Bloom filter',
            u'Would corrupt other items; you want counting or cuckoo'),
           (u'HyperLogLog for a number someone bills on',
            u'0.8% error is not a rounding difference to finance'),
           (u'Averaging p99 across instances',
            u'Percentiles do not average; you need mergeable histograms'),
           (u'A sketch where a set of 10,000 would do',
            u'Complexity with no payoff'),
           (u'“Use a trie” with no top-K precomputation',
            u'Then every keystroke scans a subtree'),
           (u'Geohash with no boundary handling',
            u'Nearby points can sit in different cells'),
           (u'Last-write-wins presented as conflict resolution',
            u'It is conflict <i>deletion</i>; say which write you are losing'),
           (u'Naming a structure before naming the problem',
            u'Flashcards, not design')],
          [232.0, 290.0]),
    h2(u'7.5 Real systems worth name-dropping'),
    cards(
        ('', u'Google Bigtable & Chrome',
         [u'Bloom filters per SSTable to skip files on read, and in Chrome’s Safe Browsing to '
          u'check URLs locally before asking the server. The two canonical citations.']),
        ('', u'Redis probabilistic commands',
         [u'PFADD/PFCOUNT for HyperLogLog, BF.* for Bloom, CMS.* and TOPK.* for sketches — '
          u'evidence that these are production tools, not textbook curiosities.']),
    ),
    cards(
        ('', u'Dynamo & Cassandra',
         [u'Merkle-tree anti-entropy, vector clocks for sibling detection, consistent hashing '
          u'for placement. One paper, three structures.']),
        ('', u'Uber H3 · Google S2',
         [u'Hierarchical spatial indexing in the open, and the reason “geohash” is no longer '
          u'the best answer to a proximity question.']),
    ),
)

# ---- cheat sheet ----
book.page(
    u'<span class="chip rev">R E V I S I O N</span>'
    u'<h1 class="big">One-page cheat sheet</h1>'
    + p(u'The night-before page. The numbers are the part that makes a mention credible.', 'sub')
    + u'<hr class="thin">',
    h2(u'The sizes to quote'),
    table([u'Structure', u'Memory', u'Accuracy', u'The one-liner'],
          [(u'Bloom filter', u'~9.6 bits/item at 1%', u'no false negatives',
            u'“probably present, definitely absent”'),
           (u'Cuckoo filter', u'~12 bits/item at 1%', u'no false negatives',
            u'“Bloom, but deletable”'),
           (u'HyperLogLog', u'12 KB fixed', u'~0.81% error',
            u'“count distinct, mergeable, forever”'),
           (u'Count-min sketch', u'grid, e.g. 4×64k', u'never undercounts',
            u'“frequency in fixed memory”'),
           (u'Space-Saving', u'k counters', u'exact for real heavy hitters',
            u'“top-K in one pass”'),
           (u't-digest', u'a few KB', u'accurate in the tails',
            u'“percentiles that merge”'),
           (u'Skip list', u'O(n), ~1.33 pointers/node', u'exact',
            u'“ordered, O(log n) rank”'),
           (u'Merkle tree', u'one hash per block', u'exact',
            u'“diff two replicas in log(n)”')],
          [104.0, 122.0, 132.0, 164.0]),
    h2(u'Pick one in ten seconds'),
    bullets([
        u'<b>Membership at scale</b> → Bloom (or cuckoo if you delete).',
        u'<b>Distinct count</b> → HyperLogLog. <b>Frequency</b> → count-min. '
        u'<b>Top-K</b> → Space-Saving.',
        u'<b>Percentiles</b> → t-digest or HDR histogram, never an average of percentiles.',
        u'<b>Ranking / ordering</b> → skip list. <b>Prefix search</b> → trie with top-K. '
        u'<b>Full text</b> → inverted index.',
        u'<b>Proximity</b> → S2/H3/quadtree. <b>Replica repair</b> → Merkle. '
        u'<b>Concurrent writes</b> → vector clocks, then CRDTs.']),
)

book.page(
    h2(u'Eight facts', 'qhead'),
    facts([
        (u'The error has a direction',
         u'Bloom: false positives only. Count-min: over-counts only. Say which way it is wrong.'),
        (u'Sketches cannot enumerate',
         u'They answer questions about a set they cannot list. Need the members? Keep the data.'),
        (u'Mergeability is the superpower',
         u'HLL, count-min and t-digest merge, so per-shard and per-hour sketches roll up.'),
        (u'Deletion is expensive',
         u'Classic Bloom cannot delete. Counting Bloom pays ~4×; cuckoo pays a little.'),
        (u'12 KB and 0.81%',
         u'The two HyperLogLog numbers. Quote them and the mention becomes credible.'),
        (u'Percentiles never average',
         u'Merge distributions, not summaries. This one is worth a whole sentence out loud.'),
        (u'Precompute at the node',
         u'A trie is only fast for typeahead when each node already knows its top completions.'),
        (u'Merkle turns compare into descend',
         u'Equal roots mean identical data; unequal roots mean one path to walk.'),
    ], tone='acc'),
    h2(u'Where each one already runs'),
    table([u'Structure', u'In production'],
          [(u'Bloom filter', u'LSM engines (per-SSTable), crawlers, Chrome Safe Browsing, '
                             u'Redis BF.*'),
           (u'HyperLogLog', u'Redis PFADD, BigQuery APPROX_COUNT_DISTINCT, Presto, analytics '
                            u'pipelines'),
           (u'Count-min', u'Hot-key detection in proxies, abuse pipelines, Redis CMS.*'),
           (u't-digest', u'Elasticsearch percentiles, Prometheus/HDR-style latency reporting'),
           (u'Skip list', u'Redis sorted sets, LevelDB/RocksDB memtables'),
           (u'Inverted index', u'Elasticsearch/OpenSearch, Lucene, every search box you use'),
           (u'Merkle tree', u'Dynamo, Cassandra, Riak repair; Git; blockchains'),
           (u'CRDT', u'Yjs and Automerge in collaborative editors; Riak data types')],
          [124.0, 398.0]),
)

book.page(
    closing(u'IF YOU SAY NOTHING ELSE, SAY THIS',
            u'“Every one of these structures trades exactness, deletability or enumerability '
            u'for memory. So I name the problem first, then the structure, then the number and '
            u'the direction of the error: a Bloom filter at 9.6 bits an item that can only be '
            u'wrong by saying yes; a HyperLogLog at 12 KB and 0.8%; a count-min sketch that '
            u'never undercounts. If I cannot say what I gave up, I have not chosen the '
            u'structure — I have just named it.”'),
    p(u'<b>Sources &amp; further reading</b> — Bloom (1970), <i>Space/time trade-offs in hash '
      u'coding with allowable errors</i>; Fan et al., <i>Cuckoo Filter</i> (2014); Flajolet et '
      u'al., <i>HyperLogLog</i> (2007) and Heule et al., <i>HyperLogLog in Practice</i> (2013); '
      u'Cormode &amp; Muthukrishnan, <i>Count-Min Sketch</i> (2005); Metwally et al., '
      u'<i>Space-Saving</i> (2005); Dunning &amp; Ertl, <i>t-digest</i>; Broder, <i>MinHash</i> '
      u'and Charikar, <i>SimHash</i>; Pugh, <i>Skip Lists</i> (1990); Shapiro et al., '
      u'<i>Conflict-free Replicated Data Types</i> (2011); DeCandia et al., <i>Dynamo</i> (SOSP '
      u'2007); Google S2 and Uber H3 documentation; the Redis probabilistic module docs; '
      u'Lucene’s index-format documentation.', 'src'),
)

book.write('v_datastructures.html')
