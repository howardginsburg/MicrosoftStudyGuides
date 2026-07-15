# GH-300 Study Guide — PUBLIC EDITION — CONTENT TEMPLATE CONTRACT

You are authoring ONE domain of a **shareable, clean-room** GH-300 (GitHub Copilot) study guide as an
**HTML fragment**. A separate build step wraps it with CSS/JS and injects original SVG diagrams.

## ⛔ CLEAN-ROOM SOURCING RULE (most important)
- Ground **every** fact ONLY in your assigned **public Microsoft Learn source pack** (`learn_src_dN.md`),
  gathered from public Microsoft Learn documentation (learn.microsoft.com).
- Do **NOT** use, reference, quote, or paraphrase any PowerPoint/instructor-deck material, GitHub Docs
  (docs.github.com), blogs, or brain-dumps. **Every hyperlink in the output MUST be a learn.microsoft.com
  URL — the build FAILS on any other host.** If a fact isn't supported by the public source pack, either
  omit it or keep it to well-known, non-copyrightable product facts — never invent specifics.
- Paraphrase in your own words. Never paste passages from Learn verbatim; state facts plainly.

## Heading hierarchy (drives the auto Table of Contents)
- `<h1>` = the Domain (one per file). `<h2>` = skill group. `<h3>` = individual objective.
- EVERY h1/h2/h3 MUST have the stable `id` specified in the outline below.

## Wrapper structure
```html
<section class="domain" id="domainN" data-domain="N">
  <h1 id="dN">Domain N — ... <span class="weight">15–20%</span></h1>
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
1. **Concept** — `<div class="concept"><p>...</p></div>` — what it is / why / how. 1–3 short paragraphs.
2. **Key facts** — `<div class="facts"><h4>Key facts</h4><ul><li>...</li></ul></div>` — testable specifics
   (settings, plan tiers, commands, limits, defaults, steps).
3. **Diagram** (where a visual genuinely helps) — reference an ORIGINAL SVG from the diagram library BY ID:
   `<figure class="diagram" data-svg="DIAGRAM-ID"><figcaption>Caption in your words.</figcaption></figure>`
   Use only ids listed in `diagram_catalog.md`. No raster `<img>`, no .png/slide references.
4. **Code** (where relevant) — `<div class="code"><pre><code class="lang-bash">...</code></pre></div>`. Languages:
   `lang-bash`, `lang-powershell`, `lang-json`, `lang-yaml`, `lang-python`, `lang-javascript`,
   `lang-typescript`, `lang-csharp`. Author minimal, correct, ORIGINAL examples. HTML-escape `<`, `>`, `&`.
5. **Callouts** (optional): `<div class="callout key">`, `<div class="callout tip">`, `<div class="callout warn">`
   with `<b>Key:/Tip:/Gotcha:</b>`.
6. **Exam tips & gotchas** — `<div class="tips"><h4>Exam tips &amp; gotchas</h4><ul><li>...</li></ul></div>`
   — 2–5 distinguishing points.
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
Use the real public learn.microsoft.com URLs recorded in your source pack (1–3 links).

## Writing rules
- Technical accuracy is paramount. Distinguish the three plan tiers (Copilot **Free**, **Pro/Pro+**,
  **Business**, **Enterprise**) precisely where the source pack specifies which features/settings each has.
- Depth: thorough but tight — precise bullets and short paragraphs.
- Cover EVERY objective in the outline; don't merge or skip.
- Output ONLY the HTML fragment (one top-level `<section class="domain">…</section>`). No markdown, no code
  fences, no commentary.

---

# EXAM OUTLINE — stable heading ids (GH-300, Skills measured as of Aug 7, 2026)

## Domain 1 — Use GitHub Copilot responsibly  `#domain1` / h1 `#d1`  (15–20%)
### 1.1 Understand responsible AI principles  `#sg-1-1` / h2 `#g-1-1`
- 1.1.1 Describe the risks and limitations of generative AI tools — `#obj-1-1-1` / h3 `#o-1-1-1`
- 1.1.2 Describe ethical and responsible AI usage — `#obj-1-1-2` / h3 `#o-1-1-2`
- 1.1.3 Identify potential harms and mitigation strategies of AI usage — `#obj-1-1-3` / h3 `#o-1-1-3`
### 1.2 Validate and operate AI tools  `#sg-1-2` / h2 `#g-1-2`
- 1.2.1 Explain the need to validate AI output — `#obj-1-2-1` / h3 `#o-1-2-1`
- 1.2.2 Identify how to operate GitHub Copilot responsibly — `#obj-1-2-2` / h3 `#o-1-2-2`

## Domain 2 — Use GitHub Copilot features  `#domain2` / h1 `#d2`  (25–30%)
### 2.1 Use GitHub Copilot in the IDE  `#sg-2-1` / h2 `#g-2-1`
- 2.1.1 Enable Copilot in the IDE — `#obj-2-1-1` / h3 `#o-2-1-1`
- 2.1.2 Trigger Copilot through inline suggestions, chat, CLI, and agent mode — `#obj-2-1-2` / h3 `#o-2-1-2`
- 2.1.3 Configure content exclusions for specific files or repositories — `#obj-2-1-3` / h3 `#o-2-1-3`
### 2.2 Use GitHub Copilot CLI  `#sg-2-2` / h2 `#g-2-2`
- 2.2.1 Define GitHub Copilot CLI and how it benefits developers — `#obj-2-2-1` / h3 `#o-2-2-1`
- 2.2.2 Identify the steps for installing GitHub Copilot CLI — `#obj-2-2-2` / h3 `#o-2-2-2`
- 2.2.3 Describe key GitHub Copilot CLI features and commands — `#obj-2-2-3` / h3 `#o-2-2-3`
- 2.2.4 Use GitHub Copilot CLI interactively and in sessions — `#obj-2-2-4` / h3 `#o-2-2-4`
- 2.2.5 Generate scripts and manage files with GitHub Copilot CLI — `#obj-2-2-5` / h3 `#o-2-2-5`
### 2.3 Use GitHub Copilot features and capabilities  `#sg-2-3` / h2 `#g-2-3`
- 2.3.1 Use Agent Mode, Copilot Edits, and MCP; manage Agent Sessions and delegate to Sub-Agents — `#obj-2-3-1` / h3 `#o-2-3-1`
- 2.3.2 Use Copilot for code review and coding assistance — `#obj-2-3-2` / h3 `#o-2-3-2`
- 2.3.3 Utilize Spaces, Spark, pull request summaries, and instructions files — `#obj-2-3-3` / h3 `#o-2-3-3`
- 2.3.4 Understand Copilot Chat limits, options, feedback, commands, and prompt files — `#obj-2-3-4` / h3 `#o-2-3-4`
### 2.4 Manage organization-wide settings and policies  `#sg-2-4` / h2 `#g-2-4`
- 2.4.1 Configure organization-wide policy management and Copilot Code Review policies — `#obj-2-4-1` / h3 `#o-2-4-1`
- 2.4.2 Utilize audit log events — `#obj-2-4-2` / h3 `#o-2-4-2`
- 2.4.3 Manage subscriptions using the REST API — `#obj-2-4-3` / h3 `#o-2-4-3`

## Domain 3 — Understand GitHub Copilot data and architecture  `#domain3` / h1 `#d3`  (10–15%)
### 3.1 Describe data handling and flow  `#sg-3-1` / h2 `#g-3-1`
- 3.1.1 Explain data usage, flow, and sharing — `#obj-3-1-1` / h3 `#o-3-1-1`
- 3.1.2 Describe input processing and prompt building — `#obj-3-1-2` / h3 `#o-3-1-2`
- 3.1.3 Explain proxy filtering and post-processing — `#obj-3-1-3` / h3 `#o-3-1-3`
### 3.2 Understand lifecycle and limitations  `#sg-3-2` / h2 `#g-3-2`
- 3.2.1 Visualize the code suggestion lifecycle — `#obj-3-2-1` / h3 `#o-3-2-1`
- 3.2.2 Describe the limitations of LLMs and Copilot — `#obj-3-2-2` / h3 `#o-3-2-2`

## Domain 4 — Apply prompt engineering and context crafting  `#domain4` / h1 `#d4`  (10–15%)
### 4.1 Craft effective prompts  `#sg-4-1` / h2 `#g-4-1`
- 4.1.1 Describe prompt structure and context — `#obj-4-1-1` / h3 `#o-4-1-1`
- 4.1.2 Understand how context is determined — `#obj-4-1-2` / h3 `#o-4-1-2`
- 4.1.3 Use zero-shot and few-shot prompting — `#obj-4-1-3` / h3 `#o-4-1-3`
- 4.1.4 Apply best practices for prompt crafting — `#obj-4-1-4` / h3 `#o-4-1-4`
### 4.2 Engineer prompts for performance  `#sg-4-2` / h2 `#g-4-2`
- 4.2.1 Explain prompt engineering principles — `#obj-4-2-1` / h3 `#o-4-2-1`
- 4.2.2 Describe prompt process flow and chat history usage — `#obj-4-2-2` / h3 `#o-4-2-2`

## Domain 5 — Improve developer productivity with GitHub Copilot  `#domain5` / h1 `#d5`  (10–15%)
### 5.1 Enhance productivity and code quality  `#sg-5-1` / h2 `#g-5-1`
- 5.1.1 Use Copilot for code generation, refactoring, and documentation — `#obj-5-1-1` / h3 `#o-5-1-1`
- 5.1.2 Accelerate learning and reduce context switching — `#obj-5-1-2` / h3 `#o-5-1-2`
- 5.1.3 Generate sample data and modernize legacy code — `#obj-5-1-3` / h3 `#o-5-1-3`
### 5.2 Support testing and security  `#sg-5-2` / h2 `#g-5-2`
- 5.2.1 Generate unit and integration tests — `#obj-5-2-1` / h3 `#o-5-2-1`
- 5.2.2 Identify edge cases and write assertions — `#obj-5-2-2` / h3 `#o-5-2-2`
- 5.2.3 Suggest security improvements and performance optimizations — `#obj-5-2-3` / h3 `#o-5-2-3`

## Domain 6 — Configure privacy, content exclusions, and safeguards  `#domain6` / h1 `#d6`  (10–15%)
### 6.1 Manage privacy settings and exclusions  `#sg-6-1` / h2 `#g-6-1`
- 6.1.1 Configure content exclusions and editor settings — `#obj-6-1-1` / h3 `#o-6-1-1`
- 6.1.2 Describe ownership and limitations of outputs — `#obj-6-1-2` / h3 `#o-6-1-2`
### 6.2 Apply safeguards and troubleshoot  `#sg-6-2` / h2 `#g-6-2`
- 6.2.1 Enable suggestions matching public code filtering — `#obj-6-2-1` / h3 `#o-6-2-1`
- 6.2.2 Resolve issues with suggestions and content exclusions — `#obj-6-2-2` / h3 `#o-6-2-2`
