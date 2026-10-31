# Process Log — agg2 / sales-2025h1-dirty

Agent: data analyst (agg2 harness). Date of run: this session.
Deliverable: `report.md` (same directory). This file documents how it was produced.

## Steps taken

1. **Read harness instructions** at `/home/z/my-project/harness-lab/harnesses/agg2/INSTRUCTIONS.md`; followed its mandated method (profile first → independent cross-check → verification table → date/price hygiene → labeled definitions → DQ section → assumptions → dual best-selling).
2. **Read the input CSV** `/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv` in full (141 data rows + header, 7 columns) to eyeball the dirt before tooling.
3. **Ran the mandated profiler FIRST** (exact command from instructions):
   `python3 /home/z/my-project/harness-lab/harnesses/agg2/scripts/profile_csv.py /home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv`
   Output: 141 raw = 131 unique + 10 dupes; NET 60,215.00; GROSS 62,595.00; refunds 2,380.00 (11 rows); 1 zero row; 7 missing-region rows (1,010.00); dupes +735.00 if wrongly counted; 0 arithmetic price violations. Wrote `profile.json` next to the CSV.
4. **Wrote an independent cross-check** `crosscheck.py` in the run directory — a deliberately *different* implementation, not a copy of the profiler:
   - dedup via sort + `itertools.groupby` on raw lines (vs profiler's seen-set), with a row-identity assert;
   - **date format census first** (regex per pattern), then an explicit dual-format parser (ISO `yyyy-mm-dd` → `dd/mm/yyyy`), an ambiguity guard (flag dd/mm rows where day ≤ 12 AND month ≤ 12), and a parse-failure list;
   - per-product **unit-price constancy on positive rows** with old/new price and first-affected date (this is a check the profiler does NOT do — its "price violations" check is only `units×price==amount` arithmetic);
   - units-based best-sellers (gross and net units) alongside net revenue;
   - monthly/gross/refund breakdowns from parsed dates;
   - per-column missing-field census, signed duplicate value, refund-by-month.
   Ran it; wrote `crosscheck.json`.
5. **Compared** every profiler figure against the cross-check — all matched exactly (see Verification table in report.md §3).
6. **Caught and corrected two profiler blind spots:**
   - *Monthly buckets:* profiler slices `date[:7]`, so the two `dd/mm/yyyy` rows landed in junk buckets `"29/05/2"` (180.00) and `"14/05/2"` (80.00), understating May by 260.00. Correct May = 11,755.00; months sum to NET 60,215.00 exactly.
   - *Duplicate value:* profiler reports duplicates' positive value only (+735.00); the SIGNED value is +270.00 because two duplicate rows are refunds (ORD-0014 −420.00, ORD-0083 −45.00). Report discloses both.
7. **Price hygiene:** per-product price constancy found Monitor at two prices (210.00 → 220.00, first affected 2025-05-12; 16 positive rows at old, 10 at new; clean step change — all rows before the date at 210, all after at 220). All other products constant. Arithmetic consistency `units×price==amount` verified on all positive and all refund rows (0 violations).
8. **Context matrix:** ran a small one-off snippet computing net revenue product×month (and later Monitor units by month) to substantiate the "notable" claims; its column sums reconcile with the monthly table.
9. **Self-review pass:** recomputed headline ratios before finalizing; fixed three of my own draft claims (Laptop share is 66.4% not 64.4%; March is ~5.7× February not ~4×; dropped a false "despite fewer units" clause — May–June is also Monitor's best two-month unit stretch, 23 units).
10. **Wrote deliverables:** `report.md` and this `process.md`.

## Commands run

- `mkdir -p /home/z/my-project/harness-lab/runs/sales-2025h1-dirty/agg2`
- `python3 /home/z/my-project/harness-lab/harnesses/agg2/scripts/profile_csv.py /home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv`
- `python3 /home/z/my-project/harness-lab/runs/sales-2025h1-dirty/agg2/crosscheck.py` (my own script; source left in the run dir for audit)
- two short `python3 -c` snippets (product×month matrix; share/unit spot-checks)

## Assumptions made

- Dedup on exact full-row content (mandated); cross-checked that no order_id repeats with *differing* content, so content-based and id-based dedup coincide here (131 unique either way).
- The two `dd/mm/yyyy` rows are day-first — unambiguous because day > 12.
- Missing-region rows stay in all money totals (only `region` is missing); disclosed separately (+1,010.00 signed: 1,170.00 sales − 160.00 refund ORD-0043).
- Zero-amount row (ORD-1001) kept in counts, contributes 0.00 to money.
- NET (not GROSS) is the "Total revenue" headline, per instructions.
- "Best-selling" reported by gross units (Keyboard, 97) AND by net revenue (Laptop, 40,000.00) since they differ; net-units sensitivity shown (ranking unchanged).
- June treated as a partial month (data ends 2025-06-27).

## Things I was unsure about / judgment calls

- Whether "best-selling" should mean units or revenue — instructions require both when they differ; they do, so both are given and the usage is labeled.
- The profiler's `duplicate_value_if_counted` is positive-only; instructions demand the SIGNED value, so I computed +270.00 myself and report both (735.00 / 270.00).
- Refund ORD-0067 (−220.00 on 2025-05-07) is priced at the *new* Monitor price before any positive sale at that price exists (first: 2025-05-12). I report this factually without asserting a cause (original sale not in dataset, or refund mispriced/misdated).
- The profiler's monthly mis-bucketing: I did not "fix" profile.json; the report's monthly table comes from the independently parsed dates, and the discrepancy is documented in report §3.
- The one-off product×month snippet hardcoded a May fallback for the 2 non-ISO rows; acceptable only because crosscheck.py's real parser proved both are May 2025 (0 parse failures, 0 ambiguous). The authoritative monthly figures in the report come from crosscheck.py.

## Artifacts

- `report.md` — deliverable.
- `crosscheck.py`, `crosscheck.json` — independent verification implementation and its output (kept for audit).
- `profile.json` — profiler output, written next to the source CSV at `/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/profile.json`.
