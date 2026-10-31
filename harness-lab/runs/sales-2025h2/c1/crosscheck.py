#!/usr/bin/env python3
"""Independent cross-check for sales-2025h2/c1 report.

Second implementation, deliberately different from profile_csv.py:
  - parsing: plain text split(',') (file verified to contain no quote chars)
  - arithmetic: exact integer CENTS derived by string manipulation (no float, no Decimal)
  - aggregation: SQLite SQL engine (SUM/GROUP BY), not Python loops over Decimal
Definitions are fixed by the harness (unique-row / NET / GROSS / refund), only the
implementation is independent.
"""
import sqlite3
import sys
from pathlib import Path

CSV = Path("/home/z/my-project/harness-lab/tasks/sales-2025h2/sales.csv")


def to_cents(s: str) -> int:
    """Exact string->integer-cents conversion. Handles optional sign, 0-2 decimals."""
    s = s.strip()
    sign = -1 if s.startswith("-") else 1
    s = s.lstrip("+-")
    if "." in s:
        ip, fp = s.split(".")
        fp = (fp + "00")[:2]  # truncate beyond cents; input has exactly 2 decimals
    else:
        ip, fp = s, "00"
    return sign * (int(ip or "0") * 100 + int(fp or "0"))


def fmt(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    c = abs(cents)
    return f"{sign}{c // 100}.{c % 100:02d}"


def main() -> int:
    text = CSV.read_text()  # CRLF line endings; split on both
    lines = [ln for ln in text.replace("\r\n", "\n").split("\n") if ln.strip()]
    header = lines[0].split(",")
    assert header == ["order_id", "date", "product", "units", "unit_price",
                      "region", "amount"], header

    raw = []
    for ln in lines[1:]:
        f = ln.split(",")
        assert len(f) == 7, (ln, f)
        raw.append(tuple(x.strip() for x in f))

    # exact row-content dedup (definition fixed by harness)
    seen, unique, dupes = set(), [], []
    for r in raw:
        (dupes if r in seen else unique).append(r)
        seen.add(r)

    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE u (order_id TEXT, date TEXT, product TEXT, "
                 "units INT, unit_price_cents INT, region TEXT, amount_cents INT)")
    conn.executemany(
        "INSERT INTO u VALUES (?,?,?,?,?,?,?)",
        [(r[0], r[1], r[2], int(r[3]), to_cents(r[4]), r[5], to_cents(r[6]))
         for r in unique])

    q = lambda sql, *p: conn.execute(sql, p).fetchall()

    net, = q("SELECT COALESCE(SUM(amount_cents),0) FROM u")[0]
    gross, = q("SELECT COALESCE(SUM(amount_cents),0) FROM u WHERE amount_cents > 0")[0]
    refunds, = q("SELECT COALESCE(SUM(-amount_cents),0) FROM u WHERE amount_cents < 0")[0]
    neg_rows = q("SELECT order_id, amount_cents FROM u WHERE amount_cents < 0 ORDER BY order_id")
    zero_rows = q("SELECT order_id FROM u WHERE amount_cents = 0 ORDER BY order_id")
    miss_rows = q("SELECT order_id, amount_cents FROM u WHERE TRIM(region) = '' ORDER BY order_id")
    miss_val, = q("SELECT COALESCE(SUM(amount_cents),0) FROM u WHERE TRIM(region) = ''")[0]

    monthly = q("SELECT SUBSTR(date,1,7) m, SUM(amount_cents) FROM u GROUP BY m ORDER BY m")
    prod_net = q("SELECT product, SUM(amount_cents) FROM u GROUP BY product ORDER BY product")
    # units: refund rows carry positive units but negative amounts, so report both
    prod_units_all = q("SELECT product, SUM(units) FROM u GROUP BY product ORDER BY product")
    prod_units_net = q("""SELECT product, SUM(CASE WHEN amount_cents >= 0 THEN units ELSE 0 END)
                          FROM u GROUP BY product ORDER BY product""")
    price_bad = q("SELECT order_id FROM u WHERE amount_cents > 0 "
                  "AND units * unit_price_cents <> amount_cents")

    dupe_signed = sum(to_cents(r[6]) for r in dupes)
    dupe_pos = sum(to_cents(r[6]) for r in dupes if to_cents(r[6]) > 0)

    print("== INDEPENDENT CROSS-CHECK (SQLite + integer cents) ==")
    print(f"raw={len(raw)} unique={len(unique)} dupes={len(dupes)} "
          f"(identity: {len(raw)} == {len(unique)} + {len(dupes)})")
    print(f"NET   = {fmt(net)}")
    print(f"GROSS = {fmt(gross)}")
    print(f"refund total = {fmt(refunds)} rows={[(i, fmt(a)) for i, a in neg_rows]}")
    print(f"zero rows = {[i for i, in zero_rows]}")
    print(f"missing region: n={len(miss_rows)} value={fmt(miss_val)} ids={[i for i, _ in miss_rows]}")
    print(f"dupe signed value = {fmt(dupe_signed)} (positive-only = {fmt(dupe_pos)})")
    print("monthly NET:")
    for m, v in monthly:
        print(f"  {m}: {fmt(v)}")
    print("product NET:")
    for p, v in prod_net:
        print(f"  {p}: {fmt(v)}")
    print("units ALL rows (refund units included as positives):")
    for p, v in sorted(prod_units_all, key=lambda t: -t[1]):
        print(f"  {p}: {v}")
    print("units NET of refunds (refund-row units excluded):")
    for p, v in sorted(prod_units_net, key=lambda t: -t[1]):
        print(f"  {p}: {v}")
    print(f"price-consistency violations (positive rows): {[i for i, in price_bad]}")

    # identity check: NET == GROSS - refunds
    assert net == gross - refunds, (net, gross, refunds)
    # monthly sum == NET
    assert sum(v for _, v in monthly) == net
    # product sum == NET
    assert sum(v for _, v in prod_net) == net
    print("internal identities: NET = GROSS - refunds; monthly sum = product sum = NET  OK")

    # expected values from profile.json (the evidence base)
    import json
    prof = json.loads(CSV.parent.joinpath("profile.json").read_text())
    checks = [
        ("raw_rows", len(raw), prof["raw_rows"]),
        ("unique_rows", len(unique), prof["unique_rows"]),
        ("duplicate_rows", len(dupes), prof["duplicate_rows"]),
        ("NET", fmt(net), f"{prof['net_revenue']:.2f}"),
        ("GROSS", fmt(gross), f"{prof['gross_revenue']:.2f}"),
        ("refund_total", fmt(refunds), f"{prof['refund_total']:.2f}"),
        ("negative_rows", len(neg_rows), prof["negative_rows"]),
        ("zero_rows", len(zero_rows), prof["zero_amount_rows"]),
        ("missing_region_rows", len(miss_rows), prof["missing_region_rows"]),
        ("missing_region_value", fmt(miss_val), f"{prof['missing_region_value']:.2f}"),
        ("dupe_value_pos_only", fmt(dupe_pos), f"{prof['duplicate_value_if_counted']:.2f}"),
    ]
    for m, v in monthly:
        checks.append((f"month {m}", fmt(v), f"{prof['net_by_month'][m]:.2f}"))
    for p, v in prod_net:
        checks.append((f"product {p}", fmt(v), f"{prof['net_by_product'][p]:.2f}"))

    fails = 0
    print("\n== COMPARISON TO PROFILER ==")
    for name, mine, theirs in checks:
        ok = mine == theirs
        fails += (not ok)
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: independent={mine} profiler={theirs}")
    print(f"\n{len(checks) - fails}/{len(checks)} checks PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
