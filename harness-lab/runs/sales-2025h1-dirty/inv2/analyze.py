#!/usr/bin/env python3
"""Analysis of sales-2025h1-dirty/sales.csv for inv2 report.
Prints a structured audit so every judgment call is quantified.
"""
import csv
from collections import defaultdict
from datetime import datetime, date

PATH = "/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv"

rows = []
with open(PATH, newline="") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=2):  # i = physical line number in file
        row["_line"] = i
        rows.append(row)

print(f"data rows (raw): {len(rows)}")

# ---------- date parsing: ISO default; slash dates parsed day-first ----------
def parse_date(s):
    s = s.strip()
    if "/" in s:
        return datetime.strptime(s, "%d/%m/%Y").date(), "slash-dayfirst"
    return datetime.strptime(s, "%Y-%m-%d").date(), "iso"

slash_rows, bad_dates = [], []
for r in rows:
    try:
        r["_date"], style = parse_date(r["date"])
        if style == "slash-dayfirst":
            slash_rows.append((r["_line"], r["order_id"], r["date"]))
    except ValueError:
        bad_dates.append((r["_line"], r["order_id"], r["date"]))

print(f"\nslash-format dates parsed day-first: {len(slash_rows)}")
for ln, oid, d in slash_rows:
    print(f"  line {ln}: {oid} '{d}'")
print(f"unparseable dates: {len(bad_dates)}")
for ln, oid, d in bad_dates:
    print(f"  line {ln}: {oid} '{d}'")

date_min = min(r["_date"] for r in rows)
date_max = max(r["_date"] for r in rows)
print(f"date range: {date_min} .. {date_max}")

# ---------- exact duplicates (full-row identical) ----------
seen = {}
dups = []  # (line, order_id, amount) for repeat occurrences
for r in rows:
    key = (r["order_id"], r["date"].strip(), r["product"].strip(), r["units"].strip(),
           r["unit_price"].strip(), r["region"].strip(), r["amount"].strip())
    if key in seen:
        dups.append((r["_line"], r["order_id"], r["amount"], seen[key]))
    else:
        seen[key] = r["_line"]

print(f"\nexact duplicate rows (repeats removed): {len(dups)}")
dup_amount_sum = 0.0
for ln, oid, amt, first_ln in dups:
    print(f"  line {ln}: {oid} amount {amt} (first seen line {first_ln})")
    dup_amount_sum += float(amt)
print(f"sum of amounts on duplicate rows: {dup_amount_sum:.2f}")

# order_id conflicts: same order_id, different content
by_oid = defaultdict(list)
for r in rows:
    by_oid[r["order_id"]].append(r)
conflicts = {oid: rs for oid, rs in by_oid.items()
             if len({(x["date"], x["product"], x["units"], x["unit_price"], x["region"], x["amount"]) for x in rs}) > 1}
print(f"order_ids with conflicting content: {len(conflicts)}")
for oid in conflicts:
    print(f"  {oid}")

# ---------- unique dataset ----------
urows = []
removed = set(ln for ln, _, _, _ in dups)
for r in rows:
    if r["_line"] not in removed:
        urows.append(r)
print(f"\nunique rows: {len(urows)}")

# ---------- refunds (negative amounts) ----------
refunds = [r for r in urows if float(r["amount"]) < 0]
refund_total = sum(float(r["amount"]) for r in refunds)
print(f"\nrefund rows (negative amount, unique): {len(refunds)}  total: {refund_total:.2f}")
for r in refunds:
    amt, units, price = float(r["amount"]), int(r["units"]), float(r["unit_price"])
    match = abs(amt) == units * price
    print(f"  line {r['_line']}: {r['order_id']} {r['_date']} {r['product']} units={units} "
          f"unit_price={price:.2f} amount={amt:.2f} |units*price|==|amount|: {match}")

# ---------- arithmetic consistency: amount == units * unit_price ----------
mismatch = []
for r in urows:
    amt, units, price = float(r["amount"]), int(r["units"]), float(r["unit_price"])
    if abs(amt) != abs(units * price):
        mismatch.append((r["_line"], r["order_id"], units, price, amt))
print(f"\nrows where |amount| != units*unit_price: {len(mismatch)}")
for m in mismatch:
    print(f"  {m}")

# zero-unit rows
zero = [r for r in urows if int(r["units"]) == 0]
print(f"\nzero-unit rows: {len(zero)}")
for r in zero:
    print(f"  line {r['_line']}: {r['order_id']} {r['_date']} {r['product']} amount={r['amount']}")

# missing region
missing_region = [r for r in urows if not r["region"].strip()]
print(f"\nrows with missing region (unique): {len(missing_region)}")
for r in missing_region:
    print(f"  line {r['_line']}: {r['order_id']} {r['_date']} {r['product']} amount={r['amount']}")

# ---------- headline metrics (unique rows) ----------
gross = sum(float(r["amount"]) for r in urows if float(r["amount"]) > 0)
net = sum(float(r["amount"]) for r in urows)
print(f"\nTOTAL gross sales (positive amounts only): {gross:.2f}")
print(f"TOTAL refunds (negative amounts):          {refund_total:.2f}")
print(f"TOTAL net revenue (gross + refunds):       {net:.2f}")
print(f"raw net sum over all 141 rows (dupes in):  {sum(float(r['amount']) for r in rows):.2f}")

# ---------- per-product ----------
prod = defaultdict(lambda: {"gross_units": 0, "refund_units": 0, "net_units": 0,
                            "net_rev": 0.0, "gross_rev": 0.0, "orders": 0, "prices": defaultdict(list)})
for r in urows:
    p = prod[r["product"].strip()]
    units, amt = int(r["units"]), float(r["amount"])
    p["orders"] += 1
    if amt > 0:
        p["gross_units"] += units
        p["gross_rev"] += amt
    else:
        p["refund_units"] += units
    p["net_units"] += units if amt > 0 else -units
    p["net_rev"] += amt
    p["prices"][float(r["unit_price"])].append(r["_date"])

print("\nper-product (unique rows):")
print(f"{'product':<10} {'orders':>6} {'grossU':>7} {'refU':>5} {'netU':>6} {'grossRev':>10} {'netRev':>10}  prices")
for name, d in sorted(prod.items(), key=lambda kv: -kv[1]["net_rev"]):
    prices = "; ".join(f"{pr:.2f} ({len(ds)} rows, {min(ds)}..{max(ds)})" for pr, ds in sorted(d["prices"].items()))
    print(f"{name:<10} {d['orders']:>6} {d['gross_units']:>7} {d['refund_units']:>5} {d['net_units']:>6} "
          f"{d['gross_rev']:>10.2f} {d['net_rev']:>10.2f}  {prices}")

# ---------- monthly ----------
monthly = defaultdict(lambda: {"net": 0.0, "gross": 0.0, "refunds": 0.0, "orders": 0})
for r in urows:
    m = r["_date"].strftime("%Y-%m")
    amt = float(r["amount"])
    monthly[m]["net"] += amt
    monthly[m]["orders"] += 1
    if amt > 0:
        monthly[m]["gross"] += amt
    else:
        monthly[m]["refunds"] += amt

print("\nmonthly (unique rows):")
print(f"{'month':<8} {'orders':>6} {'gross':>10} {'refunds':>9} {'net':>10}")
for m in sorted(monthly):
    d = monthly[m]
    print(f"{m:<8} {d['orders']:>6} {d['gross']:>10.2f} {d['refunds']:>9.2f} {d['net']:>10.2f}")

# ---------- regions ----------
reg = defaultdict(float)
for r in urows:
    reg[r["region"].strip() or "(missing)"] += float(r["amount"])
print("\nnet revenue by region (unique rows):")
for k, v in sorted(reg.items(), key=lambda kv: -kv[1]):
    print(f"  {k:<10} {v:>10.2f}")
