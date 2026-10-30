"""Generate the two sales CSVs (with deliberate data traps) + ground truth.

Task 1 (sales-2025h1): 8 exact duplicate rows, 5 refunds (negative), 4 missing regions.
Task 2 (sales-2025h2): 6 exact duplicates, 3 refunds, 5 missing regions,
                       1 bulk outlier order (200 units), 1 zero-unit cancelled row.
Ground truth is written to ground_truth.json and only consulted AFTER selection.
"""
import csv
import json
import random
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

LAB = Path("/home/z/my-project/harness-lab")
random.seed(42)

PRODUCTS = {
    "Keyboard": Decimal("45.00"),
    "Headset": Decimal("80.00"),
    "Monitor": Decimal("210.00"),
    "Laptop": Decimal("1250.00"),
}
REGIONS = ["Jakarta", "Bandung", "Surabaya", "Medan", "Denpasar"]


def rand_date(h1: bool) -> str:
    if h1:
        start = date(2025, 1, 1)
        d = start + timedelta(days=random.randint(0, 180))
    else:
        start = date(2025, 7, 1)
        d = start + timedelta(days=random.randint(0, 181))
    return d.isoformat()


def make_rows(h1: bool, n: int) -> list[dict]:
    rows = []
    for i in range(1, n + 1):
        product = random.choices(list(PRODUCTS), weights=[35, 30, 25, 10])[0]
        units = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 15, 10, 5])[0]
        refund = random.random() < 0.04
        amount = -PRODUCTS[product] * units if refund else PRODUCTS[product] * units
        rows.append(
            {
                "order_id": f"ORD-{i:04d}",
                "date": rand_date(h1),
                "product": product,
                "units": str(units),
                "unit_price": f"{PRODUCTS[product]:.2f}",
                "region": random.choice(REGIONS) if random.random() > 0.05 else "",
                "amount": f"{amount:.2f}",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def truth(rows: list[dict]) -> dict:
    seen, deduped, dupes = set(), [], 0
    for r in rows:
        key = tuple(r.items())
        if key in seen:
            dupes += 1
            continue
        seen.add(key)
        deduped.append(r)
    net = sum((Decimal(r["amount"]) for r in deduped), Decimal(0))
    gross = sum((Decimal(r["amount"]) for r in deduped if Decimal(r["amount"]) > 0), Decimal(0))
    refunds = sum((-Decimal(r["amount"]) for r in deduped if Decimal(r["amount"]) < 0), Decimal(0))
    missing_region = sum(1 for r in deduped if not r["region"])
    by_prod: dict[str, Decimal] = defaultdict(lambda: Decimal(0))
    by_month: dict[str, Decimal] = defaultdict(lambda: Decimal(0))
    for r in deduped:
        amt = Decimal(r["amount"])
        by_prod[r["product"]] += amt
        by_month[r["date"][:7]] += amt
    top = max(by_prod, key=by_prod.get)
    return {
        "net_revenue": float(net),
        "gross_revenue": float(gross),
        "refunds_total": float(refunds),
        "duplicate_rows": dupes,
        "missing_region_rows": missing_region,
        "top_product": top,
        "top_product_revenue": float(by_prod[top]),
        "monthly_net": {k: float(v) for k, v in sorted(by_month.items())},
        "n_rows_raw": len(rows),
        "n_rows_unique": len(deduped),
    }


# ---- Task 1 ----
rows1 = make_rows(True, 120)
dupes1 = [dict(rows1[i]) for i in random.sample(range(len(rows1)), 8)]
rows1_full = rows1 + dupes1
random.shuffle(rows1_full)
write_csv(LAB / "tasks" / "sales-2025h1" / "sales.csv", rows1_full)
t1 = truth(rows1_full)

# ---- Task 2: different quirks ----
rows2 = make_rows(False, 110)
dupes2 = [dict(rows2[i]) for i in random.sample(range(len(rows2)), 6)]
# one bulk outlier + one cancelled zero-unit row
rows2.append(
    {
        "order_id": "ORD-0901",
        "date": "2025-09-14",
        "product": "Laptop",
        "units": "200",
        "unit_price": "1250.00",
        "region": "Jakarta",
        "amount": "250000.00",
    }
)
rows2.append(
    {
        "order_id": "ORD-0902",
        "date": "2025-08-03",
        "product": "Headset",
        "units": "0",
        "unit_price": "80.00",
        "region": "Bandung",
        "amount": "0.00",
    }
)
rows2_full = rows2 + dupes2
random.shuffle(rows2_full)
write_csv(LAB / "tasks" / "sales-2025h2" / "sales.csv", rows2_full)
t2 = truth(rows2_full)
t2["bulk_outlier"] = {"order_id": "ORD-0901", "amount": 250000.0}
t2["zero_unit_rows"] = 1

(LAB / "ground_truth.json").write_text(json.dumps({"sales-2025h1": t1, "sales-2025h2": t2}, indent=2))
print("task1 rows:", len(rows1_full), "| task2 rows:", len(rows2_full))
print("ground_truth.json written (sealed until after selection)")
