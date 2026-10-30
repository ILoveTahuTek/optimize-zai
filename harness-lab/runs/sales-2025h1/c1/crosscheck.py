#!/usr/bin/env python3
"""Independent cross-check for the c1 sales-2025h1 report.

Deliberately implemented DIFFERENTLY from scripts/profile_csv.py:
  - pandas instead of stdlib csv+dict
  - integer-cents arithmetic instead of Decimal
  - drop_duplicates(keep='first') instead of set-of-tuples dedup
  - datetime parsing for months instead of string slicing
  - signed duplicate value, units rankings, refund-impact check added
"""
import sys
import pandas as pd

SRC = "/home/z/my-project/harness-lab/tasks/sales-2025h1/sales.csv"


def cents(s: str) -> int:
    return int(round(float(str(s).strip()) * 100))


def fmt(c: int) -> str:
    sign = "-" if c < 0 else ""
    return f"{sign}{abs(c)//100}.{abs(c)%100:02d}"


def main() -> int:
    df = pd.read_csv(SRC, dtype=str, keep_default_na=False)
    raw = len(df)

    # exact duplicate rows: first occurrence kept
    dup_mask = df.duplicated(keep="first")
    uni = df[~dup_mask].copy()
    dupes = df[dup_mask]
    n_uni, n_dup = len(uni), len(dupes)

    for col in ("units", "unit_price", "amount"):
        uni[col + "_c"] = uni[col].map(cents)
    uni["amt"] = uni["amount_c"]
    uni["neg"] = uni["amt"] < 0
    uni["zero"] = uni["amt"] == 0

    net = int(uni["amt"].sum())
    gross = int(uni.loc[~uni["neg"], "amt"].sum())
    refunds = int(-uni.loc[uni["neg"], "amt"].sum())
    dupe_signed = int(dupes["amount"].map(cents).sum())

    neg_rows = uni[uni["neg"]]
    zero_rows = uni[uni["zero"]]
    miss_region = uni[uni["region"].str.strip() == ""]

    # monthly totals via datetime, not string slicing
    uni["month"] = pd.to_datetime(uni["date"], format="%Y-%m-%d").dt.strftime("%Y-%m")
    monthly = uni.groupby("month")["amt"].sum().astype(int).sort_index()

    # product rankings
    net_by_prod = uni.groupby("product")["amt"].sum().astype(int).sort_values(ascending=False)
    uni["units_i"] = uni["units"].astype(int)
    units_by_prod_all = uni.groupby("product")["units_i"].sum().sort_values(ascending=False)
    units_by_prod_norefund = uni[~uni["neg"]].groupby("product")["units_i"].sum().sort_values(ascending=False)

    # price consistency (positive rows only, like the profiler)
    bad = uni[(~uni["neg"]) & (uni["units_i"] * uni["unit_price_c"] != uni["amt"])]

    print("== INDEPENDENT CROSS-CHECK (pandas / integer cents) ==")
    print(f"rows: {raw} raw = {n_uni} unique + {n_dup} duplicates")
    print(f"identity holds: {raw == n_uni + n_dup}")
    print(f"NET   : {fmt(net)}")
    print(f"GROSS : {fmt(gross)}")
    print(f"refund: {fmt(refunds)} across {len(neg_rows)} rows {sorted(neg_rows['order_id'].tolist())}")
    print(f"net == gross - refunds: {net == gross - refunds}")
    print(f"zero rows: {len(zero_rows)} {sorted(zero_rows['order_id'].tolist())}")
    print(f"missing region: {len(miss_region)} rows, signed value {fmt(int(miss_region['amt'].sum()))}")
    print(f"DUPLICATE rows: {n_dup}, SIGNED value {fmt(dupe_signed)}")
    dup_neg = dupes[dupes["amount"].map(cents) < 0]
    print(f"  duplicate rows that are refunds: {len(dup_neg)} {dup_neg['order_id'].tolist() if len(dup_neg) else ''}")
    print(f"  unsigned (positive-only) duplicate value: {fmt(int(dupes[dupes['amount'].map(cents) > 0]['amount'].map(cents).sum()))}")
    print(f"price-consistency violations: {len(bad)} {bad['order_id'].tolist() if len(bad) else ''}")
    print("NET by month:")
    for m, v in monthly.items():
        print(f"  {m}: {fmt(v)}")
    print(f"monthly sum == NET: {int(monthly.sum()) == net}")
    print("NET by product (desc):")
    for p, v in net_by_prod.items():
        print(f"  {p}: {fmt(v)}")
    print("UNITS by product, all unique rows (desc):")
    for p, v in units_by_prod_all.items():
        print(f"  {p}: {int(v)}")
    print("UNITS by product, positive rows only i.e. refunds netted out (desc):")
    for p, v in units_by_prod_norefund.items():
        print(f"  {p}: {int(v)}")
    rank_all = list(units_by_prod_all.index)
    rank_nrf = list(units_by_prod_norefund.index)
    print(f"units ranking unchanged after netting refunds: {rank_all == rank_nrf}")
    print(f"date range: {uni['date'].min()} .. {uni['date'].max()}")
    print(f"regions: {sorted(uni['region'].str.strip().unique().tolist())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
