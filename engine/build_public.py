"""Assemble a PUBLIC (clean-room) certification study guide -> interactive HTML + print HTML.

Exam-agnostic build engine. Everything specific to one exam lives in a GUIDE directory:
    <guide>/config.json          exam metadata + fragment order (see template/config.example.json)
    <guide>/content/*.html       authored fragments (frontmatter, domainN, appendices)
    <guide>/assets/diagrams/*.svg original inline-SVG diagrams referenced by data-svg="ID"
Shared UI (screen.css / print.css / app.js) is read from engine/assets and inlined,
so the output HTML is fully self-contained (offline, no CDN).

Usage:
    python engine/build_public.py <guide-dir>
    python engine/build_public.py examples/DP-600

Clean-room rules enforced here:
  * Reads ONLY from the guide dir + engine assets. No decks / slide renders / .pptx.
  * Diagrams are ORIGINAL inline SVG injected from <guide>/assets/diagrams/<id>.svg
    via <figure class="diagram" data-svg="ID">. No raster images, no base64 PNG.
"""
import os, re, sys, json, html

ENGINE = os.path.dirname(os.path.abspath(__file__))
SHARED_ASSETS = os.path.join(ENGINE, "assets")
REPO   = os.path.dirname(ENGINE)              # repo root (parent of engine/)
DOCS   = os.path.join(REPO, "docs")           # published Pages site (flat files)

GUIDE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
CFG_PATH = os.path.join(GUIDE, "config.json")
if not os.path.exists(CFG_PATH):
    sys.exit(f"!! No config.json found in guide dir: {GUIDE}\n   Pass the guide directory, e.g. python engine/build_public.py guides/DP-600")
cfg = json.load(open(CFG_PATH, encoding="utf-8"))

EXAM      = cfg.get("exam", "EXAM")
DOC_TITLE = cfg.get("doc_title", f"{EXAM} Study Guide (Community Edition)")
BRAND     = cfg.get("brand", EXAM)
BRAND_SUB = cfg.get("brand_sub", "Study Guide")
FRAGMENTS = cfg.get("fragments", ["frontmatter.html", "appendices.html"])
OUT_HTML  = cfg.get("output_html", f"{EXAM}.html")

# Built HTML is published ONLY to /docs (flat filenames). Source stays in the guide dir.
OUTDIR = DOCS
CONTENT  = os.path.join(GUIDE, "content")
DIAGRAMS = os.path.join(GUIDE, "assets", "diagrams")
DIST     = os.path.join(GUIDE, "dist")
os.makedirs(DIST, exist_ok=True)
os.makedirs(OUTDIR, exist_ok=True)

# ---------------- Syntax highlighting (build-time, data-driven) ----------------
# Language definitions live in engine/languages.json (shared, exam-agnostic). Add a language
# there, never here. Every field is optional; a language with no "keywords" still gets strings,
# numbers, comments, and function-call highlighting. Unknown languages use a generic C-style profile.
LANG_PATH = os.path.join(ENGINE, "languages.json")
LANGS = {}
if os.path.exists(LANG_PATH):
    LANGS = {k: v for k, v in json.load(open(LANG_PATH, encoding="utf-8")).items() if not k.startswith("_")}

DEFAULT_LANG = {"case_insensitive": False, "line_comment": ["//", "#"], "block_comment": True,
                "quotes": ["\"", "'"], "keywords": []}

def build_pattern(cfg):
    line  = cfg.get("line_comment", [])
    block = cfg.get("block_comment", False)
    quotes = cfg.get("quotes", ["\""])
    alts, com = [], []
    if block: com.append(r"/\*[\s\S]*?\*/")
    for lc in line: com.append(re.escape(lc)+r"[^\n]*")
    if com: alts.append("(?P<com>"+"|".join(com)+")")
    if quotes:
        strs = [q + r"(?:\\.|[^" + re.escape(q) + r"\\])*" + q for q in quotes]
        alts.append("(?P<str>"+"|".join(strs)+")")
    alts.append(r"(?P<num>\b\d+\.?\d*\b)")
    alts.append(r"(?P<word>[A-Za-z_][A-Za-z0-9_]*)")
    return re.compile("|".join(alts))

PATTERNS = {name: build_pattern(cfg) for name, cfg in LANGS.items()}
DEFAULT_PATTERN = build_pattern(DEFAULT_LANG)

def highlight(raw_escaped, lang):
    cfg = LANGS.get(lang, DEFAULT_LANG)
    pattern = PATTERNS.get(lang, DEFAULT_PATTERN)
    ci = cfg.get("case_insensitive", False)
    kw_list = cfg.get("keywords", []) or []
    kws = set(k.upper() for k in kw_list) if ci else set(kw_list)
    text = html.unescape(raw_escaped)
    out, last = [], 0
    for m in pattern.finditer(text):
        if m.start() > last: out.append(html.escape(text[last:m.start()]))
        kind, val = m.lastgroup, m.group()
        if kind == "com":   out.append('<span class="tok-com">'+html.escape(val)+'</span>')
        elif kind == "str": out.append('<span class="tok-str">'+html.escape(val)+'</span>')
        elif kind == "num": out.append('<span class="tok-num">'+html.escape(val)+'</span>')
        else:
            key = val.upper() if ci else val
            if kws and key in kws: out.append('<span class="tok-kw">'+html.escape(val)+'</span>')
            elif text[m.end():m.end()+1] == "(": out.append('<span class="tok-fn">'+html.escape(val)+'</span>')
            else: out.append(html.escape(val))
        last = m.end()
    if last < len(text): out.append(html.escape(text[last:]))
    return "".join(out)

CODE_RE = re.compile(r'(<code class="lang-([a-z0-9]+)">)(.*?)(</code>)', re.S)
def apply_highlighting(t):
    return CODE_RE.sub(lambda m: m.group(1)+highlight(m.group(3), m.group(2))+m.group(4), t)

# ---------------- Inject original inline SVG diagrams ----------------
SVG_RE = re.compile(r'<figure class="diagram" data-svg="([^"]+)">')
missing, injected = [], []
def inject_svgs(t):
    def repl(m):
        did = m.group(1)
        p = os.path.join(DIAGRAMS, did + ".svg")
        if not os.path.exists(p):
            missing.append(did)
            return '<figure class="diagram"><div class="callout warn"><b>[diagram missing: '+html.escape(did)+']</b></div>'
        svg = open(p, encoding="utf-8").read().strip()
        injected.append(did)
        return '<figure class="diagram">\n' + svg + '\n'
    return SVG_RE.sub(repl, t)

# ---------------- Clean-room guard ----------------
def clean_room_check(t):
    problems = []
    if re.search(r'data-img=', t): problems.append("found deck-style data-img reference")
    if re.search(r'data:image/(png|jpe?g)', t): problems.append("found raster data-image (png/jpeg)")
    if re.search(r'slides/|deck\d\d_s\d\d|\.pptx', t): problems.append("found deck/slide path reference")
    # external links must resolve to learn.microsoft.com only
    for url in re.findall(r'href="(https?://[^"]+)"', t):
        host = re.sub(r'^https?://', '', url).split('/')[0].lower()
        if not (host == "learn.microsoft.com" or host.endswith(".learn.microsoft.com")):
            problems.append(f"external link not on learn.microsoft.com: {url}")
    return problems

# ---------------- Assemble ----------------
def read(p): return open(p, encoding="utf-8").read()

frags = []
for f in FRAGMENTS:
    p = os.path.join(CONTENT, f)
    if not os.path.exists(p):
        print("!! MISSING FRAGMENT:", f); continue
    frags.append(read(p))
body = "\n".join(frags)
body = apply_highlighting(body)
body = inject_svgs(body)

problems = clean_room_check(body)

screen_css = read(os.path.join(SHARED_ASSETS,"screen.css"))
print_css  = read(os.path.join(SHARED_ASSETS,"print.css"))
app_js     = read(os.path.join(SHARED_ASSETS,"app.js"))

INTERACTIVE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>%s</style></head><body>
<header class="topbar">
  <button id="menu-btn" title="Menu">&#9776;</button>
  <div class="brand">%s<small>%s</small></div>
  <div class="spacer"></div>
  <input id="search" type="search" placeholder="Search the guide&hellip;" autocomplete="off">
  <span id="progress-indicator"></span>
  <button id="collapse-btn">Collapse all</button>
  <button id="theme-btn" title="Toggle light/dark">&#9681;</button>
  <button id="print-btn" title="Print / Save as PDF">Print</button>
</header>
<nav id="toc" class="sidebar"></nav>
<main><div class="wrap"><div id="content">%s</div><div id="noresults">No matches. Try another keyword.</div></div></main>
<script>%s</script></body></html>""" % (
    html.escape(DOC_TITLE), screen_css, html.escape(BRAND), html.escape(BRAND_SUB), body, app_js)

print_body = body.replace('<details class="q">', '<details class="q" open>')
PRINT = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>%s</title><style>%s</style></head><body>
<main><div class="wrap"><div id="content">%s</div></div></main></body></html>""" % (
    html.escape(DOC_TITLE), print_css, print_body)

out_html_path = os.path.join(OUTDIR, OUT_HTML)
open(out_html_path,"w",encoding="utf-8").write(INTERACTIVE)
open(os.path.join(DIST,"print.html"),"w",encoding="utf-8").write(PRINT)

n_obj = body.count('class="objective"')
n_q   = body.count('<details class="q"')
n_svg = body.count('<svg')
n_cite= body.count('class="learn-more"')
size_mb = round(len(INTERACTIVE.encode("utf-8"))/1024/1024, 2)
print(f"Exam: {EXAM}")
print("Interactive ->", out_html_path, f"({size_mb} MB)")
print("Print       ->", os.path.join(DIST,"print.html"))
print(f"objectives={n_obj}  practice_q={n_q}  inline_svg={n_svg}  learn_more_cites={n_cite}")
print(f"diagrams injected={len(set(injected))}  missing={sorted(set(missing))}")
print("CLEAN-ROOM:", "PASS - no deck/raster refs, links -> learn.microsoft.com" if not problems else "FAIL -> "+"; ".join(problems))
