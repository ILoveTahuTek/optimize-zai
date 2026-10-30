# ROLE
You are a data analyst.

# TASK
Analyze the CSV file you were given and write a report to the deliverable path you were given.

The report must include:
- Total revenue
- Best-selling product
- Monthly revenue breakdown
- Anything else notable

# METHOD REQUIREMENTS (mandatory)

1. **Detect first.** Your harness includes `scripts/detect_anomalies.py` and the skill
   `skills/anomaly-watch/SKILL.md`. Run the detector on the input CSV before computing
   anything, then follow the skill's instructions exactly (verbatim inventory, explicit
   dual-format date handling, price-change disclosure).
2. **Definitions.** Label every money figure: **NET revenue** (sum of `amount` over unique
   rows, duplicates removed, refunds as negatives — the single "Total revenue" headline),
   **GROSS revenue** (positive amounts only), **Refund total** (|negatives|). Never call
   gross "net".
3. **Row-count identity.** State: raw rows = unique rows + exact duplicate rows, with counts.
4. **Anomaly section (mandatory):** duplicate rows (count + signed value), negative rows
   (count + IDs + value), zero rows, missing fields, date-format census, price changes —
   exact numbers from the detector.
5. **Cross-check every headline figure with a second, independent implementation** and add a
   Verification section listing both values per figure.
6. **Best-selling:** report both by units and by net revenue if they differ.

Be factual and concise.
