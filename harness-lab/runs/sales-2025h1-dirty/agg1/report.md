# Sales Analysis — H1 2025 (sales.csv)

**Scope:** 141 raw order rows, 2025-01-01 to 2025-06-27. Pre-analysis hygiene profiling and anomaly detection were run on the raw file before any aggregation (see Anomaly section and Verification table).

## Executive summary

1. H1 2025 **NET revenue is 60,215.00** (GROSS 62,595.00 less 2,380.00 refunds), but it is highly concentrated: Laptop alone is 40,000.00 (66.4% of NET) and the top-5 orders — all Laptops — are 22,500.00 (37.4% of NET).
2. "Best-selling" depends on the metric: **Laptop leads by net revenue (40,000.00) while Keyboard leads by units (93 net / 101 absolute)** — the Laptop's 1,250.00 price point, not volume, drives the revenue lead.
3. Monthly revenue is volatile — a March peak of 20,115.00 (33.4% of H1) and a **−56.5% drop into June (5,110.00)** even though June has a full month of rows (21, latest 2025-06-27) — and all data-hygiene defects found (10 duplicate rows, 2 non-ISO dates, 7 missing regions, 1 zero row) are accounted for below and do not change the headline.

## Definitions (labels used throughout)

- **NET revenue** = sum of `amount` over unique rows, duplicates removed, refunds as negatives. This is the single "Total revenue" headline.
- **GROSS revenue** = sum of positive `amount` only (unique rows).
- **Refund total** = |negative amounts| (unique rows).

## Row-count identity

**141 raw rows = 131 unique rows + 10 exact duplicate rows** (verified: 141 = 131 + 10).

## Headline figures

| Figure | Value |
|---|---|
| **NET revenue (headline "Total revenue")** | **60,215.00** |
| GROSS revenue | 62,595.00 |
| Refund total (11 rows) | 2,380.00 (3.8% of GROSS) |
| Identity check | GROSS 62,595.00 − Refunds 2,380.00 = NET 60,215.00 ✓ |

## Best-selling product

- **By net revenue (used for the headline): Laptop — 40,000.00 NET** (14 unique rows).
- **By units: Keyboard — 93 net units** (units signed by refund direction; 101 units if refund units are counted as absolute movement). Keyboard wins under either units convention, so the units leader is unambiguous.

| Product | Units (net / abs) | NET revenue | GROSS revenue |
|---|---|---|---|
| Laptop | 32 / 32 | 40,000.00 | 40,000.00 |
| Monitor | 49 / 63 | 10,510.00 | 11,990.00 |
| Headset | 69 / 87 | 5,520.00 | 6,240.00 |
| Keyboard | 93 / 101 | 4,185.00 | 4,365.00 |
| **Total** | 243 / 283 | **60,215.00** | **62,595.00** |

*Both metrics are shown because they differ; NET revenue is the decision metric here, and the units leader (Keyboard) contributes only 7.0% of NET.*

## Monthly revenue breakdown (NET, unique rows, dual-format date parse)

| Month | Rows | NET revenue | Share of H1 | MoM |
|---|---|---|---|---|
| 2025-01 | 19 | 10,195.00 | 16.9% | — |
| 2025-02 | 19 | 3,515.00 | 5.8% | −65.5% |
| 2025-03 | 27 | 20,115.00 | 33.4% | +472.1% |
| 2025-04 | 24 | 9,525.00 | 15.8% | −52.6% |
| 2025-05 | 21 | 11,755.00 | 19.5% | +23.4% |
| 2025-06 | 21 | 5,110.00 | 8.5% | −56.5% |
| **Total** | **131** | **60,215.00** | 100% | |

*May includes 260.00 from the 2 rows recorded in DD/MM/YYYY format (see Anomaly section). The profiler's raw monthly table showed those 260.00 under two malformed keys (`14/05/2`, `29/05/2`) because it slices the date string; the dual-format parse folds them into May. All other months match the profiler exactly.*

## Anomaly section (counts verbatim from the detector/profiler)

- **Duplicate rows: 10** exact duplicates (10 order IDs, each appearing exactly twice). **SIGNED value +270.00** (includes two refund copies: ORD-0014 −420.00, ORD-0083 −45.00). If all raw rows were summed, NET would be overstated by 270.00 (60,485.00 vs 60,215.00). *Note: the profiler prints "duplicates add 735.00 if wrongly counted" — that figure is the positive-only sum of the extra copies (735.00), i.e. it ignores the −465.00 of duplicated refunds. Both numbers reconcile to the same underlying rows; the signed figure per the report spec is 270.00.*
- **Negative rows (refunds): 11**, total **−2,380.00**: ORD-0083, ORD-0101, ORD-0118, ORD-0014, ORD-0067, ORD-0033, ORD-0084, ORD-0005, ORD-0128, ORD-0049, ORD-0043.
- **Zero rows: 1** — ORD-1001 (2025-04-02, Headset, units=0, amount 0.00; no revenue impact).
- **Missing fields:** region missing on **7 rows**, worth **1,010.00 NET** (1.7% of NET); these rows are kept in all totals. No other field (order_id, date, product, units, unit_price, amount) is ever blank.
- **Date-format census:** **129 ISO (YYYY-MM-DD), 2 DD/MM/YYYY, 0 unparseable.** The 2 non-ISO rows are ORD-0071 (`29/05/2025`, Keyboard, 180.00) and ORD-0066 (`14/05/2025`, Headset, 80.00). Both were handled with an explicit dual-format parse (ISO tried first, then day-first) and land in **2025-05**; day-first is unambiguous here because `29/05/2025` cannot be read as an ISO date.
- **Price change: Monitor 210.00 → 220.00.** Last order at 210.00: 2025-04-28 (18 unique rows at 210.00). **First affected order at 220.00: ORD-0067, 2025-05-07** (a −220.00 refund); the first revenue order at the new price is ORD-0038, 2025-05-12. 11 unique rows carry the 220.00 price (10 revenue rows, 5,060.00 GROSS; net 4,840.00 after the refund). No other product has more than one unit price; the profiler found 0 price-consistency violations (amount = units × unit_price holds on every positive row).
- **Concentration / outliers (not defects):** top-5 orders are ORD-0098 5,000.00, ORD-0129 5,000.00, ORD-0055 5,000.00, ORD-0111 3,750.00, ORD-0027 3,750.00 — all Laptop, 22,500.00 = 37.4% of NET.
- **Region mix (NET):** Bandung 25,935.00 (43.1%), Medan 15,775.00 (26.2%), Jakarta 9,100.00 (15.1%), Surabaya 6,785.00 (11.3%), Denpasar 1,610.00 (2.7%), missing-region rows 1,010.00 (1.7%).

## Verification table (tool vs independent second implementation)

Every headline figure was recomputed with an independently written script (`verify.py`, stdlib `csv`, full-row dedupe, explicit dual-format date parse) rather than copied from the tools.

| Figure | Tool (profiler / detector) | Independent (verify.py) | Match |
|---|---|---|---|
| Raw rows | 141 | 141 | ✓ |
| Unique rows | 131 | 131 | ✓ |
| Exact duplicate rows | 10 | 10 | ✓ |
| **NET revenue** | 60,215.00 | 60,215.00 | ✓ |
| GROSS revenue | 62,595.00 | 62,595.00 | ✓ |
| Refund total / rows | 2,380.00 / 11 (same IDs) | 2,380.00 / 11 (same IDs) | ✓ |
| Zero rows | 1 (ORD-1001) | 1 (ORD-1001) | ✓ |
| Missing region | 7 rows, 1,010.00 | 7 rows, 1,010.00 | ✓ |
| Date census | 129 ISO / 2 DD/MM / 0 unparseable | 129 ISO / 2 DD/MM / 0 unparseable | ✓ |
| Monthly row census | 19/19/27/24/21/21 (=131) | 19/19/27/24/21/21 (=131) | ✓ |
| NET by product | Laptop 40,000 / Monitor 10,510 / Headset 5,520 / Keyboard 4,185 | identical | ✓ |
| NET by month | Jan 10,195; Feb 3,515; Mar 20,115; Apr 9,525; Jun 5,110; May split 11,495 + 80 + 180 (malformed keys) | Jan 10,195; Feb 3,515; Mar 20,115; Apr 9,525; **May 11,755**; Jun 5,110 | ✓ reconciled* |
| Duplicate value | 735.00 ("if wrongly counted", positive-only) | 270.00 signed (735.00 positive-only reproduced) | ✓ reconciled** |
| Price change | Monitor 210.00 → 220.00 | same; first affected ORD-0067 (2025-05-07); 11 rows at 220.00 | ✓ |
| Top-5 orders | identical list | identical list | ✓ |

\* Monthly totals reconcile exactly: tool total = 60,215.00 (the two DD/MM rows appear as malformed keys worth 80.00 + 180.00); independent parse moves those 260.00 into May (11,495 + 260 = 11,755). No month other than May differs.
\** Not a data disagreement — a definitional one, disclosed per the data-hygiene skill. The profiler's script sums only positive duplicate amounts (`amount > 0`), giving 735.00; the report spec requires the signed value of the 10 duplicate copies, which is 270.00 (735.00 − 465.00 of duplicated refunds). Both were reproduced from the same 10 rows.

## Assumptions & Limitations

1. **Deduplication = exact match on all 7 fields, first occurrence kept** (matches the tools' definition). Alternative considered: dedupe by `order_id` only — equivalent here because every repeated `order_id` is an exact-duplicate pair (verified: 10 IDs × 2 copies, no ID repeated with different content). Affects 10 rows / 270.00 signed.
2. **Refunds stay in NET as negatives** (mandated definition). Alternative: exclude them entirely → headline would be GROSS 62,595.00; rejected because refunds are real revenue events. 11 rows / 2,380.00 affected. Any figure labeled GROSS is definition-dependent on this choice.
3. **Dual-format date parse, day-first fallback.** The 2 non-ISO rows (`29/05/2025`, `14/05/2025`) cannot be ISO dates (day 29/14 out of month range), so day-first is unambiguous; both fall in May 2025, moving 260.00 into May's NET. 2 rows affected. This is the only reason May (11,755.00) differs from the profiler's raw table (11,495.00 + malformed keys).
4. **Units are signed by refund direction for "best-selling by units"** (refund rows carry positive `units` with negative `amount`). Alternative: count absolute units — reported as well; Keyboard leads under both conventions, so the conclusion is robust. 11 refund rows affect this.
5. **Zero row ORD-1001 kept in row counts** (contributes 0.00); alternative would be to drop it — no effect on any money figure. 1 row.
6. **Missing-region rows kept in all revenue totals**; the region mix section simply excludes them (1,010.00 / 1.7% of NET unattributed). 7 rows.
7. **Monitor price change requires no adjustment** — NET by product uses actual `amount` values, not price × units, so the 210.00→220.00 change flows through correctly. Disclosure made per spec; 11 rows at the new price.
8. **June looks like a genuine slowdown, not truncation** — June has 21 rows (equal to May) and activity through 2025-06-27, so only ~3 days of the month are absent; even so, single-month reads are noisy given H1 volatility (Feb −65.5%, Mar +472%).
9. The file contains **no rows outside H1 2025** (min 2025-01-01, max 2025-06-27), so no period filtering was applied.
