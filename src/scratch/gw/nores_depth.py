# P_i WITHOUT residue completeness, multiplicity form n_a in (m, Kmax*m]; failures classified by K - i
# (K = floor(M/m); i >= K+1 is GW itself since every kappa, lambda <= K).
import sys, numpy as np
from itertools import product
d, m0, m1, Kmax = map(int, sys.argv[1:5]); step = int(sys.argv[5]) if len(sys.argv) > 5 else 1
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
    N = np.array(list(product(range(m + 1, Kmax * m + 1, step), repeat=d)), dtype=np.int64)
    tot = 0; byKi = {}; ex = {}
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64); V = X @ N.T; Mx = V.max(0); Kk = Mx // m
        kap = V // m; lam = (Mx[None, :] - V) // m
        tot += V.shape[1]
        for i in range(1, int(Kk.max()) + 1):
            p = np.minimum(kap, i).sum(0) - d * np.minimum(lam, i).sum(0)
            bad = p > 0
            if bad.any():
                for gap in np.unique(Kk[bad] - i):
                    key = int(gap); c = int((bad & (Kk - i == gap)).sum()); byKi[key] = byKi.get(key, 0) + c
                    if key not in ex:
                        j = int(np.argmax(bad & (Kk - i == gap))); ex[key] = (i, int(Kk[j]), tuple(int(t) for t in N[j]), sorted(D))
    print(f"d={d} m={m} inst={tot} no-residue P_i failures by K-i: {dict(sorted(byKi.items()))}", flush=True)
    for key in sorted(ex): print("   K-i=%d ex (i,K,n,D) =" % key, ex[key], flush=True)
