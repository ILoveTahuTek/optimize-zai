#!/usr/bin/env python3
"""Compare primary analysis (analysis_primary.json) with the independent awk cross-check
(crosscheck.txt). Prints VERDICT per figure. Also verifies refund magnitudes equal units*price."""
import json, re
from pathlib import Path

D = "/home/z/my-project/harness-lab/runs/sales-2025h1-dirty/dom2"
prim = json.loads((Path(D) / "analysis_primary.json").read_text())
txt = (Path(D) / "crosscheck.txt").read_text().splitlines()

def head(key):
    line = next(l for l in txt if l.startswith(key))
    return dict(re.findall(r"(\w+)=([-\d.]+)", line))

ok = True
def check(name, a, b):
    global ok
    same = a == b
    ok &= same
    print(f"{'MATCH' if same else 'MISMATCH':8s} {name}: primary={a} crosscheck={b}")

r = head("raw=")
check("raw_rows", str(prim["raw_rows"]), r["raw"])
check("unique_rows", str(prim["unique_rows"]), r["unique"])
check("dup_rows", str(prim["exact_duplicate_rows"]), r["dupes"])
check("dup_signed_value", prim["duplicate_signed_value"], r["dup_signed"])

h = head("NET=")
check("NET_revenue", prim["net_revenue"], h["NET"])
check("GROSS_revenue", prim["gross_revenue"], h["GROSS"])
check("refund_total", prim["refund_total"], h["REFUND"])

for l in (l for l in txt if l.startswith("MONTH ")):
    f = dict(re.findall(r"(\w+)=([-\d.]+)", l))
    m = re.match(r"MONTH (\S+)", l).group(1)
    p = prim["monthly"][m]
    check(f"month {m} rows", str(p["rows"]), f["rows"])
    check(f"month {m} net", p["net"], f["net"])
    check(f"month {m} gross", p["gross"], f["gross"])
    check(f"month {m} refund", p["refund"], f["refund"])

for l in (l for l in txt if l.startswith("PRODUCT ")):
    f = dict(re.findall(r"(\w+)=([-\d.]+)", l))
    p = re.match(r"PRODUCT (\S+)", l).group(1)
    pp = prim["products"][p]
    check(f"product {p} units_sold", str(pp["units_sold"]), f["units_sold"])
    check(f"product {p} units_ref", str(pp["units_ref"]), f["units_ref"])
    check(f"product {p} net_revenue", pp["net"], f["net"])
    check(f"product {p} gross_revenue", pp["gross"], f["gross"])

tail = next(l for l in txt if l.startswith("missing_region"))
f = {}
for tok in tail.split():
    k, _, v = tok.partition("=")
    f[k] = v
check("missing_region_rows", str(len(prim["missing_region_rows"])), f["missing_region"])
check("unparsed_dates", str(len(prim["unparsed_dates"])), f["unparsed"])
ref_mm = f.get("refund_mag_mismatch", "").strip()
print("refund |amount| == units*price for all refund rows:", ref_mm == "" or ref_mm == "-")
print("positive-row amount == units*price mismatches:", f.get("amount_mismatch_pos", "").strip() or "none")
print("\nOVERALL:", "ALL FIGURES MATCH" if ok else "DISCREPANCIES FOUND")
