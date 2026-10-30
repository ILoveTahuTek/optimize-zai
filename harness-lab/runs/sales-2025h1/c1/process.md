# Process Log — c1 / sales-2025h1

## Steps taken

1. **Read the harness instructions** at `/home/z/my-project/harness-lab/harnesses/c1/INSTRUCTIONS.md`, the method skill `/home/z/my-project/harness-lab/harnesses/c1/skills/data-hygiene/SKILL.md`, and skimmed the profiler script `/home/z/my-project/harness-lab/harnesses/c1/scripts/profile_csv.py` to understand its definitions before running anything.

2. **Profiled first (skill step 1–2).** Ran:
   ```
   python3 /home/z/my-project/harness-lab/harnesses/c1/scripts/profile_csv.py /home/z/my-project/harness-lab/tasks/sales-2025h1/sales.csv
   ```
   Output: 128 raw = 120 unique + 8 duplicates; NET 48,755.00; GROSS 49,015.00; refunds 260.00 (4 rows); 0 zero rows; 4 missing-region rows worth 2,190.00; 0 price violations. Evidence base saved by the profiler to `/home/z/my-project/harness-lab/tasks/sales-2025h1/profile.json` (read in full).

3. **Independent cross-check (skill step 3).** Wrote a deliberately different second implementation at `/home/z/my-project/harness-lab/runs/sales-2025h1/c1/crosscheck.py`:
   - pandas `read_csv(dtype=str)` + `drop_duplicates(keep="first")` instead of stdlib `csv.DictReader` + set-of-tuples dedup;
   - integer-cents arithmetic instead of `Decimal`;
   - `pd.to_datetime(...).strftime("%Y-%m")` month keys instead of string slicing `date[:7]`;
   - groupby aggregations for monthly/product totals and units rankings.
   Ran it; every headline number matched the profiler exactly (row counts, NET, GROSS, refund total + IDs, zero rows, missing-region count/value, all 6 monthly totals, product totals, price violations).

4. **Supplemental queries** (heredoc pandas): details of the 4 refund rows, the 4 missing-region rows, Laptop revenue share, monthly shares, and the SIGNED value of the 8 duplicate rows (5,115.00) — see assumptions below.

5. **Wrote the deliverable** `report.md` and this `process.md`.

## Commands / scripts run

- `python3 /home/z/my-project/harness-lab/harnesses/c1/scripts/profile_csv.py <input.csv>` (profiler)
- `python3 /home/z/my-project/harness-lab/runs/sales-2025h1/c1/crosscheck.py` (my cross-check; left in place as an audit artifact)
- One-off pandas heredoc for row-level detail (refunds, missing regions, shares); not saved as a file.

## Assumptions made

1. **"Units" definition for best-selling:** I treat refund rows as *negative* units (mirroring the NET convention) as primary — Keyboard 75 — and also report the exclude-refunds view (Keyboard 79). Both give the same ranking, so the choice doesn't affect any conclusion. (Refund rows carry positive `units` with negative `amount`; netting subtracts their units.)
2. **Duplicate-row value:** the INSTRUCTIONS demand a SIGNED value, but the profiler only prints a positive-only sum (5,205.00). I computed the signed sum independently (+5,115.00) and disclosed both figures and their difference (one duplicated refund, ORD-0078, −90.00) in the report.
3. **Missing-region rows** are kept in all revenue totals (they are valid unique sales); only region-level breakdowns would be affected. They were not imputed.
4. **Date coverage** assumed complete H1 (Jan–Jun); the data confirmed 2025-01-01..2025-06-28 with all six months present.

## Uncertainties / things I was unsure about

- The profiler's positive-only "duplicates add 5205.00" line vs. the skill's signed-value requirement is a genuine mismatch in the tooling; I resolved it by reporting both and flagging which one the method requires. No disagreement in any *revenue* number.
- No pandas dependency was guaranteed by the harness; I checked (`import pandas` succeeded) before relying on it for the cross-check. The integer-cents parsing would raise on malformed amounts — none existed.
- `profile.json` is written next to the *input* CSV, not the run directory; I left it there since it is the profiler's auditable trail, and referenced it in the report.
- Everything else matched exactly; there were no discrepancies requiring the skill's "STOP and disclose" path.
