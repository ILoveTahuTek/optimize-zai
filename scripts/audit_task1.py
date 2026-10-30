"""Unmask the selection key, then audit every task-1 report against the sealed ground truth."""
import json
import re
from pathlib import Path

LAB = Path("/home/z/my-project/harness-lab")

pairs = re.findall(r"'(cand_\d)': '(\w+)'", (LAB / "selection/key.json").read_text())
key = dict(pairs)
print("KEY:", key)
choice = "cand_1"
print(f"SELECTED: {choice} -> {key[choice]}\n")

gt = json.loads((LAB / "ground_truth.json").read_text())["sales-2025h1"]
print(
    "GROUND TRUTH:",
    json.dumps(
        {
            k: gt[k]
            for k in ("net_revenue", "gross_revenue", "refunds_total", "duplicate_rows", "missing_region_rows", "top_product")
        }
    ),
)


def audit(label: str) -> int:
    text = (LAB / f"runs/sales-2025h1/{label}/report.md").read_text()
    checks = {
        "net_revenue_correct": f"{gt['net_revenue']:,.2f}" in text or f"{gt['net_revenue']:.2f}" in text,
        "gross_correct": f"{gt['gross_revenue']:,.2f}" in text,
        "refund_total_correct": f"{gt['refunds_total']:,.2f}" in text or f"{gt['refunds_total']:.2f}" in text,
        "dupes_count_correct": str(gt["duplicate_rows"]) in text,
        "top_product_named": gt["top_product"].lower() in text.lower(),
        "no_gross_mislabeled_as_net": not ("net sales" in text.lower() and "49,015" in text),
        "has_verification_section": "verification" in text.lower(),
        "explicit_definitions": ("net" in text.lower() and "gross" in text.lower() and "=" in text),
    }
    passed = sum(checks.values())
    print(f"\n{label}: {passed}/{len(checks)}")
    for k, v in checks.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    return passed


scores = {lab: audit(lab) for lab in ("base", "inv1", "dom1", "c1")}
print("\n=== AUDIT SCOREBOARD (task 1) ===")
for lab, s in sorted(scores.items(), key=lambda kv: -kv[1]):
    print(f"  {lab:5s} {s}/8")
print(f"\nselection matched best? selected->{key[choice]}  best={max(scores, key=scores.get)}")
