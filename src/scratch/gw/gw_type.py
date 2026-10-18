# Check of the corner-reflection theorem  g(Delta) <= t(D) * l(Delta)  on every residue-complete down-set
# (all d directions) and every n = s + m k, k in [0,K]^d.  Also reports how often t(D) > d (GW not covered).
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
    tested = viol = over = 0; tmax = 0
    for D in lev:
        if any(u not in D for u in U): continue
        t = sum(all(add(y, u) not in D for u in U) for y in D)
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        if not ok.any(): continue
        tmax = max(tmax, t)
        N = (S[ok][:, None, :] + m * ks[None, :, :]).reshape(-1, d)
        V = X @ N.T; M = V.max(0)
        g = (V // m).sum(0); l = ((M[None, :] - V) // m).sum(0)
        assert np.all(g + l == M - m + 1)
        tested += len(g); viol += int((g > t * l).sum()); over += len(g) * (t > d)
    print(f"d={d} m={m} K={K} instances={tested} g>t*l violations={viol} instances with t>d={over} max t={tmax}", flush=True)
