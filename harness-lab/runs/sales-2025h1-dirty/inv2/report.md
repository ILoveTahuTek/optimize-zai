# Sales Analysis — H1 2025 (sales.csv)

Prepared for decision-making. Source file: `/home/z/my-project/harness-lab/tasks/sales-2025h1-dirty/sales.csv` (141 data rows, 2025-01-01 through 2025-06-27). Analysis script: `/home/z/my-project/harness-lab/runs/sales-2025h1-dirty/inv2/analyze.py`.

## Executive Summary

- Revenue is concentrated in a single high-ticket product line — laptop deal flow, not the high-volume accessory lines, drives nearly all of the month-to-month swings.
- Returns cluster in the accessory lines (headsets and monitors) while the biggest revenue line has none, so a returns review should start there before those lines are scaled further.
- The file contains duplicates, negative-amount rows, mixed date formats and missing regions; all headline figures below use the conservative reading (exact duplicates removed, refunds netted), and every cleaning choice is quantified in the Assumptions & Limitations section.

## Assumptions & Limitations

The cleaning choices below move the headline totals by a known, quantified amount, so any alternative figure can be re-derived from this list alone.

Every judgment call made on this dirty file, the alternative considered, and why the chosen treatment was used:

1. **Exact-duplicate rows removed (10 rows affected).** Ten rows are byte-identical repeats of an earlier row (same order_id, date, product, units, price, region, amount), e.g. ORD-0057 on lines 39 and 57. Alternative: keep both and treat as two identical same-day orders. Chosen: keep the first occurrence only — an identical order_id with identical full content is a re-entry/re-submission artifact, and no order_id appears anywhere with *conflicting* content (verified), so there is no case where two rows represent genuinely distinct orders. Effect: the raw undeduplicated sum is 60,485.00 vs 60,215.00 after dedup (a 270.00 inflation, 10 of 141 rows = 7.1% of rows). **Total revenue is (definition-dependent)** on this choice.
2. **Negative amounts treated as refunds and netted (11 rows affected, −2,380.00).** Eleven unique rows carry a negative amount while units stay positive; in every case the magnitude exactly equals units × unit_price, and none of these order_ids has a positive counterpart anywhere in the file. Alternative: (a) report gross only and ignore negatives, or (b) treat them as data errors. Chosen: net them against revenue — the pattern is unambiguous full-quantity returns, and since the original sales rows for those order_ids are not present, netting is the only economically meaningful treatment. Both readings are shown: gross sales 62,595.00, refunds −2,380.00, net 60,215.00. **Total revenue and the monthly/product breakdowns are (definition-dependent)** on this choice.
3. **Refund units subtracted from unit counts ("net units").** Refund rows carry positive units, so raw units would overstate volume. Alternative: count gross units (263 vs 243 net). Chosen: net units, consistent with netting revenue. Note: the best-selling ranking is identical under both readings, so that headline does not change.
4. **Mixed date formats: 2 rows parsed day-first.** ORD-0071 ("29/05/2025", line 73) and ORD-0066 ("14/05/2025", line 88) use DD/MM/YYYY while all other rows use YYYY-MM-DD. The alternative (month-first) was not actually available — 29 and 14 cannot be months — so no ambiguity survived; both rows land in May. All 141 rows parsed to valid dates. **2 rows affected.**
5. **"Best-selling" defined as most net units sold.** Alternative: highest net revenue. Chosen: units, the plain reading of "best-selling"; the revenue view is reported alongside because the two answers differ (Keyboard by units, Laptop by revenue). **Best-selling product is (definition-dependent).**
6. **Missing region kept as "(missing)" (7 unique rows affected, 1,010.00 net).** Alternative: drop the rows from the region view or impute a region. Chosen: keep and bucket separately — dropping them would inflate the other regions' shares, and imputing geography would fabricate data. No headline metric depends on region.
7. **Zero-unit order kept (1 row).** ORD-1001 (2025-04-02, Headset, 0 units, 0.00). It has no effect on revenue or units; it counts as an April order in order counts.
8. **June is a partial month.** Data ends 2025-06-27, so June's figures understate a full month and month-over-month comparisons against June are caveated.
9. **Refund timing = the row's own date.** Refunds are booked in the month of their negative-amount row; there is no original-sale row to pair them with (verified above).
10. **Scope limits.** "Revenue" means the file's `amount` field as given (currency not stated; no tax, cost or margin fields). Arithmetic was verified on every row (`amount` = units × unit_price in all 131 unique rows, sign aside) — no rows had to be corrected, so no normalization counts to report beyond the items above.

## Total Revenue

The business netted just over sixty thousand in H1, but the honest number is only trustworthy after removing duplicate entries and netting refunds — both are quantified here.

| Measure | Amount | Notes |
|---|---:|---|
| Gross sales (positive amounts, deduped) | 62,595.00 | 120 sale rows |
| Refunds (negative amounts) | −2,380.00 | 11 rows, all full-quantity returns |
| **Total net revenue** | **60,215.00** | **(definition-dependent:** assumes dedup + refund netting**)** |
| Raw sum of the file as received | 60,485.00 | includes 10 duplicate rows worth +270.00 |
| Net revenue if refunds were excluded instead of netted | 62,595.00 | alternative reading of the negative rows |

Cross-checks: product, monthly and regional views below each sum independently to 60,215.00, and every row satisfies amount = units × unit_price.

## Best-Selling Product

Volume and value point at different products: the keyboard sells the most units at a low price point, while the laptop generates two-thirds of revenue — the right "best-seller" depends on whether the decision is about unit velocity or revenue.

**By units (headline): Keyboard — 93 net units (definition-dependent)** (97 gross units less 4 refunded; 38.3% of all net units sold).

| Product | Net units | Gross units | Refunded units | Net revenue | Revenue share |
|---|---:|---:|---:|---:|---:|
| Keyboard | 93 | 97 | 4 | 4,185.00 | 7.0% |
| Headset | 69 | 78 | 9 | 5,520.00 | 9.2% |
| Monitor | 49 | 56 | 7 | 10,510.00 | 17.5% |
| Laptop | 32 | 32 | 0 | 40,000.00 | 66.4% |
| **Total** | **243** | **263** | **20** | **60,215.00** | 100% |

By revenue the ranking inverts: Laptop leads with 40,000.00 (66.4% of net revenue) despite being last in units. Unit ranking is the same whether gross or net units are used, so the Keyboard result is robust to the refund-units choice.

## Monthly Revenue Breakdown

Revenue is lumpy and laptop-driven: the two strong months are exactly the months with heavy laptop deal flow, and the two weak months are the months with almost none — so the monthly trend is really a laptop pipeline trend.

Net revenue by month **(definition-dependent:** same dedup and refund-netting choices as the total**)**:

| Month | Orders | Gross sales | Refunds | Net revenue | Share of net |
|---|---:|---:|---:|---:|---:|
| 2025-01 | 19 | 10,855.00 | −660.00 | 10,195.00 | 16.9% |
| 2025-02 | 19 | 3,915.00 | −400.00 | 3,515.00 | 5.8% |
| 2025-03 | 27 | 20,160.00 | −45.00 | 20,115.00 | 33.4% |
| 2025-04 | 24 | 10,365.00 | −840.00 | 9,525.00 | 15.8% |
| 2025-05 | 21 | 11,975.00 | −220.00 | 11,755.00 | 19.5% |
| 2025-06 (to Jun 27) | 21 | 5,325.00 | −215.00 | 5,110.00 | 8.5% |
| **Total** | **131** | **62,595.00** | **−2,380.00** | **60,215.00** | 100% |

What is behind the swings (net revenue from laptops by month): Jan 8,750 / Feb 1,250 / Mar 15,000 / Apr 6,250 / May 7,500 / Jun 1,250. February and June are the weak months and each had exactly one laptop sale; March's peak is twelve laptop units. June is additionally a partial month (ends Jun 27), but the laptop gap, not the missing days, is the main driver of its softness.

## Other Notable Findings

Several patterns here matter for pricing, returns and regional strategy as much as the headline totals do.

- **Monitor price increase mid-period.** Every Monitor row from 2025-01-13 to 2025-04-28 is priced 210.00 (18 rows); every Monitor row from 2025-05-07 to 2025-06-21 is priced 220.00 (11 rows) — a clean +4.8% step change with no overlap, and no other product's price moves. Worth checking whether May–June monitor demand held up post-increase (net monitor revenue: Apr 1,470.00 → May 2,200.00 → Jun 2,640.00, suggesting it did).
- **Refunds concentrate in two accessory lines.** Of the 20 refunded units, Headsets account for 9 (11.5% of gross headset units) and Monitors 7 (12.5% of gross monitor units); Keyboards 4 (4.1%) and Laptops 0. In money, refunds are 3.8% of gross revenue (2,380.00 of 62,595.00). February's headset line netted exactly 0.00 — all five units sold that month came back.
- **Revenue is regionally concentrated.** Bandung 25,935.00 (43.1%), Medan 15,775.00 (26.2%), Jakarta 9,100.00 (15.1%), Surabaya 6,785.00 (11.3%), Denpasar 1,610.00 (2.7%), region missing 1,010.00 (1.7%). Bandung's lead is almost entirely laptops: 21,250.00 of its 25,935.00 is laptop revenue.
- **7 rows have no region** (1,010.00 net; includes one −160.00 refund), listed in the Assumptions section; ORD-1001 is a zero-unit, zero-amount order (kept, no financial effect).
- **Data quality, in one line:** of 141 incoming rows, 131 survive cleaning (10 exact duplicates removed, 11 negative-amount rows retained as refunds, 2 non-ISO dates parsed day-first, 7 missing-region rows retained, 1 zero-unit row retained, 0 unparseable dates, 0 arithmetic inconsistencies).
