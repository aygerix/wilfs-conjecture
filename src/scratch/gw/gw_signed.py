# GW with SIGNED weights: n = s + m*k, s in [1,m-1]^d, k in [-K,K]^d (entries of n may be negative), all down-sets D.
# E = d*max v - (d+1)*sum floor(v/m) - d*(m-1)   (floor for negatives).  Reports fails split by sign pattern of n.
import sys, numpy as np
from itertools import product
d, m0, m1, K = map(int, sys.argv[1:5])
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
def downsets(M):
    lev = {frozenset([tuple([0] * d)])}
    for m in range(1, M + 1):
        if m >= m0: yield m, lev
        nxt = set()
        for D in lev:
            for x in D:
                for u in U:
                    y = tuple(p + q for p, q in zip(x, u))
                    if y not in D and all(y[a] == 0 or tuple(y[b] - (b == a) for b in range(d)) in D for a in range(d)):
                        nxt.add(D | {y})
        lev = nxt
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    ks = np.array(list(product(range(-K, K + 1), repeat=d)), dtype=np.int64)
    tested = {'pos': 0, 'neg': 0, 'mixed': 0}; fails = {'pos': 0, 'neg': 0, 'mixed': 0}; worst = None
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        if not ok.any(): continue
        N = (S[ok][:, None, :] + m * ks[None, :, :]).reshape(-1, d)
        V = X @ N.T; E = d * V.max(0) - (d + 1) * np.floor_divide(V, m).sum(0) - d * (m - 1)
        pos = (N > 0).all(1); neg = (N < 0).all(1); mix = ~pos & ~neg
        for key, msk in (('pos', pos), ('neg', neg), ('mixed', mix)):
            tested[key] += int(msk.sum()); fails[key] += int((E[msk] < 0).sum())
        j = int(np.argmin(E))
        if worst is None or E[j] < worst[0]: worst = (int(E[j]), tuple(int(t) for t in N[j]), sorted(D))
    print(f"d={d} m={m} K={K} tested={tested} fails={fails} minE={worst[0]} n={worst[1]} D={worst[2][:12]}", flush=True)
