# ATOP_gamma (any c): r(x) = (lambda(x) - c) mod m satisfies r in the permutation hull, r(0) = (-c) mod m,
# r(x+y) <= r(x) + r(y) + gamma (gamma = c mod m).  Maximize sum_{u in X} (r(u)+1)(|u|+d), X = Ap ∩ [c, c+m);
# ATOP_gamma holds iff max <= m((d+1)m + d - 1)/2, and then TOP'' and Wilf hold (Lemma A).
import sys, random, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def atop_g(s):
    m, c = s.m, s.c; gam = c % m
    Pp, best = factorizations_down_set(s, 'grlex'); d = len(Pp)
    T = sorted(best.values()); Ts = set(T); idx = {z: i for i, z in enumerate(T)}; lam = {x: w for w, x in best.items()}
    X = [x for x in T if lam[x] >= c]
    nv = m + m * m
    Aeq = lil_matrix((3 * m + 1, nv)); beq = np.zeros(3 * m + 1); row = 0
    for z in range(m):
        Aeq[row, z] = 1
        for j in range(m): Aeq[row, m + z * m + j] = -j
        row += 1
    for z in range(m):
        for j in range(m): Aeq[row, m + z * m + j] = 1
        beq[row] = 1; row += 1
    for j in range(m):
        for z in range(m): Aeq[row, m + z * m + j] = 1
        beq[row] = 1; row += 1
    Aeq[row, idx[tuple([0] * d)]] = 1; beq[row] = (-c) % m; row += 1
    sub = []
    for i, x in enumerate(T):
        if sum(x) == 0: continue
        for y in T[i:]:
            if sum(y) == 0: continue
            z = tuple(a + b for a, b in zip(x, y))
            if z in Ts: sub.append((idx[z], idx[x], idx[y]))
    Aub = lil_matrix((max(1, len(sub)), nv)); bub = np.full(max(1, len(sub)), float(gam))
    for k, (z, x, y) in enumerate(sub): Aub[k, z] += 1; Aub[k, x] -= 1; Aub[k, y] -= 1
    cost = np.zeros(nv)
    for u in X: cost[idx[u]] -= (sum(u) + d)
    r = linprog(cost, A_ub=Aub.tocsr(), b_ub=bub, A_eq=Aeq.tocsr(), b_eq=beq, bounds=[(0, None)] * nv, method='highs')
    assert r.status == 0
    lhs = -r.fun + sum(sum(u) + d for u in X); rhs = m * ((d + 1) * m + d - 1) / 2
    true = sum(((lam[u] - c) % m + 1) * (sum(u) + d) for u in X)
    assert true <= lhs + 1e-6
    return lhs / rhs, true / rhs
if __name__ == '__main__':
    E0, E1, seed, budget, mmax = map(int, sys.argv[1:6]); rnd = random.Random(seed); t0 = time.time()
    n = 0; bad = []; worst = None; byg = {}
    while time.time() - t0 < budget:
        e = rnd.randint(E0, E1); m = rnd.randint(3 * e + 1, mmax)
        try: s = NS.from_generators([m] + rnd.sample(range(m + 1, 3 * m), e - 1))
        except ValueError: continue
        if s.e != e or s.c <= 3 * s.m: continue
        ra, rt = atop_g(s); n += 1; g0 = s.c % s.m == 0
        byg[g0] = max(byg.get(g0, 0), ra)
        if ra > 1 + 1e-9: bad.append((s.P, s.c, round(ra, 4))); print('FAIL', s.P, 'c', s.c, 'gamma', s.c % s.m, f'{ra:.4f}', 'true', round(rt, 4), flush=True)
        if worst is None or ra > worst[0]: worst = (round(ra, 4), s.P, s.c, s.c % s.m)
    print(f'e in [{E0},{E1}], c > 3m, 3e < m, gens < 3m, seed {seed}: {n} S, ATOP_gamma fails {len(bad)}; worst {worst}; max ratio m|c {byg.get(True)}, m∤c {byg.get(False)}; {time.time()-t0:.0f}s')
