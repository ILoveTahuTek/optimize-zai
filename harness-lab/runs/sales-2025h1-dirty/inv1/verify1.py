#!/usr/bin/env python3
"""Verification script 1: pure stdlib (csv module), manual loops, no pandas.

Definitions (per INSTRUCTIONS.md), all computed over UNIQUE rows
(exact duplicate rows removed):
  NET revenue   = sum(amount) over unique rows (negatives included)
  GROSS revenue = sum of positive amounts over unique rows
  Refund total  = sum(|negative amounts|) over unique rows
"""
import csv
from collections import defaultdict
from decimal import Decimal

PATH = "/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv"

with open(PATH, newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

raw_count = len(rows)

# --- exact duplicate detection: full-row tuple identity, keep first occurrence
seen = set()
unique_rows = []
dup_rows = []
for r in rows:
    key = tuple(r[k] for k in ("order_id", "date", "product", "units",
                               "unit_price", "region", "amount"))
    if key in seen:
        dup_rows.append(r)
    else:
        seen.add(key)
        unique_rows.append(r)

uniq_count = len(unique_rows)
dup_count = len(dup_rows)

# --- money figures over unique rows
net = Decimal("0")
gross = Decimal("0")
refund = Decimal("0")
neg_count = 0
zero_amount_rows = []
for r in unique_rows:
    a = Decimal(r["amount"])
    net += a
    if a > 0:
        gross += a
    elif a < 0:
        refund += -a
        neg_count += 1
    else:
        zero_amount_rows.append(r)

# --- missing-field rows (any empty cell) over unique rows
missing_rows = [r for r in unique_rows
                if any((v is None or v.strip() == "") for v in r.values())]
# also count missing on raw rows for reference
missing_raw = [r for r in rows
               if any((v is None or v.strip() == "") for v in r.values())]

# --- monthly revenue (net) over unique rows
def month_of(datestr):
    d = datestr.strip()
    if "/" in d:  # DD/MM/YYYY variant
        dd, mm, yy = d.split("/")
        return f"{yy}-{mm}"
    return d[:7]  # YYYY-MM-DD

monthly = defaultdict(Decimal)
monthly_gross = defaultdict(Decimal)
monthly_refund = defaultdict(Decimal)
for r in unique_rows:
    m = month_of(r["date"])
    a = Decimal(r["amount"])
    monthly[m] += a
    if a > 0:
        monthly_gross[m] += a
    elif a < 0:
        monthly_refund[m] += -a

# --- product aggregation over unique rows
prod_rev_net = defaultdict(Decimal)
prod_rev_gross = defaultdict(Decimal)
prod_units_sold = defaultdict(int)      # units on positive-amount rows
prod_units_abs = defaultdict(int)       # units on all rows (net of returns, abs view)
prod_units_allrows = defaultdict(int)   # units as listed (incl. refund rows)
for r in unique_rows:
    p = r["product"]
    a = Decimal(r["amount"])
    u = int(r["units"])
    prod_rev_net[p] += a
    if a > 0:
        prod_rev_gross[p] += a
        prod_units_sold[p] += u
    else:
        prod_units_allrows[p] += u
    prod_units_abs[p] += abs(u)

# --- sanity: amount vs units*unit_price mismatch check
mismatch = []
for r in unique_rows:
    expected = Decimal(r["units"]) * Decimal(r["unit_price"])
    if abs(expected) != abs(Decimal(r["amount"])):
        mismatch.append((r["order_id"], r["units"], r["unit_price"], r["amount"], str(expected)))
    elif (Decimal(r["units"]) > 0 and Decimal(r["amount"]) < 0) or (Decimal(r["units"]) < 0):
        pass  # refund convention: negative amount, positive units — not a mismatch

# refund rows: negative amount, positive units — expected = units*price, amount = -expected
refund_convention_bad = []
for r in unique_rows:
    a = Decimal(r["amount"])
    exp = Decimal(r["units"]) * Decimal(r["unit_price"])
    if a < 0 and a != -exp:
        refund_convention_bad.append((r["order_id"], str(a), str(exp)))

# --- duplicate order_ids whose rows differ (partial duplicates)
by_id = defaultdict(list)
for r in unique_rows:
    by_id[r["order_id"]].append(r)
conflicting_ids = {oid: v for oid, v in by_id.items() if len(v) > 1}

# --- price variation per product
prices = defaultdict(set)
for r in unique_rows:
    prices[r["product"]].add(r["unit_price"])

print("=== SCRIPT 1 (stdlib csv) ===")
print(f"raw data rows: {raw_count}")
print(f"unique rows: {uniq_count}")
print(f"exact duplicate rows: {dup_count}")
print(f"identity ok: {raw_count == uniq_count + dup_count}")
print(f"NET revenue (unique rows): {net}")
print(f"GROSS revenue (unique rows): {gross}")
print(f"Refund total (unique rows): {refund}")
print(f"negative-amount rows (unique): {neg_count}")
print(f"zero-amount rows (unique): {len(zero_amount_rows)} {[r['order_id'] for r in zero_amount_rows]}")
print(f"rows with missing fields (unique): {len(missing_rows)} -> {[r['order_id'] for r in missing_rows]}")
print(f"rows with missing fields (raw): {len(missing_raw)}")
print("dup rows detail:")
for r in dup_rows:
    print("  DUP:", r["order_id"], r["date"], r["product"], r["amount"])
print("monthly (NET | gross | refunds):")
for m in sorted(monthly):
    print(f"  {m}: net={monthly[m]} gross={monthly_gross[m]} refunds={monthly_refund[m]}")
print("product by NET revenue:", {k: str(v) for k, v in sorted(prod_rev_net.items(), key=lambda kv: -kv[1])})
print("product by GROSS revenue:", {k: str(v) for k, v in sorted(prod_rev_gross.items(), key=lambda kv: -kv[1])})
print("product by units sold (positive rows):", dict(sorted(prod_units_sold.items(), key=lambda kv: -kv[1])))
print("product by |units| all rows:", dict(sorted(prod_units_abs.items(), key=lambda kv: -kv[1])))
print("amount != |units*unit_price| mismatches:", mismatch)
print("refund rows violating -units*price:", refund_convention_bad)
print("order_ids repeated with differing rows (in unique set):", conflicting_ids)
print("unit_price values per product:", {k: sorted(v) for k, v in prices.items()})
