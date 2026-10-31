# Sales Report — sales-2025h1-dirty (2025 H1)

Source: `tasks/sales-2025h1-dirty/sales.csv` · 141 raw rows · period covered 2025-01-01 → 2025-06-27.

## Headline

**Total revenue (NET) = 60,215.00** — sum of `amount` over unique rows, refund/negative rows included as negatives. This is the single primary figure; every other money figure below is labeled.

- **Gross revenue = 62,595.00** (positive `amount` only, unique rows).
- **Refund total = 2,380.00** (absolute value of the 11 negative-amount rows).
- Identity: 62,595.00 − 2,380.00 = 60,215.00 ✓

## Row-count identity

**141 raw rows = 131 unique rows + 10 exact duplicate rows** ✓

## Best-selling product

The two definitions give different winners; both are reported.

| Rank | By **NET revenue** (primary) | By **units sold** (unique rows) |
|---|---|---|
| 1 | **Laptop — 40,000.00 NET** (66.4% of NET) | **Keyboard — 97 sales units** (93 net of refunds) |
| 2 | Monitor — 10,510.00 NET (17.5%) | Headset — 78 sales units (69 net) |
| 3 | Headset — 5,520.00 NET (9.2%) | Monitor — 56 sales units (49 net) |
| 4 | Keyboard — 4,185.00 NET (7.0%) | Laptop — 32 sales units (32 net) |

- Definition used for the headline: **NET revenue over unique rows** → best-selling product is the **Laptop**.
- **Keyboard** is best-selling **by units** (97 units sold, before deducting the 4 refunded units). "Sales units" counts `units` on positive-amount rows; net units additionally subtract refund-row units.

## Monthly revenue breakdown (NET, unique rows)

| Month | NET revenue | Share |
|---|---|---|
| 2025-01 | 10,195.00 | 16.9% |
| 2025-02 | 3,515.00 | 5.8% |
| 2025-03 | 20,115.00 | 33.4% |
| 2025-04 | 9,525.00 | 15.8% |
| 2025-05 | 11,755.00 | 19.5% |
| 2025-06 | 5,110.00 | 8.5% |
| **Total** | **60,215.00** | 100% |

Note: two rows carry DD/MM/YYYY dates (ORD-0071 `29/05/2025`, ORD-0066 `14/05/2025`, worth 260.00 NET combined). Both fall in **May 2025** and are included in the 11,755.00 above after normalization. Naive month-bucketing of the raw strings produces two spurious "months" (`29/05/2` = 180.00, `14/05/2` = 80.00) and understates May as 11,495.00.

## Data quality (exact numbers)

- **Duplicate rows: 10** exact duplicates of 10 distinct orders — ORD-0100, ORD-0057, ORD-0065, ORD-0089, ORD-0063, ORD-0034, ORD-0052, ORD-0029, plus refunds ORD-0014 (−420.00) and ORD-0083 (−45.00). Counting all raw rows would overstate NET by **270.00** (+735.00 of double-counted sales less 465.00 of double-counted refunds).
- **Negative rows (refunds): 11** unique rows, total **2,380.00** — ORD-0005 (−80.00), ORD-0014 (−420.00), ORD-0033 (−90.00), ORD-0043 (−160.00), ORD-0049 (−160.00), ORD-0067 (−220.00), ORD-0083 (−45.00), ORD-0084 (−45.00), ORD-0101 (−240.00), ORD-0118 (−80.00), ORD-0128 (−840.00). By product: Monitor 1,480.00, Headset 720.00, Keyboard 180.00, Laptop 0.
- **Zero-amount rows: 1** — ORD-1001 (2025-04-02, Headset, 0 units, 0.00). Contributes nothing to revenue; ID is out of sequence with ORD-0001–0130 and looks like a placeholder/test row.
- **Missing fields: 7 rows with empty `region`** worth **1,010.00 NET** — ORD-0034 (45.00), ORD-0075 (135.00), ORD-0086 (160.00), ORD-0089 (90.00), ORD-0105 (660.00), ORD-0046 (80.00), ORD-0043 (−160.00). `region` is the only column with missing values; no other field is empty anywhere in the file.
- **Date-format anomalies: 2** rows in DD/MM/YYYY instead of ISO (ORD-0071, ORD-0066; both May 2025 — see monthly note).
- **Price-consistency violations: 0** (`units × unit_price = amount` holds on every positive row).
- **No order_id is repeated with differing content** — deduplication by exact row is unambiguous.
- File uses CRLF line endings (cosmetic; handled by both tools).

## Anything else notable

- **Laptop concentration:** one product is 66.4% of NET revenue; the top month (March, 33.4% of NET) is laptop-driven (two 5,000.00 sales, one 3,750.00).
- **Monitor price change:** all Monitors sell at 210.00 through 2025-04-28, then at 220.00 from 2025-05-07 onward (consistent arithmetic on both sides of the change — not a data error).
- **June is the weakest month** (5,110.00 NET) but the data runs only through 2025-06-27, so June is nearly complete; it is genuinely low, not truncated.
- Refunds are spread across all months except March; the largest single refund is ORD-0128 (−840.00, 4 × Monitor, April).

## Verification (per-figure cross-check)

Every figure was computed twice: once by the harness profiler `profile_csv.py` (Python, evidence base) and once by an independent `awk` implementation written for this run (`crosscheck.awk`, saved next to this report with its output `crosscheck.out`).

| Figure | Profiler | awk cross-check | Match |
|---|---|---|---|
| raw = unique + duplicates | 141 = 131 + 10 | 141 = 131 + 10 | ✓ |
| NET revenue | 60,215.00 | 60,215.00 | ✓ |
| GROSS revenue | 62,595.00 | 62,595.00 | ✓ |
| Refund total / rows | 2,380.00 / 11 (same IDs) | 2,380.00 / 11 (same IDs) | ✓ |
| Duplicates-if-counted (positive side) | 735.00 | 735.00 (refund side −465.00 also found) | ✓ |
| Zero-amount rows | 1 (ORD-1001) | 1 (ORD-1001) | ✓ |
| Missing `region` | 7 rows / 1,010.00 | 7 rows / 1,010.00 (same IDs) | ✓ |
| NET by product (Laptop/Monitor/Headset/Keyboard) | 40,000 / 10,510 / 5,520 / 4,185 | identical | ✓ |
| NET by month | matches after normalizing the 2 stray date formats | identical (normalization built in) | ✓ |
| Price-consistency violations | 0 | 0 | ✓ |
