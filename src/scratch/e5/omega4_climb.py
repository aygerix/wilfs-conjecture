"""Max Omega/m over 4-D Apery tiles for large m (lead 2026-10-19).  Semigroups <m, m+r1..m+r4> (simplex-like grlex
tiles); random restarts + hill climbing on r maximizing Omega/m = sum_A (d+|y|)/m.  Also reports MaxCL min ratio at
the best tile.  usage: python omega4_climb.py seed m restarts steps"""
import sys, random, math
sys.path.insert(0, '/home/jmercedes/wilf/nowrap')
from pmin_tile import apery, minimal_gens, tile
seed, m, R, ST = map(int, sys.argv[1:5]); rng = random.Random(seed)
def omega(r):
    gens = [m+x for x in r]
    if len(set(x % m for x in gens)) < 4 or None in apery(m, gens): return None
    n, ap = minimal_gens(m, gens)
    if len(n) != 4: return None
    D = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values()); Ds = set(D); d = 4
    A = [y for y in D if all(tuple(y[i]+(i == a) for i in range(d)) not in Ds for a in range(d))]
    return sum(d+sum(y) for y in A)/m, D, A, [g % m for g in n]
best = None
for rs in range(R):
    r = sorted(rng.sample(range(1, m), 4)); cur = omega(r)
    while cur is None: r = sorted(rng.sample(range(1, m), 4)); cur = omega(r)
    for st in range(ST):
        r2 = list(r); a = rng.randrange(4); r2[a] = min(m-1, max(1, r2[a]+rng.choice([-3, -2, -1, 1, 2, 3, rng.randint(-m//4, m//4)])))
        if len(set(r2)) < 4: continue
        z = omega(r2)
        if z is not None and z[0] >= cur[0]: r, cur = r2, z
    if best is None or cur[0] > best[0][0]: best = (cur, r)
(Om, D, A, P), r = best; d = 4; M1 = m*(m-1)//2
S = min((d+1)*M1-sum((d+sum(y))*((sum(y[i]*P[i] for i in range(d))-sg) % m) for y in A) for sg in range(m))
Ct = (d+1)*m-Om*m
print("m=%d best Omega/m=%.3f r=%s height=%d t=%d MaxCL_ratio=%.3f" % (m, Om, r, max(sum(x) for x in D), len(A), S/(Ct*(m-1)/2)), flush=True)
