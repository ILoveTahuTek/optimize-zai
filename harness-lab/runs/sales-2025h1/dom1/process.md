# Process Log — dom1 / sales-2025h1

## 1. Steps taken

1. **Read harness instructions** — `/home/z/my-project/harness-lab/harnesses/dom1/INSTRUCTIONS.md`. Listed the harness directory: it contained only `INSTRUCTIONS.md` and `scripts/profile_csv.py`.
2. **Profiled first (mandatory step).** Ran the provided profiler before any own computation:
   `python3 /home/z/my-project/harness-lab/harnesses/dom1/scripts/profile_csv.py /home/z/my-project/harness-lab/tasks/sales-2025h1/sales.csv`
   Output: 128 raw = 120 unique + 8 exact duplicates; NET $48,755.00; GROSS $49,015.00; refunds $260.00 across 4 rows; 0 zero-amount rows; 4 missing-region rows worth $2,190.00; 0 price-consistency violations; net by product and by month. It also wrote `profile.json` next to the input file (`tasks/sales-2025h1/profile.json`).
3. **Read the full CSV** (128 data rows + header, CRLF line endings) to sanity-check what the profiler saw.
4. **Independent cross-check (evidence base + verification).** Wrote `verify_dom1.py` (in this run directory) that deliberately uses a different implementation from the profiler: sort-based dedup instead of a hash set; manual CRLF normalization + `csv.reader` instead of `csv.DictReader`; exact `Decimal` arithmetic. It recomputes every headline figure, asserts internal identities (raw = unique + dupes; gross − refunds = net; product/month/region sums = net), and compares each shared figure against the profiler's values. **Result: all 10 shared figures matched exactly ("ALL CHECKS AGREE").** Exit code 0.
5. **Extra checks in the cross-check** (beyond the profiler): `amount = units × unit_price` sign-and-quantity identity including refund rows (0 violations), order_id reuse with conflicting content (none), per-column missing-field counts (only `region` missing, 4 rows), date range (2025-01-01 .. 2025-06-28), units by product on both a gross and a net-of-refund-units basis, refunds by month, region breakdown with missing-region bucket, and detailed duplicate/refund row listings.
6. **Wrote the deliverable** `report.md` per the required content (headline NET/GROSS/refund, row-count identity, best-selling by both definitions, monthly breakdown, data-quality section, notables).
7. **Verified both deliverable files exist** in `/home/z/my-project/harness-lab/runs/sales-2025h1/dom1/`.

## 2. Commands / scripts run

- `python3 harnesses/dom1/scripts/profile_csv.py tasks/sales-2025h1/sales.csv` (provided profiler)
- `wc -l`, `tail | od -c`, `awk` one-liner on the CSV — only to resolve a line-count question (see §3), not for analysis.
- `python3 runs/sales-2025h1/dom1/verify_dom1.py` (my independent cross-check; source kept in this directory for audit)
- `mkdir -p runs/sales-2025h1/dom1` (create output directory)

## 3. Assumptions and resolutions

- **Line-count discrepancy investigated:** the Read tool reported "130 lines" while `wc -l` reported 129 and the profiler saw 128 data rows. Resolved: the file has 129 newline-terminated lines (1 header + 128 data rows, CRLF endings, no blank lines); Read's count includes the trailing-newline artifact. No missing or extra data rows.
- **Duplicate-value convention:** the profiler's `duplicate_value_if_counted` ($5,205.00) sums only positive duplicate rows. I reported that figure as "gross" and additionally stated the effect on net of counting all 8 duplicates including the duplicated refund (+$5,115.00), labeled as such in the report.
- **Missing-region rows are kept in all totals** (they are unique rows and the NET definition excludes nothing else); they are shown as their own bucket in the regional breakdown and flagged in data quality.
- **"Best-selling by units" definition:** refund rows carry positive `units` with negative `amount`. I used gross units (units on positive-amount rows) as the primary units metric and disclosed the net-of-refund-units variant in a footnote, because it flips the units ranking (Keyboard 75 → 71 net vs Monitor 72 net).

## 4. Things I was unsure about / deviations

- **Referenced skill missing:** INSTRUCTIONS.md step 1 references `skills/data-hygiene/SKILL.md`, but no such file exists anywhere under `/home/z/my-project` (searched with Glob `**/SKILL.md`; the harness directory contains only the profiler script). I proceeded by following the profiler's docstring definitions (which the instructions say downstream reports must match) and the explicit METHOD REQUIREMENTS in INSTRUCTIONS.md, and I performed the skill's "evidence base + independent cross-check" requirement myself via `verify_dom1.py`.
- **Ground truth not consulted:** `harness-lab/ground_truth.json` exists in the workspace. I deliberately did not open it, to keep this analysis independent; all numbers derive solely from the profiler + my cross-check.
- **No Jun 29–30 rows** (data ends 2025-06-28). Treated as data-as-is for an H1 file, not an error; not adjusted.

## 5. Outputs

- `runs/sales-2025h1/dom1/report.md` — final report
- `runs/sales-2025h1/dom1/process.md` — this log
- `runs/sales-2025h1/dom1/verify_dom1.py` — independent cross-check script (audit trail)
- `tasks/sales-2025h1/profile.json` — profiler output (written by the profiler next to the input)
