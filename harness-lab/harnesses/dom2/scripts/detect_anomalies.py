#!/usr/bin/env python3
"""Anomaly detector for a sales CSV — run BEFORE analysis.

  python3 detect_anomalies.py <input.csv>

Inventories the data BEFORE parsing anything: date-format census, per-product price
constancy, exact duplicates, refunds, zero rows, missing fields, top-5 largest orders,
and a monthly row census using a strict dual-format parser (ISO first, then dd/mm/yyyy;
anything else is UNPARSED and listed). Writes detect.json next to the input.
Stdlib only.
"""
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DMY = re.compile(r"^\d{2}/\d{2}/\d{4}$")
REQUIRED = {"order_id", "date", "product", "units", "unit_price", "region", "amount"}


def strict_date(s: str):
    s = s.strip()
    if ISO.match(s):
        try:
            return datetime.strptime(s, "%Y-%m-%d").date().isoformat()
        except ValueError:
            return None
    if DMY.match(s):
        try:
            return datetime.strptime(s, "%d/%m/%Y").date().isoformat()
        except ValueError:
            return None
    return None


def main(path: str) -> int:
    src = Path(path)
    rows = list(csv.DictReader(open(src, newline=""))) if src.is_file() else []
    if not rows:
        print(f"ERROR: cannot read {src}")
        return 1
    if REQUIRED - set(rows[0]):
        print(f"ERROR: missing columns: {sorted(REQUIRED - set(rows[0]))}")
        return 1

    seen, unique, dupes = set(), [], []
    for r in rows:
        key = tuple(sorted(r.items()))
        (dupes if key in seen else unique).append(r)
        seen.add(key)

    fmt_census = defaultdict(int)
    non_iso, unparsed = [], []
    monthly = defaultdict(int)
    for r in unique:
        s = r["date"].strip()
        if ISO.match(s):
            fmt_census["ISO"] += 1
        elif DMY.match(s):
            fmt_census["DD/MM/YYYY"] += 1
            non_iso.append(r["order_id"])
        else:
            fmt_census["OTHER"] += 1
            unparsed.append(r["order_id"])
        d = strict_date(s)
        monthly[d[:7] if d else "UNPARSED"] += 1

    negatives = [r for r in unique if Decimal(r["amount"]) < 0]
    zeros = [r for r in unique if Decimal(r["amount"]) == 0]
    missing_region = [r for r in unique if not r["region"].strip()]

    prices: dict[str, set] = defaultdict(set)
    for r in unique:
        if Decimal(r["amount"]) > 0:
            prices[r["product"]].add(str(Decimal(r["unit_price"])))
    price_changes = {p: sorted(v) for p, v in prices.items() if len(v) > 1}

    top5 = sorted(unique, key=lambda r: -Decimal(r["amount"]))[:5]

    report = {
        "raw_rows": len(rows),
        "unique_rows": len(unique),
        "exact_duplicate_rows": len(dupes),
        "date_format_census": dict(fmt_census),
        "non_iso_date_rows": non_iso,
        "unparsed_date_rows": unparsed,
        "monthly_row_census_strict": dict(sorted(monthly.items())),
        "negative_rows": len(negatives),
        "negative_ids": [r["order_id"] for r in negatives],
        "refund_total": float(sum((-Decimal(r["amount"]) for r in negatives), Decimal(0))),
        "zero_rows": [r["order_id"] for r in zeros],
        "missing_region_rows": len(missing_region),
        "price_changes": price_changes,
        "top5_orders": [(r["order_id"], float(Decimal(r["amount"]))) for r in top5],
    }
    (src.parent / "detect.json").write_text(json.dumps(report, indent=2, default=str))

    print("== ANOMALY INVENTORY (pre-parse) ==")
    print(f"rows: {report['raw_rows']} raw = {report['unique_rows']} unique + {report['exact_duplicate_rows']} exact duplicates")
    print(f"date formats: {dict(fmt_census)}")
    print(f"non-ISO dates: {len(non_iso)} rows {non_iso[:10]}")
    print(f"unparseable dates: {len(unparsed)} {unparsed[:10]}")
    print(f"monthly row census (strict parse): {dict(sorted(monthly.items()))}")
    print(f"negative rows: {len(negatives)} {report['negative_ids']} total {report['refund_total']:.2f}")
    print(f"zero-amount rows: {len(zeros)} {report['zero_rows']}")
    print(f"missing region: {len(missing_region)} rows")
    print(f"PRICE CHANGES: {price_changes if price_changes else 'none'}")
    print(f"top-5 largest orders: {report['top5_orders']}")
    print(f"detect.json -> {src.parent / 'detect.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
