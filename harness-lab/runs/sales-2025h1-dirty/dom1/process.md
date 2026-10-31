# Process Log — dom1 probe on sales-2025h1-dirty

## What I was asked to do

Per `harnesses/dom1/INSTRUCTIONS.md`: profile the CSV first, compute the analysis from the
profiler's evidence base using the fixed NET/GROSS/refund definitions, do one independent
cross-check, and write a factual report (headline NET, gross separate, row-count identity,
exact-number data-quality section, best-selling by units AND by revenue, notable findings).

Input: `/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv`
Deliverable: `/home/z/my-project/harness-lab/runs/sales-2025h1-dirty/dom1/report.md`

## Steps taken, in order

1. **Read INSTRUCTIONS.md** and listed the harness dir. Found `scripts/profile_csv.py`; the
   instructions also reference `skills/data-hygiene/SKILL.md`, which does NOT exist in the
   harness directory (see "Issues / uncertainties" below).
2. **Ran the profiler (mandatory first step, before any own computation):**
   `python3 harnesses/dom1/scripts/profile_csv.py tasks/sales-2025h1-dirty/sales.csv`
   Output: 141 raw = 131 unique + 10 dupes; NET 60215.00; GROSS 62595.00; refunds 2380.00
   across 11 IDs; 1 zero row (ORD-1001); 7 missing-region rows worth 1010.00; 0 price
   violations; net by product; net by month **including two spurious month keys**
   `29/05/2` (180.00) and `14/05/2` (80.00). Profiler also wrote
   `tasks/sales-2025h1-dirty/profile.json`.
3. **Read the full CSV** (143 lines) to understand the anomalies behind the profiler output:
   found the two DD/MM/YYYY dates (ORD-0071, ORD-0066 — both May 2025), the zero-unit row,
   the 7 blank-region rows, and verified visually that the duplicate rows are byte-identical
   full-row copies with no embedded commas/quotes (so plain comma-splitting is safe).
4. **Independent cross-check** (required by the method): wrote a separate `awk`
   implementation (`crosscheck.awk` in this run dir) rather than reusing the Python code —
   different tool, independently coded definitions. It recomputes the row-count identity,
   NET/GROSS/refunds, duplicate values, zero rows, missing fields (all 7 columns, not just
   region), price consistency, per-product and per-month sums, plus extra checks the
   profiler lacks: normalization of the stray date formats, order_id-collides-with-different-
   content detection, and date-range bounds. Output saved as `crosscheck.out`.
   Every overlapping figure matched the profiler exactly.
5. **Spot-check by hand:** hand-summed the June rows; first attempt gave 3860.00, which
   exposed that I had missed ORD-0069 (1,250.00 laptop, 2025-06-01); with it, June = 5110.00
   ✓ matches both scripts. (My error, not the data's.)
6. **Derived the remaining figures** from the agreed evidence base: unit counts by product
   (sales units = units on positive-amount rows; net units additionally subtract refund-row
   units), monthly shares, refund-by-product split, duplicate-inflation arithmetic
   (+735.00 sales side, −465.00 refund side, +270.00 NET if raw rows were summed).
7. **Wrote report.md**, then this log.

## Commands / scripts run

- `python3 /home/z/my-project/harness-lab/harnesses/dom1/scripts/profile_csv.py <csv>`
- `awk -f runs/sales-2025h1-dirty/dom1/crosscheck.awk <csv>` (my script; two bugs fixed en
  route — see below)
- `od -c` on the file head → confirmed CRLF line endings, no BOM.

## Assumptions made (and why)

1. **Monthly bucketing normalizes the two DD/MM/YYYY dates into their real month (2025-05).**
   The instructions define money figures but not date handling; the raw strings unambiguously
   denote 29 May / 14 May 2025, so excluding them from May (or reporting them as the profiler's
   spurious keys) would misstate the monthly breakdown. I report the normalized numbers and
   disclose the un-normalized view (May 11,495.00 + 260.00 in two stray buckets) in the report.
2. **"Best-selling by units" = sum of `units` on positive-amount rows** ("sales units"), with
   net units (refund units subtracted) shown alongside; the winner (Keyboard) is the same
   under both, so the choice does not change the conclusion.
3. **Deduplication = exact full-row match** (the profiler's definition), not order_id-level:
   I additionally verified no order_id appears twice with *differing* content, so the two
   definitions coincide here.
4. The `duplicate_value_if_counted` figure (735.00) counts only positive-amount duplicates;
   I report the refund-side duplicate value (−465.00) and the combined NET overstatement
   (270.00) explicitly, since "if wrongly counted" is ambiguous on its own.
5. The zero-amount row (ORD-1001) contributes 0 to NET/GROSS and 0 units, so no definitional
   choice is affected by it.

## Issues / uncertainties

- **The referenced skill file is missing.** INSTRUCTIONS.md says the harness includes
  `skills/data-hygiene/SKILL.md`, but `harnesses/dom1/` contains only `INSTRUCTIONS.md` and
  `scripts/profile_csv.py`. I followed the skill's documented *spirit* as restated in
  INSTRUCTIONS.md itself ("evidence base + independent cross-check"): profiler first, then an
  independently implemented cross-check, then a per-figure verification table. (The library
  EXPERIENCE.md confirms the missing-skill behavior is a known probe failure mode — relative
  path references; I did not hunt for the skill outside the harness since its content was
  fully restated in the instructions.)
- **sqlite3 CLI is not installed** in this environment, so the cross-check is awk-based
  instead of SQL-based; awk is still an independent implementation from the Python profiler.
- **Profiler output needed interpretation:** its month buckets are raw `date[:7]`, so the two
  malformed dates surfaced as fake months rather than as an explicit warning. My cross-check
  adds an explicit malformed-date count and normalization.
- **My own awk bugs during development** (all caught and fixed before the figures were used):
  (a) mawk rejects using a name as both array (from `split()`) and scalar loop variable —
  renamed the loop var; (b) forgot to strip `\r` before the header comparison (file is CRLF) —
  header check false-alarmed twice; (c) first version added refund-row units instead of
  subtracting them, which briefly produced impossible "net units > sales units" for
  Keyboard/Headset/Monitor — caught by sanity check, fixed, rerun. Final `crosscheck.out`
  in this directory is from the corrected script.

## Artifacts in this run directory

- `report.md` — the deliverable
- `crosscheck.awk` — independent cross-check implementation
- `crosscheck.out` — its full output (verification evidence)
- `process.md` — this log

The profiler additionally wrote `tasks/sales-2025h1-dirty/profile.json` (next to the input,
per its design).
