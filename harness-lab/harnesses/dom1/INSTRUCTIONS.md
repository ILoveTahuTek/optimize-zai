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

1. **Profile first.** Your harness includes `scripts/profile_csv.py` and the skill
   `skills/data-hygiene/SKILL.md`. Run the profiler on the input CSV before computing
   anything yourself, then follow the skill's instructions (evidence base + independent
   cross-check).
2. **Definitions.** Use exactly these definitions and label every money figure with one of them:
   - **NET revenue** = sum of `amount` over unique rows (exact duplicate rows removed), refund/negative rows included as negatives. This is the single primary headline number ("Total revenue").
   - **GROSS revenue** = sum of positive `amount` over unique rows. Report separately, labeled "gross".
   - **Refund total** = sum of |negative amounts| over unique rows.
   Never call the gross figure "net".
3. **Row-count identity.** State: raw rows = unique rows + exact duplicate rows, with actual counts.
4. **Data quality section:** duplicate rows (count + value if counted), negative rows (count + IDs + value), zero-amount rows, missing fields (count + value) — taken from the profiler and stated as exact numbers.
5. **Best-selling:** report both by units and by revenue if they differ, and say which definition you use.

Be factual and concise.
