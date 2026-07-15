# AI-103 Study Guide — PUBLIC EDITION — CONTENT TEMPLATE CONTRACT

You are authoring ONE domain of a **shareable, clean-room** AI-103 study guide as an **HTML fragment**. A separate build step wraps it with CSS/JS and injects original SVG diagrams.

## ⛔ CLEAN-ROOM SOURCING RULE (most important)
- Ground **every** fact ONLY in your assigned **public Microsoft Learn source pack** (`learn_src_dN.md`) — which was gathered from public Microsoft Learn documentation.
- Do **NOT** use, reference, quote, or paraphrase any PowerPoint/instructor-deck, courseware, brain-dump, or real exam material. If a fact isn't supported by the public source pack, either omit it or keep it to well-known, non-copyrightable product facts — never invent specifics.
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
4. **Code** (where relevant) — `<div class="code"><pre><code class="lang-python">...</code></pre></div>`. Languages: `lang-python`, `lang-json`, `lang-bash`, `lang-powershell`, `lang-csharp`, `lang-yaml`, `lang-bicep`, `lang-rest` (rest maps to generic highlighting). Author minimal, correct, ORIGINAL examples. HTML-escape `<`, `>`, `&` inside code.
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
- Technical accuracy is paramount; where the source pack gives specifics (e.g., Foundry deployment types, RAG grounding, agent tool schemas, content safety filters, Content Understanding analyzers), follow them exactly.
- Depth: thorough but tight — precise bullets and short paragraphs.
- Cover EVERY objective in the outline; don't merge or skip.
- Include ≥1 short code example for objectives that involve SDK/config work (model deployment, RAG, agents, speech, search indexing, Content Understanding).
- SCOPE GUARD: cover exactly the measured skills below; do not add off-syllabus topics.
- Output ONLY the HTML fragment (one top-level `<section class="domain">…</section>`). No markdown, no code fences, no commentary.

## Objective outline & required IDs

### Domain 1 — Plan and manage an Azure AI solution (25–30%) → domain1.html, id="domain1"
- h2 `g-1-1` "1.1 Choose the appropriate Foundry services for generative AI and agents"
  - `o-1-1-1` 1.1.1 Choose an appropriate model for each task (LLMs, small language models, multimodal models, and Foundry Tools)
  - `o-1-1-2` 1.1.2 Choose the appropriate Foundry services for generative tasks, grounding, vector search, agent workflows, or multimodal processing
  - `o-1-1-3` 1.1.3 Choose an appropriate method for retrieval and indexing
  - `o-1-1-4` 1.1.4 Choose appropriate memory, tool, and knowledge integration services for agent solutions
- h2 `g-1-2` "1.2 Set up AI solutions in Foundry"
  - `o-1-2-1` 1.2.1 Design Azure infrastructure for AI apps and agent-based solutions
  - `o-1-2-2` 1.2.2 Choose appropriate deployment options
  - `o-1-2-3` 1.2.3 Configure model and agent deployments
  - `o-1-2-4` 1.2.4 Integrate Foundry projects with CI/CD pipelines
- h2 `g-1-3` "1.3 Manage, monitor, and secure AI systems"
  - `o-1-3-1` 1.3.1 Manage quotas, scaling, rate limits, and cost footprints for model and agent workloads
  - `o-1-3-2` 1.3.2 Monitor model performance, drift, safety events, and grounding quality
  - `o-1-3-3` 1.3.3 Monitor data ingestion quality, search index health, and relevance performance
  - `o-1-3-4` 1.3.4 Configure security, including managed identity, private networking, keyless credentials, and role policies
- h2 `g-1-4` "1.4 Implement responsible AI across generative AI and agentic systems"
  - `o-1-4-1` 1.4.1 Configure safety filters, guardrails, risk detection, and content moderation
  - `o-1-4-2` 1.4.2 Apply responsible AI instrumentation, including evaluators, safety evaluations, and explanation tooling
  - `o-1-4-3` 1.4.3 Implement auditing through trace logging, provenance metadata, and approval workflows
  - `o-1-4-4` 1.4.4 Govern agent behavior with oversight modes, constraints, and tool-access controls

### Domain 2 — Implement generative AI and agentic solutions (30–35%) → domain2.html, id="domain2"
- h2 `g-2-1` "2.1 Build generative applications by using Foundry"
  - `o-2-1-1` 2.1.1 Deploy and consume LLMs, small models, code models, and multimodal models
  - `o-2-1-2` 2.1.2 Implement retrieval-augmented generation (RAG) in an application
  - `o-2-1-3` 2.1.3 Design workflows, tool-augmented flows, and multistep reasoning pipelines
  - `o-2-1-4` 2.1.4 Evaluate models and apps, including detecting fabrications, relevance, quality, and safety
  - `o-2-1-5` 2.1.5 Integrate generative workflows into applications by using Foundry SDKs and connectors
  - `o-2-1-6` 2.1.6 Configure an application to connect to a Foundry project
- h2 `g-2-2` "2.2 Build agents by using Foundry"
  - `o-2-2-1` 2.2.1 Define agent roles, goals, conversation-tracking approach, and tool schemas
  - `o-2-2-2` 2.2.2 Build agents that integrate retrieval, function-calling, and conversation memory
  - `o-2-2-3` 2.2.3 Integrate agent tools, including APIs, knowledge stores, search, content understanding, and custom functions
  - `o-2-2-4` 2.2.4 Implement orchestrated multi-agent solutions
  - `o-2-2-5` 2.2.5 Build autonomous or semiautonomous workflows with safeguards and approval flow controls
  - `o-2-2-6` 2.2.6 Integrate monitoring into deployed agents, evaluate agent behavior, and perform error analysis
- h2 `g-2-3` "2.3 Optimize and operationalize generative AI systems"
  - `o-2-3-1` 2.3.1 Tune generation behavior, such as prompt engineering and adjusting model parameters
  - `o-2-3-2` 2.3.2 Implement model reflection, chain-of-thought evaluations, and self-critique loops
  - `o-2-3-3` 2.3.3 Set up observability by implementing tracing, token analytics, safety signals, and latency breakdowns
  - `o-2-3-4` 2.3.4 Orchestrate multiple models, flows, or hybrid LLM and rules engines

### Domain 3 — Implement computer vision solutions (10–15%) → domain3.html, id="domain3"
- h2 `g-3-1` "3.1 Design and implement image- and video-generation solutions"
  - `o-3-1-1` 3.1.1 Implement a solution that generates images from text prompts and reference media
  - `o-3-1-2` 3.1.2 Implement a solution that generates videos from text prompts and reference media
  - `o-3-1-3` 3.1.3 Configure image-editing workflows, including inpainting, mask-based edits, and prompt-driven modifications
  - `o-3-1-4` 3.1.4 Implement workflows to edit generated videos
  - `o-3-1-5` 3.1.5 Select and apply appropriate generation and editing controls provided by the platform
- h2 `g-3-2` "3.2 Design and implement multimodal understanding workflows"
  - `o-3-2-1` 3.2.1 Build a solution that analyzes visual context by using multimodal models
  - `o-3-2-2` 3.2.2 Configure apps to produce concise or detailed captions for single or multiple images
  - `o-3-2-3` 3.2.3 Implement a solution that enables question-answering grounded in visual evidence
  - `o-3-2-4` 3.2.4 Configure generation of alt-text and extended image descriptions aligned to accessibility guidelines
  - `o-3-2-5` 3.2.5 Implement visual understanding by configuring Azure Content Understanding in Foundry Tools to extract visual characteristics
  - `o-3-2-6` 3.2.6 Implement video analysis workflows to process and interpret video segments
  - `o-3-2-7` 3.2.7 Configure single-task and pro-mode Content Understanding pipelines
  - `o-3-2-8` 3.2.8 Implement solutions that identify objects, components, or regions within images or video
- h2 `g-3-3` "3.3 Implement responsible AI for multimodal content"
  - `o-3-3-1` 3.3.1 Implement filters to classify unsafe or disallowed visual content
  - `o-3-3-2` 3.3.2 Detect and mitigate indirect prompt injection by using embedded text in images
  - `o-3-3-3` 3.3.3 Enforce visual policy rules, such as watermarks, flagging prohibited symbols, brand usage, and detecting inappropriate content

### Domain 4 — Implement text analysis solutions (10–15%) → domain4.html, id="domain4"
- h2 `g-4-1` "4.1 Apply language model text analysis"
  - `o-4-1-1` 4.1.1 Extract entities, topics, summaries, and structured JSON outputs by using generative prompting and Foundry Tools
  - `o-4-1-2` 4.1.2 Configure detection of sentiment, tone, safety issues, and sensitive content
  - `o-4-1-3` 4.1.3 Translate text by using Azure Translator in Foundry Tools or LLM-powered translation flows
  - `o-4-1-4` 4.1.4 Customize language model outputs for domain tasks, such as compliance summarization and domain extraction
- h2 `g-4-2` "4.2 Implement speech solutions"
  - `o-4-2-1` 4.2.1 Convert speech to text and text to speech for agentic interactions
  - `o-4-2-2` 4.2.2 Integrate speech as an agent modality, including custom speech models
  - `o-4-2-3` 4.2.3 Enable multimodal reasoning from audio inputs
  - `o-4-2-4` 4.2.4 Translate speech into other languages by using language models and Foundry Tools

### Domain 5 — Implement information extraction solutions (10–15%) → domain5.html, id="domain5"
- h2 `g-5-1` "5.1 Build retrieval and grounding pipelines"
  - `o-5-1-1` 5.1.1 Ingest and index content, such as documents, images, audio, and video
  - `o-5-1-2` 5.1.2 Configure semantic search, hybrid search, and vector search for grounding
  - `o-5-1-3` 5.1.3 Implement enrichment by using custom or built-in skills for text, images, and layout
  - `o-5-1-4` 5.1.4 Configure RAG ingestion flow, including documents and using optical character recognition (OCR)
  - `o-5-1-5` 5.1.5 Connect retrieval pipelines directly to workflows and agent tools
- h2 `g-5-2` "5.2 Extract content from documents"
  - `o-5-2-1` 5.2.1 Extract information by using multimodal pipelines that combine OCR, layout analysis, and field extraction
  - `o-5-2-2` 5.2.2 Produce clean, grounded representations to use with agents and RAG by using Content Understanding
  - `o-5-2-3` 5.2.3 Implement analyzers for generating structured or markdown outputs for downstream reasoning by using Content Understanding
