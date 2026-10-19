# Column-reflection criterion CRC: kappa(x) <= sum_a lambda(R_a x) for every cell x (R_a = reflection inside the
# a-column of x).  CRC at every cell => GW and every P_i.  Report: instances where CRC holds everywhere; failing cells
# (count, worst deficit, type of failing cell: corner / non-corner); global variant using local heights.
import sys, numpy as np
from itertools import product
d, m0, m1, K = map(int, sys.argv[1:5]); kmin = int(sys.argv[5]) if len(sys.argv) > 5 else 1
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
    ks = np.array(list(product(range(kmin, K + 1), repeat=d)), dtype=np.int64)
    tot = good = 0; failcells = 0; worst = 0; ftypes = {'corner': 0, 'inner': 0}; ex = None
    for D in lev:
        if any(u not in D for u in U): continue
        Ds = sorted(D); X = np.array(Ds, dtype=np.int64); idx = {x: i for i, x in enumerate(Ds)}
        R = np.zeros((d, len(Ds)), dtype=np.int64)
        for i, x in enumerate(Ds):
            for a in range(d):
                t = x
                while add(t, U[a]) in D: t = add(t, U[a])
                h = t[a] + 1
                y = tuple(h - 1 - x[b] if b == a else x[b] for b in range(d)); R[a, i] = idx[y]
        corner = np.array([all(add(x, u) not in D for u in U) for x in Ds])
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            N = s[None, :] + m * ks; V = X @ N.T; Mx = V.max(0)
            kap = V // m; lam = (Mx[None, :] - V) // m
            rhs = sum(lam[R[a]] for a in range(d))                      # (m, nk)
            deficit = kap - rhs
            tot += V.shape[1]
            allok = (deficit <= 0).all(0); good += int(allok.sum())
            bad = deficit > 0
            failcells += int(bad.sum()); worst = max(worst, int(deficit.max()))
            ftypes['corner'] += int((bad & corner[:, None]).sum()); ftypes['inner'] += int((bad & ~corner[:, None]).sum())
            if ex is None and (~allok).any():
                j = int(np.argmax(~allok)); ex = (tuple(int(t) for t in N[j]), Ds, [Ds[i] for i in range(len(Ds)) if bad[i, j]])
    print(f"d={d} m={m} K={K} inst={tot} CRC-everywhere={good} ({100*good/max(tot,1):.1f}%) failing cells={failcells} {ftypes} worst deficit={worst} ex={ex}", flush=True)
