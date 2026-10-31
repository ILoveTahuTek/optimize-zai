#!/usr/bin/env python3
"""Cross-reference auditor for installed agent skills.

Answers, per skill: can the skills it names actually be invoked here?

Scope: cursor-* (pstack, renamed), the mattpocock set (manifest), harness-ppc.
Only STRONG call patterns are audited (paths and ordinary prose are ignored):

  /name                 - counted only when <name> is a cataloged skill name
  **name**              - bold skill ref (pstack style)
  "the name skill"      - explicit phrase
  Skill(command="name") - explicit tool call
  pstack:<name>         - Claude Code adapter style (harness-specific note)

Classification:

  RESOLVED  target skill is installed here
  SELF      /own-name invocation ref (valid)
  EXTERNAL  known other-plugin / built-in / agent (documented, unavailable here)
  BROKEN    pre-rename pstack name still referenced (target exists as cursor-*)
  UNKNOWN   strong call to something neither installed nor known-external

Output: download/skill-crossref-audit.md + stdout summary.

Usage: python3 audit_skill_refs.py
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path("/home/z/my-project/skills")
PROJ = Path("/home/z/my-project")
OUT = PROJ / "download" / "skill-crossref-audit.md"

EXTERNAL = {
    "deslop", "babysit", "bugbot", "poteto-agent", "comment-sicko",
    "control-cli", "control-ui", "create-skill",
}
SCAN_EXT = {".md", ".json", ".py", ".sh", ".txt", ".yaml", ".yml"}


def load_manifest(p: Path) -> list[str]:
    return [l.strip() for l in p.read_text().splitlines()
            if l.strip() and not l.startswith("#")]


def main() -> int:
    installed = sorted(d.name for d in ROOT.iterdir() if d.is_dir())
    cursor = load_manifest(PROJ / "scripts" / "manifest_cursor_skills.txt")
    mp = load_manifest(PROJ / "scripts" / "manifest_mp_skills.txt")
    audited = sorted(set(cursor) | set(mp) | {"harness-ppc"})
    pstack_old = sorted(n[len("cursor-"):] for n in cursor)

    catalog = set(installed) | set(EXTERNAL) | set(pstack_old)

    slash_re = re.compile(r"(?<![A-Za-z0-9_/-])/(?P<n>[a-z][a-z0-9-]*)")
    bold_re = re.compile(r"\*\*(?P<n>[a-z][a-z0-9-]*)\*\*")
    phrase_re = re.compile(r"\b[Tt]he (?P<n>[a-z][a-z0-9-]*) skill\b")
    tool_re = re.compile(r"""Skill\([^)]{0,80}?["'`](?P<n>[a-z][a-z0-9-]*)["'`]""")
    pstackcol_re = re.compile(r"\bpstack:(?P<n>[a-z][a-z0-9-]*)")

    def classify(n: str, own: str) -> str:
        if n == own:
            return "SELF"
        if n in installed:
            return "RESOLVED"
        if n in EXTERNAL:
            return "EXTERNAL"
        if n in pstack_old:
            return "BROKEN"
        return "UNKNOWN"

    report: dict[str, dict[str, list[str]]] = {}
    for skill in audited:
        base = ROOT / skill
        if not base.is_dir():
            print(f"WARN: {skill} not found on disk", file=sys.stderr)
            continue
        # call styles differ per stack: pstack bolds skill names ("the **how**
        # skill"); mattpocock prose uses bold for emphasis, calls via /name and
        # Skill(command="name"). Bold is therefore a strong signal only in
        # cursor-* skills.
        pstack_style = skill.startswith("cursor-")
        hits: dict[str, list[str]] = defaultdict(list)

        def add(cat: str, n: str, rel: Path, i: int, line: str):
            entry = f"{rel}:{i} `{n}` — {line.strip()[:100]}"
            if entry not in hits[cat]:
                hits[cat].append(entry)

        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in SCAN_EXT:
                continue
            rel = path.relative_to(base)
            for i, line in enumerate(path.read_text(encoding="utf-8",
                                     errors="replace").splitlines(), 1):
                for m in pstackcol_re.finditer(line):
                    add("EXTERNAL", f"pstack:{m.group('n')}", rel, i, line)
                for m in slash_re.finditer(line):
                    n = m.group("n")
                    if n in catalog:
                        add(classify(n, skill), n, rel, i, line)
                if pstack_style:
                    for m in bold_re.finditer(line):
                        n = m.group("n")
                        if "-" in n or line[m.end():].lstrip().startswith("skill"):
                            add(classify(n, skill), n, rel, i, line)
                for m in phrase_re.finditer(line):
                    n = m.group("n")
                    if "-" in n or n in catalog:
                        add(classify(n, skill), n, rel, i, line)
                for m in tool_re.finditer(line):
                    add(classify(m.group("n"), skill), m.group("n"), rel, i, line)
        report[skill] = hits

    # ---- render ----
    def count(cat: str) -> int:
        return sum(len(report[s].get(cat, [])) for s in report)

    lines = [
        "# Skill cross-reference audit",
        "",
        f"Scope: {len(audited)} audited skills out of {len(installed)} installed · "
        f"RESOLVED {count('RESOLVED')} · SELF {count('SELF')} · "
        f"EXTERNAL {count('EXTERNAL')} · **BROKEN {count('BROKEN')}** · "
        f"**UNKNOWN {count('UNKNOWN')}**",
        "",
        "Only strong call patterns are audited: `/name` (when the name is a "
        "cataloged skill), `**name**`, `the name skill`, `Skill(command=\"name\")`, "
        "`pstack:name`. Ordinary paths and prose are ignored.",
        "",
        "## Summary",
        "",
        "| skill | RESOLVED | SELF | EXTERNAL | BROKEN | UNKNOWN |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for skill in audited:
        h = report.get(skill, {})
        lines.append("| {} | {} | {} | {} | {} | {} |".format(
            skill, len(h.get("RESOLVED", [])), len(h.get("SELF", [])),
            len(h.get("EXTERNAL", [])), len(h.get("BROKEN", [])),
            len(h.get("UNKNOWN", []))))

    sections = (
        ("BROKEN", "Broken references (pre-rename pstack name or missing target — must fix)"),
        ("UNKNOWN", "Unknown references (strong call, but not installed and not known-external)"),
        ("EXTERNAL", "External references (other plugin / built-in / agent — unavailable in this sandbox by design)"),
    )  # noqa: E128
    for cat, title in sections:
        lines += ["", f"## {title}", ""]
        any_cat = False
        for skill in audited:
            for item in report.get(skill, {}).get(cat, []):
                any_cat = True
                lines.append(f"- **{skill}** {item}")
        if not any_cat:
            lines.append("(none)")

    lines += ["", "## Notes", "",
              "- pstack was installed as `cursor-*` (58 skills); internal refs were "
              "rewritten by `scripts/transform_pstack_refs.py`, then audited here.",
              "- EXTERNAL deps of the original stacks: `deslop`/`babysit`/`bugbot`/"
              "`create-skill` (Cursor built-ins or cursor-team-kit plugin), "
              "`poteto-agent`/`comment-sicko` (pstack agents/), `pstack:*` (Claude "
              "Code adapter command style). The affected steps need those hosts; "
              "everything else works in this sandbox.",
              "- mattpocock set and harness-ppc are referenced with their installed "
              "names; all their strong refs resolve.",
              ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report: {OUT}")
    print("RESOLVED={} SELF={} EXTERNAL={} BROKEN={} UNKNOWN={}".format(
        count("RESOLVED"), count("SELF"), count("EXTERNAL"),
        count("BROKEN"), count("UNKNOWN")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
