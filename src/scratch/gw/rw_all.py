# Exhaustive test over ALL down-sets D of N^d with |D| = m (not only Groebner tiles) and ALL s in [1,m-1]^d with
# x.s mod m bijective on D.  Tests the residue form RW (n = s) and the multiplicity form (n = s + m*k, k in {0,1,2}^d,
# k != 0).  Wilf form for weights n:  E(D,n) = d*max v - (d+1)*sum floor(v/m) - d*(m-1) >= 0,  v = x.n.
# stats: [tested, fails, equalities] per (form, minimal?).  "minimal" = v(D) is the Apery set Ap(<m,n>, m) (D is a factorization tile of a real semigroup).
import sys, numpy as np
from itertools import product
d, m0, m1 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
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
                    if y in D: continue
                    if all(y[a] == 0 or tuple(y[b] - (b == a) for b in range(d)) in D for a in range(d)):
                        nxt.add(D | {y})
        lev = nxt
def apery(m, n):
    INF = 10 ** 9; w = [INF] * m; w[0] = 0
    import heapq; h = [(0, 0)]
    while h:
        c, r = heapq.heappop(h)
        if c > w[r]: continue
        for g in n:
            r2 = (r + g) % m
            if c + g < w[r2]: w[r2] = c + g; heapq.heappush(h, (c + g, r2))
    return w
for m, lev in downsets(m1):
    S = np.array(list(product(range(1, m), repeat=d)), dtype=np.int64)
    ar = np.arange(m)[:, None]
    stats = {}
    worst = {}
    for D in lev:
        if any(u not in D for u in U): continue        # all d directions used
        X = np.array(sorted(D), dtype=np.int64)
        R = (X @ S.T) % m
        ok = np.all(np.sort(R, axis=0) == ar, axis=0)
        if not ok.any(): continue
        Sg = S[ok]
        for k in product(range(3), repeat=d):
            N = Sg + m * np.array(k)
            V = X @ N.T
            E = d * V.max(0) - (d + 1) * (V // m).sum(0) - d * (m - 1)
            key = 'RW' if not any(k) else ('mult_all' if min(k) > 0 else 'mixed')
            for idx in range(len(E)):
                n = tuple(int(t) for t in N[idx])
                w = apery(m, n); minimal = int(V[:, idx].sum()) == sum(w)
                st = stats.setdefault((key, 'min' if minimal else 'NONmin'), [0, 0, 0]); st[0] += 1
                if E[idx] == 0: st[2] += 1
                if E[idx] < 0:
                    st[1] += 1
                    if (key, minimal) not in worst or E[idx] < worst[(key, minimal)][0]:
                        worst[(key, minimal)] = (int(E[idx]), n, sorted(D))
    print(f"d={d} m={m} downsets={len(lev)}", {f"{a}/{b}": v for (a, b), v in sorted(stats.items(), key=str)}, flush=True)
    for kk, v in worst.items(): print('   worst', kk, v[0], 'n=', v[1], 'D=', v[2][:12], flush=True)
