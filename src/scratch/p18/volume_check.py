"""Sanity check of the cube-volume near-Wilf inequality, for random S:
   e*ell >= q*m * (1 + (m - 1 + N)/(q*m))^{-(e-1)} - e*rho, with N = sum of the non-m minimal generators,
   and the stronger per-band form u_t >= m * ((t+1) m / L0)^{e-1}, L0 = c + m - 1 + N.
usage: python volume_check.py seed trials"""
import sys, random, math
sys.path.insert(0, '../nowrap')
from pmin_tile import apery, minimal_gens
rng = random.Random(int(sys.argv[1])); T = int(sys.argv[2]); bad = 0; worst = None; tot = 0
for _ in range(T):
    m = rng.randint(5, 120); kk = rng.randint(1, 6)
    gens = sorted(set(rng.randint(m + 1, rng.choice([2, 3, 6]) * m) for _ in range(kk)))
    if math.gcd(m, *gens) != 1: continue
    ap = apery(m, gens)
    if None in ap: continue
    n, ap = minimal_gens(m, gens); e = len(n) + 1; d = e - 1
    c = max(ap) - m + 1
    if c <= m: continue
    tot += 1
    g = sum(w // m for w in ap); ell = c - g; q = -(-c // m); rho = q * m - c; N = sum(n)
    L0 = c + m - 1 + N
    for t in range(q):
        u = sum(1 for w in ap if w < (t + 1) * m)
        if u < m * ((t + 1) * m / L0) ** d - 1e-9: bad += 1
    rhs = q * m * (1 + (m - 1 + N) / (q * m)) ** (-d) - e * rho
    if e * ell < rhs - 1e-9: bad += 1
    r = e * ell / max(rhs, 1e-9)
    if worst is None or r < worst[0]: worst = (round(r, 4), m, n, c, e)
print("tested", tot, "violations", bad, "min e*ell/rhs", worst)
