# GW test: ALL down-sets D of N^d, |D| = m, using all d directions; ALL n = s + m*k, s in [1,m-1]^d, k in [0,K]^d,
# with x.n mod m bijective on D.  E(D,n) = d*max v - (d+1)*sum floor(v/m) - d*(m-1), v = x.n.  GW <=> E >= 0.
# minimal <=> v(D) = Ap(<m,n>, m).  Prints per m: tested/fails/equalities split by minimality, and min E on non-minimal.
import sys, heapq, numpy as np
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
def apsum(m, n):
    w = [None] * m; w[0] = 0; h = [(0, 0)]
    while h:
        c, r = heapq.heappop(h)
        if c > w[r]: continue
        for g in n:
            r2 = (r + g) % m
            if w[r2] is None or c + g < w[r2]: w[r2] = c + g; heapq.heappush(h, (c + g, r2))
    return sum(w)
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    ks = np.array(list(product(range(K + 1), repeat=d)), dtype=np.int64)
    st = {'min': [0, 0, 0], 'non': [0, 0, 0]}; minnon = None; fails = []; cache = {}
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        if not ok.any(): continue
        N = (S[ok][:, None, :] + m * ks[None, :, :]).reshape(-1, d)
        V = X @ N.T
        E = d * V.max(0) - (d + 1) * (V // m).sum(0) - d * (m - 1)
        Vs = V.sum(0)
        for idx in range(len(E)):
            n = tuple(int(t) for t in N[idx])
            if n not in cache: cache[n] = apsum(m, n)
            mn = int(Vs[idx]) == cache[n]; b = st['min' if mn else 'non']
            b[0] += 1; b[1] += E[idx] < 0; b[2] += E[idx] == 0
            if E[idx] < 0: fails.append((int(E[idx]), n, sorted(D)))
            if not mn and (minnon is None or E[idx] < minnon[0]): minnon = (int(E[idx]), n, sorted(D))
    print(f"d={d} m={m} K={K} downsets={len(lev)} minimal[tested,fails,eq]={st['min']} nonminimal={st['non']} "
          f"minE_nonmin={minnon[0] if minnon else None} at n={minnon[1] if minnon else None} D={minnon[2] if minnon else None}", flush=True)
    for f in fails[:5]: print('   FAIL', f, flush=True)
