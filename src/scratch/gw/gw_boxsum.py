# Sharper reflection criterion:  g <= sum_{corners y} l_y,  l_y = sum_{x <= y} kappa(x)  (exact image size of y's
# reflection).  BOX-SUM conjecture  BS:  sum_y l_y <= d * l.   BS => GW.  Test on every instance; split by t > d.
import sys, numpy as np
from itertools import product
d, m0, m1, K = map(int, sys.argv[1:5])
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
    ks = np.array(list(product(range(K + 1), repeat=d)), dtype=np.int64)
    tot = big = fail_all = fail_big = 0; worst = None
    for D in lev:
        if any(u not in D for u in U): continue
        Ds = sorted(D); X = np.array(Ds, dtype=np.int64)
        cor = [i for i, y in enumerate(Ds) if all(add(y, u) not in D for u in U)]
        below = np.array([[all(p <= q for p, q in zip(x, Ds[j])) for x in Ds] for j in cor])   # t x m
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        if not ok.any(): continue
        N = (S[ok][:, None, :] + m * ks[None, :, :]).reshape(-1, d)
        V = X @ N.T; M = V.max(0); kap = V // m; lam = (M[None, :] - V) // m
        lsum = (below.astype(np.int64) @ kap).sum(0); l = lam.sum(0)
        bad = lsum > d * l; tot += len(l); fail_all += int(bad.sum())
        if len(cor) > d: big += len(l); fail_big += int(bad.sum())
        if bad.any():
            j = int(np.argmax(lsum - d * l))
            r = (int(lsum[j] - d * l[j]), tuple(int(t) for t in N[j]), len(cor), Ds)
            if worst is None or r[0] > worst[0]: worst = r
    print(f"d={d} m={m} K={K} instances={tot} BS fails={fail_all}; with t>d: {big}, BS fails among them={fail_big}; worst={worst}", flush=True)
