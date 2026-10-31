# RESTORE — rebuilding the sandbox from this backup

This repository is a curated backup of the Z.ai sandbox project (`/home/z/my-project`),
maintained by `scripts/backup_push.sh` inside the sandbox. It contains no secrets
(`.env` and tokens are excluded by design).

## What lives here

- `harness-template/` — harness-agnostic PPC loop: protocol, stdlib scripts, examples
- `skills/` — three organized stacks (see `skills/INDEX.md`):
  - `skills/harness-ppc/` — our PPC skill (invoke: "pakai harness loop")
  - `skills/mattpocock/` — mattpocock/skills set (upstream names)
  - `skills/cursor/` — pstack installed as `cursor-*` (refs pre-rewritten)
- `harness-lab/` — full experiment evidence (3 tasks, 13 rollouts, library)
- `scripts/` — experiment + maintenance scripts (`backup_push.sh`,
  `install_mp_skills.sh`, `install_pstack_skills.sh`, `audit_skill_refs.py`)
- `download/` — deliverables (`RESULT-harness2-experiment.md`, `skill-crossref-audit.md`)
- `AGENTS.md` — standing instructions for agents in the restored sandbox

## Restore into a fresh sandbox

```bash
git clone https://github.com/ILoveTahuTek/optimize-zai.git
cd optimize-zai

# 1) project content (merge; do not delete platform files)
cp -a harness-lab scripts download harness-template AGENTS.md /home/z/my-project/

# 2) skills: flatten each group into the sandbox's skills/ dir
mkdir -p /home/z/my-project/skills
cp -a skills/harness-ppc /home/z/my-project/skills/
cp -a skills/mattpocock/* /home/z/my-project/skills/
cp -a skills/cursor/*      /home/z/my-project/skills/
# (sandbox resolves skills by dir name, so groups are flattened on restore;
#  inside THIS repo they stay organized per skills/INDEX.md)

# 3) alternatively/also: pull the latest skill versions straight from upstream
bash /home/z/my-project/scripts/install_mp_skills.sh
bash /home/z/my-project/scripts/install_pstack_skills.sh

# 4) verify the tooling and the skill graph
python3 /home/z/my-project/harness-template/scripts/new_lab.py --help
python3 /home/z/my-project/scripts/audit_skill_refs.py
python3 -c "import json; json.load(open('/home/z/my-project/harness-lab/selection/key.json')); print('key.json ok')"
```

Then read `/home/z/my-project/AGENTS.md` and `harness-template/PROTOCOL.md` before
running tasks. The PPC skill triggers on "pakai harness loop" / "pakai workflow PPC",
or automatically for non-trivial tasks in repeated domains.

## Refresh the backup (from inside the sandbox)

```bash
GHTOKEN=<fine-grained token, Contents: read/write> \
  bash /home/z/my-project/scripts/backup_push.sh
```

The token is used transiently through a git credential helper — never written to disk,
never stored in the repo. Rotate the token after use.
