# Sales Analysis Report — sales-2025h1-dirty (2025 H1)

Source: `/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv`
Scope: order-level sales rows, 2025-01-01 through 2025-06-27. All money figures are computed over **unique rows** (exact duplicate rows removed) and are labeled **net**, **gross**, or **refund** per the definitions below.

## Definitions used

- **NET revenue** = sum of `amount` over unique rows, refund/negative rows included as negatives. **This is the single primary headline number.**
- **GROSS revenue** = sum of positive `amount` over unique rows (reported separately, labeled "gross").
- **Refund total** = sum of |negative `amount`| over unique rows (reported separately).

## Total revenue

- **Total revenue (NET): 60,215.00**
- Gross revenue: 62,595.00
- Refund total: 2,380.00
- Internal identity holds: gross 62,595.00 − refund 2,380.00 = net 60,215.00

## Row-count identity

**Raw data rows (141) = unique rows (131) + exact duplicate rows (10).** ✔ Verified.

## Best-selling product

The two definitions differ, so both are reported. **I use net revenue as the primary "best-selling" definition**; the units view is given alongside.

| Rank | By NET revenue (primary) | By units sold (units on positive-amount/sale rows) |
|---|---|---|
| 1 | **Laptop — 40,000.00 net** (66.4% of net) | **Keyboard — 97 units** |
| 2 | Monitor — 10,510.00 net (17.5%) | Headset — 78 units |
| 3 | Headset — 5,520.00 net (9.2%) | Monitor — 56 units |
| 4 | Keyboard — 4,185.00 net (6.9%) | Laptop — 32 units |

Best-selling **by revenue**: Laptop (40,000.00 net; it has no refunds, so gross is also 40,000.00). Best-selling **by units**: Keyboard (97 units sold). If refund rows are included as |units| (a returns-inclusive view), ranking is unchanged: Keyboard 101, Headset 87, Monitor 63, Laptop 32.

## Monthly revenue breakdown (unique rows)

| Month | Net revenue | Gross revenue | Refunds |
|---|---|---|---|
| 2025-01 | 10,195.00 | 10,855.00 | 660.00 |
| 2025-02 | 3,515.00 | 3,915.00 | 400.00 |
| 2025-03 | 20,115.00 | 20,160.00 | 45.00 |
| 2025-04 | 9,525.00 | 10,365.00 | 840.00 |
| 2025-05 | 11,755.00 | 11,975.00 | 220.00 |
| 2025-06 | 5,110.00 | 5,325.00 | 215.00 |
| **Total** | **60,215.00** | **62,595.00** | **2,380.00** |

Monthly net figures sum exactly to the headline net 60,215.00. (Two rows carry DD/MM/YYYY dates — ORD-0071 "29/05/2025", ORD-0066 "14/05/2025" — normalized to May 2025.)

## Data quality

| Issue | Count (unique rows) | Value |
|---|---|---|
| Exact duplicate rows (removed) | 10 duplicate copies (each of 10 rows appears exactly twice) | 735.00 gross / 270.00 net carried by the copies — skipping dedup would overstate net as 60,485.00 and gross as 63,330.00 |
| Negative-amount (refund) rows | 11 | 2,380.00 refund total (3.8% of gross) |
| Rows with missing fields (empty `region`) | 7 unique rows (9 raw rows incl. duplicates): ORD-0034, ORD-0086, ORD-0089, ORD-0105, ORD-0075, ORD-0046, ORD-0043 | 1,010.00 net with no region attribution (1.7% of net) |
| Zero-amount rows | 1 (ORD-1001: Headset, 0 units, Medan, 2025-04-02) | 0.00 — no monetary effect |

All duplicates are full-row, byte-identical copies appearing exactly twice (double-append/load pattern), and no `order_id` is repeated with differing content after dedup. Every row's `amount` equals ±(units × unit_price) — no arithmetic mismatches.

## Anything else notable

- **March 2025 is the peak month** (20,115.00 net, 33.4% of H1), driven by four Laptop orders totaling 15,000.00 (ORD-0055, ORD-0092, ORD-0111, ORD-0129).
- **Monitor price rose from 210.00 to 220.00 in May 2025** — every January–April Monitor is priced 210.00; 220.00 first appears 2025-05-07 (a refund) and on sales from 2025-05-12.
- **June is likely under-counted**: the data ends 2025-06-27 (5,110.00 net), so June should not be compared 1:1 with full months.
- Largest single refund: ORD-0128, −840.00 (Monitor, Surabaya, 2025-04-06).
- Refund rows consistently carry positive `units` with negative `amount`; no negative or zero units exist except the single 0-unit row ORD-1001.

## Verification

Every headline figure was computed by two (in fact three) independent methods: **(A)** Python stdlib script `verify1.py` (csv module, manual dedup, Decimal), **(B)** pandas script `verify2.py` (drop_duplicates, groupby), **(C)** awk one-liner (sort/uniq dedup). Values match exactly in all runs.

| Headline figure | Method A | Method B | Method C | Match |
|---|---|---|---|---|
| Raw data rows | 141 | 141 | — | ✔ |
| Unique rows / exact duplicate rows | 131 / 10 | 131 / 10 | 131 | ✔ |
| Total revenue (NET) | 60,215.00 | 60,215.00 | 60,215 | ✔ |
| Gross revenue | 62,595.00 | 62,595.00 | 62,595 | ✔ |
| Refund total | 2,380.00 | 2,380.00 | 2,380 | ✔ |
| Monthly net (Jan→Jun) | 10,195 / 3,515 / 20,115 / 9,525 / 11,755 / 5,110 | identical | identical | ✔ |
| Product net (Laptop/Monitor/Headset/Keyboard) | 40,000 / 10,510 / 5,520 / 4,185 | identical | identical | ✔ |
| Units sold (Keyboard/Headset/Monitor/Laptop) | 97 / 78 / 56 / 32 | identical | identical | ✔ |
| Negative rows / missing-field rows / zero rows | 11 / 7 / 1 | 11 / 7 / 1 | — | ✔ |
| Duplicate-copy value (gross/net) | 735.00 / 270.00 | — | 735 / 270 | ✔ |

Additional arithmetic cross-checks: monthly net sums to 60,215.00; product net sums to 60,215.00; gross − refund = net.
