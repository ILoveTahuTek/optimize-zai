#!/usr/bin/env bash
# Smoke test for harness-template/scripts (synthetic data, throwaway dir /tmp/ppc-smoke)
set -euo pipefail
T=/home/z/my-project/harness-template/scripts
W=/tmp/ppc-smoke
rm -rf "$W" && mkdir -p "$W" && cd "$W"

echo "=== 0. synthetic data + fake library (for MIGRATE hint) ==="
printf 'date,region,product,amount\n2025-01-05,East,Widget,100\n2025-01-05,East,Widget,100\n2025-02-11,West,Gadget,-40\n' > mini.csv
mkdir -p fake-lab/library/data-report
printf '# Library — data-report\n' > fake-lab/library/data-report/INDEX.md

echo "=== 1. new_lab.py (with input + library hint) ==="
python3 "$T/new_lab.py" --domain data-report --task t-smoke \
  --input mini.csv --lab-root fake-lab
test -f fake-lab/data-report/tasks/t-smoke/input/mini.csv
test -f fake-lab/data-report/tasks/t-smoke/harnesses/base/INSTRUCTIONS.md

echo "=== 2. new_lab.py --adopt-from ==="
mkdir -p lib-harness && printf '# adopted harness\n' > lib-harness/INSTRUCTIONS.md
python3 "$T/new_lab.py" --domain data-report --task t-adopt \
  --input mini.csv --lab-root fake-lab --adopt-from lib-harness
test -f fake-lab/data-report/tasks/t-adopt/harnesses/base/ADOPTED.md

echo "=== 3. fake runs (one leaks its own label in text) ==="
R=fake-lab/data-report/tasks/t-smoke/runs
mkdir -p "$R/alpha" "$R/beta"
printf 'base report: total 60\nrun dir: %s/alpha\n' "$W/$R" > "$R/alpha/report.md"
printf 'cand report: total 60, verified twice\n' > "$R/beta/report.md"
python3 "$T/blind_reports.py" --runs "$R" \
  --out fake-lab/data-report/tasks/t-smoke/selection --seed 7 --scrub > blind.out
cat blind.out
! grep -qE 'alpha|beta' blind.out
python3 - <<'PY'
import json
k = json.load(open("fake-lab/data-report/tasks/t-smoke/selection/key.json"))
assert sorted(k) == ["RUN-A", "RUN-B"] and set(k["RUN-A"]) == {"harness", "source"}
texts = [open(f"fake-lab/data-report/tasks/t-smoke/selection/blind/{r}.report.md").read() for r in ("RUN-A","RUN-B")]
assert any("«scrubbed»" in t for t in texts), "scrub failed"
assert not any("/alpha" in t or "/beta" in t for t in texts), "label leaked"
print("blind_reports: key.json strict-JSON OK, scrub OK, stdout clean OK")
PY

echo "=== 4. score_audit.py ==="
A=fake-lab/data-report/tasks/t-smoke/audit
python3 "$T/score_audit.py" \
  --checklist /home/z/my-project/harness-template/scaffold/examples/checklist.json \
  --answers   /home/z/my-project/harness-template/scaffold/examples/answers.json \
  --out "$A/scores.md" > /dev/null
grep -q 'cand-x' "$A/scores.md" && grep -q '7.5/8' "$A/scores.md" && grep -q 'max raw = 8' "$A/scores.md"
echo "score_audit OK"

echo "=== 5. write_library_entry.py ==="
mkdir -p winner && printf '# winner harness\n' > winner/INSTRUCTIONS.md
python3 "$T/write_library_entry.py" --lab fake-lab --domain data-report \
  --harness winner --task t-smoke --name winner-1 \
  --cue "when smoke-testing tabular reports" --lesson "template scripts work" \
  --evidence "base 4/8 -> winner 8/8" --confidence high \
  --component "INSTRUCTIONS.md :: stub -> real :: smoke passed" > /dev/null
test -f fake-lab/library/data-report/harnesses/t-smoke/harness/INSTRUCTIONS.md
grep -q 'harnesses/t-smoke' fake-lab/library/data-report/INDEX.md
grep -qi 'confidence' fake-lab/library/data-report/harnesses/t-smoke/EXPERIENCE.md
echo "write_library_entry OK"

echo "ALL SMOKE TESTS PASSED"
