#!/usr/bin/env python3
"""Independent re-implementation (2nd implementation) for cross-checking the
profiler/detector outputs. Uses only the stdlib csv module; dedupes on the full
row tuple; parses dates with an explicit dual-format (ISO then DD/MM/YYYY) pass.
"""
import csv
from collections import Counter, defaultdict
from datetime import datetime

SRC = "/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv"

with open(SRC, newline="", encoding="utf-8") as f:
    raw = list(csv.DictReader(f))

raw_rows = len(raw)

# --- exact duplicate rows (full-row identity over all 7 fields) ---
seen = set()
unique = []
dup_extra = []  # the extra copies only
for r in raw:
    key = tuple((r.get(k) or "").strip() for k in
                ("order_id", "date", "product", "units", "unit_price", "region", "amount"))
    if key in seen:
        dup_extra.append(r)
    else:
        seen.add(key)
        unique.append(r)

unique_rows = len(unique)
dup_count = len(dup_extra)
dup_ids = Counter((r.get("order_id") or "").strip() for r in dup_extra)
dup_signed_value = sum(float(r["amount"]) for r in dup_extra)

# --- missing-field census across ALL fields ---
missing = defaultdict(list)
for r in unique:
    for k, v in r.items():
        if (v or "").strip() == "":
            missing[k].append((r.get("order_id") or "<blank-id>").strip())

# --- dual-format date parse: ISO first, then DD/MM/YYYY ---
def parse_date(s):
    s = (s or "").strip()
    try:
        return datetime.strptime(s, "%Y-%m-%d").date(), "ISO"
    except ValueError:
        pass
    try:
        return datetime.strptime(s, "%d/%m/%Y").date(), "DD/MM/YYYY"
    except ValueError:
        return None, "UNPARSED"

fmt_census = Counter()
non_iso = []
unparsed = []
for r in unique:
    d, fmt = parse_date(r["date"])
    fmt_census[fmt] += 1
    if fmt == "DD/MM/YYYY":
        non_iso.append(r["order_id"])
    if fmt == "UNPARSED":
        unparsed.append(r["order_id"])

# --- money figures over unique rows ---
amt = [float(r["amount"]) for r in unique]
net = sum(amt)
gross = sum(a for a in amt if a > 0)
refund_rows = [r for r in unique if float(r["amount"]) < 0]
refund_total = sum(-float(r["amount"]) for r in refund_rows)
refund_ids = [r["order_id"] for r in refund_rows]
zero_rows = [r["order_id"] for r in unique if float(r["amount"]) == 0]

# --- breakdowns ---
net_by_month = defaultdict(float)
row_by_month = Counter()
net_by_product = defaultdict(float)
units_signed = Counter()    # units * sign(amount): refunds net out
units_abs = Counter()       # absolute units moved (refunds still count as movement)
for r in unique:
    d, _ = parse_date(r["date"])
    a = float(r["amount"])
    if d:
        mk = d.strftime("%Y-%m")
        net_by_month[mk] += a
        row_by_month[mk] += 1
    p = r["product"]
    u = int(r["units"])
    net_by_product[p] += a
    sign = -1 if a < 0 else 1
    units_signed[p] += sign * u
    units_abs[p] += u

# --- price changes: products with >1 distinct unit price ---
price_by_product = defaultdict(set)
for r in unique:
    price_by_product[r["product"]].add(float(r["unit_price"]))
price_changes = {}
for p, prices in price_by_product.items():
    if len(prices) > 1:
        old, new = sorted(prices)
        # first affected order: earliest date at the NEW price (tie: file order)
        first = None
        for r in unique:  # unique preserves file order
            if r["product"] == p and float(r["unit_price"]) == new:
                d, _ = parse_date(r["date"])
                cand = (d or datetime.min.date(), r["order_id"])
                if first is None or (cand[0], ) < (first[0], ):
                    if first is None or cand[0] < first[0]:
                        first = cand
        n_new = sum(1 for r in unique if r["product"] == p and float(r["unit_price"]) == new)
        price_changes[p] = (old, new, first, n_new)

# --- top orders ---
top5 = sorted(((r["order_id"], float(r["amount"])) for r in unique),
              key=lambda t: -t[1])[:5]

print("== INDEPENDENT VERIFICATION ==")
print(f"raw rows: {raw_rows} = unique {unique_rows} + exact duplicates {dup_count}")
print(f"identity check: {raw_rows == unique_rows + dup_count}")
print(f"duplicate extra copies by order_id: {dict(dup_ids)}")
print(f"duplicate extra copies SIGNED value: {dup_signed_value:.2f}")
print(f"missing fields by column: { {k: v for k, v in missing.items()} }")
print(f"date format census: {dict(fmt_census)}  non-ISO ids: {non_iso}  unparsed: {unparsed}")
print(f"NET revenue  (unique, refunds negative): {net:.2f}")
print(f"GROSS revenue (positive amounts only):  {gross:.2f}")
print(f"Refund total: {refund_total:.2f} across {len(refund_rows)} rows {refund_ids}")
print(f"zero-amount rows: {len(zero_rows)} {zero_rows}")
print(f"net by month (dual-format parse): "
      f"{ {k: f'{v:.2f}' for k, v in sorted(net_by_month.items())} }")
print(f"monthly net sum check: {sum(net_by_month.values()):.2f}")
print(f"monthly row census (dual-format): {dict(sorted(row_by_month.items()))} "
      f"(total {sum(row_by_month.values())})")
print(f"net by product: { {k: f'{v:.2f}' for k, v in sorted(net_by_product.items())} }")
print(f"units SIGNED by product: {dict(units_signed)}")
print(f"units ABS by product: {dict(units_abs)}")
for p, (old, new, first, n_new) in price_changes.items():
    print(f"price change: {p} {old:.2f} -> {new:.2f}; first affected order {first[1]} "
          f"on {first[0]}; {n_new} orders at new price")
print(f"top-5 orders by amount: {top5}")
