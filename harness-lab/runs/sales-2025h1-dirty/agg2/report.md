# Sales Analysis Report — sales-2025h1-dirty

**Source:** `/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv` (141 raw rows, 2025-01-01 → 2025-06-27)
**Evidence base:** `profile.json` (via `profile_csv.py`) + independent cross-check (`crosscheck.py`, second implementation).

---

## 1. Headline

- **Total revenue (NET revenue): 60,215.00** — sum of `amount` over the 131 unique rows, exact duplicates removed, refunds kept as negatives.
- **GROSS revenue: 62,595.00** (positive rows only).
- **Refund total: 2,380.00** (11 unique refund rows). Refunds = 3.80% of gross.

Every money figure below is labeled NET / GROSS / refund per the definitions in §2.

## 2. Definitions used

| Term | Definition |
|---|---|
| Unique row | First occurrence of a row whose full 7-field content is identical to an earlier row |
| Duplicate row | Any later exact content match (10 rows) |
| **NET revenue** | Σ `amount` over unique rows, refunds as negatives — **the "Total revenue" headline** |
| **GROSS revenue** | Σ `amount` over unique rows where `amount > 0` |
| **Refund total** | Σ \|`amount`\| over unique rows where `amount < 0` |

GROSS is never reported as "net".

## 3. Verification (profiler vs. independent cross-check)

Cross-check = `crosscheck.py`: a second implementation with different mechanics (sort+groupby dedup on raw lines vs. seen-set; explicit dual-format date parser vs. string slicing; Decimal throughout). All figures match exactly.

| Figure | profile_csv.py | crosscheck.py | Match |
|---|---:|---:|:--:|
| Raw rows | 141 | 141 | ✔ |
| Unique rows | 131 | 131 | ✔ |
| Exact duplicate rows | 10 | 10 | ✔ |
| **NET revenue** | 60,215.00 | 60,215.00 | ✔ |
| **GROSS revenue** | 62,595.00 | 62,595.00 | ✔ |
| **Refund total** | 2,380.00 | 2,380.00 | ✔ |
| Refund rows (unique) | 11 | 11 | ✔ |
| Zero-amount rows | 1 (ORD-1001) | 1 (ORD-1001) | ✔ |
| Missing-region rows (unique) | 7 | 7 | ✔ |
| Missing-region signed value | 1,010.00 | 1,010.00 | ✔ |
| Net by product (all 4) | §7 | identical | ✔ |
| Net by month | §8* | identical after date fix | ✔ |
| Months sum to NET | — | 60,215.00 = 60,215.00 | ✔ |

\* The profiler buckets months by `date[:7]`, which mis-files the two non-ISO dates into spurious buckets `"29/05/2"` (180.00) and `"14/05/2"` (80.00), understating May by 260.00. Corrected in §8 via the dual-format parser.

## 4. Row-count identity

**141 raw rows = 131 unique rows + 10 exact duplicate rows.**
Duplicate order_ids: ORD-0014, ORD-0029, ORD-0034, ORD-0052, ORD-0057, ORD-0063, ORD-0065, ORD-0083, ORD-0089, ORD-0100 (each appears exactly twice).
- Duplicates' SIGNED value: **+270.00** (8 sale rows +735.00, 2 refund rows −465.00).
- If duplicates were wrongly counted, NET would be overstated at 60,485.00 (+270.00).

## 5. Date hygiene (census before parsing)

| Pattern | Raw rows | Unique rows | Value (net) |
|---|---:|---:|---:|
| ISO `yyyy-mm-dd` | 139 | 129 | 59,955.00 |
| `dd/mm/yyyy` | 2 | 2 | 260.00 |
| other/unparseable | 0 | 0 | — |

The 2 non-ISO rows are **ORD-0071 `29/05/2025`** (Keyboard, 180.00) and **ORD-0066 `14/05/2025`** (Headset, 80.00). Both are unambiguous day-first (day > 12, so month-first is impossible); the dual-format parser (ISO → dd/mm/yyyy) resolved all 141 dates with **0 parse failures and 0 ambiguous dd/mm rows**. Both correctly land in **May 2025** — the profiler's naive slicing had them in junk buckets (§3 note).

## 6. Price hygiene (per-product unit-price constancy, positive rows)

| Product | Distinct prices | Verdict |
|---|---|---|
| Keyboard | 45.00 | constant |
| Headset | 80.00 | constant |
| Laptop | 1,250.00 | constant |
| **Monitor** | **210.00 → 220.00** | **price change — disclosed below** |

**Monitor price change:** old price **210.00** (16 positive rows), new price **220.00** (10 positive rows), **first affected date 2025-05-12**. All Monitor sales dated before 2025-05-12 are at 210.00; all from that date on are at 220.00 — a clean step change.
Arithmetic consistency: `units × unit_price = amount` holds on **all** positive rows and `= |amount|` on all refund rows (0 violations).

## 7. Best-selling product

The two measures disagree, so **both are reported**; the "best seller" depends on the measure used.

| Rank | By units sold (GROSS units, positive rows) | By NET revenue |
|---|---|---|
| 1 | **Keyboard — 97 units** (44 sale orders) | **Laptop — 40,000.00 NET** (66.4% of NET) |
| 2 | Headset — 78 | Monitor — 10,510.00 |
| 3 | Monitor — 56 | Headset — 5,520.00 |
| 4 | Laptop — 32 | Keyboard — 4,185.00 |

Net units (after subtracting refund units): Keyboard 93, Headset 69, Monitor 49, Laptop 32 (Laptop has no refunds). **By revenue the best-seller is Laptop; by units it is Keyboard.**

## 8. Monthly revenue breakdown (unique rows, dates correctly parsed)

| Month | NET revenue | GROSS revenue | Refunds |
|---|---:|---:|---:|
| 2025-01 | 10,195.00 | 10,855.00 | 660.00 |
| 2025-02 | 3,515.00 | 3,915.00 | 400.00 |
| 2025-03 | **20,115.00** | 20,160.00 | 45.00 |
| 2025-04 | 9,525.00 | 10,365.00 | 840.00 |
| 2025-05 | 11,755.00 | 11,975.00 | 220.00 |
| 2025-06 | 5,110.00 | 5,325.00 | 215.00 |
| **Total** | **60,215.00** | **62,595.00** | **2,380.00** |

Net product×month (for context, sums match the table above):

| Month | Headset | Keyboard | Laptop | Monitor |
|---|---:|---:|---:|---:|
| 2025-01 | 560 | 675 | 8,750 | 210 |
| 2025-02 | 0 | 585 | 1,250 | 1,680 |
| 2025-03 | 1,680 | 1,125 | 15,000 | 2,310 |
| 2025-04 | 1,040 | 765 | 6,250 | 1,470 |
| 2025-05 | 1,200 | 855 | 7,500 | 2,200 |
| 2025-06 | 1,040 | 180 | 1,250 | 2,640 |

## 9. Data quality section

| Issue | Count | Value |
|---|---|---|
| Exact duplicate rows | 10 (10 order_ids, each ×2) | SIGNED **+270.00** (+735.00 from 8 sale rows; −465.00 from 2 refund rows) |
| Negative (refund) rows, unique | 11 | −2,380.00 (refund total 2,380.00) |
| — refund rows in raw file (2 are duplicated) | 13 | ORD-0014 and ORD-0083 each appear twice |
| Zero-amount rows | 1 (ORD-1001, 2025-04-02, Headset, 0 units) | 0.00 |
| Missing fields | `region` empty on **7 unique rows** (9 raw rows) | signed **+1,010.00** (1,170.00 from 6 sales + −160.00 refund ORD-0043) |

Refund row IDs (unique): ORD-0005 (−80), ORD-0014 (−420), ORD-0033 (−90), ORD-0043 (−160), ORD-0049 (−160), ORD-0067 (−220), ORD-0083 (−45), ORD-0084 (−45), ORD-0101 (−240), ORD-0118 (−80), ORD-0128 (−840).
Missing-region order_ids (unique): ORD-0034, ORD-0043, ORD-0046, ORD-0075, ORD-0086, ORD-0089, ORD-0105.

## 10. Anything else notable

1. **Revenue concentration in Laptop:** 66.4% of NET revenue (40,000.00 of 60,215.00) comes from Laptop — only 14 sale orders / 32 units (12% of units sold) at a constant 1,250.00.
2. **March spike:** 20,115.00 NET (33.4% of H1, ~5.7× February, the lowest month) driven by 15,000.00 of Laptop sales in March alone (12 Laptop units).
3. **Monitor price step 210→220 on 2025-05-12** (§6): May–June Monitor NET (4,840.00) is the product's highest two-month stretch — also its highest two-month unit stretch (23 units) — so the higher price came with no volume drop.
4. **Refund ORD-0067 anomaly:** a Monitor refund of −220.00 dated **2025-05-07** is priced at the *new* 220.00 price, five days *before* the first positive sale at 220.00 (2025-05-12). The original sale behind this refund is not in the dataset (or the refund is mispriced/misdated).
5. **June looks weak (5,110.00) but is partial** — data ends 2025-06-27.
6. Zero-unit row ORD-1001 contributes no money but would distort units-based metrics if summed naively (it adds 0 here; flagged for completeness).

## 11. Assumptions & limitations

| # | Judgment call | Alternative considered | Why chosen | Rows affected |
|---|---|---|---|---|
| 1 | Dedup on exact full-row content (all 7 fields) | Dedup on `order_id` alone | Matches the profiler's mandated definition; on this dataset both give identical results — no order_id repeats with differing content, so no judgment risk | 10 duplicate rows removed |
| 2 | Duplicate refund rows counted once (ORD-0014, ORD-0083) | Count twice | Duplicates are exact content matches; treating them as separate refund events would double-count 465.00 of refunds | 2 refund rows |
| 3 | `dd/mm/yyyy` parsed day-first | Month-first | Both rows have day > 12 → month-first impossible; unambiguous | 2 rows |
| 4 | Missing-region rows kept in all totals | Exclude them | Product, units, price and amount are present; only region is unknown, and totals must reconcile to raw data | 7 unique rows (1,010.00 signed) |
| 5 | Zero-amount row kept in row counts, excluded from money impact | Drop it | Contributes 0.00 either way; retained for auditability | 1 row |
| 6 | NET (not GROSS) is the "Total revenue" headline | GROSS | Mandated definition; refunds are real revenue reductions | 11 refund rows |
| 7 | Units-based "best-selling" uses GROSS units (positive rows) | Net units | Gross units = units actually sold; net units shown alongside as sensitivity — ranking is unchanged (Keyboard still #1) | 11 refund rows |
| 8 | Monthly breakdown uses parsed calendar month | Profiler's `date[:7]` slice | Slicing mis-files 2 non-ISO rows into junk buckets and understates May by 260.00 | 2 rows |
| 9 | June treated as partial month (ends 06-27) | Full-month comparison | Cannot compare like-for-like with Jan–May | — |

**Definition-dependent figures:** NET vs GROSS revenue, duplicate-row value (signed vs positive-only: +270.00 vs +735.00), and units-based best-seller (gross vs net) all change with the definition — the chosen definition is stated inline wherever used.

---

*Artifacts: `crosscheck.py` / `crosscheck.json` (independent verification), `process.md` (process log) in this run directory; profiler output `profile.json` next to the source CSV.*
