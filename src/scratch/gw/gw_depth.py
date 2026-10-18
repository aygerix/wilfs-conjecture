# Depth-refined corner reflection:  |U_i| <= t_i |L_i|  for every depth i, where U_i = {kappa >= i},
# L_i = {lambda >= i}, t_i = #corners with kappa >= i.  Hence GW holds if  sum_i t_i |L_i| <= d sum_i |L_i|.
# Counts, among instances with t(D) > d, how many this covers; asserts |U_i| <= t_i |L_i|.
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
    big = cov1 = covd = 0
    for D in lev:
        if any(u not in D for u in U): continue
        Ds = sorted(D); cm = np.array([all(add(y, u) not in D for u in U) for y in Ds])
        if cm.sum() <= d: continue
        X = np.array(Ds, dtype=np.int64)
        ok = np.all(np.sort((X @ S.T) % m, axis=0) == ar, axis=0)
        if not ok.any(): continue
        N = (S[ok][:, None, :] + m * ks[None, :, :]).reshape(-1, d)
        V = X @ N.T; M = V.max(0); kap = V // m; lam = (M[None, :] - V) // m
        Kmax = int(kap.max())
        lhs = np.zeros(V.shape[1], dtype=np.int64); Lsum = np.zeros(V.shape[1], dtype=np.int64)
        t1 = (cm[:, None] & (kap >= 1)).sum(0)
        for i in range(1, Kmax + 1):
            Ui = (kap >= i).sum(0); Li = (lam >= i).sum(0); ti = (cm[:, None] & (kap >= i)).sum(0)
            assert np.all(Ui <= ti * Li)
            lhs += ti * Li; Lsum += Li
        big += V.shape[1]; covd += int((lhs <= d * Lsum).sum()); cov1 += int((t1 <= d).sum())
    print(f"d={d} m={m} K={K} instances with t>d: {big}; covered by t_1<=d: {cov1}; by depth-weighted: {covd}", flush=True)
