#!/usr/bin/env bash
# Refresh the curated sandbox backup in /home/z/my-project/.backup/ and push to GitHub.
# Secrets are excluded by design (.env, tokens). The token is used transiently via a
# credential helper and never written to disk.
#
# Usage:
#   GHTOKEN=<fine-grained token with Contents: read/write> bash scripts/backup_push.sh [branch]
set -euo pipefail

PROJ=/home/z/my-project
BK="$PROJ/.backup"
BRANCH="${1:-main}"
REMOTE_URL="${OPTIMIZE_ZAI_URL:-https://github.com/ILoveTahuTek/optimize-zai.git}"

mkdir -p "$BK"

# 1) Curated mirror of the project (no .git, no .env, no third-party clones, no uploads)
rsync -a --delete \
  --exclude '.git/' \
  --exclude '.env' \
  --exclude 'repo-harness2/' \
  --exclude 'skills/' \
  --exclude 'upload/' \
  --exclude '__pycache__/' \
  --exclude '.backup/' \
  "$PROJ/" "$BK/"

# 2) Skills, organized: harness-ppc (ours, verbatim) + mattpocock/ + cursor/
#    (pstack renamed) per manifests; INDEX.md generated. Third-party groups are
#    copied into their own subdirs and can never touch harness-ppc.
python3 "$PROJ/scripts/gen_backup_skills.py" "$BK"

# 2b) Repo-level docs are canonical in $PROJ/backup-docs and must survive rsync --delete
cp -a "$PROJ/backup-docs/README.md"   "$BK/README.md"
cp -a "$PROJ/backup-docs/RESTORE.md"  "$BK/RESTORE.md"
cp -a "$PROJ/backup-docs/gitignore"   "$BK/.gitignore"

# 3) Guard: refuse to commit if any secret-looking file slipped in
if find "$BK" -maxdepth 2 -name '.env' -o -maxdepth 2 -name '*.pem' | grep -q .; then
  echo "ABORT: secret-looking file found in staging" >&2
  exit 3
fi

# 4) Commit (clean history lives in .backup, separate from the platform's .git)
cd "$BK"
if [ ! -d .git ]; then
  git init -b "$BRANCH" >/dev/null
  git config user.name  "ILoveTahuTek"
  git config user.email "ILoveTahuTek@users.noreply.github.com"
fi
git add -A
if ! git diff --cached --quiet; then
  git commit -q -m "backup: sandbox snapshot $(date '+%F %H:%M %Z')"
else
  echo "no changes to commit"
fi

# 5) Push — token via inline credential helper (never in the URL, never in output)
if [ -n "${GHTOKEN:-}" ]; then
  git -c credential.helper='!f() { printf "username=x-access-token\npassword=%s\n" "$GHTOKEN"; }; f' \
    push "$REMOTE_URL" "HEAD:refs/heads/${BRANCH}"
  echo "pushed: $REMOTE_URL ($BRANCH)"
else
  echo "GHTOKEN not set — committed locally in $BK, NOT pushed."
fi
