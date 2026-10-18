# RGCL0: is MaxCL at sigma = 0 implied by LOCAL subadditivity only?
#  variables r(x) >= 0 on cells, r(0) = 0;  constraints  r(u+v) <= r(u) + r(v) for geometric splits (u,v,u+v in D),
#  and successor relations r(f) <= r(x) + r(e_a) whenever x + e_a not in D and f in D is the cell with phi(f) = phi(x)+p_a.
#  maximize  sum_A (|y|-1) r(y) - (d+1) sum_N r   subject to sum r = 1.  RGCL0 holds iff max <= 0.
#  Variants: geo-only (no successor relations) for contrast.
import sys, random, itertools
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
def rgcl0(cells, d, m, succ=True):
    S = set(cells); zero = tuple([0]*d)
    X = list(cells); idx = {x: i for i, x in enumerate(X)}
    inv = {cells[x] % m: x for x in cells}
    A = set(y for y in X if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d)))
    c = np.array([(sum(x) - 1 if x in A else -(d + 1)) for x in X], float)
    rows = []
    for y in X:
        for u in itertools.product(*[range(k+1) for k in y]):
            v = tuple(a - b for a, b in zip(y, u))
            if u == zero or v == zero or u > v: continue
            rows.append((idx[y], idx[u], idx[v]))
    if succ:
        for x in X:
            for a in range(d):
                xa = tuple(x[:a] + (x[a]+1,) + x[a+1:])
                if xa in S: continue
                ea = tuple(int(i == a) for i in range(d))
                if ea not in S: continue
                f = inv[(cells[x] + cells[ea]) % m]
                rows.append((idx[f], idx[x], idx[ea]))
    Aub = np.zeros((len(rows), len(X)))
    for k, (t, u, v) in enumerate(rows):
        Aub[k, t] += 1; Aub[k, u] -= 1; Aub[k, v] -= 1
    bounds = [(0, None)]*len(X); bounds[idx[zero]] = (0, 0)
    res = linprog(-c, A_ub=Aub, b_ub=np.zeros(len(rows)), A_eq=np.ones((1, len(X))), b_eq=[1.0], bounds=bounds, method='highs')
    return -res.fun
if __name__ == '__main__':
    from ns import NS
    from srcl import tile_of
    from math import gcd
    from functools import reduce
    tests = [NS.from_generators(g) for g in ([39, 71, 72, 77], [25, 44, 45, 49], [36, 37, 42, 43], [29, 50, 69, 90], [58, 240, 241, 253, 254, 256, 280, 281])]
    rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); MMAX = int(sys.argv[3])
    while len(tests) < NT:
        m = rng.randint(6, MMAX); k = rng.randint(2, 8)
        if rng.random() < 0.5:
            base = rng.randint(m + 1, 3*m); gens = sorted(set([m] + [base + rng.randint(0, max(1, m//3)) for _ in range(k)]))
        else:
            gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4, 6])*m) for _ in range(k)]))
        if reduce(gcd, gens) != 1: continue
        tests.append(NS.from_generators(gens))
    n = f1 = f2 = 0
    for s in tests:
        cells, d = tile_of(s)
        v1 = rgcl0(cells, d, s.m, succ=True); v2 = rgcl0(cells, d, s.m, succ=False)
        n += 1
        if v1 > 1e-9:
            f1 += 1; print('RGCL0 FAIL', s.P[:8], 'm', s.m, 'd', d, 'max', round(v1, 4), flush=True)
        if v2 > 1e-9: f2 += 1
    print('tiles', n, '| RGCL0 (geo + successor) fails', f1, '| geo-only fails', f2)
