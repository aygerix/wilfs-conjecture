"""Count CR-failing (core, s) pairs with k+s >= 6 for core dimension k (lead, 2026-10-19), shapes only (no labelings).
Uses lcr3_exh.shapes / cr_fail_range.  Prints the number of height-3 core shapes, the failing (C,s) count, the shapes
failing for every s, and the largest s* and |C|+s* (the modulus range a labeling check must cover).
usage: python lcr4_count.py k"""
import sys
from lcr3_exh import shapes, cr_fail_range
k = int(sys.argv[1]); n3 = 0; nf = 0; ninf = 0; smax = 0; mmax = 0; hist = {}
for P, T in shapes(k):
    if not T: continue
    n3 += 1
    ss = cr_fail_range(k, P, T)
    if ss is None: continue
    if ss == float('inf'): ninf += 1; continue
    size = 1+k+len(P)+len(T)
    cnt = sum(1 for s in range(max(0, 6-k), int(ss)+1) if s < ss)
    if cnt:
        nf += cnt; smax = max(smax, float(ss)); mmax = max(mmax, size+int(ss))
        hist[size] = hist.get(size, 0)+cnt
print("k", k, "height-3 core shapes", n3, "failing-for-all-s", ninf, "CR-failing (C,s) with k+s>=6:", nf, "max s*", round(smax, 2), "max m needed", mmax)
print("failing (C,s) by |C|:", dict(sorted(hist.items())))
