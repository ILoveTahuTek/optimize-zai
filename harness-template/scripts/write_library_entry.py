#!/usr/bin/env python3
"""Promote a winning harness into the domain library (PROTOCOL.md section 3, step 8).

Usage:
  python3 write_library_entry.py --lab harness-lab --domain data-report \
      --harness <task>/harnesses/agg1 --task sales-2025h4 --name agg1 \
      --cue "when to reach for this harness" \
      --lesson "what it now guarantees" \
      --evidence "base said X (defect), adopted said Y (verified)" \
      [--confidence high] \
      [--component "scripts/profile_csv.py :: deterministic profiler :: all runs converged"]

Creates/updates:
  <lab>/library/<domain>/harnesses/<task>/harness/   full tree copy, runnable as-is
  <lab>/library/<domain>/harnesses/<task>/EXPERIENCE.md
  <lab>/library/<domain>/INDEX.md                    (created or appended)
"""
from __future__ import annotations

import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

EXPERIENCE = """# {task}

- adopted: `{name}` ({today})
- source: `{harness}`

## Cue
{cue}

## Lesson
{lesson}

## Evidence
{evidence}

## Confidence
{confidence}

## Components
{components}
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Promote a winning harness to the library.")
    ap.add_argument("--lab", default="harness-lab")
    ap.add_argument("--domain", required=True)
    ap.add_argument("--harness", required=True, help="path to the winning harness tree")
    ap.add_argument("--task", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--cue", required=True)
    ap.add_argument("--lesson", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--confidence", default="medium")
    ap.add_argument("--component", action="append", default=[],
                    help="repeatable: '<file> :: <change> :: <observed>'")
    a = ap.parse_args()

    harness = Path(a.harness)
    if not harness.is_dir():
        print(f"ERROR: harness tree not found: {harness}", file=sys.stderr)
        return 2

    lib = Path(a.lab) / "library" / a.domain
    entry = lib / "harnesses" / a.task
    shutil.copytree(harness, entry / "harness", dirs_exist_ok=True)

    comps = "\n".join(f"- {c}" for c in a.component) or "- (not itemized)"
    (entry / "EXPERIENCE.md").write_text(
        EXPERIENCE.format(task=a.task, name=a.name, today=date.today().isoformat(),
                          harness=harness, cue=a.cue, lesson=a.lesson,
                          evidence=a.evidence, confidence=a.confidence,
                          components=comps),
        encoding="utf-8")

    index = lib / "INDEX.md"
    section = (f"## `harnesses/{a.task}/`\n"
               f"- harness: {a.name}\n"
               f"- why: `harnesses/{a.task}/EXPERIENCE.md`\n"
               f"- cue: {a.cue}\n")
    if index.exists():
        txt = index.read_text(encoding="utf-8")
        if f"harnesses/{a.task}/" in txt:
            print(f"INDEX.md already covers {a.task}; EXPERIENCE.md refreshed in place.")
        else:
            index.write_text(txt.rstrip("\n") + "\n\n" + section, encoding="utf-8")
    else:
        index.write_text(
            f"# Library — {a.domain}\n\n"
            "Each entry is an earlier task in THIS domain whose harness was chosen,\n"
            "stored with its FULL component tree and why it was picked.\n\n" + section,
            encoding="utf-8")

    print(f"library entry written: {entry}")
    print(f"index: {index}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
