# Process Log — inv1 / sales-2025h1-dirty

Date: 2025 session. Agent: solver (data-analyst role per `harnesses/inv1/INSTRUCTIONS.md`).

## Steps taken

1. Read the harness instructions at `harnesses/inv1/INSTRUCTIONS.md`. The harness directory contained only `INSTRUCTIONS.md` — no `skills/` or `scripts/` present, so no additional tools to load.
2. Inspected the task data `tasks/sales-2025h1-dirty/sales.csv` (142 lines = 1 header + 141 data rows; 7 columns: order_id, date, product, units, unit_price, region, amount). Visual scan revealed expected dirt: repeated rows, negative amounts, empty `region` cells, one 0-unit/0-amount row, two DD/MM/YYYY dates.
3. Checked tooling: Python 3.12.16 with pandas 2.2.3 available. Created run directory `runs/sales-2025h1-dirty/inv1/`.
4. Wrote **`verify1.py`** — independent method A: pure stdlib (`csv` module), manual exact-duplicate removal via full-row tuple set (keep first), `Decimal` arithmetic. Computes: raw/unique/dup counts, net, gross, refund, negative-row count, zero-amount rows, missing-field rows (unique and raw), monthly net/gross/refund (with DD/MM/YYYY normalization), product revenue/units aggregations, plus sanity checks (amount vs ±units×unit_price, conflicting order_ids, per-product price sets).
5. Wrote **`verify2.py`** — independent method B: pandas `read_csv(dtype=str)` + `drop_duplicates` + `groupby`. Same definitions.
6. Ran both scripts. All outputs matched exactly (net 60,215.00; gross 62,595.00; refund 2,380.00; 141 = 131 + 10; 11 negative rows; 1 zero row; 7 unique missing-region rows; identical monthly and product tables).
7. Ran a **third independent method C** (shell/awk): `awk` with an in-script `seen[]` dedup, and `sort | uniq -cd` to list duplicate lines. Results matched A and B. The `sort | uniq -c` listing also confirmed every duplicated row appears exactly twice and no order_id repeats with differing content.
8. Wrote an awk one-liner to value the 10 duplicate copies: gross 735.00 / net 270.00 (first attempt mis-parsed the field index because `uniq -c` prefixes whitespace; fixed by splitting the row on commas — noted as a self-corrected stumble).
9. Hand cross-checks (mental arithmetic, documented in report): gross − refund = net (62,595 − 2,380 = 60,215); monthly net sums to net; product net sums to net; refund units reconcile per product (e.g., Keyboard 97 sold + 4 refund units = 101 |units|; Headset 78 + 9 = 87; Monitor 56 + 7 = 63; Laptop 32 + 0 = 32).
10. Wrote deliverable `report.md` per the instruction template (Total revenue with single NET headline; labeled gross/refund; row-count identity; best-selling by both units and revenue with the chosen definition stated; monthly breakdown; data-quality section with exact counts/values; Verification section; notable findings).

## Commands / scripts run

- `mkdir -p runs/sales-2025h1-dirty/inv1`
- `python3 verify1.py` and `python3 verify2.py` (scripts kept in the run dir for audit)
- awk dedup+aggregate one-liner over the CSV (method C)
- `sort sales.csv | tail -n +2 | uniq -cd` (duplicate listing) and companion awk to value duplicate copies
- awk lookups: first 220.00-Monitor rows (price-change dating), Laptop revenue by month, latest order dates (June completeness check)

## Assumptions

- The header line is not a data row; "raw data rows" = 141.
- "Unique rows" means exact full-row duplicates removed (all 7 columns identical), keep-first; safe because every duplicate appears exactly twice, so keep-first vs keep-last is irrelevant.
- The two DD/MM/YYYY dates (ORD-0071, ORD-0066) are interpreted as day-first (29 May, 14 May 2025) and assigned to 2025-05; all other dates are ISO YYYY-MM-DD.
- "Units sold" for best-selling-by-units = units on positive-amount (sale) rows; a |units|-over-all-rows variant is also reported and does not change the ranking.
- Missing fields = empty cells; only `region` is ever empty; no imputation attempted (region is not needed for any headline figure).
- The zero-amount/0-unit row ORD-1001 is kept in the unique set (contributes 0.00); it is flagged in data quality rather than dropped.
- Currency is whatever the `amount` column denotes (no currency unit given in the data); figures reported unit-less as in the source.
- "Rows with missing fields" is reported on unique rows (7) with the raw count (9) noted, since money figures are all unique-row based.

## Uncertainties / notes

- verify2.py's duplicate-value merge printed 0.0 due to a flawed pandas merge (overlapping columns); I did not rely on it — duplicate values were confirmed by methods A and C instead. Headline cross-checks in verify2 were unaffected.
- June 2025 appears low (5,110.00 net) but the data ends 2025-06-27; flagged June as likely incomplete rather than a true sales decline.
- I cannot determine from the data whether duplicate/negative rows are legitimate business events or pipeline artifacts; per instructions, dedup is applied and refunds are kept as negatives, and both are documented in the report.
