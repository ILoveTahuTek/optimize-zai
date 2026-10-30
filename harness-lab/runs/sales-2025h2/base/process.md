# Process Log — sales-2025h2 (base harness)

## What I did, step by step

1. **Read the harness instructions** at `/home/z/my-project/harness-lab/harnesses/base/INSTRUCTIONS.md`. The harness directory contains only `INSTRUCTIONS.md` — no `skills/` or `scripts/` subdirectories, so no additional tooling was provided. Required report contents: total revenue, best-selling product, monthly revenue breakdown, anything else notable; factual and concise.
2. **Read the input CSV** `/home/z/my-project/harness-lab/tasks/sales-2025h2/sales.csv` in full (118 data rows, 7 columns: `order_id, date, product, units, unit_price, region, amount`). During this read I spotted likely data-quality issues worth testing for: apparent duplicate rows, two negative amounts, one huge order (200 units), one zero-unit row, and blank regions.
3. **Created the run directory** `/home/z/my-project/harness-lab/runs/sales-2025h2/base/` (`mkdir -p`), confirmed Python 3.12.16 available.
4. **Wrote and ran an analysis script** `analyze.py` (stdlib only — `csv`, `collections`, no pandas needed). Commands run:
   - `mkdir -p /home/z/my-project/harness-lab/runs/sales-2025h2/base && python3 --version`
   - `python3 /home/z/my-project/harness-lab/runs/sales-2025h2/base/analyze.py`
   The script: counts rows; detects exact duplicate rows; validates `amount == units × unit_price`; flags negative amounts, zero-unit rows, missing regions, and large orders; computes totals on three bases (raw / deduplicated / deduplicated-ex-outlier); breaks down products (orders, units, revenue), months (revenue, order counts), and regions; prints sum checks.
5. **Ran independent sanity checks** with a short inline `python3 -c` snippet: outlier share of total (86.1%), raw-minus-duplicates arithmetic (295,110 − 4,630 = 290,480), product revenue reconciliation (Monitor and Headset revenue reconcile exactly with units minus refunded units), outlier vs. next-largest order (50×).
6. **Wrote the deliverable** `report.md` and this `process.md`.

## Key assumptions

- **Deduplication:** the 6 repeated rows are byte-identical repeats of an earlier row (same order_id, date, product, units, price, region, amount), so I treated them as accidental re-loads, not separate orders, and kept the first occurrence. All headline figures use this deduplicated basis (112 orders).
- **Refunds:** the two negative amounts (ORD-0052 −210.00, ORD-0048 −160.00) are treated as refunds/returns and kept as negative revenue, i.e. totals are net. Their `units` stay positive in the source, so I reported unit counts as-is but noted the +3-unit overstatement in the report.
- **Outlier handling:** ORD-0901 (200 Laptops = 250,000.00) is 86.1% of deduplicated revenue and 50× the next-largest order. I did **not** delete it (it may be a genuine bulk order); instead every key metric is shown with and without it so the reader can choose the basis.
- **"Best-selling product":** ambiguous between units and revenue, so I reported both and called out that the answer differs (Keyboard by units/orders ex-outlier; Laptop by revenue either way).
- **Amount integrity:** `amount == units × unit_price` in magnitude for every row, so I used the `amount` column directly rather than recomputing from units × price.

## Things I was unsure about

- Whether the duplicate rows should be treated as legitimate repeat orders. They share identical order_ids *and* identical values, and order_ids are unique otherwise, which strongly suggests loading duplication — but I can't verify the upstream system.
- Whether ORD-0901 is real (bulk B2B sale) or a units data-entry error (e.g., 2 → 200). Flagged for verification rather than silently excluded or included.
- Whether the zero-unit ORD-0902 is a cancellation or partial data entry; it contributes 0 to all sums either way, so it only affects the order count (112 vs. 111).
- Whether the missing-region rows represent a real "unknown/online" segment or an extract defect. I report them as `(missing)` rather than imputing.
- The instructions say "total revenue" without specifying a basis; I made the deduplicated net figure the headline and showed raw and ex-outlier figures alongside, with the reasoning stated in the report.

## Outputs produced

- `/home/z/my-project/harness-lab/runs/sales-2025h2/base/report.md` — deliverable report
- `/home/z/my-project/harness-lab/runs/sales-2025h2/base/analyze.py` — reproducible analysis script (run: `python3 analyze.py`)
- `/home/z/my-project/harness-lab/runs/sales-2025h2/base/process.md` — this log
