# Downward-routing Hall family: demand(x) = min(i, kappa(x)) may be sent to ANY w < x; capacity of w is
# d*min(i, lam(w)) with lam either global (M - v) or local (height h(w)).  Hall <=> for every down-set Z of D:
#     sum_{x in Z} min(i,kappa)  <=  d * sum_{w in Z \ Max(Z)} min(i, lam(w)).
# Test on residue-complete, multiplicity-form instances, for i = 2, 3 and i = infinity (GW-strength).
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
def subdownsets(D):
    # all down-sets Z of D containing 0 (as index bitmasks), by closure growth
    Ds = sorted(D, key=lambda x: (sum(x), x)); idx = {x: i for i, x in enumerate(Ds)}
    preds = [[idx[sub(x, U[a])] for a in range(d) if x[a] > 0] for x in Ds]
    out = set(); stack = [1]
    while stack:
        z = stack.pop()
        if z in out: continue
        out.add(z)
        for j in range(len(Ds)):
            if not (z >> j) & 1 and all((z >> p) & 1 for p in preds[j]): stack.append(z | (1 << j))
    return Ds, out
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    ks = np.array(list(product(range(1, K + 1), repeat=d)), dtype=np.int64)
    tot = 0; fails = {}; ex = {}
    for D in lev:
        if any(u not in D for u in U): continue
        Ds, Zs = subdownsets(D)
        X = np.array(Ds, dtype=np.int64)
        above = np.all(X[None, :, :] >= X[:, None, :], axis=2)
        # masks: for each Z, membership vector and non-maximal-in-Z vector
        Zl = sorted(Zs); mem = np.array([[(z >> j) & 1 for j in range(m)] for z in Zl], dtype=np.int64)
        nonmax = np.zeros_like(mem)
        for r, z in enumerate(Zl):
            for j in range(m):
                if (z >> j) & 1 and any((z >> k) & 1 and k != j and above[j, k] for k in range(m)): nonmax[r, j] = 1
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            N = s[None, :] + m * ks; V = X @ N.T; Mx = V.max(0)
            kap = V // m; lamg = (Mx[None, :] - V) // m
            H = np.where(above[:, :, None], V[None, :, :], -1).max(1) - V; laml = H // m
            tot += V.shape[1]
            for i in (2, 3, 99):
                for nm, lam in (('glob', lamg), ('loc', laml)):
                    dem = mem @ np.minimum(kap, i); cap = d * (nonmax @ np.minimum(lam, i))
                    bad = (dem > cap).any(0)
                    if bad.any():
                        key = (i, nm); fails[key] = fails.get(key, 0) + int(bad.sum())
                        if key not in ex:
                            j = int(np.argmax(bad)); r = int(np.argmax(dem[:, j] > cap[:, j]))
                            ex[key] = (tuple(int(t) for t in N[j]), Ds, [Ds[q] for q in range(m) if mem[r, q]])
    print(f"d={d} m={m} K={K} inst={tot} routing-Hall fails {dict(sorted(fails.items()))}", flush=True)
    for key in sorted(ex): print("   ex", key, "n=", ex[key][0], "Z=", ex[key][2], flush=True)
