# Microsoft Certification Study Guides

Community-built, **clean-room** study guides for Microsoft certification exams — each grounded only in
public **Microsoft Learn** documentation, with original writing, original SVG diagrams, and original
practice questions. Every guide ships with a matching **practice-exam simulator**. Guides are published
as a static **GitHub Pages** site.

**🔗 Live site:** https://howardginsburg.github.io/MicrosoftStudyGuides/

Because everything is original and Learn-grounded (no courseware, no exam dumps, no copied images),
the guides are safe to share.

---

## Available guides

The catalog is generated from each guide's `config.json` — browse the live site for the current list:

**👉 https://howardginsburg.github.io/MicrosoftStudyGuides/**

Each guide is a single self-contained interactive HTML file (sidebar TOC, per-objective progress
checkboxes, search, reveal-answer practice, copy-code buttons, light/dark toggle, Print button).

---

## Practice-exam simulator

Every guide that ships a question bank also gets a **practice exam** at
[`exam.html`](https://howardginsburg.github.io/MicrosoftStudyGuides/exam.html). From a guide card on the
landing page, the **"Practice exam"** link deep-links to that exam (`exam.html?exam=<EXAM>`). The
simulator lets you:

- pick **Exam mode** (timed, feedback at the end) or **Practice mode** (instant per-question feedback),
- choose how many questions and which domains to include, and randomize order,
- get a scored report with a **readiness estimate** and a **per-domain breakdown** vs the blueprint
  weighting, plus per-question review with explanations and Microsoft Learn references.

Question banks are original, clean-room, and Learn-grounded — like the guides, they contain no real exam
questions or courseware. Readiness bands are unofficial (based on percent correct only).

---

## What's new: objective links and appearance controls

The guide and practice-exam experiences now share a few quality-of-life improvements that make it easier
to move between assessment and study without changing the content model or scoring behavior:

- **Quiz objective deep-links.** In the practice-exam review screens, a question's objective now links
  directly to the matching objective section in the generated guide when the build can prove a matching
  anchor exists. Links open in a new tab (`target="_blank" rel="noopener"`) so an in-progress timed run is
  not replaced. If an objective cannot be matched, the simulator safely falls back to the same plain-text
  objective label it used before.
- **Shared theme and text-size controls.** The light/dark theme toggle is available on both the guide
  pages and the practice-exam page, and both surfaces now include **A-** / **A+** controls for text size.
  The controls use shared browser storage keys: `msg-theme` for the selected theme (`light` or `dark`)
  and `msg-textscale` for the text-size step (integer range `-2` through `+3`, default `0`). Older guide
  preferences stored under `dp600-theme` migrate once into `msg-theme`.

For authors and maintainers, objective links are generated at build time rather than hand-edited in the
published HTML. `engine/build_quiz.py` reads each guide's `config.json` to find the guide output file
(`output_html`) and derives each question's anchor from its objective code:

```text
objective code 2.2.3 -> objective_anchor obj-2-2-3 -> objective_href <EXAM>.html#obj-2-2-3
```

When a question has a matching objective anchor in the guide source content, the built quiz JSON includes
the derived `objective_anchor` and `objective_href` fields in `docs/quiz/<EXAM>.json`. The simulator
renders `objective_href` as the clickable target and otherwise renders the objective as plain text. The
validation is warn-only, so unmatched objectives are visible to maintainers without blocking the build.
Run `python engine\build_quiz.py guides\<EXAM>` to regenerate a single quiz bank or
`python engine\build_all.py` to regenerate every guide, quiz bank, and manifest; no manual edits to
`docs/<EXAM>.html` or `docs/quiz/<EXAM>.json` are required.

---

## How it works

```
guides/<EXAM>/     SOURCE for each guide (config + content fragments + diagrams + research + questions)
  questions/         practice-exam bank for the guide (one domainN.json per domain, optional scenarios.json)
engine/            reusable, exam-agnostic build tooling
  build_public.py    one guide     -> docs/<EXAM>.html      (inlines CSS/JS/SVG; runs a clean-room guard)
  build_quiz.py      one guide's questions -> docs/quiz/<EXAM>.json + docs/quiz/exams.json (clean-room guard)
  build_index.py     all configs   -> docs/guides.json      (guide catalog manifest)
  build_all.py       build every guide + every quiz bank + regenerate the manifest
template/          starting points for a new exam (config.example.json, TEMPLATE.md authoring contract)
docs/              PUBLISHED site (committed, served by Pages)
  index.html         landing page; JS fetches guides.json + quiz/exams.json and renders the guide cards
  exam.html          standalone practice-exam simulator (fetches quiz/exams.json + quiz/<EXAM>.json)
  guides.json        generated guide catalog manifest
  quiz/exams.json    generated practice-exam catalog manifest
  quiz/<EXAM>.json   each built question bank
  <EXAM>.html        each built guide
```

The published site is **flat files** in `/docs`. The landing page can't list a directory on Pages, so
the build emits a `guides.json` manifest (and a `quiz/exams.json` manifest for the practice exams) that
`index.html` reads client-side — add or refresh a guide and both catalogs update themselves.

---

## Generate or refresh a guide (agentic)

Everything is driven by **`GENERATE_PUBLIC_STUDY_GUIDE.prompt.md`**. Open the repo with an AI coding
agent and ask it to either flow:

**Create a new guide**
> Use GENERATE_PUBLIC_STUDY_GUIDE to **create** a guide for exam `DP-700`

The agent scaffolds `guides/DP-700/`, fetches the official Skills Measured blueprint, researches public
Microsoft Learn (parallel sub-agents), authors original content + diagrams + practice questions **and a
matching practice-exam bank**, builds `docs/DP-700.html` + `docs/quiz/DP-700.json`, and regenerates the
`docs/guides.json` and `docs/quiz/exams.json` manifests.

**Refresh an existing guide** (full re-check)
> Use GENERATE_PUBLIC_STUDY_GUIDE to **refresh** `DP-600`

The agent re-fetches the blueprint, diffs the outline, re-pulls Learn for changed objectives, re-authors
what changed **in both the guide and its question bank**, bumps `last_refreshed`, and rebuilds both.

Both flows end by regenerating the manifests, then you commit + push and Pages redeploys.

---

## Build it yourself

Plain Python 3 (standard library only — no third-party packages):

```powershell
python engine\build_all.py                 # build every guide + every quiz bank + manifests -> docs\
python engine\build_public.py guides\DP-600  # build just one guide -> docs\DP-600.html
python engine\build_quiz.py   guides\DP-600  # build just one practice-exam bank -> docs\quiz\DP-600.json
python guides\DP-600\make_diagrams.py        # regenerate a guide's SVG diagrams

# preview the landing page / practice exams (fetch() needs http, not file://):
cd docs; python -m http.server            # then open http://localhost:8000/
```

---

## GitHub Pages

Served from **`/docs` on the default branch** (Settings → Pages). Public repo, so it works on the Free
plan. Push to the default branch and the site redeploys automatically.

---

## Requirements

- **Python 3** (standard library only) to build.
- A modern browser to view the guides (fully offline / self-contained; no internet or CDN needed).
- For generating/refreshing guides: an AI coding agent with the **Microsoft Learn MCP tools**.

## License & disclaimer

Code and original content are released under the **MIT License** (see `LICENSE`).

These guides are independent, unofficial study aids. They are **not affiliated with, endorsed by, or
sponsored by Microsoft**. "Microsoft", "Power BI", "Fabric", and certification exam names are trademarks
of Microsoft, used nominatively. Content is original and grounded in public Microsoft Learn
documentation; objective titles quote the public Skills Measured blueprint. Provided as-is, without warranty.
