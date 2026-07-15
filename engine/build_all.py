"""Full-site rebuild: build every guide in guides/ -> docs/, then regenerate the catalog manifest.

For each guide this builds the study guide (build_public.py) AND, when the guide ships an
authored question bank (a questions/ directory), the practice-exam simulator bank
(build_quiz.py -> docs/quiz/<EXAM>.json). It finishes by regenerating docs/guides.json so the
guide catalog and the practice-exam catalog (docs/quiz/exams.json) both stay in sync.

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
quizzes = 0
for gd in guide_dirs:
    name = os.path.basename(gd)
    print(f"\n=== Building {name} ===")
    r = subprocess.run([PY, os.path.join(ENGINE, "build_public.py"), gd])
    if r.returncode != 0:
        failed.append(name)

    # Rebuild the practice-exam bank whenever this guide ships authored questions,
    # so the test simulator never drifts from the guide it belongs to.
    if os.path.isdir(os.path.join(gd, "questions")):
        print(f"--- Practice exam: {name} ---")
        q = subprocess.run([PY, os.path.join(ENGINE, "build_quiz.py"), gd])
        if q.returncode != 0:
            failed.append(f"{name} (quiz)")
        else:
            quizzes += 1

print("\n=== Regenerating catalog manifest ===")
subprocess.run([PY, os.path.join(ENGINE, "build_index.py")])

if failed:
    sys.exit(f"\n!! build failed for: {', '.join(failed)}")
print(f"\nAll {len(guide_dirs)} guide(s) built ({quizzes} practice exam bank(s)) + manifest regenerated -> docs/")
