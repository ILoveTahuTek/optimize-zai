# Process Log — dom2 on task `sales-2025h1-dirty`

Agent: data-analyst solver under harness `harnesses/dom2` (INSTRUCTIONS.md followed).
Deliverable: `report.md` (same directory). This file documents how it was produced.

## 1. Steps taken (in order)

1. **Read harness instructions** at `/home/z/my-project/harness-lab/harnesses/dom2/INSTRUCTIONS.md`. Method requirements: run `scripts/detect_anomalies.py` BEFORE computing anything; follow the referenced skill `skills/anomaly-watch/SKILL.md` (verbatim inventory, dual-format dates, price-change disclosure); label NET vs GROSS vs Refund; state the row-count identity; mandatory anomaly section; cross-check every headline figure with a second independent implementation; report best-selling by units AND by net revenue.
2. **Looked for the referenced skill.** `Glob **/anomaly-watch/**` under `/home/z/my-project` returned nothing; the harness directory contains only `INSTRUCTIONS.md` and `scripts/detect_anomalies.py`. → Assumption A1 below.
3. **Ran the detector first**, before any computation:
   `python3 /home/z/my-project/harness-lab/harnesses/dom2/scripts/detect_anomalies.py /home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv`
   Output captured verbatim into report §4; tool also wrote `detect.json` next to the input CSV.
4. **Sanity-checked the raw file** (line/record counts, CRLF check) after initially miscounting rows from the pager: file is 7,368 bytes, CRLF line endings, 142 physical lines = 1 header + **141 data rows**, matching the detector's `raw_rows=141`. No embedded-carriage-return issues.
5. **Primary analysis** (`analysis_primary.py`, Python stdlib + `Decimal`):
   - exact-duplicate removal on the full 7-column row tuple (keep first occurrence);
   - NET = Σ `amount` over unique rows; GROSS = Σ positive; Refund = Σ |negative|;
   - identity check NET = GROSS − Refund;
   - monthly NET/GROSS/refund/rows with dual-format date parse (ISO first, then `DD/MM/YYYY`; anything else → UNPARSED list);
   - per-product units sold (positive rows), units on refund rows, net/gross revenue, order counts;
   - Monitor price timeline per price point;
   - `amount == units × unit_price` consistency check; order_id content-conflict check; region split; top-5 orders.
   Output: printed summary + `analysis_primary.json`.
6. **Independent cross-check** (`crosscheck.awk`, POSIX awk — different language and logic: whole-line dedupe via `seen[$0]++`, format sniff by presence of `-` vs `/` in the date, float arithmetic): computes raw/unique/dup counts, dup signed value, NET/GROSS/Refund, per-month rows/net/gross/refund, per-product units/net/gross, missing-region and unparsed counts. Output: `crosscheck_raw.txt` → sorted `crosscheck.txt`.
7. **Automated comparison** (`compare.py`): asserts equality of every shared figure between `analysis_primary.json` and `crosscheck.txt`; also checks refund magnitudes `|amount| == units × unit_price`. Result: **ALL FIGURES MATCH** (no discrepancies; every check MATCH).
8. **Bug caught during cross-check:** the awk consistency check initially compared `units × region` (column 6) instead of `unit_price` (column 5), flagging all rows as mismatches. Fixed (`$4*$5`), re-run; both implementations then agreed there are no positive-row amount mismatches and no refund-magnitude mismatches. Headline figures were unaffected (the bug was in a side check only).
9. **Wrote `report.md`** per the mandated structure (headline NET labeled "Total revenue", GROSS and Refund labeled separately, row-count identity, best-selling by units and by net revenue, monthly breakdown, verbatim anomaly inventory + detailed anomaly section, other notable findings, verification table with both implementations' values).

## 2. Commands run

```
python3 /home/z/my-project/harness-lab/harnesses/dom2/scripts/detect_anomalies.py \
        /home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv
python3 analysis_primary.py
awk -f crosscheck.awk /home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv | sort > crosscheck_raw.txt
python3 compare.py
```
(plus small awk/python one-liners for the CRLF/row-count sanity check; `sed -i` fix of crosscheck.awk col 6→5)

## 3. Artifacts produced

| File | Purpose |
|---|---|
| `report.md` | Deliverable |
| `analysis_primary.py` / `analysis_primary.json` | Primary implementation + its raw output |
| `crosscheck.awk` / `crosscheck.txt` (and `crosscheck_raw.txt`) | Independent implementation + its raw output |
| `compare.py` | Figure-by-figure comparison (verdict: ALL MATCH) |
| `detect.json` | Written by the harness detector next to the input CSV (tool behavior, not relocated) |

## 4. Assumptions

- **A1 (missing skill file):** `INSTRUCTIONS.md` references `skills/anomaly-watch/SKILL.md`, but no such file exists anywhere under the project (globbed). I followed the skill's mandates as restated in INSTRUCTIONS.md (verbatim detector inventory, explicit dual-format date handling, price-change disclosure) and the detector script's documented behavior. Flagging in case the harness intends the skill to ship with it.
- **A2 (dedupe definition):** "unique rows" = exact duplicates across all 7 columns removed, keep-first. Implemented two independent ways (Python tuple key; awk whole-line key) with identical results: 131 unique / 10 duplicates.
- **A3 (duplicate signed value):** reported as the sum of `amount` over the 10 duplicate (2nd-copy) rows = +270.00; since every duplicate is a pair, this equals the overcount raw-vs-unique (60,485.00 − 60,215.00).
- **A4 (refunds):** refund rows carry positive `units`; "units sold" counts positive-amount rows only, and net-of-refund units are reported alongside. All 11 refunds satisfy `|amount| = units × unit_price` (full-line returns), so no partial-credit interpretation was needed.
- **A5 (day-first dates):** `DD/MM/YYYY` interpreted day-first per the detector; both non-ISO rows (29/05, 14/05) have day > 12, so the choice cannot change any month assignment.
- **A6 (zero row):** ORD-1001 (0 units, 0.00) counts as a row but contributes 0.00 to all money figures.
- **A7 (float in cross-check):** awk uses float64; at these magnitudes (≤ 62,595.00) cent-level results are exact after `%.2f` rounding; agreement with Decimal primary confirms it.

## 5. Things I was unsure about

- The referenced anomaly-watch skill being absent (A1) — proceeded per INSTRUCTIONS.md's own restatement.
- Whether "best-selling" should net refunds out of units — resolved by reporting both (ranking is unchanged either way: Keyboard #1 units, Laptop #1 revenue).
- Whether the report should normalize Monitor's 210.00→220.00 price change to a single price — I did **not** normalize (amounts already reflect each row's price); I disclosed the change and its date range instead, per the harness's price-change-disclosure requirement.
- June 2025 is a partial month (data ends 2025-06-27); flagged in the report so the June figure isn't read as a full-month decline.

## 6. Key numbers (for quick reference)

- Raw 141 = unique 131 + exact duplicates 10 (dup signed value +270.00)
- **NET 60,215.00** · GROSS 62,595.00 · Refunds 2,380.00 (11 rows)
- Monthly NET: Jan 10,195 · Feb 3,515 · Mar 20,115 · Apr 9,525 · May 11,755 · Jun 5,110
- Best-selling: Keyboard 97 units sold (by units) vs Laptop 40,000.00 (by NET revenue)
- Anomalies: 10 exact dups; 11 refunds; 1 zero row (ORD-1001); 7 missing-region rows (1,010.00); 2 DD/MM/YYYY dates; Monitor price 210.00→220.00 (May onward)
- Verification: 100% of compared figures MATCH between Python/Decimal and awk implementations.
