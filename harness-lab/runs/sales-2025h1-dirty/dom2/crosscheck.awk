#!/usr/bin/env awk -f
# Independent cross-check for sales-2025h1-dirty (different language + logic from analysis_primary.py).
# Line-based: dedupe exact duplicate LINES, dual-format date (ISO yyyy-mm-dd if it contains '-',
# else dd/mm/yyyy if it contains '/'). Float arithmetic, rounded at print time.
# Portable POSIX awk: no asorti; MONTH/PRODUCT lines are sorted downstream with `sort`.
BEGIN { FS = "," }
NR == 1 { next }
{
    sub(/\r$/, "")                 # strip CRLF
    line = $0
    if (seen[line]++) { dups++; dupval += $7; next }   # exact duplicate row (2nd+ copy)
    uniq++
    amt = $7 + 0
    net += amt
    if (amt > 0) { gross += amt; units[$3] += $4; pgross[$3] += amt }
    else if (amt < 0) { refund += -amt; refunits[$3] += $4 }
    pnet[$3] += amt
    # dual-format month extraction
    if (index($2, "-") > 0) m = substr($2, 1, 7)
    else if (index($2, "/") > 0) { split($2, a, "/"); m = a[3] "-" a[2] }
    else { bad[++nb] = $1 }
    mnet[m] += amt; mrows[m]++
    if (amt > 0) mgross[m] += amt; else if (amt < 0) mrefund[m] += -amt
    if ($6 == "") missreg++
    if (amt != $4 * $5 + 0 && amt >= 0) mismatch = mismatch " " $1
    if (amt < 0 && (-amt) != $4 * $5 + 0) refmismatch = refmismatch " " $1
}
END {
    printf "raw=%d unique=%d dupes=%d dup_signed=%.2f raw_net_minus_unique_net=%.2f\n", NR - 1, uniq, dups, dupval, dupval
    printf "NET=%.2f GROSS=%.2f REFUND=%.2f\n", net, gross, refund
    for (m in mnet) printf "MONTH %s rows=%d net=%.2f gross=%.2f refund=%.2f\n", m, mrows[m], mnet[m], mgross[m], mrefund[m]
    for (p in pnet) printf "PRODUCT %s units_sold=%d units_ref=%d net=%.2f gross=%.2f\n", p, units[p], refunits[p], pnet[p], pgross[p]
    printf "missing_region=%d unparsed=%d amount_mismatch_pos=%s refund_mag_mismatch=%s\n", missreg, nb, mismatch, refmismatch
}
