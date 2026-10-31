---
name: harness-ppc
description: "Harness-agnostic Propose-Probe-Compose (PPC) quality loop: improve the harness around the model (instructions, skills, scripts, output contracts) instead of the model, using behavioral-contrast evidence, blind selection, sealed ground-truth audit, and a persistent per-domain library. Use when the user asks to apply the harness workflow ('pakai harness loop', 'pakai workflow PPC', 'apply the harness template', 'optimize pakai PPC'), when migrating a previously adopted harness to new data in the same domain, or for any non-trivial task in a repeated domain where reliability matters."
---

# PPC Loop (Propose · Probe · Compose) — harness-agnostic template

Authoritative spec: `/home/z/my-project/harness-template/PROTOCOL.md` — read it fully
before the first loop run in a session. Tooling: `/home/z/my-project/harness-template/scripts/`
(Python stdlib only; all smoke-tested). Validation evidence:
`/home/z/my-project/download/RESULT-harness2-experiment.md` (task 1: 5/8 → 8/8;
library transfer: 8/10 → 10/10; task 3 k=2: pool → 10/10).

## When to run, and which tier

- T0 single pass: trivial or throwaway tasks — NO loop.
- T1 k=1: repeated but cheap domain — base → 1 candidate → compose → blind select.
- T2 k≥2 parallel: dirty data or high stakes — base → 2k candidates → 2 compositions → blind select.

Skip for pure conversation, one-shot edits, or incomparable outputs.

## Role mapping in this environment

| Role | Who |
|---|---|
| SOLVER | a Task subagent, model pinned, stateless — it receives ONLY the harness tree path + input dir path, nothing else |
| PROPOSER / COMPOSER / SELECTOR / AUDITOR | you (the main agent) |
| Harness | the solver's `INSTRUCTIONS.md` + `skills/` + `scripts/` as one runnable tree |

## Running order (compressed — PROTOCOL.md §3 is authoritative)

1. MIGRATE: if `harness-lab/library/<domain>/INDEX.md` exists, adopt its newest harness
   verbatim as base (`new_lab.py --adopt-from ...`).
2. BASE ROLLOUT with a subagent → `runs/base/report.md`.
3. DEFECT SCAN: one line per defect, verbatim quote as evidence.
4. PROPOSE candidates (full runnable trees; generic + domain levers; every defect → mechanism).
5. PROBE: smoke-test scripts on synthetic mini-data first; fresh subagent per candidate.
6. COMPOSE + self-containment check: absolute paths, no references outside the tree.
7. SELECT: `blind_reports.py --scrub` → write `selection/ranking.md` FIRST → only then
   open `key.json`.
8. AUDIT: sealed ground truth + `score_audit.py`, post-selection only.
9. PERSIST: `write_library_entry.py` (cue / lesson / evidence / confidence) if winner ≠ base.

## Non-negotiable rules (full list: PROTOCOL.md §4)

1. Evidence = behavioral contrast between harness runs on the same input, never opinions.
2. Harness must be self-contained: absolute paths (relative skill references failed 3 of 4
   times in validation), assets inside the tree.
3. Ground truth stays sealed OUTSIDE the lab tree until ranking.md exists.
4. Selection keys are strict JSON; reports share one schema; scrub labels (`--scrub`).
5. Never tune candidates on ground truth; every adopted edit cites mechanism + evidence.

## Lab layout (created by scripts)

```
harness-lab/<domain>/tasks/<task>/{input, harnesses/{base,candidates,composed},
runs, selection/{blind,key.json,ranking.md}, audit/{checklist.json,answers.json,scores.md}}
harness-lab/library/<domain>/{INDEX.md, harnesses/<task>/{harness/, EXPERIENCE.md}}
```
