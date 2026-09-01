# -*- coding: utf-8 -*-
"""Volume: Rate Limiting & Throttling."""
from kit import (Book, cover, toc, qa, facts, table, cards, callout, formula, closing,
                 part, fig, kv, bullets, strip, codebox, codes, p, h2, h3, cd, STAR)
import figs_rl as F

THEME = dict(
    bgimg=(u'radial-gradient(52% 37% at 90% 7%, rgba(140,210,255,.30) 0%, '
           u'rgba(140,210,255,.08) 58%, rgba(140,210,255,0) 72%),'
           u'radial-gradient(34% 24% at 2% 99%, rgba(190,170,255,.30) 0%, '
           u'rgba(190,170,255,.06) 62%, rgba(190,170,255,0) 74%),'
           u'linear-gradient(157deg,#080c26 0%,#0e1440 20%,#141f5e 38%,#1a2c7c 56%,'
           u'#213f96 72%,#2a5bb0 88%,#3a86c8 100%)'),
    hi=u'#8ec6ff', eye=u'#93b4ea', ledec=u'#ccd8ee', cardp=u'#c2d0e8', metac=u'#9fb0cd',
    barg=u'linear-gradient(90deg,#8ec6ff 0%,#b39cf5 100%)',
    acc=u'#3538a8', acctint=u'#eef0fa', qn=u'#8b93ff',
)
EYEBROW = (u'S Y S T E M &nbsp;D E S I G N &nbsp; / &nbsp; '
           u'I N T E R V I E W &nbsp;P L A Y B O O K')

book = Book(u'The Complete Guide to Rate Limiting', THEME)

# ═════════════════════════════════════════════════════════ front matter
book.raw(cover(
    THEME, EYEBROW,
    u'The Complete Guide<br>to <span class="hi">Rate Limiting</span>',
    u'Five algorithms, drawn rather than described — then what changes the moment the limiter '
    u'runs on more than one machine, and what it takes to run one in production.',
    [(u'Five algorithms, one picture each',
      u'Fixed window, sliding log, sliding counter, token bucket, leaky bucket.'),
     (u'One trace, five verdicts',
      u'The same 23 requests through all five, simulated — not illustrated.'),
     (u'Distributed, honestly',
      u'Local vs central vs gossip, the read-modify-write race, and the atomic fix.'),
     (u'Production-ready, not textbook',
      u'Fail open or closed, picking the number, and the eight easy mistakes.')],
    u'7 parts · 14 diagrams · 14 interview Q&amp;A · one-page cheat sheet',
    u'Revised August 2026'))

book.page(toc(
    u'C O N T E N T S',
    u'What’s inside',
    u'Built to be read by looking. Every algorithm gets one page and one diagram; Part 4 puts '
    u'all five side by side on the same traffic, and Part 5 is where interviews are actually '
    u'won or lost.',
    [(u'1', u'', u'What a limit is, and where it goes',
      u'Rate limit vs throttle vs quota vs load shedding, and the layer to put each one on.'),
     (u'2', u'', u'The window algorithms',
      u'Fixed window and its famous boundary bug; sliding window log; sliding window counter.'),
     (u'3', u'', u'The bucket algorithms',
      u'Token bucket, leaky bucket in both forms, and why two of them are the same algorithm.'),
     (u'4', u'', u'All five, side by side',
      u'One arrival trace run through every algorithm, plus the decision in four questions.'),
     (u'5', u'', u'Rate limiting across many machines',
      u'Local vs central vs gossip, the counter race, Lua atomicity, and Redis on the hot '
      u'path.'),
     (u'6', u'', u'Production concerns',
      u'Fail open or closed, picking the number, and the eight mistakes that bite in prod.'),
     (u'7', u'', u'The interview itself',
      u'How to structure the answer, 14 asked-in-real-interviews Q&amp;A, and the red flags.'),
     (STAR, u'star', u'One-page cheat sheet',
      u'The night-before page: the five algorithms in one table, the numbers, eight facts.')],
    u'<b>Part of the HLD concept series.</b> Redis mechanics, caching and resiliency patterns '
    u'are separate volumes; this one is only about deciding whether a request may proceed.'))

book.page(
    h2(u'How to use this guide', 'qhead'),
    cards(
        ('', u'Look first',
         [u'Each algorithm is one page: a diagram, ten lines of code, and the trade in two '
          u'sentences. Read the picture, then the words.']),
        ('', u'Say out loud',
         [u'The coloured callouts are the exact sentences that earn the point in an '
          u'interview.']),
        ('', u'Defend',
         [u'Every algorithm here is wrong for something. Knowing which is the answer.']),
    ),
    callout(u'FOUR WORDS INTERVIEWERS USE INTERCHANGEABLY — YOU SHOULD NOT',
            [u'<b>Rate limiting</b> caps requests per unit of time to protect the system. '
             u'<b>Throttling</b> is what you do to a caller that exceeds it — reject, delay or '
             u'degrade. <b>A quota</b> is a business allowance over a long period (10,000 calls '
             u'a month) and is billing, not protection. <b>Load shedding</b> drops traffic when '
             u'the system is already in trouble, regardless of who sent it. A serious design '
             u'has all four, and they fail differently.'],
            'blue'),
    fig(u'0.1', F.fig_family(),
        u'The whole book on one row. Every page that follows is one of these five boxes drawn '
        u'larger.'),
    callout(u'THE ONE THING TO INTERNALISE',
            [u'Every algorithm on the next six pages answers the same question — <b>“has this '
             u'caller used more than X in the last Y?”</b> — and they differ only in how much '
             u'memory they spend to answer it and how honest the answer is at the edges. Pick '
             u'the cheapest one whose dishonesty you can live with.'],
            'teal'),
)

# ═════════════════════════════════════════════════════════ Part 1
book.page(
    part(u'What a limit is, and where it goes', u'PART 1',
         u'Before any algorithm: a rate limit is four decisions — who you count, how many, over '
         u'how long, and what you do when the answer is no.'),
    h2(u'1.1 The four inputs'),
    strip([(u'1', u'Identity', u'IP, API key, user, tenant — what the counter is keyed by'),
           (u'2', u'Limit', u'the number of units allowed'),
           (u'3', u'Window', u'the period the number applies to'),
           (u'4', u'Action', u'reject, delay, degrade, or just log')]),
    fig(u'1.1', F.fig_where(),
        u'The same request can meet three different limiters. Each one knows something the '
        u'others do not.'),
)

book.page(
    h2(u'1.2 Why you are doing this at all', 'qhead'),
    fig(u'1.2', F.fig_why(),
        u'What the limit is actually for: not punishing the noisy caller, but disconnecting '
        u'everybody else from them.'),
    kv([(u'Protect capacity',
         u'One client should not be able to consume the headroom you sized for everyone.'),
        (u'Contain abuse',
         u'Credential stuffing, scraping and enumeration are all rate problems before they '
         u'are anything else.'),
        (u'Control cost',
         u'When a request costs you money — an LLM call, an SMS, a third-party API — the '
         u'limit is the budget.'),
        (u'Enforce fairness',
         u'A shared pool with no per-tenant limit is a pool one tenant will take.'),
        (u'Meet someone else’s limit',
         u'You are often the client. Shaping your own outbound traffic is the same problem '
         u'from the other side.'),
        (u'Make failure predictable',
         u'A limit turns “everything got slow” into “that one caller got 429s”, which is a '
         u'far better outage.')]),
    callout(u'INTERVIEW LINE',
            [u'“I would start by asking what the limit is protecting. If it is capacity, I '
             u'limit at the gateway on the API key. If it is cost, the limit belongs in the '
             u'service and it counts cost units, not requests. If it is abuse, it is per IP at '
             u'the edge and it is deliberately blunt. Those are three different limiters and I '
             u'would probably ship all three.”'],
            'teal'),
)

# ═════════════════════════════════════════════════════════ Part 2
book.page(
    part(u'The window algorithms', u'PART 2',
         u'Chop time into windows and count. Three variants, in the order interviewers walk '
         u'you through them: the cheap one, the exact one, and the one you actually run.'),
    h2(u'2.1 Fixed window counter'),
    p(u'One counter, one window start. When the clock crosses a window boundary the counter '
      u'resets. That is the whole algorithm.'),
    fig(u'2.1', F.fig_fixed(),
        u'Three consecutive windows, limit five. The counter drops to zero at every boundary, '
        u'regardless of what happened one millisecond earlier.'),
    codebox(u'Fixed window — the whole thing',
            u'<span class="cm">// roll forward in whole windows so the grid stays aligned</span>\n'
            u'if (now - windowStart &gt;= windowMillis) {\n'
            u'    windowStart += ((now - windowStart) / windowMillis) * windowMillis;\n'
            u'    count = 0;\n'
            u'}\n'
            u'if (count &lt; maxRequests) { count++; return true; }\n'
            u'return false;',
            u'<b>O(1) memory, O(1) time.</b> In Redis this is literally '
            u'<b>INCR key</b> then <b>EXPIRE key window</b> — two commands, no script.'),
)

book.page(
    h2(u'2.2 …and the bug that spawned three more algorithms', 'qhead'),
    fig(u'2.2', F.fig_boundary(),
        u'The boundary burst. With a limit of 100 per minute, a client can legally take 200 in '
        u'a two-second span straddling the reset.'),
    kv([(u'When it is fine',
         u'Internal traffic, a crude abuse ceiling, or any limit set so far above real usage '
         u'that 2x still does not hurt.'),
        (u'When it is not',
         u'Public APIs, anything adversarial, and anything you bill for — a customer who '
         u'notices will call the 2x a bug, and they will be right.')]),
    codebox(u'Fixed window in Redis — and the second bug hiding in it',
            u'MULTI\n'
            u'  INCR   ratelimit:{user42}:1724500860   <span class="cm">-- key carries the window id</span>\n'
            u'  EXPIRE ratelimit:{user42}:1724500860 60\n'
            u'EXEC\n'
            u'<span class="cm">-- EXPIRE on every call resets the TTL, so a busy key never dies.</span>\n'
            u'<span class="cm">-- Set it only when INCR returns 1, or SET key 0 EX 60 NX first.</span>',
            u'The window id is <i>in the key</i>, so the old window expires on its own and '
            u'there is no reset code at all.'),
    callout(u'HOW TO USE THIS IN AN INTERVIEW',
            [u'Implement fixed window first, then attack it yourself before the interviewer '
             u'does: <b>“this is O(1) and two Redis commands, but it lets a client take twice '
             u'the limit across a boundary — so if this is a public API I would move to a '
             u'sliding window.”</b> Volunteering the flaw is worth more than avoiding it.'],
            'purple'),
)

book.page(
    h2(u'2.3 Sliding window log — the exact one', 'qhead'),
    p(u'Keep a timestamp for every allowed request. Drop the ones that have aged out, count '
      u'what is left. No approximation anywhere.'),
    fig(u'2.3', F.fig_log(),
        u'The window is a bracket anchored to <i>now</i>, sliding continuously. There is no '
        u'boundary, so there is nothing to exploit.'),
    codes(
        codebox(u'Sliding window log',
                u'long cutoff = now - windowMillis;\n'
                u'<span class="cm">// evict what slid out</span>\n'
                u'while (!log.isEmpty()\n'
                u'       &amp;&amp; log.peekFirst() &lt;= cutoff)\n'
                u'    log.pollFirst();\n\n'
                u'if (log.size() &gt;= maxRequests)\n'
                u'    return false;\n'
                u'log.offerLast(now);\n'
                u'return true;'),
        codebox(u'The cost, in numbers',
                u'per client   : up to LIMIT timestamps\n'
                u'per timestamp: 8 bytes (+ overhead)\n\n'
                u'1M clients\n'
                u'  x 1,000 req/window\n'
                u'  x 8 bytes        = <span class="hl">8 GB</span>\n\n'
                u'<span class="cm">// and that is before Redis</span>\n'
                u'<span class="cm">// ZSET key overhead</span>',
                u'Amortised <b>O(1)</b> per call — each timestamp is added once and evicted '
                u'once — but the memory is why this rarely ships unmodified.'),
    ),
)

book.page(
    h2(u'2.4 Sliding window counter — the one you actually run', 'qhead'),
    p(u'Throw the timestamps away. Keep two fixed-window counts and interpolate between them.'),
    fig(u'2.4', F.fig_counter(),
        u'Two counters and one multiply. The previous window’s contribution decays smoothly to '
        u'zero, which is exactly what kills the boundary burst.'),
    codebox(u'Sliding window counter',
            u'long b = now / windowMillis;\n'
            u'if      (b == cur + 1) { prev = curr; curr = 0; cur = b; }   <span class="cm">// rolled once</span>\n'
            u'else if (b &gt;  cur + 1) { prev = 0;    curr = 0; cur = b; }   <span class="cm">// idle client</span>\n\n'
            u'double overlap  = 1.0 - (now - cur * windowMillis) / (double) windowMillis;\n'
            u'double estimate = curr + prev * overlap;\n\n'
            u'if (estimate &lt; maxRequests) { curr++; return true; }\n'
            u'return false;',
            u'<b>Two ints and a long per client.</b> Cloudflare reported roughly 0.003% error '
            u'against an exact log on real traffic — and this is the algorithm most large '
            u'public APIs are actually running.'),
)

# ═════════════════════════════════════════════════════════ Part 3
book.page(
    part(u'The bucket algorithms', u'PART 3',
         u'Stop thinking in windows. A bucket has no boundary to reset at, which is why these '
         u'two never had the fixed-window bug in the first place.'),
    h2(u'3.1 Token bucket'),
    fig(u'3.1', F.fig_token(),
        u'Tokens accrue while you are quiet and are spent when you are busy. Capacity is the '
        u'burst you tolerate; refill rate is the rate you actually enforce.'),
    codebox(u'Token bucket — lazy refill, no background thread',
            u'<span class="cm">// how many tokens WOULD have arrived since the last call</span>\n'
            u'double add = (now - lastRefillNanos) / 1e9 * refillRatePerSecond;\n'
            u'tokens = Math.min(capacity, tokens + add);   <span class="cm">// the cap is the point</span>\n'
            u'lastRefillNanos = now;\n\n'
            u'if (tokens &gt;= 1.0) { tokens -= 1.0; return true; }\n'
            u'return false;',
            u'<b>Never spawn a timer.</b> Computing the refill on read is mathematically '
            u'identical to a continuous top-up and costs nothing. Saying this unprompted is a '
            u'strong signal.'),
)

book.page(
    h2(u'3.2 Leaky bucket — and the answer to “aren’t these the same?”', 'qhead'),
    fig(u'3.2', F.fig_leaky(),
        u'Two different things share one name. The meter is a limiter; the queue is a traffic '
        u'shaper, and it is the only one of the five that can make a request wait.'),
    codes(
        codebox(u'Leaky bucket, meter form',
                u'double out = (now - lastLeakNanos)\n'
                u'             / 1e9 * leakRatePerSecond;\n'
                u'water = Math.max(0.0, water - out);\n'
                u'lastLeakNanos = now;\n\n'
                u'if (water + 1.0 &lt;= capacity) {\n'
                u'    water += 1.0; return true;\n'
                u'}\n'
                u'return false;',
                u'Compare it line by line with token bucket. <b>water = capacity - tokens.</b> '
                u'Same compare, opposite sign.'),
        codebox(u'The two forms, decided',
                u'meter  -&gt; allow / deny\n'
                u'          O(1) memory\n'
                u'          == token bucket\n\n'
                u'queue  -&gt; allow / <span class="hl">wait</span> / drop\n'
                u'          O(queue) memory\n'
                u'          adds latency\n'
                u'          smooths the OUTPUT',
                u'Reach for the queue form only when something downstream genuinely needs a '
                u'steady feed — a partner API that permits 10 calls a second.'),
    ),
)

# ═════════════════════════════════════════════════════════ Part 4
book.page(
    part(u'All five, side by side', u'PART 4 · THE PAGE TO MEMORISE',
         u'The five algorithms are not opinions. Run them against the same arrivals and they '
         u'disagree in specific, predictable ways.'),
    fig(u'4.1', F.fig_compare(),
        u'Twenty-three requests, limit five per second, every verdict produced by running the '
        u'reference implementations — not drawn by hand.'),
    kv([(u'Fixed window let 15 through — and broke the rule',
         u'Seven of them inside 180 ms across the boundary. It is the only row here that '
         u'violates the limit it was configured with.'),
        (u'Sliding log let 10 through — the truth',
         u'Never more than five in any one-second span, anywhere in the trace. This row is '
         u'the definition the others are approximating.'),
        (u'Sliding counter let 13 through — close, and cheap',
         u'It under-counts where the previous window was back-loaded, because it assumes an '
         u'even spread. Two integers bought that.'),
        (u'Both buckets let 16 through — identically',
         u'They start with a full burst allowance and refill continuously, so they are more '
         u'permissive by design, not by accident.')]),
)

book.page(
    h2(u'4.2 The comparison table', 'qhead'),
    table([u'Algorithm', u'Memory / client', u'Bursts', u'Accuracy', u'Reach for it when'],
          [(u'Fixed window', u'1 counter + 1 timestamp', u'2x at the boundary', u'Poor at edges',
            u'It is internal, or the limit is generous enough that 2x is harmless'),
           (u'Sliding log', u'Up to LIMIT timestamps', u'None — exactly N per window', u'Exact',
            u'The number is billable, or the client count is small'),
           (u'Sliding counter', u'2 ints + 1 long', u'Smoothed away', u'~99.9%',
            u'Public API, millions of clients — the production default'),
           (u'Token bucket', u'1 double + 1 timestamp', u'Up to capacity, by design',
            u'Exact for its own rule', u'Human-paced traffic that is legitimately spiky'),
           (u'Leaky bucket (meter)', u'1 double + 1 timestamp', u'Up to capacity',
            u'Same as token bucket', u'You prefer the “is there room?” framing'),
           (u'Leaky bucket (queue)', u'The queue itself', u'Absorbed, then delayed',
            u'Output is perfectly uniform',
            u'Something downstream needs a steady feed and can wait')],
          [88.0, 96.0, 84.0, 78.0, 176.0]),
    fig(u'4.2', F.fig_choose(),
        u'Four questions, four answers. Any of them is defensible; picking without asking one '
        u'of them is not.'),
)

# ═════════════════════════════════════════════════════════ Part 5
book.page(
    part(u'Rate limiting across many machines', u'PART 5 · WHERE INTERVIEWS ARE WON',
         u'Every algorithm so far assumed one process and one lock. Fifty app servers behind a '
         u'load balancer break that assumption immediately, and this is the follow-up that '
         u'separates candidates.'),
    fig(u'5.1', F.fig_dist(),
        u'The three topologies. There is no free option: you are choosing which of exactness, '
        u'latency and availability to give up.'),
    callout(u'INTERVIEW LINE',
            [u'“With fifty nodes, a purely local limiter enforces fifty times the limit — so '
             u'the state has to be shared. I would keep it in Redis with a Lua script so the '
             u'whole decision is one atomic round trip. If that round trip is too expensive at '
             u'our request rate, I would move to local counters with an asynchronous sync and '
             u'say out loud that the enforced limit is now approximate by a few percent.”'],
            'teal'),
)

book.page(
    h2(u'5.2 The race, and why one atomic operation fixes it', 'qhead'),
    fig(u'5.2', F.fig_race(),
        u'Read-modify-write across two nodes. The counter is shared, but the decision was not '
        u'— so both nodes decided yes.'),
    codebox(u'Distributed token bucket — one Lua script, one round trip, atomic',
            u'<span class="cm">-- KEYS[1] = bucket:{clientId}   ARGV = now, rate, capacity</span>\n'
            u'local b    = redis.call(&#39;HMGET&#39;, KEYS[1], &#39;tokens&#39;, &#39;ts&#39;)\n'
            u'local tk   = tonumber(b[1]) or tonumber(ARGV[3])\n'
            u'local ts   = tonumber(b[2]) or tonumber(ARGV[1])\n'
            u'tk = math.min(tonumber(ARGV[3]), tk + (ARGV[1] - ts) * ARGV[2])\n'
            u'local ok = tk &gt;= 1\n'
            u'if ok then tk = tk - 1 end\n'
            u'redis.call(&#39;HSET&#39;, KEYS[1], &#39;tokens&#39;, tk, &#39;ts&#39;, ARGV[1])\n'
            u'redis.call(&#39;EXPIRE&#39;, KEYS[1], 60)\n'
            u'return { ok and 1 or 0, tk }',
            u'<b>The braces matter.</b> <b>bucket:{user42}</b> forces every key for one client '
            u'onto one Redis slot — a script that spans slots will not run, and a counter split '
            u'across shards is not a counter.'),
    kv([(u'Why not a distributed lock?',
         u'It works, and it is the wrong shape: a lock is two round trips plus a failure mode, '
         u'where the script is one round trip and no failure mode.'),
        (u'Why the EXPIRE matters',
         u'Without it you keep one key per client forever. With it, an idle client costs '
         u'nothing and its bucket comes back full — which is correct.')]),
)

# ═════════════════════════════════════════════════════════ Part 6
book.page(
    part(u'Production concerns', u'PART 6',
         u'The algorithm is a day of work. These are the decisions that decide whether the '
         u'limiter helps you at 3 a.m. or becomes the outage.'),
    fig(u'6.1', F.fig_failures(),
        u'The four failure modes worth naming unprompted. Each has one correct answer and one '
        u'tempting wrong one.'),
    h2(u'6.2 Fail open or fail closed?'),
    cards(
        ('good', u'Fail open — the usual choice',
         [u'Redis is down, so allow the request. You lose protection for the duration, but the '
          u'API stays up. Pair it with a small in-process limiter so “open” still has a '
          u'ceiling.']),
        ('bad', u'Fail closed — only when the limit is the product',
         [u'Reject everything the limiter cannot verify. Correct for spend caps and hard '
          u'quotas; catastrophic for a public API, where a Redis blip becomes a full '
          u'outage.']),
    ),
)

book.page(
    h2(u'6.3 Picking the number', 'qhead'),
    strip([(u'1', u'Measure', u'p99 of real per-client rate over a fortnight'),
           (u'2', u'Set high', u'~10x that, so nobody legitimate is hit'),
           (u'3', u'Shadow', u'log what would have been rejected, reject nothing'),
           (u'4', u'Enforce', u'turn it on for new clients first'),
           (u'5', u'Tighten', u'lower it only with the shadow data in hand')]),
    p(u'The mistake is picking a round number and shipping it. The limit exists to stop the '
      u'pathological case, so it should sit far above the legitimate one — and the only way to '
      u'know where that is, is to have measured.'),
    h2(u'6.4 Things that are easy to get wrong'),
    kv([(u'Counting rejected requests',
         u'A throttled client that keeps retrying should not dig its own hole deeper. Only '
         u'record allowed requests — every implementation in this guide does.'),
        (u'Clock skew',
         u'Window boundaries computed from each node’s own clock will not agree. Use the '
         u'store’s clock (Redis <b>TIME</b>) or a monotonic source plus one epoch.'),
        (u'Unbounded key growth',
         u'One key per client per window, with no TTL, is a memory leak with a schedule. '
         u'Always <b>EXPIRE</b>.'),
        (u'Limiting after the expensive work',
         u'A limiter that runs after authentication, deserialisation and a database lookup has '
         u'already spent what it was meant to save.'),
        (u'One config for all clients',
         u'Tiers are the whole business model: free, paid, partner, internal. Make the limit a '
         u'lookup, not a constant.'),
        (u'No observability',
         u'Emit allowed, rejected and near-limit per client. The first question in an incident '
         u'is “who is being throttled?” and you need it answerable in one query.'),
        (u'No way to raise a limit quickly',
         u'The limit will be wrong for somebody eventually. If changing it needs a deploy, you '
         u'have built an incident. Keep it in config you can edit live.'),
        (u'Testing only the happy path',
         u'Test the boundary, the concurrent race, and the store being down. Those three are '
         u'the entire bug surface of a rate limiter.')]),
)

# ═════════════════════════════════════════════════════════ Part 7
book.page(
    part(u'The interview itself', u'PART 7',
         u'“Design a rate limiter” is asked as an LLD question and as a component of half the '
         u'HLD questions. The structure below fits in ninety seconds.'),
    h2(u'7.1 The order to say it in'),
    strip([(u'1', u'Clarify', u'What is it protecting? Who is the caller?'),
           (u'2', u'Key', u'IP, API key, tenant — and say why'),
           (u'3', u'Algorithm', u'Name two, pick one, justify in one sentence'),
           (u'4', u'Distribute', u'Where the state lives, and the atomicity story'),
           (u'5', u'Respond', u'429, Retry-After, headers, jitter'),
           (u'6', u'Fail', u'Open or closed, and what happens when Redis dies')]),
    callout(u'THE NINETY-SECOND ANSWER',
            [u'“I would put a token bucket at the API gateway keyed on the API key, because '
             u'traffic is spiky and capacity gives me a burst allowance separate from the '
             u'sustained rate. State goes in Redis behind a Lua script so refill and compare '
             u'are one atomic round trip, with the client id in a hash tag so it stays on one '
             u'slot. On rejection I return 429 with Retry-After, and I send RateLimit headers '
             u'on successful responses too. If Redis is unreachable I fail open, but with a '
             u'local in-process bucket as a backstop so ‘open’ still has a ceiling.”'],
            'teal'),
    h2(u'7.2 What they are actually scoring'),
    kv([(u'Did you name a trade-off?',
         u'Any of the five is a defensible answer. Picking one without saying what it costs '
         u'is not.'),
        (u'Did you reach the distributed part?',
         u'Most candidates stop at the algorithm. The interesting half starts at the second '
         u'app server.'),
        (u'Did you think about the caller?',
         u'429, Retry-After and jitter are half the design, and almost nobody volunteers '
         u'them.'),
        (u'Did you handle your own failure?',
         u'A limiter on every request path is a new single point of failure. Say what happens '
         u'when it breaks.')]),
)

book.page(
    qa(u'1', u'Design a rate limiter for our public API. Where do you start?',
       [u'With what the limit protects, because that decides everything else. If it is '
        u'capacity, it goes at the gateway keyed on the API key. If it is cost, it goes in the '
        u'service and counts cost units. If it is abuse, it goes at the edge keyed on IP and it '
        u'is deliberately blunt. Then I would name the four inputs — identity, limit, window, '
        u'action — and only after that pick an algorithm.']),
    qa(u'2', u'Which algorithm, and why?',
       [u'Token bucket for the general case: two numbers per client, and capacity lets me '
        u'tolerate a burst without raising the sustained rate. If memory across millions of '
        u'clients is the binding constraint I would use a sliding window counter instead, which '
        u'is two integers and tracks an exact log to within a fraction of a percent. I would '
        u'mention fixed window only to explain why I am not using it.']),
    qa(u'3', u'Explain the fixed window boundary problem.',
       [u'The counter resets on a wall-clock boundary, not relative to the caller. With 100 per '
        u'minute, a client takes 100 in the last second of one minute and 100 in the first '
        u'second of the next — every window saw exactly 100, and the client got 200 in about '
        u'two seconds. Sliding window fixes it by anchoring the window to now; buckets never '
        u'had the problem because they never reset.']),
    qa(u'4', u'Token bucket and leaky bucket — aren’t they the same thing?',
       [u'In the counter form, yes — mathematically identical, with water = capacity minus '
        u'tokens. Token bucket asks “do I have a token to spend?”, the leaky-bucket meter asks '
        u'“is there room in the bucket?”, and those are the same comparison. The genuine '
        u'difference is the queue form of leaky bucket, which holds requests and drains them at '
        u'a fixed rate — that one reshapes the output, and it is the only algorithm here that '
        u'can make a caller wait instead of telling it no.']),
    qa(u'5', u'How accurate is the sliding window counter, really?',
       [u'It assumes the previous window’s requests were spread evenly across it, so it is '
        u'exact when traffic is smooth and drifts when it is not — under-counting if the '
        u'previous window was back-loaded, over-counting if front-loaded. Cloudflare measured '
        u'roughly 0.003% error on production traffic. I would say the number and then say the '
        u'assumption, because the assumption is the part that can bite you.']),
)

book.page(
    qa(u'6', u'You have fifty app servers. How does this still work?',
       [u'A purely local limiter enforces fifty times the limit, so the state has to be shared. '
        u'Central Redis with a Lua script is exact and costs one round trip per request. Local '
        u'counters with an asynchronous sync are fast and approximate. I would default to Redis '
        u'and only move to gossip if the round trip is measurably too expensive — and I would '
        u'say out loud that gossip means the enforced limit is now a few percent loose.']),
    qa(u'7', u'Redis is on the hot path for every request. What happens when it dies?',
       [u'I fail open, because a rate limiter taking down the API is worse than the API being '
        u'briefly unprotected — but “open” still has a ceiling: each node falls back to a local '
        u'in-process limiter sized at the global limit divided by node count. I would also '
        u'circuit-break the Redis call so a slow Redis does not add its timeout to every '
        u'request, and alert on the fallback being active. If the limit were a paid spend cap I '
        u'would fail closed instead, and I would say why the answer flipped.']),
    qa(u'8', u'Two servers read the counter at 99 at the same instant. Walk me through it.',
       [u'Both read 99, both compare against 100, both allow, and the counter lands at 101 — '
        u'one request over, silently, and it gets worse with concurrency. The fix is to make '
        u'the read and the write one operation: <b>INCR</b> is enough for a fixed window '
        u'counter, and anything with more state — token bucket refill, sliding counter '
        u'interpolation — needs a Lua script so the whole decision runs as one critical '
        u'section on one shard.']),
    qa(u'9', u'What do you key the limit on?',
       [u'The account or API key whenever the caller is authenticated, because that is the real '
        u'identity and it survives the client changing networks. IP only for unauthenticated '
        u'traffic, and knowing that carrier NAT puts thousands of users behind one address '
        u'while IPv6 hands one user billions. In practice I would run several layers at once — '
        u'a global ceiling, per-key, and a tighter one on the few endpoints that are expensive '
        u'— and the narrowest layer is the one that usually says no.']),
)

book.page(
    qa(u'10', u'What exactly do you return to the client?',
       [u'<b>429 Too Many Requests</b> with <b>Retry-After</b>, plus '
        u'<b>RateLimit-Limit</b>, <b>-Remaining</b> and <b>-Reset</b> — and I send those '
        u'headers on successful responses too, so a well-behaved client can pace itself instead '
        u'of discovering the limit by hitting it. Not 503, which means “we are overloaded”, and '
        u'never a silent drop, which teaches the client to retry harder.']),
    qa(u'11', u'The client ignores it and keeps hammering. Now what?',
       [u'First make sure I am not causing it: rejected requests must not extend the window, '
        u'and Retry-After must be honest. Then escalate — a longer cooldown for repeat '
        u'offenders, then a cheap deny at the edge so the request never reaches application '
        u'code, and finally a block with a human in the loop. The important property is that '
        u'rejecting must be far cheaper than serving, otherwise the abuse still wins.']),
    qa(u'12', u'How do you pick the actual number?',
       [u'Measure the p99 of real per-client rate over a couple of weeks, set the limit around '
        u'ten times that, run it in shadow mode logging what it would have rejected, then '
        u'enforce — new clients first. Tighten only with shadow data in hand. The limit is '
        u'there to stop the pathological caller, so it belongs far above the legitimate one, '
        u'and picking a round number without measuring is how you page yourself.']),
    qa(u'13', u'Some requests cost a hundred times more than others. How do you limit that?',
       [u'Count cost units rather than requests: tokens for an LLM call, rows scanned for a '
        u'query, seconds of CPU. A token bucket takes this naturally — deduct N tokens instead '
        u'of one. Where the cost is only known afterwards, reserve an estimate up front and '
        u'reconcile the difference when the work finishes, which is exactly how metered APIs '
        u'bill.']),
    qa(u'14', u'Gateway or service — where does the limiter belong?',
       [u'Both, for different reasons. The gateway rejects cheaply and protects everything '
        u'behind it, but it only knows the identity and the route. The service knows what the '
        u'request will actually cost and can limit on that. A single limiter at the gateway is '
        u'the right first answer; adding “and a cost-based one in the service for the expensive '
        u'endpoints” is the senior one.']),
)

book.page(
    h2(u'7.3 Red flags interviewers listen for', 'qhead'),
    table([u'Saying this', u'Says this about you'],
          [(u'Only naming one algorithm', u'Has memorised a blog post, not the trade-off'),
           (u'Fixed window presented as the final answer', u'Does not know the boundary bug'),
           (u'A local counter, with many app servers', u'Enforces N times the limit and has '
                                                       u'not noticed'),
           (u'GET then SET on a shared counter', u'Has never met a race condition'),
           (u'“Token bucket and leaky bucket are different”, with no detail',
            u'Repeating a comparison table without understanding it'),
           (u'No answer for the limiter being down', u'Has added a single point of failure to '
                                                     u'every request'),
           (u'Silently dropping over-limit requests', u'Guarantees a retry storm'),
           (u'Retries with no jitter', u'Will rebuild the exact spike they just shed'),
           (u'Keys with no TTL', u'A memory leak on a schedule'),
           (u'One limit for every customer', u'Has not thought about tiers, and cannot bill'),
           (u'Limiting after the expensive work', u'Has already spent what the limit was '
                                                  u'meant to save')],
          [232.0, 290.0]),
    h2(u'7.4 Real systems worth name-dropping'),
    cards(
        ('', u'Cloudflare’s sliding window counter',
         [u'The blog post that made the two-counter approximation standard, with the measured '
          u'error rate. The single best citation in this whole topic.']),
        ('', u'Stripe’s rate limiters',
         [u'Four limiters of different kinds running together — request rate, concurrency, '
          u'fleet usage, worker utilisation. Good evidence you think in layers.']),
    ),
    cards(
        ('', u'Envoy / the gateway tier',
         [u'Local and global rate limiting as a first-class filter, with a gRPC ratelimit '
          u'service behind it. This is what “put it at the gateway” means in practice.']),
        ('', u'GCRA / the generic cell rate algorithm',
         [u'A leaky bucket expressed as a single timestamp — no counter at all. Worth naming '
          u'if you want to show you have read past the standard five.']),
    ),
)

# ---- cheat sheet ----
book.page(
    u'<span class="chip rev">R E V I S I O N</span>'
    u'<h1 class="big">One-page cheat sheet</h1>'
    + p(u'The night-before page. If you remember only this, you can still hold a good '
        u'conversation about rate limiting.', 'sub')
    + u'<hr class="thin">',
    h2(u'The five, in one line each'),
    table([u'Algorithm', u'State', u'The one-line verdict'],
          [(u'Fixed window', u'counter + window start',
            u'Cheapest. Leaks 2x across the boundary. Implement it, then criticise it.'),
           (u'Sliding log', u'a timestamp per allowed request',
            u'Exact and expensive. Use it when the number is billable.'),
           (u'Sliding counter', u'two counts + a bucket id',
            u'The production default: ~99.9% accurate for O(1) memory.'),
           (u'Token bucket', u'tokens + last-refill time',
            u'Burst up to capacity, then the refill rate. The usual right answer.'),
           (u'Leaky bucket, meter', u'water + last-leak time',
            u'Token bucket inside out. Same behaviour, different framing.'),
           (u'Leaky bucket, queue', u'the queue',
            u'The only one that delays instead of rejecting. Traffic shaping, not limiting.')],
          [104.0, 138.0, 280.0]),
    h2(u'The numbers'),
    formula(u'1M clients × 1,000 hits × 8 bytes = 8 GB of log &nbsp;·&nbsp; sliding counter '
            u'error about 0.003% &nbsp;·&nbsp; N nodes local = N × the limit',
            u'Set the limit at roughly 10× the measured p99 per-client rate, always with a TTL '
            u'on the key and always with jitter on the client’s retry.'),
)

book.page(
    h2(u'Rate limiting in eight facts', 'qhead'),
    facts([
        (u'It is four decisions, not one',
         u'Identity, limit, window, action. The algorithm is the smallest of them.'),
        (u'Fixed window leaks 2x',
         u'The counter resets on the clock, not on the caller. That is the whole bug.'),
        (u'Sliding window anchors to now',
         u'No boundary means nothing to straddle. Log is exact; counter approximates it.'),
        (u'Token and leaky are the same',
         u'In counter form, water = capacity − tokens. Only the queue form differs.'),
        (u'Local counters multiply',
         u'N nodes each enforcing the limit enforce N times the limit.'),
        (u'Read-modify-write races',
         u'INCR for a counter, a Lua script for anything with more state. One shard, always.'),
        (u'Saying no has a cost',
         u'429 plus Retry-After plus jitter, or the rejections become the load.'),
        (u'Fail open, with a ceiling',
         u'The limiter must not be able to take down what it protects — unless it is the bill.'),
    ], tone='acc'),
    h2(u'The five failure modes'),
    table([u'Name', u'Mechanism', u'Primary fix'],
          [(u'Boundary burst', u'Fixed window resets on wall-clock time',
            u'Sliding window counter, or a bucket'),
           (u'Limit multiplication', u'Every node counts independently',
            u'Shared state in Redis, or gossip with a shared budget'),
           (u'Counter race', u'GET then SET across nodes',
            u'INCR, or a Lua script keyed to one slot'),
           (u'Retry storm', u'Every rejected client retries on the same second',
            u'Retry-After plus full jitter; never drop silently'),
           (u'Limiter outage', u'Redis is unreachable and it is on every request path',
            u'Fail open behind a circuit breaker, with a local backstop limiter')],
          [110.0, 200.0, 212.0]),
)

book.page(
    closing(u'IF YOU SAY NOTHING ELSE, SAY THIS',
            u'“A rate limit is four decisions — who I count, how many, over what window, and '
            u'what I do when the answer is no. I would use a token bucket keyed on the API key '
            u'at the gateway, because capacity gives me a burst allowance independent of the '
            u'sustained rate. The state lives in Redis behind a Lua script so refill and '
            u'compare are one atomic round trip on one slot, because otherwise fifty app '
            u'servers each enforce the full limit and two of them will race on the same '
            u'counter. Rejections get 429 with Retry-After, the RateLimit headers go on '
            u'successful responses too, and clients retry with full jitter. If Redis is '
            u'unreachable I fail open behind a local backstop — a rate limiter must never be '
            u'the reason the API is down.”'),
    p(u'<b>Sources &amp; further reading</b> — Cloudflare, <i>How we built rate limiting '
      u'capable of scaling to millions of domains</i> (the sliding window counter and its '
      u'measured error); Stripe engineering, <i>Scaling your API with rate limiters</i>; the '
      u'Envoy documentation on local and global rate limiting; the IETF draft on the '
      u'<b>RateLimit-Limit</b>, <b>-Remaining</b> and <b>-Reset</b> header fields; RFC 6585 '
      u'§4 for 429; AWS Architecture Blog, <i>Exponential backoff and jitter</i>; the ITU-T '
      u'and ATM Forum definitions of the generic cell rate algorithm (GCRA); the Redis '
      u'documentation on Lua scripting, hash tags and <b>INCR</b>/<b>EXPIRE</b>; Kong, NGINX '
      u'and Envoy rate-limit module documentation for how these ship in practice.', 'src'),
)

book.write('v_ratelimiting.html')
