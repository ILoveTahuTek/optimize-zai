# Process log — agg1 / sales-2025h1-dirty

## Steps taken (in order)

1. **Read the harness instructions** at `/home/z/my-project/harness-lab/harnesses/agg1/INSTRUCTIONS.md`, then both required skills:
   - `/home/z/my-project/harness-lab/harnesses/agg1/skills/data-hygiene/SKILL.md`
   - `/home/z/my-project/harness-lab/harnesses/agg1/skills/anomaly-watch/SKILL.md`
2. **Detect, then profile** (per the mandated method order): ran both tools on the raw input before computing anything myself.
   - `python3 /home/z/my-project/harness-lab/harnesses/agg1/scripts/profile_csv.py /home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv`
   - `python3 /home/z/my-project/harness-lab/harnesses/agg1/scripts/detect_anomalies.py /home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv`
   - Read the side-car artifacts `profile.json` and `detect.json` (written next to the input by the tools) and the first 30 rows of the CSV to learn the schema: `order_id,date,product,units,unit_price,region,amount`.
3. **Environment checks:** `mkdir -p` for the run dir; `wc -l` (142 lines = 1 header + 141 data rows, matching the profiler); `tail` of the file.
4. **Independent second implementation** (required by INSTRUCTIONS.md #7 and data-hygiene skill step 3): wrote `/home/z/my-project/harness-lab/runs/sales-2025h1-dirty/agg1/verify.py` — stdlib `csv` only, dedupe on the full 7-field row tuple (first occurrence kept), explicit dual-format date parse (ISO `%Y-%m-%d` first, then day-first `%d/%m/%Y`), and recomputation of every headline figure: NET/GROSS/refunds, zero/missing/dupe counts, monthly + product breakdowns, signed & absolute units, price-change cutover, top-5 orders.
5. **Investigated the one apparent disagreement** (duplicate value 735.00 vs my 270.00):
   - Recomputed duplicates standalone (listed all 10 duplicated rows with amounts).
   - Read the profiler source `profile_csv.py`. Root cause: its `dupe_value` sums **positive duplicate amounts only** (`if Decimal(r["amount"]) > 0`), dropping two duplicated refunds (ORD-0014 −420.00, ORD-0083 −45.00). Positive-only = 735.00; signed = 270.00. Raw-row sum = 60,485.00 = NET 60,215.00 + 270.00, confirming the signed figure is the true overstatement. Disclosed prominently in the report (Anomaly section + Verification table) rather than silently picking one, per the skill.
   - Also identified that the profiler's `net_by_month` uses `date[:7]` string slicing, which is why the 2 DD/MM/YYYY rows show as malformed keys `29/05/2` / `14/05/2` (180.00 + 80.00). My dual-format parse folds them into 2025-05 → May 11,755.00. Required by the anomaly-watch skill ("handle exactly those N rows with an explicit dual-format parse"). No other month differs; totals reconcile at 60,215.00.
6. **Drill-down queries** (ad-hoc python3 heredocs, stdlib only): inspected ORD-0067 / ORD-1001 / ORD-0071 / ORD-0066 and the top-5 orders; enumerated all Monitor@220 rows (cutover: last @210 = 2025-04-28; first affected = refund ORD-0067 2025-05-07; first revenue order @220 = ORD-0038 2025-05-12; 11 rows @220); NET by region; month-over-month deltas; GROSS by product + unit counts (to fix the product table); min/max dates (2025-01-01 → 2025-06-27, nothing outside H1).
7. **Wrote the deliverable** `report.md`, then corrected two figures after recomputation (GROSS-by-product column; a transcription typo "5,115" → 5,110 in the verification table).
8. **Wrote this process log.**

## Assumptions made

- "Exact duplicate" = identical content in all 7 fields (the tools' definition, confirmed by reading the profiler source). Dedupe-by-order_id was considered and rejected as unnecessary — verified equivalent here (10 IDs × 2 identical copies each).
- Refund rows keep positive `units`; for "best-selling by units" I sign units by the amount's sign (net units) and also report absolute units. Keyboard leads under both conventions, so the conclusion is convention-independent.
- The 2 non-ISO dates are day-first (`29/05/2025` cannot be ISO — month 29 is invalid), so the parse is unambiguous; both map to May 2025.
- Zero row ORD-1001 (units=0) and the 7 missing-region rows (1,010.00 NET) are kept in all revenue totals and only flagged.
- NET (not GROSS) is the headline "Total revenue", per INSTRUCTIONS.md #3.

## Uncertainties / judgment calls

- **Profiler's "duplicates add 735.00" vs signed 270.00:** resolved as a definitional difference in the tool (positive-only sum), not a data error; both figures appear in the report with the reconciliation (735.00 = 270.00 + 465.00 of duplicated refunds). INSTRUCTIONS.md #5 requires the signed value, so 270.00 is used for the anomaly section and the tool's 735.00 is quoted verbatim with the caveat.
- **First affected order for the Monitor price change:** the detector reports the change but not the first affected order. I defined "first affected" as the earliest-dated unique row carrying the new 220.00 price — which turned out to be a refund (ORD-0067, 2025-05-07); I also state the first *revenue* order at 220.00 (ORD-0038, 2025-05-12) and the last order at 210.00 (2025-04-28) so the reader can choose the interpretation.
- **June −56.5% MoM:** June has 21 rows (same as May) and activity through 2025-06-27, so I treated the decline as real rather than truncation, with a volatility caveat.
- Whether the profiler's `net_by_month` garbage keys should be "fixed" in my table or echoed verbatim: I report my dual-format monthly table (correct attribution) and disclose the tool's raw output in the Verification table footnote, per the skills' cross-check-and-disclose requirement.

## Artifacts

- `/home/z/my-project/harness-lab/runs/sales-2025h1-dirty/agg1/report.md` — deliverable report
- `/home/z/my-project/harness-lab/runs/sales-2025h1-dirty/agg1/verify.py` — independent second implementation (audit trail)
- `/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/profile.json` and `detect.json` — tool outputs (written by the tools next to the input)
