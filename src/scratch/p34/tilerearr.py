"""TILE-MAX-REARR (shape only) (lead, 2026-10-21). For every down-set D (|D| = m) that is a tile for SOME b
(a.b mod m injective on D), with weights w(y) = |y| + n over Max(D) sorted decreasingly:
    sum_k w_(k) (m - k) <= (n+1) m (m-1)/2.
Also reports the best constant ratio for TILE-MAX itself, max over b of LHS / ((n+1) m(m-1)/2).
Usage: python tilerearr.py N MMIN MMAX"""
import sys, itertools
sys.path.insert(0, '.')
from subadd_lp import downsets
N, MMIN, MMAX = map(int, sys.argv[1:4])
tot = fail = 0; worstR = 0.0; worstT = 0.0
for m in range(MMIN, MMAX + 1):
    for D in downsets(N, m):
        Ds = set(D)
        mx = [a for a in D if all(tuple(a[s] + (s == t) for s in range(N)) not in Ds for t in range(N))]
        istile = False; bestT = 0.0
        for b in itertools.product(range(m), repeat=N):
            eps = {a: sum(x * y for x, y in zip(a, b)) % m for a in D}
            if len(set(eps.values())) != m: continue
            istile = True
            lhs = sum((sum(y) + N) * eps[y] for y in mx); bestT = max(bestT, lhs / ((N + 1) * m * (m - 1) / 2))
        if not istile: continue
        tot += 1
        w = sorted((sum(y) + N for y in mx), reverse=True)
        lhs = sum(wk * (m - k) for k, wk in enumerate(w, 1)); r = lhs / ((N + 1) * m * (m - 1) / 2)
        worstR = max(worstR, r); worstT = max(worstT, bestT)
        if r > 1 + 1e-12:
            fail += 1
            if fail <= 5: print("REARR FAIL m=%d D=%s max=%s ratio=%.4f (TILE-MAX ratio %.4f)" % (m, D, mx, r, bestT), flush=True)
    print("m=%d: tile shapes %d, REARR failures %d, max REARR ratio %.4f, max TILE-MAX ratio %.4f" % (m, tot, fail, worstR, worstT), flush=True)
