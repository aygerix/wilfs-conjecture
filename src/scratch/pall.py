# PALL (position-aware load lemma) at sigma = 0: exists a fractional one-level geometric split scheme
# (each maximal y, |y|>=2, weight |y|-1 on unordered splits {u, y-u}) such that for every threshold tau
#   sum_{z in N\0, r(z) >= tau} load(z) <= (d+1) * #{z in N\0 : r(z) >= tau}.
# PALL(0) + subadditivity => MaxCL(0) by Abel summation.  Also report the plain Load Lemma (pointwise) for contrast.
import sys, itertools, random
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
def pall(cells, d, m, sigma=0, pointwise=False):
    S = set(cells); zero = tuple([0]*d)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    Aset = set(A)
    r = {x: (cells[x] - sigma) % m for x in cells}
    N1 = [z for z in cells if z not in Aset and z != zero]
    idx = {z: i for i, z in enumerate(N1)}
    var = []; rows_eq = []
    for y in A:
        if sum(y) < 2: continue
        sp = set()
        for u in itertools.product(*[range(k+1) for k in y]):
            v = tuple(a - b for a, b in zip(y, u))
            if u == zero or v == zero: continue
            sp.add(tuple(sorted([u, v])))
        start = len(var)
        for (u, v) in sp: var.append((y, u, v))
        rows_eq.append((start, len(var), sum(y) - 1))
    nv = len(var)
    if nv == 0: return True
    L = np.zeros((len(N1), nv))
    for j, (y, u, v) in enumerate(var):
        L[idx[u], j] += 1; L[idx[v], j] += 1
    Aeq = np.zeros((len(rows_eq), nv)); beq = []
    for i, (s, e, h) in enumerate(rows_eq): Aeq[i, s:e] = 1; beq.append(h)
    if pointwise:
        Aub = L; bub = np.full(len(N1), d + 1.0)
    else:
        order = sorted(N1, key=lambda z: -r[z])
        Aub = np.zeros((len(order), nv)); bub = []
        acc = np.zeros(nv)
        for k, z in enumerate(order):
            acc = acc + L[idx[z]]; Aub[k] = acc; bub.append((d + 1.0)*(k + 1))
    res = linprog(np.zeros(nv), A_ub=Aub, b_ub=np.array(bub), A_eq=Aeq, b_eq=np.array(beq, float), bounds=[(0, None)]*nv, method='highs')
    return res.status == 0
if __name__ == '__main__':
    from ns import NS
    from srcl import tile_of
    from math import gcd
    from functools import reduce
    tests = [NS.from_generators(g) for g in ([39, 71, 72, 77], [58, 240, 241, 253, 254, 256, 280, 281], [75, 534, 548, 551, 563, 567, 569, 587, 597], [36, 37, 42, 43], [29, 50, 69, 90])]
    rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); MMAX = int(sys.argv[3])
    while len(tests) < NT:
        m = rng.randint(8, MMAX); k = rng.randint(2, 10)
        if rng.random() < 0.5:
            base = rng.randint(m + 1, 3*m); gens = sorted(set([m] + [base + rng.randint(0, max(1, m//3)) for _ in range(k)]))
        else:
            gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4, 6])*m) for _ in range(k)]))
        if reduce(gcd, gens) != 1: continue
        tests.append(NS.from_generators(gens))
    n = fp = fw = 0
    for s in tests:
        cells, d = tile_of(s)
        okp = pall(cells, d, s.m, 0, pointwise=True); okw = pall(cells, d, s.m, 0)
        n += 1; fp += not okp; fw += not okw
        if not okw: print('PALL(0) FAIL', s.P[:8], 'm', s.m, 'd', d, flush=True)
        if not okp and n <= 5: print('  pointwise Load Lemma fails (expected sometimes):', s.P[:6], 'PALL ok' if okw else '', flush=True)
    print('tiles', n, '| pointwise Load Lemma fails', fp, '| PALL(0) fails', fw)
