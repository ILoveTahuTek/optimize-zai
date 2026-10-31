# Sales Analysis Report — `sales.csv` (H1 2025, "sales-2025h1-dirty")

**Method (summary):** the harness anomaly detector (`scripts/detect_anomalies.py`) was run on the raw file **before** any analysis; its inventory is reproduced verbatim below. All money figures are computed over **unique rows only** (exact duplicates removed), with refunds kept as negatives in NET. Every headline figure was recomputed by a **second, independent implementation** (Python/Decimal vs POSIX awk) — see Verification. Dates were parsed dual-format: ISO `YYYY-MM-DD` first, then `DD/MM/YYYY`; 0 rows failed to parse.

---

## 1. Headline figures (labeled per definitions)

| Figure | Value | Definition |
|---|---|---|
| **Total revenue (NET)** | **60,215.00** | Sum of `amount` over 131 unique rows; refunds as negatives. **This is the single "Total revenue" headline.** |
| GROSS revenue | 62,595.00 | Positive `amount` rows only (119 unique rows) |
| Refund total | 2,380.00 | Absolute value of the 11 negative rows |

Identity check: 62,595.00 − 2,380.00 = 60,215.00 ✓

**Row-count identity:** 141 raw rows = **131 unique rows + 10 exact duplicate rows** ✓

## 2. Best-selling product

By units and by net revenue **differ**, so both are reported:

| Rank | By units sold (positive-amount rows) | By NET revenue |
|---|---|---|
| 1 | **Keyboard — 97 units** (47 orders) | **Laptop — 40,000.00** (32 units, 14 orders) |
| 2 | Headset — 78 units | Monitor — 10,510.00 |
| 3 | Monitor — 56 units | Headset — 5,520.00 |
| 4 | Laptop — 32 units | Keyboard — 4,185.00 |

Net of refunds (units sold − units on refund rows) the ranking is unchanged: Keyboard 93, Headset 69, Monitor 49, Laptop 32. Laptop is #1 on revenue despite being #4 on units (unit price 1,250.00 vs Keyboard 45.00).

## 3. Monthly revenue breakdown (NET, unique rows)

| Month | Unique rows | **NET revenue** | GROSS | Refunds |
|---|---|---|---|---|
| 2025-01 | 19 | **10,195.00** | 10,855.00 | 660.00 |
| 2025-02 | 19 | **3,515.00** | 3,915.00 | 400.00 |
| 2025-03 | 27 | **20,115.00** | 20,160.00 | 45.00 |
| 2025-04 | 24 | **9,525.00** | 10,365.00 | 840.00 |
| 2025-05 | 21 | **11,755.00** | 11,975.00 | 220.00 |
| 2025-06 | 21 | **5,110.00** | 5,325.00 | 215.00 |
| **Total** | **131** | **60,215.00** | **62,595.00** | **2,380.00** |

Monthly row counts match the detector's strict-parser census exactly (19/19/27/24/21/21). The two `DD/MM/YYYY` rows (ORD-0071 `29/05/2025`, ORD-0066 `14/05/2025`) are included in **May** under the dual-format rule; both have day > 12 so the day-first reading is unambiguous. Note 2025-06 is a partial month (last order 2025-06-27).

## 4. Anomaly section (mandatory)

**Verbatim detector inventory** (run before any analysis):

```
== ANOMALY INVENTORY (pre-parse) ==
rows: 141 raw = 131 unique + 10 exact duplicates
date formats: {'ISO': 129, 'DD/MM/YYYY': 2}
non-ISO dates: 2 rows ['ORD-0071', 'ORD-0066']
unparseable dates: 0 []
monthly row census (strict parse): {'2025-01': 19, '2025-02': 19, '2025-03': 27, '2025-04': 24, '2025-05': 21, '2025-06': 21}
negative rows: 11 ['ORD-0083', 'ORD-0101', 'ORD-0118', 'ORD-0014', 'ORD-0067', 'ORD-0033', 'ORD-0084', 'ORD-0005', 'ORD-0128', 'ORD-0049', 'ORD-0043'] total 2380.00
zero-amount rows: 1 ['ORD-1001']
missing region: 7 rows
PRICE CHANGES: {'Monitor': ['210.00', '220.00']}
top-5 largest orders: [('ORD-0098', 5000.0), ('ORD-0129', 5000.0), ('ORD-0055', 5000.0), ('ORD-0111', 3750.0), ('ORD-0027', 3750.0)]
```

- **Exact duplicate rows: 10** (second copies of ORD-0014, ORD-0029, ORD-0034, ORD-0052, ORD-0057, ORD-0063, ORD-0065, ORD-0083, ORD-0089, ORD-0100; each appears exactly twice, byte-identical). Signed value of the 10 duplicate copies: **+270.00** — leaving them in would overstate NET revenue by 270.00 (raw sum 60,485.00 vs true NET 60,215.00). 8 of the 10 duplicated rows are positive sales; ORD-0014 (−420.00) and ORD-0083 (−45.00) are duplicated refunds.
- **Negative rows (refunds): 11, total 2,380.00.** IDs: ORD-0083 (−45.00), ORD-0101 (−240.00), ORD-0118 (−80.00), ORD-0014 (−420.00), ORD-0067 (−220.00), ORD-0033 (−90.00), ORD-0084 (−45.00), ORD-0005 (−80.00), ORD-0128 (−840.00), ORD-0049 (−160.00), ORD-0043 (−160.00). Every refund magnitude equals `units × unit_price` (full-line returns).
- **Zero-amount rows: 1** — ORD-1001 (2025-04-02, Headset, 0 units, 0.00). Contributes nothing to revenue; likely a data-entry artifact.
- **Missing fields:** `region` empty on 7 unique rows (ORD-0034, ORD-0086, ORD-0089, ORD-0105, ORD-0075, ORD-0046, ORD-0043), worth 1,010.00 NET (1.7% of NET revenue). No other column has missing values; no `order_id` appears with conflicting content.
- **Date-format census (unique rows):** ISO `YYYY-MM-DD` = 129; `DD/MM/YYYY` = 2 (ORD-0071, ORD-0066, both May); other/unparseable = 0.
- **Price changes:** **Monitor changed from 210.00 to 220.00** — 210.00 observed on 18 unique rows 2025-01-13 → 2025-04-28; 220.00 observed on 11 unique rows 2025-05-07 → 2025-06-21 (incl. one 220.00 refund, ORD-0067). Keyboard (45.00), Headset (80.00), Laptop (1,250.00) are constant. Monitor revenue mixes the two price points; no per-row price normalization was attempted (the `amount` column already reflects the row's price).

## 5. Anything else notable

- **Region split (NET):** Bandung 25,935.00 (29 rows) > Medan 15,775.00 (30) > Jakarta 9,100.00 (27) > Surabaya 6,785.00 (22) > Denpasar 1,610.00 (16) > missing 1,010.00 (7). Bandung alone is 43% of NET.
- **March is the peak month (20,115.00)** and is laptop-driven: four Laptop orders (ORD-0129, ORD-0055 at 5,000.00 each; ORD-0111 3,750.00; ORD-0092 1,250.00) account for 15,000.00 of it. Laptop demand is lumpy — February had only 1,250.00.
- **Largest orders:** three 5,000.00 orders (ORD-0098, ORD-0129, ORD-0055 — 4 Laptops each), then two 3,750.00 (ORD-0111, ORD-0027).
- **Internal consistency passed:** on all positive-amount unique rows `amount = units × unit_price`; on all 11 refund rows `|amount| = units × unit_price`. Refunds are 3.8% of GROSS.

## 6. Verification (two independent implementations)

Primary = Python 3 + `Decimal`, dedupe on full row tuple. Cross-check = POSIX awk, dedupe on whole raw line, float arithmetic. Result: **all figures match** (full log in `crosscheck.txt`).

| Figure | Primary | Cross-check |
|---|---|---|
| Raw rows | 141 | 141 |
| Unique rows | 131 | 131 |
| Exact duplicate rows | 10 | 10 |
| Duplicate signed value | +270.00 | +270.00 |
| **NET revenue** | **60,215.00** | **60,215.00** |
| GROSS revenue | 62,595.00 | 62,595.00 |
| Refund total | 2,380.00 | 2,380.00 |
| Monthly NET 01/02/03/04/05/06 | 10,195 / 3,515 / 20,115 / 9,525 / 11,755 / 5,110 | identical |
| Units sold Keyboard/Headset/Monitor/Laptop | 97 / 78 / 56 / 32 | identical |
| Product NET Laptop/Monitor/Headset/Keyboard | 40,000 / 10,510 / 5,520 / 4,185 | identical |
| Missing-region rows / unparsed dates | 7 / 0 | 7 / 0 |

---
*All amounts are in the file's currency units, 2 decimals. "Units sold" counts positive-amount rows; refund rows carry positive `units` and are excluded there (net-of-refund units shown in §2). Analysis scripts and raw outputs: `analysis_primary.py`, `crosscheck.awk`, `compare.py`, `analysis_primary.json`, `crosscheck.txt` in this directory; detector output `detect.json` next to the input CSV.*
