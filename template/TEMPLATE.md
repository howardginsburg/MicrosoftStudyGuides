# Study Guide — PUBLIC EDITION — CONTENT TEMPLATE CONTRACT

> **This is an agent-facing contract.** The `GENERATE_PUBLIC_STUDY_GUIDE` prompt fills in `<EXAM>` and
> the objective outline (bottom section) from the official Skills Measured page, then hands one copy of
> this contract to each domain-authoring sub-agent. You don't edit it by hand.
> `guides/DP-600/content/TEMPLATE_PUBLIC.md` shows a fully filled-in version.

You are authoring ONE domain of a **shareable, clean-room** study guide for exam **`<EXAM>`** as an **HTML fragment**. A separate build step (`engine/build_public.py`) wraps it with CSS/JS and injects original SVG diagrams.

## ⛔ CLEAN-ROOM SOURCING RULE (most important)
- Ground **every** fact ONLY in your assigned **public Microsoft Learn source pack** (`learn_src_dN.md`), gathered from public Microsoft Learn documentation via the Microsoft Learn MCP tools.
- Do **NOT** use, reference, quote, or paraphrase any PowerPoint / instructor-deck / courseware / brain-dump material. If a fact isn't supported by the public source pack, omit it or keep it to well-known, non-copyrightable product facts — never invent specifics.
- Paraphrase in your own words. Never paste passages from Learn verbatim.
- Every external link must resolve to `learn.microsoft.com` (the build fails otherwise).

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
   Use only ids listed in `diagram_catalog.md`. Do NOT write raster `<img>` tags or reference any .png/slide. The build injects the inline SVG.
4. **Code** (for query/scripting objectives) — `<div class="code"><pre><code class="lang-sql">...</code></pre></div>`.
   Supported languages: `lang-sql`, `lang-kql`, `lang-dax`, `lang-python`, `lang-m`, `lang-json`,
   `lang-powershell`, `lang-bash`, `lang-csharp`, `lang-javascript`, `lang-typescript`, `lang-yaml`,
   `lang-bicep`. Any other `lang-<x>` still gets generic highlighting; to enrich one, add it to
   `engine/languages.json` (never edit the engine code). Use lowercase/alphanumeric ids (e.g. `csharp`, not `c#`).
   Author minimal, correct, ORIGINAL examples. HTML-escape `<`, `>`, `&` inside code.
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
- Technical accuracy is paramount; follow the source pack's specifics exactly.
- Depth: thorough but tight — precise bullets and short paragraphs.
- Cover EVERY objective in the outline; don't merge or skip.
- Include ≥1 code example for every query/scripting/optimize objective.
- SCOPE GUARD: include exactly the measured skills; exclude anything not on the published Skills Measured list.
- Output ONLY the HTML fragment (one top-level `<section class="domain">…</section>`). No markdown, no code fences, no commentary.

## Objective outline & required IDs
<!-- Paste the exam's real domains, weightings, skill groups, and objectives here, each with its
     stable id (domainN / dN / g-N-M / sg-N-M / o-N-M-K / obj-N-M-K), one file per domain
     (domain1.html id="domain1", etc.). See guides/DP-600/content/TEMPLATE_PUBLIC.md for a model. -->
