#!/usr/bin/env python3
"""Blind the run reports for selection (PROTOCOL.md section 3, step 6).

Usage:
  python3 blind_reports.py --runs <runs_dir> --out <task>/selection [--seed 7] [--scrub]

Expects <runs_dir>/<harness>/report.md (or flat <runs_dir>/<harness>.report.md).
Writes:
  <out>/blind/RUN-A.report.md ...  anonymized copies, shuffled, identical schema
  <out>/key.json                   strict JSON mapping RUN-X -> harness
Stdout prints ONLY the blinded names — the mapping is never echoed to the console.

--scrub replaces each report's own harness name / run-dir path with «scrubbed» so the
label cannot leak through the text (a real failure observed in the validation run).
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path


def collect(runs: Path):
    pairs = []
    for child in sorted(runs.iterdir()):
        if child.is_dir():
            r = child / "report.md"
            if r.exists():
                pairs.append((child.name, r))
        elif child.name.endswith(".report.md"):
            pairs.append((child.name[: -len(".report.md")], child))
    return pairs


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Anonymize run reports for blind selection.")
    ap.add_argument("--runs", required=True, help="runs dir containing per-harness reports")
    ap.add_argument("--out", required=True, help="selection dir to write blind/ + key.json")
    ap.add_argument("--seed", type=int, default=None, help="shuffle seed (reproducible)")
    ap.add_argument("--scrub", action="store_true",
                    help="replace harness names / run-dir paths inside report text")
    a = ap.parse_args()

    runs, out = Path(a.runs), Path(a.out)
    if not runs.is_dir():
        print(f"ERROR: runs dir not found: {runs}", file=sys.stderr)
        return 2
    pairs = collect(runs)
    if len(pairs) < 2:
        print("ERROR: need >= 2 reports to blind", file=sys.stderr)
        return 2

    blind = out / "blind"
    blind.mkdir(parents=True, exist_ok=True)
    rng = random.Random(a.seed)
    order = list(range(len(pairs)))
    rng.shuffle(order)

    letters = [chr(ord("A") + i) for i in range(len(pairs))]
    key = {}
    for slot, idx in enumerate(order):
        name, path = pairs[idx]
        run_id = f"RUN-{letters[slot]}"
        text = path.read_text(encoding="utf-8", errors="replace")
        if a.scrub:
            run_dir = path.parent.resolve()
            patterns = {name, str(run_dir), path.parent.name}
            for pat in patterns:
                if pat:
                    text = re.sub(re.escape(pat), "«scrubbed»", text)
        (blind / f"{run_id}.report.md").write_text(text, encoding="utf-8")
        key[run_id] = {"harness": name, "source": str(path)}

    (out / "key.json").write_text(
        json.dumps(key, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"blinded {len(pairs)} reports -> {blind}")
    for f in sorted(blind.iterdir()):
        print(f"  {f.name}")
    print(f"key (SEALED until ranking.md is written): {out / 'key.json'}")
    print("next: write ranking.md FIRST, only then open key.json (rule 4/5)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
