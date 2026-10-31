#!/usr/bin/env bash
# Install/update Matt Pocock's agent skills (github.com/mattpocock/skills) into this sandbox.
#
# Usage:
#   bash scripts/install_mp_skills.sh [INCLUDE_WIP=1]
#
# - Stable categories (engineering, productivity, misc) are installed into
#   /home/z/my-project/skills/<name>/ (pristine upstream copy, per-skill).
# - skills/in-progress is skipped unless INCLUDE_WIP=1 (work-in-progress upstream).
# - Existing local copies are compared first: SAME is kept, DIFFERENT/NEW is synced.
set -euo pipefail

SRC=/tmp/mp-skills
DEST=/home/z/my-project/skills
INCLUDE_WIP="${1:-0}"

rm -rf "$SRC"
if [ -n "${MP_SKILLS_REF:-}" ]; then
  git clone --depth 1 -q --branch "$MP_SKILLS_REF" https://github.com/mattpocock/skills.git "$SRC"
else
  git clone --depth 1 -q https://github.com/mattpocock/skills.git "$SRC"
fi
UPSTREAM=$(git -C "$SRC" log -1 --format='%h %ad' --date=short)
echo "upstream: $UPSTREAM"

new=0; updated=0; same=0
for cat in engineering productivity misc; do
  for skill_dir in "$SRC/skills/$cat"/*/; do
    name=$(basename "$skill_dir")
    [ "$name" = "deprecated" ] && continue
    target="$DEST/$name"
    if [ -d "$target" ]; then
      if diff -rq "$skill_dir" "$target" >/dev/null 2>&1; then
        same=$((same+1)); echo "SAME      $name"
      else
        rsync -a --delete "$skill_dir" "$target/"
        updated=$((updated+1)); echo "UPDATED   $name"
      fi
    else
      rsync -a "$skill_dir" "$target/"
      new=$((new+1)); echo "NEW       $name"
    fi
  done
done

if [ "$INCLUDE_WIP" = "1" ]; then
  echo "--- including skills/in-progress (WIP, upstream may be unstable) ---"
  for skill_dir in "$SRC/skills/in-progress"/*/; do
    name=$(basename "$skill_dir")
    rsync -a --delete "$skill_dir" "$DEST/$name/"
    echo "INSTALLED(WIP) $name"
  done
else
  echo "skipped skills/in-progress (set INCLUDE_WIP=1 to install): $(ls "$SRC/skills/in-progress" | grep -v README | tr '\n' ' ')"
fi

echo "summary: new=$new updated=$updated same=$same"
echo "installed at: $DEST"
