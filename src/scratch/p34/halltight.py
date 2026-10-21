"""Exact HALL-TM ratios on all small tiles at sigma = phi(0) (lead, 2026-10-20): lam*(D,p) = max over Y subset Max of
sum_Y (|y|-1) r(y) / ((N+1) sum_{down(Y) minus Y minus 0} r). Reports max lam*, max MaxCL ratio (Y = Max), and the
instances where the worst Y is a proper subset.  Usage: python halltight.py N MMIN MMAX"""
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from subadd_lp import downsets
N, MMIN, MMAX = map(int, sys.argv[1:4])
for m in range(MMIN, MMAX + 1):
    tot = 0; best = Fr(0); bestA = Fr(0); proper = 0; worst = None; gap = Fr(0); gapinst = None
    for D in downsets(N, m):
        Ds = set(D)
        mx = [a for a in D if all(tuple(a[s] + (s == t) for s in range(N)) not in Ds for t in range(N))]
        mxs = set(mx)
        if all(sum(y) <= 1 for y in mx): continue
        below = {y: {a for a in D if a not in mxs and any(a) and all(a[i] <= y[i] for i in range(N))} for y in mx}
        subs = [Y for k in range(1, len(mx) + 1) for Y in itertools.combinations(mx, k) if any(sum(y) > 1 for y in Y)]
        for b in itertools.product(range(m), repeat=N):
            if b[0] > b[1] and D == sorted(D): pass
            e = {a: sum(x * y for x, y in zip(a, b)) % m for a in D}
            if len(set(e.values())) != m: continue
            tot += 1; lm = Fr(-1); lY = None
            for Y in subs:
                dem = sum((sum(y) - 1) * e[y] for y in Y)
                cap = (N + 1) * sum(e[a] for a in set().union(*(below[y] for y in Y)))
                v = Fr(dem, cap) if cap else (Fr(10**6) if dem else Fr(0))
                if v > lm: lm, lY = v, Y
            vA = [v for v in [None]]
            dA = sum((sum(y) - 1) * e[y] for y in mx); cA = (N + 1) * sum(e[a] for a in D if a not in mxs)
            rA = Fr(dA, cA) if cA else Fr(0)
            if lm > best: best, worst = lm, (D, b, lY, mx)
            if rA > bestA: bestA = rA
            if lm > rA:
                proper += 1
                if lm - rA > gap: gap, gapinst = lm - rA, (D, b, lY, float(lm), float(rA))
    print("N=%d m=%d instances %d  max lam* %s (%.4f)  max MaxCL-ratio %.4f  proper-worst %d  max gap %.4f" % (N, m, tot, best, float(best), float(bestA), proper, float(gap)), flush=True)
    if worst: print("   worst:", worst[0], "p=", worst[1], "Y=", worst[2])
    if gapinst: print("   gap inst:", gapinst)
