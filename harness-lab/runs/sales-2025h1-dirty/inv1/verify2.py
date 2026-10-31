#!/usr/bin/env python3
"""Verification script 2: pandas-based, independent code path from verify1.py.

Same definitions; all money figures over UNIQUE rows (drop_duplicates on all
columns). Used only to cross-check verify1.py outputs.
"""
import pandas as pd

PATH = "/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv"

df = pd.read_csv(PATH, dtype=str, keep_default_na=False)
raw_count = len(df)

df_u = df.drop_duplicates(keep="first").copy()
uniq_count = len(df_u)
dup_count = raw_count - uniq_count

df_u["amount_d"] = df_u["amount"].map(lambda s: float(s))
net = round(df_u["amount_d"].sum(), 2)
gross = round(df_u.loc[df_u["amount_d"] > 0, "amount_d"].sum(), 2)
refund = round(-df_u.loc[df_u["amount_d"] < 0, "amount_d"].sum(), 2)
neg_count = int((df_u["amount_d"] < 0).sum())
zero_rows = df_u[df_u["amount_d"] == 0]

missing_mask = (df_u == "").any(axis=1)
missing_ids = df_u.loc[missing_mask, "order_id"].tolist()

def month_of(s):
    s = s.strip()
    if "/" in s:
        dd, mm, yy = s.split("/")
        return f"{yy}-{mm}"
    return s[:7]

df_u["month"] = df_u["date"].map(month_of)
monthly_net = round(df_u.groupby("month")["amount_d"].sum(), 2).to_dict()
monthly_gross = round(df_u[df_u["amount_d"] > 0].groupby("month")["amount_d"].sum(), 2).to_dict()
monthly_refund = round(-df_u[df_u["amount_d"] < 0].groupby("month")["amount_d"].sum(), 2).to_dict()

df_u["units_i"] = df_u["units"].astype(int)
prod_net = round(df_u.groupby("product")["amount_d"].sum(), 2).sort_values(ascending=False).to_dict()
prod_gross = round(df_u[df_u["amount_d"] > 0].groupby("product")["amount_d"].sum(), 2).sort_values(ascending=False).to_dict()
pos = df_u[df_u["amount_d"] > 0]
prod_units = pos.groupby("product")["units_i"].sum().sort_values(ascending=False).to_dict()

# exact duplicate rows (the dropped ones) with their amounts
dup_rows = df.merge(df_u.drop(columns=["amount_d", "month", "units_i"]), how="left",
                    indicator=True).loc[lambda x: x["_merge"] == "left_only"]
dup_value_pos = round(dup_rows["amount"].astype(float).pipe(lambda s: s[s > 0]).sum(), 2)
dup_value_all = round(dup_rows["amount"].astype(float).sum(), 2)

print("=== SCRIPT 2 (pandas) ===")
print(f"raw data rows: {raw_count}")
print(f"unique rows: {uniq_count}")
print(f"exact duplicate rows: {dup_count}")
print(f"NET revenue: {net}")
print(f"GROSS revenue: {gross}")
print(f"Refund total: {refund}")
print(f"negative-amount rows (unique): {neg_count}")
print(f"zero-amount rows (unique): {len(zero_rows)} ids={zero_rows['order_id'].tolist()}")
print(f"missing-field rows (unique): {missing_mask.sum()} ids={missing_ids}")
print(f"dup rows gross value: {dup_value_pos}; dup rows net value: {dup_value_all}")
print("monthly net:", dict(sorted(monthly_net.items())))
print("monthly gross:", dict(sorted(monthly_gross.items())))
print("monthly refunds:", dict(sorted(monthly_refund.items())))
print("product NET rev:", prod_net)
print("product GROSS rev:", prod_gross)
print("product units (positive rows):", prod_units)
