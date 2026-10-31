# Process Log — inv2, task sales-2025h1-dirty

Date: 2025-10-30 (workspace clock). Harness: `/home/z/my-project/harness-lab/harnesses/inv2/INSTRUCTIONS.md`.

## Steps taken

1. **Read the harness instructions** (`INSTRUCTIONS.md`). Requirements extracted: report to `runs/sales-2025h1-dirty/inv2/report.md`; executive summary = exactly three one-sentence, decision-relevant takeaways with numbers kept to the body; mandatory Assumptions & Limitations section listing every judgment call with the alternative considered; so-what opening sentence per section; no silent normalization — every affected-row count reported; inline "(definition-dependent)" flags on headline figures that depend on a choice.
2. **Inspected the input** `tasks/sales-2025h1-dirty/sales.csv` (142 lines = header + 141 data rows + trailing newline; 7,368 bytes). Read the full file manually to eyeball the dirt before coding: spotted mixed date formats, negative amounts, blank regions, repeated order_ids, a zero-unit row, and two price points for Monitor.
3. **Wrote the audit script** `runs/sales-2025h1-dirty/inv2/analyze.py` (pure stdlib: csv, datetime, collections — no pandas dependency). It reports, with counts: raw row count; date-format anomalies; exact duplicates (full-row key incl. order_id) and their amount sum; order_id conflicts; refund rows and whether |amount| = units × unit_price; arithmetic inconsistencies; zero-unit rows; missing-region rows; gross/refund/net totals (deduped and raw); per-product units/revenue with price histories; monthly gross/refunds/net; regional net revenue.
4. **Ran the script**: `python3 .../inv2/analyze.py`. Key outputs captured below.
5. **Ran a second, independent cross-check** (inline `python3 -c` one-off, not saved as a file): month × product net-revenue cross-tab, laptop gross units per month, per-product gross vs refund units, and refund rates. Confirmed the drivers of monthly swings.
6. **Verified internal consistency** (all via the scripts): every row satisfies amount = units × unit_price (0 mismatches); product, monthly and regional views each sum to 60,215.00 = gross 62,595.00 − refunds 2,380.00; 131 unique rows ↔ 131 distinct order_ids; none of the 11 refund order_ids has a positive counterpart anywhere in the file (they are standalone negative entries).
7. **Caught and fixed one bug in my own cross-check**: a one-off verification script built its dedup key including the injected `_line` field, so it reported "141 unique rows". Re-ran with the 7 CSV fields only → 131 unique rows, matching analyze.py. No output was written from the buggy run.
8. **Wrote `report.md`** following the METHOD REQUIREMENTS, then this `process.md`.

## Commands run

- `wc -l` / `ls -la` on the task directory (file size + line count).
- `python3 /home/z/my-project/harness-lab/runs/sales-2025h1-dirty/inv2/analyze.py`
- Three inline `python3 -c` cross-checks (cross-tab, refund pairing, uniqueness — one of which had the `_line` bug and was re-run).
- `mkdir -p /home/z/my-project/harness-lab/runs/sales-2025h1-dirty/inv2`

## Key numbers produced (for traceability)

- 141 raw data rows → 131 unique after removing 10 exact duplicates (their amounts sum to +270.00; raw net sum 60,485.00 vs deduped 60,215.00).
- Gross 62,595.00; refunds −2,380.00 (11 rows, each exactly = units × unit_price, no positive counterpart rows); net 60,215.00.
- Net units: Keyboard 93, Headset 69, Monitor 49, Laptop 32 (gross 97/78/56/32; refunded 4/9/7/0).
- Net revenue: Laptop 40,000.00 (66.4%), Monitor 10,510.00, Headset 5,520.00, Keyboard 4,185.00.
- Monthly net: Jan 10,195 / Feb 3,515 / Mar 20,115 / Apr 9,525 / May 11,755 / Jun (to 27th) 5,110.
- Anomalies: 2 DD/MM/YYYY dates (ORD-0071 "29/05/2025", ORD-0066 "14/05/2025"); 7 missing-region rows (1,010.00 net); 1 zero-unit row (ORD-1001); Monitor price step 210.00 → 220.00 between 2025-04-28 and 2025-05-07; 0 order_id conflicts; 0 arithmetic mismatches; 0 unparseable dates.

## Assumptions made (mirrored in the report's Assumptions & Limitations)

1. Exact full-row duplicates = re-entry artifacts → keep first occurrence, drop 10 repeats.
2. Negative amounts = full-quantity refunds → net against revenue; subtract their units from unit counts.
3. DD/MM/YYYY rows parsed day-first (forced: 29 and 14 cannot be months).
4. "Best-selling" = most net units (revenue view reported alongside because it inverts the ranking).
5. Missing regions bucketed as "(missing)", not imputed or dropped.
6. Zero-unit row kept (no financial effect).
7. Refund booked in the month of its own row date.
8. June treated as a partial month (data ends 2025-06-27).
9. "Revenue" = the file's `amount` field; currency unstated, no tax/cost fields.

## Things I was unsure about

- **Refunds vs corrections:** the negative rows could in principle be corrections rather than customer returns. The evidence for full-quantity refunds is strong (magnitude = units × unit_price on all 11 rows), but the label "refund" is an interpretation; the financial treatment (netting) is the same either way.
- **Duplicates:** genuinely ambiguous in the abstract (could be two identical same-day orders), but identical order_ids plus zero conflicting content made dedup the defensible choice. I quantified the alternative (+270.00) in the report rather than silently choosing.
- **`amount` vs recomputed value:** I used the `amount` column as authoritative; recomputing units × unit_price would change nothing (0 mismatches), so there is no divergence to report.
- **Executive summary rule:** "Numbers only in the body sections" — I interpreted this as: the summary must contain no figures/quantities, so I wrote it figure-free and pushed all digits into the body. Spelled-out counts were also avoided to be safe.
- **Currency:** not stated anywhere in the file; figures reported as bare amounts.

## Deliverables

- Report: `/home/z/my-project/harness-lab/runs/sales-2025h1-dirty/inv2/report.md`
- Process log: `/home/z/my-project/harness-lab/runs/sales-2025h1-dirty/inv2/process.md` (this file)
- Audit script (reproducible): `/home/z/my-project/harness-lab/runs/sales-2025h1-dirty/inv2/analyze.py`
