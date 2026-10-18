# IntervalCL(sigma): for every f: {1..m-1} -> [0,inf) with f(a)+f(b) >= f(a+b) whenever a+b <= m-1 (integer, no wrap):
#   sum_{y in A} (|y|-1) f(r(y)) <= (d+1) sum_{z in N, r(z) != 0} f(r(z)),   r = <phi - sigma>.
# Stronger than GCL (fewer relations => more f) and implies MaxCL (f = id).  LP: min sum c f, c = -w, sum f = 1.
import sys, random
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
_cache = {}
def int_subadd(m):
    if m in _cache: return _cache[m]
    rows, cols, vals = [], [], []; k = 0
    for a in range(1, m):
        for b in range(a, m - a):
            rows += [k, k, k]; cols += [a - 1, b - 1, a + b - 1]; vals += [-1, -1, 1]; k += 1
    M = coo_matrix((vals, (rows, cols)), shape=(max(k, 1), m - 1)).tocsr(); _cache[m] = M; return M
def icl_min(cvec, m):
    Aub = int_subadd(m)
    res = linprog(np.array(cvec[1:], float), A_ub=Aub, b_ub=np.zeros(Aub.shape[0]), A_eq=np.ones((1, m - 1)), b_eq=[1.0],
                  bounds=[(0, None)]*(m - 1), method='highs')
    return res.fun, res.x
if __name__ == '__main__':
    from ns import NS
    from srcl import tile_of
    from groupcone_adv import tile_weights
    from math import gcd
    from functools import reduce
    rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); MMAX = int(sys.argv[3]); mode = sys.argv[4]
    tests = [NS.from_generators(g) for g in ([39, 71, 72, 77], [25, 44, 45, 49], [36, 37, 42, 43], [29, 50, 69, 90], [14, 22, 23, 57, 61, 62, 63])]
    while len(tests) < NT:
        m = rng.randint(6, MMAX); k = rng.randint(2, 10)
        if rng.random() < 0.5:
            base = rng.randint(m + 1, 3*m); gens = sorted(set([m] + [base + rng.randint(0, max(1, m//3)) for _ in range(k)]))
        else:
            gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4])*m) for _ in range(k)]))
        if reduce(gcd, gens) != 1: continue
        tests.append(NS.from_generators(gens))
    f = 0; worst = None; nlp = 0
    for s in tests:
        cells, d = tile_of(s); m = s.m
        wt = tile_weights(cells, d)
        inv = {v % m: x for x, v in cells.items()}
        sigs = range(m) if mode == 'all' else ([0] if mode == 'zero' else [0, s.c % m])
        for sg in sigs:
            cvec = [wt[inv[(g + sg) % m]] for g in range(m)]
            v, fx = icl_min(cvec, m); nlp += 1
            if v < -1e-9:
                f += 1
                if f <= 6: print('ICL FAIL', s.P[:8], 'c', s.c, 'm', m, 'd', d, 'sigma', sg, 'min', round(v, 5),
                                 'f', [round(t*1000, 1) for t in fx][:40], flush=True)
            if worst is None or v < worst[0]: worst = (v, s.P[:6], s.c, m, sg)
    print(len(tests), 'tiles,', nlp, 'LPs; IntervalCL fails', f, '; min', worst)
