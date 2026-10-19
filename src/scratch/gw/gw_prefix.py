# Nested-neighbourhood Hall test.  If every gap (x,i) may go to ANY element (w,h) with h <= i, Hall with capacity d is
# exactly the prefix family  P_i:  sum_{j<=i} |U_j| <= d * sum_{j<=i} |L_j|   (all i >= 1), i.e.
#   sum_x min(i, kappa(x)) <= d * sum_x min(i, lambda(x)).
# Also the suffix family S_i: sum_{j>=i}|U_j| <= d sum_{j>=i}|L_j| (depth-raising).  i = 1 of either family is GW.
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
    tot = 0; badP = {}; badS = {}; exP = exS = None; gwbad = 0
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            N = s[None, :] + m * ks                   # (nk, d)
            V = X @ N.T                               # (m, nk)
            Mx = V.max(0); kap = V // m; lam = (Mx[None, :] - V) // m
            tot += V.shape[1]
            top = int(max(kap.max(), lam.max()))
            for i in range(1, top + 1):
                p = np.minimum(kap, i).sum(0) - d * np.minimum(lam, i).sum(0)
                q = np.maximum(kap - i + 1, 0).sum(0) - d * np.maximum(lam - i + 1, 0).sum(0)
                if (p > 0).any():
                    badP[i] = badP.get(i, 0) + int((p > 0).sum())
                    if exP is None: j = int(np.argmax(p > 0)); exP = (tuple(N[j]), sorted(D), i)
                if (q > 0).any():
                    badS[i] = badS.get(i, 0) + int((q > 0).sum())
                    if exS is None: j = int(np.argmax(q > 0)); exS = (tuple(N[j]), sorted(D), i)
    print(f"d={d} m={m} K={K} inst={tot} prefix-fail-by-i={dict(sorted(badP.items()))} suffix-fail-by-i={dict(sorted(badS.items()))}", flush=True)
    if exP: print("  exP", exP, flush=True)
    if exS: print("  exS", exS, flush=True)
