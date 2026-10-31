#!/usr/bin/awk -f
# Independent cross-check for sales-2025h1-dirty (awk; deliberately NOT the Python profiler).
# Assumes: no quoted fields, comma-only separators (verified by reading the file).
# Definitions match harness: NET = sum(amount) over unique rows; GROSS = positive-only;
# refunds = |negative amounts|; duplicate = later exact full-row match.
BEGIN { FS = "," }
NR == 1 {
    sub(/\r$/, "")                       # file is CRLF; strip so header compare is exact
    if ($0 != "order_id,date,product,units,unit_price,region,amount")
        print "HEADER MISMATCH: " $0
    next
}
{
    sub(/\r$/, "")                       # file is CRLF; strip so string compares are exact
    raw++
    if (seen[$0]++) {                       # exact full-row duplicate
        dupes++
        if ($7 + 0 > 0) dupeval += $7
        duperef += ($7 + 0 < 0 ? -$7 : 0)
        next
    }
    uniq++
    amt = $7 + 0
    net += amt
    if (amt < 0) { neg++; negid[neg] = $1; refund += -amt }
    else if (amt == 0) { zero++; zeroid[zero] = $1 }
    else gross += amt
    if ($6 == "") { missreg++; missval += amt; mrid[missreg] = $1 }
    if (amt > 0 && $4 * $5 != amt) pricebad++
    # month bucket, normalizing stray DD/MM/YYYY rows to YYYY-MM
    d = $2
    if (d ~ /^[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]$/) {
        split(d, p, "/"); m = p[3] "-" p[2]; baddate++
        badid[baddate] = $1 ":" d
    } else m = substr(d, 1, 7)
    bymonth[m] += amt
    byprod[$3] += amt
    if (amt > 0) upos[$3] += $4
    unet[$3] += (amt < 0 ? -$4 : $4)      # refund rows carry positive units; subtract them
    nd = (m substr(d, length(d) - 2))     # YYYY-MM-DD normalized key for range check
    if (mind == "" || nd < nmin) { nmin = nd; mind = d }
    if (nd > nmax) { nmax = nd; maxd = d }
    for (i = 1; i <= 7; i++) if ($i == "") empty[i]++
    if ($1 in oid && oidrow[$1] != $0) idx[$1] = 1   # same order_id, different content
    oid[$1]++; oidrow[$1] = $0
}
END {
    printf "raw=%d unique=%d dupes=%d (identity %s)\n", raw, uniq, dupes, (raw == uniq + dupes ? "OK" : "FAIL")
    printf "dupe_pos_value=%.2f dupe_refund_value=%.2f raw_sum_overstates_net_by=%.2f\n", dupeval, duperef, dupeval - duperef
    printf "NET=%.2f GROSS=%.2f refunds=%.2f identity %s\n", net, gross, refund, (net == gross - refund ? "OK" : "FAIL")
    printf "negrows=%d:", neg
    for (i = 1; i <= neg; i++) printf " %s", negid[i]
    printf "\n"
    printf "zerorows=%d:", zero
    for (i = 1; i <= zero; i++) printf " %s", zeroid[i]
    printf "\n"
    printf "missing_region=%d value=%.2f:", missreg, missval
    for (i = 1; i <= missreg; i++) printf " %s", mrid[i]
    printf "\n"
    printf "price_violations=%d baddate_rows=%d:", pricebad, baddate
    for (i = 1; i <= baddate; i++) printf " %s", badid[i]
    printf "\n"
    for (m in bymonth) printf "month %s %.2f\n", m, bymonth[m]
    for (pr in byprod) printf "prod %s net=%.2f units_pos=%d units_net=%d\n", pr, byprod[pr], upos[pr], unet[pr]
    for (i in empty) printf "empty_field col=%d count=%d\n", i, empty[i]
    n = 0
    for (k in idx) { printf "id_diff_content %s\n", k; n++ }
    if (n == 0) print "no order_id repeated with differing content"
    printf "date_range=%s..%s (normalized ISO)\n", mind, maxd
}
