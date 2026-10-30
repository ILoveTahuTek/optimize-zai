"""Task-3 (k=2) audit: unmask selection key, audit all 7 reports vs sealed ground truth."""
import json
import re
from pathlib import Path

LAB = Path("/home/z/my-project/harness-lab")
raw = (LAB / "selection2/key.txt").read_text()
key = eval(raw.strip())  # key.txt holds a dict literal written by us
print("KEY:", key)
choice = "cand_5"
print(f"SELECTED: {choice} -> {key[choice]}\n")

gt = json.loads((Path("/home/z/my-project/scripts/gt_sealed") / "ground_truth_h3.json").read_text())
print(
    "SEALED TRUTH:",
    json.dumps(
        {
            "net": gt["net_revenue"],
            "gross": gt["gross_revenue"],
            "refunds": gt["refunds_total"],
            "dupes": gt["duplicate_rows"],
            "raw/unique": f"{gt['n_rows_raw']}/{gt['n_rows_unique']}",
            "top": gt["top_product"],
            "zero": gt["zero_ids"],
            "dmy_rows": gt["dmy_format_rows"],
            "price_changes": gt["price_changes"],
        }
    ),
)


def audit(label: str) -> int:
    text = (LAB / f"runs/sales-2025h1-dirty/{label}/report.md").read_text()
    low = text.lower()
    checks = {
        "net_correct": f"{gt['net_revenue']:,.2f}" in text,
        "gross_correct": f"{gt['gross_revenue']:,.2f}" in text,
        "refund_total_correct": f"{gt['refunds_total']:,.2f}" in text,
        "row_identity": bool(re.search(rf"{gt['n_rows_raw']}[^0-9]+{gt['n_rows_unique']}", text)) and f"{gt['duplicate_rows']}" in text,
        "top_product": gt["top_product"].lower() in low,
        "zero_row_flagged": "zero" in low and ("1001" in text or "zero-amount" in low or "zero-unit" in low or "zero unit" in low),
        "date_format_anomaly": bool(re.search(r"\d{1,2}/\d{2}/\d{4}", text)) or "dd/mm" in low or "non-iso" in low or "0071" in text,
        "price_change_flagged": "210" in text and "220" in text and any(w in low for w in ("change", "rose", "increas", "step", "→", "->")),
        "has_verification_section": "verification" in low,
        "explicit_definitions": ("net" in low and "gross" in low and "=" in text),
    }
    passed = sum(checks.values())
    print(f"\n{label}: {passed}/10")
    for k, v in checks.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    return passed


scores = {lab: audit(lab) for lab in ("base", "inv1", "dom1", "inv2", "dom2", "agg1", "agg2")}
print("\n=== SCOREBOARD task-3 (k=2) ===")
for lab, s in sorted(scores.items(), key=lambda kv: -kv[1]):
    print(f"  {lab:5s} {s}/10")
print(f"\nselection matched best? selected->{key[choice]}  best={max(scores, key=scores.get)}")
