# Sufficient condition (*) for local P_3 (multiplicity form):
#   3|Y'| <= d|T| + 2d|T3| + 2|A1| + |A2| + |Q0|
# T  = non-max w with m <= h(w) < 2m,  T3 = w with 2m <= h(w) < 3m  (h = max upward value),
# Y' = nonzero x all of whose lower covers lie in T u T3,  A_j = {a : k_a = j},  Q0 = {e_a+e_b in D : kappa = 2}.
# mode 'res': residue-complete n = s + m k (k >= 1);  mode 'nores': all n_a in (m, Kmax m].
import sys, numpy as np
from itertools import product
d, m0, m1, Kmax = map(int, sys.argv[1:5]); mode = sys.argv[5]
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
    if mode == 'res':
        S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
        ks = np.array(list(product(range(1, Kmax + 1), repeat=d)), dtype=np.int64)
    else:
        Nall = np.array(list(product(range(m + 1, Kmax * m + 1), repeat=d)), dtype=np.int64)
    tot = bad = lp3bad = 0; worst = None
    for D in lev:
        if any(u not in D for u in U): continue
        Ds = sorted(D); X = np.array(Ds, dtype=np.int64); idx = {x: i for i, x in enumerate(Ds)}
        above = np.all(X[None, :, :] >= X[:, None, :], axis=2)
        lowc = [[idx[sub(x, U[a])] for a in range(d) if x[a] > 0] for x in Ds]
        upc = [[idx[add(x, U[a])] for a in range(d) if add(x, U[a]) in D] for x in Ds]
        unit = [idx[u] for u in U]
        pairs = [i for i, x in enumerate(Ds) if sum(x) == 2]
        if mode == 'res':
            ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
            Ns = (s[None, :] + m * ks for s in S[ok])
        else:
            Ns = [Nall]
        for N in Ns:
            V = X @ N.T; H = np.where(above[:, :, None], V[None, :, :], -1).max(1) - V   # (m, nk)
            kap = V // m; nonmax = np.array([len(u) > 0 for u in upc])
            T = nonmax[:, None] & (H >= m) & (H < 2 * m); T3 = (H >= 2 * m) & (H < 3 * m)
            TT = T | T3
            Yp = np.zeros_like(T)
            for i in range(len(Ds)):
                if lowc[i]: Yp[i] = np.all(TT[lowc[i]], axis=0)
            k = N // m
            A1 = (k == 1).sum(1); A2 = (k == 2).sum(1)
            Q0 = (kap[pairs] == 2).sum(0) if pairs else 0
            lhs = 3 * Yp.sum(0); rhs = d * T.sum(0) + 2 * d * T3.sum(0) + 2 * A1 + A2 + Q0
            # local P_3 itself as a control
            lam = H // m
            lp3 = np.minimum(kap, 3).sum(0) - d * np.minimum(lam, 3).sum(0)
            tot += V.shape[1]; b = lhs > rhs; bad += int(b.sum()); lp3bad += int((lp3 > 0).sum())
            if b.any():
                j = int(np.argmax(lhs - rhs)); exc = int((lhs - rhs)[j])
                if worst is None or exc > worst[0]: worst = (exc, tuple(int(t) for t in N[j]), Ds)
    print(f"d={d} m={m} {mode} inst={tot} (*)-fail={bad} localP3-fail={lp3bad} worst={worst}", flush=True)
