# Sales Analysis Report — `sales.csv` (2025 H1)

**Source:** `/home/z/my-project/harness-lab/tasks/sales-2025h1/sales.csv`
**Method:** the mandatory profiler (`profile_csv.py`) was run first; every headline figure was then re-derived by an independent cross-check (`verify_dom1.py`, sort-based dedup, different parse path). All 10 shared figures agreed exactly. All money figures use exact decimal arithmetic.

**Definitions used (every money figure below is labeled):**
- **NET revenue** = sum of `amount` over unique rows (exact duplicates removed), refunds included as negatives — the primary headline number.
- **GROSS revenue** = sum of positive `amount` over unique rows.
- **Refund total** = sum of |negative `amount`| over unique rows.

---

## 1. Headline

| Metric | Value |
|---|---|
| **Total revenue (NET)** | **$48,755.00** |
| Gross revenue | $49,015.00 |
| Refund total | $260.00 |

## 2. Row-count identity

**128 raw rows = 120 unique rows + 8 exact duplicate rows.**

## 3. Best-selling product

The two definitions give different winners, so both are reported. **The definition used for the headline claim is NET revenue.**

| Product | Units sold (gross units on positive rows) | NET revenue | Share of NET |
|---|---|---|---|
| **Laptop** | 20 | **$25,000.00** | 51.3% |
| Monitor | 72 | $15,120.00 | 31.0% |
| Headset | 69 | $5,440.00 | 11.2% |
| Keyboard | 75 | $3,195.00 | 6.6% |

- **Best-selling by NET revenue: Laptop** — $25,000.00 (51.3% of NET) from only 20 units.
- **Best-selling by units: Keyboard** — 75 units (236 total gross units), yet the smallest revenue line.
- Footnote: if refund units are subtracted (net units), the units ranking flips to **Monitor (72)** ahead of Keyboard (71), because 3 of the 4 refunds are Keyboard orders.

## 4. Monthly revenue breakdown (unique rows)

| Month | NET revenue | GROSS revenue | Refunds | Share of NET |
|---|---|---|---|---|
| 2025-01 | $6,225.00 | $6,315.00 | $90.00 | 12.8% |
| 2025-02 | $10,625.00 | $10,625.00 | $0.00 | 21.8% |
| 2025-03 | $4,740.00 | $4,820.00 | $80.00 | 9.7% |
| 2025-04 | $4,925.00 | $4,925.00 | $0.00 | 10.1% |
| 2025-05 | $10,175.00 | $10,265.00 | $90.00 | 20.9% |
| 2025-06 | $12,065.00 | $12,065.00 | $0.00 | 24.7% |
| **Total** | **$48,755.00** | **$49,015.00** | **$260.00** | 100% |

## 5. Data quality (exact figures from the profiler)

- **Exact duplicate rows: 8** — ORD-0072 ($240.00), ORD-0098 ($3,750.00), ORD-0039 ($400.00), ORD-0011 ($420.00), ORD-0032 ($180.00), ORD-0016 ($135.00), ORD-0054 ($80.00), ORD-0078 (−$90.00 refund). If all 8 were wrongly counted, the net total would be overstated by $5,115.00 (the profiler's positive-only duplicate value is $5,205.00 gross).
- **Negative (refund) rows: 4** — ORD-0078 Keyboard −$90.00, ORD-0107 Headset −$80.00, ORD-0094 Keyboard −$45.00, ORD-0116 Keyboard −$45.00. **Refund total: $260.00.**
- **Zero-amount rows: 0.**
- **Missing fields:** `region` missing on **4** unique rows (ORD-0002, ORD-0046, ORD-0008, ORD-0059) worth **$2,190.00 NET**; all other columns (order_id, date, product, units, unit_price, amount) have **0** missing values.
- **Price consistency: 0 violations** — `amount = units × unit_price` holds on all 120 unique rows, refunds included. No order_id is reused with conflicting content; dates span 2025-01-01 to 2025-06-28.

## 6. Other notables

- **Revenue is concentrated in one product:** Laptop contributes 51.3% of NET revenue from 8.5% of units (20 of 236). Keyboard is the volume leader (31.8% of units) but only 6.6% of NET revenue.
- **Seasonality:** June is the strongest month ($12,065.00 NET), March the weakest ($4,740.00). The half splits into a strong start (Feb), a soft March–April (~10% each), and a strong May–June finish; June also had zero refunds.
- **Regions (NET):** Jakarta $11,315.00 > Surabaya $10,950.00 > Denpasar $10,210.00 > Medan $7,095.00 > Bandung $6,995.00; the 4 missing-region rows ($2,190.00 NET) would outrank Medan and Bandung if treated as a "region" — the data-capture gap is material and worth fixing at source.
- **Deduplication matters here:** 8 of 128 raw rows (6.3%) are exact duplicates; naive counting would inflate gross by $5,205.00 (10.6% of GROSS).
