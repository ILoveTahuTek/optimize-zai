#!/usr/bin/env python3
"""Independent cross-check for dom1 report (deliberately different implementation
from profile_csv.py: sort-based dedup instead of hash-set; extra checks).

Reads the CSV, recomputes every headline figure, and asserts agreement with the
profiler's numbers. Stdlib only.
"""
import csv
import io
import sys
from collections import defaultdict
from decimal import Decimal

PATH = "/home/z/my-project/harness-lab/tasks/sales-2025h1/sales.csv"
D = Decimal

# --- load: read raw text, normalize CRLF, parse via csv.reader (different path
# from DictReader used by the profiler) ---
with open(PATH, newline="") as f:
    text = f.read()
lines = [ln for ln in text.replace("\r\n", "\n").split("\n") if ln.strip() != ""]
reader = csv.reader(io.StringIO("\n".join(lines) + "\n"))
header = next(reader)
rows = [dict(zip(header, r)) for r in reader]

# --- dedup by sorting (different algorithm than the profiler's hash set) ---
tuples = sorted(tuple(sorted(r.items())) for r in rows)
unique_t, dupes = [], []
for i, t in enumerate(tuples):
    if i > 0 and t == tuples[i - 1]:
        dupes.append(dict(t))
    else:
        unique_t.append(t)
unique = [dict(t) for t in unique_t]

# --- headline figures ---
amounts = [D(r["amount"]) for r in unique]
net = sum(amounts, D(0))
gross = sum((a for a in amounts if a > 0), D(0))
neg = [r for r in unique if D(r["amount"]) < 0]
refund = sum((-D(r["amount"]) for r in neg), D(0))
zeros = [r for r in unique if D(r["amount"]) == 0]
dupe_value = sum((D(r["amount"]) for r in dupes if D(r["amount"]) > 0), D(0))

# --- breakdowns ---
by_prod_net = defaultdict(lambda: D(0))
by_prod_units_gross = defaultdict(int)   # units on positive rows
by_prod_units_net = defaultdict(int)     # refund units subtracted
by_month_net = defaultdict(lambda: D(0))
by_month_gross = defaultdict(lambda: D(0))
by_month_refund = defaultdict(lambda: D(0))
by_region_net = defaultdict(lambda: D(0))
missing_region = []
for r in unique:
    a = D(r["amount"])
    u = int(r["units"])
    p = r["product"]
    m = r["date"][:7]
    reg = r["region"].strip()
    by_prod_net[p] += a
    if a > 0:
        by_prod_units_gross[p] += u
        by_prod_units_net[p] += u
        by_month_gross[m] += a
    else:
        by_prod_units_net[p] -= u
        by_month_refund[m] += -a
    by_month_net[m] += a
    if reg == "":
        missing_region.append(r)
        reg = "(missing)"
    by_region_net[reg] += a

# --- consistency checks ---
price_bad = [r["order_id"] for r in unique
             if D(r["units"]) * D(r["unit_price"]) != abs(D(r["amount"]))]
missing_fields = {c: sum(1 for r in unique if not r[c].strip())
                  for c in header if c != "region"}
# same order_id used by two *different* unique rows
id_seen = {}
id_conflicts = []
for r in unique:
    key = tuple(sorted(r.items()))
    if r["order_id"] in id_seen and id_seen[r["order_id"]] != key:
        id_conflicts.append(r["order_id"])
    id_seen[r["order_id"]] = key
dates = sorted(r["date"] for r in unique)

# --- internal identities ---
assert gross - refund == net, "gross - refund != net"
assert sum(by_prod_net.values(), D(0)) == net, "product sum != net"
assert sum(by_month_net.values(), D(0)) == net, "month sum != net"
assert sum(by_region_net.values(), D(0)) == net, "region sum != net"
assert len(rows) == len(unique) + len(dupes), "raw != unique + dupes"

# --- expected profiler values (from profile.json produced earlier) ---
expected = {
    "raw": 128, "unique": 120, "dupes": 8,
    "net": D("48755.00"), "gross": D("49015.00"), "refund": D("260.00"),
    "dupe_value": D("5205.00"), "neg": 4, "zeros": 0, "missing_region": 4,
}
checks = [
    ("raw rows", len(rows), expected["raw"]),
    ("unique rows", len(unique), expected["unique"]),
    ("duplicate rows", len(dupes), expected["dupes"]),
    ("NET", net, expected["net"]),
    ("GROSS", gross, expected["gross"]),
    ("refund", refund, expected["refund"]),
    ("dupe value", dupe_value, expected["dupe_value"]),
    ("negative rows", len(neg), expected["neg"]),
    ("zero rows", len(zeros), expected["zeros"]),
    ("missing region rows", len(missing_region), expected["missing_region"]),
]
print("== CROSS-CHECK vs profiler ==")
ok = True
for name, got, exp in checks:
    match = "OK" if got == exp else "MISMATCH"
    if got != exp:
        ok = False
    print(f"{name:20s} cross-check={got}  profiler={exp}  {match}")
print(f"price sign/qty identity violations: {price_bad}")
print(f"order_id reused with different content: {id_conflicts}")
print(f"missing fields (non-region): {missing_fields}")
print(f"date range: {dates[0]} .. {dates[-1]}")

print("\n== DETAILS (unique rows) ==")
print(f"units by product (gross): {dict(sorted(by_prod_units_gross.items()))}")
print(f"units by product (net of refund units): {dict(sorted(by_prod_units_net.items()))}")
print(f"net by product: { {k: f'{v:.2f}' for k, v in sorted(by_prod_net.items())} }")
print(f"net by month: { {k: f'{v:.2f}' for k, v in sorted(by_month_net.items())} }")
print(f"gross by month: { {k: f'{v:.2f}' for k, v in sorted(by_month_gross.items())} }")
print(f"refunds by month: { {k: f'{v:.2f}' for k, v in sorted(by_month_refund.items())} }")
print(f"net by region: { {k: f'{v:.2f}' for k, v in sorted(by_region_net.items())} }")
print(f"missing-region ids: {[r['order_id'] for r in missing_region]}")
print(f"refund ids: {[(r['order_id'], r['product'], str(r['amount'])) for r in neg]}")
print(f"dupes detail: {[(d['order_id'], d['amount']) for d in dupes]}")
print("\nRESULT:", "ALL CHECKS AGREE" if ok else "MISMATCH FOUND")
sys.exit(0 if ok else 1)
