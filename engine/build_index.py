"""Generate docs/guides.json — the catalog manifest the landing page reads.

Scans every guides/*/config.json and emits a flat JSON array describing each published guide.
The static docs/index.html fetches this file and renders the guide cards client-side, so the
catalog stays in sync automatically whenever a guide is built/refreshed.

Usage:
    python engine/build_index.py
"""
import os, sys, json, glob

ENGINE = os.path.dirname(os.path.abspath(__file__))
REPO   = os.path.dirname(ENGINE)
GUIDES = os.path.join(REPO, "guides")
DOCS   = os.path.join(REPO, "docs")
os.makedirs(DOCS, exist_ok=True)

entries = []
for cfg_path in sorted(glob.glob(os.path.join(GUIDES, "*", "config.json"))):
    try:
        cfg = json.load(open(cfg_path, encoding="utf-8"))
    except Exception as e:
        print(f"!! skipping {cfg_path}: {e}")
        continue
    exam = cfg.get("exam", "")
    out_html = cfg.get("output_html", f"{exam}.html")
    # Only list guides whose built HTML actually exists in /docs.
    if not os.path.exists(os.path.join(DOCS, out_html)):
        print(f"-- {exam}: {out_html} not built yet, listing anyway (status will show)")
    entries.append({
        "exam":          exam,
        "title":         cfg.get("title", ""),
        "description":   cfg.get("description", ""),
        "weights":       cfg.get("weights", {}),
        "official_url":  cfg.get("official_url", ""),
        "status":        cfg.get("status", "draft"),
        "last_refreshed":cfg.get("last_refreshed", ""),
        "file":          out_html,  # relative link, resolves under the Pages subpath
    })

# Sort by exam code for a stable catalog order.
entries.sort(key=lambda e: e["exam"])

manifest = {
    "generated": __import__("datetime").date.today().isoformat(),
    "count": len(entries),
    "guides": entries,
}
out = os.path.join(DOCS, "guides.json")
json.dump(manifest, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"Wrote {out}  ({len(entries)} guide(s): {', '.join(e['exam'] for e in entries) or 'none'})")
