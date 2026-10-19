# Increments Delta_i = A_i - d*B_i (A_i=#{kappa>=i}, B_i=#{lambda>=i}).  Single crossing (- ... - + ... +) would make the
# prefix family a consequence of GW.  Count instances with a '+' followed later by a '-' (strictly), and report one.
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
    tot = multi = 0; ex = None
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            N = s[None, :] + m * ks; V = X @ N.T
            Mx = V.max(0); kap = V // m; lam = (Mx[None, :] - V) // m
            top = int(max(kap.max(), lam.max()))
            inc = np.array([(kap >= i).sum(0) - d * (lam >= i).sum(0) for i in range(1, top + 1)])  # (top, nk)
            tot += inc.shape[1]
            pos = inc > 0; neg = inc < 0
            # exists i<j with pos[i] and neg[j]
            seenpos = np.maximum.accumulate(pos, axis=0)
            bad = (seenpos[:-1] & neg[1:]).any(0) if top > 1 else np.zeros(inc.shape[1], bool)
            multi += int(bad.sum())
            if ex is None and bad.any():
                j = int(np.argmax(bad)); ex = (tuple(N[j]), sorted(D), inc[:, j].tolist())
    print(f"d={d} m={m} K={K} inst={tot} non-single-crossing={multi} ex={ex}", flush=True)
