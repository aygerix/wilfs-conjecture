# Flip-local minima of E (fixed n): residue-complete down-sets (all d directions) such that NO single flip
# (corner y -> addable z, same residue, all unit vectors kept) gives E' < E.  Any (D,n) descends by E-decreasing
# flips to such a local minimum, so GW <=> GW on local minima.  Question: are local minima always covered by the
# corner-reflection criterion GW-9 (sum_i t_i |L_i| <= d sum_i |L_i|), or at least t(D) <= d?
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
def ev(D, n, m):
    V = {x: sum(a * b for a, b in zip(x, n)) for x in D}; M = max(V.values())
    return d * (M - m + 1) - (d + 1) * sum(v // m for v in V.values()), V, M
def covered(D, V, M, m):
    cor = [y for y in D if all(add(y, u) not in D for u in U)]
    kap = {x: V[x] // m for x in D}; lam = {x: (M - V[x]) // m for x in D}
    lhs = Ls = 0
    for i in range(1, max(kap.values()) + 1):
        Li = sum(1 for x in D if lam[x] >= i); lhs += sum(1 for y in cor if kap[y] >= i) * Li; Ls += Li
    return len(cor), lhs <= d * Ls
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64); ar = np.arange(m)[:, None]
    nloc = nbig = nunc = 0; ex = None; Emin = None
    for D in lev:
        if any(u not in D for u in U): continue
        X = np.array(sorted(D), dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        for s in S[ok]:
            for k in product(range(K + 1), repeat=d):
                n = tuple(int(si + m * ki) for si, ki in zip(s, k))
                e0, V, M = ev(D, n, m); res = {x: V[x] % m for x in D}; local = True
                for y in D:
                    if not any(y) or any(add(y, u) in D for u in U): continue
                    Dm = D - {y}
                    for x in Dm:
                        for u in U:
                            z = add(x, u)
                            if z in Dm or z == y: continue
                            if sum(a * b for a, b in zip(z, n)) % m != res[y]: continue
                            if not all(z[a] == 0 or sub(z, U[a]) in Dm for a in range(d)): continue
                            D2 = Dm | {z}
                            if any(uu not in D2 for uu in U): continue
                            if ev(D2, n, m)[0] < e0: local = False; break
                        if not local: break
                    if not local: break
                if not local: continue
                nloc += 1; t, cov = covered(D, V, M, m)
                Emin = e0 if Emin is None else min(Emin, e0)
                if t > d:
                    nbig += 1
                    if not cov:
                        nunc += 1
                        if ex is None: ex = (n, e0, t, sorted(D))
    print(f"d={d} m={m} K={K} flip-local minima={nloc} (min E {Emin}); with t>d: {nbig}; not covered by GW-9: {nunc}; ex={ex}", flush=True)
