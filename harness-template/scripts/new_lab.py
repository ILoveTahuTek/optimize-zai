#!/usr/bin/env python3
"""Instantiate the PPC file contract for one task (PROTOCOL.md section 2).

Usage:
  python3 new_lab.py --domain data-report --task sales-2025h4 \
      [--input file_or_dir ...] [--lab-root harness-lab] \
      [--adopt-from /path/to/harness_tree]

Creates:
  <lab-root>/<domain>/tasks/<task>/{input,harnesses/{base,candidates,composed},
  runs,selection/blind,audit}

If a library entry exists for the domain, a hint is printed (--adopt-from to adopt it).
"""
from __future__ import annotations

import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

STUB = """# Base harness — {task} ({domain})

Replace this stub with the real harness before the base rollout.
A harness is everything around the solver: instructions, skills, scripts,
output contract. See PROTOCOL.md sections 1-2.

## Output contract (minimum)
- `report.md`: method, definitions, headline numbers, verification notes
- `process.md`: what was done, in order
"""


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Instantiate the PPC lab file contract for one task.")
    ap.add_argument("--domain", required=True)
    ap.add_argument("--task", required=True)
    ap.add_argument("--input", action="append", default=[],
                    help="file or directory to copy into input/ (repeatable)")
    ap.add_argument("--lab-root", default="harness-lab")
    ap.add_argument("--adopt-from", default=None,
                    help="harness tree to adopt verbatim as base (e.g. a library entry)")
    a = ap.parse_args()

    root = Path(a.lab_root) / a.domain / "tasks" / a.task
    dirs = [
        root / "input",
        root / "harnesses" / "base",
        root / "harnesses" / "candidates",
        root / "harnesses" / "composed",
        root / "runs",
        root / "selection" / "blind",
        root / "audit",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    for item in a.input:
        src = Path(item)
        if not src.exists():
            print(f"ERROR: --input not found: {src}", file=sys.stderr)
            return 2
        dst = root / "input" / src.name
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    base = root / "harnesses" / "base"
    if a.adopt_from:
        src = Path(a.adopt_from)
        if not src.exists():
            print(f"ERROR: --adopt-from not found: {src}", file=sys.stderr)
            return 2
        shutil.copytree(src, base, dirs_exist_ok=True)
        (base / "ADOPTED.md").write_text(
            f"Adopted verbatim from: {src.resolve()}\nDate: {date.today().isoformat()}\n",
            encoding="utf-8")
    else:
        (base / "INSTRUCTIONS.md").write_text(
            STUB.format(task=a.task, domain=a.domain), encoding="utf-8")

    lib_index = Path(a.lab_root) / "library" / a.domain / "INDEX.md"
    print(f"lab ready: {root}")
    for d in dirs:
        print(f"  {d}")
    if lib_index.exists():
        print(f"HINT: library entry exists for this domain: {lib_index}")
        print("      consider --adopt-from <library harness tree>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
