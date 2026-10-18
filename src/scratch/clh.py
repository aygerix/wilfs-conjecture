# CL-H: CL slack(M mod m) + d_high*(ell - q) >= 0 ?  (high generators n_b >= c counted exactly; q = ceil(c/m))
# Also: do all CL(ref) failures have high generators?  Seeded random/adversarial suite as in E47/E49.
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from exp_cl_adv import tile_slack, with_conductor
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); MMAX = int(sys.argv[3])
tests = []
for gens, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((17, 27, 28), 68),
                ((18, 28, 29), 72), ((30, 44, 48, 49), 118), ((23, 39, 40, 42), 77)]:
    tests.append(with_conductor(gens, c))
seen = set()
while len(tests) < N:
    m = rng.randint(6, MMAX); k = rng.randint(1, 15)
    if rng.random() < 0.5:
        base = rng.randint(m + 1, 3 * m)
        gens = sorted(set([m] + [base + rng.randint(0, max(1, m // 3)) for _ in range(k)]))
    else:
        gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4, 6]) * m) for _ in range(k)]))
    if reduce(gcd, gens) != 1: continue
    s0 = NS.from_generators(gens)
    for cc in sorted(set([s0.c] + [int(s0.c * f) for f in (0.2, 0.35, 0.5, 0.65, 0.8, 0.95)])):
        if cc <= m: continue
        s = s0 if cc == s0.c else with_conductor(gens, cc)
        key = (tuple(s.P), s.c)
        if key in seen: continue
        seen.add(key); tests.append(s)
clf = clhf = 0; nohigh = 0; minclh = None
for s in tests:
    d, sl = tile_slack(s)
    sref = sl[(s.c + s.m - 1) % s.m]
    dh = sum(1 for p in s.P if p >= s.c)
    q = -(-s.c // s.m)
    if sref < 0:
        clf += 1
        if dh == 0: nohigh += 1; print('CL fail without high gens', s.P, s.c)
    v = sref + dh * (s.ell - q)
    if v < 0: clhf += 1; print('CL-H FAIL', s.P, s.c, sref, dh, s.ell, q)
    if minclh is None or v < minclh[0]: minclh = (v, s.P[:6], s.c, s.W)
print(len(tests), 'S; CL(ref) fails', clf, '(without high gens:', nohigh, '); CL-H fails', clhf, '; min CL-H value', minclh)
