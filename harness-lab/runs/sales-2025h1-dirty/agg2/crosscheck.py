#!/usr/bin/env python3
"""INDEPENDENT cross-check for sales-2025h1-dirty — deliberately a second,
differently-structured implementation (NOT a copy of profile_csv.py):

  - dedup via sorted full-line grouping (sort + groupby), not a seen-set
  - date handling via a regex FORMAT CENSUS first, then an explicit
    dual-format parser (ISO yyyy-mm-dd, then dd/mm/yyyy)
  - per-product unit-price CONSTANCY on positive rows (with first-affected
    date of each new price) — arithmetic units*price==amount checked separately
  - units-based best sellers (gross units and net units) alongside net revenue
  - missing-field census per column; signed duplicate value
Stdlib only. Writes crosscheck.json next to itself.
"""
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import date
from decimal import Decimal
from itertools import groupby
from pathlib import Path

RUN_DIR = Path(__file__).parent
CSV = "/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv"

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")          # yyyy-mm-dd
DMY = re.compile(r"^\d{2}/\d{2}/\d{4}$")          # dd/mm/yyyy
OTHER = re.compile(r"^\d{4}-\d{2}$")              # bare yyyy-mm


def parse_date(s: str):
    """Dual-format parser: try ISO first, then dd/mm/yyyy. Returns date or None."""
    s = s.strip()
    if ISO.match(s):
        y, m, d = map(int, s.split("-"))
        return date(y, m, d)
    if DMY.match(s):
        d, m, y = map(int, s.split("/"))
        return date(y, m, d)
    return None


def fmt_of(s: str) -> str:
    s = s.strip()
    if ISO.match(s):
        return "ISO yyyy-mm-dd"
    if DMY.match(s):
        return "dd/mm/yyyy"
    if OTHER.match(s):
        return "yyyy-mm"
    return "other/empty"


def main() -> int:
    with open(CSV, newline="") as f:
        rows = list(csv.DictReader(f))

    # --- row-count identity: sort full raw lines, group identical ones -------
    with open(CSV, newline="") as f:
        lines = f.read().splitlines()
    body = sorted(lines[1:])
    groups = [(k, len(list(g))) for k, g in groupby(body)]
    unique_lines = len(groups)
    dupe_rows = sum(n - 1 for _, n in groups if n > 1)
    assert unique_lines + dupe_rows == len(rows), "row identity broken"

    # unique rows = the FIRST raw occurrence of each content group,
    # recovered by walking in file order and marking seen content
    seen_content, uniq, dups = set(), [], []
    for r in rows:
        c = tuple(r.items())
        (dups if c in seen_content else uniq).append(r)
        seen_content.add(c)

    # --- date format CENSUS (raw rows, before any parsing) -------------------
    census = defaultdict(int)
    for r in rows:
        census[fmt_of(r["date"])] += 1
    # ambiguity guard: any dd/mm where BOTH day and month <= 12?
    ambiguous = [r["order_id"] for r in rows if DMY.match(r["date"].strip())
                 and int(r["date"].strip().split("/")[0]) <= 12
                 and int(r["date"].strip().split("/")[1]) <= 12]

    parsed_fail = [r["order_id"] for r in rows if parse_date(r["date"]) is None]

    # --- money aggregates on unique rows (Decimal) ---------------------------
    amt = lambda r: Decimal(r["amount"])
    neg = [r for r in uniq if amt(r) < 0]
    zero = [r for r in uniq if amt(r) == 0]
    pos = [r for r in uniq if amt(r) > 0]
    gross = sum((amt(r) for r in pos), Decimal(0))
    refunds = sum((-amt(r) for r in neg), Decimal(0))
    net = gross - refunds
    dupe_signed = sum((amt(r) for r in dups), Decimal(0))
    dupe_positive = sum((amt(r) for r in dups if amt(r) > 0), Decimal(0))

    # --- per-product price constancy on POSITIVE rows ------------------------
    prices_by_product = defaultdict(set)
    for r in pos:
        prices_by_product[r["product"]].add(Decimal(r["unit_price"]))
    price_changes = []
    for prod, prices in sorted(prices_by_product.items()):
        if len(prices) > 1:
            old = min(prices)
            new = max(prices)
            first_new = min(parse_date(r["date"]) for r in pos
                            if r["product"] == prod and Decimal(r["unit_price"]) == new)
            n_new = sum(1 for r in pos if r["product"] == prod
                        and Decimal(r["unit_price"]) == new)
            n_old = sum(1 for r in pos if r["product"] == prod
                        and Decimal(r["unit_price"]) == old)
            # arithmetic consistency per price row (units*price==amount)
            price_changes.append({
                "product": prod, "old_price": float(old), "new_price": float(new),
                "first_affected_date": first_new.isoformat(),
                "rows_at_old": n_old, "rows_at_new": n_new,
            })

    arith_bad = [r["order_id"] for r in pos
                 if Decimal(r["units"]) * Decimal(r["unit_price"]) != amt(r)]
    arith_bad_neg = [r["order_id"] for r in neg
                     if Decimal(r["units"]) * Decimal(r["unit_price"]) != -amt(r)]

    # --- breakdowns with CORRECTLY PARSED dates ------------------------------
    net_m, gross_m, ref_m = defaultdict(Decimal), defaultdict(Decimal), defaultdict(Decimal)
    for r in uniq:
        d = parse_date(r["date"])
        m = d.strftime("%Y-%m") if d else "UNPARSED"
        net_m[m] += amt(r)
        if amt(r) > 0:
            gross_m[m] += amt(r)
        elif amt(r) < 0:
            ref_m[m] += -amt(r)

    net_p = defaultdict(Decimal)
    units_gross_p, units_net_p = defaultdict(int), defaultdict(int)
    orders_p = defaultdict(int)
    for r in uniq:
        net_p[r["product"]] += amt(r)
        if amt(r) > 0:
            units_gross_p[r["product"]] += int(r["units"])
            orders_p[r["product"]] += 1
        elif amt(r) < 0:
            units_net_p[r["product"]] -= int(r["units"])  # returns subtract
    for p in units_net_p:
        units_net_p[p] += units_gross_p[p]

    # --- missing-field census per column (unique rows) -----------------------
    miss = {c: sum(1 for r in uniq if not r[c].strip()) for c in rows[0]}
    miss_raw = {c: sum(1 for r in rows if not r[c].strip()) for c in rows[0]}
    miss_val = sum((amt(r) for r in uniq if not r["region"].strip()), Decimal(0))
    miss_pos = sum((amt(r) for r in uniq if not r["region"].strip() and amt(r) > 0), Decimal(0))

    out = {
        "raw_rows": len(rows),
        "unique_rows": unique_lines,
        "duplicate_rows": dupe_rows,
        "duplicate_ids": sorted({r["order_id"] for r in dups}),
        "duplicate_signed_value": float(dupe_signed),
        "duplicate_positive_value": float(dupe_positive),
        "net_revenue": float(net),
        "gross_revenue": float(gross),
        "refund_total": float(refunds),
        "refund_rows": len(neg),
        "refund_rows_raw_counted": sum(1 for r in rows if Decimal(r["amount"]) < 0),
        "negative_ids": [r["order_id"] for r in neg],
        "zero_rows": len(zero),
        "zero_ids": [r["order_id"] for r in zero],
        "date_census_raw": dict(census),
        "date_ambiguous_dmy": ambiguous,
        "date_parse_failures": parsed_fail,
        "price_constancy": price_changes,
        "arithmetic_violations_positive": arith_bad,
        "arithmetic_violations_negative": arith_bad_neg,
        "net_by_month": {k: float(v) for k, v in sorted(net_m.items())},
        "gross_by_month": {k: float(v) for k, v in sorted(gross_m.items())},
        "refunds_by_month": {k: float(v) for k, v in sorted(ref_m.items())},
        "net_by_product": {k: float(v) for k, v in sorted(net_p.items())},
        "units_gross_by_product": dict(sorted(units_gross_p.items())),
        "units_net_by_product": dict(sorted(units_net_p.items())),
        "sale_orders_by_product": dict(sorted(orders_p.items())),
        "missing_fields_unique": {k: v for k, v in miss.items() if v},
        "missing_fields_raw": {k: v for k, v in miss_raw.items() if v},
        "missing_region_value_signed": float(miss_val),
        "missing_region_value_positive": float(miss_pos),
        "month_sum_equals_net": float(sum(net_m.values())) == float(net),
    }
    (RUN_DIR / "crosscheck.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
