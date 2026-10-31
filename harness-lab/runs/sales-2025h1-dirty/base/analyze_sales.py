#!/usr/bin/env python3
"""Analysis of sales-2025h1-dirty CSV. Pure stdlib; no pandas dependency."""
import csv
from collections import Counter, defaultdict
from datetime import datetime

PATH = "/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv"

rows = []
with open(PATH, newline="") as f:
    reader = csv.DictReader(f)
    for i, r in enumerate(reader, start=2):  # line number in file
        r["_line"] = i
        rows.append(r)

print(f"Data rows (excl. header): {len(rows)}")

# ---------- 1. Date parsing / normalization ----------
def parse_date(s):
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None

date_anomalies = []
for r in rows:
    d = parse_date(r["date"])
    r["_date"] = d
    if d is None:
        date_anomalies.append((r["_line"], r["order_id"], r["date"]))
    elif r["date"].strip() != d.isoformat():
        date_anomalies.append((r["_line"], r["order_id"], f"{r['date']} -> normalized {d.isoformat()}"))
print(f"\nNon-ISO date rows (normalized): {date_anomalies}")

# ---------- 2. Duplicates ----------
seen_exact = {}
exact_dupes = []
for r in rows:
    key = (r["order_id"], r["date"], r["product"], r["units"], r["unit_price"], r["region"], r["amount"])
    if key in seen_exact:
        exact_dupes.append((r["_line"], seen_exact[key], r["order_id"]))
    else:
        seen_exact[key] = r["_line"]
print(f"\nExact duplicate rows (line, first-seen line, order_id): {exact_dupes}")

# same order_id appearing more than once with DIFFERENT content?
by_oid = defaultdict(list)
for r in rows:
    by_oid[r["order_id"]].append(r["_line"])
conflicting = {oid: lines for oid, lines in by_oid.items() if len(lines) > 1 and oid not in {d[2] for d in exact_dupes}}
print(f"order_ids repeated with conflicting content: {conflicting}")

# dedupe: keep first occurrence
kept, dropped_lines = [], set()
for r in rows:
    key = (r["order_id"], r["date"], r["product"], r["units"], r["unit_price"], r["region"], r["amount"])
    if key in seen_exact and seen_exact[key] != r["_line"]:
        dropped_lines.add(r["_line"])
        continue
    kept.append(r)
print(f"Rows kept after dedupe: {len(kept)} (dropped {len(dropped_lines)} exact duplicates)")

# ---------- 3. Arithmetic consistency: amount == units * unit_price ----------
mismatches = []
for r in kept:
    expected = round(float(r["units"]) * float(r["unit_price"]), 2)
    actual = round(float(r["amount"]), 2)
    if abs(expected - actual) > 0.005 and not (abs(expected) == abs(actual) and actual < 0):
        mismatches.append((r["_line"], r["order_id"], r["units"], r["unit_price"], r["amount"], expected))
    elif actual < 0 and abs(expected) != abs(actual):
        mismatches.append((r["_line"], r["order_id"], r["units"], r["unit_price"], r["amount"], expected))
print(f"\nAmount != |units*price| mismatches: {mismatches}")

# negative amounts (refunds?) and zero-unit rows
negatives = [(r["_line"], r["order_id"], r["product"], r["units"], r["amount"]) for r in kept if float(r["amount"]) < 0]
zeros = [(r["_line"], r["order_id"], r["product"], r["units"], r["amount"]) for r in kept if float(r["units"]) == 0]
print(f"Negative amounts (refunds): {len(negatives)}")
for n in negatives: print("   ", n)
print(f"Zero-unit rows: {zeros}")

# negative amounts where units are positive -> sign-only anomaly
neg_units_pos = [n for n in negatives if int(n[3]) > 0]
print(f"Negative amounts with positive units (pure sign anomalies / refunds): {len(neg_units_pos)}")

# ---------- 4. Missing regions ----------
missing_region = [(r["_line"], r["order_id"]) for r in kept if not r["region"].strip()]
print(f"\nMissing region rows: {missing_region}")

# ---------- 5. Price consistency per product ----------
price_by_product = defaultdict(set)
for r in kept:
    price_by_product[r["product"]].add(float(r["unit_price"]))
print(f"\nUnit prices per product: {dict(price_by_product)}")

# when did monitor price change 210 -> 220?
mon = sorted([(r["_date"], r["unit_price"], r["order_id"]) for r in kept if r["product"] == "Monitor"])
last210 = max([m for m in mon if m[1] == "210.00"], default=None)
first220 = min([m for m in mon if m[1] == "220.00"], default=None)
print(f"Monitor @210 last seen: {last210[0] if last210 else None}; Monitor @220 first seen: {first220[0] if first220 else None}")

# ---------- 6. Metrics on deduplicated data ----------
# Net amounts (as recorded), plus gross/refund split
net_total = sum(float(r["amount"]) for r in kept)
gross = sum(float(r["amount"]) for r in kept if float(r["amount"]) > 0)
refunds = sum(float(r["amount"]) for r in kept if float(r["amount"]) < 0)
print(f"\nNET total revenue: {net_total:.2f}")
print(f"Gross (positive rows): {gross:.2f} | Refund rows total: {refunds:.2f}")

# monthly
monthly = defaultdict(float)
monthly_gross = defaultdict(float)
for r in kept:
    if r["_date"]:
        m = r["_date"].strftime("%Y-%m")
        monthly[m] += float(r["amount"])
        if float(r["amount"]) > 0:
            monthly_gross[m] += float(r["amount"])
print("\nMonthly net revenue:")
for m in sorted(monthly):
    print(f"  {m}: net {monthly[m]:>10.2f}   gross {monthly_gross[m]:>10.2f}")

# product ranking: net revenue and units
prod_rev = defaultdict(float)
prod_units = defaultdict(int)
prod_units_gross = defaultdict(int)
for r in kept:
    amt = float(r["amount"])
    prod_rev[r["product"]] += amt
    prod_units[r["product"]] += int(r["units"])
    if amt > 0:
        prod_units_gross[r["product"]] += int(r["units"])
print("\nProduct net revenue:")
for p, v in sorted(prod_rev.items(), key=lambda x: -x[1]):
    print(f"  {p}: {v:.2f}")
print("Product units (all rows incl. refund rows' units):")
for p, v in sorted(prod_units.items(), key=lambda x: -x[1]):
    print(f"  {p}: {v}")
print("Product units (positive-amount rows only):")
for p, v in sorted(prod_units_gross.items(), key=lambda x: -x[1]):
    print(f"  {p}: {v}")

# order counts per product (deduped)
prod_orders = Counter(r["product"] for r in kept)
print("\nOrder count per product:", dict(prod_orders))

# region
region_rev = defaultdict(float)
for r in kept:
    region_rev[r["region"].strip() or "(missing)"] += float(r["amount"])
print("\nRevenue by region:")
for g, v in sorted(region_rev.items(), key=lambda x: -x[1]):
    print(f"  {g}: {v:.2f}")

# top single orders
top = sorted(kept, key=lambda r: -float(r["amount"]))[:5]
print("\nTop 5 orders by amount:")
for r in top:
    print(f"  {r['order_id']} {r['_date']} {r['product']} x{r['units']} = {r['amount']} ({r['region']})")
