"""Full-site rebuild: build every guide in guides/ -> docs/, then regenerate the catalog manifest.

Usage:
    python engine/build_all.py
"""
import os, sys, glob, subprocess

ENGINE = os.path.dirname(os.path.abspath(__file__))
REPO   = os.path.dirname(ENGINE)
GUIDES = os.path.join(REPO, "guides")
PY     = sys.executable

guide_dirs = sorted(d for d in glob.glob(os.path.join(GUIDES, "*")) if os.path.exists(os.path.join(d, "config.json")))
if not guide_dirs:
    sys.exit("!! No guides found under guides/*/config.json")

failed = []
for gd in guide_dirs:
    name = os.path.basename(gd)
    print(f"\n=== Building {name} ===")
    r = subprocess.run([PY, os.path.join(ENGINE, "build_public.py"), gd])
    if r.returncode != 0:
        failed.append(name)

print("\n=== Regenerating catalog manifest ===")
subprocess.run([PY, os.path.join(ENGINE, "build_index.py")])

if failed:
    sys.exit(f"\n!! build failed for: {', '.join(failed)}")
print(f"\nAll {len(guide_dirs)} guide(s) built + manifest regenerated -> docs/")
