# ATOP on abstract down-sets T (X = all maximal cells, the worst case): max over r in the permutation hull of {0..m-1},
# r(0) = 0, r(x+y) <= r(x) + r(y) (x, y, x+y in T), of sum_{u in X} (r(u)+1)(|u|+d), versus m((d+1)m + d - 1)/2.
import sys, itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
def atop_shape(T, X=None):
    T = sorted(set(T)); m = len(T); d = len(T[0]); Tset = set(T); idx = {z: i for i, z in enumerate(T)}
    unit = lambda a: tuple(int(b == a) for b in range(d))
    if X is None: X = [x for x in T if all(tuple(p + q for p, q in zip(x, unit(a))) not in Tset for a in range(d))]
    nv = m + m * m
    Aeq = lil_matrix((3 * m + 1, nv)); beq = np.zeros(3 * m + 1); row = 0
    for z in range(m):
        Aeq[row, z] = 1
        for j in range(m): Aeq[row, m + z * m + j] = -j
        row += 1
    for z in range(m):
        for j in range(m): Aeq[row, m + z * m + j] = 1
        beq[row] = 1; row += 1
    for j in range(m):
        for z in range(m): Aeq[row, m + z * m + j] = 1
        beq[row] = 1; row += 1
    Aeq[row, idx[tuple([0] * d)]] = 1; row += 1
    sub = []
    for i, x in enumerate(T):
        if sum(x) == 0: continue
        for y in T[i:]:
            if sum(y) == 0: continue
            z = tuple(a + b for a, b in zip(x, y))
            if z in Tset: sub.append((idx[z], idx[x], idx[y]))
    Aub = lil_matrix((max(1, len(sub)), nv)); bub = np.zeros(max(1, len(sub)))
    for k, (z, x, y) in enumerate(sub): Aub[k, z] += 1; Aub[k, x] -= 1; Aub[k, y] -= 1
    cost = np.zeros(nv)
    for u in X: cost[idx[u]] -= (sum(u) + d)
    r = linprog(cost, A_ub=Aub.tocsr(), b_ub=bub, A_eq=Aeq.tocsr(), b_eq=beq, bounds=[(0, None)] * nv, method='highs')
    assert r.status == 0, r.message
    lhs = -r.fun + sum(sum(u) + d for u in X); rhs = m * ((d + 1) * m + d - 1) / 2
    return lhs, rhs, m, d, len(X)
def book(d, n, pages=None):
    pages = pages or list(range(1, d))
    T = set()
    for j in pages:
        for a in range(n + 1):
            for b in range(n + 1 - a):
                z = [0] * d; z[0] = a; z[j] = b; T.add(tuple(z))
    return sorted(T)
if __name__ == '__main__':
    for d in (3, 4, 5):
        for n in range(2, 8):
            T = book(d, n)
            if len(T) > 60: continue
            lhs, rhs, m, d_, nx = atop_shape(T)
            print(f'book d={d} pages={d-1} n={n}: m={m} |A|={nx} ATOP {lhs:.1f} / {rhs:.1f}  slack {(rhs-lhs)/rhs:+.4f}', 'FAIL' if lhs > rhs + 1e-6 else '')
