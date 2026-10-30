#!/usr/bin/env python3
"""Sales analysis for /home/z/my-project/harness-lab/tasks/sales-2025h2/sales.csv

Stdlib only. Prints a set of factual metrics to stdout:
- row counts, duplicate detection, validation of amount == units * unit_price
- totals (raw / deduplicated / ex-outlier variants)
- best-selling product by units and by revenue
- monthly revenue breakdown
- region breakdown
- data-quality flags
"""
import csv
from collections import defaultdict
from datetime import datetime

CSV_PATH = "/home/z/my-project/harness-lab/tasks/sales-2025h2/sales.csv"

rows = []
with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    for i, r in enumerate(reader, start=2):  # line 1 is header
        r["_line"] = i
        r["units"] = int(r["units"])
        r["unit_price"] = float(r["unit_price"])
        r["amount"] = float(r["amount"])
        r["_month"] = r["date"][:7]
        rows.append(r)

print(f"rows: {len(rows)}")
print(f"date range: {min(r['date'] for r in rows)} .. {max(r['date'] for r in rows)}")

# --- duplicate detection -------------------------------------------------
seen_full = {}
seen_id = {}
full_dups = []
id_dups = []
for r in rows:
    key = (r["order_id"], r["date"], r["product"], r["units"], r["unit_price"], r["region"], r["amount"])
    if key in seen_full:
        full_dups.append((r["_line"], seen_full[key], r["order_id"]))
    else:
        seen_full[key] = r["_line"]
    if r["order_id"] in seen_id and seen_id[r["order_id"]] not in [d[1] for d in full_dups if d[2] == r["order_id"]]:
        pass  # handled below via full_dups check
    seen_id.setdefault(r["order_id"], r["_line"])

print(f"\nexact duplicate rows (dup_line, first_line, order_id): {full_dups}")

# deduplicated view: keep first occurrence of each full-row key
dedup = []
seen_keys = set()
for r in rows:
    key = (r["order_id"], r["date"], r["product"], r["units"], r["unit_price"], r["region"], r["amount"])
    if key in seen_keys:
        continue
    seen_keys.add(key)
    dedup.append(r)
print(f"deduplicated rows: {len(dedup)}")

# --- validation: amount vs units*unit_price ------------------------------
mismatches = [r for r in dedup if abs(r["units"] * r["unit_price"] - r["amount"]) > 0.005]
print(f"\nrows where amount != units*unit_price (after dedup): {len(mismatches)}")
for r in mismatches:
    print("  ", r["order_id"], r["units"], r["unit_price"], r["amount"])

# --- quality flags -------------------------------------------------------
negatives = [r for r in dedup if r["amount"] < 0]
zero_units = [r for r in dedup if r["units"] == 0]
missing_region = [r for r in dedup if not r["region"].strip()]
big_orders = [r for r in dedup if r["amount"] > 10000]
print(f"\nnegative amounts (possible refunds/returns): {[(r['order_id'], r['product'], r['units'], r['amount']) for r in negatives]}")
print(f"zero-unit rows: {[(r['order_id'], r['order_id'] and r['date'], r['product'], r['amount']) for r in zero_units]}")
print(f"rows with missing region: {len(missing_region)} -> {[r['order_id'] for r in missing_region]}")
print(f"large orders (>10k): {[(r['order_id'], r['product'], r['units'], r['amount']) for r in big_orders]}")

# next largest order ex-outlier
others = sorted((r["amount"] for r in dedup), reverse=True)
print(f"top 5 amounts after dedup: {others[:5]}")

# --- totals ---------------------------------------------------------------
raw_total = sum(r["amount"] for r in rows)
dedup_total = sum(r["amount"] for r in dedup)
outlier_ids = {r["order_id"] for r in big_orders}
ex_outlier = sum(r["amount"] for r in dedup if r["order_id"] not in outlier_ids)
net_of_refunds_ex_outlier = ex_outlier + sum(-r["amount"] for r in negatives)  # remove refund effect
print(f"\nTOTAL raw (all {len(rows)} rows, dupes included): {raw_total:,.2f}")
print(f"TOTAL deduplicated (unique orders, net of refunds): {dedup_total:,.2f}")
print(f"TOTAL deduplicated excluding order(s) {sorted(outlier_ids)}: {ex_outlier:,.2f}")
print(f"  of which refunds sum: {sum(r['amount'] for r in negatives):,.2f}")
print(f"  ex-outlier gross sales (refunds counted as +|amount|): {net_of_refunds_ex_outlier:,.2f}")

# --- product breakdown ----------------------------------------------------
def product_table(dataset, label):
    units_by_p = defaultdict(int)
    rev_by_p = defaultdict(int)
    orders_by_p = defaultdict(int)
    for r in dataset:
        units_by_p[r["product"]] += r["units"]
        rev_by_p[r["product"]] += r["amount"]
        orders_by_p[r["product"]] += 1
    print(f"\nPRODUCT BREAKDOWN ({label}): product | orders | units | revenue")
    for p in sorted(rev_by_p, key=rev_by_p.get, reverse=True):
        print(f"  {p:10s} | {orders_by_p[p]:3d} | {units_by_p[p]:5d} | {rev_by_p[p]:12,.2f}")

product_table(dedup, "deduplicated, all orders incl. outlier & refunds")
product_table([r for r in dedup if r["order_id"] not in outlier_ids], "deduplicated, ex-outlier")

# --- monthly breakdown ----------------------------------------------------
def monthly_table(dataset, label):
    rev = defaultdict(float)
    orders = defaultdict(int)
    for r in dataset:
        rev[r["_month"]] += r["amount"]
        orders[r["_month"]] += 1
    print(f"\nMONTHLY REVENUE ({label}):")
    for m in sorted(rev):
        print(f"  {m} | orders={orders[m]:3d} | revenue={rev[m]:12,.2f}")
    print(f"  sum check: {sum(rev.values()):,.2f}")

monthly_table(dedup, "deduplicated")
monthly_table([r for r in dedup if r["order_id"] not in outlier_ids], "deduplicated ex-outlier (ORD-0901 in Sep removed)")

# --- region breakdown ------------------------------------------------------
def region_table(dataset, label):
    rev = defaultdict(float)
    for r in dataset:
        rev[r["region"] or "(missing)"] += r["amount"]
    print(f"\nREGION REVENUE ({label}):")
    for g in sorted(rev, key=rev.get, reverse=True):
        print(f"  {g:10s} | {rev[g]:12,.2f}")

region_table([r for r in dedup if r["order_id"] not in outlier_ids], "deduplicated ex-outlier")
