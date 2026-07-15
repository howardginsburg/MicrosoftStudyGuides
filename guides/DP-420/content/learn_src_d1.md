# Domain 1 research pack — Design and Implement Data Models (DP-420)

Clean-room notes paraphrased from public Microsoft Learn. Each objective lists key facts + the real learn.microsoft.com Sources actually retrieved.

---

## 1.1 Non-relational data model (NoSQL)

### obj-1-1-1 Store multiple entity types in the same container
- Containers are schema-agnostic; you can co-locate different entity types (e.g., `book` and `review`) in one container.
- Add a discriminator property (commonly `type`) to distinguish entity shapes at query time.
- Co-location is most useful when related documents share the same partition key so they land in one logical partition (e.g., partition by `bookId`).
- Fewer containers can mean fewer throughput allocations and lets you read related types with a single partition-scoped query.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/modeling-data
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning

### obj-1-1-2 Store multiple related entities in the same document (embedding)
- Embedding nests related data (arrays/objects) inside a single JSON item; a full read is one operation.
- Embed for contained/one-to-few relationships, infrequently changing data, bounded data, and data read together.
- Denormalized (embedded) models generally give better read performance.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/modeling-data

### obj-1-1-3 Denormalize data across documents
- Denormalization duplicates fields (e.g., author name + thumbnail into each book) to avoid extra reads.
- Trade-off: writes must fan-out to update duplicated data; acceptable when the duplicated data rarely changes.
- Hybrid models mix embedding + referencing; precomputed aggregates (e.g., `countOfBooks`) optimize read-heavy workloads.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/modeling-data

### obj-1-1-4 Reference between documents (normalize)
- Store a reference (e.g., `pub-id`) instead of embedding; each entity is a separate item.
- Reference for one-to-many with unbounded growth, many-to-many, and frequently changing/large related data.
- No foreign keys/constraints; referential integrity is the app's (or a trigger/change-feed's) responsibility.
- Normalizing generally gives better write performance but can need more round trips on read.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/modeling-data

### obj-1-1-5 Identify partition key, id, and unique keys
- `id` is unique within a logical partition; partition key + `id` uniquely identifies an item.
- Partition key value is immutable after item creation; changing it requires re-creating the item.
- Unique keys enforce uniqueness of one/more property values within a logical partition; defined at container creation.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning
  - https://learn.microsoft.com/en-us/azure/cosmos-db/concepts-limits

### obj-1-1-6 Identify data and associated access patterns
- Model around how the app reads/writes; read-heavy vs write-heavy drives embed vs reference.
- List queries first, then pick partition key + document shape to serve them with partition-scoped reads.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/modeling-data
  - https://learn.microsoft.com/en-us/azure/cosmos-db/model-partition-example

### obj-1-1-7 Default TTL on a container (transactional store)
- Container `DefaultTimeToLive`: null = no auto-expiry; -1 = TTL enabled but items don't expire by default; n = items expire n seconds after last modification.
- Item `ttl` overrides the container default; only effective if container TTL isn't null.
- Expired items disappear from queries immediately; background delete uses leftover RUs (provisioned) or billed RUs (serverless). Max TTL 2,147,483,647 s.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/time-to-live
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-time-to-live

### obj-1-1-8 Versioning documents
- Keep historical versions as separate items (event sourcing / snapshot+delta) rather than overwriting.
- TTL can age out old versions automatically (container TTL -1, per-item `ttl` on history items).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/modeling-data
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-design-patterns

### obj-1-1-9 Document schema versioning
- Schema-free storage lets shapes evolve; add a `schemaVersion`/`_schema` property so code can branch per version.
- Migrate lazily (on read/write) or in bulk; distinguish types with a discriminator when mixing.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/modeling-data

---

## 1.2 Partitioning strategy

### obj-1-2-1 Choose a partitioning strategy for a workload
- Logical partition = items sharing a partition key value; scope of transactions; up to 20 GB and 10,000 RU/s each.
- Physical partitions are managed internally: up to 50 GB and 10,000 RU/s each; splits are automatic and non-disruptive.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning

### obj-1-2-2 Choose a partition key
- Good key: high cardinality (wide value range), immutable, evenly spreads storage + RU, aligns with common query filters.
- Anti-patterns: low-cardinality fields (status/type/country), high-cardinality with no query alignment (random GUID never filtered), `/id` for mixed-query workloads.
- Key length ≤ 2048 bytes (101 bytes without large partition keys); string or numeric value.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning

### obj-1-2-3 Plan for transactions when choosing a partition key
- Transactional batch and stored-procedure/trigger transactions are scoped to a single logical partition.
- Choose a key that groups items that must be changed atomically into the same partition key value.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/database-transactions-optimistic-concurrency
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning

### obj-1-2-4 Cost of a cross-partition query
- A query without the partition key fans out to all physical partitions; overhead ~2–3 RU per extra physical partition, plus latency.
- Include the partition key (or HPK prefix) in the filter to route to a subset of partitions.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-query-container

### obj-1-2-5 Evaluate data distribution
- Uneven key values create hot partitions and risk the 20 GB logical-partition ceiling.
- Evaluate value frequency; use synthetic/hierarchical keys when a single value grows too large or too hot.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning

### obj-1-2-6 Evaluate throughput distribution
- Provisioned RU/s is split evenly across physical partitions; skew wastes RU and causes 429s on hot partitions.
- Aim for even RU consumption across logical partition key values.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning
  - https://learn.microsoft.com/en-us/azure/cosmos-db/set-throughput

### obj-1-2-7 Synthetic partition key
- Concatenate multiple properties (or add a random/hashed suffix) to raise cardinality and spread writes.
- Downside: queries filtering on only one component may go cross-partition unless all component values are supplied.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/modeling-data

### obj-1-2-8 Hierarchical partition key (subpartitioning)
- Up to three levels (e.g., TenantId > UserId > SessionId); `kind: MultiHash`, `version: 2`.
- Lets a first-level prefix exceed 20 GB / 10,000 RU/s; queries by full key or a prefix route to a subset of partitions; middle-only or lower-only filters fan out.
- First level should have high cardinality; set at container creation only; supported in newer .NET/Java/Python/JS SDKs.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/hierarchical-partition-keys
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning

### obj-1-2-9 Workloads needing multiple partition keys
- No single key serves all query patterns → options: hierarchical key, synthetic key, or global secondary indexes (preview) which maintain a synchronized copy with a different key.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning
  - https://learn.microsoft.com/en-us/azure/cosmos-db/hierarchical-partition-keys

---

## 1.3 Sizing and scaling

### obj-1-3-1 Throughput and storage requirements
- RUs normalize CPU/IO/memory; a 1 KB point read ≈ 1 RU; writes/queries cost more. Same query on same data = deterministic RU.
- Estimate with the capacity calculator; account for item size, indexed properties, consistency (strong/bounded ≈ 2× read RU), query complexity.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/request-units
  - https://learn.microsoft.com/en-us/azure/cosmos-db/estimate-ru-with-capacity-planner

### obj-1-3-2 Serverless vs provisioned vs free tier
- Provisioned: reserve RU/s (manual or autoscale); billed hourly for provisioned RU/s; supports geo-distribution; SLA-backed latency.
- Serverless: pay per consumed RU; single region only; good for spiky/low average traffic.
- Free tier: first 1000 RU/s + 25 GB free per account (one free-tier account per subscription).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/throughput-serverless
  - https://learn.microsoft.com/en-us/azure/cosmos-db/serverless
  - https://learn.microsoft.com/en-us/azure/cosmos-db/free-tier

### obj-1-3-3 Database-level provisioned throughput
- Shared RU/s across up to 25 containers; manual min 400 RU/s, autoscale min 1000 RU/s (100–1000 range).
- No per-container guarantee; a busy container/tenant can starve others; container-level is recommended default.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/set-throughput
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-provision-database-throughput

### obj-1-3-4 Granular scale units and resource governance
- Scale unit = container (or shared database). RU/s reserved is available in every account region (total = R × N regions).
- Autoscale scales 10%–100% of max instantly; use per-container throughput for isolation.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/provision-throughput-autoscale
  - https://learn.microsoft.com/en-us/azure/cosmos-db/request-units

### obj-1-3-5 Cost of global distribution
- Each added region provisions the same RU/s again (R × N); multi-region write adds cost. Storage billed per region.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/request-units
  - https://learn.microsoft.com/en-us/azure/cosmos-db/distribute-data-globally

### obj-1-3-6 Configure throughput in the portal
- Data Explorer / Scale & Settings to set manual or autoscale RU/s on a container or database.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-provision-container-throughput
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-provision-autoscale-throughput

---

## 1.4 Client connectivity (SDK)

### obj-1-4-1 Gateway vs direct
- Gateway: HTTPS 443, single endpoint, extra hop, all SDKs, best behind strict firewalls / limited sockets.
- Direct: TCP (TLS), fewer hops, best performance, .NET + Java only; needs ports 10000–20000 (public) or 0–65535 (private endpoints).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/sdk-connection-modes

### obj-1-4-2 Implement a connectivity mode
- Set `ConnectionMode` (Direct/Gateway) via `CosmosClientOptions`.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/sdk-connection-modes
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-dotnet-get-started

### obj-1-4-3 Create a connection to a database
- Construct `CosmosClient(endpoint, key)` or with Microsoft Entra credential; get database/container proxies (no network call to get proxies).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-dotnet-get-started
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/quickstart-dotnet

### obj-1-4-4 Emulator for offline dev
- Local endpoint `https://localhost:8081/`, well-known key; import TLS cert or disable validation (Gateway); Windows + Docker (Linux/Windows) variants; preinstalled on GitHub `windows-latest` runners.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-develop-emulator
  - https://learn.microsoft.com/en-us/azure/cosmos-db/emulator

### obj-1-4-5 Handle connection errors
- Transient network/timeout/503; direct mode needs the TCP port range open (else 503). Use retries and health checks.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/sdk-connection-modes
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/troubleshoot-dotnet-sdk

### obj-1-4-6 Singleton client
- Create ONE `CosmosClient` per app lifetime and reuse; it's thread-safe and caches routing/connections. New instances per request cause socket exhaustion and latency.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/best-practice-dotnet
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/sdk-connection-modes

### obj-1-4-7 Specify a region
- `ApplicationRegion`/`ApplicationPreferredRegions` sets preferred read region for lowest latency and failover order.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/best-practice-dotnet
  - https://learn.microsoft.com/en-us/azure/cosmos-db/distribute-data-globally

### obj-1-4-8 Threading and parallelism
- Query options: `MaxConcurrency` (parallel partition fan-out), `MaxItemCount`, `MaxBufferedItemCount`; bulk via `AllowBulkExecution`.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/best-practice-dotnet
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query-metrics-performance

### obj-1-4-9 SDK logging
- `CosmosClientOptions` supports a distributed-tracing/logging factory; capture diagnostics from responses.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/best-practice-dotnet
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query-metrics-performance

---

## 1.5 SQL query language

### obj-1-5-1 Arrays, nested objects, aggregation, ordering
- `SELECT ... FROM c JOIN t IN c.tags` (intra-item self-join over arrays); aggregates `COUNT/SUM/AVG/MIN/MAX`; `ORDER BY` (single or composite via composite index).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/getting-started
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/join

### obj-1-5-2 Correlated subquery
- A subquery in `FROM`/`WHERE` that references the outer item; optimizes array filtering (e.g., filter tags once, use in multiple places).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/subquery

### obj-1-5-3 Array and type-checking functions
- Arrays: `ARRAY_CONTAINS`, `ARRAY_LENGTH`, `ARRAY_SLICE`, `ARRAY_CONCAT`. Type checks: `IS_DEFINED`, `IS_NULL`, `IS_STRING`, `IS_NUMBER`, `IS_ARRAY`, `IS_OBJECT`.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/getting-started

### obj-1-5-4 Mathematical, string, date functions
- Math: `ABS`, `CEILING`, `FLOOR`, `ROUND`. String: `CONCAT`, `CONTAINS`, `STARTSWITH`, `ENDSWITH`, `UPPER`, `LOWER`, `TRIM`. Date: `GetCurrentDateTime`, `DateTimeAdd`, `DateTimeDiff`.
- Note: `UPPER`/`LOWER` in a filter can't use the index → full scan.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/getting-started
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query-metrics-performance

### obj-1-5-5 Queries based on variable data
- Use parameterized queries (`@name`) to bind runtime values (safety + plan reuse); schema-agnostic with `IS_DEFINED` for optional properties.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/getting-started

---

## 1.6 Data access with SDK

### obj-1-6-1 Point operation vs query
- Point read (`ReadItem` by id + partition key) ≈ 1 RU for ~1 KB, lowest latency; use a query when you don't know the id or filter across items.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/optimize-cost-reads-writes
  - https://learn.microsoft.com/en-us/azure/cosmos-db/request-units

### obj-1-6-2 Create/update/delete point operations
- `CreateItemAsync`, `ReadItemAsync`, `ReplaceItemAsync`, `UpsertItemAsync`, `DeleteItemAsync`; pass partition key for efficiency.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-dotnet-get-started

### obj-1-6-3 Patch (partial update)
- `PatchItemAsync` with ops Add/Set/Replace/Remove/Increment/Move; max 10 ops per single-item patch; conditional predicate supported; multi-item patch within one partition is a transaction.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partial-document-update
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partial-document-update-getting-started

### obj-1-6-4 Transactional batch
- `TransactionalBatch` = all-or-nothing operations within ONE logical partition key; up to 100 operations / 2 MB.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/transactional-batch

### obj-1-6-5 Bulk support
- `AllowBulkExecution = true` groups concurrent point operations into batched backend requests for high-throughput ingest; use many concurrent tasks.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/tutorial-dotnet-bulk-import
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/best-practice-dotnet

### obj-1-6-6 Optimistic concurrency (ETags)
- Every item has `_etag`; pass `IfMatchEtag` in `ItemRequestOptions`; mismatch → HTTP 412 (precondition failed) so you can retry.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/database-transactions-optimistic-concurrency

### obj-1-6-7 Override consistency per request
- Requests can only weaken (not strengthen) the account default via request options; strong/bounded read RU ≈ 2× weaker levels.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-consistency

### obj-1-6-8 Session consistency with session tokens
- Session token returned per write; cache and pass it to guarantee read-your-writes; tokens are partition-bound; missing token → reads behave as eventual.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels

### obj-1-6-9 Pagination
- `MaxItemCount` sets page size (a hint, not a hard cap); iterate `FeedIterator.ReadNextAsync()` while `HasMoreResults`.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query-metrics-performance
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-dotnet-get-started

### obj-1-6-10 Continuation token
- `FeedResponse.ContinuationToken` resumes a query later/elsewhere; not valid across different query text; don't hand-edit.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query-metrics-performance

### obj-1-6-11 Transient errors and 429s
- 429 = request rate too large; response has `x-ms-retry-after-ms`. SDK auto-retries up to a configurable limit (MaxRetryAttemptsOnRateLimitedRequests / MaxRetryWaitTimeOnRateLimitedRequests). Fix by raising RU/s or spreading load.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/troubleshoot-request-rate-too-large

### obj-1-6-12 Item TTL
- Set the `ttl` property on the item (positive int seconds or -1); only effective when container `DefaultTimeToLive` is not null.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/time-to-live

### obj-1-6-13 Query metrics
- `feedResponse.Diagnostics.GetQueryMetrics()` → `ServerSideCumulativeMetrics` (cumulative + per-partition + `TotalRequestCharge`); `feedResponse.RequestCharge` for RU. Watch Retrieved vs Output doc count and Index Utilization.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query-metrics-performance
  - https://learn.microsoft.com/en-us/azure/cosmos-db/find-request-unit-charge

---

## 1.7 Server-side programming (JavaScript)

### obj-1-7-1 Write, deploy, call a stored procedure
- JS registered per container; use `getContext()`, `getCollection()`, `getResponse()`; must supply a partition key value at execution; upfront RU charge (avg of prior runs).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/how-to-write-stored-procedures-triggers-udfs
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-use-stored-procedures-triggers-udfs

### obj-1-7-2 Transactional stored procedures within a partition
- Sprocs run in an ACID transaction scoped to one logical partition; thrown JS error rolls back; bounded execution via `createDocument` boolean + resume by count.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/how-to-write-stored-procedures-triggers-udfs
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning

### obj-1-7-3 Triggers
- Pre-triggers (before write, manipulate `getRequest().getBody()`, no input params) and post-triggers (after write, run in same transaction); must be specified per operation and by `TriggerOperation`.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/how-to-write-stored-procedures-triggers-udfs

### obj-1-7-4 User-defined functions (UDF)
- Pure JS functions callable inside queries (e.g., `udf.tax(c.income)`); no data access; extend query expressions.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/how-to-write-stored-procedures-triggers-udfs
