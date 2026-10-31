#!/usr/bin/env python3
"""Build the organized skills/ tree of the backup repository + its INDEX.md.

Layout produced (inside <backup>/skills/):

  skills/
    INDEX.md                <- generated: what each group is, how to invoke
    harness-ppc/            <- our own skill, copied verbatim (never overwritten)
    mattpocock/<name>/      <- mattpocock set, per scripts/manifest_mp_skills.txt
    cursor/cursor-<name>/   <- pstack renamed, per scripts/manifest_cursor_skills.txt

Usage: python3 gen_backup_skills.py <backup_root>
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

PROJ = Path("/home/z/my-project")
SKILLS = PROJ / "skills"


def load_manifest(p: Path) -> tuple[str, list[str]]:
    version = ""
    names = []
    for line in p.read_text().splitlines():
        if line.startswith("# upstream:"):
            version = line.split("upstream:", 1)[1].strip()
        elif line.strip() and not line.startswith("#"):
            names.append(line.strip())
    return version, names


def frontmatter(skill_dir: Path) -> tuple[str, str]:
    p = skill_dir / "SKILL.md"
    if not p.exists():
        return skill_dir.name, "(no SKILL.md)"
    text = p.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    name, desc = skill_dir.name, ""
    if m:
        fm = m.group(1)
        nm = re.search(r"^name:\s*(.+)$", fm, re.M)
        dm = re.search(r"^description:\s*(.+?)(?=^\w+:|\Z)", fm, re.M | re.S)
        if nm:
            name = nm.group(1).strip().strip('"')
        if dm:
            desc = " ".join(dm.group(1).split())
    return name, desc


def copy_group(manifest: Path, dest_group: Path) -> list[tuple[str, str, str]]:
    version, names = load_manifest(manifest)
    rows = []
    for n in names:
        src = SKILLS / n
        if not src.is_dir():
            print(f"WARN: manifest skill missing on disk: {n}", file=sys.stderr)
            continue
        shutil.copytree(src, dest_group / n, dirs_exist_ok=True)
        inv, desc = frontmatter(src)
        rows.append((n, inv, desc))
    return rows


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    bk = Path(sys.argv[1])
    skills_root = bk / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)

    # harness-ppc: copy fresh but never clobber manually — it is owned by us,
    # so a verbatim refresh is safe; the point of "no overwrite" is to not let
    # third-party groups touch it.
    shutil.copytree(SKILLS / "harness-ppc", skills_root / "harness-ppc",
                    dirs_exist_ok=True)

    mp_rows = copy_group(PROJ / "scripts" / "manifest_mp_skills.txt",
                         skills_root / "mattpocock")
    cur_rows = copy_group(PROJ / "scripts" / "manifest_cursor_skills.txt",
                          skills_root / "cursor")

    mp_ver, _ = load_manifest(PROJ / "scripts" / "manifest_mp_skills.txt")
    cur_ver, _ = load_manifest(PROJ / "scripts" / "manifest_cursor_skills.txt")

    def table(rows, title):
        out = [f"## {title}", "", "| install dir | invoke as | description |",
               "|---|---|---|"]
        for n, inv, desc in rows:
            out.append(f"| `{n}` | `{inv}` | {desc[:160]} |")
        return out

    lines = [
        "# skills/ — index",
        "",
        "Three stacks, organized by origin so each skill can be invoked by its",
        "`name:` (the Skill tool matches the install dir). Restoring = copying a",
        "group back into the sandbox's flat `skills/` dir (see RESTORE.md).",
        "",
        "| group | count | source |",
        "|---|---|---|",
        f"| `harness-ppc/` | 1 | authored in this sandbox (PPC loop) |",
        f"| `mattpocock/` | {len(mp_rows)} | github.com/mattpocock/skills @ {mp_ver} |",
        f"| `cursor/` | {len(cur_rows)} | github.com/cursor/plugins `pstack` @ {cur_ver}, installed as `cursor-*` with internal refs rewritten |",
        "",
        "Cross-reference audit (all strong calls resolve):",
        "`download/skill-crossref-audit.md`.",
    ]
    lines += ["", "## harness-ppc", ""]
    inv, desc = frontmatter(SKILLS / "harness-ppc")
    lines += [f"- `{inv}` — {desc}",
              "- spec: `harness-template/PROTOCOL.md`; triggers: \"pakai harness loop\", "
              "\"pakai workflow PPC\""]
    lines += table(mp_rows, "mattpocock/")
    lines += table(cur_rows, "cursor/ (pstack, renamed)")
    (skills_root / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"skills tree built: {skills_root} "
          f"(harness-ppc 1, mattpocock {len(mp_rows)}, cursor {len(cur_rows)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
