#!/usr/bin/env python3
"""Method A: pure-stdlib Python analysis of sales.csv (csv module + Decimal)."""
import csv
import hashlib
from collections import defaultdict
from decimal import Decimal

PATH = "/home/z/my-project/harness-lab/tasks/sales-2025h1/sales.csv"
Q = Decimal("0.01")
out = []

def emit(k, v):
    out.append(f"{k}={v}")

def money(d: Decimal) -> str:
    return str(d.quantize(Q))

with open(PATH, "rb") as f:
    sha = hashlib.sha256(f.read()).hexdigest()
emit("sha256", sha)

with open(PATH, newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    raw = [row for row in reader if row]  # ignore fully blank lines if any

emit("header", ",".join(header))
emit("bad_fieldcount_rows", sum(1 for r in raw if len(r) != len(header)))

FIELDS = len(header)
IDX = {name: i for i, name in enumerate(header)}
# order_id,date,product,units,unit_price,region,amount

def amount_of(r):
    return Decimal(r[IDX["amount"]])

def units_of(r):
    return int(r[IDX["units"]])

# --- dedup on the exact tuple of all fields ---
seen = {}
dups = []
for r in raw:
    key = tuple(r)
    if key in seen:
        dups.append(key)
    else:
        seen[key] = r
uniq = list(seen.values())

emit("raw_rows", len(raw))
emit("unique_rows", len(uniq))
emit("dup_rows", len(dups))
emit("dup_value", money(sum((Decimal(t[IDX["amount"]]) for t in dups), Decimal("0"))))

# --- data quality (raw-level and unique-level) ---
neg_raw = [r for r in raw if amount_of(r) < 0]
neg_uniq = [r for r in uniq if amount_of(r) < 0]
zero_raw = [r for r in raw if amount_of(r) == 0]
zero_uniq = [r for r in uniq if amount_of(r) == 0]
emit("neg_rows_raw", len(neg_raw))
emit("neg_rows_unique", len(neg_uniq))
emit("neg_value_raw", money(sum((-amount_of(r) for r in neg_raw), Decimal("0"))))
emit("refund_total", money(sum((-amount_of(r) for r in neg_uniq), Decimal("0"))))
emit("zero_rows_raw", len(zero_raw))
emit("zero_rows_unique", len(zero_uniq))

missing_cells = 0
missing_rows = set()
missing_by_field = defaultdict(int)
for i, r in enumerate(raw):
    for j in range(FIELDS):
        if r[j].strip() == "":
            missing_cells += 1
            missing_rows.add(i)
            missing_by_field[header[j]] += 1
emit("missing_cells_raw", missing_cells)
emit("missing_rows_raw", len(missing_rows))
for fld, cnt in sorted(missing_by_field.items()):
    emit(f"missing_field[{fld}]", cnt)

# --- headline money figures over UNIQUE rows ---
net = sum((amount_of(r) for r in uniq), Decimal("0"))
gross = sum((amount_of(r) for r in uniq if amount_of(r) > 0), Decimal("0"))
emit("net_revenue", money(net))
emit("gross_revenue", money(gross))
emit("refund_total2", money(sum((-amount_of(r) for r in neg_uniq), Decimal("0"))))

# --- integrity: amount vs units*unit_price (either sign) ---
mismatch = 0
for r in uniq:
    amt = amount_of(r)
    calc = Decimal(r[IDX["unit_price"]]) * units_of(r)
    if amt != calc and amt != -calc:
        mismatch += 1
emit("amount_sign_price_mismatches", mismatch)

# --- monthly breakdown over UNIQUE rows ---
mo = defaultdict(lambda: {"orders": 0, "units": 0, "gross": Decimal("0"), "refund": Decimal("0"), "net": Decimal("0")})
for r in uniq:
    m = r[IDX["date"]][:7]
    a = amount_of(r)
    d = mo[m]
    d["orders"] += 1
    d["units"] += units_of(r)
    if a > 0:
        d["gross"] += a
    elif a < 0:
        d["refund"] += -a
    d["net"] += a
for m in sorted(mo):
    d = mo[m]
    emit(f"orders[{m}]", d["orders"])
    emit(f"units[{m}]", d["units"])
    emit(f"gross[{m}]", money(d["gross"]))
    emit(f"refund[{m}]", money(d["refund"]))
    emit(f"net[{m}]", money(d["net"]))
emit("months", ",".join(sorted(mo)))
emit("date_min", min(r[IDX["date"]] for r in uniq))
emit("date_max", max(r[IDX["date"]] for r in uniq))

# --- product breakdown over UNIQUE rows ---
pr = defaultdict(lambda: {"units": 0, "signed_units": 0, "orders": 0, "gross": Decimal("0"), "net": Decimal("0")})
for r in uniq:
    p = r[IDX["product"]]
    a = amount_of(r)
    d = pr[p]
    d["orders"] += 1
    d["units"] += units_of(r)
    d["signed_units"] += units_of(r) * (1 if a > 0 else -1 if a < 0 else 0)
    if a > 0:
        d["gross"] += a
    d["net"] += a
for p in sorted(pr):
    d = pr[p]
    emit(f"p_orders[{p}]", d["orders"])
    emit(f"p_units[{p}]", d["units"])
    emit(f"p_signed_units[{p}]", d["signed_units"])
    emit(f"p_gross[{p}]", money(d["gross"]))
    emit(f"p_net[{p}]", money(d["net"]))

# --- region breakdown over UNIQUE rows (net) ---
rg = defaultdict(lambda: {"orders": 0, "net": Decimal("0")})
for r in uniq:
    reg = r[IDX["region"]].strip() or "(missing)"
    rg[reg]["orders"] += 1
    rg[reg]["net"] += amount_of(r)
for reg in sorted(rg):
    emit(f"r_orders[{reg}]", rg[reg]["orders"])
    emit(f"r_net[{reg}]", money(rg[reg]["net"]))

print("\n".join(out))
