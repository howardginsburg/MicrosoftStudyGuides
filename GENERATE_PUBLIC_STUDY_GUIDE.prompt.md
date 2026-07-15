# Generate or Refresh a Public Certification Study Guide

This repo (**MicrosoftStudyGuides**) hosts community-built, clean-room study guides for Microsoft
certification exams and publishes them as a GitHub Pages site. This prompt drives two workflows:

- **Create** a new guide for an exam number, or
- **Refresh** an existing guide against the latest Skills Measured blueprint + Microsoft Learn docs.

**How to run:** open the repo with an AI coding agent and say either
*"Use GENERATE_PUBLIC_STUDY_GUIDE to **create** a guide for exam `DP-700`"* or
*"Use GENERATE_PUBLIC_STUDY_GUIDE to **refresh** `DP-600`"*.
If no exam number is given, **ask for it first** (ask_user), and confirm create-vs-refresh.

---

## Repo layout you operate on
```
guides/<EXAM>/            SOURCE for one guide (not served directly)
  config.json             exam metadata + catalog fields + fragment order
  make_diagrams.py        generates this exam's original inline-SVG library
  content/                frontmatter.html, domain1..N.html, appendices.html,
                          learn_src_dN.md (research), TEMPLATE_PUBLIC.md, diagram_catalog.md
  assets/diagrams/*.svg   original SVGs
engine/                   reusable, exam-agnostic build tooling (do not special-case an exam here)
  build_public.py         one guide  -> docs/<EXAM>.html   (self-contained; inlines CSS/JS/SVG)
  build_index.py          all configs -> docs/guides.json  (catalog manifest)
  build_all.py            build every guide + regenerate the manifest
  languages.json          shared syntax-highlighting language pack (add a language here, not in code)
  assets/                 shared UI (screen.css, print.css, app.js) inlined into every guide
template/                 config.example.json, TEMPLATE.md (authoring contract)
docs/                     PUBLISHED Pages site (flat files) -> committed
  index.html              static landing page; JS fetches guides.json and renders cards
  guides.json             generated catalog manifest
  <EXAM>.html             each built guide
```
**Pages URL:** `https://howardginsburg.github.io/MicrosoftStudyGuides/` — a guide is
`.../MicrosoftStudyGuides/<EXAM>.html`. The site is served from `/docs` on the default branch, so
built HTML lives ONLY in `/docs`; guide folders keep source only. Landing/manifest links stay
**relative** (`DP-600.html`, `guides.json`) so they resolve under the repo subpath.

---

## 🔒 Clean-room sourcing rule (non-negotiable)
Everything must be **original** and grounded **only in publicly available Microsoft Learn
documentation** plus the official Skills Measured outline. This is what makes the guides shareable.
- Ground every fact via the **Microsoft Learn MCP tools** (`MicrosoftDocs-microsoft_docs_search`,
  `-microsoft_docs_fetch`, `-microsoft_code_sample_search`). These are deferred tools — search for
  them first if not surfaced.
- **Paraphrase** — never paste passages verbatim. Product facts/behaviors aren't copyrightable;
  specific wording, images, and training materials are.
- **Do NOT use any instructor decks, PowerPoints, courseware, brain-dumps, or real exam questions.**
  All practice questions must be original scenarios you write.
- **Author all diagrams as original inline SVG** in your own visual style. Never embed Microsoft
  images, slide renders, or third-party graphics.
- Every external link in the output must resolve to `learn.microsoft.com` (the build fails otherwise).

---

## FLOW A — Create a NEW guide

### 1. Scaffold
Copy `guides/DP-600` → `guides/<EXAM>` as the skeleton, then clear DP-600-specific content (you will
replace `config.json`, `content/*.html`, `make_diagrams.py`, and `assets/diagrams/*`). Keep the engine
and `template/` untouched.

### 2. Get the blueprint
- Fetch the official study guide: `https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/<EXAM>`
  (follow redirects to the current Skills Measured section).
- Extract the **exact** domains, their **weightings**, and every measured **objective** (verbatim titles).
- Assign stable heading ids: domains `domainN`/`dN`, skill groups `g-N-M`/`sg-N-M`, objectives `o-N-M-K`
  (wrapper `obj-N-M-K`). Fill `guides/<EXAM>/content/TEMPLATE_PUBLIC.md`'s outline (see the DP-600 one as a model).
- Fill `guides/<EXAM>/config.json`: `exam`, `title`, `description`, `doc_title`, `brand`, `brand_sub`,
  `official_url`, `weights` (domain→%), `status` ("complete" when done), `last_refreshed` (today),
  `fragments` (one per domain + frontmatter/appendices), `output_html` = `<EXAM>.html`.
- Scope: include exactly the measured skills; exclude off-syllabus topics. Confirm judgment calls.

### 3. Research each domain from public Learn (parallel)
Dispatch **one background subagent per domain**. Each pulls facts + real source URLs from public
Microsoft Learn (via the MCP tools) into `content/learn_src_dN.md`, organized by objective id, with a
`Sources:` URL list per objective and short representative code snippets where relevant. Instruct them:
**public Learn only, no decks, cite real URLs you actually retrieved.**

### 4. Original diagram library
Adapt `guides/<EXAM>/make_diagrams.py` (reuse its `svg/box/arrow/chip/txt` primitives + palette) to
generate an original inline-SVG set covering this exam's key concepts. It writes each SVG to
`assets/diagrams/<id>.svg` and a `content/diagram_catalog.md` (`id → concept`). Run it.

### 5. Author domain content (parallel)
Dispatch **one background subagent per domain**. Each authors `content/domainN.html` from **its
`learn_src_dN.md` only**, following `template/TEMPLATE.md`. Per objective, in order:
1. **Concept** (`div.concept`) — what/why/how, own words
2. **Key facts** (`div.facts`) — testable specifics
3. **Diagram** where it helps — `<figure class="diagram" data-svg="ID"><figcaption>…</figcaption></figure>` (ids from the catalog only; build injects the SVG)
4. **Code** where relevant — `<pre><code class="lang-…">` (HTML-escape `<`,`>`,`&`); original, minimal, correct. Languages: sql, kql, dax, python, m, json, powershell, bash, csharp, javascript, typescript, yaml, bicep. Any other `lang-<x>` still gets generic highlighting; enrich one by adding it to `engine/languages.json` (never edit engine code)
5. **Callouts** — `div.callout key|tip|warn`
6. **Exam tips & gotchas** (`div.tips`)
7. **Practice** (`div.practice`) — 2–4 original `<details class="q">` reveal-answer questions with rationale
8. **Learn more** (`div.learn-more`) — REQUIRED; the real learn.microsoft.com URLs for that objective

### 6. Front matter + appendices
- `content/frontmatter.html`: cover, "how to use", exam facts, blueprint/weighting table, and a
  **Disclaimer & attribution** block (independent, unofficial, **not affiliated with or endorsed by
  Microsoft**; product names are trademarks used nominatively; content original + Learn-grounded;
  objective titles quote the public blueprint; no warranty). Reuse the DP-600 wording.
- `content/appendices.html`: decision tables, cheat-sheets, a "which one when?" rapid-fire, glossary.

### 7. Build + publish the site
```powershell
python engine\build_public.py guides\<EXAM>   # -> docs\<EXAM>.html  (must print CLEAN-ROOM: PASS)
python engine\build_index.py                  # -> docs\guides.json  (catalog picks up the new guide)
```
Or `python engine\build_all.py` to rebuild everything. Fix and rebuild until CLEAN-ROOM: PASS and `missing=[]`.

### 8. QA, then commit
- Coverage: build prints `objectives=` — confirm it matches the blueprint's objective count.
- Render `docs\index.html` **via a local web server** (JS `fetch('guides.json')` needs http, not file://):
  `python -m http.server` in `docs/`, open `http://localhost:8000/`, confirm the new card renders and its
  link opens the guide, with **0 console errors**. Also screenshot the guide itself.
- Commit + push. Pages redeploys automatically; the new card appears on the landing page.

---

## FLOW B — Refresh an EXISTING guide (full re-check)
1. **Re-fetch** the Skills Measured page for `<EXAM>` → **diff** against the current
   `guides/<EXAM>/config.json` + `TEMPLATE_PUBLIC.md` outline: note **added / renamed / retired**
   objectives and any **weight** changes.
2. **Re-pull** public Learn (MCP tools) for changed objectives → update the relevant
   `content/learn_src_dN.md`.
3. **Re-author** only what changed in `content/domainN.html`: add new objectives, update changed ones,
   remove retired ones (keep ids stable where the objective is unchanged). Regenerate diagrams if a
   concept shifted. Keep everything clean-room + original.
4. Update `config.json`: refreshed `weights`/`title`/`description` if they changed, and set
   `last_refreshed` to today.
5. **Rebuild**: `python engine\build_public.py guides\<EXAM>` then `python engine\build_index.py`
   (or `build_all.py`).
6. **QA** as in Flow A step 8, then commit + push.

Both flows END by regenerating `docs/guides.json`, so the landing catalog stays in sync automatically.

---

## Environment notes (this machine)
- Windows; backslash paths. CDN access is blocked → the engine **inlines all CSS/JS/SVG** so guides are
  fully offline. Never add a CDN `<script src>`/`<link href>`. (The landing page's `fetch` is same-origin
  and works on Pages / a local server.)
- PowerShell: fresh process per call; `&&` only chains native commands; no heredocs (pipe a
  single-quoted here-string to `python -`). Python 3 standard library only.
- Preferred models: use a strong model (Opus/GPT-5-class) for the most technically nuanced domain; a
  fast Sonnet-class model is fine for the rest and for research.
- Track the pipeline as todos; run the two parallel phases (research, then authoring) as background
  subagents; assemble/QA sequentially.

## Reference implementation
`guides/DP-600/` is a complete guide built exactly this way — copy it as the starting point; only the
blueprint (`config.json` + `TEMPLATE_PUBLIC.md` outline), research packs, diagrams, and content change per exam.
