# DP-420 Domain 5 — Research Pack (Maintain an Azure Cosmos DB solution, 25–30%)

Grounded from Microsoft Learn (fetched April/May 2026 revisions). Each objective lists key facts + Sources.

## 5.1 Monitor and troubleshoot

### 5.1.1 Evaluate response status code and failure metrics
- Azure Monitor collects Cosmos DB metrics automatically (no config), 1-minute granularity, ~7-day retention by default.
- **Total Requests** metric can be split by **StatusCode** dimension. Key codes: 429 (rate limited / RU exceeded), 401/403 (auth), 404 (not found), 449 (retriable transient write conflict), 410 (partition split), 503 (service unavailable), 5xx.
- Server-side metrics: throughput, storage, availability, latency, consistency. Client-side: request charge, activity ID, exception/stack, HTTP status/substatus, diagnostic string.
- Dimension values (e.g., container name) are case-insensitive.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/monitor ; https://learn.microsoft.com/en-us/azure/cosmos-db/monitor-reference

### 5.1.2 Monitor Normalized RU Consumption
- **Normalized RU Consumption** = 0–100% metric; measures utilization of provisioned throughput across partition key ranges/regions. It is the MAX utilization across all partitions.
- Reaching 100% means at least one physical partition's RU budget for that second is fully used → subsequent requests in that partition throttled with 429.
- A single hot partition can pin normalized RU to 100% even while total account RU is low → indicates a hot partition / skew.
- Split by PhysicalPartitionId / Region to find the hot partition.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/monitor-normalized-request-units

### 5.1.3 Monitor server-side latency
- Metric measures latency inside the Cosmos DB service (excludes network). Split by operation type, region, connection mode.
- High server-side latency often points to cross-partition/fan-out queries, unindexed queries, or large response sizes; high client latency with low server latency points to network/SDK.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/monitor-server-side-latency

### 5.1.4 Monitor replication (P2P latency & availability)
- Multi-region: monitor availability metric and replication latency between write and read regions.
- Bounded Staleness exposes P2P replication latency guarantees; monitor to confirm SLA.
- "Region failed over" activity metric fires when a region fails over.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/monitor-reference

### 5.1.5 Configure Azure Monitor alerts
- Recommended alert rules: **Rate limiting on RU** (metric alert, StatusCode = 429), **Region failed over** (Count > 1), **Rotate keys** (activity log alert, account keys rotated).
- Metric alerts (thresholds/dynamic), Log (KQL) alerts, Activity log alerts.
- Alert on logical partition key storage approaching 20 GB with a dedicated how-to.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/create-alerts ; https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-alert-on-logical-partition-key-storage-size

### 5.1.6 Resource logs (diagnostic settings) & KQL
- Resource (data plane) logs are NOT collected until you create a **diagnostic setting** routing them to Log Analytics / Storage / Event Hubs.
- Categories: DataPlaneRequests, QueryRuntimeStatistics, PartitionKeyStatistics, PartitionKeyRUConsumption, ControlPlaneRequests, MongoRequests, etc.
- **Resource-specific mode** (recommended) → tables like CDBDataPlaneRequests, CDBPartitionKeyStatistics, CDBPartitionKeyRUConsumption, CDBControlPlaneRequests. Legacy AzureDiagnostics table is the alternative.
- Full-text query feature deobfuscates the query text in logs (extra cost; disable after troubleshooting).
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/monitor-resource-logs ; https://learn.microsoft.com/en-us/azure/cosmos-db/diagnostic-queries ; https://learn.microsoft.com/en-us/azure/cosmos-db/monitor-logs-basic-queries

### 5.1.7 Monitor throughput across partitions
- **PartitionKeyRUConsumption** log shows RU consumed per logical partition key → find hot logical partitions.
- Normalized RU by PhysicalPartitionId shows physical-partition utilization.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/monitor-resource-logs

### 5.1.8 Monitor data distribution across partitions
- **PartitionKeyStatistics** log reports storage size per top logical partition key → detect skew / a partition approaching 20 GB.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/monitor-resource-logs

### 5.1.9 Security monitoring — logging & auditing
- **ControlPlaneRequests** log audits control-plane operations (throughput changes, firewall/network changes, key operations). Enable via audit-control-plane-logs.
- disableKeyBasedMetadataWriteAccess prevents changing metadata via account keys (forces ARM/RBAC).
- Activity log audits point-in-time restore actions and key rotation.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/audit-control-plane-logs

## 5.2 Backup and restore

### 5.2.1 Choose periodic vs continuous
- **Periodic** (default): full backup every 4 hours; last 2 retained by default (configurable interval + retention); stored in Azure Blob, GRS-replicated; restore ONLY via Microsoft support ticket; deleted container/db snapshots kept 30 days.
- **Continuous**: point-in-time restore (PITR) self-service to any second; two tiers — **7-day (free)** and **30-day (paid storage)**; you trigger restore via portal/CLI/PS/ARM. Restore always goes to a NEW account in same region(s).
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/periodic-backup-restore-introduction ; https://learn.microsoft.com/en-us/azure/cosmos-db/continuous-backup-restore-introduction

### 5.2.2 Configure periodic backup
- Set backup interval + retention (portal/CLI/PS/ARM). Two backups free; extra copies charged. Backups don't consume RUs.
- Backup storage redundancy: Geo (default), Zone, or Local.
- What ISN'T restored: account keys (new keys generated), firewall/VNet/private endpoint, RBAC assignments, stored procs/triggers/UDFs, TTL-expired docs, analytical store, materialized views; restored account is single-region (write region).
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/periodic-backup-restore-introduction ; https://learn.microsoft.com/en-us/azure/cosmos-db/periodic-backup-storage-redundancy

### 5.2.3 Configure continuous backup & PITR
- Enable at account creation or migrate periodic→continuous (one-way). Choose 7-day (free) or 30-day tier; can switch tiers but not the retention numbers.
- Mutations backed up asynchronously within ~100 seconds.
- Supported: NoSQL, MongoDB, Gremlin, Table (NOT Cassandra). Not restored: firewall/VNet/private endpoint, data-plane RBAC, stored procs/triggers/UDFs, all source regions.
- CMK + continuous requires user- or system-assigned managed identity (not first-party identity).
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/provision-account-continuous-backup ; https://learn.microsoft.com/en-us/azure/cosmos-db/continuous-backup-restore-introduction ; https://learn.microsoft.com/en-us/azure/cosmos-db/migrate-continuous-backup

### 5.2.4 Locate a restore point
- Best practice: get the **latest restorable timestamp** for the container before restoring.
- Use the **event feed** (portal "Click here" link) or enumerate restorable resources via CLI/PS to find create/replace/delete events on databases/containers.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/get-latest-restore-timestamp ; https://learn.microsoft.com/en-us/azure/cosmos-db/restore-account-continuous-backup

### 5.2.5 Restore from a restore point
- Restore live or deleted account; entire account or selected databases/containers into a NEW account in the same region.
- `az cosmosdb restore --target-database-account-name --account-name --restore-timestamp --resource-group --location [--databases-to-restore] [--disable-ttl True] [--public-network-access Disabled]`. TTL is restored by default → pass --disable-ttl True to avoid immediate expiry.
- A subset of containers under a shared-throughput database can't be restored alone (whole db only).
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/restore-account-continuous-backup

## 5.3 Security

### 5.3.1 Service-managed vs customer-managed keys
- Encryption at rest is always ON (AES-256), no toggle, no extra cost. Default = **service-managed keys** (Microsoft).
- Optional **customer-managed keys (CMK)** add a 2nd layer (double encryption) using keys in Azure Key Vault; must be enabled at account creation (or via existing-accounts flow); account-level granularity.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/database-encryption-at-rest ; https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-setup-customer-managed-keys

### 5.3.2 Network-level access control
- **IP firewall** (ipRules/ipRangeFilter, CIDR) → non-listed IPs get 403. "Accept connections from within Azure datacenters" adds 0.0.0.0.
- **VNet service endpoints** allow specific subnets.
- **Private endpoints (Private Link)** = private IPs in your subnet; combine with `publicNetworkAccess=Disabled` (takes precedence over all firewall rules).
- Auth token still ALWAYS required regardless of network rules.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-configure-firewall ; https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-configure-vnet-service-endpoint ; https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-configure-private-endpoints

### 5.3.3 Configure data encryption
- Encryption in transit (TLS/HTTPS) + at rest (AES-256) automatic. Double encryption via CMK only covers main transactional store — Synapse Link analytical store and continuous backups aren't double-encrypted.
- CMK metadata NOT encrypted with CMK: account/db/container names, stored-proc names, index property paths, partition key values.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/database-encryption-at-rest

### 5.3.4 Control plane access via Azure RBAC
- Control plane = manage resources (metadata), NOT data. Built-in **Cosmos DB Operator** manages accounts but blocks keys/connection strings/data.
- Custom control-plane role: Actions `Microsoft.DocumentDB/*`. Assigned with `az role assignment create`.
- Native data-plane RBAC definitions/assignments are stored inside the account → require control-plane permissions to create.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/security/how-to-grant-control-plane-role-based-access

### 5.3.5 Control plane access to Data Explorer via Azure RBAC
- Data Explorer honors control-plane Azure RBAC. Reader can view; to read/write DATA in Data Explorer without keys you also need data-plane RBAC (or key access).
- `disableKeyBasedMetadataWriteAccess` forces metadata changes via ARM/RBAC only.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/security/how-to-grant-control-plane-role-based-access

### 5.3.6 Data plane access via Microsoft Entra ID
- Native data-plane RBAC with Entra ID; built-in **Cosmos DB Built-in Data Reader** and **Cosmos DB Built-in Data Contributor**.
- Custom role dataActions e.g. `.../readMetadata`, `.../sqlDatabases/containers/*`, `.../items/*`. No `notDataActions` support.
- `az cosmosdb sql role definition create/list` + `az cosmosdb sql role assignment create --scope /` (scope = account, db, or container).
- Disable keys: `properties.disableLocalAuth=true` forces Entra ID.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/security/how-to-grant-data-plane-role-based-access ; https://learn.microsoft.com/en-us/azure/cosmos-db/reference-data-plane-security

### 5.3.7 Configure CORS
- CORS supported for **API for NoSQL only** (uses HTTP). Set `cors.allowedOrigins` (comma-separated) via portal or ARM. Wildcard `*` allowed but no sub-domain wildcards (`https://*.x.com` unsupported). Only authenticated requests evaluated.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-configure-cross-origin-resource-sharing

### 5.3.8 Manage account keys with Azure Key Vault
- Store account keys / connection strings as **secrets** in Key Vault instead of app config; retrieve at runtime using **managed identity** (no secrets in code).
- Prefer disabling keys entirely (disableLocalAuth) + Entra ID where possible; Key Vault is the mitigation when keys are still required.
- Sources: https://learn.microsoft.com/en-us/azure/key-vault/general/overview ; https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-setup-managed-identity

### 5.3.9 Implement customer-managed keys for encryption
- Store CMK in Azure Key Vault (RSA ≥3072). Key Vault needs Soft Delete + Purge Protection. Grant Cosmos DB principal Get/WrapKey/UnwrapKey (access policy) or Key Vault Crypto Service Encryption User (RBAC).
- Set Key URI at account creation. Revoke by disabling the key → only account deletion possible after revoke. Rotate via new key version or new Key URI.
- CMK adds RU overhead (~+5% point read, +6% write, +15% queries/change feed).
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-setup-customer-managed-keys

### 5.3.10 Implement Always Encrypted
- Client-side encryption of sensitive properties; service never sees plaintext or keys. Uses **DEK** (data encryption key, database-level, stored in Cosmos DB) wrapped by a **CMK** (column master key) in Key Vault.
- Container-level **encryption policy** (immutable, set at creation) maps each property to a DEK + type.
- **Deterministic** = same ciphertext for same plaintext → equality filters allowed (weaker). **Randomized** = stronger but no querying.
- .NET (Microsoft.Azure.Cosmos.Encryption) / Java packages; uses KeyResolver + managed identity.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-always-encrypted

## 5.4 Data movement

### 5.4.1 Choose a data movement strategy
- SDK Bulk (code, high-throughput one-off migrations), ADF/Synapse pipelines (no-code scheduled ETL), Kafka connector (streaming pipelines), Stream Analytics (streaming output sink), Spark connector (data engineering), IoT Hub custom endpoint (device routing). Match tool to source, streaming vs batch, code vs no-code.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/tutorial-dotnet-bulk-import ; https://learn.microsoft.com/en-us/azure/data-factory/connector-azure-cosmos-db

### 5.4.2 SDK bulk operations
- `new CosmosClient(..., new CosmosClientOptions { AllowBulkExecution = true })`. Immutable once set. SDK groups concurrent point operations into batched service calls per partition. Use `Task.WhenAll`. Exclude indexes + high RU for fastest import.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/tutorial-dotnet-bulk-import

### 5.4.3 ADF & Synapse pipelines
- Cosmos DB connector supports copy in/out (source & sink), no-code, scheduled; also a manual periodic-backup mechanism (export to storage).
- Sources: https://learn.microsoft.com/en-us/azure/data-factory/connector-azure-cosmos-db

### 5.4.4 Kafka connector
- Kafka Connect: **Sink** (Kafka→Cosmos, exactly-once) and **Source** (Cosmos change feed→Kafka, at-least-once, exactly-once for single task). Formats: JSON, JSON+schema, AVRO. Config: connection.endpoint, master.key, databasename, containers.topicmap (topic#container).
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/kafka-connector ; https://learn.microsoft.com/en-us/azure/cosmos-db/kafka-connector-sink ; https://learn.microsoft.com/en-us/azure/cosmos-db/kafka-connector-source

### 5.4.5 Azure Stream Analytics
- Cosmos DB (NoSQL) as an ASA **output** sink for streaming results; upsert on document id.
- ASA has no fixed IP → allow via "Accept connections from within Azure datacenters" firewall option.
- Sources: https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-documentdb-output

### 5.4.6 Spark connector
- `cosmos.oltp` format reads/writes transactional store (consumes RUs); `cosmos.olap` reads analytical store (RU-free, read-only, via Synapse Link). Only Spark can write back.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/quickstart-spark

### 5.4.7 Cosmos DB as IoT Hub custom endpoint
- IoT Hub can route device messages directly to Cosmos DB (custom endpoint). JSON if contentType=application/json & contentEncoding=UTF-8, else base64.
- Supports **synthetic partition keys** (partition key template, e.g., deviceId+month) to stay under 20 GB logical partition limit.
- System-assigned MI auth requires assigning **Cosmos DB Built-in Data Contributor** via CLI/PS (not portal).
- Sources: https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-endpoints

## 5.5 DevOps

### 5.5.1 Declarative vs imperative
- Declarative (ARM/Bicep/Terraform) = desired-state, idempotent, repeatable, source-controlled → best for CI/CD & environment parity. Imperative (CLI/PowerShell/SDK) = step-by-step commands → best for one-off ops, scripting, ad-hoc automation.
- Control plane API isn't for high-volume calls.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/manage-with-templates ; https://learn.microsoft.com/en-us/azure/cosmos-db/manage-with-cli

### 5.5.2 Provision/manage via ARM templates
- ARM/Bicep manage account, databases, containers, throughput, indexing policy, RBAC, firewall (ipRules), CORS, backup policy. `az deployment group create --template-file`. Samples repo available.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/manage-with-templates ; https://learn.microsoft.com/en-us/azure/cosmos-db/samples-resource-manager-templates ; https://learn.microsoft.com/en-us/azure/cosmos-db/manage-with-bicep

### 5.5.3 Migrate between standard & autoscale throughput
- Migration is supported ONLY via portal, **CLI**, or **PowerShell** (NOT SDK, NOT ARM).
- CLI: `az cosmosdb sql database|container throughput migrate --throughput-type 'autoscale'|'manual'`. On enabling autoscale, system picks starting max RU/s from current manual + storage.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-provision-autoscale-throughput ; https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-choose-offer

### 5.5.4 Initiate regional failover via PS/CLI
- `az cosmosdb failover-priority-change --failover-policies <region>=<priority>` reorders failover priorities / triggers manual failover of the write region (single-write accounts). Service-managed failover is automatic.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-database-account ; https://learn.microsoft.com/en-us/azure/cosmos-db/manage-with-cli

### 5.5.5 Maintain indexing policies via ARM
- Store the container's indexingPolicy in the ARM/Bicep template; deploy changes through CI/CD. Index transformation runs online (query IndexTransformationProgress). Keeps prod indexing consistent & source-controlled.
- Sources: https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-indexing-policy ; https://learn.microsoft.com/en-us/azure/cosmos-db/index-policy
