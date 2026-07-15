# DP-600 Study Guide — PUBLIC EDITION — CONTENT TEMPLATE CONTRACT

You are authoring ONE domain of a **shareable, clean-room** DP-600 study guide as an **HTML fragment**. A separate build step wraps it with CSS/JS and injects original SVG diagrams.

## ⛔ CLEAN-ROOM SOURCING RULE (most important)
- Ground **every** fact ONLY in your assigned **public Microsoft Learn source pack** (`learn_src_dN.md`) — which was gathered from public Microsoft Learn documentation.
- Do **NOT** use, reference, quote, or paraphrase any PowerPoint/instructor-deck material. Do not read deck files. If a fact isn't supported by the public source pack, either omit it or keep it to well-known, non-copyrightable product facts — never invent specifics.
- Paraphrase in your own words. Never paste passages from Learn verbatim; state facts plainly.

## Heading hierarchy (drives the auto Table of Contents)
- `<h1>` = the Domain (one per file). `<h2>` = skill group. `<h3>` = individual objective.
- EVERY h1/h2/h3 MUST have the stable `id` specified in the outline below.

## Wrapper structure
```html
<section class="domain" id="domainN" data-domain="N">
  <h1 id="dN">Domain N — ... <span class="weight">25–30%</span></h1>
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
2. **Key facts** — `<div class="facts"><h4>Key facts</h4><ul><li>...</li></ul></div>` — testable specifics (settings, roles, limits, steps, defaults).
3. **Diagram** (where a visual genuinely helps) — reference an ORIGINAL SVG from the diagram library BY ID:
   `<figure class="diagram" data-svg="DIAGRAM-ID"><figcaption>Caption in your words.</figcaption></figure>`
   Use only ids listed in `diagram_catalog.md`. Do NOT write raster `<img>` tags, do NOT reference any .png/slide. The build injects the inline SVG.
4. **Code** (for SQL/KQL/DAX/M/PySpark objectives) — `<div class="code"><pre><code class="lang-sql">...</code></pre></div>`. Languages: `lang-sql`, `lang-kql`, `lang-dax`, `lang-python`, `lang-m`, `lang-json`. Author minimal, correct, ORIGINAL examples. HTML-escape `<`, `>`, `&` inside code.
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
Use the real public Microsoft Learn URLs recorded in your source pack for this objective (1–3 links). These reinforce that the guide is grounded in public docs.

## Writing rules
- Technical accuracy is paramount; where the source pack gives specifics (e.g., Direct Lake framing/fallback, incremental refresh RangeStart/RangeEnd, XMLA read-write), follow them exactly.
- Depth: thorough but tight — precise bullets and short paragraphs.
- Cover EVERY objective in the outline; don't merge or skip.
- Include ≥1 code example for every Domain-2 §2.2/§2.3 objective and every DAX/optimize objective in Domain 3.
- SCOPE GUARD: exclude "Prepare for AI", Copilot grounding, and Fabric IQ/ontology — not on the exam.
- Output ONLY the HTML fragment (one top-level `<section class="domain">…</section>`). No markdown, no code fences, no commentary.

## Objective outline & required IDs
### Domain 1 — Maintain a data analytics solution (25–30%) → domain1.html, id="domain1"
- h2 `g-1-1` "1.1 Implement security and governance"
  - `o-1-1-1` 1.1.1 Implement workspace-level access controls
  - `o-1-1-2` 1.1.2 Implement item-level access controls
  - `o-1-1-3` 1.1.3 Implement row-level, column-level, object-level, and file-level access control
  - `o-1-1-4` 1.1.4 Apply sensitivity labels to items
  - `o-1-1-5` 1.1.5 Endorse items
- h2 `g-1-2` "1.2 Maintain the analytics development lifecycle"
  - `o-1-2-1` 1.2.1 Configure version control for a workspace
  - `o-1-2-2` 1.2.2 Create and manage a Power BI Desktop project (.pbip)
  - `o-1-2-3` 1.2.3 Create and configure deployment pipelines
  - `o-1-2-4` 1.2.4 Perform impact analysis of downstream dependencies (lakehouses, warehouses, dataflows, semantic models)
  - `o-1-2-5` 1.2.5 Deploy and manage semantic models by using the XMLA endpoint
  - `o-1-2-6` 1.2.6 Create and update reusable assets (.pbit, .pbids, shared semantic models)

### Domain 2 — Prepare data (45–50%) → domain2.html, id="domain2"
- h2 `g-2-1` "2.1 Get data"
  - `o-2-1-1` 2.1.1 Create a data connection
  - `o-2-1-2` 2.1.2 Discover data by using OneLake catalog and Real-Time hub
  - `o-2-1-3` 2.1.3 Ingest or access data as needed
  - `o-2-1-4` 2.1.4 Choose between different data stores
  - `o-2-1-5` 2.1.5 Implement OneLake integration for Eventhouse and semantic models
- h2 `g-2-2` "2.2 Transform data"
  - `o-2-2-1` 2.2.1 Create views, functions, and stored procedures
  - `o-2-2-2` 2.2.2 Enrich data by adding new columns or tables
  - `o-2-2-3` 2.2.3 Implement a star schema for a lakehouse or warehouse
  - `o-2-2-4` 2.2.4 Denormalize data
  - `o-2-2-5` 2.2.5 Aggregate data
  - `o-2-2-6` 2.2.6 Merge or join data
  - `o-2-2-7` 2.2.7 Identify and resolve duplicate data, missing data, or null values
  - `o-2-2-8` 2.2.8 Convert column data types
  - `o-2-2-9` 2.2.9 Filter data
- h2 `g-2-3` "2.3 Query and analyze data"
  - `o-2-3-1` 2.3.1 Select, filter, and aggregate data by using the Visual Query Editor
  - `o-2-3-2` 2.3.2 Select, filter, and aggregate data by using SQL
  - `o-2-3-3` 2.3.3 Select, filter, and aggregate data by using KQL
  - `o-2-3-4` 2.3.4 Select, filter, and aggregate data by using DAX

### Domain 3 — Implement and manage semantic models (25–30%) → domain3.html, id="domain3"
- h2 `g-3-1` "3.1 Design and build semantic models"
  - `o-3-1-1` 3.1.1 Choose a storage mode
  - `o-3-1-2` 3.1.2 Implement a star schema for a semantic model
  - `o-3-1-3` 3.1.3 Implement relationships, such as bridge tables and many-to-many relationships
  - `o-3-1-4` 3.1.4 Write calculations that use DAX variables and functions (iterators, table filtering, windowing, information functions)
  - `o-3-1-5` 3.1.5 Implement calculation groups, dynamic format strings, and field parameters
  - `o-3-1-6` 3.1.6 Identify use cases for and configure large semantic model storage format
  - `o-3-1-7` 3.1.7 Design and build composite models
- h2 `g-3-2` "3.2 Optimize enterprise-scale semantic models"
  - `o-3-2-1` 3.2.1 Implement performance improvements in queries and report visuals
  - `o-3-2-2` 3.2.2 Improve DAX performance
  - `o-3-2-3` 3.2.3 Configure Direct Lake, including default fallback and refresh behavior
  - `o-3-2-4` 3.2.4 Choose between Direct Lake on OneLake and Direct Lake on SQL analytics endpoint
  - `o-3-2-5` 3.2.5 Implement incremental refresh for semantic models
