# ATOP: residue-free relaxation of TOP'' (m | c).  Variables r: T -> R with r in the convex hull of permutations of
# {0..m-1} (Birkhoff: r = P v, P doubly stochastic), r(0) = 0, and geometric subadditivity r(x+y) <= r(x) + r(y) for all
# nonzero x, y with x + y in T.  Maximize sum_{u in X} (r(u)+1)(l(u)+d); ATOP holds iff max <= m((d+1)m + d - 1)/2.
# The true residues r = lambda mod m satisfy every constraint when m | c, so ATOP  =>  TOP''  =>  Wilf.
import sys, itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def atop(s, Xmode='X'):
    m, c = s.m, s.c
    Pp, best = factorizations_down_set(s, 'grlex'); d = len(Pp)
    T = sorted(best.values()); idx = {z: i for i, z in enumerate(T)}; lam = {x: w for w, x in best.items()}
    Tset = set(T)
    if Xmode == 'X': X = [x for x in T if lam[x] >= c]
    else: X = [x for x in T if all(tuple(x[b] + (b == a) for b in range(d)) not in Tset for a in range(d))]
    nP = m * m; nv = m + nP                      # r_z (m), P_{z,j} (m*m)
    Aeq = lil_matrix((3 * m + 1, nv)); beq = np.zeros(3 * m + 1); row = 0
    for z in range(m):                           # r_z - sum_j j P_{zj} = 0
        Aeq[row, z] = 1
        for j in range(m): Aeq[row, m + z * m + j] = -j
        row += 1
    for z in range(m):                           # row sums
        for j in range(m): Aeq[row, m + z * m + j] = 1
        beq[row] = 1; row += 1
    for j in range(m):                           # column sums
        for z in range(m): Aeq[row, m + z * m + j] = 1
        beq[row] = 1; row += 1
    Aeq[row, idx[tuple([0] * d)]] = 1; beq[row] = 0; row += 1
    sub = []
    for x in T:
        if sum(x) == 0: continue
        for y in T:
            if sum(y) == 0 or y < x: continue
            z = tuple(a + b for a, b in zip(x, y))
            if z in Tset: sub.append((idx[z], idx[x], idx[y]))
    Aub = lil_matrix((len(sub), nv)); bub = np.zeros(len(sub))
    for k, (z, x, y) in enumerate(sub):
        Aub[k, z] += 1; Aub[k, x] -= 1; Aub[k, y] -= 1
    cost = np.zeros(nv)
    for u in X: cost[idx[u]] -= (sum(u) + d)
    r = linprog(cost, A_ub=Aub.tocsr() if sub else None, b_ub=bub if sub else None, A_eq=Aeq.tocsr(), b_eq=beq,
                bounds=[(0, None)] * nv, method='highs')
    assert r.status == 0, r.message
    lhs = -r.fun + sum(sum(u) + d for u in X)
    rhs = m * ((d + 1) * m + d - 1) / 2
    true = sum(((lam[u] - c) % m + 1) * (sum(u) + d) for u in X)
    return lhs, rhs, true, d, len(X), len(sub)
if __name__ == '__main__':
    for g in sys.argv[1:]:
        s = NS.from_generators(list(map(int, g.split(','))))
        lhs, rhs, true, d, nx, ns_ = atop(s)
        print(f'<{g}> m={s.m} c={s.c} m|c={s.c % s.m == 0} e={s.e} |X|={nx} sub={ns_}: ATOP max {lhs:.2f}  bound {rhs:.1f}  true {true}  ->',
              'HOLDS' if lhs <= rhs + 1e-6 else 'FAILS', f' (normalized slack {(rhs - lhs) / rhs:.4f})')
