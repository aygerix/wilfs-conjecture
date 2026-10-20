r"""Depth-four LP (lead, 2026-10-20): do value-truncated order-Macaulay constraints imply Wilf at 3m < c <= 4m?
Variables n[j][k][s]: # Apery elements w != 0 of order j (longest factorization), Kunz level k (j <= k <= 4), residue side
s = 0 (r < h) or 1 (r >= h); level 4 forces s = 0.  Element 0: order 0, level 0, side 0.
Constraints (all PROVED facts): side counts h-1 and m-h; some level-4 element; e-1 order-1 elements (the generators);
for every value threshold T in {tm, tm+h}: h_T(j) = #{w < T, order j} satisfies condensed Macaulay
j h_T(j) <= (e-1)(1 + sum_{i<j} h_T(i)) and h_T(2) <= C(e,2).  Objective W = (e-1)(3m+h) - e*sum k n.
usage: python d4lp.py emin emax mmax"""
import sys, itertools
import numpy as np
from scipy.optimize import linprog
def solve(e, m, h, extra=None):
    idx = {}
    for j in range(1, 5):
        for k in range(j, 5):
            for s in (0, 1):
                if k == 4 and s == 1: continue
                idx[(j, k, s)] = len(idx)
    N = len(idx); A, b, Ae, be = [], [], [], []
    def row(d):
        r = np.zeros(N)
        for key, v in d.items(): r[idx[key]] += v
        return r
    Ae.append(row({key: 1 for key in idx if key[2] == 0})); be.append(h - 1)
    Ae.append(row({key: 1 for key in idx if key[2] == 1})); be.append(m - h)
    Ae.append(row({key: 1 for key in idx if key[0] == 1})); be.append(e - 1)
    A.append(row({key: -1 for key in idx if key[1] == 4})); b.append(-1)
    for t in range(1, 5):
        for plus in (0, 1):
            inT = lambda key: key[1] < t or (plus and key[1] == t and key[2] == 0)
            hT = {j: {key: 1 for key in idx if key[0] == j and inT(key)} for j in range(1, 5)}
            for j in range(2, 5):
                d = {}
                for key in hT[j]: d[key] = d.get(key, 0) + j
                for i in range(1, j):
                    for key in hT[i]: d[key] = d.get(key, 0) - (e - 1)
                A.append(row(d)); b.append(e - 1)
            A.append(row(hT[2])); b.append(e * (e - 1) // 2)
    if extra: extra(idx, row, A, b, Ae, be)
    cobj = row({key: -e * key[1] for key in idx})  # W = const + cobj.n
    const = (e - 1) * (3 * m + h)
    res = linprog(cobj, A_ub=np.array(A), b_ub=np.array(b), A_eq=np.array(Ae), b_eq=np.array(be), bounds=[(0, None)] * N, method="highs")
    if res.status != 0: return None, None
    sol = {key: round(res.x[i], 3) for key, i in idx.items() if res.x[i] > 1e-7}
    return const + res.fun, sol
if __name__ == "__main__":
    emin, emax, mmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    for e in range(emin, emax + 1):
        worst = None
        for m in range(e + 2, mmax + 1):
            if 3 * e >= m: continue  # Eliahou: 3e >= m is Wilf
            for h in range(e + 1, m + 1):  # h <= e is DEPTH4-EH
                W, sol = solve(e, m, h)
                if W is None: continue
                if worst is None or W < worst[0]: worst = (W, m, h, sol)
        print("e", e, "min LP W", worst[0] if worst else None, "at m,h", worst[1:3] if worst else None); print("   sol", worst[3] if worst else None)
