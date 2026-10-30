# Sales Analysis Report — 2025 H1 (Jan–Jun)

**Source:** `tasks/sales-2025h1/sales.csv` (128 data rows; 120 unique orders after removing 8 exact duplicate rows)

## Headline numbers

| Metric | Value |
|---|---|
| Total revenue (120 unique orders, amounts as recorded) | **48,755.00** |
| Total revenue excluding the 4 refund rows (net sales) | 49,015.00 |
| Total revenue if duplicate rows were not removed (raw file sum) | 53,870.00 |
| Unique orders | 120 |
| Date range covered | 2025-01-01 → 2025-06-28 |

## Best-selling product

- **By units sold: Keyboard** — 79 units across 40 orders (45.00 each; 3,195.00 revenue). This holds even after netting out refunds (75 units).
- **By revenue: Laptop** — 25,000.00 from only 20 units in 10 orders (1,250.00 each), i.e. ~51% of total revenue from 8% of orders.

Full product breakdown (deduplicated, amounts as recorded):

| Product | Orders | Units | Revenue | Share of revenue |
|---|---|---|---|---|
| Laptop | 10 | 20 | 25,000.00 | 51.3% |
| Monitor | 35 | 72 | 15,120.00 | 31.0% |
| Headset | 35 | 70 | 5,440.00 | 11.2% |
| Keyboard | 40 | 79 | 3,195.00 | 6.6% |

## Monthly revenue breakdown

| Month | Orders | Units | Revenue |
|---|---|---|---|
| 2025-01 | 21 | 44 | 6,225.00 |
| 2025-02 | 19 | 41 | 10,625.00 |
| 2025-03 | 20 | 38 | 4,740.00 |
| 2025-04 | 15 | 33 | 4,925.00 |
| 2025-05 | 25 | 45 | 10,175.00 |
| 2025-06 | 20 | 40 | 12,065.00 |

**Trend:** weak mid-period trough in March–April (~4,700–4,900/month), followed by a strong recovery in May–June. **June was the best month (12,065.00)**; March the worst (4,740.00). Month totals are volatile because a few large Laptop orders dominate: Feb was lifted by a 3-unit Laptop order (3,750.00) and June by a 4-unit Laptop order (5,000.00 — the largest single order in the file).

## Revenue by region

Jakarta 11,315.00 · Surabaya 10,950.00 · Denpasar 10,210.00 · Medan 7,095.00 · Bandung 6,995.00 · (region missing) 2,190.00. Denpasar leads in order count (32) but Jakarta/Surabaya lead in revenue, driven by Laptop purchases.

## Other notable findings (data quality)

1. **8 exact duplicate rows** (orders ORD-0011, ORD-0016, ORD-0032, ORD-0039, ORD-0054, ORD-0072, ORD-0078, ORD-0098 each appear twice identically). All headline figures above use deduplicated data; keeping them would overstate revenue by 5,115.00.
2. **4 rows have negative amounts** despite positive units — consistent with refunds/returns: ORD-0116 (Keyboard, −45.00), ORD-0078 (Keyboard, −90.00), ORD-0107 (Headset, −80.00), ORD-0094 (Keyboard, −45.00). Total −260.00.
3. **4 orders have a blank region** (ORD-0046, ORD-0002, ORD-0008, ORD-0059), worth 2,190.00 combined.
4. Unit prices are perfectly consistent per product (Keyboard 45.00, Headset 80.00, Monitor 210.00, Laptop 1,250.00), so revenue variation is driven purely by order mix and volume.
5. Excluding the negative-amount rows, `amount = units × unit_price` holds for every order; the 4 refund rows are sign-flipped amounts.

## Method notes

Figures are computed on **deduplicated data with amounts as recorded** (refund rows included as negatives). "Best-selling" is reported both by units and by revenue because the two answers differ. A fully reproducible script is at `analyze.py` alongside this report.
