# Local prefix test: replace lambda(w) = floor((M - v(w))/m) by the LOCAL height lam_h(w) = floor(h(w)/m),
# h(w) = max{v(u) : w + u in D}.  LP_i: sum min(i, kappa) <= d sum min(i, lam_h).  Residue-complete instances,
# multiplicity form only (all k_a >= 1).  Report failures of LP_i per i, and of P_i (global) as a control.
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
    ks = np.array(list(product(range(1, K + 1), repeat=d)), dtype=np.int64)
    tot = 0; lf = {}; gf = {}; ex = {}
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64); idx = {tuple(x): i for i, x in enumerate(X.tolist())}
        # upward-closure matrix: above[i, j] = 1 if X[j] >= X[i]
        above = np.all(X[None, :, :] >= X[:, None, :], axis=2)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            N = s[None, :] + m * ks; V = X @ N.T                      # (m, nk)
            Mx = V.max(0); kap = V // m; lam = (Mx[None, :] - V) // m
            # h(w) = max_{j above w} V[j] - V[w]
            H = np.where(above[:, :, None], V[None, :, :], -1).max(1) - V
            lamh = H // m
            tot += V.shape[1]
            top = int(max(kap.max(), lam.max()))
            for i in range(1, top + 1):
                pl = np.minimum(kap, i).sum(0) - d * np.minimum(lamh, i).sum(0)
                pg = np.minimum(kap, i).sum(0) - d * np.minimum(lam, i).sum(0)
                if (pl > 0).any():
                    lf[i] = lf.get(i, 0) + int((pl > 0).sum())
                    if i not in ex: j = int(np.argmax(pl > 0)); ex[i] = (tuple(int(t) for t in N[j]), sorted(D))
                if (pg > 0).any(): gf[i] = gf.get(i, 0) + int((pg > 0).sum())
    print(f"d={d} m={m} K={K} inst={tot} LOCAL-fail={dict(sorted(lf.items()))} global-fail={dict(sorted(gf.items()))}", flush=True)
    for i in sorted(ex)[:3]: print("   ex i=%d" % i, ex[i], flush=True)
