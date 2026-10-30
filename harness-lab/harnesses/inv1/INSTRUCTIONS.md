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

1. **Definitions first.** Use exactly these definitions and label every money figure with one of them:
   - **NET revenue** = sum of `amount` over unique rows (exact duplicate rows removed), refund/negative rows included as negatives. This is the single primary headline number.
   - **GROSS revenue** = sum of positive `amount` over unique rows. Report it separately, labeled "gross".
   - **Refund total** = sum of |negative amounts| over unique rows. Report separately.
   Never call the gross figure "net". Never present more than one number under the label "Total revenue".
2. **Row-count identity.** State explicitly: raw data rows = unique rows + exact duplicate rows, with the actual counts.
3. **Verify every headline number two independent ways** (e.g., a Python script AND a separate hand computation or second script). Add a "Verification" section listing each headline figure and the two values you obtained; they must match exactly.
4. **Data quality section (exact numbers required):** count and value of exact duplicate rows, count and value of negative-amount rows, count of rows with missing fields, and any zero-amount rows.
5. **Best-selling:** report both by units and by revenue if they differ, and say which definition you use.

Be factual and concise.
