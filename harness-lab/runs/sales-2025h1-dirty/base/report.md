# Sales Analysis Report — 2025 H1 (dirty data)

**Source:** `tasks/sales-2025h1-dirty/sales.csv` (141 data rows, orders 2025-01-01 → 2025-06-27, 4 products, 5 regions)
**Method:** The file contained quality issues (duplicate rows, mixed date formats, negative amounts, a zero-unit order, missing regions). Figures below are computed on the **131 unique orders** remaining after removing 10 exact duplicate rows. "Net" = negative-amount rows (treated as refunds/returns) subtracted.

## Total revenue

- **Net total revenue: 60,215.00**
- Gross (positive-amount orders): 62,595.00
- Refunds/returns (11 negative-amount rows): −2,380.00 (3.8% of gross)

## Best-selling product

Two reasonable definitions; both are given.

| Metric | Leader | Detail |
|---|---|---|
| **By revenue (net)** | **Laptop** | 40,000.00 — 66.4% of net revenue (32 units, 14 orders @ 1,250.00) |
| **By units sold** | **Keyboard** | 97 units on positive orders (101 incl. refund rows), 47 orders @ 45.00 |

Full net revenue ranking: Laptop 40,000.00 · Monitor 10,510.00 · Headset 5,520.00 · Keyboard 4,185.00.

## Monthly revenue breakdown (net)

| Month | Net revenue | Gross | Refunds |
|---|---:|---:|---:|
| 2025-01 | 10,195.00 | 10,855.00 | −660.00 |
| 2025-02 | 3,515.00 | 3,915.00 | −400.00 |
| 2025-03 | 20,115.00 | 20,160.00 | −45.00 |
| 2025-04 | 9,525.00 | 10,365.00 | −840.00 |
| 2025-05 | 11,755.00 | 11,975.00 | −220.00 |
| 2025-06 | 5,110.00 | 5,325.00 | −215.00 |
| **Total** | **60,215.00** | **62,595.00** | **−2,380.00** |

Pattern: **March is the peak** (20,115.00, 33% of H1), driven by three large laptop orders (ORD-0055 5,000 · ORD-0129 5,000 · ORD-0111 3,750 = 13,750 of the month). **February is the trough** (3,515.00). June is also low, but the data ends 2025-06-27, so June may be partially complete.

## Other notable findings

1. **Data quality issues found and handled:**
   - **10 exact duplicate rows** removed (ORD-0100, ORD-0057, ORD-0014, ORD-0083, ORD-0065, ORD-0089, ORD-0063, ORD-0034, ORD-0052, ORD-0029). No order_id appeared twice with conflicting content.
   - **2 rows in DD/MM/YYYY format** instead of ISO (ORD-0071 `29/05/2025`, ORD-0066 `14/05/2025`); normalized to 2025-05-29 and 2025-05-14.
   - **1 zero-unit order** (ORD-1001, Headset ×0, amount 0.00) — likely a test/placeholder record; included, it contributes nothing to revenue.
   - **7 orders with missing region** (net 1,010.00, 1.7% of revenue); counted under "(missing)".
   - Arithmetic is otherwise clean: every row satisfies `amount = units × unit_price` (up to sign).
2. **Monitor price increase:** unit price went from 210.00 to 220.00 (+4.8%) between 2025-04-28 (last 210 order) and 2025-05-07 (first 220 order).
3. **Refunds skew to Monitors:** Monitors account for 1,480.00 of the 2,380.00 refunded (Headset 720.00, Keyboard 180.00, Laptop 0.00). Largest single refund: ORD-0128, 840.00 (4 × Monitor).
4. **Region concentration:** Bandung 25,935.00 (43.1%), Medan 15,775.00 (26.2%), Jakarta 9,100.00 (15.1%), Surabaya 6,785.00 (11.3%), Denpasar 1,610.00 (2.7%), missing 1,010.00 (1.7%).
5. **Largest orders:** three 4-unit laptop orders of 5,000.00 each (ORD-0098 Bandung, ORD-0129 Bandung, ORD-0055 Medan).

## Assumptions & caveats

- Negative amounts have positive units and magnitude exactly `units × unit_price`; they were treated as **refunds/returns** and netted against revenue. If they are instead sign-entry errors, gross revenue would be 62,595.00.
- "Total revenue" headline figure is the **net** number (60,215.00); both views are provided above.
- Duplicates were defined as fully identical rows; first occurrence kept.
- 283 total units across all rows (283 = 97+78+56+32 on positive orders, plus units on refund rows).
