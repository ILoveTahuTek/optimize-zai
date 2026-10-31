# Process Log — sales-2025h1-dirty / base harness

## Steps taken

1. **Read harness instructions** at `/home/z/my-project/harness-lab/harnesses/base/INSTRUCTIONS.md`. Role: data analyst; deliverable = factual, concise report with total revenue, best-selling product, monthly revenue breakdown, anything else notable. Harness dir contained no other files/skills.
2. **Inspected the data** by reading `/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv` in full (141 data rows + header). Visual scan revealed the "dirty" aspects: repeated rows, negative amounts, empty `region` cells, two `DD/MM/YYYY` dates, a zero-unit row, and a Monitor price that changes mid-period.
3. **Wrote an analysis script** `analyze_sales.py` (pure Python 3 stdlib — no pandas, to avoid dependency risk) saved in this run directory. It:
   - parses dates tolerantly (`%Y-%m-%d` first, then `%d/%m/%Y`), normalizing and logging non-ISO dates;
   - detects exact duplicate rows (full tuple match) and separately checks for the same `order_id` with conflicting content;
   - validates `amount == units × unit_price` per row (up to sign);
   - lists negative-amount rows, zero-unit rows, and missing-region rows;
   - checks per-product unit prices and locates the Monitor price changeover;
   - computes net total, gross, refund total, monthly net/gross, product net revenue and unit counts, region revenue, and top orders — all on deduplicated data.
4. **Ran the script** (`python3 analyze_sales.py`) and reviewed output.
5. **Cross-checked derived figures** with a small `python3 -c` sanity pass (monthly sum = 60,215 = net total; refund split by product sums to −2,380; missing-region net = 1,010; unit totals reconcile: 263 positive-order units + 20 refund-row units = 283).
6. **Wrote `report.md`** from the verified numbers, keeping both "net" and "gross" views wherever the refund treatment could change the answer.

## Commands / scripts run

- `python3 --version` → 3.12.16
- `python3 /home/z/my-project/harness-lab/runs/sales-2025h1-dirty/base/analyze_sales.py`
- `python3 -c "..."` (inline arithmetic cross-checks)
- `wc -l` on the CSV (141 lines + header)

Script retained at `/home/z/my-project/harness-lab/runs/sales-2025h1-dirty/base/analyze_sales.py` for reproducibility.

## Key results produced by the script

- 141 rows → 10 exact duplicates dropped → 131 unique orders; no conflicting order_id reuse.
- 2 non-ISO dates normalized (ORD-0071, ORD-0066).
- 11 negative-amount rows, all with positive units and |amount| = units × price; total −2,380.00.
- 1 zero-unit row (ORD-1001); 7 missing-region rows.
- Net revenue 60,215.00 (gross 62,595.00); monthly net: Jan 10,195 / Feb 3,515 / Mar 20,115 / Apr 9,525 / May 11,755 / Jun 5,110.
- Product net revenue: Laptop 40,000 · Monitor 10,510 · Headset 5,520 · Keyboard 4,185. Units: Keyboard 97 / Headset 78 / Monitor 56 / Laptop 32 on positive orders.
- Monitor price 210 → 220 between 2025-04-28 and 2025-05-07. All rows satisfy amount = units × price.

## Assumptions made

1. **Exact-row duplicates are data-entry artifacts**; first occurrence kept, later identical rows dropped. (No case of a reused order_id with different content, so this was unambiguous.)
2. **Negative amounts = refunds/returns**, not sign errors, because magnitude exactly equals units × unit_price in every case. Headline "total revenue" is therefore net; gross also reported.
3. **`DD/MM/YYYY` interpretation** for the two odd dates: `29/05/2025` → 29 May 2025, `14/05/2025` → 14 May 2025. Safe here because day > 12 in both cases rules out the reversed reading; both land inside the H1 window.
4. **Zero-unit and missing-region rows retained** (not deleted); zero-unit contributes 0.00, missing regions reported as "(missing)".
5. **"Best-selling" is ambiguous** (revenue vs units), so the report states both: Laptop by revenue, Keyboard by units/order count.

## Things I was unsure about

- Whether negative amounts are truly refunds or data-entry sign flips — if the latter, "total revenue" would be 62,595.00. Both numbers are in the report; net was chosen as headline since refund-like rows are a common real-world pattern and the magnitudes are internally consistent.
- Whether June looks low (5,110) because the export stops at 2025-06-27 (partial month) or because of genuine seasonality; flagged as a caveat rather than resolved.
- Whether the 10 duplicated rows were intentional (e.g., re-imported batches). Nothing in the data distinguishes originals from copies; removal is the standard treatment.
- Whether ORD-1001 (0 units, 0.00) should be excluded as a test record — kept, since it does not affect any monetary figure.

## Deliverables produced

- `report.md` — final analysis report (this directory)
- `process.md` — this log
- `analyze_sales.py` — reproducible analysis script (this directory)
