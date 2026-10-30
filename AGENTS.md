# AGENTS.md — standing instructions for this sandbox

For any agent (human-guided or autonomous) working inside `/home/z/my-project/`:

1. **Workflow.** For any non-trivial task in a repeated domain (reports, analyses, code
   with checkable output), run the `harness-ppc` skill — the Propose–Probe–Compose loop.
   Spec: `harness-template/PROTOCOL.md`; scripts: `harness-template/scripts/` (stdlib only).
   Trigger phrases: "pakai harness loop", "pakai workflow PPC", "apply the harness template".
2. **Library first.** Before proposing new harnesses, check
   `harness-lab/library/<domain>/INDEX.md` and adopt the newest harness verbatim as base.
3. **Evidence discipline.** Ground truth is sealed outside the lab tree until blind
   selection is written; selection keys are strict JSON; audit is post-selection only.
4. **Lab is evidence.** `harness-lab/` is an append-only experiment record — do not rewrite
   past tasks; add new task dirs instead.
5. **Secrets.** Never write tokens/keys to files or commits; they live only in the current
   shell session and must be rotated by the user after use.
6. **Backup.** This project mirrors `github.com/ILoveTahuTek/optimize-zai` (curated:
   excludes third-party clones and vendored skills). See `RESTORE.md` in that repo.
