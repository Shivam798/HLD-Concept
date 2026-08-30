# HLD Concepts — the building-block guides

One PDF per **concept** that shows up in every high-level-design interview. Each volume is
self-contained: its own cover, its own contents page, its own numbering, its own interview Q&A
and its own one-page cheat sheet. Nothing here depends on reading another volume first.

The companion repo [`../HLD-IQ`](../HLD-IQ) holds the 28 **questions** (design Twitter, design
Uber…) plus [`HLD-CHEATSHEET.md`](../HLD-IQ/HLD-CHEATSHEET.md). These guides are the concepts
those questions assume you already know.

---

## Shipped

| # | Guide | Pages | What it covers |
|---|-------|-------|----------------|
| 1 | [Caching](Caching-System-Design-Guide.pdf) | 41 | The seven cache layers, six patterns (cache-aside → refresh-ahead), invalidation and consistency, eviction policies, the famous failure modes (stampede, penetration, avalanche, hot key, big key, pollution, cold start), capacity planning, 15 Q&A |
| 2 | [Redis](Redis-System-Design-Guide.pdf) | 34 | Threading model, data types and encodings, expiry, RDB/AOF, replication, Sentinel, Cluster slots, memory; then Redis beyond caching — all five rate limiters, locks, leaderboards, queues, idempotency, HyperLogLog, geo — plus a command reference and 15 Q&A |
| 3 | [Databases](Databases-System-Design-Guide.pdf) | 28 | Choosing a store from the access pattern, nine store families, B-tree vs LSM, indexing and query plans, keyset pagination, data modelling and single-table design, ID schemes, isolation levels and write skew, connection pools, replica lag, online migrations, 14 Q&A |
| 4 | [Sharding](Sharding-System-Design-Guide.pdf) | 24 | When to shard (and the five cheaper moves first), shard-key selection, hash vs range vs directory vs geo, consistent hashing with virtual nodes, rendezvous and jump hashing, routing topologies, resharding a live system, cross-shard queries and uniqueness, 14 Q&A |
| 5 | [HLD Data Structures](Data-Structures-System-Design-Guide.pdf) | 21 | Bloom and cuckoo filters with the sizing formula, HyperLogLog, count-min sketch, Space-Saving top-K, t-digest and why percentiles don't average, reservoir sampling, skip lists, inverted indexes, tries for autocomplete, Merkle trees, vector clocks, CRDTs, geohash/S2/H3, Snowflake IDs, 14 Q&A |
| 6 | [Replication & Consistency](Replication-System-Design-Guide.pdf) | 22 | CAP and PACELC said correctly, the consistency ladder, single-leader vs multi-leader vs leaderless, sync/async/semi-sync, replication lag anomalies, failover and fencing, quorums (W+R>N), hinted handoff, read repair, Raft, logical clocks, multi-region shapes with RPO/RTO, 14 Q&A |
| 7 | [Messaging & Streams](Messaging-System-Design-Guide.pdf) | 21 | Queue vs log, Kafka partitions/offsets/consumer groups/ISR/compaction, the outbox pattern and CDC, delivery semantics and idempotent consumers, event-carried state vs event sourcing, sagas, consumer lag, poison messages and DLQs, backpressure, replay, 14 Q&A |
| 8 | [Rate Limiting](Rate-Limiting-System-Design-Guide.pdf) | 27 | Rate limit vs throttle vs quota vs load shedding, all five algorithms with a diagram each (fixed window and its boundary burst, sliding log, sliding counter, token bucket, leaky bucket in both forms), all five run side by side on one simulated trace, distributed limiting — local vs central vs gossip, the counter race and the Lua fix, the 429 / Retry-After / RateLimit contract, jitter, layered keys, fail open vs closed, 14 Q&A |

Every volume has the same shape, so you can navigate any of them the same way:

```
cover → contents → how to use → Part 1..N → the interview itself (Q&A + red flags) → cheat sheet
```

## Suggested reading order

1. **Databases** — everything else sits on top of the data layer.
2. **Caching** then **Redis** — the two questions asked in almost every interview.
3. **Replication & Consistency** — the language every distributed answer needs.
4. **Sharding** — the answer to "and what happens when one machine isn't enough?".
5. **Messaging & Streams** — how the pieces talk once they stop calling each other.
6. **HLD Data Structures** — the vocabulary the other volumes reference (Bloom, HLL, Merkle…).
7. **Rate Limiting** — a self-contained component question, and the one most likely to be asked
   on its own as well as inside a larger design.

## Planned

Same format, same depth. Ordered by how often they decide an interview:

- [ ] **Load Balancing, DNS, CDN & the Edge** — DNS and anycast, L4 vs L7, algorithms and
      health checks, TLS termination, HTTP/2 and HTTP/3, CDN caching and purge, WAF, global
      traffic management
- [ ] **APIs & Communication** — REST vs gRPC vs GraphQL, sync vs async, WebSocket vs SSE vs
      long-poll, pagination, versioning, idempotency keys, timeouts and deadlines, contracts
- [ ] **Resiliency & Failure Handling** — timeouts, retries with jitter, circuit breakers,
      bulkheads, load shedding, graceful degradation, cascading-failure anatomy, chaos testing,
      failover and blast radius
- [ ] **Distributed Transactions & Data Integrity** — 2PC, sagas and compensations, the outbox,
      idempotent consumers, double-entry ledgers, event sourcing and CQRS, reconciliation
- [ ] **Estimation & Capacity Planning** — the latency numbers, back-of-envelope templates,
      QPS/storage/bandwidth maths, latency budgets, headroom and cost
- [ ] **Observability & Operations** — metrics vs logs vs traces, SLIs/SLOs and error budgets,
      alerting that doesn't page for nothing, dashboards, deploys, canaries and rollbacks
- [ ] **Security & Abuse** — authn vs authz, OAuth2/OIDC and JWT, session design, encryption in
      transit and at rest, secrets, bot defence, PII and compliance (rate limiting itself now
      has its own volume)
- [ ] **Search, Geo & Analytics Stores** — inverted indexes and relevance, Elasticsearch
      operationally, geospatial indexing end to end, time-series stores and cardinality,
      OLAP/warehouse and the lambda vs kappa argument

## Notes

- Sources for each volume are listed on its last page.
- `.build/` holds the generator: `kit.py` (page components), `svgkit.py` + `figs_*.py`
  (diagrams — `figs_rl.py` also carries runnable ports of the five rate-limit algorithms, so
  Figure 4.1 of that volume is simulated rather than drawn), `vol_*.py` (one file per volume),
  the recovered Segoe UI subsets plus Selawik as
  a metric-compatible fallback, and the QA scripts. Rebuild a volume with
  `python3 vol_x.py && ./render.sh v_x.html && python3 verify.py v_x.html v_x.pdf`
  (`verify.py` proves no glyph silently vanished; `check.py` catches overflow and font
  fallbacks).
- `.backups/` holds the pre-split versions of the Caching and Redis PDFs (they were one
  combined book originally).
- All volumes share one visual system — Segoe UI/Selawik typography, the same figure language,
  the same "interview line" and "red flag" conventions — so a page from any of them reads as
  part of the same set.
