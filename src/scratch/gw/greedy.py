# Greedy downward matchings, capacity d per element unit (w,h), h <= lam_loc(w).
# Cells processed by decreasing v; gaps of x by decreasing depth j.  Gap (x,j) may take (w,h) with w < x, h <= j.
# Rules: 'near'  - w with largest v(w) first, then largest h;
#        'same'  - prefer h = j (same depth), then largest v(w);
#        'far'   - w with smallest v(w) first, then largest h;
#        'deep'  - largest h first, then largest v(w).
import sys, numpy as np
from itertools import product
d, m0, m1, K = map(int, sys.argv[1:5]); rules = sys.argv[5].split(',')
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
def greedy(Ds, V, kap, lam, below, rule):
    m = len(Ds); cap = {}
    for w in range(m):
        for h in range(1, lam[w] + 1): cap[(w, h)] = d
    order = sorted(range(m), key=lambda x: -V[x])
    for x in order:
        for j in range(kap[x], 0, -1):
            cands = [(w, h) for w in below[x] for h in range(1, min(j, lam[w]) + 1) if cap[(w, h)] > 0]
            if not cands: return False
            if rule == 'near': key = lambda e: (-V[e[0]], -e[1])
            elif rule == 'same': key = lambda e: (e[1] != j, -V[e[0]], -e[1])
            elif rule == 'far': key = lambda e: (V[e[0]], -e[1])
            else: key = lambda e: (-e[1], -V[e[0]])
            e = min(cands, key=key); cap[e] -= 1
    return True
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    tot = 0; fails = {r: 0 for r in rules}
    for D in lev:
        if any(u not in D for u in U): continue
        Ds = sorted(D); X = np.array(Ds, dtype=np.int64)
        below = [[w for w in range(m) if w != x and all(p <= q for p, q in zip(Ds[w], Ds[x]))] for x in range(m)]
        above = np.all(X[None, :, :] >= X[:, None, :], axis=2)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            for k in product(range(1, K + 1), repeat=d):
                n = s + m * np.array(k); V = (X @ n).tolist(); Va = np.array(V)
                kap = [v // m for v in V]
                lam = ((np.where(above, Va[None, :], -1).max(1) - Va) // m).tolist()
                tot += 1
                for r in rules:
                    if not greedy(Ds, V, kap, lam, below, r): fails[r] += 1
    print(f"d={d} m={m} K={K} inst={tot} greedy fails {fails}", flush=True)
