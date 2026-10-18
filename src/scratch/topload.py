# TOP-load LP: for each top-layer u in X (|n(u)| >= 2), weights on splits {x, n(u)-x} (0 < x < n(u)) summing to |n(u)|-1;
# minimize L = max load on nonzero cells (all such cells are non-X).  TL holds iff L* <= d+1.
# If m | c and TL holds then TOP'' holds (window subadditivity rho(u) <= rho(x)+rho(y)-1), hence Wilf.
import sys, itertools, random, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
sys.path.insert(0, 'src')
from ns import NS, all_by_genus
from cl import factorizations_down_set
def topload(s):
    m, c = s.m, s.c
    Pp, best = factorizations_down_set(s, 'grlex'); d = len(Pp)
    T = set(best.values()); lam = {x: w for w, x in best.items()}
    X = [x for x in T if lam[x] >= c]
    X2 = [y for y in X if sum(y) >= 2]
    if not X2: return 0.0, d, len(X)
    cells = sorted({u for y in X2 for u in itertools.product(*[range(v + 1) for v in y]) if 0 < sum(u) < sum(y)})
    zi = {z: i for i, z in enumerate(cells)}
    cols = []
    for k, y in enumerate(X2):
        seen = set()
        for u in itertools.product(*[range(v + 1) for v in y]):
            v = tuple(a - b for a, b in zip(y, u))
            if sum(u) == 0 or sum(v) == 0: continue
            key = min(u, v)
            if key in seen: continue
            seen.add(key); cols.append((k, zi[u], zi[v]))
    nv = len(cols) + 1
    Aeq = lil_matrix((len(X2), nv)); beq = np.array([sum(y) - 1 for y in X2], float)
    Aub = lil_matrix((len(cells), nv)); bub = np.zeros(len(cells))
    for j, (k, a, b) in enumerate(cols):
        Aeq[k, j] = 1; Aub[a, j] += 1; Aub[b, j] += 1
    for i in range(len(cells)): Aub[i, nv - 1] = -1
    cost = np.zeros(nv); cost[-1] = 1
    r = linprog(cost, A_ub=Aub.tocsr(), b_ub=bub, A_eq=Aeq.tocsr(), b_eq=beq, bounds=[(0, None)] * nv, method='highs')
    assert r.status == 0
    return r.fun, d, len(X)
if __name__ == '__main__':
    mode = sys.argv[1]; t0 = time.time(); worst = None; n = 0; bad = 0; nmc = 0; badmc = 0
    def feed():
        if mode == 'g':
            for g, s in all_by_genus(int(sys.argv[2])):
                if s.m >= 3 and s.e >= 3: yield s
        else:
            rnd = random.Random(int(sys.argv[2])); budget = int(sys.argv[3])
            while time.time() - t0 < budget:
                e = rnd.randint(3, 9); m = rnd.randint(max(10, 3 * e + 1), 60); q = rnd.randint(4, 7)
                gens = [m] + rnd.sample(range(m + 1, 3 * m), e - 1)
                try: s = NS.from_generators(gens + list(range(q * m, q * m + m + 1)))
                except ValueError: continue
                if s.e >= 3 and s.c % s.m == 0 and s.c > 3 * s.m: yield s
    for s in feed():
        L, d, tau = topload(s); n += 1
        ok = L <= d + 1 + 1e-9; bad += not ok
        if s.c % s.m == 0: nmc += 1; badmc += not ok
        key = L / (d + 1)
        if worst is None or key > worst[0]: worst = (round(key, 4), s.P, s.m, s.c, d, tau, round(L, 3))
    print(f'mode {mode} {sys.argv[2:]}: {n} S ({nmc} with m|c); TL fails {bad} ({badmc} with m|c); worst L*/(d+1) {worst}; {time.time()-t0:.0f}s')
