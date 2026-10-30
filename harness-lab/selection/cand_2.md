# Sales Analysis Report — 2025 H1 (sales.csv)

**Dataset:** `/home/z/my-project/harness-lab/tasks/sales-2025h1/sales.csv` (sha256 `4b480867…ee2ce9c`), 128 data rows, 7 columns (`order_id, date, product, units, unit_price, region, amount`), observed date range 2025-01-01 to 2025-06-28.

**Row-count identity:** raw data rows (128) = unique rows (120) + exact duplicate rows (8). ✅

**Money-figure definitions used throughout:**
- **NET revenue** = Σ `amount` over unique rows (exact duplicates removed; refund/negative rows included as negatives). This is the single primary headline number.
- **GROSS revenue** = Σ positive `amount` over unique rows (reported separately as "gross").
- **Refund total** = Σ |negative `amount`| over unique rows.

---

## Headline figures (unique rows, n = 120)

| Metric | Value |
|---|---|
| **Total revenue (NET)** | **$48,755.00** |
| Gross revenue | $49,015.00 |
| Refund total | $260.00 |

Internal consistency: gross − refunds = $49,015.00 − $260.00 = $48,755.00 = NET ✅

## Best-selling product

The two definitions differ, so both are reported. Primary designation: **by units (units as recorded in `units`, summed over unique rows) → Keyboard**.

| Rank | By units (primary definition) | By NET revenue |
|---|---|---|
| 1 | **Keyboard** — 79 units (40 orders) | **Laptop** — $25,000.00 |
| 2 | Monitor — 72 units | Monitor — $15,120.00 |
| 3 | Headset — 70 units | Headset — $5,440.00 |
| 4 | Laptop — 20 units | Keyboard — $3,195.00 |

Caveat: refund rows carry positive `units` with negative `amount`. If refund units are instead counted as negative (net-of-refunds view), the units ranking changes: Monitor 72 > Keyboard 71 > Headset 68 > Laptop 20. Both views are stated; "units as recorded" is the definition used above.

## Monthly revenue breakdown (unique rows; NET includes refunds)

| Month | Orders | Units | Gross | Refunds | NET |
|---|---|---|---|---|---|
| 2025-01 | 21 | 44 | $6,315.00 | $90.00 | **$6,225.00** |
| 2025-02 | 19 | 41 | $10,625.00 | $0.00 | **$10,625.00** |
| 2025-03 | 20 | 38 | $4,820.00 | $80.00 | **$4,740.00** |
| 2025-04 | 15 | 33 | $4,925.00 | $0.00 | **$4,925.00** |
| 2025-05 | 25 | 45 | $10,265.00 | $90.00 | **$10,175.00** |
| 2025-06 | 20 | 40 | $12,065.00 | $0.00 | **$12,065.00** |
| **Total** | **120** | **241** | **$49,015.00** | **$260.00** | **$48,755.00** |

Columns cross-foot exactly to the headline figures.

## Data quality (exact numbers)

- **Exact duplicate rows: 8** occurrences (raw 128 vs unique 120), worth **$5,115.00** of raw `amount`. Duplicated orders: ORD-0098 ($3,750.00), ORD-0039 ($400.00), ORD-0011 ($420.00), ORD-0072 ($240.00), ORD-0032 ($180.00), ORD-0016 ($135.00), ORD-0054 ($80.00), ORD-0078 (−$90.00). All money figures above are computed after removing these.
- **Negative-amount (refund) rows: 5** raw occurrences covering **4 unique rows**, raw value −$350.00; **$260.00** after dedup (ORD-0078 −$90.00 appears twice). Unique refund orders: ORD-0078 Keyboard −$90.00 (2025-01-28), ORD-0107 Headset −$80.00 (2025-03-25), ORD-0116 Keyboard −$45.00 (2025-05-17), ORD-0094 Keyboard −$45.00 (2025-05-19).
- **Rows with missing fields: 4** rows / 4 missing cells, all in the `region` column (ORD-0046, ORD-0002, ORD-0059, ORD-0008; combined gross $2,190.00). No other column has missing values.
- **Zero-amount rows: 0** (raw and unique).
- Integrity: in all 120 unique rows, `amount` equals units × unit_price or its negation (0 exceptions); every row has exactly 7 fields; all dates parse and fall within 2025-01-01…2025-06-28. File uses CRLF line endings.

## Other notable findings

- **Laptop dominates revenue:** $25,000.00 net = **51.3%** of total NET from only 20 units (8% of units) across 10 orders. Keyboard is the volume leader but the smallest revenue line.
- **June was the strongest month** ($12,065.00 net, boosted by ORD-0069, the largest single order at $5,000.00); **March the weakest** ($4,740.00). Pattern is lumpy rather than steadily growing: two soft months (Mar, Apr) between two strong pairs.
- **By region (NET):** Jakarta leads ($11,315.00 from 18 orders), Surabaya $10,950.00, Denpasar $10,210.00 (most orders, 32), Medan $7,095.00, Bandung $6,995.00; the 4 missing-region orders add $2,190.00 — regional totals understate those sales.
- **Refunds are minimal:** $260.00 = 0.53% of gross; all 4 refunds are Keyboard/Headset orders.
- Duplicate rows cluster on high-value orders (ORD-0098 alone is $3,750.00), so naive raw-file sums would overstate gross revenue by $5,115.00 (≈10.4%).

## Verification

Every headline figure was computed by two independent implementations (Python 3 stdlib + Decimal; mawk with integer-cent arithmetic), and the headline money figures and row counts additionally by a third (SQLite SQL over `SELECT DISTINCT`). All shared output lines of Methods A and B are diff-identical.

| Figure | Method A (Python) | Method B (mawk) | Method C (SQLite) | Match |
|---|---|---|---|---|
| Raw rows | 128 | 128 | 128 | ✅ |
| Unique rows | 120 | 120 | 120 | ✅ |
| Exact duplicate rows | 8 | 8 | 8 | ✅ |
| Duplicate value | $5,115.00 | $5,115.00 | (not computed) | A=B ✅ |
| **NET revenue** | **$48,755.00** | **$48,755.00** | **$48,755.00** | ✅ |
| Gross revenue | $49,015.00 | $49,015.00 | $49,015.00 | ✅ |
| Refund total | $260.00 | $260.00 | $260.00 | ✅ |
| NET Jan / Feb / Mar / Apr / May / Jun | 6,225 / 10,625 / 4,740 / 4,925 / 10,175 / 12,065 | same | same | ✅ |
| Negative rows (raw / unique) | 5 / 4 | 5 / 4 | (not computed) | A=B ✅ |
| Missing-field rows (region) | 4 | 4 | (not computed) | A=B ✅ |
| Zero-amount rows | 0 | 0 | (not computed) | A=B ✅ |

Cross-foot checks (all passed): monthly NET sums to $48,755.00; monthly gross to $49,015.00; monthly refunds to $260.00; monthly orders to 120; product units/gross/net sum to 241 / $49,015.00 / $48,755.00; region NET sums to $48,755.00; NET = GROSS − Refunds.

*Analysis scripts and raw outputs: `method_a.py`, `method_b.awk`, `method_a.out`, `method_b.out`, `sqlite_check.out` (same directory).*
