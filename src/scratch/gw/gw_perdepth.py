# Per-depth GW (PD):  for every i >= 1,  |U_i| <= d |L_i|,  U_i = {kappa >= i}, L_i = {lambda >= i}.
# Summing over i gives GW (g = sum |U_i|, l = sum |L_i|).  Test on every residue-complete down-set.
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
    tot = fails = 0; ex = None; bydepth = {}
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        if not ok.any(): continue
        N = (S[ok][:, None, :] + m * ks[None, :, :]).reshape(-1, d)
        V = X @ N.T; M = V.max(0); kap = V // m; lam = (M[None, :] - V) // m
        bad = np.zeros(V.shape[1], dtype=bool)
        for i in range(1, int(kap.max()) + 1):
            b = (kap >= i).sum(0) > d * (lam >= i).sum(0); bad |= b
            if b.any():
                bydepth.setdefault('i=K' , 0)
                Kc = M // m
                bydepth['i=K'] += int((b & (Kc == i)).sum()); bydepth.setdefault('i<K', 0); bydepth['i<K'] += int((b & (Kc != i)).sum())
        tot += V.shape[1]; fails += int(bad.sum())
        if bad.any() and ex is None:
            j = int(np.argmax(bad)); ex = (tuple(int(t) for t in N[j]), sorted(D))
    print(f"d={d} m={m} K={K} instances={tot} PD fails={fails} by depth={bydepth} ex={ex}", flush=True)
