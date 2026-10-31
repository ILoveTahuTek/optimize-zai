"""Harnessing-level recursion: store the adopted harness + experience in the domain library,
mirror of harness2/core/library.py layout. Also seal the ground truth away from the lab tree
before task 2 (leak hardening, mirror of leak_globs).
"""
import shutil
from pathlib import Path

LAB = Path("/home/z/my-project/harness-lab")
SURFACE_FILES = ["INSTRUCTIONS.md", "scripts/profile_csv.py", "skills/data-hygiene/SKILL.md"]
TASK = "sales-2025h1"
DOMAIN = "data-report"

entry = LAB / "library" / DOMAIN / "harnesses" / TASK
harness_dir = entry / "harness"
harness_dir.mkdir(parents=True, exist_ok=True)
for rel in SURFACE_FILES:
    src = LAB / "harnesses" / "c1" / rel
    dst = harness_dir / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst)

experience = """# sales-2025h1

- adopted: `c1`  (composed from probes inv1 + dom1 on base evidence)
- components: 1 skill, 1 script; INSTRUCTIONS.md rewrite (~2.4k chars always-on)

## Why this was chosen

Blind selector picked it from four anonymized reports; the external audit then
confirmed it as top-tier: 8/8 checks vs base harness 5/8. Base run held correct
numbers but mislabeled GROSS as "net sales", presented three competing totals
under one label, and had no verification section.

## What each edit did

- component: INSTRUCTIONS.md (system prompt + guardrails)
  change: mandated single NET headline, explicit NET/GROSS/refund definitions, row-count
  identity, exact-number data-quality section, per-figure verification table
  observed: base report's mislabeled totals and missing verification disappeared; audit 5/8 -> 8/8
- component: scripts/profile_csv.py (new script)
  change: deterministic pre-analysis profiler (dupes/refunds/zero rows/missing fields/net split)
  observed: every run starts from identical evidence base; ad-hoc dedup decisions eliminated
- component: skills/data-hygiene/SKILL.md (new skill)
  change: profiler-first workflow + one independent cross-check requirement
  observed: dom1 probe followed its spirit even when it could not find the file
- component: skill/script path references
  change: relative paths -> absolute paths
  observed: dom1 probe could not locate the skill via relative reference; c1 rollout found
  everything immediately -- relative harness paths are a real defect class

## Transferable lesson

- **cue**: When a task gives tabular data to a fresh solver under a time budget
- **lesson**: Ship a deterministic profiler script + written definitions (NET/GROSS/refunds)
  + a mandatory per-figure verification table inside the harness, and reference every
  harness asset by ABSOLUTE path.
- **evidence**: Task-1 audit: base 5/8, inv1 8/8, dom1 7/8, composed c1 8/8; probe run
  demonstrated the relative-path failure mode directly.
- **confidence**: high for this observed contrast; untested on data with quirks beyond
  duplicates/refunds/missing-fields (e.g. outliers, zero rows)
"""
(entry / "EXPERIENCE.md").write_text(experience)

index = [f"# Library — {DOMAIN}", "",
         "Each entry is an earlier task in THIS domain whose harness was chosen, stored",
         "with its FULL component tree and why it was picked.", "",
         f"## `harnesses/{TASK}/`",
         "- harness: `harnesses/sales-2025h1/harness/` — 1 skill, 1 script; INSTRUCTIONS.md rewrite",
         "- why:     `harnesses/sales-2025h1/EXPERIENCE.md`",
         "- cue:     When a task gives tabular data to a fresh solver under a time budget", ""]
(LAB / "library" / DOMAIN / "INDEX.md").write_text("\n".join(index))

# Leak hardening for task 2: move ground truth out of the lab tree
gt_src = LAB / "ground_truth.json"
gt_dst = Path("/home/z/my-project/scripts/gt_sealed")
gt_dst.mkdir(parents=True, exist_ok=True)
shutil.move(str(gt_src), gt_dst / "ground_truth.json")

print("library written:")
for p in sorted((LAB / "library").rglob("*")):
    if p.is_file():
        print("  ", p.relative_to(LAB))
print("ground truth sealed ->", gt_dst)
