# Lift monotonicity: for every GW instance (D, n) with some n_a > m, is there a with n_a > m and
# E(D, n - m e_a) <= E(D, n)?  If always yes, GW reduces to the residue form RW (all n_a < m).
# Also tests the stronger "E(D, n - m e_a) <= E(D, n) for the a maximising x*_a" and the variant over all D.
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
    ks = np.array([k for k in product(range(K + 1), repeat=d) if any(k)], dtype=np.int64)
    tested = stuck = 0; ex = None
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        if not ok.any(): continue
        Sg = S[ok]
        def Ev(N):
            V = X @ N.T; return d * V.max(0) - (d + 1) * (V // m).sum(0) - d * (m - 1)
        for k in ks:
            N = Sg + m * k; E0 = Ev(N); good = np.zeros(len(N), dtype=bool)
            for a in range(d):
                if k[a] == 0: continue
                N2 = N.copy(); N2[:, a] -= m; good |= Ev(N2) <= E0
            tested += len(N); bad = np.nonzero(~good)[0]; stuck += len(bad)
            if len(bad) and ex is None: ex = (tuple(int(t) for t in N[bad[0]]), int(E0[bad[0]]), sorted(D))
    print(f"d={d} m={m} K={K} lifted instances={tested} no E-nonincreasing lift-down={stuck} example={ex}", flush=True)
