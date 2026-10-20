r"""Depth-four LP, v2 (lead, 2026-10-20): generator distribution g[(k,s)] (level k, side s) enumerated; for each value
threshold T the truncated order sequence h_T has h_T(1) = #generators below T (exact), so condensed Macaulay
j h_T(j) <= h_T(1)(1 + sum_{i<j} h_T(i)) is linear.  Also Macaulay h_T(2) <= C(h_T(1)+1, 2).
usage: python d4lp2.py e mmax mstep"""
import sys, itertools
import numpy as np
from scipy.optimize import linprog
BINS = [(1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0)]
def comps(n, k):
    if k == 1: yield (n,); return
    for i in range(n + 1):
        for r in comps(n - i, k - 1): yield (i,) + r
def solve(e, m, h, g):
    idx = {}
    for j in range(2, 5):
        for k in range(j, 5):
            for s in (0, 1):
                if k == 4 and s == 1: continue
                idx[(j, k, s)] = len(idx)
    N = len(idx); A, b, Ae, be = [], [], [], []
    def row(d):
        r = np.zeros(N)
        for key, v in d.items(): r[idx[key]] += v
        return r
    glo = sum(g[i] for i, B in enumerate(BINS) if B[1] == 0); ghi = e - 1 - glo
    Ae.append(row({key: 1 for key in idx if key[2] == 0})); be.append(h - 1 - glo)
    Ae.append(row({key: 1 for key in idx if key[2] == 1})); be.append(m - h - ghi)
    if g[6] == 0: A.append(row({key: -1 for key in idx if key[1] == 4})); b.append(-1)
    for t in range(1, 6):
        for plus in (0, 1):
            inT = lambda k, s: k < t or (plus and k == t and s == 0)
            h1 = sum(g[i] for i, B in enumerate(BINS) if inT(*B))
            hT = {j: {key: 1 for key in idx if key[0] == j and inT(key[1], key[2])} for j in range(2, 5)}
            for j in range(2, 5):
                d = {}
                for key in hT[j]: d[key] = d.get(key, 0) + j
                for i in range(2, j):
                    for key in hT[i]: d[key] = d.get(key, 0) - h1
                A.append(row(d)); b.append(h1 * (1 + h1))
            A.append(row(hT[2])); b.append(h1 * (h1 + 1) // 2)
    cobj = row({key: -e * key[1] for key in idx})
    const = (e - 1) * (3 * m + h) - e * sum(g[i] * B[0] for i, B in enumerate(BINS))
    res = linprog(cobj, A_ub=np.array(A), b_ub=np.array(b), A_eq=np.array(Ae), b_eq=np.array(be), bounds=[(0, None)] * N, method="highs")
    if res.status != 0: return None, None
    return const + res.fun, {key: round(res.x[i], 2) for key, i in idx.items() if res.x[i] > 1e-7}
if __name__ == "__main__":
    e, mmax, mstep = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    worst = None; neg = 0; tot = 0
    for g in comps(e - 1, len(BINS)):
        for m in range(3 * e + 1, mmax + 1, mstep):
            for h in range(e + 1, m + 1):
                if g[0] + g[2] + g[4] + g[6] > h - 1 or g[1] + g[3] + g[5] > m - h: continue
                W, sol = solve(e, m, h, g)
                if W is None: continue
                tot += 1
                if W < -1e-6: neg += 1
                if worst is None or W < worst[0]: worst = (W, m, h, g, sol)
    print("e", e, "feasible", tot, "negative", neg, "min W", worst[0], "m,h", worst[1:3], "gens by (level,side)", dict(zip(BINS, worst[3])))
    print("   sol", worst[4])
