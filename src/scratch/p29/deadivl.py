r"""DEAD on shifted-interval families S = <m, a, a+1, ..., a+d> (lead, 2026-10-20).  Reports max (Lam-O)/W and failures.
usage: deadivl.py mlo mhi"""
import sys
from dead import info
mlo, mhi = map(int, sys.argv[1:3]); worst = None; nf = 0; n = 0
for m in range(mlo, mhi + 1):
    for a in range(m + 1, 3 * m):
        for d in range(1, m):
            r = info([m] + list(range(a, a + d + 1)))
            if r is None or r["W"] <= 0: continue
            n += 1; rat = (r["Lam"] - r["O"]) / r["W"]
            if r["D"] < 0:
                nf += 1
                if nf <= 5: print("FAIL", r)
            if worst is None or rat > worst[0]: worst = (rat, r)
print("S", n, "fails", nf, "max ratio", worst[0], worst[1])
