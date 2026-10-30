# Process Log — sales-2025h2 / c1 (adopted-harness rollout)

Date: 2025-10-30. Harness: `/home/z/my-project/harness-lab/harnesses/c1/` (INSTRUCTIONS.md + skills/data-hygiene + scripts/profile_csv.py). Task: analyze `/home/z/my-project/harness-lab/tasks/sales-2025h2/sales.csv`, deliver `report.md` here.

## Steps taken (in order)

1. **Read the harness.** Read `INSTRUCTIONS.md`, `skills/data-hygiene/SKILL.md`, and `scripts/profile_csv.py` (incl. its docstring definitions) before touching the data.
2. **Inspected the input** without computing anything: `Read` first 30 lines; `wc -l` (119 newlines; file ends `\r\n`, so 119 lines = 1 header + 118 data rows). Noted CRLF line endings, no quote characters (`grep -c '"'` = 0), which later justified parsing by plain `split(',')` in the cross-check.
3. **Ran the profiler (evidence base):**
   `python3 /home/z/my-project/harness-lab/harnesses/c1/scripts/profile_csv.py /home/z/my-project/harness-lab/tasks/sales-2025h2/sales.csv`
   → 118 raw = 112 unique + 6 dupes; NET 290,480.00; GROSS 290,850.00; refunds 370.00 across ORD-0052/ORD-0048; 1 zero row ORD-0902; missing region 9 rows / 4,465.00; dupes add 4,630.00; 0 price violations. It also wrote `profile.json` next to the input; read it in full.
4. **Resolved raw-row count discrepancy (investigation, no fix needed):** the `Read` tool reported "120 lines" while `wc -l`/awk/grep all reported 119 — traced to CRLF endings + tool line counting, not a data problem. awk confirmed 0 blank lines; profiler's 118 raw data rows is correct.
5. **Missing-region count sanity check:** naive visual scan found 8 `,,` rows vs profiler's 9; grep/awk enumeration found 10 raw blank-region rows, one of which (ORD-0105) is an exact duplicate → 9 unique. Matches profiler exactly. (Lesson recorded: dedup interacts with quality counts.)
6. **Built the independent cross-check** — `crosscheck.py` (written to this run dir). Deliberately different implementation from the profiler: text parsing via `split(',')`; exact integer **cents** via string manipulation (no float, no Decimal); all aggregation in **SQLite** (`SUM`/`GROUP BY`). Dedup definition itself is fixed by the harness (exact row-content match), so only the computation is independent. Ran it: **21/21 checks PASS, 0 FAIL** (raw/unique/dupe counts, NET, GROSS, refunds + IDs, zero rows, missing-region count/value, all 6 monthly totals, all 4 product nets, signed dupe value). Also asserted internal identities: NET = GROSS − refunds; monthly sum = product sum = NET.
7. **Best-selling analysis:** units sums per product via SQL both ways (all rows vs refund rows excluded) → ranking Laptop 214 > Keyboard 84 > Headset 76 > Monitor 66 unchanged by refund netting (74/65 after netting). Net-revenue ranking from product nets. Cross-checked duplicate order IDs by awk (`ORD-0021/0026/0054/0065/0068/0105`, each ×2).
8. **Notables:** quantified ORD-0901 (200× Laptop, 250,000.00, 2025-09-14) = 86.1% of NET; ex-ORD-0901 NET = 40,480.00 and September drops to 3,280.00. Computed shares (Sep 87.2% of NET, Laptop 92.1%, missing-region 1.5%).
9. **Wrote deliverables:** `report.md` (this dir) following INSTRUCTIONS.md §METHOD REQUIREMENTS point by point (definitions labeled, single "Total revenue" = NET, row-count identity, profiler-exact data-quality numbers incl. signed dupe value, verification table). Then this `process.md`.

## Commands / scripts run

- `python3 /home/z/my-project/harness-lab/harnesses/c1/scripts/profile_csv.py <task csv>` (exact path as instructed)
- `python3 /home/z/my-project/harness-lab/runs/sales-2025h2/c1/crosscheck.py` (my second implementation; kept in the run dir for audit)
- Read/inspect utilities: `wc -l`, `awk` (blank lines, field-6 empties, duplicate-ID enumeration), `grep -c '"'`, `grep -c $'\r'`, `tail | od -c` (trailing-bytes check), plus `Read` on the CSV and `profile.json`.
- One-off arithmetic for shares/ex-ORD-0901 figures via `python3 -c` (formatting only; inputs came from the verified sums).

## Assumptions made

1. **Definitions** are exactly those fixed by the harness/profiler (unique row = first occurrence of exact row-content match; NET/GROSS/refund as specified). I did not invent alternatives; where the harness required a variant (SIGNED duplicate value), I reported both signed and the profiler's positive-only value and noted they coincide here.
2. **Units on refund rows are positive** (quantity ordered, amount negative). I therefore reported units rankings both including refund-row units and netting them out, per the instructions' requirement to test whether netting changes the ranking (it does not).
3. **`amount` is authoritative** for money; `units × unit_price` was used only as a consistency check (0 violations found), not to restate amounts.
4. **CRLF parsing** in the cross-check: file has no quote chars, so `split(',')` is safe; the profiler (csv module, `newline=''`) and my parser agree on all counts, supporting this assumption.
5. The zero-amount row (ORD-0902, 0 units) is treated as a data-quality artifact with no effect on any money or units figure.
6. "Anything else notable" = genuinely salient facts (single-order dominance, immaterial refunds, region gaps, CRLF), kept factual and quantified.

## Things I was unsure about (and how I handled them)

1. **`Read` tool said the file had 120 lines vs 119 from wc/awk/grep.** Investigated (blank lines? trailing newline? CR?) and concluded it is a tool-counting quirk under CRLF, not a data issue; profiler's 118 raw data rows stands. Disclosed here rather than silently ignoring.
2. **Profiler's `duplicate_value_if_counted` is positive-only**, while the skill demands a SIGNED sum. I computed the signed sum independently (+4,630.00) and verified all 6 duplicate rows are positive, so the two coincide for this file — stated explicitly in the report. Had a duplicate refund existed, I would have reported the signed figure as primary and flagged the profiler field's limitation.
3. **Whether "best-selling" should be units or revenue.** Instructions require reporting both when they differ; #1 (Laptop) is the same either way, but places 2–4 differ, so the report carries both tables and names the definition used for each.
4. **Interpretation of "netting refunds" for units** (subtract refund-row units vs treat refunds as negative units) — both interpretations produce the same ordering here (Headset 74/Monitor 65 vs Headset 74/Monitor 65; the refund rows' units simply drop out), so the conclusion "ranking unchanged" is robust.
5. **Where profile.json lands** (next to the input, i.e., in `tasks/sales-2025h2/`, not the run dir). Left it there as the profiler's auditable trail and referenced it; my own cross-check reads it read-only for the comparison table.

## Outcome

- Deliverable: `runs/sales-2025h2/c1/report.md` — NET 290,480.00 (headline), GROSS 290,850.00, refunds 370.00, monthly + product breakdowns, data quality per profiler, verification table (21/21 exact matches, plus extra identity checks).
- No disagreements between profiler and independent recomputation; nothing required the skill's "STOP and disclose" branch.
