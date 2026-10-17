"""E6: TOP'' on adversarial / random deep semigroups (exact)."""
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from top2 import top2

def with_conductor(gens, c):
    return NS.from_generators(list(gens) + list(range(c, c + min(gens))))

tests = []
for gens, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((17, 27, 28), 68),
                ((18, 28, 29), 72), ((30, 44, 48, 49), 118), ((23, 39, 40, 42), 77)]:
    tests.append(('W0<0', with_conductor(gens, c)))
tests.append(('Backelin', NS.from_generators([213, 216, 226, 227])))
for mu, gam, p in [(10, 13, 5), (12, 17, 6), (15, 19, 7), (20, 27, 8), (25, 32, 9)]:
    tests.append(('Delgado', with_conductor((mu, gam, gam + 1), p * mu)))
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
while len(tests) < N:
    m = rng.randint(5, 60)
    k = rng.randint(1, 7)
    hi = rng.choice([2 * m, 3 * m, 5 * m, 10 * m])
    gens = sorted(set([m] + [rng.randint(m + 1, hi) for _ in range(k)]))
    if reduce(gcd, gens) != 1:
        continue
    s = NS.from_generators(gens)
    tests.append(('rand', s))
    for frac in (0.3, 0.5, 0.7, 0.9):
        cc = int(s.c * frac)
        if cc > m:
            tests.append(('trunc', with_conductor(gens, cc)))
fails = 0
minslack = None
for name, s in tests:
    lhs2, rhs = top2(s)
    if lhs2 > rhs:
        fails += 1
        print('FAIL', name, s.summary())
    sl = (rhs - lhs2) / (s.m * s.m)
    if s.W > 0 and (minslack is None or sl < minslack[0]):
        minslack = (sl, name, s.P, s.c, s.W)
print(len(tests), 'tests; fails', fails, '; min normalized slack (W>0):', minslack)
