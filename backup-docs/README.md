# optimize-zai — sandbox backup

Curated backup of the Z.ai sandbox project (`/home/z/my-project`), refreshed by
`scripts/backup_push.sh` inside the sandbox. Contains **no secrets** (`.env` and tokens
are excluded by design). Canonical copies of this README and `RESTORE.md` live in the
sandbox at `backup-docs/`; the backup script copies them in after syncing.

| Path | What |
|---|---|
| `harness-template/` | Harness-agnostic PPC loop (Propose · Probe · Compose): `PROTOCOL.md` + 4 smoke-tested stdlib scripts + scaffold examples |
| `skills/harness-ppc/` | The agent skill that auto-applies the loop to future tasks |
| `harness-lab/` | Full experiment evidence: 3 tasks, 13 solver rollouts, per-domain library with 2 adopted harnesses |
| `scripts/` | Experiment scripts, smoke tests, sealed ground truth, `backup_push.sh`, `install_mp_skills.sh` |
| `download/` | Deliverables — `RESULT-harness2-experiment.md` is the written report |
| `AGENTS.md` | Standing instructions for any agent working in the restored sandbox |

Third-party agent skills (mattpocock/skills) are NOT stored here — reinstall with one
command via `scripts/install_mp_skills.sh` (see RESTORE.md).

Method provenance: [google-research/harness2](https://github.com/google-research/harness2)
(Apache-2.0, arXiv:2610.14224). Start reading at `harness-template/PROTOCOL.md`.
