#!/usr/bin/env mawk -f
# Method B: independent verification of sales.csv headline figures (mawk).
# Money handled as integer cents to avoid float artifacts.
BEGIN { FS = "," }
NR == 1 { sub(/\r$/, ""); header = $0; next }
{
    sub(/\r$/, "")
    if (NF == 0) next
    raw++
    if (NF != 7) badfc++

    # raw-level data-quality scans (include duplicate occurrences)
    amt = $7 + 0
    cents = (amt < 0) ? int(amt * 100 - 0.5) : int(amt * 100 + 0.5)
    if (amt < 0) { negraw++; negvalraw += -cents }
    if (amt == 0) zeroraw++
    mcell = 0
    for (i = 1; i <= 7; i++) {
        if ($i == "") { mcell++; missf[i]++ }
    }
    if (mcell > 0) { missrows++; misscells += mcell }

    # exact-duplicate detection on the full raw line
    key = $0
    if (key in seen) {
        dup++
        dupval += cents
        next
    }
    seen[key] = 1

    # --- unique-row processing ---
    uniqn++
    un = $4 + 0
    m = substr($2, 1, 7)
    ord[m]++
    units[m] += un
    net += cents
    netm[m] += cents
    if (amt > 0) {
        gross += cents
        grossm[m] += cents
    } else if (amt < 0) {
        refund += -cents
        refundm[m] += -cents
        neguniq++
    } else zerouniq++

    # integrity: amount == units*unit_price or its negation
    calc = int(($5 + 0) * un * 100 + 0.5)
    if (cents != calc && cents != -calc) mism++

    p = $3
    pu[p] += un
    psu[p] += (amt > 0 ? un : (amt < 0 ? -un : 0))
    pnet[p] += cents
    if (amt > 0) pgross[p] += cents
    pord[p]++

    reg = ($6 == "" ? "(missing)" : $6)
    rord[reg]++
    rnet[reg] += cents

    if (mind == "" || $2 < mind) mind = $2
    if ($2 > maxd) maxd = $2
}
END {
    printf "header=%s\n", header
    printf "bad_fieldcount_rows=%d\n", badfc
    printf "raw_rows=%d\n", raw
    printf "unique_rows=%d\n", uniqn
    printf "dup_rows=%d\n", dup
    printf "dup_value=%.2f\n", dupval / 100
    printf "neg_rows_raw=%d\n", negraw
    printf "neg_rows_unique=%d\n", neguniq
    printf "neg_value_raw=%.2f\n", negvalraw / 100
    printf "refund_total=%.2f\n", refund / 100
    printf "zero_rows_raw=%d\n", zeroraw
    printf "zero_rows_unique=%d\n", zerouniq
    printf "missing_cells_raw=%d\n", misscells
    printf "missing_rows_raw=%d\n", missrows
    printf "missing_field[order_id]=%d\n", missf[1]
    printf "missing_field[date]=%d\n", missf[2]
    printf "missing_field[product]=%d\n", missf[3]
    printf "missing_field[units]=%d\n", missf[4]
    printf "missing_field[unit_price]=%d\n", missf[5]
    printf "missing_field[region]=%d\n", missf[6]
    printf "missing_field[amount]=%d\n", missf[7]
    printf "net_revenue=%.2f\n", net / 100
    printf "gross_revenue=%.2f\n", gross / 100
    printf "refund_total2=%.2f\n", refund / 100
    printf "amount_sign_price_mismatches=%d\n", mism
    n = split("2025-01 2025-02 2025-03 2025-04 2025-05 2025-06", ML, " ")
    for (i = 1; i <= n; i++) {
        m = ML[i]
        printf "orders[%s]=%d\n", m, ord[m]
        printf "units[%s]=%d\n", m, units[m]
        printf "gross[%s]=%.2f\n", m, grossm[m] / 100
        printf "refund[%s]=%.2f\n", m, refundm[m] / 100
        printf "net[%s]=%.2f\n", m, netm[m] / 100
    }
    printf "months=%s\n", "2025-01,2025-02,2025-03,2025-04,2025-05,2025-06"
    printf "date_min=%s\n", mind
    printf "date_max=%s\n", maxd
    np = split("Headset Keyboard Laptop Monitor", PL, " ")
    for (i = 1; i <= np; i++) {
        p = PL[i]
        printf "p_orders[%s]=%d\n", p, pord[p]
        printf "p_units[%s]=%d\n", p, pu[p]
        printf "p_signed_units[%s]=%d\n", p, psu[p]
        printf "p_gross[%s]=%.2f\n", p, pgross[p] / 100
        printf "p_net[%s]=%.2f\n", p, pnet[p] / 100
    }
    # regions discovered dynamically
    nr = 0
    for (r in rord) rlist[nr++] = r
    # insertion sort
    for (i = 1; i < nr; i++) {
        v = rlist[i]
        for (j = i - 1; j >= 0 && rlist[j] > v; j--) rlist[j+1] = rlist[j]
        rlist[j+1] = v
    }
    for (i = 0; i < nr; i++) {
        r = rlist[i]
        printf "r_orders[%s]=%d\n", r, rord[r]
        printf "r_net[%s]=%.2f\n", r, rnet[r] / 100
    }
}
