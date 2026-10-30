#!/usr/bin/env python3
"""Deterministic data-hygiene profiler for a sales CSV.

Run this BEFORE any analysis:  python3 profile_csv.py <input.csv>

Prints a readable summary and writes profile.json next to the input file.
Stdlib only. Definitions used here (downstream reports must match):
  unique row    : first occurrence of an exact row-content match
  duplicate row : any later exact row-content match
  NET revenue   : sum of amount over unique rows (negatives included)
  GROSS revenue : sum of positive amounts over unique rows
  refund total  : sum of |negative amounts| over unique rows
"""
import csv
import json
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

REQUIRED = {"order_id", "date", "product", "units", "unit_price", "region", "amount"}


def money(x: Decimal) -> str:
    return f"{x:.2f}"


def main(path: str) -> int:
    src = Path(path)
    if not src.is_file():
        print(f"ERROR: file not found: {src}")
        return 1
    with open(src, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("ERROR: empty CSV")
        return 1
    missing_cols = REQUIRED - set(rows[0])
    if missing_cols:
        print(f"ERROR: missing columns: {sorted(missing_cols)}")
        return 1

    seen: set[tuple] = set()
    unique: list[dict] = []
    dupes: list[dict] = []
    for r in rows:
        key = tuple(sorted(r.items()))
        (dupes if key in seen else unique).append(r)
        seen.add(key)

    negatives = [r for r in unique if Decimal(r["amount"]) < 0]
    zeros = [r for r in unique if Decimal(r["amount"]) == 0]
    missing_region = [r for r in unique if not r["region"].strip()]

    gross = sum((Decimal(r["amount"]) for r in unique if Decimal(r["amount"]) > 0), Decimal(0))
    refunds = sum((-Decimal(r["amount"]) for r in negatives), Decimal(0))
    net = gross - refunds
    dupe_value = sum((Decimal(r["amount"]) for r in dupes if Decimal(r["amount"]) > 0), Decimal(0))

    by_product: dict[str, Decimal] = defaultdict(lambda: Decimal(0))
    by_month: dict[str, Decimal] = defaultdict(lambda: Decimal(0))
    for r in unique:
        amt = Decimal(r["amount"])
        by_product[r["product"]] += amt
        by_month[r["date"][:7]] += amt

    price_bad = []
    for r in unique:
        if Decimal(r["amount"]) > 0 and Decimal(r["units"]) * Decimal(r["unit_price"]) != Decimal(r["amount"]):
            price_bad.append(r["order_id"])

    profile = {
        "source_file": str(src),
        "raw_rows": len(rows),
        "unique_rows": len(unique),
        "duplicate_rows": len(dupes),
        "duplicate_value_if_counted": float(dupe_value),
        "negative_rows": len(negatives),
        "negative_ids": [r["order_id"] for r in negatives],
        "refund_total": float(refunds),
        "zero_amount_rows": len(zeros),
        "zero_ids": [r["order_id"] for r in zeros],
        "missing_region_rows": len(missing_region),
        "missing_region_value": float(sum((Decimal(r["amount"]) for r in missing_region), Decimal(0))),
        "net_revenue": float(net),
        "gross_revenue": float(gross),
        "net_by_product": {k: float(v) for k, v in sorted(by_product.items())},
        "net_by_month": {k: float(v) for k, v in sorted(by_month.items())},
        "price_consistency_violations": price_bad,
    }

    out = src.parent / "profile.json"
    out.write_text(json.dumps(profile, indent=2))

    print("== DATA PROFILE ==")
    print(f"rows: {profile['raw_rows']} raw = {profile['unique_rows']} unique + {profile['duplicate_rows']} exact duplicates")
    print(f"NET revenue  (unique rows, refunds as negatives): {money(net)}")
    print(f"GROSS revenue (positive amounts only): {money(gross)}")
    print(f"refund total: {money(refunds)} across {len(negatives)} rows {profile['negative_ids']}")
    print(f"zero-amount rows: {len(zeros)} {profile['zero_ids']}")
    print(f"missing region: {len(missing_region)} rows worth {money(profile['missing_region_value'] and Decimal(str(profile['missing_region_value'])))}")
    print(f"duplicates add {money(dupe_value)} if wrongly counted")
    print(f"price-consistency violations: {len(price_bad)}")
    print(f"net by product: { {k: money(v) for k, v in by_product.items()} }")
    print(f"net by month:   { {k: money(v) for k, v in by_month.items()} }")
    print(f"profile.json -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
