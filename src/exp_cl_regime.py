"""E48: CL / Tile-CL split by regime: does every failure have 3e >= m (covered by Eliahou EJC 2020)?
Random semigroups (seeded) with few generators relative to m, plus truncations <A> u [c', oo) at every
depth; reports failures separately for 3e < m and 3e >= m, and for the CL reference residue vs other s."""
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from exp_cl_adv import tile_slack, with_conductor

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
MMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 90
stats = {'small_e': [0, 0, 0], 'large_e': [0, 0, 0]}   # [tested, CL fails (ref s), Tile-CL fails (some s)]
ex = {'small_e': None, 'large_e': None}
seen = set(); count = 0
while count < N:
    m = rng.randint(6, MMAX)
    kmax = max(1, (m - 1) // 3 - 1)
    k = rng.randint(1, min(kmax, 12))
    lo = m + 1; hi = rng.choice([2 * m, 3 * m, 4 * m, 6 * m])
    mode = rng.random()
    if mode < 0.4:      # clustered generators (Eliahou-like): near a multiple of m
        base = rng.randint(m + 1, 3 * m)
        gens = sorted(set([m] + [base + rng.randint(0, max(1, m // 4)) for _ in range(k)]))
    else:
        gens = sorted(set([m] + [rng.randint(lo, hi) for _ in range(k)]))
    if reduce(gcd, gens) != 1:
        continue
    s0 = NS.from_generators(gens)
    cands = [s0]
    for frac in (0.25, 0.4, 0.55, 0.7, 0.85):
        cc = int(s0.c * frac)
        if cc > 3 * m:
            cands.append(with_conductor(gens, cc))
    for s in cands:
        key = (tuple(s.P), s.c)
        if key in seen: continue
        seen.add(key); count += 1
        reg = 'small_e' if 3 * s.e < s.m else 'large_e'
        d, sl = tile_slack(s)
        sref = (s.c + s.m - 1) % s.m
        st = stats[reg]; st[0] += 1
        if sl[sref] < 0:
            st[1] += 1
            if ex[reg] is None or s.m < ex[reg][0]: ex[reg] = (s.m, s.e, s.c, s.P, sl)
        if min(sl) < 0 or max(sl) > s.m - 1:
            st[2] += 1
print('stats [tested, CL fails, Tile-CL fails]:', stats)
print('smallest-m CL failure per regime:', ex)
