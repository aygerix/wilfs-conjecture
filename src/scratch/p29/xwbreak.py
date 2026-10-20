r"""Search for XWILF failures in the 'all pairs wrap' regime (lead, 2026-10-20): S = <m, m + r_1, ..., m + r_k>
with every r_i > m/2 (so every pair sum wraps to level 3).  Exhaustive over r-sets for m <= M, k <= K.
usage: xwbreak.py mlo mhi kmin kmax"""
import sys, itertools
sys.path.insert(0, ".")
from xdead import analyse
mlo, mhi, kmin, kmax = map(int, sys.argv[1:5]); n = 0; nf = 0; best = None
for m in range(mlo, mhi + 1):
    R = range(m // 2 + 1, m)
    for k in range(kmin, kmax + 1):
        for rs in itertools.combinations(R, k):
            r = analyse([m] + [m + x for x in rs])
            if r is None: continue
            n += 1
            if best is None or r["XWILF"] < best["XWILF"]: best = r
            if r["XWILF"] < 0:
                nf += 1
                if nf <= 5: print("XWILF FAIL", r, flush=True)
print("S", n, "XWILF fails", nf, "min", best)
