# DP-420 Domain 3 — Research Pack (Integrate an Azure Cosmos DB Solution)

Clean-room notes paraphrased from public Microsoft Learn. Every objective lists verified facts + Sources (real learn.microsoft.com URLs). MCP Learn was unavailable; grounded via fetch_webpage against learn.microsoft.com.

---

## 3.1 Enable Azure Cosmos DB Analytical Workloads

### 3.1.1 Configure Azure Cosmos DB Mirroring for Microsoft Fabric
- Mirroring in Microsoft Fabric provides a no-ETL (zero-ETL) way to bring Azure Cosmos DB data into Microsoft Fabric for HTAP with full isolation between transactional and analytical systems.
- Cosmos DB data is continuously replicated into Fabric **OneLake** in near real-time, with **no performance impact** on transactional workloads and **without consuming Request Units (RUs)**.
- Data lands in OneLake in the open-source **Delta Lake / Parquet** format (with V-Order optimization), automatically available to all Fabric analytical engines.
- Mirroring is **GA** and is the recommended replacement for Azure Synapse Link (Synapse Link is no longer supported for new projects).
- **Continuous backup** (7-day or 30-day) is a prerequisite. 7-day continuous backup is free and recommended if enabling specifically for mirroring.
- Each mirrored Cosmos DB item creates: the mirrored database item, an auto-generated **SQL analytics endpoint** (read-only T-SQL over the Delta tables), and a default **Power BI semantic model**.
- Fabric compute used to replicate is **free**; OneLake storage is free based on capacity size. Query compute (SQL, Power BI, Spark) is charged against Fabric capacity.
- You can use **Direct Lake** mode in Power BI over the mirrored data; Copilot in Fabric adds GenAI insights.
- Currently only **API for NoSQL** accounts are supported; not available in sovereign clouds. Mirroring does **not** support accounts with multiple write regions.
- Mirroring does **not** use analytical store or change feed as its CDC source; those remain independently usable.
- Nested data appears as a JSON string in SQL analytics endpoint tables; expand with `OPENJSON`, `CROSS APPLY`, `OUTER APPLY`.
- Sources:
  - https://learn.microsoft.com/en-us/fabric/mirroring/azure-cosmos-db
  - https://learn.microsoft.com/en-us/fabric/database/mirrored-database/azure-cosmos-db
  - https://learn.microsoft.com/en-us/fabric/mirroring/azure-cosmos-db-tutorial

### 3.1.2 Choose Between Azure Cosmos DB Mirroring and the Azure Cosmos DB Spark Connector
- **Mirroring** = fully managed, no-code, near real-time replication of the whole database into OneLake; free compute, no RU cost, read-only analytics via SQL endpoint / Power BI / Spark shortcuts. Best for BI and analytics without building pipelines.
- **Spark connector** (for the transactional store, format `cosmos.oltp`) = code-first; reads and **writes** the transactional store; consumes RUs; good for data engineering, ML, and when you need to write results back to Cosmos DB.
- Mirroring is the recommended zero-ETL path for analytics; the Spark connector is the choice when you need programmatic transformation, custom pipelines, or write-back.
- The `cosmos.olap` Spark format reads the analytical store (Synapse Link, no RU cost, read-only); `cosmos.oltp` reads/writes the transactional store (consumes RUs).
- Sources:
  - https://learn.microsoft.com/en-us/fabric/mirroring/azure-cosmos-db
  - https://learn.microsoft.com/en-us/azure/synapse-analytics/synapse-link/how-to-query-analytical-store-spark-3
  - https://learn.microsoft.com/en-us/azure/cosmos-db/analytical-store-introduction

### 3.1.3 Enable the Analytical Store on a Container
- Analytical store is a fully isolated **column store** that auto-syncs operational data for large-scale analytics with **no impact** on transactional workloads and **no RU allocation**.
- Enabled via **Analytical TTL (ATTL)**: set to `-1` (infinite retention) or a positive integer `n` seconds. `0` = disabled. Enabling requires Synapse Link enabled at the account level first.
- **Auto-sync** propagates inserts/updates/deletes from transactional to analytical store, typically within ~2 minutes (up to ~5 min for shared-throughput DBs with many containers).
- Configure ATTL via portal (Data Explorer container settings; default -1 when toggled on), Azure CLI (`--analytical-storage-ttl`), PowerShell (`-AnalyticalStorageTtl`), ARM, or SDKs (`AnalyticalStoreTimeToLiveInSeconds` in .NET, `analytical_storage_ttl` in Python).
- Turning on Synapse Link at the account does **not** auto-enable analytical store; you must enable it per container.
- Two schema representations: **well-defined** (default for NoSQL/Gremlin) and **full fidelity** (default for MongoDB; must be chosen at account enablement time for NoSQL and can't be changed later).
- Schema limits: first 1000 properties, 127 nesting levels; columns can't be removed; no schema reset/versioning.
- Data tiering: combine transactional TTL and analytical TTL to keep hot data short-lived in the transactional store while retaining longer history cheaply in analytical store (ATTL >= TTTL).
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/analytical-store-introduction
  - https://learn.microsoft.com/en-us/azure/cosmos-db/configure-synapse-link

### 3.1.4 Enable a Connection to an Analytical Store and Query from Azure Synapse Spark or Azure Synapse SQL
- **Azure Synapse Link** provides the connection between Cosmos DB analytical store and Azure Synapse Analytics for near real-time HTAP.
- Steps: enable Synapse Link on the account → enable analytical store on containers → connect the Cosmos DB database to a Synapse workspace (creates a linked service) → query from Spark or serverless SQL.
- **Synapse Spark**: load the analytical store into a DataFrame with `spark.read.format("cosmos.olap")` (or create a Spark table using `cosmos.olap`). DataFrame caches a snapshot at creation; Spark table re-reads latest on each query.
- **Synapse serverless SQL pool**: query with `SELECT ... OPENROWSET(PROVIDER = 'CosmosDB', CONNECTION = 'Account=...;Database=...', OBJECT = '<container>', ...)`; auto-updated views can also be created.
- Both runtimes can **only read** from analytical store; only auto-sync writes to it. No RU impact.
- Contributor role needed to enable Synapse Link at account level; Operator to enable on containers.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/configure-synapse-link
  - https://learn.microsoft.com/en-us/azure/synapse-analytics/synapse-link/how-to-query-analytical-store-spark-3
  - https://learn.microsoft.com/en-us/azure/cosmos-db/analytical-store-introduction

### 3.1.5 Perform a Query Against the Transactional Store from Spark
- Use the **`cosmos.oltp`** Spark format to read directly from the transactional store; this consumes provisioned RUs and can impact OLTP performance (unlike `cosmos.olap`).
- Structured streaming from the change feed uses `cosmos.oltp.changeFeed` with options such as `spark.cosmos.changeFeed.startFrom` and `spark.cosmos.changeFeed.mode` (Incremental).
- Choose `cosmos.oltp` when you need the freshest data or write-back; choose `cosmos.olap` for RU-free, read-only analytics on synced data.
- Sources:
  - https://learn.microsoft.com/en-us/azure/synapse-analytics/synapse-link/how-to-query-analytical-store-spark-3
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-spark

### 3.1.6 Write Data Back to the Transactional Store from Spark
- Write a Spark DataFrame into a Cosmos DB container using `.write.format("cosmos.oltp")` with `.mode("append")` (Scala `SaveMode.Append`).
- Data is **always** ingested through the **transactional store**; if Synapse Link is enabled, new inserts/updates/deletes then auto-sync to analytical store.
- Writing consumes RUs provisioned on the target container / shared database and affects transactional performance.
- Streaming writes use `.writeStream.format("cosmos.oltp")` with a `checkpointLocation`.
- Sources:
  - https://learn.microsoft.com/en-us/azure/synapse-analytics/synapse-link/how-to-query-analytical-store-spark-3
  - https://learn.microsoft.com/en-us/azure/cosmos-db/analytical-store-introduction

### 3.1.7 Implement Change Data Capture in the Azure Cosmos DB Analytical Store
- **CDC in the analytical store** yields a continuous, incremental feed of inserted/updated/deleted data, consumed via Azure Synapse or Azure Data Factory **mapping data flows** (or Copy activity), with a no-code experience.
- Because it's based on analytical store, CDC **doesn't consume RUs**, doesn't affect transactional workloads, has lower latency and lower TCO.
- Captures **deletes, intermediate updates, and TTL** operations (TTL treated as delete). Use `{_rid}` as the sink key column to reflect updates/deletes.
- **Internally managed checkpoints** (GLSN-based, not `_ts`): each change appears exactly once; no records missed; no fixed retention limit for availability (bounded only by analytical TTL for "from beginning").
- Start options: **from beginning** (initial full snapshot then incremental), **from a timestamp**, or **from now**.
- Filter the feed by operation type (Insert / Update / Delete / TTL); apply filters, projections, and transformations via a source query (pushed down to the columnar store).
- Multiple independent CDC processes can run in parallel on the same container with different sinks/transformations.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/analytical-store-change-data-capture
  - https://learn.microsoft.com/en-us/azure/cosmos-db/get-started-change-data-capture

### 3.1.8 Implement Time Travel in Warehouse in Microsoft Fabric
- **Time travel** in Fabric Warehouse / SQL analytics endpoint queries data as it existed at a past point in time using the T-SQL query hint `OPTION (FOR TIMESTAMP AS OF 'YYYY-MM-DDTHH:MM:SS[.fff]')`.
- Results are **read-only**; INSERT/UPDATE/DELETE aren't allowed with the hint. The hint applies to the whole SELECT statement (all joined tables) and can be used once per statement.
- Retention is automatic and configurable from **1 to 120 calendar days** (default **30**). Time travel works only within the retention window.
- Timestamps use **UTC** only; at most 3 fractional-second digits; values must be deterministic.
- Time travel returns the **latest table schema**; querying a point before a schema change works only if referenced columns already existed then.
- Use cases: stable reporting during ETL, historical trend analysis, low-cost comparisons, auditing/compliance, reproducing ML results. Table-level history is also available via `CLONE TABLE`.
- Sources:
  - https://learn.microsoft.com/en-us/fabric/data-warehouse/time-travel
  - https://learn.microsoft.com/en-us/fabric/data-warehouse/how-to-query-using-time-travel
  - https://learn.microsoft.com/en-us/fabric/data-warehouse/data-retention

---

## 3.2 Implement Solutions Across Services

### 3.2.1 Integrate Events with Other Applications by Using Azure Functions and Azure Event Hubs
- The **Azure Functions trigger for Cosmos DB** fires on each change in the container's change feed, letting you build reactive, serverless event pipelines without managing worker infrastructure (built on the change feed processor: automatic checkpointing, at-least-once, dynamic scaling).
- A common integration pattern: change feed → Azure Function → publish events to **Azure Event Hubs** (via an output binding) so downstream/other applications can consume them; this decouples producers and consumers.
- Event Hubs is a high-throughput streaming ingestion service (retention up to ~90 days) often paired with Cosmos DB change feed for **lambda architecture** and real-time stream processing.
- The Functions trigger requires a **monitored container** and a **lease container** (state for scaling; `/id` partition key; can auto-create with `CreateLeaseContainerIfNotExists`).
- Supports latest-version mode (default) and all-versions-and-deletes mode (needs continuous backups + feature enabled; .NET isolated worker). Trigger currently supports **API for NoSQL** only.
- You can run and debug locally with the Cosmos DB emulator, no subscription needed.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-functions
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-design-patterns
  - https://learn.microsoft.com/en-us/azure/cosmos-db/serverless-computing-database

### 3.2.2 Denormalize Data by Using Change Feed and Azure Functions
- Cosmos DB data modeling favors **denormalization** for read efficiency; the change feed is the recommended mechanism to keep denormalized/duplicated copies in sync across partitions and containers.
- Pattern: a change to a source item triggers an Azure Function that propagates the change to embedded/duplicated copies in other items or containers (e.g., copying a product name into every order document).
- Real-time replication with the change feed guarantees only **eventual consistency**; monitor lag with the change feed estimator.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-design-patterns
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/model-partition-example
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-functions

### 3.2.3 Enforce Referential Integrity by Using Change Feed and Azure Functions
- Cosmos DB has **no foreign keys**; referential integrity is enforced in the application layer. The change feed + Azure Functions is the standard approach.
- Pattern: when a referenced item changes or is (soft) deleted, a Function reacts to the change feed event and cascades updates/cleanup to related items to keep references valid.
- Deletes aren't captured in **latest version mode**; use a **soft-delete flag** (e.g., `deleted: true`, optionally with TTL) so the deletion surfaces as an update in the change feed — or use **all versions and deletes mode** (requires continuous backups) to capture real deletes.
- Order is guaranteed **within a partition key** but not across partition keys; pick a partition key that preserves meaningful ordering for the events you must process in sequence.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-design-patterns
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-modes
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-functions

### 3.2.4 Aggregate Data by Using Change Feed and Azure Functions, Including Reporting
- Use the change feed to build **materialized views** / pre-aggregated summaries and persist them back to Cosmos DB (or another store) for fast reporting (e.g., real-time leaderboards, running totals, counts).
- An Azure Function processes each change, updates the aggregate, and writes it back — avoiding expensive full-container scans at read time.
- Because processing is per-partition-ordered and at-least-once, design aggregates to be idempotent; eventual consistency applies.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-design-patterns
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-functions
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed

### 3.2.5 Archive Data by Using Change Feed and Azure Functions
- Change feed enables **application-level data tiering/archival**: keep "hot" data in Cosmos DB and age "cold" data out to cheaper storage (e.g., **Azure Blob Storage**) via a Function reading the change feed.
- Complements TTL: use TTL to expire hot data from the transactional store after the archival Function has copied it out.
- Also supports zero-downtime migrations and updating downstream caches/search indexes/data warehouses from the change feed.
- Sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-design-patterns
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-functions
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/time-to-live

### 3.2.6 Implement Azure AI Search for an Azure Cosmos DB Solution
- **Azure AI Search** can index Cosmos DB content using an **indexer** + **data source** so the data becomes full-text / vector searchable. Cosmos DB indexing and AI Search indexing are different operations.
- Three-part workflow: create a **data source** (`"type": "cosmosdb"`, connection string with `AccountEndpoint;AccountKey;Database`, and container/collection), create a **search index**, create an **indexer** referencing both. The indexer runs on creation and can be scheduled or run on demand.
- Prerequisites: an automatic, **Consistent** indexing policy on the Cosmos DB container (default; lazy indexing not recommended); read permissions (full-access key or managed identity assigned **Cosmos DB Account Reader** + **Cosmos DB Built-in Data Reader**).
- **Change detection**: `HighWaterMarkChangeDetectionPolicy` on the `_ts` timestamp enables incremental indexing of new/changed docs.
- **Deletion detection**: only **soft-delete** policy is supported (`SoftDeleteColumnDeletionDetectionPolicy` with a Boolean flag column such as `isDeleted`).
- Use an optional **query** on the data source to flatten nested JSON, project fields, join arrays, or filter; `DISTINCT` and `GROUP BY` aren't supported (they break continuation-token pagination).
- The default document key is `_rid` (renamed to `rid`, Base64-encoded) for partitioned collections. Connect via portal Import data wizard, REST API, or SDKs.
- Sources:
  - https://learn.microsoft.com/en-us/azure/search/search-how-to-index-cosmosdb-sql
  - https://learn.microsoft.com/en-us/azure/search/search-indexer-overview
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/vector-search
