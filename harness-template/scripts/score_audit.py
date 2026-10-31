#!/usr/bin/env python3
"""Post-selection audit scoring (PROTOCOL.md section 3, step 7).

Run ONLY after selection/ranking.md exists — audit results never modify candidates
mid-loop (rule 7).

Usage:
  python3 score_audit.py --checklist audit/checklist.json \
                         --answers   audit/answers.json \
                         --out       audit/scores.md

checklist.json: {"checks": [{"id": "c1", "desc": "...", "weight": 1}, ...]}
answers.json:   {"<harness>": {"c1": 1.0, "c2": 0.5, ...}}   # 1=pass 0.5=partial 0=fail

Writes a markdown table (raw / max / %), sorted by score. Ties keep checklist order.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="Weighted checklist audit scoring.")
    ap.add_argument("--checklist", required=True)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    cl = json.loads(Path(a.checklist).read_text(encoding="utf-8"))
    ans = json.loads(Path(a.answers).read_text(encoding="utf-8"))
    checks = cl.get("checks", [])
    if not checks:
        print("ERROR: checklist has no checks", file=sys.stderr)
        return 2
    wmap = {c["id"]: float(c.get("weight", 1)) for c in checks}
    unknown = sorted({cid for marks in ans.values() for cid in marks} - set(wmap))
    if unknown:
        print(f"WARN: answers reference unknown check ids (ignored): {unknown}")
    total = sum(wmap.values())
    if total <= 0:
        print("ERROR: checklist total weight must be > 0", file=sys.stderr)
        return 2

    rows = []
    for harness, marks in ans.items():
        if harness.startswith("_"):
            continue  # metadata keys like "_comment"
        if not isinstance(marks, dict):
            print(f"WARN: answers['{harness}'] is not a mapping; skipped")
            continue
        raw = sum(wmap.get(cid, 0.0) * float(v) for cid, v in marks.items())
        rows.append((harness, raw))
    rows.sort(key=lambda r: -r[1])

    lines = [
        "# Audit scores",
        "",
        f"checklist: `{a.checklist}` · max raw = {total:g} · post-selection only (rule 7)",
        "",
        "| harness | raw | score | % |",
        "|---|---|---|---|",
    ]
    for h, raw in rows:
        lines.append(f"| {h} | {raw:g} | {raw:g}/{total:g} | {raw / total * 100:.1f}% |")
    lines += ["", "Ties keep checklist order; the delta vs base is the harness gain."]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
