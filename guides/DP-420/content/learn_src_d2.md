# DP-420 Domain 2 — Research Pack (Design and Implement Data Distribution)

Clean-room notes paraphrased from public Microsoft Learn. Every objective lists verified facts + Sources (real learn.microsoft.com URLs).

---

## 2.1 Design and implement a replication strategy for Azure Cosmos DB

### 2.1.1 Choose when to distribute data
- Azure Cosmos DB is globally distributed: an account can span multiple Azure regions to place data close to users, lowering read/write latency and raising availability.
- Add or remove regions at any time with no application redeploy or pause; the account stays highly available throughout.
- Reasons to distribute: reduce user latency (data near users), survive regional outages (business continuity), scale read/write throughput globally, meet data-residency needs.
- Trade-off: each additional region multiplies provisioned throughput cost (RU/s billed per region) and storage cost.
- Serverless accounts run in a single region only — global distribution requires provisioned throughput.
- Single-region accounts can still use zone redundancy (availability zones) for intra-region resiliency without adding a second region.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/distribute-data-globally
  - https://learn.microsoft.com/en-us/azure/cosmos-db/serverless
  - https://learn.microsoft.com/en-us/azure/reliability/reliability-cosmos-db

### 2.1.2 Define automatic (service-managed) failover policies for regional failure (NoSQL)
- Service-managed failover: Microsoft detects a write-region outage and automatically promotes a secondary region to write. You must (1) enable service-managed failover and (2) set a failover priority order for regions.
- On failover, the highest-priority available region becomes the new write region.
- Latency: declaring an outage and triggering service-managed failover can take significant time — potentially one hour or more.
- Any writes not yet replicated when the write region fails can be lost (unless the account uses strong consistency, RPO 0).
- Recovered region is NOT automatically promoted back to write; you change the write region back manually when safe.
- Per-partition automatic failover (PPAF) is a separate, faster (public preview) mechanism that fails over individual partitions automatically (typically ~3 minutes).
- Enable/configure via Azure portal, PowerShell, CLI, or ARM.
- Sources:
  - https://learn.microsoft.com/en-us/azure/reliability/reliability-cosmos-db
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-database-account
  - https://learn.microsoft.com/en-us/azure/cosmos-db/distribute-data-globally

### 2.1.3 Perform manual failovers to move single-master write regions
- Manual / forced failover (a.k.a. customer-managed failover, offline-region operation): you trigger it. Recommended way to quickly restore availability during an outage because service-managed failover can take an hour+.
- Taking the write region offline promotes the next-highest-priority read region to write.
- A forced failover of the write region can lose unreplicated writes.
- Change write region (planned failover): when all regions are healthy, change the write region deliberately — no data loss (replication catches up first); requires healthy regions, so cannot be used during an outage.
- Also used to run disaster-recovery drills: temporarily disable service-managed failover, force a failover, observe the app, then fail back.
- Do NOT run control-plane operations (change write region, change consistency, modify network) on an affected region during an outage — it delays recovery.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-database-account
  - https://learn.microsoft.com/en-us/azure/reliability/reliability-cosmos-db

### 2.1.4 Choose a consistency model
- Five well-defined levels, strongest → weakest: Strong, Bounded staleness, Session, Consistent prefix, Eventual.
- Session is the default account consistency level.
- Configured at the account level; applies to all databases/containers; can be overridden per request but only to a WEAKER level (never stronger than the account default), and only within the SDK client for reads.
- Strong = linearizability: reads always return the latest committed write; never a partial/uncommitted write.
- Bounded staleness = reads lag by at most K versions (updates) OR T time interval, whichever comes first. Best for single-write-region accounts with 2+ regions wanting near-strong cross-region consistency. Anti-pattern for multi-region writes.
- Session = within a client session, read-your-writes and write-follows-reads guaranteed via a partition-bound session token.
- Consistent prefix = never see out-of-order writes; transactional batch writes become visible together.
- Eventual = weakest; no ordering guarantee; replicas may return stale data.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-consistency

### 2.1.5 Identify use cases for different consistency models
- Strong: financial/inventory/ordering where a stale read is unacceptable; single write region only.
- Bounded staleness: globally distributed reads that must be nearly current within a known bound (e.g., leaderboards, near-real-time dashboards) on a single-write-region account.
- Session (default): user-centric apps where a user must read their own writes (profiles, shopping carts, social timelines) — best balance of consistency, availability, latency, throughput.
- Consistent prefix: apps that tolerate lag but must never see writes out of order (e.g., status transitions, comment threads within a transaction).
- Eventual: highest availability/throughput, ordering not needed (like counts, likes, retweets, non-threaded comments).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels

### 2.1.6 Impact of consistency on availability and RU cost
- Read RU cost: Strong and Bounded staleness reads consult two replicas (local minority quorum) to guarantee consistency, so they cost about twice the RUs of Session/Consistent prefix/Eventual reads (which use a single replica).
- Write RU cost is identical across all consistency levels for a given operation type.
- Availability: Strong reduces availability during failures — strong with multi-region writes is unsupported; strong needs 2+ regions (dynamic quorum) and can lose write availability if it drops below quorum.
- Weaker levels (session/consistent prefix/eventual) give higher availability and throughput.
- RPO during a region outage: Strong = 0; Bounded staleness = K & T; Session/Consistent prefix/Eventual = < 15 minutes (multi-region).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels
  - https://learn.microsoft.com/en-us/azure/reliability/reliability-cosmos-db

### 2.1.7 Impact of consistency on performance and latency
- Read latency < 10 ms at P99 (average ~4 ms) for all levels; write latency < 10 ms at P99 (average ~5 ms) for all levels EXCEPT strong across multiple regions.
- Strong multi-region write latency ≈ 2× the round-trip time (RTT) between the two farthest regions + 10 ms at P99, because the write must commit in every region.
- Strong consistency for regions spanning more than 5,000 miles (8,000 km) is blocked by default (contact support to enable) due to high write latency.
- Stronger consistency = higher latency + more RU for reads; weaker = lower latency, higher throughput.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels

### 2.1.8 Specify application connections to replicated data
- The SDK connects to a prioritized list of regions. Configure preferred/application regions so the client reads from the nearest healthy region and fails over in order.
- .NET v3: `CosmosClientOptions.ApplicationRegion` (single) or `ApplicationPreferredRegions` (ordered list). Java v4: `preferredRegions`. Python: `preferred_locations`.
- If a preferred read region is unavailable, the SDK detects it via backend response codes and reroutes to the next region in the list — no code change needed.
- For multi-region-write accounts, direct reads/writes to the same region the app is hosted in.
- Front globally distributed apps with a global load balancer (Azure Front Door / Traffic Manager) to route users to a healthy region.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-database-account
  - https://learn.microsoft.com/en-us/azure/cosmos-db/troubleshoot-sdk-availability
  - https://learn.microsoft.com/en-us/azure/reliability/reliability-cosmos-db

---

## 2.2 Design and implement multi-region writes

### 2.2.1 Choose when to use multi-region writes
- Multi-region writes (formerly "multi-master") make every region both readable and writable — active-active — enabling local low-latency writes and 99.999% read+write availability.
- Choose it when: writes must be low-latency for globally distributed users, or you need continuous write availability during a regional outage.
- Trade-offs: strong consistency is NOT supported with multi-region writes; concurrent writes to the same item in different regions can conflict, so you must adopt a conflict-resolution strategy.
- Bounded staleness is an anti-pattern for multi-region writes (reads/writes should target the local region).
- Each write region adds cost.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/distribute-data-globally
  - https://learn.microsoft.com/en-us/azure/cosmos-db/multi-region-writes
  - https://learn.microsoft.com/en-us/azure/reliability/reliability-cosmos-db

### 2.2.2 Implement multi-region writes
- Enable multiple write regions on the account (portal, PowerShell, CLI, ARM) — can be set at creation or later.
- Configure the app: set the SDK's application region so each client writes to its local region. .NET v3 uses `ApplicationRegion`/`ApplicationPreferredRegions`.
- A hub region acts as the arbiter for write conflicts.
- Replication between write regions is asynchronous; lag depends on the account consistency level.
- Avoid frequently updating or recreating the same document ID (e.g., right after TTL expiry) — it increases conflicts and hurts replication performance.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-multi-master
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-database-account
  - https://learn.microsoft.com/en-us/azure/cosmos-db/multi-region-writes

### 2.2.3 Implement a custom conflict resolution policy (NoSQL)
- Two policies (set at container creation only; cannot be changed afterward):
  - Last Write Wins (LWW) — default. Uses the system timestamp `_ts` by default; for API for NoSQL you can set a custom numeric property as the "conflict resolution path"; the highest value wins. A delete always wins over insert/replace. LWW conflicts do NOT appear in the conflict feed.
  - Custom — application-defined. Register a merge stored procedure invoked automatically on conflict (exactly-once). If no procedure is registered, or it throws, conflicts go to the conflict feed for manual resolution. Custom policy is API-for-NoSQL only.
- Conflict types: insert, replace, delete.
- Conflict feed: read unresolved conflicts and resolve them in application code (also how unreplicated writes surface after a region recovers).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/conflict-resolution-policies
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-conflicts

---

## Allowed diagrams for Domain 2
- consistency-levels
- global-distribution
- multi-region-writes
