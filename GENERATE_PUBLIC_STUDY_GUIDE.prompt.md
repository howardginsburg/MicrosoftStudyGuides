# Generate or Refresh a Public Certification Study Guide

This repo (**MicrosoftStudyGuides**) hosts community-built, clean-room study guides for Microsoft
certification exams and publishes them as a GitHub Pages site. Each guide ships with a matching
**practice-exam simulator** (a clean-room question bank served by `docs/exam.html`). This prompt
drives two workflows:

- **Create** a new guide for an exam number, or
- **Refresh** an existing guide against the latest Skills Measured blueprint + Microsoft Learn docs.

The guide and its practice-exam bank are **one deliverable** — whenever you create or refresh a guide
you author/refresh its question bank in the **same** pass and rebuild both, so the simulator never
drifts from the guide it belongs to.

**How to run:** open the repo with an AI coding agent and say either
*"Use GENERATE_PUBLIC_STUDY_GUIDE to **create** a guide for exam `DP-700`"* or
*"Use GENERATE_PUBLIC_STUDY_GUIDE to **refresh** `DP-600`"*.
If no exam number is given, **ask for it first** (ask_user), and confirm create-vs-refresh.

---

## Repo layout you operate on
```
guides/<EXAM>/            SOURCE for one guide (not served directly)
  config.json             exam metadata + catalog fields + fragment order + passing_note (for the quiz)
  make_diagrams.py        generates this exam's original inline-SVG library
  content/                frontmatter.html, domain1..N.html, appendices.html,
                          learn_src_dN.md (research), TEMPLATE_PUBLIC.md, diagram_catalog.md
  questions/              practice-exam bank for THIS exam (drives the simulator)
    domainN.json          authored questions for domain N (one file per domain)
    scenarios.json        optional shared case-study stems referenced by a question's scenario_id
  assets/diagrams/*.svg   original SVGs
engine/                   reusable, exam-agnostic build tooling (do not special-case an exam here)
  build_public.py         one guide  -> docs/<EXAM>.html   (self-contained; inlines CSS/JS/SVG)
  build_quiz.py           one guide's questions/ -> docs/quiz/<EXAM>.json + rebuilds docs/quiz/exams.json
  build_index.py          all configs -> docs/guides.json  (catalog manifest)
  build_all.py            build every guide + its quiz bank + regenerate the manifest
  languages.json          shared syntax-highlighting language pack (add a language here, not in code)
  assets/                 shared UI (screen.css, print.css, app.js) inlined into every guide
template/                 config.example.json, TEMPLATE.md (authoring contract)
docs/                     PUBLISHED Pages site (flat files) -> committed
  index.html              static landing page; JS fetches guides.json + quiz/exams.json, renders cards
                          with an "Open guide" link and a "Practice exam" link (exam.html?exam=<EXAM>)
  exam.html               standalone practice-exam simulator (fetches quiz/exams.json + quiz/<EXAM>.json)
  guides.json             generated guide catalog manifest
  quiz/exams.json         generated practice-exam catalog manifest
  quiz/<EXAM>.json         each built question bank
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
  All practice questions — both the in-guide reveal-answer questions and the simulator's question
  bank — must be original scenarios you write, grounded in public Learn behavior.
- **Author all diagrams as original inline SVG** in your own visual style. Never embed Microsoft
  images, slide renders, or third-party graphics.
- Every external link in the output must resolve to `learn.microsoft.com` (the build fails otherwise).

---

## FLOW A — Create a NEW guide

### 1. Scaffold
Copy `guides/DP-600` → `guides/<EXAM>` as the skeleton, then clear DP-600-specific content (you will
replace `config.json`, `content/*.html`, `make_diagrams.py`, `assets/diagrams/*`, and the
`questions/*.json` bank). Keep the engine and `template/` untouched.

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

### 7. Author the practice-exam bank
The simulator reads one JSON file per domain from `guides/<EXAM>/questions/`. Author them from the
**same clean-room research** (`learn_src_dN.md`) as the guide — original scenarios only.
- Add `passing_note` to `config.json` (e.g. *"<EXAM> passes at 700/1000. Microsoft does not publish
  the raw-score mapping, so the readiness estimate is unofficial and based on percent correct only."*).
- Create `questions/domainN.json` for each domain: `{ "domain": N, "domain_title": "…", "questions": […] }`.
  Roughly mirror the blueprint weighting (more questions for heavier domains). Each question:
  - `id` (unique across the exam, e.g. `q1-001`), `objective` (e.g. `1.2.3`), `type`
    (`single` | `multi` | `tf`).
  - `stem` (HTML ok), `options` (`[{ "id": "a", "text": "…" }, …]`; omit for `tf` — True/False is
    auto-injected), `answer` (a single option id for `single`/`tf`; a **non-empty list** of ids for
    `multi`), `explanation` (why the key is right / distractors wrong), and `refs` (real
    learn.microsoft.com URLs — the build fails on any other host).
  - Optional `scenario_id` referencing a shared stem in `questions/scenarios.json`
    (`{ "scenarios": [{ "id": "s-x", "text": "…" }] }`) for case-study style question sets.
- Keep the same clean-room rules: no decks, no raster/base64 images in any text, links -> learn only.

### 8. Build + publish the site
```powershell
python engine\build_all.py                    # builds every guide + every quiz bank + manifest
```
Or build just this exam:
```powershell
python engine\build_public.py guides\<EXAM>   # -> docs\<EXAM>.html   (must print CLEAN-ROOM: PASS)
python engine\build_quiz.py   guides\<EXAM>   # -> docs\quiz\<EXAM>.json + docs\quiz\exams.json (CLEAN-ROOM: PASS)
python engine\build_index.py                  # -> docs\guides.json  (catalog picks up the new guide)
```
Fix and rebuild until both builds print CLEAN-ROOM: PASS and the guide build shows `missing=[]`.

### 9. QA, then commit
- Coverage: `build_public.py` prints `objectives=` — confirm it matches the blueprint's objective
  count; `build_quiz.py` prints per-domain and per-type question counts — confirm they look sane.
- Render `docs\index.html` **via a local web server** (JS `fetch` needs http, not file://):
  `python -m http.server` in `docs/`, open `http://localhost:8000/`, confirm the new card renders with
  **both** an "Open guide" and a "Practice exam" link, and that each opens correctly with **0 console
  errors**. The practice-exam link is deep-linked (`exam.html?exam=<EXAM>`) — verify it lands on the
  right exam pre-selected. Run a few questions to confirm scoring + the per-domain readiness report.
- Commit + push. Pages redeploys automatically; the new card + its practice exam appear on the site.

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
4. **Re-author the practice-exam bank to match.** In `guides/<EXAM>/questions/`: add questions for new
   objectives, fix ones whose facts changed, and remove questions tied to retired objectives. If the
   domain weighting shifted, rebalance question counts to roughly track it. Keep `refs` on
   learn.microsoft.com and every scenario/stem original.
5. Update `config.json`: refreshed `weights`/`title`/`description`/`passing_note` if they changed, and
   set `last_refreshed` to today.
6. **Rebuild both:** `python engine\build_all.py` (rebuilds every guide **and** every quiz bank), or for
   just this exam run `build_public.py`, `build_quiz.py`, then `build_index.py`.
7. **QA** as in Flow A step 9 (guide **and** practice-exam link), then commit + push.

Both flows END by regenerating `docs/guides.json` (guide catalog) and `docs/quiz/exams.json` (practice-exam
catalog), so the landing page and the simulator stay in sync automatically.

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
blueprint (`config.json` + `TEMPLATE_PUBLIC.md` outline), research packs, diagrams, content, and the
`questions/` bank change per exam. `guides/DP-420/` and `guides/AI-103/` are further examples of a
guide plus its practice-exam bank.
