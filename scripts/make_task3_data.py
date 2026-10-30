"""Task-3 dataset: sales-2025h1-dirty.csv — new trap classes beyond tasks 1-2.

Traps:
  - 10 exact duplicate rows (incl. 1 duplicated refund row)
  - 6 unique refund rows (negative amounts)
  - 1 zero-amount row (units 0)
  - ~7 rows missing region
  - ~6 rows with DD/MM/YYYY date format mixed into ISO dates (monthly-grouping trap)
  - Monitor price changes 210.00 -> 220.00 from 2025-05-01 (price-constancy trap)

Ground truth is written straight to the sealed dir and its values are NEVER printed here.
"""
import csv
import json
import random
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

LAB = Path("/home/z/my-project/harness-lab")
GT_DIR = Path("/home/z/my-project/scripts/gt_sealed")
random.seed(99)

PRICES = {"Keyboard": Decimal("45.00"), "Headset": Decimal("80.00"), "Monitor": Decimal("210.00"), "Laptop": Decimal("1250.00")}
REGIONS = ["Jakarta", "Bandung", "Surabaya", "Medan", "Denpasar"]


def iso_or_dmy(d: date, dmy: bool) -> str:
    return d.strftime("%d/%m/%Y") if dmy else d.isoformat()


rows: list[dict] = []
for i in range(1, 131):
    product = random.choices(list(PRICES), weights=[35, 28, 27, 10])[0]
    units = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 15, 10, 5])[0]
    refund = random.random() < 0.046
    d = date(2025, 1, 1) + timedelta(days=random.randint(0, 180))
    price = PRICES[product]
    if product == "Monitor" and d >= date(2025, 5, 1):
        price = Decimal("220.00")
    amount = -price * units if refund else price * units
    dmy = random.random() < 0.05 and not refund
    rows.append(
        {
            "order_id": f"ORD-{i:04d}",
            "date": iso_or_dmy(d, dmy),
            "product": product,
            "units": str(units),
            "unit_price": f"{price:.2f}",
            "region": random.choice(REGIONS) if random.random() > 0.055 else "",
            "amount": f"{amount:.2f}",
        }
    )
rows.append({"order_id": "ORD-1001", "date": "2025-04-02", "product": "Headset", "units": "0", "unit_price": "80.00", "region": "Medan", "amount": "0.00"})

dupes = [dict(rows[i]) for i in random.sample(range(len(rows)), 10)]
full = rows + dupes
random.shuffle(full)


def parse_date(s: str):
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


(LAB / "tasks" / "sales-2025h1-dirty").mkdir(parents=True, exist_ok=True)
with open(LAB / "tasks" / "sales-2025h1-dirty" / "sales.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(full[0]))
    w.writeheader()
    w.writerows(full)

# ground truth (sealed; robust date parsing)
seen, unique, dup_count = set(), [], 0
for r in full:
    key = tuple(sorted(r.items()))
    if key in seen:
        dup_count += 1
        continue
    seen.add(key)
    unique.append(r)

net = sum((Decimal(r["amount"]) for r in unique), Decimal(0))
gross = sum((Decimal(r["amount"]) for r in unique if Decimal(r["amount"]) > 0), Decimal(0))
refunds = sum((-Decimal(r["amount"]) for r in unique if Decimal(r["amount"]) < 0), Decimal(0))
missing = sum(1 for r in unique if not r["region"].strip())
zeros = [r["order_id"] for r in unique if Decimal(r["amount"]) == 0]
dmy_rows = [r["order_id"] for r in unique if "/" in r["date"]]

by_prod: dict[str, Decimal] = defaultdict(lambda: Decimal(0))
by_month: dict[str, Decimal] = defaultdict(lambda: Decimal(0))
prices_by_prod: dict[str, set] = defaultdict(set)
for r in unique:
    amt = Decimal(r["amount"])
    by_prod[r["product"]] += amt
    d = parse_date(r["date"])
    by_month[d.strftime("%Y-%m") if d else "UNPARSED"] += amt
    if amt > 0:
        prices_by_prod[r["product"]].add(str(Decimal(r["unit_price"])))

price_changes = {p: sorted(v) for p, v in prices_by_prod.items() if len(v) > 1}

truth = {
    "net_revenue": float(net),
    "gross_revenue": float(gross),
    "refunds_total": float(refunds),
    "duplicate_rows": dup_count,
    "missing_region_rows": missing,
    "zero_ids": zeros,
    "dmy_format_rows": dmy_rows,
    "top_product": max(by_prod, key=by_prod.get),
    "monthly_net": {k: float(v) for k, v in sorted(by_month.items())},
    "price_changes": price_changes,
    "n_rows_raw": len(full),
    "n_rows_unique": len(unique),
}
GT_DIR.mkdir(parents=True, exist_ok=True)
(GT_DIR / "ground_truth_h3.json").write_text(json.dumps(truth, indent=2))
print(f"rows raw={len(full)} unique={len(unique)} dupes={dup_count} | truth sealed, values not shown")
