# (1) Lemma Y: for every down-set D (all units) and every A subset [d]:  2|Y(A)| <= |A| (|T2(A)| + 1), where
#     T2(A) = non-maximal w whose upper covers are all maximal and in directions A;
#     Y(A)  = maximal y != 0 all of whose lower covers lie in T2(A).
# (2) P_i WITHOUT residue completeness: n_a in (m, K*m] arbitrary (multiplicity form), M = max v.  Report, per i, how
#     many (D, n) violate P_i.  P_2 should never fail (theorem); P_3+ tells whether residues are needed.
import sys, numpy as np
from itertools import combinations, product
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
    ybad = 0; ptot = 0; pfail = {}; ex = {}
    N = np.array(list(product(range(m + 1, K * m + 1), repeat=d)), dtype=np.int64)   # all weights n_a in (m, Km]
    for D in lev:
        if any(u not in D for u in U): continue
        up = {x: [a for a in range(d) if add(x, U[a]) in D] for x in D}
        mx = {x for x in D if not up[x]}
        for r in range(d + 1):
            for A in combinations(range(d), r):
                As = set(A)
                T2 = {x for x in D if up[x] and all(a in As and add(x, U[a]) in mx for a in up[x])}
                Y = [y for y in mx if any(y) and all(sub(y, U[a]) in T2 for a in range(d) if y[a] > 0)]
                if 2 * len(Y) > len(A) * (len(T2) + 1): ybad += 1
        X = np.array(sorted(D), dtype=np.int64); V = X @ N.T; Mx = V.max(0)
        kap = V // m; lam = (Mx[None, :] - V) // m; top = int(max(kap.max(), lam.max()))
        ptot += V.shape[1]
        for i in range(1, min(top, 6) + 1):
            p = np.minimum(kap, i).sum(0) - d * np.minimum(lam, i).sum(0)
            f = int((p > 0).sum())
            if f:
                pfail[i] = pfail.get(i, 0) + f
                if i not in ex: j = int(np.argmax(p > 0)); ex[i] = (tuple(int(t) for t in N[j]), sorted(D))
    print(f"d={d} m={m} LemmaY-fail={ybad}  P_i-without-residues: inst={ptot} fails-by-i={dict(sorted(pfail.items()))}", flush=True)
    for i in sorted(ex): print("   ex i=%d" % i, ex[i], flush=True)
