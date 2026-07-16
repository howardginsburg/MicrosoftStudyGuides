"""Assemble a PUBLIC (clean-room) practice-exam question bank -> docs/quiz/<EXAM>.json + catalog.

Exam-agnostic quiz build engine. Everything specific to one exam lives in its GUIDE directory:
    <guide>/config.json              exam metadata + blueprint weights (shared with the study guide)
    <guide>/questions/domainN.json   authored question banks, one file per domain
    <guide>/questions/scenarios.json optional shared case-study stems referenced by scenario_id

The standalone app (docs/exam.html) fetches docs/quiz/exams.json (catalog) and then the selected
docs/quiz/<EXAM>.json bank, so output stays fully self-contained (offline, no CDN).

Usage:
    python engine/build_quiz.py <guide-dir>
    python engine/build_quiz.py guides/DP-420

Clean-room rules enforced here (mirrors engine/build_public.py):
  * Reads ONLY from the guide dir. No decks / slide renders / .pptx.
  * Any hyperlink in a stem, option, explanation or ref must resolve to learn.microsoft.com only.
  * No raster/base64 images anywhere in question text.
"""
import os, re, sys, json, glob, datetime

ENGINE = os.path.dirname(os.path.abspath(__file__))
REPO   = os.path.dirname(ENGINE)
DOCS   = os.path.join(REPO, "docs")
QUIZ   = os.path.join(DOCS, "quiz")

GUIDE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
CFG_PATH = os.path.join(GUIDE, "config.json")
if not os.path.exists(CFG_PATH):
    sys.exit(f"!! No config.json found in guide dir: {GUIDE}\n   Pass the guide directory, e.g. python engine/build_quiz.py guides/DP-420")
cfg = json.load(open(CFG_PATH, encoding="utf-8"))

EXAM      = cfg.get("exam", "EXAM")
TITLE     = cfg.get("title", EXAM)
WEIGHTS   = cfg.get("weights", {})
guide_html = cfg.get("output_html", f"{EXAM}.html")
QDIR      = os.path.join(GUIDE, "questions")
CONTENT   = os.path.join(GUIDE, "content")
os.makedirs(QUIZ, exist_ok=True)

VALID_TYPES = {"single", "multi", "tf"}

# ---------------- Clean-room guard ----------------
def _bad_host(url):
    host = re.sub(r'^https?://', '', url).split('/')[0].lower()
    return not (host == "learn.microsoft.com" or host.endswith(".learn.microsoft.com"))

def clean_room_text(label, t, problems):
    """Scan an authored HTML text field (stem/option/explanation).

    Mirrors engine/build_public.py: only actual hyperlinks (href="...") must resolve to
    learn.microsoft.com. Illustrative URLs in prose/code (e.g. the emulator endpoint
    https://localhost:8081/ or example CORS origins) are allowed, exactly as they are in the
    study guide body. Raster images and deck/slide references are always rejected.
    """
    if not isinstance(t, str):
        return
    if re.search(r'data:image/(png|jpe?g)', t):
        problems.append(f"{label}: raster data-image (png/jpeg)")
    if re.search(r'slides/|deck\d\d_s\d\d|\.pptx', t):
        problems.append(f"{label}: deck/slide path reference")
    for url in re.findall(r'href="(https?://[^"]+)"', t):
        if _bad_host(url):
            problems.append(f"{label}: external link not on learn.microsoft.com: {url}")

def clean_room_ref(label, url, problems):
    """A citation (refs[]) is a bare URL and must resolve to learn.microsoft.com."""
    if not isinstance(url, str):
        problems.append(f"{label}: ref must be a string"); return
    if _bad_host(url):
        problems.append(f"{label}: ref not on learn.microsoft.com: {url}")

# ---------------- Load shared scenarios ----------------
scenarios = {}
scen_path = os.path.join(QDIR, "scenarios.json")
if os.path.exists(scen_path):
    sdata = json.load(open(scen_path, encoding="utf-8"))
    for s in sdata.get("scenarios", []):
        scenarios[s["id"]] = s["text"]

# ---------------- Load authored objective anchors ----------------
objective_anchors = None
if os.path.isdir(CONTENT):
    objective_anchors = set()
    for cpath in glob.glob(os.path.join(CONTENT, "*.html")):
        with open(cpath, encoding="utf-8") as f:
            objective_anchors.update(re.findall(r'id="(obj-[0-9a-z-]+)"', f.read()))

# ---------------- Load + validate per-domain banks ----------------
problems = []
seen_ids = set()
all_questions = []
domain_meta = []
objective_links = 0
unmatched_objectives = 0

domain_files = sorted(glob.glob(os.path.join(QDIR, "domain*.json")))
if not domain_files:
    sys.exit(f"!! No question files found in {QDIR} (expected domain*.json)")

for path in domain_files:
    data = json.load(open(path, encoding="utf-8"))
    dnum = data.get("domain")
    dtitle = data.get("domain_title", "")
    qs = data.get("questions", [])
    for q in qs:
        qid = q.get("id", "")
        loc = f"{os.path.basename(path)}:{qid}"
        if not qid:
            problems.append(f"{loc}: missing id"); continue
        if qid in seen_ids:
            problems.append(f"{loc}: duplicate id"); 
        seen_ids.add(qid)

        qtype = q.get("type")
        if qtype not in VALID_TYPES:
            problems.append(f"{loc}: invalid type '{qtype}'")

        # Normalize true/false into explicit options for uniform rendering.
        if qtype == "tf" and not q.get("options"):
            q["options"] = [{"id": "true", "text": "True"}, {"id": "false", "text": "False"}]

        opts = q.get("options", [])
        opt_ids = [o.get("id") for o in opts]
        if len(opt_ids) != len(set(opt_ids)):
            problems.append(f"{loc}: duplicate option ids")
        if qtype in ("single",) and len(opts) < 2:
            problems.append(f"{loc}: single-choice needs >=2 options")

        ans = q.get("answer")
        if qtype == "multi":
            if not isinstance(ans, list) or not ans:
                problems.append(f"{loc}: multi answer must be a non-empty list")
            else:
                for a in ans:
                    if a not in opt_ids:
                        problems.append(f"{loc}: answer id '{a}' not in options")
        else:
            if not isinstance(ans, str):
                problems.append(f"{loc}: {qtype} answer must be a single id string")
            elif ans not in opt_ids:
                problems.append(f"{loc}: answer id '{ans}' not in options")

        if not q.get("stem"):
            problems.append(f"{loc}: missing stem")
        if not q.get("explanation"):
            problems.append(f"{loc}: missing explanation")

        sid = q.get("scenario_id")
        if sid and sid not in scenarios:
            problems.append(f"{loc}: unknown scenario_id '{sid}'")

        # Clean-room scan across all text fields.
        clean_room_text(loc + " stem", q.get("stem", ""), problems)
        clean_room_text(loc + " explanation", q.get("explanation", ""), problems)
        for o in opts:
            clean_room_text(loc + " option", o.get("text", ""), problems)
        for r in q.get("refs", []):
            clean_room_ref(loc + " ref", r, problems)

        q.pop("objective_anchor", None)
        q.pop("objective_href", None)
        objective = q.get("objective")
        if isinstance(objective, str) and objective.strip():
            code = objective.strip()
            anchor = "obj-" + code.replace(".", "-")
            if objective_anchors is not None and anchor not in objective_anchors:
                print(f"!! {loc}: objective '{code}' -> #{anchor} has no matching guide section")
                unmatched_objectives += 1
            else:
                q["objective_anchor"] = anchor
                q["objective_href"] = f"{guide_html}#{anchor}"
                objective_links += 1

        q["domain"] = dnum
        q["domain_title"] = dtitle
        all_questions.append(q)

    domain_meta.append({"domain": dnum, "title": dtitle, "count": len(qs)})

# scenario text clean-room
for sid, text in scenarios.items():
    clean_room_text(f"scenario:{sid}", text, problems)

domain_meta.sort(key=lambda d: (d["domain"] is None, d["domain"]))

# ---------------- Write bank + catalog ----------------
bank = {
    "exam": EXAM,
    "title": TITLE,
    "generated": datetime.date.today().isoformat(),
    "weights": WEIGHTS,
    "passing_note": cfg.get("passing_note",
        "DP-420 passes at 700/1000. Microsoft does not publish the raw-score mapping, so the "
        "readiness estimate below is unofficial and based on percent correct only."),
    "readiness_bands": [
        {"min": 75, "label": "Ready", "note": "Consistently strong — you're tracking well above the pass line."},
        {"min": 60, "label": "Approaching", "note": "Close — shore up weaker domains before test day."},
        {"min": 0,  "label": "Not ready yet", "note": "Keep studying — focus on your lowest-scoring domains."}
    ],
    "scenarios": scenarios,
    "domains": domain_meta,
    "questions": all_questions,
}
bank_path = os.path.join(QUIZ, f"{EXAM}.json")
json.dump(bank, open(bank_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# Rebuild the catalog from every bank already in docs/quiz.
exams = []
for bp in sorted(glob.glob(os.path.join(QUIZ, "*.json"))):
    if os.path.basename(bp) == "exams.json":
        continue
    try:
        b = json.load(open(bp, encoding="utf-8"))
    except Exception as e:
        print(f"!! skipping {bp}: {e}"); continue
    exams.append({
        "exam":    b.get("exam", ""),
        "title":   b.get("title", ""),
        "file":    os.path.basename(bp),
        "total":   len(b.get("questions", [])),
        "domains": b.get("domains", []),
    })
exams.sort(key=lambda e: e["exam"])
catalog = {"generated": datetime.date.today().isoformat(), "count": len(exams), "exams": exams}
json.dump(catalog, open(os.path.join(QUIZ, "exams.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# ---------------- Report ----------------
by_type = {}
for q in all_questions:
    by_type[q.get("type")] = by_type.get(q.get("type"), 0) + 1
print(f"Exam: {EXAM}")
print("Bank    ->", bank_path)
print("Catalog ->", os.path.join(QUIZ, "exams.json"))
print(f"questions={len(all_questions)}  scenarios={len(scenarios)}")
print(f"objective_links={objective_links}  unmatched={unmatched_objectives}")
print("by domain:", "  ".join(f"D{d['domain']}={d['count']}" for d in domain_meta))
print("by type:  ", "  ".join(f"{k}={v}" for k, v in sorted(by_type.items())))
print("CLEAN-ROOM:", "PASS - links -> learn.microsoft.com, no raster/deck refs" if not problems
      else "FAIL ->\n  " + "\n  ".join(problems))
if problems:
    sys.exit(1)
