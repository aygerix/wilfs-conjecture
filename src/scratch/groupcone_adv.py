# Group-cone MaxCL (GCL) on adversarial Apery tiles (HiGHS): for each sigma, minimize sum_g c(g) r(g) over
# r: Z/m -> [0, inf), r(0)=0, r(g)+r(h) >= r(g+h), sum r = 1.  GCL holds at sigma iff min >= 0.
import sys, random
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
_cache = {}
def subadd_matrix(m):
    if m in _cache: return _cache[m]
    rows, cols, vals = [], [], []; k = 0
    for g in range(1, m):
        for h in range(g, m):
            t = (g + h) % m
            if t == 0: continue
            # -(r_g + r_h - r_t) <= 0
            rows += [k, k]; cols += [g - 1, h - 1]; vals += [-1, -1]
            rows.append(k); cols.append(t - 1); vals.append(1); k += 1
    M = coo_matrix((vals, (rows, cols)), shape=(k, m - 1)).tocsr()
    _cache[m] = M
    return M
def gcl_min(cvec, m):
    Aub = subadd_matrix(m)
    res = linprog(np.array(cvec[1:], float), A_ub=Aub, b_ub=np.zeros(Aub.shape[0]), A_eq=np.ones((1, m - 1)), b_eq=[1.0],
                  bounds=[(0, None)]*(m - 1), method='highs')
    return res.fun, res.x
def tile_weights(cells, d):
    S = set(cells)
    A = {y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))}
    return {x: (-(sum(x) - 1) if x in A else d + 1) for x in cells}
if __name__ == '__main__':
    from ns import NS
    from exp_cl_adv import with_conductor
    from srcl import tile_of
    from math import gcd
    from functools import reduce
    rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); MMAX = int(sys.argv[3]); allsig = sys.argv[4] == 'all'
    tests = [NS.from_generators(g) for g in ([39, 71, 72, 77], [49, 55, 69, 93], [70, 184, 189, 195, 199])]
    for gens, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((30, 44, 48, 49), 118), ((23, 39, 40, 42), 77)]:
        tests.append(with_conductor(gens, c))
    while len(tests) < NT:
        m = rng.randint(6, MMAX); k = rng.randint(2, 12)
        if rng.random() < 0.5:
            base = rng.randint(m + 1, 3*m); gens = sorted(set([m] + [base + rng.randint(0, max(1, m//3)) for _ in range(k)]))
        else:
            gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4])*m) for _ in range(k)]))
        if reduce(gcd, gens) != 1: continue
        s0 = NS.from_generators(gens)
        tests.append(s0)
        for fr in (0.4, 0.7):
            if int(s0.c*fr) > m: tests.append(with_conductor(gens, int(s0.c*fr)))
    f = 0; worst = None; nlp = 0
    for s in tests:
        cells, d = tile_of(s); m = s.m
        wt = tile_weights(cells, d)
        inv = {v % m: x for x, v in cells.items()}
        sigs = range(m) if allsig else [s.c % m, 0]
        for sg in sigs:
            cvec = [wt[inv[(g + sg) % m]] for g in range(m)]
            v, r = gcl_min(cvec, m); nlp += 1
            if v < -1e-9:
                f += 1
                if f <= 5: print('GCL FAIL', s.P[:8], s.c, 'm', m, 'd', d, 'sigma', sg, 'min', v, flush=True)
            if worst is None or v < worst[0]: worst = (v, s.P[:6], s.c, m, sg)
    print(len(tests), 'tiles,', nlp, 'LPs; GCL fails', f, '; min', worst)
