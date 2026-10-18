# AMaxCL (affine MaxCL, residue-free): for every affine L(x) = l0 + alpha.x with L >= 0 on D,
#   sum_A (|y|-1) L(y) <= (d+1) sum_N L(z).     (handles every carry-free rotation, where r = L exactly)
# LP: maximize sum_x w(x) L(x) s.t. L(x) >= 0 on D, sum_x L(x) = 1.  AMaxCL holds iff max <= 0.
# Special rays: alpha = e_a (beta_a <= 0), constants, and 'reversed' L = c - x_a.
import sys, itertools, random
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
def amax(D, d):
    S = set(D)
    A = set(y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d)))
    X = list(D)
    w = np.array([(sum(x) - 1 if x in A else -(d + 1)) for x in X], float)
    M = np.array([[1.0] + list(x) for x in X])          # L = M @ (l0, alpha)
    c = -(w @ M)
    res = linprog(c, A_ub=-M, b_ub=np.zeros(len(X)), A_eq=(np.ones(len(X)) @ M).reshape(1, -1), b_eq=[1.0],
                  bounds=[(None, None)]*(d + 1), method='highs')
    return -res.fun, res.x
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'exh':
        from exp_cl_tiling import downsets
        for d, mmax in [(2, 13), (3, 10), (4, 8), (5, 7)]:
            n = f = 0; ex = None
            for m in range(2, mmax + 1):
                for D in downsets(m, d):
                    if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                    tile = any(len({sum(i*j for i, j in zip(y, p)) % m for y in D}) == m for p in itertools.product(range(1, m), repeat=d))
                    if not tile: continue
                    n += 1; v, sol = amax(D, d)
                    if v > 1e-9:
                        f += 1
                        if ex is None or v > ex[0]: ex = (round(v, 4), m, sorted(D), [round(t, 3) for t in sol])
            print('d', d, 'tile shapes', n, 'AMaxCL fails', f, 'worst', ex, flush=True)
    else:
        from ns import NS
        from srcl import tile_of
        from math import gcd
        from functools import reduce
        rng = random.Random(int(sys.argv[2])); NT = int(sys.argv[3]); MMAX = int(sys.argv[4])
        tests = [NS.from_generators(g) for g in ([39, 71, 72, 77], [25, 44, 45, 49], [36, 37, 42, 43], [29, 50, 69, 90], [58, 240, 241, 253, 254, 256, 280, 281], [14, 22, 23, 57, 61, 62, 63])]
        while len(tests) < NT:
            m = rng.randint(6, MMAX); k = rng.randint(2, 10)
            if rng.random() < 0.5:
                base = rng.randint(m + 1, 3*m); gens = sorted(set([m] + [base + rng.randint(0, max(1, m//3)) for _ in range(k)]))
            else:
                gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4, 6])*m) for _ in range(k)]))
            if reduce(gcd, gens) != 1: continue
            tests.append(NS.from_generators(gens))
        n = f = 0; worst = None
        for s in tests:
            cells, d = tile_of(s)
            v, sol = amax(list(cells), d); n += 1
            if v > 1e-9:
                f += 1
                if f <= 5: print('AMaxCL FAIL', s.P[:8], 'm', s.m, 'd', d, 'max', round(v, 4), [round(t, 3) for t in sol], flush=True)
            if worst is None or v > worst[0]: worst = (v, s.P[:6])
        print('tiles', n, 'AMaxCL fails', f, 'worst', worst)
