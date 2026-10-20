r"""XWILF in the all-pairs-wrap regime, large k (lead, 2026-10-20).  Pre-filter R subset (m/2, m), |R| = k, with
{0} u R u (R + R - m) = Z/m (then Ap is {0} u gens u wrapped pairs, all levels <= 3), then run the exact checker.
XWILF there <=> 3(m - 1 - k) <= k^2 + 2k.  usage: xwbreak2.py k mlo mhi"""
import sys, itertools
sys.path.insert(0, ".")
from xdead import analyse
k, mlo, mhi = map(int, sys.argv[1:4]); n = 0; nf = 0; best = None
for m in range(mlo, mhi + 1):
    lo = m // 2 + 1
    for rs in itertools.combinations(range(lo, m), k):
        cov = set(rs) | {0} | {(a + b - m) for i, a in enumerate(rs) for b in rs[i:]}
        if len(cov) < m: continue
        r = analyse([m] + [m + x for x in rs]); n += 1
        if r is None: continue
        if best is None or r["XWILF"] < best["XWILF"]: best = r
        if r["XWILF"] < 0:
            nf += 1
            if nf <= 5: print("XWILF FAIL", r, flush=True)
    print("m", m, "covering S so far", n, "fails", nf, flush=True)
print("k", k, "S", n, "XWILF fails", nf, "min", best)
