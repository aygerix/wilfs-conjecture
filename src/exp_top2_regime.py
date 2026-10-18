"""E49: TOP'' (top-layer inequality, Lemma A + TOP'' => Wilf) on the harder generators of E47/E48
(clustered generators near multiples of m, every-depth truncations, m up to MMAX, up to 15 extra generators).
Also records CL at the reference residue for comparison. Seeded."""
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from top2 import top2
from exp_cl_adv import tile_slack, with_conductor

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
MMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 90
tests = []
for gens, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((17, 27, 28), 68),
                ((18, 28, 29), 72), ((30, 44, 48, 49), 118), ((23, 39, 40, 42), 77)]:
    tests.append(('W0<0', with_conductor(gens, c)))
tests.append(('Backelin', NS.from_generators([213, 216, 226, 227])))
seen = set()
while len(tests) < N:
    m = rng.randint(6, MMAX)
    k = rng.randint(1, 15)
    if rng.random() < 0.5:
        base = rng.randint(m + 1, 3 * m)
        gens = sorted(set([m] + [base + rng.randint(0, max(1, m // 3)) for _ in range(k)]))
    else:
        gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4, 6]) * m) for _ in range(k)]))
    if reduce(gcd, gens) != 1:
        continue
    s0 = NS.from_generators(gens)
    for cc in sorted(set([s0.c] + [int(s0.c * f) for f in (0.2, 0.35, 0.5, 0.65, 0.8, 0.95)])):
        if cc <= m: continue
        s = s0 if cc == s0.c else with_conductor(gens, cc)
        key = (tuple(s.P), s.c)
        if key in seen: continue
        seen.add(key); tests.append(('gen', s))
fails = 0; clf = 0; both = 0; minsl = None
for name, s in tests:
    lhs2, rhs = top2(s)
    d, sl = tile_slack(s)
    clfail = sl[(s.c + s.m - 1) % s.m] < 0
    clf += clfail
    if lhs2 > rhs:
        fails += 1; both += clfail
        print('TOP2 FAIL', name, s.P, s.c, 'W', s.W)
    if s.W > 0:
        v = (rhs - lhs2) / (s.m * s.m)
        if minsl is None or v < minsl[0]: minsl = (v, s.P[:8], s.c, s.W)
print(len(tests), 'tests; TOP2 fails', fails, '; CL(ref) fails', clf, '; both', both, '; min normalized TOP2 slack (W>0)', minsl)
