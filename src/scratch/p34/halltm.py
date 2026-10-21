"""HALL-TM (lead, 2026-10-20): box transport for TM on all down-set tiles. Each maximal y demands (|y|-1) eps(y)
units of "pair credit"; a point b in B(y) minus {0, y} offers capacity (n+1) eps(b) shared by all y >= b; the transport
is valid when lambda = 0 (pairs sum >= eps(y)); checked by max-flow. Usage: python halltm.py N MMIN MMAX"""
import sys, itertools
sys.path.insert(0, '.')
from subadd_lp import downsets
from halltop import maxflow
N, MMIN, MMAX = map(int, sys.argv[1:4]); tot = fail = 0
for m in range(MMIN, MMAX + 1):
    for D in downsets(N, m):
        Ds = set(D)
        mx = [a for a in D if all(tuple(a[s] + (s == t) for s in range(N)) not in Ds for t in range(N))]
        mxs = set(mx); low = [a for a in D if a not in mxs and any(a)]
        idx = {a: i for i, a in enumerate(low)}
        below = {y: [a for a in low if all(a[i] <= y[i] for i in range(N))] for y in mx}
        for b in itertools.product(range(m), repeat=N):
            e = {a: sum(x * y for x, y in zip(a, b)) % m for a in D}
            if len(set(e.values())) != m: continue
            tot += 1
            s, t = 0, 1; yi = {y: 2 + len(low) + j for j, y in enumerate(mx)}
            edges = [(s, yi[y], (sum(y) - 1) * e[y]) for y in mx if sum(y) > 1]
            edges += [(2 + idx[a], t, (N + 1) * e[a]) for a in low]
            for y in mx:
                for a in below[y]: edges.append((yi[y], 2 + idx[a], 1 << 40))
            dem = sum(c for _, _, c in edges[:len([y for y in mx if sum(y) > 1])])
            f = maxflow(2 + len(low) + len(mx), edges, s, t)
            if f < dem:
                fail += 1
                if fail <= 4: print("HALL-TM FAIL m=%d D=%s b=%s shortfall=%d" % (m, D, b, dem - f), flush=True)
    print("m=%d tested %d failures %d" % (m, tot, fail), flush=True)
