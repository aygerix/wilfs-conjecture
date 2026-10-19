# kappa-restricted downward matching: gap (x,j), 1<=j<=kappa(x)  ->  element (x-u, h) with u <= x, u != 0,
# kappa(u) >= h, h <= j.  Element units (w,h) exist iff some such pair; capacity d.  b* = least capacity.
import sys, numpy as np
from itertools import product
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
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
def bstar(Ds, idx, kap):
    m = len(Ds)
    gaps = [(x, j) for x in range(m) for j in range(1, kap[x] + 1)]
    if not gaps: return 0
    el = {}; rows = []; cols = []
    for gi, (x, j) in enumerate(gaps):
        X = Ds[x]
        for u in Ds:
            if any(u) and all(p <= q for p, q in zip(u, X)):
                w = idx[sub(X, u)]
                for h in range(1, min(j, kap[idx[u]]) + 1):
                    if (w, h) not in el: el[(w, h)] = len(el)
                    rows.append(gi); cols.append(el[(w, h)])
    G, E = len(gaps), len(el)
    def flow(b):
        r = [0] * G + [1 + g for g in rows] + [1 + G + e for e in range(E)]
        c = [1 + g for g in range(G)] + [1 + G + e for e in cols] + [1 + G + E] * E
        cap = [1] * G + [1] * len(rows) + [b] * E
        A = csr_matrix((np.array(cap, dtype=np.int32), (r, c)), shape=(G + E + 2, G + E + 2))
        return maximum_flow(A, 0, G + E + 1).flow_value
    if flow(G) < G: return 10**6
    lo, hi = 1, G
    while lo < hi:
        mid = (lo + hi) // 2
        if flow(mid) == G: hi = mid
        else: lo = mid + 1
    return lo
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    tot = bad = 0; worst = 0; ex = None
    for D in lev:
        if any(u not in D for u in U): continue
        Ds = sorted(D); X = np.array(Ds, dtype=np.int64); idx = {x: i for i, x in enumerate(Ds)}
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            for k in product(range(1, K + 1), repeat=d):
                n = s + m * np.array(k); V = X @ n; kap = (V // m).tolist()
                b = bstar(Ds, idx, kap); tot += 1; worst = max(worst, b)
                if b > d:
                    bad += 1
                    if ex is None: ex = (tuple(int(t) for t in n), Ds, b)
    print(f"d={d} m={m} K={K} kappa-DMC inst={tot} b*>d: {bad} max b*={worst} ex={ex}", flush=True)
