# Independent LP certificate (referee) for the HT-failing realizable tiles found by shapes.py.
# kappa_D(r) = min { Def(p)/min_a p_a : p in closed Groebner cone of (D, r) }, Def(p) = 3m max_{y in Max} p.y - p.T.
# Solved as three LPs (argmin coordinate a normalised to p_a = 1, p_b >= 1) with HiGHS; then (m+1) kappa >= m(m-1)?
import sys, time
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as Fr
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from shapes import plane_partitions_nt, cells, injective_rs, open_cone, canon_shape
from tk import H_of, tops, heights

def kappa(D, m, r, cons):
    T = tops(D); ht = heights(D)
    Tsum = np.zeros(3)
    for x in D:
        for a in range(3): Tsum += np.array(T[x][a])
    Max = [x for x in D if ht[x] == 0]
    best = None
    for a in range(3):
        # variables p1,p2,p3,z ; minimize 3m z - p.T
        c = np.concatenate([-Tsum, [3*m]])
        A_ub = []; b_ub = []
        for y in Max: A_ub.append(list(y) + [-1]); b_ub.append(0)          # p.y - z <= 0
        for v in cons: A_ub.append([-vi for vi in v] + [0]); b_ub.append(0)  # -v.p <= 0
        for b in range(3):
            if b != a: row = [0, 0, 0, 0]; row[b] = -1; A_ub.append(row); b_ub.append(-1)   # p_b >= 1
        A_eq = [[1 if i == a else 0 for i in range(3)] + [0]]; b_eq = [1]
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)]*4, method='highs')
        if res.status == 0:
            if best is None or res.fun < best[0]: best = (res.fun, tuple(res.x[:3]))
    return best

if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        seen = {}
        for layers in plane_partitions_nt(m):
            D = cells(layers)
            if H_of(D) - (m - 1) < 0:
                c = canon_shape(D)
                if c not in seen: seen[c] = D
        for c, D in seen.items():
            for r in injective_rs(D, m):
                poly, cons = open_cone(D, m, r)
                if poly is None: continue
                k = kappa(D, m, r, cons)
                print(f'm={m} delta={H_of(D)-(m-1)} r={r} kappa={k[0]:.4f} at p={tuple(round(t,3) for t in k[1])} '
                      f'(m+1)kappa={((m+1)*k[0]):.1f} vs m(m-1)={m*(m-1)} -> {"OK" if (m+1)*k[0] >= m*(m-1) + 1e-6 else "FAIL"}', flush=True)
