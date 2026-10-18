# For each weight n: is min over ALL residue-bijective down-sets D of E(D,n) attained by the Apery tile?
# E(D,n) = d*max v - (d+1)*sum floor(v/m) - d*(m-1).  E(Apery) = Wilf-type defect of <m,n> (with d directions).
# Reports the n where some non-minimal D has E(D,n) < E(Apery,n)  ("GW strictly stronger than Wilf for this n").
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
def apery(m, n):
    w = [None] * m; w[0] = 0; h = [(0, 0)]
    while h:
        c, r = heapq.heappop(h)
        if c > w[r]: continue
        for g in n:
            r2 = (r + g) % m
            if w[r2] is None or c + g < w[r2]: w[r2] = c + g; heapq.heappush(h, (c + g, r2))
    return w
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    ks = np.array(list(product(range(K + 1), repeat=d)), dtype=np.int64)
    best = {}                                   # n -> min E over non-minimal D
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        if not ok.any(): continue
        N = (S[ok][:, None, :] + m * ks[None, :, :]).reshape(-1, d)
        V = X @ N.T; E = d * V.max(0) - (d + 1) * (V // m).sum(0) - d * (m - 1); Vs = V.sum(0)
        for idx in range(len(E)):
            n = tuple(int(t) for t in N[idx])
            if n not in best: best[n] = [None, None, None]
            b = best[n]
            if b[0] is None: w = apery(m, n); b[0] = sum(w); M = max(w); b[1] = d * M - (d + 1) * sum(x // m for x in w) - d * (m - 1)
            if Vs[idx] != b[0] and (b[2] is None or E[idx] < b[2][0]): b[2] = (int(E[idx]), sorted(D))
    # only n whose Apery tile is itself a d-dim down-set using all directions is comparable; E(Apery) is computed regardless
    def embdim_full(n):            # every n_a is a minimal generator of <m, n> (so the Apery tile is genuinely d-dim)
        for a in range(d):
            w = apery(m, tuple(n[b] for b in range(d) if b != a))
            if w[n[a] % m] is not None and w[n[a] % m] <= n[a]: return False
        return True
    if len(sys.argv) > 5: best = {n: b for n, b in best.items() if embdim_full(n)}
    strict = [(n, b[1], b[2]) for n, b in best.items() if b[2] is not None and b[2][0] < b[1]]
    gaps = [b[2][0] - b[1] for b in best.values() if b[2] is not None]
    print(f"d={d} m={m} K={K} weights={len(best)} with_nonmin={len(gaps)} nonmin_beats_apery={len(strict)} "
          f"min(E_nonmin - E_apery)={min(gaps) if gaps else None}", flush=True)
    for s in sorted(strict, key=lambda t: t[2][0] - t[1])[:3]: print('   ', 'n=', s[0], 'E_apery=', s[1], 'E_nonmin=', s[2][0], 'D=', s[2][1], flush=True)
