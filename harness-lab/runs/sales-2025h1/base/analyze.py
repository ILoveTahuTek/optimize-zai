#!/usr/bin/env python3
"""Sales analysis for sales-2025h1 / base harness run.

Reads the task CSV, computes headline metrics, and prints a JSON-ish summary
that the report is written from. Uses stdlib only (no pandas dependency).
"""
import csv
import json
from collections import defaultdict
from datetime import date

CSV_PATH = "/home/z/my-project/harness-lab/tasks/sales-2025h1/sales.csv"

rows = []
with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    for r in reader:
        if not any(v.strip() for v in r.values()):  # skip fully blank lines
            continue
        rows.append(r)

n_raw = len(rows)

# --- Data quality: duplicates -------------------------------------------
seen_full = {}
dup_full = []          # exact duplicate rows (all fields identical)
order_first = {}       # order_id -> first row index
conflicting = []       # same order_id but different content
for i, r in enumerate(rows):
    key = tuple(r[k] for k in ("order_id", "date", "product", "units", "unit_price", "region", "amount"))
    oid = r["order_id"].strip()
    if oid in order_first:
        j = order_first[oid]
        if rows[j] == r:
            dup_full.append(oid)
        else:
            conflicting.append((oid, j, i))
    else:
        order_first[oid] = i
    if key in seen_full:
        dup_full.append(oid) if False else None
    seen_full[key] = i

# Deduplicate: keep first occurrence of each exact-duplicate row
dedup = []
seen_keys = set()
for r in rows:
    key = tuple(r[k] for k in ("order_id", "date", "product", "units", "unit_price", "region", "amount"))
    if key in seen_keys:
        continue
    seen_keys.add(key)
    dedup.append(r)
n_dedup = len(dedup)

# --- Helpers -------------------------------------------------------------
def money(x):
    return round(x, 2)

def units_of(r):
    return int(r["units"])

def amount_of(r):
    return float(r["amount"])

# --- Totals (both raw and deduplicated) ----------------------------------
total_raw = sum(amount_of(r) for r in rows)
total_dedup = sum(amount_of(r) for r in dedup)

# amount == units * unit_price consistency check
mismatches = [r["order_id"] for r in dedup if money(units_of(r) * float(r["unit_price"])) != money(amount_of(r))]

# Negatives (refunds/returns?)
negatives = [r for r in dedup if amount_of(r) < 0]
positive_dedup = [r for r in dedup if amount_of(r) >= 0]
total_pos = sum(amount_of(r) for r in positive_dedup)

# --- Product breakdown (deduplicated, gross amounts as recorded) ---------
prod_units = defaultdict(int)
prod_rev = defaultdict(float)
prod_orders = defaultdict(int)
for r in dedup:
    p = r["product"].strip()
    prod_units[p] += units_of(r)
    prod_rev[p] += amount_of(r)
    prod_orders[p] += 1

# Net-of-refund variant (exclude negative rows)
prod_units_pos = defaultdict(int)
prod_rev_pos = defaultdict(float)
for r in positive_dedup:
    p = r["product"].strip()
    prod_units_pos[p] += units_of(r)
    prod_rev_pos[p] += amount_of(r)

best_by_units = max(prod_units.items(), key=lambda kv: kv[1])
best_by_rev = max(prod_rev.items(), key=lambda kv: kv[1])

# --- Monthly revenue (deduplicated) --------------------------------------
monthly = defaultdict(float)
monthly_orders = defaultdict(int)
monthly_units = defaultdict(int)
for r in dedup:
    m = r["date"][:7]  # YYYY-MM
    monthly[m] += amount_of(r)
    monthly_orders[m] += 1
    monthly_units[m] += units_of(r)

# --- Region breakdown (deduplicated) -------------------------------------
region_rev = defaultdict(float)
region_orders = defaultdict(int)
missing_region = []
for r in dedup:
    reg = r["region"].strip()
    region_rev[reg] += amount_of(r)
    region_orders[reg] += 1
    if not reg:
        missing_region.append(r["order_id"])

# --- Price consistency per product ---------------------------------------
price_map = defaultdict(set)
for r in dedup:
    price_map[r["product"].strip()].add(r["unit_price"])

# --- Date range -----------------------------------------------------------
dates = sorted(r["date"] for r in dedup)

out = {
    "rows_raw": n_raw,
    "rows_dedup": n_dedup,
    "duplicate_rows_removed": n_raw - n_dedup,
    "duplicate_order_ids_exact": sorted(set(dup_full)),
    "conflicting_order_ids": [c[0] for c in conflicting],
    "unique_order_ids_raw": len({r["order_id"] for r in rows}),
    "total_revenue_raw": money(total_raw),
    "total_revenue_dedup": money(total_dedup),
    "total_revenue_dedup_net_of_negatives": money(total_pos),
    "amount_mismatches": mismatches,
    "negative_rows": [
        {"order_id": r["order_id"], "date": r["date"], "product": r["product"],
         "units": r["units"], "amount": r["amount"], "region": r["region"]}
        for r in negatives
    ],
    "best_by_units": {"product": best_by_units[0], "units": best_by_units[1]},
    "best_by_revenue": {"product": best_by_rev[0], "revenue": money(best_by_rev[1])},
    "product_table": {
        p: {"orders": prod_orders[p], "units": prod_units[p], "revenue": money(prod_rev[p]),
            "unit_price": sorted(price_map[p])}
        for p in sorted(prod_rev, key=lambda x: -prod_rev[x])
    },
    "monthly": {
        m: {"orders": monthly_orders[m], "units": monthly_units[m], "revenue": money(monthly[m])}
        for m in sorted(monthly)
    },
    "regions": {
        (k if k else "(missing)"): {"orders": region_orders[k], "revenue": money(region_rev[k])}
        for k in sorted(region_rev, key=lambda x: -region_rev[x])
    },
    "missing_region_order_ids": missing_region,
    "date_min": dates[0],
    "date_max": dates[-1],
}

print(json.dumps(out, indent=2))
