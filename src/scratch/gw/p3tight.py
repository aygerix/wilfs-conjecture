# P_3 slack on residue-complete multiplicity-form instances (all k_a >= 1), split by whether P_3 = GW (top <= 3).
# Lists the tight instances (slack 0) with top >= 4 and t > d, and the minimum slack per (m, t>d) class.
import sys, numpy as np
from itertools import product
from collections import Counter
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
    hist = Counter(); shown = 0
    for D in lev:
        if any(u not in D for u in U): continue
        t = sum(1 for x in D if all(add(x, u) not in D for u in U))
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            N = s[None, :] + m * ks; V = X @ N.T; Mx = V.max(0)
            kap = V // m; lam = (Mx[None, :] - V) // m
            sl3 = d * np.minimum(lam, 3).sum(0) - np.minimum(kap, 3).sum(0)
            sl2 = d * np.minimum(lam, 2).sum(0) - np.minimum(kap, 2).sum(0)
            topk = np.maximum(kap.max(0), lam.max(0))
            for j in range(V.shape[1]):
                key = ('P3=GW' if topk[j] <= 3 else 'P3<GW', t > d)
                hist[(key, int(sl3[j]))] += 1
                if sl3[j] == 0 and topk[j] >= 4 and t > d and shown < 4:
                    shown += 1
                    print(f"  TIGHT m={m} n={tuple(int(a) for a in N[j])} D={sorted(D)} kappa={kap[:, j].tolist()} lam={lam[:, j].tolist()} sl2={int(sl2[j])}", flush=True)
    mins = {}
    for (key, sl), c in hist.items():
        mins[key] = min(mins.get(key, 10**9), sl)
    print(f"d={d} m={m} min P_3 slack by (class, t>d): {dict(sorted(mins.items()))}", flush=True)
