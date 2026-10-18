# GLL1 (one-level lattice pairing) on adversarial Apery tiles, HiGHS: minimize L s.t. each maximal y != z0 with |y|>=2
# splits |y|-1 tokens into pairs {u,v} of non-maximal cells != z0 with psi(u)+psi(v) = psi(y); loads <= L.
# GLL1 holds iff L* <= d+1 (and every such y has at least one admissible pair).
import sys, random
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
def gll1_opt(cells, d, m, sg):
    S = set(cells)
    A = {y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))}
    inv = {v % m: x for x, v in cells.items()}
    z0 = inv[sg % m]
    N = [z for z in cells if z not in A and z != z0]
    zi = {z: i for i, z in enumerate(N)}
    ys = [y for y in A if sum(y) >= 2 and y != z0]
    if not ys: return 0.0
    cols = []
    for k, y in enumerate(ys):
        tgt = (cells[y] - sg) % m; seen = set(); cnt = 0
        for u in N:
            pu = (cells[u] - sg) % m
            v = inv[(tgt - pu + sg) % m]
            if v not in zi: continue
            key = (min(zi[u], zi[v]), max(zi[u], zi[v]))
            if key in seen: continue
            seen.add(key); cols.append((k, zi[u], zi[v])); cnt += 1
        if cnt == 0: return float('inf')
    nv = len(cols) + 1
    Aeq = lil_matrix((len(ys), nv)); beq = np.array([sum(y) - 1 for y in ys], float)
    Aub = lil_matrix((len(N), nv))
    for j, (k, a, b) in enumerate(cols):
        Aeq[k, j] = 1; Aub[a, j] += 1; Aub[b, j] += 1
    for i in range(len(N)): Aub[i, nv - 1] = -1
    c = np.zeros(nv); c[-1] = 1
    res = linprog(c, A_ub=Aub.tocsr(), b_ub=np.zeros(len(N)), A_eq=Aeq.tocsr(), b_eq=beq, bounds=[(0, None)]*nv, method='highs')
    return res.fun if res.status == 0 else float('inf')
if __name__ == '__main__':
    from ns import NS
    from exp_cl_adv import with_conductor
    from srcl import tile_of
    from math import gcd
    from functools import reduce
    rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); MMAX = int(sys.argv[3]); allsig = sys.argv[4] == 'all'
    tests = [NS.from_generators(g) for g in ([39, 71, 72, 77], [49, 55, 69, 93], [70, 184, 189, 195, 199])]
    while len(tests) < NT:
        m = rng.randint(6, MMAX); k = rng.randint(2, 12)
        if rng.random() < 0.5:
            base = rng.randint(m + 1, 3*m); gens = sorted(set([m] + [base + rng.randint(0, max(1, m//3)) for _ in range(k)]))
        else:
            gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4])*m) for _ in range(k)]))
        if reduce(gcd, gens) != 1: continue
        s0 = NS.from_generators(gens); tests.append(s0)
        for fr in (0.4, 0.7):
            if int(s0.c*fr) > m: tests.append(with_conductor(gens, int(s0.c*fr)))
    stats = {}
    for s in tests:
        cells, d = tile_of(s); m = s.m
        reg = 'm>3e' if m > 3*(d+1) else 'm<=3e'
        sigs = range(m) if allsig else [s.c % m]
        for sg in sigs:
            L = gll1_opt(cells, d, m, sg)
            ok = L <= d + 1 + 1e-9
            st = stats.setdefault(reg, [0, 0, None])
            st[0] += 1; st[1] += (not ok)
            if not ok and st[2] is None: st[2] = (s.P[:8], s.c, m, d, sg, L)
    for k, v in stats.items(): print(k, 'LPs', v[0], 'GLL1 fails', v[1], 'first', v[2])
