# optimize-zai — sandbox backup

Curated backup of the Z.ai sandbox project (`/home/z/my-project`), refreshed by
`scripts/backup_push.sh` inside the sandbox. Contains **no secrets** (`.env` and tokens
are excluded by design). Canonical copies of this README and `RESTORE.md` live in the
sandbox at `backup-docs/`; the backup script copies them in after syncing.

| Path | What |
|---|---|
| `harness-template/` | Harness-agnostic PPC loop (Propose · Probe · Compose): `PROTOCOL.md` + 4 smoke-tested stdlib scripts + scaffold examples |
| `skills/` | **Organized skill stacks** — see `skills/INDEX.md` |
| `skills/harness-ppc/` | Our own PPC-loop skill (verbatim, never overwritten by other groups) |
| `skills/mattpocock/` | mattpocock/skills set (31 skills, upstream names kept) |
| `skills/cursor/` | pstack from cursor/plugins (58 skills), installed as `cursor-*` with internal cross-references rewritten so the renamed skills still call each other |
| `harness-lab/` | Full experiment evidence: 3 tasks, 13 solver rollouts, per-domain library with 2 adopted harnesses |
| `scripts/` | Experiment scripts, smoke tests, sealed ground truth, `backup_push.sh`, `install_mp_skills.sh`, `install_pstack_skills.sh`, `audit_skill_refs.py`, `gen_backup_skills.py` |
| `download/` | Deliverables — `RESULT-harness2-experiment.md`, `skill-crossref-audit.md` |
| `AGENTS.md` | Standing instructions for any agent working in the restored sandbox |

Cross-reference guarantee: every strong skill-to-skill call in all three stacks was
audited (`download/skill-crossref-audit.md`): 388 RESOLVED, 33 SELF, 10 EXTERNAL
(documented Cursor/plugin deps), 0 BROKEN.

Method provenance: [google-research/harness2](https://github.com/google-research/harness2)
(Apache-2.0, arXiv:2610.14224). Start reading at `harness-template/PROTOCOL.md`.
