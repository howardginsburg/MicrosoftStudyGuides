# Microsoft Certification Study Guides

Community-built, **clean-room** study guides for Microsoft certification exams — each grounded only in
public **Microsoft Learn** documentation, with original writing, original SVG diagrams, and original
practice questions. Guides are published as a static **GitHub Pages** site.

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

## How it works

```
guides/<EXAM>/     SOURCE for each guide (config + content fragments + diagrams + research packs)
engine/            reusable, exam-agnostic build tooling
  build_public.py    one guide   -> docs/<EXAM>.html   (inlines CSS/JS/SVG; runs a clean-room guard)
  build_index.py     all configs -> docs/guides.json   (catalog manifest)
  build_all.py       build every guide + regenerate the manifest
template/          starting points for a new exam (config.example.json, TEMPLATE.md authoring contract)
docs/              PUBLISHED site (committed, served by Pages)
  index.html         landing page; JS fetches guides.json and renders the guide cards
  guides.json        generated catalog manifest
  <EXAM>.html        each built guide
```

The published site is **flat files** in `/docs`. The landing page can't list a directory on Pages, so
the build emits a `guides.json` manifest that `index.html` reads client-side — add or refresh a guide
and the catalog updates itself.

---

## Generate or refresh a guide (agentic)

Everything is driven by **`GENERATE_PUBLIC_STUDY_GUIDE.prompt.md`**. Open the repo with an AI coding
agent and ask it to either flow:

**Create a new guide**
> Use GENERATE_PUBLIC_STUDY_GUIDE to **create** a guide for exam `DP-700`

The agent scaffolds `guides/DP-700/`, fetches the official Skills Measured blueprint, researches public
Microsoft Learn (parallel sub-agents), authors original content + diagrams + practice questions, builds
`docs/DP-700.html`, and regenerates `docs/guides.json`.

**Refresh an existing guide** (full re-check)
> Use GENERATE_PUBLIC_STUDY_GUIDE to **refresh** `DP-600`

The agent re-fetches the blueprint, diffs the outline, re-pulls Learn for changed objectives, re-authors
what changed, bumps `last_refreshed`, and rebuilds.

Both flows end by regenerating the manifest, then you commit + push and Pages redeploys.

---

## Build it yourself

Plain Python 3 (standard library only — no third-party packages):

```powershell
python engine\build_all.py                 # build every guide + manifest -> docs\
python engine\build_public.py guides\DP-600  # build just one guide -> docs\DP-600.html
python guides\DP-600\make_diagrams.py        # regenerate a guide's SVG diagrams

# preview the landing page (fetch() needs http, not file://):
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
