# Process Log — inv1 (sales-2025h1)

## Steps taken

1. **Read harness instructions** at `/home/z/my-project/harness-lab/harnesses/inv1/INSTRUCTIONS.md`: definitions (NET / GROSS / Refund), row-count identity, two-way verification, data-quality exact numbers, best-selling by units and revenue.
2. **Inspected the input** `/home/z/my-project/harness-lab/tasks/sales-2025h1/sales.csv` (full read): 7 columns, straightforward CSV. Noted visually: repeated order rows, negative amounts, a few empty `region` cells.
3. **Environment/integrity checks:**
   - `sha256sum` → `4b480867bc41636c9cb75a54421e5855f0fc05c2e302e1b0cdfab067aee2ce9c`
   - `wc -l` → 129 lines (1 header + 128 data rows)
   - `od -c` / `grep -c $'\r'` → all 129 lines are CRLF-terminated (`file` did not flag this — caught only during a diff debugging step, see "Issues" below).
4. **Method A — Python script** (`method_a.py`, stdlib `csv` + `Decimal`, dedup on the tuple of all 7 fields): computed row counts, dup count/value, negative/zero/missing counts, NET/GROSS/Refund, per-month orders/units/gross/refunds/net, per-product orders/units/signed-units/gross/net, per-region orders/net, and an `amount = ±units × unit_price` integrity check. Output: `key=value` lines in `method_a.out`.
5. **Method B — independent mawk script** (`method_b.awk`, `FS=","`, exact-duplicate detection on the full raw line, money in integer cents to avoid float artifacts): computes the same key set. Output: `method_b.out`.
6. **Compared A vs B:** `diff` after removing two cosmetic-only lines (A-only `sha256=…`; B-only explicit `missing_field[…]=0` entries for fields with no missing values). Result: **all shared figures identical**.
7. **Cross-foot checks** (small Python snippet): row identity, NET = GROSS − Refunds, monthly/product/region sums reconcile to headline figures — all True.
8. **Method C — third check via SQLite** (python `sqlite3`, money as REAL, dedup via `SELECT DISTINCT`): raw/unique/dup counts, NET, GROSS, Refund, monthly NET — all match A and B. Output: `sqlite_check.out`.
9. **Wrote deliverables:** `report.md` (this analysis) and this `process.md`.

## Commands run

```
mkdir -p /home/z/my-project/harness-lab/runs/sales-2025h1/inv1
python3 --version ; awk --version
sha256sum …/sales.csv ; file …/sales.csv ; wc -l …/sales.csv
python3 method_a.py > method_a.out
awk -f method_b.awk …/sales.csv > method_b.out
diff method_a.out method_b.out          # first run: header line differed (see Issues)
grep -v '^sha256=' method_a.out > a.norm ; grep -v ']=0$' method_b.out > b.norm
diff a.norm b.norm                      # NORMALIZED DIFF: IDENTICAL
python3 - <<EOF … sqlite3 cross-check … EOF   # → sqlite_check.out
```

## Assumptions made

1. **"Exact duplicate"** = identical in all 7 fields (byte-identical after stripping the CRLF terminator). First occurrence kept; all later identical occurrences counted as duplicates. Money figures use the 120 unique rows.
2. **Month** = first 7 characters of `date` (`YYYY-MM`); all dates are valid, ISO-formatted, within 2025-01-01…2025-06-28.
3. **Best-selling by units** uses `units` exactly as recorded (refund rows carry positive `units` with negative `amount`). Because this is ambiguous, the signed-units alternative (refund units counted negative) was also computed and disclosed in the report — it flips the #1 units spot from Keyboard (79) to Monitor (72 vs 71).
4. **Missing `region`** treated as its own "(missing)" category, not imputed; those 4 rows' amounts are still counted as revenue (they are valid sales).
5. The CSV has no quoted fields or embedded commas (verified: every row has exactly 7 fields and both parsers agree), so awk's `FS=","` is safe; Python's `csv` module used regardless.
6. Duplicated rows are treated as data-entry duplicates to be removed (per instructions), not as legitimate repeat orders.

## Things I was unsure about / issues encountered

- **CRLF line endings:** the first A-vs-B diff showed only the `header=` line differing — Method B had captured the header *before* its `sub(/\r$/,"")` strip. This revealed the file is CRLF throughout (which `file` did not report). Fixed by stripping `\r` before capturing the header; data lines were already handled. Consequence worth noting: awk dedup keys are on `\r`-stripped lines, matching Python's field-level dedup — confirmed by identical dup counts (8) in both methods and SQLite.
- **Units definition for refunds** (see Assumption 3): genuinely ambiguous; reported both views rather than silently picking one.
- **`dup_value` ($5,115.00)** includes the duplicated *negative* row (ORD-0078, −$90.00); labeled in the report so the mixed-sign composition is transparent. Verified by Methods A and B; SQLite confirmed the dup *count* but not the value (noted as "(not computed)" in the report's verification table rather than implying a third confirmation that doesn't exist).
- `file(1)` reporting plain "CSV ASCII text" despite CRLF — no action needed beyond the fix above.

## Deliverables

- `/home/z/my-project/harness-lab/runs/sales-2025h1/inv1/report.md` — final report
- `/home/z/my-project/harness-lab/runs/sales-2025h1/inv1/process.md` — this log
- Supporting artifacts in the same directory: `method_a.py`, `method_b.awk`, `method_a.out`, `method_b.out`, `sqlite_check.out`
