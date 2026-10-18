# HCR++ (shape-only MILP): minimize sum_t w(t) v(t) over integers v(t) >= 0 with
#   v(t) >= v(t + e_a) + (m+1) for every cover t -> t+e_a in D  (lam(z) - lam(t) >= (m+1)|z - t|),
#   v(t) = r(t) + m k(t), k(t) >= 0 integer, and r a bijection D -> Z/m (distinct residues of Lam - lam).
# minB / ((d-1) m (m-1)/2) >= 1 certifies Wilf for every semigroup with factorization tile D.
import sys; sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
def hcrpp_shape(D, tlim=120):
    D = sorted(set(D)); d = len(D[0]); m = len(D); Ds = set(D); idx = {z: i for i, z in enumerate(D)}
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]; add = lambda x, y: tuple(p + q for p, q in zip(x, y))
    w = np.zeros(m)
    for x in D:
        for a in range(d):
            t = x
            while add(t, U[a]) in Ds: t = add(t, U[a])
            w[idx[t]] += 1
    # variables: x[t,r] (m*m binaries), k[t] (m integers); v_t = sum_r r x[t,r] + m k[t]
    nx = m * m; nv = nx + m
    cost = np.zeros(nv)
    for t in range(m):
        for r in range(m): cost[t * m + r] = w[t] * r
        cost[nx + t] = w[t] * m
    rows = []; covers = [(idx[t], idx[add(t, u)]) for t in D for u in U if add(t, u) in Ds]
    A = lil_matrix((2 * m + len(covers), nv)); lb = np.zeros(2 * m + len(covers)); ub = np.zeros(2 * m + len(covers))
    for t in range(m):
        for r in range(m): A[t, t * m + r] = 1
        lb[t] = ub[t] = 1
    for r in range(m):
        for t in range(m): A[m + r, t * m + r] = 1
        lb[m + r] = ub[m + r] = 1
    for k, (t, z) in enumerate(covers):      # v_t - v_z >= m + 1
        row = 2 * m + k
        for r in range(m): A[row, t * m + r] += r; A[row, z * m + r] -= r
        A[row, nx + t] += m; A[row, nx + z] -= m
        lb[row] = m + 1; ub[row] = np.inf
    integ = np.ones(nv)
    bnd = Bounds(np.zeros(nv), np.concatenate([np.ones(nx), np.full(m, np.inf)]))
    res = milp(cost, constraints=[LinearConstraint(A.tocsr(), lb, ub)], integrality=integ, bounds=bnd,
               options={'time_limit': tlim, 'disp': False})
    need = (d - 1) * m * (m - 1) / 2
    lowb = getattr(res, 'mip_dual_bound', None)
    return (res.fun / need if res.x is not None else None), (lowb / need if lowb is not None else None), res.status
if __name__ == '__main__':
    from ns import NS
    from cl import factorizations_down_set
    for g in sys.argv[1:]:
        s = NS.from_generators(list(map(int, g.split(','))))
        Pp, best = factorizations_down_set(s, 'grlex')
        print(f'<{g}>: HCR++ (best found, proven lower bound, status) =', hcrpp_shape(list(best.values())))
