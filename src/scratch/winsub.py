# Assert window subadditivity: if m | c then rho(u) <= rho(x) + rho(y) - 1 for every u in X and split n(u) = x + y (x,y in T, nonzero);
# in general rho(x) + rho(y) - 1 = rho(u) - gamma + m*kappa, gamma = c mod m, kappa in {0,1,2} ({0,1} when m | c).
import sys, itertools
sys.path.insert(0, 'src')
from ns import NS, all_by_genus
from cl import factorizations_down_set
from top2 import top2
G = int(sys.argv[1]); nmc = 0; nsplit = 0
for g, s in all_by_genus(G):
    if s.m < 2: continue
    m, c = s.m, s.c; gam = c % m
    Pp, best = factorizations_down_set(s, 'grlex'); T = set(best.values()); lam = {x: w for w, x in best.items()}
    rho = {x: ((lam[x] - c) % m) + 1 for x in T}
    for u in (x for x in T if lam[x] >= c):
        for x in itertools.product(*[range(v + 1) for v in u]):
            y = tuple(a - b for a, b in zip(u, x))
            if sum(x) == 0 or sum(y) == 0: continue
            assert x in T and y in T and lam[x] < c and lam[y] < c
            k = rho[x] + rho[y] - 1 - (rho[u] - gam)
            assert k in (0, m, 2 * m) and (gam > 0 or k in (0, m)), (s.P, u, x, k)
            if gam == 0: assert rho[u] <= rho[x] + rho[y] - 1
            nsplit += 1
    nmc += gam == 0
print(f'genus <= {G}: window identity asserted on {nsplit} splits; {nmc} S with m | c (subadditivity asserted)')
s = NS.from_generators([36, 37, 42, 43]); l2, r = top2(s); print('<36,37,42,43>: m', s.m, 'c', s.c, 'W', s.W, "TOP'' slack", (r - l2) / 2)
