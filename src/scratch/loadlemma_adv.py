# Load Lemma on adversarial Apery tiles via HiGHS (scipy): minimize L s.t. for each maximal y (|y|>=2) the pair weights
# on {u, y-u} (0<u<y) sum to |y|-1 and every nonzero non-maximal cell has load <= L.  Load Lemma <=> L* <= d+1.
# Run with a python that has scipy (e.g. scratch venv).  Float LP: report L*/(d+1); borderline cases re-checked exactly.
import sys, itertools, random
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
def opt_load(cells, d):
    S = set(cells)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    N = [z for z in cells if z not in set(A) and sum(z) > 0]
    zi = {z: i for i, z in enumerate(N)}
    A2 = [y for y in A if sum(y) >= 2]
    if not A2: return 0.0, None
    cols = []
    for k, y in enumerate(A2):
        seen = set()
        for u in itertools.product(*[range(v + 1) for v in y]):
            v = tuple(a - b for a, b in zip(y, u))
            if sum(u) == 0 or sum(v) == 0: continue
            key = min(u, v)
            if key in seen: continue
            seen.add(key); cols.append((k, zi[u], zi[v]))
    nv = len(cols) + 1  # last var = L
    Aeq = lil_matrix((len(A2), nv)); beq = np.array([sum(y) - 1 for y in A2], float)
    Aub = lil_matrix((len(N), nv)); bub = np.zeros(len(N))
    for j, (k, a, b) in enumerate(cols):
        Aeq[k, j] = 1; Aub[a, j] += 1; Aub[b, j] += 1
    for i in range(len(N)): Aub[i, nv - 1] = -1
    c = np.zeros(nv); c[-1] = 1
    res = linprog(c, A_ub=Aub.tocsr(), b_ub=bub, A_eq=Aeq.tocsr(), b_eq=beq, bounds=[(0, None)]*nv, method='highs')
    return res.fun, len(cols)
if __name__ == '__main__':
    from ns import NS
    from exp_cl_adv import with_conductor
    from srcl import tile_of
    from math import gcd
    from functools import reduce
    rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); MMAX = int(sys.argv[3])
    tests = []
    for gens, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((30, 44, 48, 49), 118), ((23, 39, 40, 42), 77)]:
        tests.append(with_conductor(gens, c))
    tests += [NS.from_generators(g) for g in ([49, 55, 69, 93], [70, 184, 189, 195, 199], [77, 117, 123, 131, 132], [39, 71, 72, 77])]
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
    f = 0; worst = None
    for s in tests:
        cells, d = tile_of(s)
        L, nc = opt_load(list(cells), d)
        rel = L / (d + 1)
        if rel > 1 + 1e-9:
            f += 1
            if f <= 5: print('LOAD FAIL', s.P[:8], s.c, 'd', d, 'm', s.m, 'L*', L, flush=True)
        if worst is None or rel > worst[0]: worst = (rel, s.P[:8], s.c, d, s.m)
    print(len(tests), 'tiles; Load Lemma fails', f, '; max L*/(d+1)', worst)
