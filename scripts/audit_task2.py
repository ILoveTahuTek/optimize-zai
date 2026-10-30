"""Task-2 external audit: base harness vs adopted c1 harness against sealed ground truth."""
import json
import re
from pathlib import Path

LAB = Path("/home/z/my-project/harness-lab")
GT = json.loads(Path("/home/z/my-project/scripts/gt_sealed/ground_truth.json").read_text())
gt = GT["sales-2025h2"]
print(
    "GROUND TRUTH (task 2):",
    json.dumps(
        {
            k: gt[k]
            for k in ("net_revenue", "gross_revenue", "refunds_total", "duplicate_rows", "missing_region_rows", "top_product", "zero_unit_rows", "n_rows_raw", "n_rows_unique")
        }
    ),
)


def audit(label: str) -> int:
    text = (LAB / f"runs/sales-2025h2/{label}/report.md").read_text()
    low = text.lower()
    checks = {
        "net_revenue_correct": f"{gt['net_revenue']:,.2f}" in text,
        "gross_correct": f"{gt['gross_revenue']:,.2f}" in text,
        "refund_total_correct": f"{gt['refunds_total']:,.2f}" in text,
        "row_identity_correct": bool(re.search(rf"{gt['n_rows_raw']}[^0-9]+{gt['n_rows_unique']}", text)) and "6" in text,
        "top_product_named": gt["top_product"].lower() in low,
        "outlier_flagged": "250,000" in text and any(w in low for w in ("outlier", "wholesale", "largest", "bulk", "unusual")),
        "zero_row_flagged": "zero" in low and ("0902" in text or "zero-amount" in low or "zero unit" in low or "zero-unit" in low),
        "has_verification_section": "verification" in low,
        "explicit_definitions": ("net" in low and "gross" in low and "=" in text),
        "missing_region_counted": str(gt["missing_region_rows"]) in text,
    }
    passed = sum(checks.values())
    print(f"\n{label}: {passed}/{len(checks)}")
    for k, v in checks.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    return passed


scores = {lab: audit(lab) for lab in ("base", "c1")}
print("\n=== AUDIT SCOREBOARD (task 2) ===")
for lab, s in sorted(scores.items(), key=lambda kv: -kv[1]):
    print(f"  {lab:5s} {s}/10")
