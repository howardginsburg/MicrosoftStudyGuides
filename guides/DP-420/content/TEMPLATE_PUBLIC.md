# DP-420 Study Guide — PUBLIC EDITION — CONTENT TEMPLATE CONTRACT

You are authoring ONE domain of a **shareable, clean-room** DP-420 study guide as an **HTML fragment**. A separate build step wraps it with CSS/JS and injects original SVG diagrams.

## ⛔ CLEAN-ROOM SOURCING RULE (most important)
- Ground **every** fact ONLY in your assigned **public Microsoft Learn source pack** (`learn_src_dN.md`) — gathered from public Microsoft Learn documentation.
- Do **NOT** use, reference, quote, or paraphrase any PowerPoint/instructor-deck material. If a fact isn't supported by the public source pack, either omit it or keep it to well-known, non-copyrightable product facts — never invent specifics.
- Paraphrase in your own words. Never paste passages from Learn verbatim; state facts plainly.

## Heading hierarchy (drives the auto Table of Contents)
- `<h1>` = the Domain (one per file). `<h2>` = skill group. `<h3>` = individual objective.
- EVERY h1/h2/h3 MUST have the stable `id` specified in the outline below.

## Wrapper structure
```html
<section class="domain" id="domainN" data-domain="N">
  <h1 id="dN">Domain N — ... <span class="weight">35–40%</span></h1>
  <p class="domain-intro">1–3 sentence orientation.</p>
  <section class="skillgroup" id="sg-N-1">
    <h2 id="g-N-1">N.1 ...</h2>
    <section class="objective" id="obj-N-1-1" data-skill="...">
      <h3 id="o-N-1-1">N.1.1 ...</h3>
      ...blocks...
    </section>
  </section>
</section>
```

## Blocks INSIDE each `<section class="objective">` (in order; omit a block only if truly N/A)
1. **Concept** — `<div class="concept"><p>...</p></div>` — what it is / why / how. 1–3 short paragraphs, own words.
2. **Key facts** — `<div class="facts"><h4>Key facts</h4><ul><li>...</li></ul></div>` — testable specifics (settings, RU costs, limits, defaults, steps).
3. **Diagram** (where a visual genuinely helps) — reference an ORIGINAL SVG from the diagram library BY ID:
   `<figure class="diagram" data-svg="DIAGRAM-ID"><figcaption>Caption in your words.</figcaption></figure>`
   Use only ids listed in `diagram_catalog.md`. Do NOT write raster `<img>` tags. The build injects the inline SVG.
4. **Code** (for SQL/SDK/JS/PowerShell/CLI/JSON objectives) — `<div class="code"><pre><code class="lang-sql">...</code></pre></div>`.
   Languages: `lang-sql` (Cosmos DB NoSQL query), `lang-csharp`, `lang-javascript`, `lang-python`, `lang-json`, `lang-powershell`, `lang-bash`, `lang-bicep`, `lang-kql`, `lang-yaml`. HTML-escape `<`, `>`, `&` inside code. Author minimal, correct, ORIGINAL examples.
5. **Callouts** (optional): `<div class="callout key">`, `<div class="callout tip">`, `<div class="callout warn">` with `<b>Key:/Tip:/Gotcha:</b>`.
6. **Exam tips & gotchas** — `<div class="tips"><h4>Exam tips &amp; gotchas</h4><ul><li>...</li></ul></div>` — 2–5 distinguishing points.
7. **Practice** — `<div class="practice"><h4>Practice</h4>` then 2–4 ORIGINAL questions:
```html
<details class="q"><summary><b>Q1.</b> Scenario/question?</summary>
<div class="answer"><b>Answer:</b> correct choice. <em>Why:</em> concise rationale.</div></details>
```
then `</div>`. Questions must be your own original scenarios — never reproduce real exam items.
8. **Learn more (citations)** — REQUIRED, last block in each objective:
```html
<div class="learn-more"><b>Learn more</b>
<ul>
  <li><a href="FULL_LEARN_URL">Page title</a></li>
</ul></div>
```
Use the real public Microsoft Learn URLs recorded in your source pack for this objective (1–3 links).

## Writing rules
- Technical accuracy is paramount; follow the source pack's specifics exactly (RU cost model, partition key rules, consistency levels, backup modes, RBAC).
- Depth: thorough but tight — precise bullets and short paragraphs.
- Cover EVERY objective in the outline; don't merge or skip.
- Include ≥1 code example for every SQL query, SDK, server-side JavaScript, indexing, and DevOps objective.
- SCOPE GUARD: DP-420 centers on the **API for NoSQL**. Mention other APIs (MongoDB, Cassandra, Gremlin, Table) only where the blueprint explicitly implies them; do not drift off-syllabus.
- Output ONLY the HTML fragment (one top-level `<section class="domain">…</section>`). No markdown, no code fences, no commentary.

## Objective outline & required IDs

### Domain 1 — Design and implement data models (35–40%) → domain1.html, id="domain1"
- h2 `g-1-1` "1.1 Design and implement a non-relational data model for Azure Cosmos DB for NoSQL" (sg-1-1)
  - `o-1-1-1` 1.1.1 Store multiple entity types in the same container
  - `o-1-1-2` 1.1.2 Store multiple related entities in the same document
  - `o-1-1-3` 1.1.3 Develop a model that denormalizes data across documents
  - `o-1-1-4` 1.1.4 Develop a design by referencing between documents
  - `o-1-1-5` 1.1.5 Identify partition key, id, and unique keys
  - `o-1-1-6` 1.1.6 Identify data and associated access patterns
  - `o-1-1-7` 1.1.7 Specify a default time to live (TTL) on a container for a transactional store
  - `o-1-1-8` 1.1.8 Develop a design for versioning documents
  - `o-1-1-9` 1.1.9 Develop a design for document schema versioning
- h2 `g-1-2` "1.2 Design a data partitioning strategy for Azure Cosmos DB for NoSQL" (sg-1-2)
  - `o-1-2-1` 1.2.1 Choose a partitioning strategy based on a specific workload
  - `o-1-2-2` 1.2.2 Choose a partition key
  - `o-1-2-3` 1.2.3 Plan for transactions when choosing a partition key
  - `o-1-2-4` 1.2.4 Evaluate the cost of using a cross-partition query
  - `o-1-2-5` 1.2.5 Calculate and evaluate data distribution based on partition key selection
  - `o-1-2-6` 1.2.6 Calculate and evaluate throughput distribution based on partition key selection
  - `o-1-2-7` 1.2.7 Construct and implement a synthetic partition key
  - `o-1-2-8` 1.2.8 Design and implement a hierarchical partition key
  - `o-1-2-9` 1.2.9 Design partitioning for workloads that require multiple partition keys
- h2 `g-1-3` "1.3 Plan and implement sizing and scaling for a database created with Azure Cosmos DB" (sg-1-3)
  - `o-1-3-1` 1.3.1 Evaluate the throughput and data storage requirements for a specific workload
  - `o-1-3-2` 1.3.2 Choose between serverless, provisioned, and free tier
  - `o-1-3-3` 1.3.3 Choose when to use database-level provisioned throughput
  - `o-1-3-4` 1.3.4 Design for granular scale units and resource governance
  - `o-1-3-5` 1.3.5 Evaluate the cost of the global distribution of data
  - `o-1-3-6` 1.3.6 Configure throughput for Azure Cosmos DB by using the Azure portal
- h2 `g-1-4` "1.4 Implement client connectivity options in the Azure Cosmos DB SDK" (sg-1-4)
  - `o-1-4-1` 1.4.1 Choose a connectivity mode (gateway versus direct)
  - `o-1-4-2` 1.4.2 Implement a connectivity mode
  - `o-1-4-3` 1.4.3 Create a connection to a database
  - `o-1-4-4` 1.4.4 Enable offline development by using the Azure Cosmos DB emulator
  - `o-1-4-5` 1.4.5 Handle connection errors
  - `o-1-4-6` 1.4.6 Implement a singleton for the client
  - `o-1-4-7` 1.4.7 Specify a region for global distribution
  - `o-1-4-8` 1.4.8 Configure client-side threading and parallelism options
  - `o-1-4-9` 1.4.9 Enable SDK logging
- h2 `g-1-5` "1.5 Implement data access by using the SQL language for Azure Cosmos DB for NoSQL" (sg-1-5)
  - `o-1-5-1` 1.5.1 Implement queries that use arrays, nested objects, aggregation, and ordering
  - `o-1-5-2` 1.5.2 Implement a correlated subquery
  - `o-1-5-3` 1.5.3 Implement queries that use array and type-checking functions
  - `o-1-5-4` 1.5.4 Implement queries that use mathematical, string, and date functions
  - `o-1-5-5` 1.5.5 Implement queries based on variable data
- h2 `g-1-6` "1.6 Implement data access by using Azure Cosmos DB for NoSQL SDKs" (sg-1-6)
  - `o-1-6-1` 1.6.1 Choose when to use a point operation versus a query operation
  - `o-1-6-2` 1.6.2 Implement a point operation that creates, updates, and deletes items
  - `o-1-6-3` 1.6.3 Implement an update by using a patch operation
  - `o-1-6-4` 1.6.4 Manage multi-item transactions using SDK Transactional Batch
  - `o-1-6-5` 1.6.5 Perform a multi-item load using Bulk Support in the SDK
  - `o-1-6-6` 1.6.6 Implement optimistic concurrency control using ETags
  - `o-1-6-7` 1.6.7 Override default consistency by using query request options
  - `o-1-6-8` 1.6.8 Implement session consistency by using session tokens
  - `o-1-6-9` 1.6.9 Implement a query operation that includes pagination
  - `o-1-6-10` 1.6.10 Implement a query operation by using a continuation token
  - `o-1-6-11` 1.6.11 Handle transient errors and 429s
  - `o-1-6-12` 1.6.12 Specify TTL for an item
  - `o-1-6-13` 1.6.13 Retrieve and use query metrics
- h2 `g-1-7` "1.7 Implement server-side programming in Azure Cosmos DB for NoSQL by using JavaScript" (sg-1-7)
  - `o-1-7-1` 1.7.1 Write, deploy, and call a stored procedure
  - `o-1-7-2` 1.7.2 Design stored procedures to work with multiple items within the same logical partition transactionally
  - `o-1-7-3` 1.7.3 Implement and call triggers
  - `o-1-7-4` 1.7.4 Implement a user-defined function

### Domain 2 — Design and implement data distribution (5–10%) → domain2.html, id="domain2"
- h2 `g-2-1` "2.1 Design and implement a replication strategy for Azure Cosmos DB" (sg-2-1)
  - `o-2-1-1` 2.1.1 Choose when to distribute data
  - `o-2-1-2` 2.1.2 Define automatic failover policies for regional failure for Azure Cosmos DB for NoSQL
  - `o-2-1-3` 2.1.3 Perform manual failovers to move single master write regions
  - `o-2-1-4` 2.1.4 Choose a consistency model
  - `o-2-1-5` 2.1.5 Identify use cases for different consistency models
  - `o-2-1-6` 2.1.6 Evaluate the impact of consistency model choices on availability and associated RU cost
  - `o-2-1-7` 2.1.7 Evaluate the impact of consistency model choices on performance and latency
  - `o-2-1-8` 2.1.8 Specify application connections to replicated data
- h2 `g-2-2` "2.2 Design and implement multi-region writes" (sg-2-2)
  - `o-2-2-1` 2.2.1 Choose when to use multi-region writes
  - `o-2-2-2` 2.2.2 Implement multi-region writes
  - `o-2-2-3` 2.2.3 Implement a custom conflict resolution policy for Azure Cosmos DB for NoSQL

### Domain 3 — Integrate an Azure Cosmos DB solution (5–10%) → domain3.html, id="domain3"
- h2 `g-3-1` "3.1 Enable Azure Cosmos DB analytical workloads" (sg-3-1)
  - `o-3-1-1` 3.1.1 Configure Azure Cosmos DB Mirroring for Microsoft Fabric
  - `o-3-1-2` 3.1.2 Choose between Azure Cosmos DB Mirroring and the Azure Cosmos DB Spark connector
  - `o-3-1-3` 3.1.3 Enable the analytical store on a container
  - `o-3-1-4` 3.1.4 Enable a connection to an analytical store and query from Azure Synapse Spark or Azure Synapse SQL
  - `o-3-1-5` 3.1.5 Perform a query against the transactional store from Spark
  - `o-3-1-6` 3.1.6 Write data back to the transactional store from Spark
  - `o-3-1-7` 3.1.7 Implement Change Data Capture in the Azure Cosmos DB analytical store
  - `o-3-1-8` 3.1.8 Implement time travel in Warehouse in Microsoft Fabric
- h2 `g-3-2` "3.2 Implement solutions across services" (sg-3-2)
  - `o-3-2-1` 3.2.1 Integrate events with other applications by using Azure Functions and Azure Event Hubs
  - `o-3-2-2` 3.2.2 Denormalize data by using Change Feed and Azure Functions
  - `o-3-2-3` 3.2.3 Enforce referential integrity by using Change Feed and Azure Functions
  - `o-3-2-4` 3.2.4 Aggregate data by using Change Feed and Azure Functions, including reporting
  - `o-3-2-5` 3.2.5 Archive data by using Change Feed and Azure Functions
  - `o-3-2-6` 3.2.6 Implement Azure AI Search for an Azure Cosmos DB solution

### Domain 4 — Optimize an Azure Cosmos DB solution (15–20%) → domain4.html, id="domain4"
- h2 `g-4-1` "4.1 Optimize query performance when using the API for Azure Cosmos DB for NoSQL" (sg-4-1)
  - `o-4-1-1` 4.1.1 Adjust indexes on the database
  - `o-4-1-2` 4.1.2 Calculate the cost of the query
  - `o-4-1-3` 4.1.3 Retrieve request unit cost of a point operation or query
  - `o-4-1-4` 4.1.4 Implement Azure Cosmos DB integrated cache
- h2 `g-4-2` "4.2 Design and implement change feeds for Azure Cosmos DB for NoSQL" (sg-4-2)
  - `o-4-2-1` 4.2.1 Develop an Azure Functions trigger to process a change feed
  - `o-4-2-2` 4.2.2 Consume a change feed from within an application by using the SDK
  - `o-4-2-3` 4.2.3 Manage the number of change feed instances by using the change feed estimator
  - `o-4-2-4` 4.2.4 Implement denormalization by using a change feed
  - `o-4-2-5` 4.2.5 Implement referential enforcement by using a change feed
  - `o-4-2-6` 4.2.6 Implement aggregation persistence by using a change feed
  - `o-4-2-7` 4.2.7 Implement data archiving by using a change feed
- h2 `g-4-3` "4.3 Define and implement an indexing strategy for Azure Cosmos DB for NoSQL" (sg-4-3)
  - `o-4-3-1` 4.3.1 Choose when to use a read-heavy versus write-heavy index strategy
  - `o-4-3-2` 4.3.2 Choose an appropriate index type
  - `o-4-3-3` 4.3.3 Configure a custom indexing policy by using the Azure portal
  - `o-4-3-4` 4.3.4 Implement a composite index
  - `o-4-3-5` 4.3.5 Optimize index performance

### Domain 5 — Maintain an Azure Cosmos DB solution (25–30%) → domain5.html, id="domain5"
- h2 `g-5-1` "5.1 Monitor and troubleshoot an Azure Cosmos DB solution" (sg-5-1)
  - `o-5-1-1` 5.1.1 Evaluate response status code and failure metrics
  - `o-5-1-2` 5.1.2 Monitor the Normalized RU Consumption metric by using Azure Monitor
  - `o-5-1-3` 5.1.3 Monitor server-side latency metrics by using Azure Monitor
  - `o-5-1-4` 5.1.4 Monitor data replication in relation to latency and availability
  - `o-5-1-5` 5.1.5 Configure Azure Monitor alerts for Azure Cosmos DB
  - `o-5-1-6` 5.1.6 Implement and query Azure Monitor resource logs for Azure Cosmos DB
  - `o-5-1-7` 5.1.7 Monitor throughput across partitions
  - `o-5-1-8` 5.1.8 Monitor distribution of data across partitions
  - `o-5-1-9` 5.1.9 Monitor security by using logging and auditing
- h2 `g-5-2` "5.2 Implement backup and restore for an Azure Cosmos DB solution" (sg-5-2)
  - `o-5-2-1` 5.2.1 Choose between periodic and continuous backup
  - `o-5-2-2` 5.2.2 Configure periodic backup
  - `o-5-2-3` 5.2.3 Configure continuous backup and point-in-time restore
  - `o-5-2-4` 5.2.4 Locate a restore point for a point-in-time restore
  - `o-5-2-5` 5.2.5 Restore a database or container from a restore point
- h2 `g-5-3` "5.3 Implement security for an Azure Cosmos DB solution" (sg-5-3)
  - `o-5-3-1` 5.3.1 Choose between service-managed and customer-managed encryption keys
  - `o-5-3-2` 5.3.2 Configure network-level access control for Azure Cosmos DB
  - `o-5-3-3` 5.3.3 Configure data encryption for Azure Cosmos DB
  - `o-5-3-4` 5.3.4 Manage control plane access to Azure Cosmos DB by using Azure RBAC
  - `o-5-3-5` 5.3.5 Manage control plane access to Azure Cosmos DB Data Explorer by using Azure RBAC
  - `o-5-3-6` 5.3.6 Manage data plane access to Azure Cosmos DB by using Microsoft Entra ID
  - `o-5-3-7` 5.3.7 Configure cross-origin resource sharing (CORS) settings
  - `o-5-3-8` 5.3.8 Manage account keys by using Azure Key Vault
  - `o-5-3-9` 5.3.9 Implement customer-managed keys for encryption
  - `o-5-3-10` 5.3.10 Implement Always Encrypted
- h2 `g-5-4` "5.4 Implement data movement for an Azure Cosmos DB solution" (sg-5-4)
  - `o-5-4-1` 5.4.1 Choose a data movement strategy
  - `o-5-4-2` 5.4.2 Move data by using client SDK bulk operations
  - `o-5-4-3` 5.4.3 Move data by using Azure Data Factory and Azure Synapse pipelines
  - `o-5-4-4` 5.4.4 Move data by using a Kafka connector
  - `o-5-4-5` 5.4.5 Move data by using Azure Stream Analytics
  - `o-5-4-6` 5.4.6 Move data by using the Azure Cosmos DB Spark connector
  - `o-5-4-7` 5.4.7 Configure Azure Cosmos DB as a custom endpoint for an Azure IoT Hub
- h2 `g-5-5` "5.5 Implement a DevOps process for an Azure Cosmos DB solution" (sg-5-5)
  - `o-5-5-1` 5.5.1 Choose when to use declarative versus imperative operations
  - `o-5-5-2` 5.5.2 Provision and manage Azure Cosmos DB resources by using Azure Resource Manager templates
  - `o-5-5-3` 5.5.3 Migrate between standard and autoscale throughput by using PowerShell or Azure CLI
  - `o-5-5-4` 5.5.4 Initiate a regional failover by using PowerShell or Azure CLI
  - `o-5-5-5` 5.5.5 Maintain indexing policies in production by using Azure Resource Manager templates
