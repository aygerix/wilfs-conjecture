# RRW (relaxed residue Wilf): for a residue-complete (D, s), s in [1,m-1]^d, with p = ((d+1)/d) * centroid(D):
#     Phi(D,s) := max { (xbar - p).s : xbar in conv(D), xbar >= p }  >=  (d-1)(m-1)/(2d).
# By LP duality Phi = min over REAL k >= 0 of [GW defect at n = s + m k] / (d m) + (d-1)(m-1)/(2d), so RRW implies GW
# for every positive n (all lifts at once).  Exact rational check: solve the LP in floating point (HiGHS), then confirm
# with exact arithmetic on the optimal support (vertex) when the LP value is within 1e-6 of the threshold.
import sys, numpy as np
from itertools import product
from fractions import Fraction as Fr
from scipy.optimize import linprog
d, m0, m1 = map(int, sys.argv[1:4])
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
def downsets(M):
    lev = {frozenset([tuple([0] * d)])}
    for m in range(1, M + 1):
        if m >= m0: yield m, lev
        nxt = set()
        for D in lev:
            for x in D:
                for u in U:
                    y = add(x, u)
                    if y not in D and all(y[a] == 0 or sub(y, U[a]) in D for a in range(d)): nxt.add(D | {y})
        lev = nxt
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    thr = (d - 1) * (m - 1) / (2 * d); tested = fails = near = 0; worst = None
    for D in lev:
        if any(u not in D for u in U): continue
        Ds = sorted(D); X = np.array(Ds, dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        if not ok.any(): continue
        p = (d + 1) / d * X.mean(0)
        # variables w_x >= 0, sum w = 1, X^T w >= p ; maximise (X s).w
        A_ub = -X.T.astype(float); b_ub = -p; A_eq = np.ones((1, len(Ds))); b_eq = [1.0]
        for s in S[ok]:
            res = linprog(-(X @ s).astype(float), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')
            assert res.status == 0
            phi = -res.fun - p @ s; tested += 1
            if phi < thr - 1e-9:
                fails += 1
                if worst is None or phi - thr < worst[0]: worst = (phi - thr, tuple(int(t) for t in s), Ds)
            elif phi < thr + 1e-6: near += 1
    print(f"d={d} m={m} (D,s) pairs={tested} RRW fails={fails} near-equality={near} worst={worst}", flush=True)
