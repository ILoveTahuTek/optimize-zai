# Sales Analysis Report — 2025 H1

**Source:** `/home/z/my-project/harness-lab/tasks/sales-2025h1/sales.csv` (128 rows)
**Method:** data-hygiene profiler first, then an independent pandas/integer-cents cross-check. All figures below were confirmed by both implementations (see Verification).
**Period covered:** 2025-01-01 to 2025-06-28 (6 months, no gaps).

## 1. Headline figures

| Figure | Value | Definition |
|---|---|---|
| **Total revenue** | **48,755.00** | **NET** — sum of `amount` over unique rows, refunds included as negatives |
| Gross revenue | 49,015.00 | GROSS — sum of positive `amount` over unique rows only |
| Refund total | 260.00 | Sum of \|negative amounts\| over unique rows (4 rows) |

There is exactly one "Total revenue": the NET figure of **48,755.00**. The gross figure is reported separately above and is never referred to as net.

## 2. Best-selling product

The two definitions give **different answers**:

- **By units (primary, refund rows counted as negative units — mirrors the NET convention):** **Keyboard**, 75 units. Ranking: Keyboard 75 > Monitor 72 > Headset 69 > Laptop 20.
- **By NET revenue:** **Laptop**, 25,000.00 NET (51.3% of total NET revenue). Ranking: Laptop 25,000.00 > Monitor 15,120.00 > Headset 5,440.00 > Keyboard 3,195.00.

**Refund impact on units ranking:** none. If refunds are netted out of units (Keyboard −4, Headset −1) the ranking is unchanged, and it is also unchanged if refund rows are simply excluded (Keyboard 79 > Monitor 72 > Headset 70 > Laptop 20). The units ranking is robust to refund handling; the revenue leader (Laptop) is driven by its 1,250.00 unit price, not volume.

## 3. Monthly revenue breakdown (NET)

| Month | NET revenue | Share of H1 |
|---|---|---|
| 2025-01 | 6,225.00 | 12.8% |
| 2025-02 | 10,625.00 | 21.8% |
| 2025-03 | 4,740.00 | 9.7% |
| 2025-04 | 4,925.00 | 10.1% |
| 2025-05 | 10,175.00 | 20.9% |
| 2025-06 | 12,065.00 | 24.7% |
| **Total** | **48,755.00** | 100% |

Monthly NET figures are computed over unique rows with refunds included as negatives; they sum exactly to the NET total.

## 4. Row-count identity

**raw rows = unique rows + exact duplicate rows → 128 = 120 + 8.**

All revenue figures above use the 120 unique rows only.

## 5. Data quality

Numbers taken from the profiler (and confirmed by the cross-check):

- **Exact duplicate rows: 8.**
  - SIGNED value of the 8 duplicate rows: **+5,115.00** (this is the figure required by the method: refunds counted as negatives). One duplicate row is a duplicated refund, ORD-0078 at −90.00.
  - Note: the profiler's printed "duplicates add 5205.00 if wrongly counted" sums positive duplicate rows only; the two figures differ by exactly that −90.00 refund. If duplicates were wrongly counted, NET revenue would be overstated by 5,115.00 (to 53,870.00).
- **Negative (refund) rows: 4** — IDs ORD-0116 (−45.00), ORD-0078 (−90.00), ORD-0107 (−80.00), ORD-0094 (−45.00); total value −260.00. Three are Keyboard refunds, one Headset.
- **Zero-amount rows: 0.**
- **Missing fields (empty `region`): 4 rows**, worth 2,190.00 (4.5% of NET) — ORD-0046, ORD-0002, ORD-0008, ORD-0059. These rows are kept in all totals above; only region-level analysis would be affected.
- **Price-consistency violations: 0** — for every positive row, `units × unit_price = amount`.

## 6. Verification

Independent cross-check = separate implementation (pandas + integer-cents arithmetic + `drop_duplicates` + datetime month parsing), not a copy of the profiler's logic. All values matched exactly:

| Figure | Profiler | Independent | Match |
|---|---|---|---|
| Raw / unique / duplicate rows | 128 / 120 / 8 | 128 / 120 / 8 | ✓ |
| NET revenue | 48,755.00 | 48,755.00 | ✓ |
| GROSS revenue | 49,015.00 | 49,015.00 | ✓ |
| Refund total (4 rows: ORD-0078, ORD-0094, ORD-0107, ORD-0116) | 260.00 | 260.00 | ✓ |
| NET 2025-01 | 6,225.00 | 6,225.00 | ✓ |
| NET 2025-02 | 10,625.00 | 10,625.00 | ✓ |
| NET 2025-03 | 4,740.00 | 4,740.00 | ✓ |
| NET 2025-04 | 4,925.00 | 4,925.00 | ✓ |
| NET 2025-05 | 10,175.00 | 10,175.00 | ✓ |
| NET 2025-06 | 12,065.00 | 12,065.00 | ✓ |
| NET by product (Laptop/Monitor/Headset/Keyboard) | 25,000.00 / 15,120.00 / 5,440.00 / 3,195.00 | same | ✓ |
| Missing-region rows / value | 4 / 2,190.00 | 4 / 2,190.00 | ✓ |
| Zero rows / price violations | 0 / 0 | 0 / 0 | ✓ |

**Extra consistency checks run (all passed):**
- Row-count identity: 128 = 120 + 8.
- NET = GROSS − refunds: 49,015.00 − 260.00 = 48,755.00.
- Monthly NET totals sum to NET: 48,755.00.
- Product NET totals sum to NET: 48,755.00.
- Units ranking compared with and without refund rows (unchanged; §2).

## 7. Other notable observations

- **Strong H2-style finish:** June is the best month (12,065.00, 24.7% of H1); a clear dip occurs in March–April (~4,700–4,900 per month) between two stronger peaks (Feb, May–Jun).
- **Concentration risk:** Laptop is 51.3% of NET revenue from only 20 units; the business is price-mix dependent on one product.
- **Unit prices are fixed per product** (Keyboard 45.00, Headset 80.00, Monitor 210.00, Laptop 1,250.00) and no amount/price inconsistencies exist, so the `amount` column is fully trustworthy.
- **Regions present:** Jakarta, Bandung, Surabaya, Denpasar, Medan, plus 4 blank rows. Region rankings would shift by up to 2,190.00 (4.5%) if the blank-region rows belong to any particular region; they were not imputed.
