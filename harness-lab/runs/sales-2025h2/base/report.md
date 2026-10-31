# Sales Analysis Report — H2 2025 (sales.csv)

**Scope:** 1 July – 28 December 2025 (H2 2025). Source file: `tasks/sales-2025h2/sales.csv`, 118 rows = 112 unique orders + 6 exact duplicate rows.

## Headline figures

| Metric | Value |
|---|---|
| Total revenue (net, deduplicated) | **290,480.00** |
| Total revenue excluding outlier order ORD-0901 | **40,480.00** |
| Gross sales ex-outlier (before 370.00 of refunds) | 40,850.00 |
| Unique orders | 112 (118 raw rows, incl. 6 duplicates) |
| Average order value ex-outlier | ≈ 364.29 (40,480.00 / 111 orders, net of refunds) |

> ⚠️ **A single order dominates the total.** ORD-0901 (2025-09-14, Jakarta, Laptop × 200 @ 1,250.00 = **250,000.00**) accounts for **86.1%** of deduplicated revenue and is 50× the next-largest order (5,000.00). All figures below are shown with and without it.

## Best-selling product

| Product | Orders | Units | Revenue | Revenue ex-outlier |
|---|---|---|---|---|
| Laptop | 9 | 214 | 267,500.00 | 17,500.00 |
| Monitor | 29 | 66 | 13,440.00 | 13,440.00 |
| Headset | 35 | 76 | 5,760.00 | 5,760.00 |
| Keyboard | 39 | 84 | 3,780.00 | 3,780.00 |

- **By order count and units sold: Keyboard** (39 orders, 84 units) — the top seller once the ORD-0901 bulk purchase is excluded (Laptop drops to 14 units ex-outlier).
- **By revenue: Laptop** (267,500.00 incl. outlier; still #1 ex-outlier at 17,500.00 on just 8 orders).
- Product pricing is uniform: Laptop 1,250.00, Monitor 210.00, Headset 80.00, Keyboard 45.00. `amount = units × unit_price` holds on every row (magnitude).

## Monthly revenue breakdown (deduplicated, net of refunds)

| Month | Orders | Revenue | Revenue ex-ORD-0901 |
|---|---|---|---|
| 2025-07 | 18 | 4,075.00 | 4,075.00 |
| 2025-08 | 20 | 7,335.00 | 7,335.00 |
| 2025-09 | 16 | 253,280.00 | 3,280.00 |
| 2025-10 | 17 | 5,805.00 | 5,805.00 |
| 2025-11 | 20 | 8,710.00 | 8,710.00 |
| 2025-12 | 21 | 11,275.00 | 11,275.00 |
| **Total** | **112** | **290,480.00** | **40,480.00** |

- Ex-outlier, **December is the strongest month** (11,275.00) and the trend Nov→Dec is clearly upward; September is the weakest (3,280.00).

## Revenue by region (ex-outlier, deduplicated)

| Region | Revenue |
|---|---|
| Medan | 15,645.00 |
| Jakarta | 7,585.00 |
| Surabaya | 5,645.00 |
| Bandung | 4,665.00 |
| *(missing)* | 4,465.00 |
| Denpasar | 2,475.00 |

Medan leads largely on Laptop sales; (missing) region would rank 4th if it were a region — 9 orders lack a region value.

## Data quality findings

1. **6 exact duplicate rows** (ORD-0105, ORD-0026, ORD-0054, ORD-0021, ORD-0065, ORD-0068; dup sum 4,630.00). Raw sum of all 118 rows is 295,110.00 — an overstatement of 4,630.00 vs. the deduplicated 290,480.00. Appears to be a data-load/append error.
2. **Extreme outlier ORD-0901** (200 Laptops, 250,000.00). Verify authenticity: it may be a legitimate bulk B2B order, or a units typo (200 vs. e.g. 2) — 0.8% of all orders drive 86% of revenue.
3. **2 negative-amount rows**, consistent with returns/refunds: ORD-0052 (Monitor, −210.00) and ORD-0048 (Headset, −160.00), total −370.00. Their `units` remain positive, so unit counts are overstated by 3 units if the goods were actually returned.
4. **1 zero-value order**: ORD-0902 (Headset, 0 units, 0.00, 2025-08-03, Bandung) — likely cancelled or a placeholder.
5. **9 orders (≈8%) missing `region`** (ORD-0105, ORD-0015, ORD-0070, ORD-0024, ORD-0069, ORD-0003, ORD-0091, ORD-0050, ORD-0078).

## Method notes

- Figures labelled "deduplicated" keep the first occurrence of each unique order row; refunds are included as negative revenue (net basis).
- Analysis script: `analyze.py` (stdlib CSV parsing; all totals re-verified with independent arithmetic checks).
