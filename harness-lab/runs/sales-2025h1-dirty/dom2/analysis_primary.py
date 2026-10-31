#!/usr/bin/env python3
"""Primary analysis for sales-2025h1-dirty. Run AFTER detect_anomalies.py.

Definitions (per harness INSTRUCTIONS.md):
  NET revenue   = sum(amount) over UNIQUE rows (exact duplicates removed), refunds as negatives.
  GROSS revenue = sum(amount) over UNIQUE rows where amount > 0.
  Refund total  = |sum(amount) over UNIQUE rows where amount < 0|.
Dates: dual-format parse — ISO (YYYY-MM-DD) first, then DD/MM/YYYY; anything else = UNPARSED.
Stdlib only, Decimal arithmetic.
"""
import csv, json, sys
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

SRC = Path("/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv")
OUT = Path("/home/z/my-project/harness-lab/runs/sales-2025h1-dirty/dom2")

def parse_date(s: str):
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):  # dual format: ISO first, then dd/mm/yyyy
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None

D = lambda x: Decimal(x)

rows = [r for r in csv.DictReader(open(SRC, newline="")) if r]
raw = len(rows)

# Exact-duplicate removal on full raw row content (keep first occurrence)
seen, unique, dupes = set(), [], []
for r in rows:
    key = tuple(r.items())
    if key in seen:
        dupes.append(r)
    else:
        seen.add(key)
        unique.append(r)

dup_signed_value = sum((D(r["amount"]) for r in dupes), Decimal(0))  # overcount if dupes included

net = sum((D(r["amount"]) for r in unique), Decimal(0))
gross = sum((D(r["amount"]) for r in unique if D(r["amount"]) > 0), Decimal(0))
refund = sum((-D(r["amount"]) for r in unique if D(r["amount"]) < 0), Decimal(0))

neg = [r for r in unique if D(r["amount"]) < 0]
zer = [r for r in unique if D(r["amount"]) == 0]
miss_region = [r["order_id"] for r in unique if not r["region"].strip()]

# Monthly breakdown (unique rows, dual-format dates)
mon = defaultdict(lambda: {"net": Decimal(0), "gross": Decimal(0), "refund": Decimal(0), "rows": 0})
unparsed = []
for r in unique:
    d = parse_date(r["date"])
    if d is None:
        unparsed.append(r["order_id"]); continue
    m = d.strftime("%Y-%m")
    a = D(r["amount"])
    mon[m]["net"] += a; mon[m]["rows"] += 1
    if a > 0: mon[m]["gross"] += a
    elif a < 0: mon[m]["refund"] += -a

# Product aggregates (unique rows)
prod = defaultdict(lambda: {"units_sold": 0, "units_ref": 0, "net": Decimal(0), "gross": Decimal(0), "orders": 0})
for r in unique:
    p = prod[r["product"]]; a = D(r["amount"])
    p["net"] += a; p["orders"] += 1
    if a > 0:
        p["units_sold"] += int(r["units"]); p["gross"] += a
    elif a < 0:
        p["units_ref"] += int(r["units"])
for p in prod.values():
    p["units_net"] = p["units_sold"] - p["units_ref"]

# Monitor price timeline (all unique rows, per price point)
mp = defaultdict(list)
for r in unique:
    if r["product"] == "Monitor":
        mp[r["unit_price"]].append(r["date"])
mon_timeline = {k: {"min_date": min(v), "max_date": max(v), "n": len(v)} for k, v in sorted(mp.items())}

# Consistency: amount == units * unit_price ?
inconsistent = [r["order_id"] for r in unique if D(r["amount"]) != D(r["units"]) * D(r["unit_price"])]

# order_id appearing with DIFFERENT content (not exact dups)
byid = defaultdict(set)
for r in unique:
    byid[r["order_id"]].add(tuple(r.items()))
oid_conflicts = sorted(k for k, v in byid.items() if len(v) > 1)

regions = defaultdict(lambda: {"net": Decimal(0), "rows": 0})
for r in unique:
    k = r["region"].strip() or "(missing)"
    regions[k]["net"] += D(r["amount"]); regions[k]["rows"] += 1

top5 = sorted(unique, key=lambda r: -D(r["amount"]))[:5]

res = {
    "raw_rows": raw, "unique_rows": len(unique), "exact_duplicate_rows": len(dupes),
    "duplicate_signed_value": str(dup_signed_value),
    "duplicate_order_ids": sorted({r["order_id"] for r in dupes}),
    "net_revenue": str(net), "gross_revenue": str(gross), "refund_total": str(refund),
    "identity_holds": net == gross - refund,
    "monthly": {m: {k: (str(v) if isinstance(v, Decimal) else v) for k, v in d.items()} for m, d in sorted(mon.items())},
    "unparsed_dates": unparsed,
    "negative_rows": [{"id": r["order_id"], "date": r["date"], "product": r["product"],
                       "units": r["units"], "unit_price": r["unit_price"], "amount": r["amount"]} for r in neg],
    "zero_rows": [{"id": r["order_id"], "date": r["date"], "product": r["product"],
                   "units": r["units"], "amount": r["amount"]} for r in zer],
    "missing_region_rows": miss_region,
    "products": {k: {kk: (str(vv) if isinstance(vv, Decimal) else vv) for kk, vv in v.items()} for k, v in sorted(prod.items())},
    "monitor_price_timeline": mon_timeline,
    "amount_inconsistencies": inconsistent,
    "order_id_conflicts": oid_conflicts,
    "regions": {k: {"net": str(v["net"]), "rows": v["rows"]} for k, v in sorted(regions.items())},
    "top5_orders": [(r["order_id"], str(D(r["amount"]))) for r in top5],
}
(OUT / "analysis_primary.json").write_text(json.dumps(res, indent=2))

print(f"rows: raw={raw} unique={len(unique)} dupes={len(dupes)} dup_signed={dup_signed_value}")
print(f"dup order_ids: {sorted({r['order_id'] for r in dupes})}")
print(f"NET={net}  GROSS={gross}  REFUND={refund}  identity(net==gross-refund): {net == gross - refund}")
print("monthly:")
for m, d in sorted(mon.items()):
    print(f"  {m}: rows={d['rows']:3d} net={d['net']:>10} gross={d['gross']:>10} refund={d['refund']:>8}")
print(f"unparsed dates: {unparsed}")
print("products (units_sold / units_net / net / gross):")
for k, v in sorted(prod.items()):
    print(f"  {k:9s} sold={v['units_sold']:3d} net={v['units_net']:3d} netrev={v['net']:>10} gross={v['gross']:>10} orders={v['orders']}")
print(f"monitor timeline: {mon_timeline}")
print(f"amount != units*price: {inconsistent}")
print(f"order_id content conflicts: {oid_conflicts}")
print(f"missing region ids: {miss_region}")
print(f"regions: { {k: str(v['net']) for k, v in sorted(regions.items())} }")
print(f"top5: {res['top5_orders']}")
