# Sales Analysis Report — sales-2025h2

Source: `/home/z/my-project/harness-lab/tasks/sales-2025h2/sales.csv` (118 data rows, 2025-07 through 2025-12).
Method: profiler (`profile_csv.py`) run first; every headline figure independently recomputed with a second implementation (SQLite + integer-cents arithmetic, `crosscheck.py`). All values below were verified to match the profiler exactly (see Verification).

## Total revenue

- **Total revenue (NET)** = **290,480.00** — sum of `amount` over the 112 unique rows, refund/negative rows included as negatives. This is the single headline figure.
- **Gross revenue** = **290,850.00** — sum of positive `amount` over unique rows.
- **Refund total** = **370.00** — sum of |negative amounts| over unique rows (2 rows). Identity holds: gross 290,850.00 − refunds 370.00 = net 290,480.00.

## Best-selling product

By **units** (unique rows): **Laptop — 214 units**.
By **net revenue**: **Laptop — 267,500.00 net (92.1% of net revenue)**.

The #1 product is Laptop under both definitions; the definition matters only for places 2–4:

| Rank | By units (all rows) | By net revenue |
|---|---|---|
| 1 | Laptop — 214 | Laptop — 267,500.00 |
| 2 | Keyboard — 84 | Monitor — 13,440.00 |
| 3 | Headset — 76 | Headset — 5,760.00 |
| 4 | Monitor — 66 | Keyboard — 3,780.00 |

**Refund netting and the units ranking:** netting refunds out of units (excluding the units on the 2 refund rows: 1 Monitor, 2 Headset) gives Laptop 214, Keyboard 84, Headset 74, Monitor 65 — the ranking is unchanged. (Units here are as recorded on the order lines; the 2 refund rows carry positive units with negative amounts, and the 1 zero-amount row carries 0 units.)

## Monthly revenue breakdown (NET)

| Month | Net revenue | Share of net |
|---|---|---|
| 2025-07 | 4,075.00 | 1.4% |
| 2025-08 | 7,335.00 | 2.5% |
| 2025-09 | 253,280.00 | 87.2% |
| 2025-10 | 5,805.00 | 2.0% |
| 2025-11 | 8,710.00 | 3.0% |
| 2025-12 | 11,275.00 | 3.9% |
| **Total** | **290,480.00** | 100% |

All figures are NET (unique rows, refunds as negatives). The monthly sums and the product sums each equal the 290,480.00 total.

## Row-count identity

**Raw rows 118 = unique rows 112 + exact duplicate rows 6.**

## Data quality (exact numbers from the profiler)

- **Exact duplicate rows: 6**, signed value if wrongly counted **+4,630.00** (all 6 are positive-amount rows, so the signed sum equals the positive-only sum; no duplicated refund). Duplicate order IDs, each appearing exactly twice: ORD-0021, ORD-0026, ORD-0054, ORD-0065, ORD-0068, ORD-0105.
- **Negative rows (refunds): 2** — ORD-0052 (−210.00, Monitor, 2025-08-30) and ORD-0048 (−160.00, Headset, 2025-09-24); total −370.00.
- **Zero-amount rows: 1** — ORD-0902 (Headset, 0 units, 0.00; no revenue impact).
- **Missing fields (region): 9 unique rows** worth **4,465.00** net (1.5% of net revenue) — ORD-0003, ORD-0015, ORD-0024, ORD-0050, ORD-0069, ORD-0070, ORD-0078, ORD-0091, ORD-0105. (10 raw rows have a blank region; one, ORD-0105, is a duplicate.) No other required fields are missing.
- **Price consistency:** 0 violations — for every positive row, `units × unit_price = amount`.

## Anything else notable

1. **One wholesale order dominates the half.** ORD-0901 (2025-09-14, Jakarta): 200 units of Laptop for **250,000.00** — 86.1% of total net revenue. Excluding it, net revenue for the half would be **40,480.00**, and September would drop from 253,280.00 to 3,280.00 (last of the six months). The apparent September/Laptop "peak" is a single-transaction effect, not a trend; ordinary monthly net revenue runs ~3,300–11,300.
2. **Refunds are immaterial:** 370.00 (0.13% of gross), both in H2 products (Monitor, Headset).
3. **Duplicate rows would overstate revenue by +4,630.00 (1.6%)** if not removed; they were excluded from all figures above.
4. **Region coverage is incomplete:** 9 unique rows (4,465.00 net) have no region, which limits any regional breakdown (none is claimed in this report).
5. File hygiene: the CSV uses CRLF line endings and has no quoting; it parses cleanly (header + 118 data rows).

## Verification

Second implementation: `crosscheck.py` — CSV parsed by plain `split(',')`, money handled as exact integer cents (string parsing, no floats/Decimal), all aggregation done in SQLite SQL (`SUM`/`GROUP BY`) rather than Python loops. Independent values matched the profiler exactly on all 21 checks (0 disagreements):

| Figure | Profiler | Independent | Match |
|---|---|---|---|
| NET revenue | 290,480.00 | 290,480.00 | ✓ |
| GROSS revenue | 290,850.00 | 290,850.00 | ✓ |
| Refund total | 370.00 | 370.00 | ✓ |
| Monthly 2025-07 | 4,075.00 | 4,075.00 | ✓ |
| Monthly 2025-08 | 7,335.00 | 7,335.00 | ✓ |
| Monthly 2025-09 | 253,280.00 | 253,280.00 | ✓ |
| Monthly 2025-10 | 5,805.00 | 5,805.00 | ✓ |
| Monthly 2025-11 | 8,710.00 | 8,710.00 | ✓ |
| Monthly 2025-12 | 11,275.00 | 11,275.00 | ✓ |
| Duplicate rows | 6 (+4,630.00) | 6 (+4,630.00) | ✓ |
| Negative rows | 2 | 2 | ✓ |
| Zero-amount rows | 1 | 1 | ✓ |
| Missing-region rows / value | 9 / 4,465.00 | 9 / 4,465.00 | ✓ |
| Row counts (raw/unique/dupe) | 118/112/6 | 118/112/6 | ✓ |

Extra checks run beyond the required minimum, all passing: (a) internal identities — NET = GROSS − refunds; monthly sum = product sum = NET; (b) per-product net totals (Laptop 267,500.00, Monitor 13,440.00, Headset 5,760.00, Keyboard 3,780.00) re-derived independently; (c) units × unit_price = amount re-verified independently (0 violations); (d) duplicate order IDs enumerated independently (6 IDs, each ×2); (e) units rankings computed both with and without refund rows.
