# DP-600 Domain 1 — Research Notes (Public Microsoft Learn Sources)

> **Purpose:** Raw research notes for the study-guide author. Every fact below was extracted from a public Microsoft Learn page (URLs listed under each objective). No instructor decks or proprietary materials were used.
>
> **Date gathered:** 2026-07-13

---

## o-1-1-1 · Workspace-Level Access Controls (Workspace Roles)

### Facts

- Four workspace roles exist in Microsoft Fabric: **Admin**, **Member**, **Contributor**, **Viewer** (in descending order of privilege).
- Roles are assigned to individuals, security groups, Microsoft 365 groups, or distribution lists.
- Microsoft Entra ID **service principals** (app registrations) can also be assigned to workspace roles, inheriting the same permissions as users for API-based operations (Items REST API, Job Scheduler API).
- If a user is in multiple groups, they receive the **highest** permission from any assigned role.
- **Admin** only:
  - Update or delete the workspace itself.
  - Add/remove admins.
  - Create workspace identity.
  - **Connect workspace to a Git repository** (only Admin can do this).
- **Admin + Member**:
  - Add Members (or roles with lower permissions).
  - Allow others to reshare items (Contributors/Viewers can reshare only if explicitly granted Reshare permission on an item).
- **Admin + Member + Contributor**:
  - Write/delete pipelines, notebooks, Spark job definitions, ML models, experiments, eventstreams.
  - Write/delete Eventhouses, KQL Querysets, Real-Time Dashboards, schemas/data of KQL Databases, Lakehouses, data warehouses, shortcuts.
  - Execute notebooks, Spark job definitions, ML models, experiments, pipelines.
  - Schedule data refreshes via on-premises gateway.
  - Modify gateway connection settings.
  - Read Lakehouse and Data Warehouse data through OneLake APIs and Spark (**ReadAll**).
  - Read Lakehouse data through Lakehouse explorer (ReadAll).
  - Subscribe to OneLake events.
  - Can edit OneLake security roles (Admin and Member only; Contributor cannot).
- **All four roles (including Viewer)**:
  - View and read content of pipelines, notebooks, Spark job definitions, ML models/experiments, eventstreams.
  - View and read content of KQL databases, KQL querysets, digital twin builder items, real-time dashboards.
  - Connect to SQL analytics endpoint of Lakehouse or Warehouse.
  - Read Lakehouse and Data Warehouse data via T-SQL through TDS endpoint (**ReadData** — all four roles).
  - View execution output of pipelines, notebooks, ML models/experiments.
- **Viewer** cannot: write data, create items, read via OneLake APIs/Spark (ReadAll requires Contributor+).
- Workspace roles do **not** span workspaces or capacities; they are scoped to a single workspace.
- OneLake security roles can **override** workspace defaults for fine-grained data access within a workspace.

### Key distinctions

| Capability | Admin | Member | Contributor | Viewer |
|---|:---:|:---:|:---:|:---:|
| Delete/update workspace | ✅ | ❌ | ❌ | ❌ |
| Add admins | ✅ | ❌ | ❌ | ❌ |
| Add members | ✅ | ✅ | ❌ | ❌ |
| Write data / create items | ✅ | ✅ | ✅ | ❌ |
| ReadAll (OneLake / Spark) | ✅ | ✅ | ✅ | ❌ |
| ReadData (T-SQL/TDS) | ✅ | ✅ | ✅ | ✅ |
| Connect workspace to Git | ✅ | ❌ | ❌ | ❌ |
| Edit OneLake security roles | ✅ | ✅ | ❌ | ❌ |

### Sources

1. <https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces>
2. <https://learn.microsoft.com/en-us/fabric/security/permission-model>

---

## o-1-1-2 · Item-Level Access Controls (Sharing Individual Items, Item Permissions)

### Facts

- **Item permissions** control access to individual Fabric items within a workspace; they are scoped to that single item only.
- You can grant item access to a user who has **no workspace role** — the user can access that specific item via a sharing link without seeing the workspace.
- Sharing an item grants **Read** permission by default.
  - Read = can see metadata and view associated reports, but **does NOT** allow access to underlying data in SQL or OneLake.
  - For DirectLake mode reports, the recipient must also have OneLake data permissions on the underlying Delta tables.
- Additional permissions that can be granted at share time (semantic model example):
  - **Allow recipients to modify this semantic model** (Write).
  - **Allow recipients to share this semantic model** (Reshare).
  - **Allow recipients to build content with the data** → grants **Build** permission, enabling creation of new reports/dashboards on top of the semantic model.
- Workspace role and item permission coexist; removing item permissions alone is not enough if the user has a workspace Viewer role (they can still see the item in the workspace). To fully block access, remove both.
- Different Fabric items expose different specific permissions. Key semantic model permissions: **Read**, **Build**, **Write**, **Reshare**.
- **Compute permissions** (SQL analytics endpoint, semantic model DAX security) provide a more granular layer on top of item permissions:
  - SQL analytics endpoint supports native SQL security (T-SQL GRANT/DENY).
  - Semantic model supports DAX-based security (RLS, OLS).
- Security evaluation order in Fabric:
  1. **Microsoft Entra authentication** (can the user authenticate to the tenant?)
  2. **Fabric access** (does the user have permission within Fabric/the workspace/item?)
  3. **Data security** (RLS, OLS, OneLake roles — can the user access the specific data?)

### Sources

1. <https://learn.microsoft.com/en-us/fabric/security/permission-model>
2. <https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-share>
3. <https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-permissions>  *(referenced in permission-model article)*

---

## o-1-1-3 · Row-Level Security (RLS), Column-Level Security (CLS), Object-Level Security (OLS), and OneLake Data Access Roles

### RLS — Row-Level Security

**Facts:**
- RLS restricts data at the **row** level using DAX filter expressions on table columns inside a **role** definition.
- Defined in **Power BI Desktop** → Modeling → **Manage Roles**; then published to the service.
- RLS only applies to users with workspace **Viewer** permissions. It does **not** apply to Admin, Member, or Contributor workspace roles (they see all data).
- RLS role members are managed in the Power BI service → semantic model → **Security** option.
- Two types of rules:
  - **Static RLS**: hard-coded value, e.g., `[Region] = "West"`.
  - **Dynamic RLS**: uses DAX functions `USERPRINCIPALNAME()` or `USERNAME()` so one role works for all users based on a mapping table; most common production approach.
- `CUSTOMDATA()` function used in embedded scenarios for app-passed identity string.
- **Bi-directional cross-filtering with RLS**: enabled per relationship (checkbox: *Apply security filter in both directions*). Can negatively impact query performance.
- For **Direct Lake** semantic models, RLS is supported; DAX query fallback to DirectQuery still respects RLS filters.
- For **Analysis Services live connections**, RLS is configured in the AS model, not in Power BI Desktop.
- Workflow: Define roles (Desktop) → Publish → Add members to roles (Service) → Validate with **Test as role** feature.

**Key TMDL/DAX snippet (static):**
```dax
[Region] = "West"
```
**Dynamic (UPN-based):**
```dax
[UserEmail] = USERPRINCIPALNAME()
```

### OLS — Object-Level Security (Table-Level + Column-Level)

**Facts:**
- OLS secures specific **tables** or **columns** from report viewers — hides both the data **and** the metadata (name).
- Applies to tabular models at **compatibility level 1400+** (Fabric/Power BI Premium, Azure AS, SSAS).
- Configured via:
  - **TMDL view** in Power BI Desktop (no external tools needed).
  - Open-source **Tabular Editor** (GUI-based).
  - **TMSL** (JSON scripting) or **TOM** (programmatic API).
- OLS is defined within model roles (same role object as RLS).
- `metadataPermission` property on `tablePermissions` or `columnPermissions` object:
  - `"none"` = table/column hidden and metadata concealed.
  - `"read"` = visible.
- Visualizations that reference an OLS-secured object display the same message as for a non-existing object.
- **Restrictions**:
  - Cannot secure a table that breaks a relationship chain (error at design time).
  - RLS and OLS from different roles cannot be combined on the same user (error at query time).
  - Dynamic calculations referencing secured objects are automatically restricted.
  - OLS models are **not** supported with: Q&A visuals, Quick insights, Smart narrative, Excel Data Types gallery.

**TMSL snippet (table-level, set to none):**
```json
"roles": [
  {
    "name": "Users",
    "modelPermission": "read",
    "tablePermissions": [
      { "name": "Product", "metadataPermission": "none" }
    ]
  }
]
```
**TMDL snippet (column-level):**
```
createOrReplace
  role CategoriesOLS
    modelPermission: read
    tablePermission Customers
      columnPermission Address
        metadataPermission: none
```

### CLS (Column-Level Security)

- In the OLS context, **column-level security** is implemented via `columnPermissions` in the role definition (same mechanism as OLS above).
- Set `metadataPermission: none` on a specific column to hide it and its name.
- In OneLake security context, **CLS** is enforced at the storage layer for engines that support it (Lakehouse, Spark notebooks, SQL Analytics Endpoint in user-identity mode, Direct Lake semantic models).

### OneLake Data Access Roles (File-Level/Folder-Level Security)

**Facts:**
- OneLake security uses **RBAC** (deny-by-default model); users start with **no access** unless explicitly granted by an OneLake role.
- Each role has: **Type** (GRANT only, no DENY type currently), **Permission** (Read or ReadWrite), **Scope** (tables, folders, or schemas), **Members** (Entra identities/groups).
- **Supported Fabric items**: Lakehouse, Azure Databricks Mirrored Catalog, Mirrored Databases.
- **Permissions**:
  - `Read` = read data + view table/column metadata (equivalent to VIEW_DEFINITION + SELECT in SQL).
  - `ReadWrite` = read + write data + view metadata.
- **Default roles** (auto-created with each item):
  - Lakehouse `DefaultReader`: Read on all folders under `Tables/` and `Files/` → assigned to all users with ReadAll permission.
  - Lakehouse `DefaultReadWriter`: Read on all folders → assigned to all users with Write permission.
  - To restrict access to specific users/folders: modify or remove the default role and create custom roles.
- **Workspace role interaction**:
  - Admin, Member, Contributor → automatically have Write permission to OneLake (overrides any OneLake security Read restriction).
  - Viewer → No access by default; OneLake security roles must explicitly grant access.
  - Admin and Member can edit OneLake security roles; Contributor and Viewer cannot.
- **Engine support for RLS/CLS in OneLake**:
  - Lakehouse (GA), Spark notebooks (GA), SQL Analytics Endpoint in user-identity access mode (GA), Direct Lake semantic models on OneLake mode (GA).
  - Eventhouse: RLS only (Public Preview).
- For non-authorized engine access (e.g., external tools not registered as authorized engines), if RLS/CLS is defined, the query is **blocked** entirely (rather than partially filtered) to prevent leakage.
- Custom OneLake roles are managed through the item's **OneLake security role management UX** (within the Lakehouse or Mirrored Database settings).

### Sources

1. <https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls>  *(RLS)*
2. <https://learn.microsoft.com/en-us/analysis-services/tabular-models/object-level-security>  *(OLS/CLS via TMSL)*
3. <https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-object-level-security>  *(OLS Power BI-focused page, referenced in permission-model)*
4. <https://learn.microsoft.com/en-us/fabric/onelake/security/data-access-control-model>  *(OneLake data access roles)*
5. <https://learn.microsoft.com/en-us/fabric/security/permission-model>  *(security layer overview)*

---

## o-1-1-4 · Sensitivity Labels (Microsoft Purview Information Protection)

### Facts

- Sensitivity labels in Fabric come from **Microsoft Purview Information Protection**; they must be created and published in the **Microsoft Purview compliance portal** before users can apply them.
- **Licensing required**:
  - Appropriate Microsoft Purview Information Protection license.
  - Power BI Pro or PPU license to apply labels to Power BI items.
  - Labels must also be published to the user via a label policy (being in the "allowed users" list alone is not sufficient).
- **Five label capabilities** and their Fabric support:

  | Capability | Description | Fabric Support |
  |---|---|---|
  | **Manual labeling** | User manually applies a label | All Fabric items |
  | **Default labeling** | Label applied automatically on item create/edit | All Fabric items (with limits for non-PBI items) |
  | **Mandatory labeling** | Users cannot save without a label | Fully supported for Power BI items only |
  | **Programmatic labeling** | Via Power BI admin REST APIs | All Fabric items |
  | **Downstream inheritance** | Label propagates to dependent (downstream) items | All Fabric items (with limits) |

- **Downstream inheritance** rules:
  - Power BI item → Power BI item: ✅
  - Fabric item → Fabric item: ✅
  - Fabric item → Power BI item: ✅
  - Power BI item → Fabric item: ❌ (not supported)
  - Downstream inheritance is **on by default**.
- **Inheritance upon creation** examples (a new item inherits the label of its parent at creation time):
  - Pipeline created from a Lakehouse → inherits Lakehouse label.
  - Notebook created from a Lakehouse → inherits Lakehouse label.
  - KQL Queryset created from KQL Database → inherits KQL Database label.
- **Inheritance from data sources**: currently supported for **Power BI semantic models only** (label from source data propagates to the semantic model, then downstream).
- **Supported export paths** where label travels with the exported file:
  - Export to Excel, PDF, PowerPoint.
  - Analyze in Excel (downloads an Excel file with live connection).
  - PivotTable in Excel with live connection (requires Microsoft 365 E3+).
  - Download to .pbix from Fabric.
  - (CSV, TXT, and cross-tenant exports are **not** supported for label persistence.)
- **Access control via labels**: Requires a Purview *protection policy* (for Fabric items in the same tenant) or a Purview *publishing policy* (for .pbix files and supported export paths). Cross-tenant access control via labels is not supported.
- **Power BI Desktop**: Sensitivity labels supported since December 2020 release. Sensitivity labels are **not** supported with Power BI Projects (.pbip) files.
- **Monitoring**: Governance experiences in OneLake catalog let admins identify labeled/unlabeled assets and monitor label coverage.

### Sources

1. <https://learn.microsoft.com/en-us/fabric/governance/information-protection>
2. <https://learn.microsoft.com/en-us/power-bi/enterprise/service-security-sensitivity-label-overview>  *(referenced in the main article for Power BI-specific details)*
3. <https://learn.microsoft.com/en-us/microsoft-365/compliance/create-sensitivity-labels>  *(creating labels in Purview compliance portal)*

---

## o-1-1-5 · Endorse Items (Promoted, Certified, Master Data)

### Facts

- Endorsement in Fabric and Power BI surfaces high-quality, trustworthy items to users. Three levels exist:

  | Badge | Who can apply | Meaning |
  |---|---|---|
  | **Promoted** | Any user with **Write** permissions on the item | Creator believes item is ready for sharing and reuse; encourages collaborative use. |
  | **Certified** | Only users **specified by the Fabric administrator** | Org-authorized reviewer confirms item meets quality standards, is authoritative, ready for org-wide use. Any user can **request** certification. |
  | **Master data** | Only users **specified by the Fabric administrator** | Data in the item is a core organizational data source (e.g., product codes, customer lists) — the single source of truth. Any user can **request** the designation. |

- **What can be endorsed**:
  - Promoted and Certified: all Fabric items and Power BI items **except Power BI dashboards**.
  - Master data: all Fabric and Power BI items that **contain data** (e.g., lakehouses, semantic models). Cannot be applied to reports/dashboards.
- **Admin enablement**:
  - Certification and master data endorsement must be **enabled by a Fabric administrator** (admin portal settings).
  - Certification enablement can be **delegated to domain administrators**, allowing different certifiers per domain.
- **Visibility**: Endorsed items display a badge in the UI and are listed first (given precedence) in certain lists.
- Endorsed items appear in lineage view with their badge (certified or promoted icons visible on semantic model cards).
- Endorsement is separate from sensitivity labels; both can be applied to the same item.

### Sources

1. <https://learn.microsoft.com/en-us/fabric/governance/endorsement-overview>
2. <https://learn.microsoft.com/en-us/fabric/fundamentals/endorsement-promote-certify>  *(step-by-step how-to, referenced in overview)*
3. <https://learn.microsoft.com/en-us/fabric/admin/endorsement-certification-enable>  *(admin enablement, referenced in overview)*

---

## o-1-2-1 · Configure Version Control for a Workspace (Git Integration)

### Facts

- Git integration in Microsoft Fabric is **workspace-level**: a workspace is connected to a single Git branch and folder.
- **Supported Git providers**: Azure DevOps (cloud-based only), GitHub (cloud-based only), GitHub Enterprise (cloud-based only). On-premises Azure DevOps Server is not supported.
- **Only a workspace Admin** can connect or disconnect a workspace from a Git repo. Contributors and Members can commit and update but cannot connect/disconnect.
  - Exception: an Admin can enable the workspace setting **"Allow users with at least Contributor role to change Git branch"**, which lets Contributors/Members also switch branches.
- **Prerequisites for the tenant**:
  - Fabric capacity is required.
  - Tenant switch: *Users can synchronize workspace items with their Git repositories* must be enabled.
  - For GitHub: additional tenant switch *Users can synchronize workspace items with GitHub repositories* required.
- **Connecting to Azure DevOps**: requires OAuth2 or Service Principal authentication; URL format: `https://dev.azure.com/{org}/{project}/_git/{repo}`.
- **Connecting to GitHub**: requires a Personal Access Token (fine-grained token with Contents read/write, or a classic token with repo scopes).
- **Connecting flow**: Workspace Settings → Git integration → Select provider → Provide org/project/repo/branch/folder → **Connect and sync**.
- **Initial sync logic**: if workspace is empty and Git branch has content → content copied to workspace; if Git has content and workspace has content → user chooses direction.
- **Workspace structure** (subfolders) is preserved in the Git repository.
- **Day-to-day operations**:
  - **Commit**: changes saved in workspace → user selects items → adds commit comment → **Commit**.
  - **Update from Git**: pull latest changes from branch → **Update all**.
  - **Undo**: revert workspace items to last synced state.
- **Supported items** for Git integration include: Lakehouses, Notebooks, Spark Job Definitions, Dataflow Gen2, Pipelines, Eventhouses, KQL databases, Warehouses (preview), Power BI Reports (preview), Semantic models (preview), SQL databases, and many more. Unsupported items are ignored (not synced, not deleted).
- **Source code format**: Semantic models use TMDL; Reports use PBIR (Power BI Enhanced Report format). These are stored as human-readable text files.
- Git integration is also the basis for **PBIP deployment to Fabric** (alongside Fabric APIs and the desktop Publish button).

### Sources

1. <https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration>
2. <https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-get-started>
3. <https://learn.microsoft.com/en-us/fabric/cicd/git-integration/source-code-format>  *(TMDL/PBIR format in source control, referenced in intro article)*

---

## o-1-2-2 · Power BI Desktop Project (.pbip) Format (TMDL, PBIR)

### Facts

- **.pbip** is the **Power BI Project** format: saves report and semantic model definitions as **individual plain-text files** in a folder structure, not as a single binary .pbix.
- Must be **enabled in Preview Features**: File → Options and settings → Options → Preview features → check **Power BI Project (.pbip) save option**.
- **Folder structure** created on save as PBIP:
  ```
  Project/
  ├── AdventureWorks.Report/         ← report definition folder
  ├── AdventureWorks.SemanticModel/ ← semantic model definition folder
  ├── .gitignore                    ← auto-created; excludes cache.abf and localSettings.json
  └── AdventureWorks.pbip           ← pointer file (optional shortcut to the report)
  ```
- The `.pbip` pointer file is **optional** — you can open by opening `definition.pbir` directly from the Report folder.
- Multiple reports can share one semantic model in the same folder (each report has its own `.pbir` file).
- **TMDL (Tabular Model Definition Language)**: YAML-like syntax used for semantic model definitions inside the `.SemanticModel/definition/` folder.
- **PBIR (Power BI Enhanced Report format)**: JSON-based format for report pages and visuals inside the `.Report/` folder.
- **Key benefits**:
  - Text-editor friendly (VS Code recommended — supports IntelliSense, validation, Git integration).
  - Git/source control ready — enables version history, team collaboration, CI/CD.
  - Programmatic generation/editing using TOM (Tabular Object Model) for semantic model metadata.
  - Supports batch operations (e.g., update all measures across tables).
- **External tool editing** supported but with caveats:
  - Changes outside Power BI Desktop require a **Desktop restart** to take effect.
  - Some files (report.json, mobileState.json, diagramLayout.json) have undocumented schemas — external edits not supported during preview.
  - Files must be **saved in UTF-8 without BOM** encoding.
- **Deploying PBIP to Fabric**:
  - Via Fabric Git Integration (recommended for team workflows).
  - Via Fabric REST APIs.
  - Via Power BI Desktop **Publish** (uses a temp .pbix internally, deploys both metadata and data cache).
- **Converting**: PBIX ↔ PBIP conversion only via Power BI Desktop File → Save As. No programmatic conversion.
- **Sensitivity labels** are **not** supported with PBIP files.
- **Considerations**: Maximum path length 260 characters on Windows (long table/object names can exceed this). Cannot save directly to OneDrive/SharePoint; use locally synced OneDrive folder (with risk of sync conflicts).
- Git configured with `autocrlf` recommended to avoid CRLF line-ending diffs.

### Sources

1. <https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview>
2. <https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset>  *(semantic model folder details, referenced in overview)*
3. <https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report>  *(report folder details, referenced in overview)*

---

## o-1-2-3 · Deployment Pipelines (Dev/Test/Prod Stages, Deployment Rules)

### Facts

**Pipeline structure:**
- A deployment pipeline can have **2 to 10 stages** (default: 3 — Development, Test, Production).
- Stages can be added, deleted, or renamed.
- **Development** → **Test** → **Production** is the canonical flow; content is cloned from source to target stage.
- Each stage maps to a Fabric workspace.
- A Fabric capacity is required.

**Deployment process:**
- Content is **copied** (not moved) from source to target stage; paired items in the target are **overwritten**.
- **Item pairing**: an item in one stage is paired with the same item in an adjacent stage. Pairing happens on initial assignment or on first deploy. Items with the same name but not explicitly paired will create **duplicates** (not overwrite).
  - Paired items remain paired even if renamed — name differences between stages are allowed.
  - Items added after workspace assignment are **not** automatically paired.
- Folders hierarchy is preserved; flat list view allows cross-folder selection.
- Deployment can be triggered manually or via **Deployment pipelines REST APIs** (automation).

**Deployment Rules:**
- Rules are configured on the **target stage** (e.g., Production) so that when content arrives from the source stage it uses the target's configuration.
- **Types of rules**:
  - **Data source rules**: change connection strings between stages (same source type required, e.g., SQL Server → different SQL Server).
  - **Parameter rules**: override Power Query parameter values.
  - **Default lakehouse rules**: specify default lakehouse for notebooks in the target stage.
- **Which items support which rules**:
  - Dataflow Gen1: data source rules + parameter rules.
  - Semantic model: data source rules + parameter rules.
  - Paginated report: data source rules only.
  - Notebook: default lakehouse rule only.
  - Mirrored database: data source rules only.
- **Supported data sources for data source rules**: Azure AS, Azure Synapse, SSAS, Azure SQL, SQL Server, OData, Oracle, SapHana (import only), SharePoint, Teradata. For others → use parameters instead.
- **Key limitations for deployment rules**:
  - Must be item **owner** to create a rule.
  - Cannot create rules in the **Development** stage.
  - Rules are deleted when the item is removed.
  - If the data source/parameter referenced in a rule is changed or removed in the source stage, the rule becomes invalid and deployment fails.
  - Rules do not take effect until the next deployment (though comparison shows them).

**Retirement notice:** Beginning February 12, 2026, deployment pipelines will retire support for semantic models that have not been upgraded to Enhanced Metadata.

### Sources

1. <https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines>
2. <https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/create-rules>
3. <https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/get-started-with-deployment-pipelines>  *(referenced in intro article)*

---

## o-1-2-4 · Impact Analysis of Downstream Dependencies + Lineage View

### Facts

**Data Lineage View:**
- Lineage view shows the flow of data from data sources → dataflows → semantic models → reports → dashboards for all artifacts in a workspace, including external dependencies (data sources and semantic models in other workspaces).
- **Access**: workspace list view → View → **Lineage**.
- **Permission required**: at least **Contributor** role to access lineage view. Viewers cannot access it. Also requires a **Power BI Pro** license.
- Information shown on cards: last refresh time, endorsement badges (certified/promoted), data source type, gateway info.
- Selecting the double arrows under an artifact highlights all artifacts related to it (upstream and downstream) and dims the rest.
- Clicking an artifact card opens a **side pane** with detailed metadata.

**Semantic Model Impact Analysis:**
- Accessed from within lineage view via the **impact analysis button** on a semantic model's card.
- **Impact summary**: shows count of potentially impacted workspaces, reports, dashboards + total views for downstream items.
- **Usage metrics** (last 30 days, excluding current day): number of unique Viewers (distinct users) and Views (view count) per downstream report/dashboard.
- Helps prioritize which downstream items need investigation (e.g., a report with 20,000 viewers is more critical than one with 3 viewers).
- **Notify contacts**: sends an email to the contact lists of all affected workspaces; appears with the sender's name for follow-up.
- Impact analysis can only be performed on semantic models **in your own workspace** (not on external semantic models displayed in lineage view — navigate to their source workspace).
- Items you don't have access to are listed as **"Limited access"** in the panel (privacy protection).
- **From Power BI Desktop**: when republishing a changed semantic model, a warning message shows the count of potentially impacted workspaces/reports/dashboards and links to the full impact analysis in the service.
- Usage metrics are **not** supported for personal workspaces (My Workspace).

### Sources

1. <https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-data-lineage>
2. <https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-dataset-impact-analysis>

---

## o-1-2-5 · Deploy/Manage Semantic Models via the XMLA Endpoint

### Facts

**What the XMLA endpoint is:**
- The XMLA endpoint exposes the **XML for Analysis (XMLA)** protocol for open-platform connectivity to Power BI semantic models in Premium, PPU, or Power BI Embedded workspaces.
- Data over the XMLA protocol is **fully encrypted**.
- **Connection string URL format**: `powerbi://api.powerbi.com/v1.0/[tenant name]/[workspace name]` — used like an Analysis Services server name in client tools.
- Workspace names in the connection string must be **URI-encoded** (e.g., `Sales%20Workspace`).

**Read-only vs. Read-write:**
- **Read-only** is enabled **by default** for all Premium/PPU capacity semantic model workloads.
  - Allows: querying model data, metadata, events, schema.
- **Read-write** must be explicitly enabled by an admin.
  - Enables: semantic model management, metadata scripting (TMSL), processing/refresh operations, advanced modeling, debugging.
- **To enable read-write (Premium capacity)**: Admin portal → Capacity settings → Power BI Premium → [capacity] → Workloads → **XMLA Endpoint** → select **Read Write**. (Applies to all workspaces and models on that capacity.)
- **To enable read-write (PPU)**: Admin portal → Premium Per User → Semantic model workload settings → **XMLA Endpoint** → **Read Write**.

**Client tools that use the XMLA endpoint:**
| Tool | Requires |
|---|---|
| Excel PivotTables | Read-only |
| SQL Server Management Studio (SSMS ≥ 18.9) | Read-only for queries; Read-write for scripting |
| SQL Server Profiler (with SSMS ≥ 18.9) | Read-only |
| Visual Studio with Analysis Services Projects (SSDT) | Read-write (model compatibility level ≥ 1500) |
| Analysis Services Deployment Wizard | Read-write |
| PowerShell (SqlServer module ≥ 21.1.18256) | Read-write |
| Power BI Report Builder | Read-only |
| Tabular Editor 2.x | Read-only for queries; Read-write for metadata |
| DAX Studio | Read-only |
| ALM Toolkit | Read-only for queries; Read-write for metadata |

- **Client libraries**: tools use MSOLAP, ADOMD, and AMO client library abstractions (same libraries as Azure AS / SSAS).
- **Large models optimization**: for write operations, enabling the **large models** feature on the semantic model is recommended, especially for models > 1 GB (significantly reduces write overhead).
- **Single-user application** (developer tools, admin scripts): uses one user account or app identity; needs valid PPU license unless on Premium capacity.
- **Multi-user application**: for PPU workspaces, each user must sign in individually; for Premium workspaces, a service account can act on behalf of users.
- **Azure Analysis Services cmdlets (Az.AnalysisServices)** are **not** supported for Power BI semantic models — use the SqlServer module instead.
- **TMSL** (Tabular Model Scripting Language) is the JSON-based scripting language used via SSMS or the XMLA endpoint to manage model metadata (refresh, alter model structure, etc.).

### Sources

1. <https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools>
2. <https://learn.microsoft.com/en-us/analysis-services/tmsl/tabular-model-scripting-language-tmsl-reference>  *(TMSL reference, linked from XMLA endpoint article)*

---

## o-1-2-6 · Reusable Assets: .pbit Templates, .pbids Data Source Files, Shared Semantic Models

### Facts

**.pbit — Power BI Template Files:**
- Extension: `.pbit`; created via File → Export → **Power BI template** in Power BI Desktop.
- A `.pbit` file contains: report pages + visuals, data model definition (schema, relationships, measures), all query definitions.
- `.pbit` does **NOT** contain data (unlike `.pbix`).
- When opened, Power BI Desktop prompts for: parameter values (if defined), then credentials + data source location.
- After providing credentials and data source, the template creates a full report identical to the source.
- Useful for standardizing report layouts and data models; acts as a starting point for new report authors.
- `.pbit` files are smaller than `.pbix` because they contain no data cache. Metadata (e.g., filter values, slicer selections) is preserved in the template.
- To use: double-click the `.pbit` file, or File → Import → **Power BI template** in Power BI Desktop.

**.pbids — Power BI Data Source Files:**
- Extension: `.pbids`; identifies a connection specification for Power BI Desktop to use when loading data.
- Contains connection information (protocol, server, database address) but **NOT** authentication credentials or table/schema definitions.
- When opened, Power BI Desktop prompts for credentials, then shows the Navigator to select tables.
- Supports specifying `mode` as `DirectQuery` or `Import`; if mode is absent or null, the user is prompted.
- Currently supports a **single data source** per file (multiple sources → error).
- **Creating a `.pbids` file**:
  - Recommended: export from existing `.pbix` via File → Options and settings → **Data source settings** → select source → export as PBIDS.
  - Or: manually author JSON with `.pbids` extension using the Data Source Reference (DSR) format.
- **Example (Azure SQL):**
  ```json
  {
    "version": "0.1",
    "connections": [
      {
        "details": {
          "protocol": "tds",
          "address": {
            "server": "myserver.database.windows.net",
            "database": "mydatabase"
          }
        },
        "mode": "DirectQuery"
      }
    ]
  }
  ```
- Useful for distributing standardized data connection specs to report developers without sharing credentials.

**Shared Semantic Models (Live Connection):**
- A semantic model published to the Power BI service can be shared across workspaces for multiple report authors to build reports on top of it (this is the "managed self-service BI" pattern).
- **Sharing a semantic model**: from the semantic model's options menu (OneLake catalog or data details page) → **Share** → configure access type:
  - **Read** (default): can view metadata and reports built on it; cannot query underlying data via SQL/OneLake.
  - **Build**: can create new reports and dashboards on top of the semantic model (also called "build permission").
  - **Write**: can modify the semantic model.
  - **Reshare**: can grant access to others.
- **Build permission** is the key permission for self-service report creation on a shared semantic model.
- Downstream reports built on shared semantic models appear in **lineage view** with the source workspace name on the semantic model card.
- **Impact analysis** is particularly valuable for shared semantic models (changes can affect reports across many workspaces).
- Semantic model access is also managed via **Manage permissions** on the semantic model (not just the Share dialog).

### Sources

1. <https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-templates>  *(pbit templates)*
2. <https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-sources#use-pbids-files-to-get-data>  *(pbids files)*
3. <https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-share>  *(sharing shared semantic models)*
4. <https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-build-permissions>  *(Build permission, referenced in share article)*

---

## Summary — Unique URLs Captured

| # | URL |
|---|---|
| 1 | https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces |
| 2 | https://learn.microsoft.com/en-us/fabric/security/permission-model |
| 3 | https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls |
| 4 | https://learn.microsoft.com/en-us/analysis-services/tabular-models/object-level-security |
| 5 | https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-object-level-security |
| 6 | https://learn.microsoft.com/en-us/fabric/onelake/security/data-access-control-model |
| 7 | https://learn.microsoft.com/en-us/fabric/governance/information-protection |
| 8 | https://learn.microsoft.com/en-us/power-bi/enterprise/service-security-sensitivity-label-overview |
| 9 | https://learn.microsoft.com/en-us/microsoft-365/compliance/create-sensitivity-labels |
| 10 | https://learn.microsoft.com/en-us/fabric/governance/endorsement-overview |
| 11 | https://learn.microsoft.com/en-us/fabric/fundamentals/endorsement-promote-certify |
| 12 | https://learn.microsoft.com/en-us/fabric/admin/endorsement-certification-enable |
| 13 | https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration |
| 14 | https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-get-started |
| 15 | https://learn.microsoft.com/en-us/fabric/cicd/git-integration/source-code-format |
| 16 | https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview |
| 17 | https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset |
| 18 | https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report |
| 19 | https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines |
| 20 | https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/create-rules |
| 21 | https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/get-started-with-deployment-pipelines |
| 22 | https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-data-lineage |
| 23 | https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-dataset-impact-analysis |
| 24 | https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools |
| 25 | https://learn.microsoft.com/en-us/analysis-services/tmsl/tabular-model-scripting-language-tmsl-reference |
| 26 | https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-templates |
| 27 | https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-sources |
| 28 | https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-share |
| 29 | https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-build-permissions |
| 30 | https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-permissions |
