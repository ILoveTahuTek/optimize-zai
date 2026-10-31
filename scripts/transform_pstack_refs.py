#!/usr/bin/env python3
"""Rewrite internal pstack cross-references after the cursor-* rename.

Only narrow, unambiguous patterns are rewritten (prose must not be mangled:
pstack has skills named after common words like `how`, `why`, `correct`):

  1. frontmatter `name: <n>`        -> `name: cursor-<n>`   (own name only)
  2. `/n`                            -> `/cursor-n`           (slash-command refs,
      also fixes `../n/SKILL.md` -> `../cursor-n/SKILL.md`)
  3. `**n**`                         -> `**cursor-n**`        (bold skill refs)
  4. `the n skill` / `The n skill`   -> `the cursor-N skill`  (explicit phrase)

References to OTHER plugins / built-ins (deslop, babysit, bugbot, poteto-agent,
cursor-team-kit, control-cli, control-ui, create-skill) are intentionally left
untouched; the cross-ref auditor reports them as external.

Usage: python3 transform_pstack_refs.py <skill_dir> <names_file> [--dry-run]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def build_rules(pairs: list[tuple[str, str]]):
    """pairs: (referenced_name, target_name). Returns [(regex, fn)]."""
    rules = []
    for n, target in pairs:
        esc = re.escape(n)
        # 2) slash refs: /n not followed by more name chars (catches ../n/... too)
        rules.append((re.compile(rf"(?P<pre>[/])({esc})(?![a-z0-9-])"),
                      lambda m, t=target: f"{m.group('pre')}{t}"))
        # 3) bold refs: **n**
        rules.append((re.compile(rf"\*\*({esc})\*\*"),
                      lambda m, t=target: f"**{t}**"))
        # 4) explicit phrase: the n skill
        rules.append((re.compile(rf"\b([Tt]he )({esc})( skill\b)"),
                      lambda m, t=target: f"{m.group(1)}{t}{m.group(3)}"))
    return rules


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    skill_dir = Path(sys.argv[1])
    names = [l.strip() for l in Path(sys.argv[2]).read_text().splitlines()
             if l.strip() and not l.startswith("#")]
    dry = "--dry-run" in sys.argv

    own_name = None
    fm = re.match(r"^---\n(.*?)\n---\n", skill_dir.joinpath("SKILL.md").read_text(),
                  re.S) if skill_dir.joinpath("SKILL.md").exists() else None
    if fm:
        m = re.search(r"^name:\s*(\S+)", fm.group(1), re.M)
        if m:
            own_name = m.group(1)

    # pairs = every pstack skill name -> cursor-<name>; plus ALIASES: principle
    # skills are referenced by their SHORT title ("the **<title>** principle
    # skill"), so <title> must map to cursor-principle-<title> as well.
    pairs = [(n, f"cursor-{n}") for n in names]
    for n in names:
        if n.startswith("principle-"):
            pairs.append((n[len("principle-"):], f"cursor-{n}"))
    rules = build_rules(pairs)
    changes = {}
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".json", ".sh", ".py", ".txt", ".yaml", ".yml"}:
            continue
        text = orig = path.read_text(encoding="utf-8", errors="replace")

        # 1) own frontmatter name
        if own_name and path.name == "SKILL.md":
            text = re.sub(rf"^(name:\s*){re.escape(own_name)}\s*$",
                          rf"\g<1>cursor-{own_name}", text, count=1, flags=re.M)

        for rx, fn in rules:
            text = rx.sub(fn, text)

        if text != orig:
            changes[str(path.relative_to(skill_dir))] = sum(
                1 for _ in range(1))  # marker; real counts below
            if not dry:
                path.write_text(text, encoding="utf-8")

    for f in changes:
        print(f"  rewritten: {skill_dir.name}/{f}")
    if not changes and own_name and own_name.startswith("cursor-"):
        pass
    print(f"  {skill_dir.name}: {len(changes)} file(s) changed"
          + (" (dry-run)" if dry else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
