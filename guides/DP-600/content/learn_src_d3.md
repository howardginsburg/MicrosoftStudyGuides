# DP-600 Domain 3 — Implement and Manage Semantic Models
## Public Microsoft Learn Research Notes

> **Critical sourcing note**: Every fact below is grounded in publicly accessible Microsoft Learn
> documentation. Short code snippets are illustrative; the exam guide author must write final originals.

---

## o-3-1-1 — Choose a Storage Mode

### Facts

- **Import** — data ingested into the VertiPaq in-memory columnar store. Typical 10× source
  compression (e.g. 10 GB source → ~1 GB model). Supports all DAX functions, calculated tables,
  calculated columns, Q&A, Quick Insights. Requires scheduled or on-demand refresh.
  Max upload from Power BI Desktop: **10 GB**. Can grow beyond 10 GB in the service after the
  first refresh when **Large semantic model storage format** is enabled.

- **DirectQuery** — no data cached; only metadata loaded. Each visual interaction sends native
  SQL/KQL to the source. No calculated tables. DAX limited to translatable functions.
  Refresh limits: 8×/day shared, 48×/day Premium. Dashboard tile auto-refresh: every 15 min.

- **Direct Lake** — Fabric-only. VertiPaq engine processes queries (comparable Import speed)
  but reads columns directly from Delta/Parquet files in OneLake on demand (*transcoding*).
  Refresh = *framing* (metadata-only, takes seconds). Two variants: **Direct Lake on OneLake**
  and **Direct Lake on SQL analytics endpoint** — see o-3-2-4 for key differences.
  Requires a Fabric capacity licence.

- **Dual** — table is simultaneously Import and DirectQuery. Power BI picks the most efficient
  mode per query. Primary use: dimension tables in composite models paired with DirectQuery
  fact tables, enabling efficient native SQL joins.

- **Composite** — semantic model with tables in mixed storage modes (or DirectQuery from
  multiple sources). Strive to deliver best of Import performance with real-time DirectQuery data.

**Tradeoff summary**

| Mode | Query speed | Data freshness | Fabric licence req. | Size limit |
|------|-------------|---------------|---------------------|-----------|
| Import | Fastest (VertiPaq) | Refresh schedule | No | 10 GB upload; grows in service with large model setting |
| DirectQuery | Slower (source query) | Real-time | No | None |
| Direct Lake | Import-comparable | Seconds (framing) | Yes | SKU guardrails |
| Dual | Import or DQ per query | Import partitions + source | No | Same as Import/DQ |
| Composite | Mixed | Mixed | No (DL requires Fabric) | Mixed |

### Sources
- https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand
- https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview
- https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models

---

## o-3-1-2 — Implement a Star Schema for a Semantic Model

### Facts

- **Dimension tables** — describe business entities (products, customers, dates, locations).
  Always contain a unique identifier column (surrogate key) and descriptive attributes.
  Act as the "one" side of one-to-many relationships. Optimized for **filtering and grouping**.

- **Fact tables** — store observations/events (sales, transactions, telemetry).
  Contain foreign key columns (referencing dimensions) + numeric measure columns.
  Act as the "many" side of relationships. Optimized for **summarization**.

- **Surrogate keys** — numeric identifiers added to dimension tables for uniqueness.
  In Power Query: use *Add Index Column*. Merge index back to fact table.

- **Measures in semantic models** — two types:
  - *Explicit measures*: DAX-defined; shown with calculator icon; recommended.
  - *Implicit measures*: auto-aggregation by visuals; shown with ∑ icon; avoid in complex models.

- **Design patterns worth knowing for exam**:
  - *Snowflake dimensions*: normalised sub-tables (e.g., Product → Subcategory → Category).
    Generally avoid in Power BI — merge into a single denormalised dimension table for performance.
  - *Role-playing dimensions*: same date table referenced multiple times via inactive relationships
    (e.g., OrderDate, ShipDate, DueDate). Use `USERELATIONSHIP()` in measures to activate.
  - *Factless fact tables*: bridge tables containing only key columns (no measures).
    Used to resolve many-to-many relationships between two dimension tables.
  - *Degenerate dimensions*: key attributes stored in the fact table without a separate dimension
    (e.g., invoice number).

- Don't mix dimension and fact purpose in the same table.
- Fact tables should always load at a **consistent grain** (granularity).
- Power BI relationships are based on a **single unique column** on the "one" side.

### Sources
- https://learn.microsoft.com/en-us/power-bi/guidance/star-schema
- https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand
- https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many

---

## o-3-1-3 — Relationships

### Facts

**Cardinality types and cross-filter options**

| Cardinality | Cross filter options |
|-------------|---------------------|
| One-to-many (Many-to-one) | Single or Both |
| One-to-one | Both only |
| Many-to-many | Single (either direction) or Both |

- Filters always propagate from the "one" side automatically.
- **Bi-directional** (Both) = filters flow in both directions. Use with caution; can cause
  performance degradation and ambiguity.

**Performance order (fastest → slowest filter propagation)**
1. One-to-many intra-source relationships
2. Many-to-many via bridge table + at least one bi-directional relationship
3. Native many-to-many cardinality relationships
4. Cross-source group relationships

**Many-to-many with bridge table (best practice for dimension-to-dimension M:M)**
1. Add entity tables (e.g., `Account`, `Customer`).
2. Add a *factless fact table* / bridge table (e.g., `AccountCustomer`) with one row per association.
3. Create two one-to-many relationships: `Account 1→* AccountCustomer` and `Customer 1→* AccountCustomer`.
4. Set **one** of the relationships to bi-directional so filters propagate through to fact tables.

**USERELATIONSHIP** — activates an inactive relationship within a CALCULATE expression.

```dax
Sales by Shipping Date =
CALCULATE(
    SUM(Sales[SalesAmount]),
    USERELATIONSHIP(Sales[ShipDate], 'Date'[Date])
)
-- The active relationship (OrderDate → Date) is suspended; ShipDate → Date activated instead.
```

**CROSSFILTER** — modifies cross-filter direction for duration of expression evaluation.

```dax
Different Countries Sold =
CALCULATE(
    DISTINCTCOUNT(Customer[Country-Region]),
    CROSSFILTER(Customer[CustomerCode], Sales[CustomerCode], BOTH)
)
-- Direction values: None | Both | OneWay | OneWay_LeftFiltersRight | OneWay_RightFiltersLeft
```

**Referential integrity**:
- "Assume referential integrity" option: available for DirectQuery; tells Power BI to use
  INNER JOIN instead of LEFT OUTER JOIN → better query performance. Only safe when FK values
  all exist in PK table.
- For Direct Lake: one-side columns **must** contain unique values; queries fail if duplicates detected.

### Sources
- https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand
- https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many
- https://learn.microsoft.com/en-us/power-bi/guidance/relationships-bidirectional-filtering
- https://learn.microsoft.com/en-us/dax/userelationship-function-dax
- https://learn.microsoft.com/en-us/dax/crossfilter-function-dax

---

## o-3-1-4 — DAX Variables and Functions

### Facts

**VAR / RETURN**
- Variables improve **performance** (expression evaluated once, not repeatedly).
- Variables improve **readability** and enable **debugging** (temporarily return VAR value).
- Variables are always evaluated in the **outer** filter context, not the RETURN context
  (replaces need for EARLIER/EARLIEST in most cases).

```dax
Sales YoY Growth % =
VAR SalesPriorYear =
    CALCULATE([Sales], PARALLELPERIOD('Date'[Date], -12, MONTH))
RETURN
    DIVIDE([Sales] - SalesPriorYear, SalesPriorYear)
-- SalesPriorYear evaluated once; used twice in RETURN
```

**Iterator functions: SUMX / AVERAGEX**
- Iterate over a table row by row, evaluating an expression per row, then aggregate results.
- Syntax: `SUMX(<table>, <expression>)` / `AVERAGEX(<table>, <expression>)`

```dax
-- Revenue = quantity × unit price per row, then sum all rows
Revenue = SUMX(Sales, Sales[Qty] * Sales[UnitPrice])
-- Correct: iterates row by row; unlike SUM which can't do cross-column arithmetic
```

**CALCULATE / FILTER / ALL / ALLEXCEPT**
- `CALCULATE(<expression>, <filter1>, ...)` — evaluates expression in modified filter context.
- Best practice: use **Boolean expressions** as filter arguments (optimised for in-memory column stores):
  ```dax
  Red Sales = CALCULATE([Sales], 'Product'[Color] = "Red")         -- Boolean (fast)
  Red Sales = CALCULATE([Sales], FILTER('Product', 'Product'[Color] = "Red"))  -- table (slower)
  ```
- Use `FILTER` only when Boolean won't work: multi-table conditions, measure references, OR logic.
- `KEEPFILTERS` — use to preserve existing column filters instead of replacing them:
  ```dax
  Red Sales = CALCULATE([Sales], KEEPFILTERS('Product'[Color] = "Red"))
  ```
- `ALL(table)` / `ALL(table[column])` — removes all filters from table or specific column.
- `ALLEXCEPT(table, col1, col2, ...)` — removes all filters **except** the specified columns.
  Useful for running totals / % of total:
  ```dax
  % of Category = DIVIDE([Sales], CALCULATE([Sales], ALLEXCEPT('Product', 'Product'[Category])))
  ```

**Time intelligence — DATESYTD**
- `DATESYTD(<dates>[, <year_end_date>])` — returns YTD date set.
- Optional `year_end_date` for fiscal year (e.g., `"6-30"` for fiscal year ending June 30).
- Not supported in DirectQuery calculated columns / RLS rules.

```dax
YTD Sales = CALCULATE(SUM(Sales[Amount]), DATESYTD('Date'[Date]))
Fiscal YTD Sales = CALCULATE(SUM(Sales[Amount]), DATESYTD('Date'[Date], "6-30"))
```

**Windowing functions — WINDOW / OFFSET / INDEX**
- Introduced for non-visual-calculation use (measures and calculated columns) in addition to visual calculations.
- `WINDOW(from, from_type, to, to_type[, relation][, orderBy][, blanks][, partitionBy]...)`
  - `from_type` / `to_type`: `ABS` (absolute position, 1-based) or `REL` (relative to current row).
  - Returns **multiple rows** (a table) in the defined window.

```dax
-- 3-day rolling average of unit price per product
3-day Avg Price =
AVERAGEX(
    WINDOW(-2, REL, 0, REL,
        SUMMARIZE(ALLSELECTED('Sales'), 'Date'[Date], 'Product'[Product]),
        ORDERBY('Date'[Date]),
        KEEP,
        PARTITIONBY('Product'[Product])
    ),
    CALCULATE(AVERAGE(Sales[Unit Price]))
)
```

- `OFFSET(delta[, relation][, orderBy][, partitionBy]...)` — returns **single row** at relative offset.
  - Negative `delta` = look back; positive = look forward.

```dax
-- Difference vs previous month (visual calculation example)
SalesDiffPrevMonth = [SalesAmount] - CALCULATE(SUM([SalesAmount]), OFFSET(-1, ROWS, HIGHESTPARENT))
```

- `INDEX(position[, relation][, orderBy][, partitionBy]...)` — returns single row at **absolute** position.

**Information functions**

| Function | Returns | Use case |
|----------|---------|----------|
| `USERPRINCIPALNAME()` | UPN string at query time (e.g., `joe@contoso.com`) | Row-level security, personalisation |
| `HASONEVALUE(column)` | TRUE if exactly one value in filter context | Safe conditional checks |
| `SELECTEDVALUE(col[, alt])` | Single visible value, or `alt` if 0 or 2+ values | Preferred over `IF(HASONEVALUE(),VALUES())` |
| `ISBLANK(value)` | TRUE if BLANK | Null / empty guards |

```dax
-- Recommended pattern (SELECTEDVALUE)
Australian Tax =
IF(SELECTEDVALUE(Customer[Country]) = "Australia", [Sales] * 0.10)

-- Older verbose pattern (avoid)
Australian Tax =
IF(HASONEVALUE(Customer[Country]),
    IF(VALUES(Customer[Country]) = "Australia", [Sales] * 0.10))
```

**DIVIDE vs `/` operator**
- `DIVIDE(numerator, denominator[, alt])` — returns BLANK (or alt) on divide-by-zero; no need for IF guard.
- Use `/` only when denominator is a **constant** (faster; no zero-check overhead).

```dax
Margin % = DIVIDE([Profit], [Sales])   -- safe; returns BLANK when Sales = 0
```

### Sources
- https://learn.microsoft.com/en-us/power-bi/guidance/dax-variables
- https://learn.microsoft.com/en-us/power-bi/guidance/dax-avoid-avoid-filter-as-filter-argument
- https://learn.microsoft.com/en-us/power-bi/guidance/dax-selectedvalue
- https://learn.microsoft.com/en-us/power-bi/guidance/dax-divide-function-operator
- https://learn.microsoft.com/en-us/dax/window-function-dax
- https://learn.microsoft.com/en-us/dax/offset-function-dax
- https://learn.microsoft.com/en-us/dax/datesytd-function-dax
- https://learn.microsoft.com/en-us/dax/userprincipalname-function-dax
- https://learn.microsoft.com/en-us/dax/relationship-functions-dax

---

## o-3-1-5 — Calculation Groups, Dynamic Format Strings, and Field Parameters

### Facts

**Calculation groups**
- A table-like object containing *calculation items* that modify how existing measures are evaluated.
- Purpose: eliminate dozens of parallel measures (e.g., YTD, PY, YoY%) by applying
  the same logic dynamically to any selected measure.
- Key DAX function: `SELECTEDMEASURE()` — placeholder for the measure being evaluated by the
  calculation item.
- Enabling a calculation group **forces "Discourage implicit measures"** (blocks auto-aggregation
  columns; calculation items only apply to explicit measures).
- Each calculation group has a **precedence** integer that controls order of application when
  multiple calculation groups exist.
- Can be created in Model view, the ribbon button, or via TMDL script.
- `SELECTEDMEASURENAME()` and `ISNUMERIC(SELECTEDMEASURE())` useful for conditional logic.

```dax
-- Example calculation item: Year-over-Year %
YOY% =
DIVIDE(
    SELECTEDMEASURE() - CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date])),
    CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
)
```

**Dynamic format strings (per calculation item)**
- Each calculation item can have its own format string DAX expression.
- Toggle "Dynamic format string" on in the calculation item Properties pane.
- Example: `"#,##0.00%"` forces percentage display only for YOY% item, while other items keep
  the underlying measure format.

**Dynamic format strings (standalone, per measure)**
- Set on any measure independently of calculation groups.
- Prevents the FORMAT() function problem (FORMAT returns a text string, losing numeric type).
- In Measure tools ribbon: Format > Dynamic. Enter a DAX expression that returns a format string.
- The measure **keeps its data type** — visuals (charts) still receive numeric values.

```dax
-- Example: look up currency format from table based on slicer selection
[Measure Format] =
SELECTEDVALUE('Currency Formats'[Format], "#,##0.00")
-- Then set this expression as the Dynamic format string for the Sales Amount measure
```

**Field parameters**
- Allow report readers to dynamically switch the dimensions or measures shown in a visual.
- Created in Power BI Desktop: Modeling tab > New parameter > Fields.
- Backed by a calculated table with three columns per field entry: display name, NAMEOF() reference, order integer.

```dax
My Parameter = {
    ("Customer",  NAMEOF('Customer'[Customer]),  0),
    ("Category",  NAMEOF('Product'[Category]),   1),
    ("Color",     NAMEOF('Product'[Color]),       2)
}
```

- Can mix measures and dimensions in the same parameter.
- Add to slicer + use in visual field drop zones.
- Editing: modify DAX directly; separate entries with commas; use `Shift+Enter` for new lines.
- **Limitations**: no implicit measures, no AI visuals / Q&A support, can't be used as drill-through
  linked fields (use underlying fields directly), can't use with live connection (unless local model added).

### Sources
- https://learn.microsoft.com/en-us/power-bi/transform-model/calculation-groups
- https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-dynamic-format-strings
- https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters
- https://learn.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups

---

## o-3-1-6 — Large Semantic Model Storage Format, Scale-Out

### Facts

**Large semantic model storage format**
- Default service size limit: **1 GB** (standard for Pro/shared workspaces).
- Power BI Desktop upload limit: **10 GB** (unchanged by large model setting).
- With *Large semantic model storage format* enabled, size limit = capacity size
  (e.g., F64 capacity has 25 GB per-model max memory). Models **can grow beyond 10 GB on refresh**.
- Available on: **Fabric F SKUs, Premium P SKUs, Embedded A SKUs, PPU, and Pro workspaces
  on Reserved Capacity**. NOT available on standard Pro or Free without Premium.
- Also **required** to enable **XMLA write operations** even for small models.
- Default segment size when large format enabled: **8 million rows** (same as Azure Analysis Services).
- Storage format on disk changes from `ABF` (Analysis Services Backup File) to `PremiumFiles`.

**How to enable**
- Individual model: service > semantic model Settings > **Large semantic model storage format** slider = On.
- Workspace default: workspace Settings > Premium > Default storage format > Large semantic model storage format.
- PowerShell:
  ```powershell
  Set-PowerBIDataset -Id <Semantic model ID> -TargetStorageMode PremiumFiles
  ```

**Memory management**
- *Semantic model eviction*: inactive models evicted from memory to free capacity; reloaded on next query.
- *On-demand load* (default enabled): column pages paged in from OneLake/PremiumFiles on demand —
  dramatically faster reloads for evicted large models vs full reload.

**Considerations**
- Models near half the capacity size may fail refresh (memory spike during refresh ≈ 2× model size).
- Use XMLA endpoint / Enhanced refresh REST API for fine-grained partition refresh on very large models.

**Semantic model scale-out**
- Creates **read-only replicas** of the primary read-write semantic model.
- Query load distributed across replicas; primary handles writes and refreshes.
- **Prerequisites**: Large semantic model storage format enabled + Premium/Fabric F SKU capacity.
- Enable per-semantic-model via **Power BI REST API** (`queryScaleOutSettings`).
- By default, read-only replicas auto-sync after each refresh. Can disable for manual control.
- Default connections: Power BI Desktop + Live connection reports → **read-only replica**;
  XMLA clients → **read-write** semantic model.
- Force read-only or read-write by appending `?readonly` or `?readwrite` to connection URL.
- Total CUs consumed by all replicas cannot exceed the per-model SKU limit.
- Disabling Large semantic model storage format also **disables scale-out**.

### Sources
- https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-large-models
- https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-scale-out

---

## o-3-1-7 — Composite Models

### Facts

**Definition**: a semantic model containing tables in more than one storage mode, OR DirectQuery tables from different data sources.

**Supported composite model types (by tooling)**

| Combination | Tooling |
|-------------|---------|
| DQ to Power BI semantic model + Import/DQ | Power BI Desktop |
| DQ tables from different sources | Power BI Desktop |
| Import + DQ in same model | Power BI Desktop |
| Import + Direct Lake | Power BI web modeling only |
| DQ + Direct Lake | XMLA only |

- Note: **Direct Lake on SQL** is single-source and **cannot** be in a composite model. Direct Lake on OneLake can be combined with Import tables in web modeling.

**Chaining onto a published semantic model**
1. Live-connect to an existing Power BI semantic model.
2. Select **Make changes to this model** → converts live connection to DirectQuery connection.
3. Add local Import/DirectQuery tables on top of the published model's tables.

**Dual storage mode**
- Table marked as Dual = both Import (in-memory) and DirectQuery.
- Power BI chooses per query.
- Best practice: configure **dimension tables as Dual** when paired with DirectQuery fact tables.
  Enables Power BI to generate a single efficient native SQL join instead of two separate queries.

**Cross-source relationships**
- Created as **many-to-many by default** when tables come from different sources; can be changed.
- Performance impact vs same-source relationships.
- Cannot use DAX to retrieve "one-side" values from the "many" side across sources.

### Sources
- https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models
- https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand
- https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview

---

## o-3-2-1 — Performance Improvements in Queries and Report Visuals

### Facts

**Performance Analyzer**
- Found in: Power BI Desktop — **Optimize ribbon > Performance Analyzer**;
  in service — Edit a report > View menu > Performance Analyzer.
- Start recording, then interact with visuals; each interaction logged.
- Per-visual timing breakdown:
  - **DAX query** — time from query sent to results returned from semantic model.
  - **Direct query** — time for external query (DirectQuery tables only).
  - **Visual display** — time to render visual (images, geocoding included).
  - **Other** — query prep, waiting for other visuals, background processing.
  - **Evaluated parameters** — field parameter evaluation time.
- **"Copy query"** — exports the exact DAX sent by the visual to clipboard.
- **"Run in DAX query view"** — opens the DAX in query view for investigation/optimization.
- **Export** — saves a JSON log of all captured timings.

**Optimization strategies for reports and visuals**
- Reduce number of visuals per page — each visual fires at least one DAX query.
- Remove unused columns from queries (minimise visual field list).
- Pre-filter data in Power Query / at source before loading.
- Use Import mode or Dual for frequently queried dimension tables.
- Use aggregation tables for large DirectQuery models.
- Clear the data cache before baseline testing: `EVALUATE ROW("x", NOW())` in DAX Studio,
  or use the "Clear Data Cache" option.
- Consider Auto page refresh settings (can be source of excessive query load).

### Sources
- https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-performance-analyzer
- https://learn.microsoft.com/en-us/power-bi/guidance/report-performance-troubleshoot

---

## o-3-2-2 — Improve DAX Performance

### Facts

**Storage engine vs. formula engine**
- *Storage engine (SE)*: multi-threaded, columnar, highly optimised. Handles simple column
  filters, aggregations natively. Generates datacache results.
- *Formula engine (FE)*: single-threaded, handles complex expressions. Avoid pushing heavy
  logic here. High FE time in Performance Analyzer = optimisation opportunity.
- Goal: maximise SE work; minimise FE overhead.

**Use variables to avoid repeated CALCULATE**
```dax
-- Inefficient: PARALLELPERIOD(...) evaluated twice
Growth % = DIVIDE([Sales] - CALCULATE([Sales], PARALLELPERIOD(...)), CALCULATE([Sales], PARALLELPERIOD(...)))

-- Efficient: evaluated once
Growth % =
VAR PriorPeriodSales = CALCULATE([Sales], PARALLELPERIOD('Date'[Date], -12, MONTH))
RETURN DIVIDE([Sales] - PriorPeriodSales, PriorPeriodSales)
```

**Filter columns not tables**
- Boolean column filters → SE-optimised path.
- `FILTER(table, condition)` as filter arg → iterates entire table in FE → slower.
```dax
-- Preferred (Boolean)
Sales Red = CALCULATE([Sales], 'Product'[Color] = "Red")
-- Avoid for simple cases
Sales Red = CALCULATE([Sales], FILTER('Product', 'Product'[Color] = "Red"))
```

**Use KEEPFILTERS** to preserve existing filters when adding a Boolean filter:
```dax
CALCULATE([Sales], KEEPFILTERS('Product'[Color] = "Red"))
```

**DIVIDE over manual zero-check**
```dax
Margin % = DIVIDE([Profit], [Sales])   -- handles divide-by-zero, returns BLANK; no IF wrapper needed
```

**SELECTEDVALUE over HASONEVALUE + VALUES** — more concise, slightly more efficient.

**COUNTROWS over COUNT** — `COUNTROWS(table)` is more efficient, ignores BLANKs, and is self-documenting.

**Avoid complex calculated columns** that force row-by-row FE work at query time; prefer measures.

**Avoid scanning large tables with FILTER** — especially in measures applied to large fact tables; use column filters or pre-aggregated lookup tables.

### Sources
- https://learn.microsoft.com/en-us/power-bi/guidance/dax-variables
- https://learn.microsoft.com/en-us/power-bi/guidance/dax-avoid-avoid-filter-as-filter-argument
- https://learn.microsoft.com/en-us/power-bi/guidance/dax-selectedvalue
- https://learn.microsoft.com/en-us/power-bi/guidance/dax-divide-function-operator
- https://learn.microsoft.com/en-us/power-bi/guidance/dax-countrows

---

## o-3-2-3 — Configure Direct Lake (Framing, Fallback, Refresh)

### Facts

**Framing**
- A Direct Lake *refresh* operation is called **framing**; it is a **metadata-only** operation.
- Takes **seconds** (contrast: Import refresh can take minutes/hours).
- Process: semantic model reads the Delta log of each table, updates references to the latest
  Parquet files in OneLake, sets a new *baseline* for future transcoding events.
- Evicts resident column segments whose underlying data changed; **dictionaries usually NOT dropped**
  (incremental framing — minimises reload burden).
- After framing, all queries see data **as of the last framing point** — not necessarily the
  very latest files (important for consistency in long-running ETL scenarios).
- Framing fails if Delta table exceeds Fabric capacity guardrails (e.g., >10,000 Parquet files on F2).

**Column loading (transcoding)**
- On-demand: when a query needs a column not yet in memory, the engine loads the entire column
  from OneLake. Columns stay resident until evicted.
- Loading only the columns needed → efficient use of capacity memory.

**Automatic updates**
- Setting on the semantic model: enabled by default.
- Automatically frames the model when source Delta tables change → near real-time data.
- Disable when you need controlled framing (e.g., during long ETL writes for consistency).

**DirectQuery fallback (Direct Lake on SQL only)**
- Falls back when ANY of the following conditions exist:
  - SQL RLS, OLS, or DDM (dynamic data masking) detected at the SQL analytics endpoint.
  - Table based on an unmaterialized SQL view.
  - A single table exceeds Fabric capacity guardrails.
  - Semantic model not yet framed after table creation/modification.
- **DirectLakeBehavior** property controls this (set in Model view > Properties pane, or via TOM/TMSL):

| Value | Behaviour |
|-------|-----------|
| `Automatic` | (Default) Silent fallback to DirectQuery. Reports work; performance may degrade. |
| `DirectLakeOnly` | Query **fails** if conditions not met. Use during development to surface issues. |
| `DirectQueryOnly` | Always uses DirectQuery. Use to measure baseline fallback performance. |

- **Direct Lake on OneLake always runs in DirectLakeOnly mode** — never falls back.
- Diagnose fallback: `EVALUATE TABLETRAITS()` — check `[DirectLakeFallbackInfo]` column per table.
  A value of `None` = Direct Lake mode active.

**Common fallback fixes**

| Cause | Fix |
|-------|-----|
| Table not framed | Refresh (frame) the semantic model |
| Unmaterialized SQL view | Materialise view as Delta table, or accept DirectQuery |
| SQL RLS/OLS | Move security to semantic model RLS/OLS, or accept fallback |
| Delta table exceeds guardrails | OPTIMIZE + VACUUM the Delta table; upgrade SKU if needed |

### Sources
- https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-how-it-works
- https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview

---

## o-3-2-4 — Direct Lake on OneLake vs. Direct Lake on SQL Analytics Endpoint

### Facts

**Key comparison table**

| Capability | DL on OneLake | DL on SQL analytics endpoint |
|------------|---------------|------------------------------|
| Data source | Any Fabric item backed by Delta tables (lakehouse, warehouse, mirrored DB, etc.) | Single lakehouse or warehouse (via SQL analytics endpoint) |
| Multi-source support | Yes — can read from multiple Fabric items | No — single source only |
| DirectQuery fallback | **Never** — always DirectLakeOnly mode | **Yes** — when SQL security / views / guardrails trigger it |
| DirectLakeBehavior property | Not applicable (always DL only) | Applicable: Automatic / DirectLakeOnly / DirectQueryOnly |
| Composite models (with Import) | **Supported** — via Power BI web modeling | **Not supported** — cannot mix DL-on-SQL with DQ or Dual in same model |
| Calculated tables | **Yes (preview)** | No (except calculation groups, what-if, field params) |
| Calculated columns | **Yes (preview, unmaterialized)** — User Context only; no Standard Expression Context | No |
| Connect to SQL views | Not supported (non-materialised) | Yes — but causes DQ fallback |
| SQL analytics endpoint OLS/RLS | Not applied (OneLake security used) | Applied — causes DQ fallback if enforced |
| Recommended for new models | **Yes** (recommended default per docs) | Legacy option; use OneLake for new models |
| Licence requirement | Fabric capacity (F SKU or P SKU) | Fabric capacity (F SKU or P SKU) |

**Security semantics difference**
- DL on OneLake: uses **OneLake security** (file-level ACLs). SQL-based RLS is NOT applied; model-level RLS recommended.
- DL on SQL: uses SQL analytics endpoint security — RLS/OLS/DDM defined at SQL endpoint is honoured,
  but triggers DirectQuery fallback.
- Both modes: **Fabric fixed identity** cloud connection recommended when model-level RLS is defined.

**Guardrail behaviour difference**
- DL on OneLake: if guardrail exceeded, **refresh fails** and model cannot be queried until tables are optimised.
- DL on SQL: if guardrail exceeded (and fallback enabled), silently falls back to DirectQuery;
  refresh succeeds with a warning.

### Sources
- https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview
- https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-how-it-works

---

## o-3-2-5 — Implement Incremental Refresh

### Facts

**Purpose**: partition a table and refresh only the most recent data partition, reducing refresh time,
resource consumption, and enabling very large semantic models.

**Setup steps**
1. Create two reserved Power Query **DateTime** parameters, case-sensitive names:
   - `RangeStart` (DateTime)
   - `RangeEnd` (DateTime)
2. Filter the source table in Power Query using these parameters (must be a folding step):
   ```powerquery
   #"Filtered Rows" = Table.SelectRows(Source, each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd)
   ```
3. In Power BI Desktop: right-click table > **Incremental refresh and real-time data**.
4. Define the **Archive (Store data starting)** period and **Refresh (Refresh data in the last)** period.
5. Optionally enable **Detect data changes** (specify a timestamp column to check for changes).
6. Optionally enable **Get the latest data in real time with DirectQuery** (Premium only) to add a real-time DQ partition.
7. Publish to the Power BI service. Service creates partitions automatically on first refresh.

**Rolling window pattern**
- New refresh cycles create incremental partitions for the refresh period.
- Partitions outside the incremental window become historical (not re-refreshed).
- Partitions outside the archive window are dropped.
- Process is automatic and invisible in the service UI.

**Query folding — critical requirement**
- The `RangeStart`/`RangeEnd` filter **must fold** back to the data source as a native query predicate.
- If folding is not confirmed, Power BI Desktop shows a warning.
- Verify using Power Query Diagnostics or a profiling tool (e.g., SQL Profiler).
- For SQL sources (SQL Database, Azure Synapse, Oracle, Teradata): folding is reliable.
- Non-folding transformations after the source step break folding.

**Supported plans**
- Incremental refresh (Import only): Power BI Premium, PPU, Pro, Power BI Embedded.
- Real-time DirectQuery partition: **Premium, PPU, Embedded only** (not Pro).

**Refresh time limits**
- Pro: **2 hours** per refresh.
- Premium capacity: **5 hours** per refresh.
- XMLA endpoint refreshes: **no time limit**.

**Detect data changes**
- Optional optimisation: specify a "Last Modified" DateTime column.
- During refresh, Power BI checks whether any rows in a partition have a newer modification timestamp.
- Partitions with no changes skip the actual data reload, reducing refresh time further.

**Hybrid tables** (Import + DirectQuery)
- Created when "Get latest data in real time with DirectQuery" is enabled.
- Historical partitions = Import; most-recent partition = DirectQuery.
- Shows data as of the last refresh for historical data + real-time for the latest partition.
- Requires Premium capacity; configure dimension tables as **Dual** for best query performance.

**First publish**
- After publishing, the first refresh loads historical data per the archive period (may take a long time).
- Subsequent refreshes are fast (only the incremental period is refreshed).

### Sources
- https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview
- https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure
- https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand

---

## URL Index (all unique sources cited above)

1. https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand
2. https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview
3. https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models
4. https://learn.microsoft.com/en-us/power-bi/guidance/star-schema
5. https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand
6. https://learn.microsoft.com/en-us/power-bi/guidance/relationships-many-to-many
7. https://learn.microsoft.com/en-us/power-bi/guidance/relationships-bidirectional-filtering
8. https://learn.microsoft.com/en-us/dax/userelationship-function-dax
9. https://learn.microsoft.com/en-us/dax/crossfilter-function-dax
10. https://learn.microsoft.com/en-us/power-bi/guidance/dax-variables
11. https://learn.microsoft.com/en-us/power-bi/guidance/dax-avoid-avoid-filter-as-filter-argument
12. https://learn.microsoft.com/en-us/power-bi/guidance/dax-selectedvalue
13. https://learn.microsoft.com/en-us/power-bi/guidance/dax-divide-function-operator
14. https://learn.microsoft.com/en-us/dax/window-function-dax
15. https://learn.microsoft.com/en-us/dax/offset-function-dax
16. https://learn.microsoft.com/en-us/dax/datesytd-function-dax
17. https://learn.microsoft.com/en-us/dax/userprincipalname-function-dax
18. https://learn.microsoft.com/en-us/dax/relationship-functions-dax
19. https://learn.microsoft.com/en-us/power-bi/transform-model/calculation-groups
20. https://learn.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups
21. https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-dynamic-format-strings
22. https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters
23. https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-large-models
24. https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-scale-out
25. https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-performance-analyzer
26. https://learn.microsoft.com/en-us/power-bi/guidance/report-performance-troubleshoot
27. https://learn.microsoft.com/en-us/power-bi/guidance/dax-countrows
28. https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-how-it-works
29. https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview
30. https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure
