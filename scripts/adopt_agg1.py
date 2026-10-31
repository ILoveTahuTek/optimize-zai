"""Adopt agg1 into the domain library after the k=2 run + update EXPERIENCE and INDEX."""
import shutil
from pathlib import Path

LAB = Path("/home/z/my-project/harness-lab")
TASK = "sales-2025h1-dirty"
entry = LAB / "library" / "data-report" / "harnesses" / TASK
harness_dir = entry / "harness"
if harness_dir.exists():
    shutil.rmtree(harness_dir)
harness_dir.mkdir(parents=True)
for rel in ["INSTRUCTIONS.md", "scripts/profile_csv.py", "scripts/detect_anomalies.py",
            "skills/data-hygiene/SKILL.md", "skills/anomaly-watch/SKILL.md"]:
    src = LAB / "harnesses" / "agg1" / rel
    dst = harness_dir / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst)

experience = """# sales-2025h1-dirty

- adopted: `agg1` (k=2 parallel composition; merged from pool base/inv1/dom1/inv2/dom2)
- components: 2 scripts, 2 skills; INSTRUCTIONS.md full rewrite (~3.1k chars always-on)

## Why this was chosen

Blind selector picked it from seven anonymized reports; external audit vs sealed ground
truth: 10/10 (with inv1, dom1, dom2, agg2 — pool numbers all converged correct). It was
chosen for process completeness, not for different numbers: verbatim tool inventories,
per-figure two-implementation verification, tool-vs-spec discrepancies reconciled openly
(malformed month keys from naive date slicing; positive-only duplicate value 735 vs signed
270), and an assumptions catalog with alternatives, effects and affected-row counts.

## What each edit did

- component: scripts/detect_anomalies.py (new, from dom2)
  change: pre-parse anomaly inventory (date-format census, price constancy, dupes, refunds)
  observed: caught the 2 DD/MM/YYYY rows and the Monitor 210->220 step with row counts
- component: scripts/profile_csv.py (carried from dom1/c1)
  change: deterministic NET/GROSS/refund/duplicate evidence base
  observed: all runs converged on identical correct headline numbers
- component: skills/* referenced by ABSOLUTE path
  change: fixed the recurring relative-reference defect (dom1 probe round 1, dom1+dom2 probes
  round 2 all lost relatively-referenced skill files even though the files existed)
  observed: agg1 rollout read both skills immediately
- component: INSTRUCTIONS.md (merged inv1+inv2 discipline)
  change: definitions + row identity + anomaly section + assumptions-with-alternatives +
  exec summary + verification table
  observed: audit 10/10; base harness 8/10 lacked verification and identity guarantees

## Transferable lesson

- **cue**: When refining analysis harnesses for dirty tabular data
- **lesson**: Correctness saturates fast (base numbers were already right); what the harness
  buys is STRUCTURAL guarantees (verification, definitions, anomaly disclosure) instead of
  hope, at a real cost (+54% solver tokens vs base). Prefer absolute paths or inline
  instructions over relative skill references — the latter failed 3 of 4 times it was tried.
- **evidence**: task-3 scoreboard: base 8/10, inv2 9/10, five harnesses 10/10; skill-file
  loss reproduced across two different harnesses and two different solver runs.
- **confidence**: high for structural-guarantee claims; cost/benefit of the kitchen-sink
  harness on easy data is still open (agg1 was the priciest composition to run).
"""
(entry / "EXPERIENCE.md").write_text(experience)

index_lines = [
    "# Library — data-report", "",
    "Each entry is an earlier task in THIS domain whose harness was chosen, stored",
    "with its FULL component tree and why it was picked.", "",
    "## `harnesses/sales-2025h1/`",
    "- harness: c1 — 1 skill, 1 script; definitions + verification",
    "- why: `harnesses/sales-2025h1/EXPERIENCE.md`",
    "- cue: When a task gives tabular data to a fresh solver under a time budget", "",
    "## `harnesses/sales-2025h1-dirty/`",
    "- harness: agg1 — 2 skills, 2 scripts; + anomaly inventory + assumptions catalog, absolute paths",
    "- why: `harnesses/sales-2025h1-dirty/EXPERIENCE.md`",
    "- cue: When refining analysis harnesses for dirty tabular data", "",
]
(LAB / "library" / "data-report" / "INDEX.md").write_text("\n".join(index_lines))
print("library updated:")
for p in sorted((LAB / "library").rglob("*")):
    if p.is_file():
        print("  ", p.relative_to(LAB))
