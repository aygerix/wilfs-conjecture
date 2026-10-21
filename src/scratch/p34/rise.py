"""RISE test on all down-set tiles (lead, 2026-10-20):
   sum_{y in Max} sum_i sum_{t=1}^{y_i} [eps(y) - eps(y - t e_i)] <= C(m,2)       (sufficient for TILE-MAX-AFF)
eps = (a.b + shift) mod m.  Usage: python rise.py N MMIN MMAX"""
import sys, itertools
sys.path.insert(0, '.')
from subadd_lp import downsets
N, MMIN, MMAX = map(int, sys.argv[1:4]); tot = fail = 0; worst = None
for m in range(MMIN, MMAX + 1):
    for D in downsets(N, m):
        Ds = set(D)
        mx = [a for a in D if all(tuple(a[s] + (s == t) for s in range(N)) not in Ds for t in range(N))]
        fib = [(y, [tuple(y[s] - t * (s == i) for s in range(N)) for i in range(N) for t in range(1, y[i] + 1)]) for y in mx]
        for b in itertools.product(range(m), repeat=N):
            e0 = {a: sum(x * y for x, y in zip(a, b)) % m for a in D}
            if len(set(e0.values())) != m: continue
            for sh in range(m):
                E = lambda a: (e0[a] + sh) % m
                v = sum(len(lst) * E(y) - sum(E(a) for a in lst) for y, lst in fib)
                sl = m * (m - 1) // 2 - v; tot += 1
                if worst is None or sl < worst[0]: worst = (sl, m, D, b, sh)
                if sl < 0:
                    fail += 1
                    if fail <= 4: print("RISE FAIL m=%d D=%s b=%s sh=%d slack=%d" % (m, D, b, sh, sl), flush=True)
    print("m=%d tested %d failures %d worst %s" % (m, tot, fail, worst[0] if worst else None), flush=True)
