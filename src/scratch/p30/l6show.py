"""Tight cases of L6 (incU = #pure carried triples with all pair sums >= h); print triples and unused U2-incidences."""
import sys, itertools, jid
def show(m, B):
    r = jid.info(m, B); h = r["h"]; Bs = sorted(B); k = len(B)
    ps = {}; ts = {}
    for i in range(k):
        for j in range(i, k): ps.setdefault(Bs[i] + Bs[j], []).append((Bs[i], Bs[j]))
    for i in range(k):
        for j in range(i, k):
            for l in range(j, k): ts.setdefault(Bs[i] + Bs[j] + Bs[l], []).append((Bs[i], Bs[j], Bs[l]))
    print(r)
    return r, ps, ts
k, mlo, mhi = map(int, sys.argv[1:4]); shown = 0
for m in range(mlo, mhi + 1):
    for B in itertools.combinations(range(1, m), k):
        r = jid.info(m, B)
        if not r: continue
        pure = r["qres"] - r["qQbig"]
        if pure > 0 and r["incU"] - pure <= 0 and shown < 6:
            shown += 1; print("L6 slack", r["incU"] - pure, r)
