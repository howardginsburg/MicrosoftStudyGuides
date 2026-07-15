# Domain 4 research pack — Optimize an Azure Cosmos DB Solution (15–20%)

Clean-room notes paraphrased from public Microsoft Learn docs. Every objective lists Sources (real learn.microsoft.com URLs).

---

## 4.1 Optimize query performance (API for NoSQL)

### 4.1.1 Adjust indexes on the database
- Every container has an indexing policy. Default policy: indexes EVERY property of every item, using range indexes for strings/numbers. Good performance out of the box.
- Custom policy controls: indexing **mode** (consistent / none), **included/excluded paths**, and index kinds (range, spatial, composite, plus vector/full-text/tuple).
- Path notation: scalar path ends `/?`; array elements `/[]`; wildcard `/*` matches everything below a node.
- Include/exclude strategy: the root `/*` MUST be either included or excluded.
  - Include `/*` → selectively EXCLUDE paths (recommended; auto-indexes new props).
  - Exclude `/*` → selectively INCLUDE paths (partition key path not indexed by default — include it explicitly).
- Precedence: more precise (deeper) path wins; `/?` more precise than `/*`.
- Indexing mode `none` = key-value store, no secondary indexes; disables queries; used to speed bulk loads (then switch to consistent). New containers can't use lazy indexing.
- System props `id` and `_ts` always indexed when mode is consistent; `_etag` excluded by default.
- Modifying policy triggers an online, in-place index transformation (async, consumes RUs at lower priority; no write-availability impact). Track via IndexTransformationProgress in SDK/portal.
- Adding an index takes time (transformation); removing an index takes effect immediately (engine stops using it → full scan). When replacing, add new index first, wait for transformation, then remove old.
- TTL requires indexing — can't enable TTL on a `none`-mode container. For TTL-only with no property indexing: mode consistent, no included paths, `/*` excluded.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-policy
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-overview
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-indexing-policy

### 4.1.2 Calculate the cost of the query
- All operation cost normalized to Request Units (RU). 1-KB point read ≈ 1 RU. RU is a currency abstracting CPU/IOPS/memory.
- Query cost driven by: provisioned throughput, partition key filter (single vs cross-partition), SDK options, network latency, indexing policy, query shape.
- Cheapest→most expensive read: point read (id+PK) > query with PK filter > query with equality/range filter on any property > query without filters.
- Cross-partition (fan-out) queries cost more; results merged client side; ORDER BY merge-sorted; COUNT summed.
- Query execution metrics (in Diagnostics): TotalTime, DocumentLoadTime, IndexLookupTime, RetrievedDocumentCount, OutputDocumentCount, IndexHitRatio (matched/loaded ratio — low ratio = inefficient scan).
- PopulateIndexMetrics option surfaces used indexes + potential new indexes (has overhead; debug only).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query-metrics
  - https://learn.microsoft.com/en-us/azure/cosmos-db/request-units
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-metrics

### 4.1.3 Retrieve RU cost of a point operation or query
- Portal: Data Explorer → run query → Query Stats shows request charge.
- SDK returns request charge on every response:
  - .NET v3: `response.RequestCharge` (double).
  - Java: `getRequestCharge()`.
  - Node.js: `result.headers['x-ms-request-charge']`.
  - Python: `container.client_connection.last_response_headers["x-ms-request-charge"]`.
  - Go: `resp.RequestCharge`.
- Underlying HTTP header is `x-ms-request-charge`. For paged queries, sum the charge across pages.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/find-request-unit-charge
  - https://learn.microsoft.com/en-us/azure/cosmos-db/request-units

### 4.1.4 Implement integrated cache
- In-memory cache inside the **dedicated gateway**. Two parts: item cache (point reads) + query cache (queries). Read-through/write-through, LRU eviction, shared capacity.
- Cache HIT = **0 RU**. First read populates cache; repeats within staleness window served free.
- Requirements: connect with dedicated gateway connection string, use **gateway** connection mode, and use **session or eventual** consistency. Strong/bounded staleness/consistent prefix reads bypass the cache.
- `MaxIntegratedCacheStaleness` = max acceptable staleness for cached reads; per-request; default 5 min; min 0, max 10 years. Higher = more hits.
- No global cache TTL; eviction only via item update/delete, LRU, or a lower MaxIntegratedCacheStaleness on a later read.
- Each dedicated gateway node has an independent cache; multi-page queries not guaranteed same node.
- Best for read-heavy, repeated point reads/queries, hot read partition key. Not for write-heavy or rarely repeated reads or change-feed reads.
- Transactional batch / bulk requests don't populate the item cache.
- Metrics: DedicatedGatewayRequests, IntegratedCacheItemHitRate, IntegratedCacheQueryHitRate, IntegratedCacheEvictedEntriesSize.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/integrated-cache
  - https://learn.microsoft.com/en-us/azure/cosmos-db/dedicated-gateway
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-configure-integrated-cache

---

## 4.2 Change feeds (API for NoSQL)

### 4.2.1 Azure Functions trigger to process a change feed
- Azure Functions Cosmos DB trigger = simplest way to consume the change feed; built on the change feed processor (scaling + reliable detection) with no worker infra to maintain.
- Requires monitored container + lease container. Lease can be auto-created via `CreateLeaseContainerIfNotExists`. Partitioned lease containers must use `/id` partition key.
- Supports latest version mode (default, all models/languages) and all-versions-and-deletes mode (.NET isolated worker; requires continuous backup + feature enabled).
- Function runs per batch of changes; add conditional logic to notify/act selectively. NoSQL API only. Can run locally with the emulator.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/change-feed-functions
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/change-feed-processor

### 4.2.2 Consume change feed with the SDK (change feed processor)
- Change feed processor is in .NET v3 and Java v4 SDKs. Fault-tolerant, at-least-once delivery.
- Four components: monitored container (source), lease container (state/coordination), compute instance (host, unique instance name), delegate (your handler).
- Build via `GetChangeFeedProcessorBuilder(processorName, onChangesDelegate).WithInstanceName(...).WithLeaseContainer(...).Build()` then `StartAsync()`.
- Life cycle: read feed → sleep if none (WithPollInterval) → send to delegate → checkpoint lease → repeat.
- Deployment unit = instances sharing same processorName + lease config but different instance names. Dynamic scaling distributes leases (1 lease owned by 1 instance; instances ≤ leases).
- Python/Node.js use the change feed pull model instead (manual checkpointing).
- Starting time: default = only changes after first init; WithStartTime(DateTime) or DateTime.MinValue (from beginning). Latest-version only.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/change-feed-processor
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed

### 4.2.3 Manage number of instances via change feed estimator
- Estimator measures lag = difference between last processed item (lease state) and latest change. Tells you if processing rate < change rate → scale out.
- Push model: `GetChangeFeedEstimatorBuilder(name, HandleEstimationAsync, interval).WithLeaseContainer(...)` — delegate receives count pending; default interval 5s.
- On-demand model: `GetChangeFeedEstimator(name, leaseContainer)` → `GetCurrentStateIterator()` returns per-lease EstimatedLag + owning InstanceName.
- Estimator shares the same lease container + processor name; deploy independently; each estimation consumes RUs (≈1-min frequency good start). Works in both change feed modes; not exact count.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/how-to-use-change-feed-estimator
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/change-feed-processor

### 4.2.4 Denormalization by change feed
- Read source container's change feed to propagate copies of data into other containers/partitions for read optimization. Eventual consistency.
- Data-movement pattern: replicate to a container with a different logical partition key; keep materialized copies in sync.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/change-feed-design-patterns
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed

### 4.2.5 Referential enforcement by change feed
- Event-computing pattern: on each change, a processor/Function validates references and cascades related updates/deletes across containers (application-level referential integrity — Cosmos has no FK constraints).
- Order guaranteed within a partition key value, not across → pick PK that keeps related events ordered.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/change-feed-design-patterns
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/change-feed-functions

### 4.2.6 Aggregation persistence by change feed
- After processing changes, build a materialized view and persist aggregated values back to Cosmos DB (e.g., real-time leaderboards, running totals). High availability, RTO 0.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/change-feed-design-patterns
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed

### 4.2.7 Data archiving by change feed
- Data movement + tiering: keep hot data in Cosmos DB, age cold data out to cheaper storage (e.g., Azure Blob Storage). Latest-version mode doesn't emit deletes → use soft-delete marker (`deleted:true`) + TTL for later cleanup; that update appears in the feed.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/change-feed-design-patterns
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-modes

---

## 4.3 Indexing strategy (API for NoSQL)

### 4.3.1 Read-heavy vs write-heavy index strategy
- Writes: every indexed path adds RU cost per write. Fewer indexed paths → cheaper/faster writes. Write-heavy → trim indexed paths (exclude unqueried paths).
- Reads: more/composite indexes reduce query RU and latency. Read-heavy → index the paths you filter/order on, add composite indexes.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-policy
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-overview

### 4.3.2 Choose an appropriate index type
- Range: equality, range (>, <, =, etc.), ORDER BY single property, string prefixes — default for strings/numbers.
- Spatial: geospatial queries (Point, Polygon, MultiPolygon, LineString); not created by default — add explicitly.
- Composite: multi-property ORDER BY (required) and multi-property filters.
- (Also vector, full-text, tuple for specialized scenarios.)
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-overview
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-policy
  - https://learn.microsoft.com/en-us/azure/cosmos-db/sql-query-geospatial-index

### 4.3.3 Configure custom indexing policy in the portal
- Data Explorer → container → Settings/Scale & Settings → Indexing Policy → edit JSON → Save. Triggers index transformation.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-indexing-policy
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-policy

### 4.3.4 Implement a composite index
- Defined in `compositeIndexes` as an array of path+order sets. Two or more paths; sequence matters; each path has implicit `/?`; no `/*` wildcard.
- ORDER BY: composite path sequence + order (ASC/DESC) must match ORDER BY; opposite order on all paths also works. Required for multi-property ORDER BY.
- Multi-filter: equality props first, at most one range filter last per composite index; multiple range filters need multiple composite indexes.
- Filter + ORDER BY: filter props first in ORDER BY; equality filters first; max one range/system function last.
- New composite index used only after transformation completes; existing range indexes used meanwhile.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-policy
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-indexing-policy

### 4.3.5 Optimize index performance
- Use include `/*` + exclude unqueried paths so new props auto-index; exclude large unqueried subtrees to cut write RU.
- Add composite indexes for ORDER BY and multi-filter queries; index the partition key path (unless `/id`) to avoid full scans on PK-hierarchy filters.
- Group multiple policy changes into one transformation; add-before-remove when replacing an index. Use index metrics + IndexHitRatio to find missing/unused indexes.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-policy
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-metrics
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query-metrics
