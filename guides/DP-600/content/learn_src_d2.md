# DP-600 Domain 2 – Prepare Data: Research Notes (PUBLIC Microsoft Learn Sources)

> **Purpose:** Clean-room research notes for the study guide author. ONLY content from public
> Microsoft Learn documentation. No instructor decks. All facts grounded with URLs retrieved live.
>
> **Exam weight:** Domain 2 = 45–50% of DP-600.
> **Generated:** 2026-07-13

---

## o-2-1-1 — Create a data connection (connections, gateways, cloud connections)

### Facts

- **Manage connections and gateways** is the central hub in Fabric settings (Settings → Manage
  connections and gateways) for creating, editing, and deleting both cloud and on-premises
  connections.
- **Three gateway types:**
  1. **On-premises data gateway (standard mode)** – multi-user, supports live connection /
     DirectQuery, managed by IT; requires gateway software on a customer-managed machine.
  2. **On-premises data gateway (personal mode)** – single-user, scheduled refresh only; no
     live connection or DirectQuery support.
  3. **Virtual network (VNet) data gateway** – Microsoft-managed SaaS; supports many users;
     requires Premium capacity or PPU; no on-premises software to install.
- **Cloud connections** are created directly in the "Connections" tab (New → Cloud) for
  cloud-native sources (Azure SQL, ADLS Gen2, SharePoint Online, REST APIs, etc.) that are
  publicly reachable without a gateway.
- **Authentication methods** for a connection: Basic, OAuth2, Service Principal (Entra app
  registration). OAuth2 caveat: long-running queries may fail if the token expires; cross-tenant
  Entra accounts are not supported.
- A connection can be made **shareable** so other workspace members can reuse it without seeing
  credentials (privacy levels still apply).
- For on-premises sources, gateway version ≥ 3000.214.2 is required to support Fabric
  **pipelines** (older versions only support Dataflows and semantic model refresh).
- Fabric Data Factory supports 26+ on-premises connectors via gateway, including SQL Server,
  Oracle, SAP HANA, PostgreSQL, MySQL, Salesforce, SharePoint, ODBC, etc.

### Code (REST – list connections)

```http
GET https://api.fabric.microsoft.com/v1/connections
Authorization: Bearer <token>
```

### Sources

- https://learn.microsoft.com/fabric/data-factory/data-source-management
- https://learn.microsoft.com/fabric/data-factory/how-to-access-on-premises-data
- https://learn.microsoft.com/power-bi/guidance/fabric-adoption-roadmap-system-oversight#architecture

---

## o-2-1-2 — Discover data via OneLake catalog and Real-Time hub

### Facts — OneLake Catalog

- **OneLake catalog** is a tenant-wide governance and discovery UI accessible from the Fabric
  navigation pane (and embedded in Teams, Excel, and Copilot Studio).
- The **Explore tab** surfaces lakehouses, warehouses, Fabric databases, mirrored items, and
  other Fabric item types. Users see only items they have permission to view.
- Item details pane shows metadata, lineage, endorsement status, sensitivity labels, and
  table-level schema information—all without leaving the explore list context.
- Catalog can be scoped by **domain** to narrow results across a large tenant.
- The **Catalog Search API** (`POST /v1/catalog/search`) supports full-text search by item
  name/description/workspace, plus type filters (e.g., `"Type eq 'Lakehouse'"`).
- Considerations: Streaming semantic models are retired and are no longer shown in the catalog.

### Facts — Real-Time hub

- **Real-Time hub** is provisioned automatically for every Fabric tenant — no setup needed.
- It is the single, tenant-wide logical place for all streaming data: streams (Eventstreams) and
  KQL tables from Eventhouses.
- **Microsoft sources page** within Real-Time hub lists pre-integrated Microsoft streaming
  sources (Azure Event Hubs, Azure IoT Hub, PostgreSQL CDC, Azure SQL CDC, etc.); selecting one
  opens a prepopulated wizard that creates an Eventstream automatically.
- Users can search/filter streams by name, parent, owner, or workspace, then set **alerts**
  (stored as Fabric Activator/Reflex items) directly on a stream.
- Real-Time hub also provides numerous out-of-box connectors (Azure, Google, AWS, Fabric events)
  for ingesting data into Fabric streaming pipelines.

### Code (Catalog Search API – example body)

```http
POST https://api.fabric.microsoft.com/v1/catalog/search
Content-Type: application/json

{
  "search": "Sales Revenue",
  "pageSize": 50,
  "filter": "Type eq 'Lakehouse'"
}
```

### Sources

- https://learn.microsoft.com/fabric/governance/onelake-catalog-explore
- https://learn.microsoft.com/fabric/governance/onelake-catalog-explore#view-item-details
- https://learn.microsoft.com/rest/api/fabric/articles/onelakecatalog/overview
- https://learn.microsoft.com/fabric/real-time-hub/real-time-hub-overview
- https://learn.microsoft.com/fabric/real-time-intelligence/user-flow-3
- https://learn.microsoft.com/fabric/real-time-intelligence/user-flow-1

---

## o-2-1-3 — Ingest or access data (Dataflows Gen2, pipelines/Copy activity, notebooks, shortcuts, COPY INTO, upload)

### Facts — Dataflows Gen2

- **Dataflow Gen2** uses the Power Query Online experience (same as Excel / Power BI); offers
  300+ built-in transformations; low-code.
- Dataflow Gen2 runs on **Fabric capacity** — scales automatically; can run standalone or as an
  activity inside a pipeline.
- Three compute modes:
  1. **Mashup Engine** (default) – standard Power Query evaluation.
  2. **High Scale / Staging** – uses a staging Lakehouse + Warehouse SQL engine; better for
     large datasets; can be disabled per query.
  3. **Spark compute** – used when Mapping Data Flow (MDF) transforms are included.
- Supports full Power Query M language; output can target Lakehouse tables or Warehouse tables.
- Supports query folding: when the source supports it, transformations are pushed down to the
  source (reduces data movement). Only operations that fold are pushed; non-folding steps
  execute in Mashup Engine.

### Facts — Pipelines / Copy Activity

- **Data Pipeline** is Fabric's ADF-equivalent orchestration tool; groups activities into
  logical workflows with schedule, event, or on-demand triggers.
- **Copy activity** is the primary data movement primitive; handles source-to-destination moves
  for hundreds of connectors; supports binary copy (no transformation) or mapping.
- **Copy job** is a simplified wrapper around Copy activity for pure data movement without full
  pipeline complexity; supports bulk copy, incremental copy, and CDC replication.
- Best for: moving petabyte-scale data; recommended for bronze (raw) ingestion.
- Activity categories: Data movement (Copy data, Copy job), Data transformation (Dataflow Gen2,
  Notebook, SQL Script, Delete data), Control flow (ForEach, Lookup, Set Variable, Webhook).
- Staging note: workspace staging times out after 60 minutes; use external storage for long-
  running jobs.

### Facts — Notebooks / Spark

- **Fabric Notebooks** support PySpark, Spark SQL, Scala, SparkR, and Python (non-Spark).
- Notebooks access data from Lakehouse (Files and Tables), Warehouse via Spark connector
  (`synapsesql`), KQL databases via KQL magic, and ADLS/S3 via shortcuts.
- Spark connector (`synapsesql`) reads data from Warehouse or Lakehouse SQL analytics endpoint
  into a DataFrame via T-SQL query:
  ```python
  df = spark.read.option("databaseName", "<warehouse>").synapsesql("<T-SQL Query>")
  ```
- Best for: complex transformations, unstructured/semi-structured data, ML pipelines.

### Facts — Shortcuts

- **OneLake shortcuts** are logical pointers (not data copies) that reference data in external
  systems: ADLS Gen2, Amazon S3, Google Cloud Storage, SharePoint, and other OneLake workspaces
  (including cross-tenant via OneLake data sharing).
- Zero-copy: shortcut data appears as part of the OneLake namespace; all Fabric engines (Spark,
  SQL endpoint, Direct Lake, KQL) can query it alongside native data.
- Shortcuts can also reference data within another Fabric workspace (internal shortcuts).
- Lakehouse SQL analytics endpoint sees shortcut-backed Delta tables alongside local tables.
- Only **Delta format** tables (not Parquet/CSV raw files) appear in the SQL analytics endpoint.
- OneLake can auto-apply file transformations (convert CSV → Delta) or AI transformations on
  shortcut targets without a pipeline.

### Facts — T-SQL COPY INTO (Warehouse)

- `COPY INTO` is the **primary** recommended T-SQL statement for high-throughput ingestion into
  a Fabric Warehouse from Azure Blob Storage or ADLS Gen2.
- Supports CSV, Parquet, ORC file formats.
- Key options: `FILE_TYPE`, `FIRSTROW` (skip header rows), `MAXERRORS`, `ERRORFILE` (rejected
  rows), `CREDENTIAL` (storage key, managed identity, Entra ID SPN).
- For best performance: file size 100 MB–1 GB each; maximize file count for parallelism;
  run multiple COPY INTO statements concurrently.
- `BULK INSERT` is also supported for legacy code compatibility; `COPY INTO` preferred for new
  code.

### Facts — Upload (Get data)

- Fabric portal supports direct file upload into a Lakehouse (Files section or Tables section)
  for small datasets, CSV, Parquet, Delta — no pipeline needed.

### Code — COPY INTO (warehouse)

```sql
-- CSV with header row skip
COPY INTO dbo.bing_covid
FROM 'https://pandemicdatalake.blob.core.windows.net/.../bing_covid-19_data.csv'
WITH ( FILE_TYPE = 'CSV', FIRSTROW = 2 );

-- Parquet
COPY INTO dbo.TaxiTrips
FROM 'https://azureopendatastorage.blob.core.windows.net/nyctlc/yellow'
WITH ( FILE_TYPE = 'PARQUET' );

-- With managed identity
COPY INTO <TableName>
FROM 'https://<account>.dfs.core.windows.net/<container>/<folder>/'
WITH ( CREDENTIAL = (IDENTITY = 'Managed Identity') );
```

### Decision guide (ingestion method)

| Scenario | Recommended method |
|---|---|
| Large-scale raw copy, many connectors, schedule | Pipeline / Copy activity |
| Pure data movement, no pipeline orchestration | Copy job |
| Low-code transformation + load | Dataflow Gen2 |
| Code-based complex transform | Notebook (Spark) |
| Real-time streaming | Eventstream |
| No-copy, reference external data | Shortcut |
| High-throughput SQL ingest from Azure storage | T-SQL COPY INTO |

### Sources

- https://learn.microsoft.com/fabric/fundamentals/get-data
- https://learn.microsoft.com/fabric/fundamentals/decision-guide-pipeline-dataflow-spark
- https://learn.microsoft.com/fabric/data-factory/copy-data-activity
- https://learn.microsoft.com/fabric/data-factory/what-is-copy-job
- https://learn.microsoft.com/fabric/onelake/onelake-shortcuts
- https://learn.microsoft.com/fabric/data-warehouse/ingest-data-copy
- https://learn.microsoft.com/fabric/data-warehouse/ingest-data-into-table
- https://learn.microsoft.com/fabric/data-engineering/how-to-use-notebook

---

## o-2-1-4 — Choose between data stores (Lakehouse vs Warehouse vs Eventhouse vs SQL database)

### Facts

**Key decision matrix (from Microsoft Learn):**

| Capability | SQL database | Data warehouse | Lakehouse | Eventhouse |
|---|---|---|---|---|
| Multi-table transaction support | ✅ | ✅ | ❌ | ⚠️ (partial) |
| Optimized for selective lookups | ✅ | ❌ | ❌ | ✅ |
| Optimized for large scans/aggregations | ⚠️ | ✅ | ✅ | ✅ |
| Write operations engine | T-SQL | T-SQL | Spark (PySpark/SQL/Scala/R) | KQL |
| Read operations engine | T-SQL | T-SQL | T-SQL (read-only endpoint), Spark, KQL | KQL, T-SQL (limited) |
| Unstructured data | ❌ | ❌ | ✅ | ⚠️ |
| Shortcuts support (inbound) | ❌ | ⚠️ | ✅ | ✅ |
| KQL ingestion | ❌ | ❌ | ❌ | ✅ |
| Efficiency of updates/deletes | High | Moderate | Moderate | Low |
| Typical ingestion frequency | Moderate-high | Moderate | Moderate-high | High |
| Small data volumes | ✅ | ✅ | ✅ | ✅ |
| Big data volumes | ❌ | ✅ | ✅ | ✅ |

**When to choose each:**

- **Lakehouse**: Best for big data engineering and data science workloads; diverse data types
  (structured, semi-structured, unstructured); PySpark/Spark SQL preferred write path; flexible
  schema evolution; bronze/silver/gold medallion architecture.
  - SQL analytics endpoint is **read-only** T-SQL over Delta tables; cannot INSERT/UPDATE/DELETE.
  - Only Delta format tables (not raw Parquet/CSV) appear in the SQL analytics endpoint.
  - Fabric auto-registers tables placed in the Tables/ folder without manual CREATE TABLE.

- **Fabric Data Warehouse**: Best for enterprise star/snowflake schema, curated data marts,
  governed BI; primary engine is T-SQL; full multi-table ACID transaction support; DML (INSERT,
  UPDATE, DELETE, MERGE) fully supported; stored procedures, views, functions, materialized views
  (note: materialized views are listed as NOT supported per current T-SQL surface area doc).
  - Data stored in Delta Parquet in OneLake; auto-replicated to OneLake Files.
  - Can ingest via COPY INTO, Pipelines, Dataflows, CTAS, INSERT..SELECT, SELECT INTO.
  - Ideal query runtime: tens of milliseconds+.

- **Eventhouse (KQL database)**: Best for real-time/streaming analytics, time-series, log
  analytics; native ingestion from Eventstream; query language is KQL; subsecond query runtime
  for time-series scans; efficient appends; low efficiency for updates/deletes.
  - OneLake availability (enableable) exports KQL data as Delta to OneLake for cross-engine access.

- **SQL database in Fabric**: Best for small-to-moderate data, OLTP-style transactional
  workloads, translytical apps needing both transactional and analytical access; auto-replicates
  data to OneLake in near real-time as Delta tables for analytics via SQL analytics endpoint.
  - Supports column-level and row-level security; multi-table transactions.
  - Not suited for very large analytical scans (compute customization is low).

**Critical exam distinction:**
- Lakehouse SQL analytics endpoint = **READ-ONLY** (SELECT, CREATE VIEW, CREATE FUNCTION, CREATE
  PROCEDURE allowed, but no INSERT/UPDATE/DELETE/CREATE TABLE).
- Fabric Warehouse = **FULL T-SQL DML** (INSERT, UPDATE, DELETE, MERGE, CREATE/ALTER/DROP TABLE).

### Sources

- https://learn.microsoft.com/azure/architecture/data-guide/technology-choices/fabric-analytical-data-stores
- https://learn.microsoft.com/fabric/data-warehouse/data-warehousing
- https://learn.microsoft.com/fabric/data-engineering/lakehouse-overview
- https://learn.microsoft.com/fabric/data-engineering/lakehouse-sql-analytics-endpoint

---

## o-2-1-5 — Implement OneLake integration for Eventhouse and semantic models

### Facts — Eventhouse / KQL → OneLake

- **OneLake availability** is a per-database or per-table toggle in the Eventhouse details pane.
  When enabled, KQL data is written in **Delta Lake format** to a OneLake path, creating a logical
  copy (not a full replica—data remains in native KQL storage, Delta is maintained in sync).
- Once enabled, the data can be queried by: Direct Lake in Power BI, Fabric Lakehouse notebooks,
  Fabric Warehouse (via shortcut), and the KQL database's own **SQL endpoint** (requires both
  OneLake availability AND schema synchronization to be enabled).
- Other Fabric engines that can access it: Warehouse, Lakehouse, Notebooks.
- If OneLake availability is turned off, the SQL endpoint option disappears from the Analyze data
  with menu.

### Facts — Semantic models → OneLake (OneLake integration)

- **OneLake integration for semantic models** writes imported model table data to Delta tables in
  OneLake automatically — giving downstream consumers (notebooks, warehouses, lakehouse SQL
  endpoint) direct access to the same data that drives Power BI reports.
- Enabled per semantic model in model settings (slider → On → Apply).
- Requires **Power BI Premium P or Fabric F SKU** — not supported on Pro, PPU, or A/EM SKUs.
- Requires model contributor (read/write/explore) permissions to access the exported folder and
  create shortcuts.
- Works with **import-mode** semantic models; exports are in Delta format with performance
  features (e.g., predicate pushdown) enabled.

### Facts — Direct Lake (semantic model OneLake integration)

- **Direct Lake** is a semantic model table storage mode that reads directly from Delta tables in
  OneLake without importing a full data copy.
- Refresh = **framing** only (copies metadata/pointers to latest Delta files, takes a few
  seconds). Import refresh copies all data (can take minutes/hours).
- Direct Lake queries are processed by the **VertiPaq** engine (same as Import mode), so they
  are much faster than DirectQuery.
- "Fallback" behavior: if data can't be served from memory (e.g., very large partitions), Direct
  Lake falls back to DirectQuery against the SQL analytics endpoint.
- Created in Power BI Desktop via OneLake catalog (select Lakehouse or Warehouse → Connect → pick
  tables); storage mode = **Direct Lake on OneLake**.
- Can mix tables from multiple Fabric items (Lakehouse, Warehouse) in one Direct Lake model.

### Sources

- https://learn.microsoft.com/fabric/real-time-intelligence/event-house-onelake-availability
- https://learn.microsoft.com/fabric/enterprise/powerbi/onelake-integration-overview
- https://learn.microsoft.com/fabric/fundamentals/direct-lake-overview
- https://learn.microsoft.com/fabric/fundamentals/direct-lake-power-bi-desktop

---

## o-2-2-1 — Create views, functions, stored procedures (T-SQL in Warehouse)

### Facts

- **Fabric Data Warehouse** supports the full DDL for: CREATE/ALTER/DROP TABLE, CREATE/ALTER/DROP
  VIEW, CREATE/ALTER/DROP PROCEDURE, CREATE/ALTER/DROP FUNCTION, plus GRANT/REVOKE permissions.
- **Lakehouse SQL analytics endpoint** also supports CREATE VIEW, CREATE FUNCTION, CREATE
  PROCEDURE — but **not** INSERT/UPDATE/DELETE/CREATE TABLE.
- **Supported CTE types:** standard, sequential, nested (nested is preview as of doc date).
- **ALTER TABLE** limitations in Warehouse: can ADD nullable columns, DROP COLUMN, add/drop PK/
  UNIQUE/FK constraints (NOT ENFORCED only). ALTER COLUMN is preview. No arbitrary column
  renames — use `sp_rename` instead.
- **MERGE** syntax is generally available in Fabric Warehouse — useful for upsert (SCD type 1).
- **TRUNCATE TABLE** is supported.
- **Session-scoped #temp tables** are supported.
- **NOT supported** (exam pitfall): Triggers, synonyms, `FOR XML`, `FOR JSON` inside subqueries,
  materialized views, `CREATE USER`, `PREDICT`, recursive CTEs, `SET ROWCOUNT`.
- Views and procedures on the Lakehouse SQL analytics endpoint reference underlying Delta tables.
- Data types in Warehouse: most T-SQL types supported; **vector** data type is NOT supported.

### Code — Views / Procedures / Window Functions

```sql
-- Create a view
CREATE VIEW dbo.vw_SalesSummary AS
SELECT c.CustomerName, SUM(f.SalesAmount) AS TotalSales
FROM dbo.FactSales f
JOIN dbo.DimCustomer c ON f.CustomerKey = c.CustomerKey
GROUP BY c.CustomerName;

-- Create a stored procedure
CREATE PROCEDURE dbo.usp_LoadFactSales
AS
BEGIN
  INSERT INTO dbo.FactSales
  SELECT * FROM dbo.stg_Sales;
END;

-- Window function (ROW_NUMBER for deduplication)
SELECT *
FROM (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY ModifiedDate DESC) AS rn
  FROM dbo.Customer
) t
WHERE rn = 1;

-- MERGE (SCD Type 1 upsert)
MERGE INTO dbo.DimCustomer AS tgt
USING dbo.stg_Customer AS src
ON tgt.CustomerKey = src.CustomerKey
WHEN MATCHED THEN
  UPDATE SET tgt.Address = src.Address
WHEN NOT MATCHED THEN
  INSERT (CustomerKey, CustomerName, Address)
  VALUES (src.CustomerKey, src.CustomerName, src.Address);
```

### Sources

- https://learn.microsoft.com/fabric/data-warehouse/tsql-surface-area
- https://learn.microsoft.com/fabric/data-warehouse/data-warehousing
- https://learn.microsoft.com/sql/t-sql/statements/merge-transact-sql?view=fabric

---

## o-2-2-2 — Enrich data (add columns and tables)

### Facts

- **T-SQL (Warehouse/SQL endpoint):** Add computed columns with ALTER TABLE … ADD (nullable
  columns) or via SELECT expressions in CTAS / INSERT..SELECT.
- **Dataflow Gen2 / Power Query:** "Add column" ribbon → Custom column (M formula), Conditional
  column, Column from examples, Index column. Can reference other queries as lookup tables.
- **PySpark (Notebooks):** `df.withColumn("new_col", expr)` for derived columns; `df.join()`
  to enrich with reference/dimension data.
- **Enrichment patterns:** joining dimension tables to add descriptive attributes; adding
  calculated metrics (margin, profit, rate); adding surrogate keys; adding audit columns
  (load_date, source_system).

### Code — PySpark enrichment

```python
from pyspark.sql.functions import col, when, lit, current_timestamp

# Add a derived column
df_enriched = df.withColumn(
    "SalesCategory",
    when(col("SalesAmount") > 1000, "High").otherwise("Low")
).withColumn("LoadDate", current_timestamp())

# Join for enrichment
df_enriched = df_sales.join(df_customer, "CustomerKey", "left")

# Type cast
df_cast = df.withColumn("SalesAmount", col("SalesAmount").cast("double"))
```

### Sources

- https://learn.microsoft.com/fabric/fundamentals/prepare-transform-data
- https://learn.microsoft.com/azure/databricks/pyspark/basics
- https://learn.microsoft.com/fabric/data-warehouse/tsql-surface-area

---

## o-2-2-3 — Implement a star schema (fact/dimension, grain, surrogate keys, SCD types)

### Facts — Star Schema Design

- **Star schema** is the recommended design for Fabric Warehouse (and lakehouse as a logical
  model in semantic models). A fact table at the center, dimension tables as "points".
- Delivers high performance due to fewer joins, likelihood of useful indexes, and lower
  maintenance as new dimensions/facts are added.
- **Fact tables**: contain quantitative measurements (sales amount, quantity, rate). Each row =
  one observation at the defined grain. Contain foreign keys to dimension tables.
- **Dimension tables**: contain descriptive attributes (customer name, product color, date
  attributes). Usually narrower rows but more attributes. Updated less frequently.
- **Integration/staging tables**: intermediate landing zone for raw source data before loading
  dimension/fact tables.
- **Grain**: the level of detail of each fact row (e.g., one row per individual sale line item,
  not per order or per day). Must be defined explicitly before designing the schema.
- **Surrogate keys**: system-generated integer PKs (not business keys) for every dimension table
  row. Enables SCD management; decouples warehouse from source system key changes.
  - Recommend: auto-generated integer column (IDENTITY) in the warehouse.
  - Never truncate/reload a dimension that uses surrogate keys — it invalidates fact table FK
    references.

### Facts — SCD Types

- **SCD Type 0**: No change allowed; attributes are fixed at insert time.
- **SCD Type 1**: Overwrite — update the existing row with new value; no history preserved.
  - Exam note: good for correcting errors, not for historical reporting.
  - Implementation: UPDATE statement (MERGE WHEN MATCHED → UPDATE).
- **SCD Type 2**: New row inserted for each change; old row expired. Preserves full history.
  - Attributes: surrogate key (new row gets new SK), effective_start_date, effective_end_date
    (set to NULL or '9999-12-31' for current), is_current / active_flag boolean.
  - Implementation: MERGE — WHEN MATCHED → expire old row (set end_date, is_current=FALSE);
    INSERT new row with new surrogate key, new start_date, is_current=TRUE.
  - Inferred members: if a fact arrives before the dimension row, insert a placeholder dimension
    row; later treat any attribute arrival as a late-arriving detail (NOT an SCD change).
- **SCD Type 3**: Add a "previous value" column to the existing row; only last two versions
  visible; limited history.
- **Hybrid SCDs**: A single dimension can apply SCD Type 1 to some columns and SCD Type 2 to
  others.

### Facts — Other Dimension Types

- **Role-playing dimension**: same physical dimension table related multiple times to a fact table
  via different foreign keys (e.g., `Airport` dimension used as both DepartureAirport and
  ArrivalAirport).
- **Junk dimension**: consolidates many low-cardinality flag/indicator columns into one dimension
  table; reduces fact table width and number of FK columns.

### Code — SCD Type 2 MERGE pattern (T-SQL)

```sql
-- Step 1: Expire changed rows
UPDATE tgt
SET tgt.EffectiveEndDate = GETDATE(), tgt.IsCurrent = 0
FROM dbo.DimCustomer tgt
JOIN dbo.stg_Customer src ON tgt.CustomerKey = src.CustomerKey
WHERE tgt.IsCurrent = 1
  AND (tgt.Address <> src.Address);   -- SCD2 attribute changed

-- Step 2: Insert new version
INSERT INTO dbo.DimCustomer
  (CustomerKey, CustomerName, Address, EffectiveStartDate, EffectiveEndDate, IsCurrent)
SELECT
  src.CustomerKey, src.CustomerName, src.Address,
  GETDATE(), NULL, 1
FROM dbo.stg_Customer src
JOIN dbo.DimCustomer tgt ON src.CustomerKey = tgt.CustomerKey
WHERE tgt.IsCurrent = 0 AND tgt.EffectiveEndDate = GETDATE();
```

### Sources

- https://learn.microsoft.com/fabric/data-warehouse/dimensional-modeling-overview
- https://learn.microsoft.com/fabric/data-warehouse/tables
- https://learn.microsoft.com/fabric/data-warehouse/dimensional-modeling-dimension-tables
- https://learn.microsoft.com/fabric/data-warehouse/dimensional-modeling-fact-tables
- https://learn.microsoft.com/fabric/data-warehouse/dimensional-modeling-load-tables
- https://learn.microsoft.com/fabric/iq/plan/powertable-concept-slowly-changing-dimensions

---

## o-2-2-4 — Data quality operations (deduplicate, missing/null, type conversion, filter, aggregate, merge/join, denormalize)

### Facts — Data Quality in PySpark (Notebooks)

- **Remove duplicates**: `df.distinct()` removes fully duplicate rows; `df.dropDuplicates(["col1","col2"])` deduplicates by subset.
- **Handle nulls**: `df.na.drop()` or `df.na.drop("any")` — drop rows with any null;
  `df.na.drop("all")` — drop only rows where ALL values are null;
  `df.na.drop("any", subset=["col1","col2"])` — scoped to specific columns.
- **Fill nulls**: `df.na.fill(0, subset=["amount"])` — fill specific columns with a value.
- **Type conversion**: `df.withColumn("col", col("col").cast("double"))` or
  `.cast("timestamp")`.
- **Filter**: `df.filter(col("region") == "US")` or `.where()` (synonymous);
  multi-condition: `df.filter((col("a") > 0) & (col("b") < 100))`.
- **Aggregate**: `df.groupBy("Region").agg(sum("Sales").alias("TotalSales"), count("*").alias("RowCount"))`.
- **Join/merge**: `df_sales.join(df_customer, "CustomerKey", "inner")` — join types: inner,
  left, right, full, left_anti, left_semi.
- **Denormalize**: flatten struct/array with `explode()`, `select(col("nested.field"))`, or
  `df.select("*", col("struct_col.*"))`.

### Facts — Data Quality in Dataflow Gen2 / Power Query (M)

- **Remove duplicates**: Home → Remove Rows → Remove Duplicates (Table.Distinct).
- **Handle nulls**: Replace Values (null → 0); Remove Rows with errors/blanks.
- **Type conversion**: Transform → Data Type → pick type (Text, Number, Date, etc.).
- **Filter rows**: AutoFilter dropdowns or Table.SelectRows with condition.
- **Add conditional column**: Add Column → Conditional Column (M equivalent: `if ... then ... else`).
- **Merge queries**: Home → Merge Queries (JOIN operation) — left outer, inner, right outer, full
  outer, left anti, right anti.
- **Append queries**: Home → Append Queries (UNION).
- **Group by / Aggregate**: Transform → Group By.

### Facts — Data Quality in T-SQL (Warehouse)

```sql
-- Remove duplicates (keep latest per CustomerID)
WITH dedup AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY ModifiedDate DESC) AS rn
  FROM dbo.Customer
)
DELETE FROM dedup WHERE rn > 1;

-- Handle NULLs
SELECT COALESCE(SalesAmount, 0) AS SalesAmount FROM dbo.FactSales;
SELECT ISNULL(Region, 'Unknown') AS Region FROM dbo.FactSales;

-- Type conversion
SELECT CAST(OrderDate AS DATE), CONVERT(VARCHAR, Amount, 1) FROM dbo.Orders;

-- Filter
SELECT * FROM dbo.FactSales WHERE SalesAmount > 0 AND Region = 'West';

-- Aggregate / GROUP BY
SELECT Region, SUM(SalesAmount) AS Total, COUNT(*) AS Rows
FROM dbo.FactSales
GROUP BY Region
HAVING SUM(SalesAmount) > 10000;
```

### Facts — Merge/JOIN patterns

- T-SQL `MERGE` supports insert, update, delete in one atomic statement (GA in Fabric Warehouse).
- PySpark join types map directly: inner ↔ INNER JOIN, left ↔ LEFT OUTER JOIN, etc.
- Power Query: Merge Queries covers the same join types plus left anti (equivalent to NOT EXISTS).

### Sources

- https://learn.microsoft.com/azure/databricks/pyspark/basics
- https://learn.microsoft.com/fabric/fundamentals/prepare-transform-data
- https://learn.microsoft.com/fabric/data-warehouse/tsql-surface-area
- https://learn.microsoft.com/en-us/power-query/power-query-what-is-power-query

---

## o-2-3-1 — Visual Query Editor (Power Query / warehouse visual query; query folding)

### Facts

- **Visual query editor** in Fabric Warehouse and SQL analytics endpoint (lakehouse) provides a
  no-code, drag-and-drop query authoring experience using the Power Query diagram view.
- Access: Warehouse ribbon → New visual query.
- Tables are dragged from the Object Explorer onto the canvas; no SQL code needed.
- Queries are **auto-saved** every few seconds (saving indicator in tab).
- The visual query editor generates a T-SQL SELECT statement (view the SQL with "View SQL").
- **Limitations:**
  - Only DQL/SELECT statements — no DDL or DML (INSERT/UPDATE/DELETE).
  - `ORDER BY` is not supported in "Visualize Results."
  - Warehouses with > 750,000 combined objects (tables + views + columns) are not supported.
  - Only Power Query operations that support **query folding** are available.
- **Query folding**: Power Query mechanism that translates M steps into source-native queries
  (T-SQL for warehouse) and pushes them to the source. Reduces data movement. Step-level folding
  indicators in the UI show which steps fold vs. execute in Mashup Engine.
- When a step cannot be folded, a banner message appears: "The query is not supported as a
  warehouse view, since it cannot be fully translated to SQL."
- Workspace Viewer role or shared recipients cannot move queries from "My queries" to "Shared
  queries."
- Queries can be saved to **My queries** (personal) or **Shared queries** (workspace-shared).

### Sources

- https://learn.microsoft.com/fabric/data-warehouse/visual-query-editor
- https://learn.microsoft.com/fabric/data-warehouse/query-warehouse
- https://learn.microsoft.com/en-us/power-query/step-folding-indicators

---

## o-2-3-2 — SQL queries (T-SQL SELECT / WHERE / GROUP BY / JOIN / window functions)

### Facts

- Fabric Warehouse and Lakehouse SQL analytics endpoint support T-SQL SELECT with:
  - `WHERE` clause: filtering rows; supports `=`, `<>`, `>`, `<`, `BETWEEN`, `IN`, `LIKE`,
    `IS NULL`, `IS NOT NULL`, `AND`/`OR`/`NOT`.
  - `GROUP BY` + aggregate functions: `SUM()`, `AVG()`, `COUNT()`, `MIN()`, `MAX()`,
    `COUNT(DISTINCT ...)`.
  - `HAVING`: filter on aggregated results.
  - `JOIN` types: `INNER JOIN`, `LEFT OUTER JOIN`, `RIGHT OUTER JOIN`, `FULL OUTER JOIN`,
    `CROSS JOIN`. Note: `CROSS APPLY` / `OUTER APPLY` may have limited support.
  - **Subqueries** and **CTEs** (standard, sequential, nested-preview).
  - `ORDER BY` (with `TOP` or `OFFSET … FETCH NEXT`).
- **Window functions** (fully supported in Warehouse/SQL endpoint):
  - Ranking: `ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)` — unique sequential numbers;
    `RANK()` — same rank for ties, gaps; `DENSE_RANK()` — same rank for ties, no gaps;
    `NTILE(n)` — distributes rows into n buckets.
  - Aggregate windows: `SUM() OVER(…)`, `AVG() OVER(…)`, `COUNT() OVER(…)`.
  - Analytic: `LAG(col, n)`, `LEAD(col, n)` — access preceding/following row values.
  - `FIRST_VALUE()`, `LAST_VALUE()`.
- **Window frames**: `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` etc.
- NOT supported in Warehouse: FOR XML, triggers, synonyms, materialized views, recursive CTEs.

### Code — T-SQL patterns

```sql
-- Basic SELECT/WHERE/GROUP BY
SELECT Region, SUM(SalesAmount) AS TotalSales, COUNT(*) AS NumOrders
FROM dbo.FactSales
WHERE OrderDate >= '2024-01-01'
GROUP BY Region
HAVING SUM(SalesAmount) > 50000
ORDER BY TotalSales DESC;

-- JOINs
SELECT f.OrderKey, c.CustomerName, p.ProductName, f.SalesAmount
FROM dbo.FactSales f
INNER JOIN dbo.DimCustomer c ON f.CustomerKey = c.CustomerKey
LEFT OUTER JOIN dbo.DimProduct p ON f.ProductKey = p.ProductKey;

-- Window function: running total
SELECT OrderDate, SalesAmount,
       SUM(SalesAmount) OVER (ORDER BY OrderDate
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS RunningTotal
FROM dbo.FactSales;

-- ROW_NUMBER for dedup / top-N per group
SELECT CustomerName, SalesAmount
FROM (
  SELECT c.CustomerName, f.SalesAmount,
         ROW_NUMBER() OVER (PARTITION BY f.CustomerKey ORDER BY f.SalesAmount DESC) AS rn
  FROM dbo.FactSales f JOIN dbo.DimCustomer c ON f.CustomerKey = c.CustomerKey
) t
WHERE rn = 1;
```

### Sources

- https://learn.microsoft.com/fabric/data-warehouse/tsql-surface-area
- https://learn.microsoft.com/fabric/data-warehouse/query-warehouse
- https://learn.microsoft.com/sql/t-sql/functions/row-number-transact-sql?view=fabric

---

## o-2-3-3 — KQL queries (pipe syntax: where / summarize / project / extend / bin)

### Facts

- **KQL (Kusto Query Language)** is the native query language for Fabric Eventhouse (KQL
  databases) and is also used in Azure Monitor, Microsoft Sentinel, and ADX.
- **Pipe syntax**: queries are chains of operators separated by `|` (pipe). Each operator
  receives a table and returns a table.
  ```
  TableName | operator1 | operator2 | operator3
  ```
- **Core operators for DP-600:**
  - `where` — filter rows: `| where EventType == "Storm" and StartTime > ago(30d)`
  - `project` — select/rename columns (drops all others): `| project City, EventType, StartTime`
  - `project-away` — drop named columns (keep the rest).
  - `extend` — add a computed column without dropping others:
    `| extend Duration = EndTime - StartTime`
  - `summarize` — aggregate; collapses to one row per unique group-by key:
    `| summarize EventCount = count() by EventType`
  - `bin()` — rounds value down to nearest multiple; used to bucket time/numeric values for
    time-series summarize:
    `| summarize EventCount = count() by bin(StartTime, 7d)`
  - `sort by` / `order by` — sort results (synonymous).
  - `take` / `limit` — return first N rows (for exploration).
  - `render` — visualize results (timechart, barchart, piechart) — exam note: render is a
    display directive, not a data transformation.
  - `join` — join two tables; supports inner, leftouter, rightouter, fullouter, leftanti, etc.
  - `make-series` — create a series array for time-series analysis.
- **Time functions**: `ago(30d)`, `now()`, `datetime()`, `startofday()`, `startofmonth()`.
- **String functions**: `contains`, `startswith`, `has`, `tostring()`.
- **Type casting**: `toint()`, `tolong()`, `todatetime()`, `tostring()`, `todynamic()`.
- `summarize` output columns: only columns explicitly listed in the `by` clause or aggregation
  expression are kept. (Exam pitfall: trying to sort by a column that was not in the summarize
  will fail.)

### Code — KQL patterns

```kusto
// Basic filter and project
StormEvents
| where StartTime between (datetime(2007-01-01) .. datetime(2007-12-31))
    and DamageProperty > 0
| project EventType, State, StartTime, DamageProperty

// Summarize with bin (weekly time series)
StormEvents
| where StartTime between (datetime(2007-01-01) .. datetime(2007-12-31))
    and DamageCrops > 0
| summarize EventCount = count() by bin(StartTime, 7d)
| render timechart

// Extend to add computed column
StormEvents
| extend Duration = EndTime - StartTime
| project EventType, Duration
| summarize AvgDuration = avg(Duration) by EventType
| sort by AvgDuration desc

// Count by category
StormEvents
| summarize EventCount = count() by EventType
| order by EventCount desc
| take 10
```

### Sources

- https://learn.microsoft.com/kusto/query/tutorials/use-aggregation-functions?view=microsoft-fabric
- https://learn.microsoft.com/kusto/query/summarize-operator?view=microsoft-fabric
- https://learn.microsoft.com/kusto/query/bin-function?view=microsoft-fabric
- https://learn.microsoft.com/fabric/real-time-intelligence/event-house-onelake-availability
- https://learn.microsoft.com/dynamics365/business-central/dev-itpro/administration/telemetry-analyze-with-kql

---

## o-2-3-4 — DAX measures (SUM / CALCULATE / DIVIDE / FILTER — brief)

### Facts

- **DAX (Data Analysis Expressions)** is the formula language for Power BI semantic models,
  Analysis Services, and Excel Power Pivot.
- **Measures** are dynamic calculation formulas whose result changes based on **filter context**
  (row/column headers, slicers, report filters). A measure has no inherent value — it is
  evaluated per cell in a report visual.
- **Basic aggregations:** `SUM()`, `AVERAGE()`, `COUNT()`, `DISTINCTCOUNT()`, `MIN()`, `MAX()`,
  `COUNTROWS()`.
- **`CALCULATE(expression, [filters])`**: the most important DAX function. Evaluates `expression`
  in a **modified filter context** defined by the filter arguments. Filter arguments can add,
  replace, or remove filters.
  - `CALCULATE(SUM(Sales[Amount]), 'Product'[Color] = "Blue")` — evaluates sum only for blue
    products.
  - `CALCULATE(SUM(Sales[Amount]), REMOVEFILTERS('Sales Order'[Channel]))` — removes the Channel
    filter (used for % of total patterns).
  - `CALCULATE(SUM(Sales[Amount]), ALLEXCEPT(Customer, Customer[CustomerKey]))` — context
    transition pattern in a calculated column.
- **`DIVIDE(numerator, denominator, [alternateResult])`**: safe division; returns alternateResult
  (default = BLANK()) when denominator is 0. Always prefer DIVIDE over `/` operator for measures.
  ```dax
  Profit Margin = DIVIDE([Gross Profit], [Revenue])
  ```
- **`FILTER(table, condition)`**: returns a filtered table (used as an argument to CALCULATE or
  other table functions); NOT a standalone measure.
  ```dax
  High Value Sales = CALCULATE(SUM(Sales[Amount]), FILTER(Sales, Sales[Amount] > 1000))
  ```
- **`TOTALYTD`, `TOTALMTD`, `TOTALQTD`**: time intelligence functions (need a proper date table
  marked as date table).
  ```dax
  YTD Sales = TOTALYTD(SUM(Sales[SaleAmount]), 'Date'[Date])
  ```
- **Exam note**: measures live in the semantic model (not in warehouse/lakehouse tables); they
  are evaluated at query time, not stored. Deep DAX is covered in Domain 3; Domain 2 focus is
  on basic measure patterns used in data preparation / model building context.

### Code — DAX patterns

```dax
-- Basic sum measure
Total Sales = SUM(Sales[SalesAmount])

-- % of total using CALCULATE + REMOVEFILTERS
Revenue % Total Channel =
DIVIDE(
    SUM(Sales[SalesAmount]),
    CALCULATE(SUM(Sales[SalesAmount]), REMOVEFILTERS('Sales Order'[Channel]))
)

-- Conditional CALCULATE
Blue Revenue =
CALCULATE(
    SUM(Sales[SalesAmount]),
    'Product'[Color] = "Blue"
)

-- Safe divide with alternate result
Profit Margin = DIVIDE([Gross Profit], [Total Revenue], 0)

-- FILTER as table argument
High Value Customers =
CALCULATE(
    COUNTROWS(Customer),
    FILTER(Customer, Customer[AnnualRevenue] > 100000)
)
```

### Sources

- https://learn.microsoft.com/dax/calculate-function-dax
- https://learn.microsoft.com/dax/divide-function-dax
- https://learn.microsoft.com/dax/dax-overview
- https://learn.microsoft.com/power-bi/create-reports/copilot-evaluate-data

---

## Appendix — Cross-Cutting Facts to Know

| Topic | Key Testable Fact |
|---|---|
| Delta format | Universal table format across all Fabric compute engines; Parquet files + transaction log |
| OneLake | Single storage per Fabric tenant; ADLS Gen2-compatible; all Fabric items write to OneLake |
| Lakehouse SQL endpoint write | READ-ONLY — no INSERT/UPDATE/DELETE/CREATE TABLE |
| Warehouse write | Full T-SQL DML: INSERT, UPDATE, DELETE, MERGE, CTAS, SELECT INTO |
| Shortcuts | Zero-copy pointers to external data; no ETL; Delta shortcuts queryable from SQL endpoint |
| Dataflow Gen2 output | Can write to Lakehouse tables OR Warehouse tables |
| COPY INTO sources | Azure Blob Storage / ADLS Gen2 only (not on-premises) |
| Gateway (personal mode) | Single user, scheduled refresh only, no DirectQuery/Live Connection |
| VNet gateway | Microsoft-managed, Premium/F capacity required, no on-premises software |
| Direct Lake refresh | Framing only (metadata) — seconds, not full data copy |
| OneLake availability (KQL) | Enables Delta export from KQL DB; required for Direct Lake from Eventhouse |
| SCD Type 1 | Overwrite, no history |
| SCD Type 2 | New row + surrogate key + effective dates + is_current flag |
| KQL summarize pitfall | Output drops all columns not in `by` or aggregation |
| bin() | Floor to nearest multiple; required for time-series `summarize … by bin(timestamp, 1h)` |
| CALCULATE | Modifies filter context; most important DAX function |
| DIVIDE | Safe division; use instead of `/` to avoid divide-by-zero errors |
| Visual query editor | SELECT only (no DML), only fold-able PQ operations; <750K objects limit |

---

*End of Domain 2 research notes. Total unique source URLs: 37.*
