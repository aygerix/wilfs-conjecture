# count condition of the Load Lemma: sum_{y max}2(|y|-1) <= (d+1)(|N|-1)  (N = non-maximal, incl. 0)
# on adversarial Apery tiles + random 4/5-generated semigroups
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from exp_cl_adv import with_conductor
from srcl import tile_of
rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); MMAX = int(sys.argv[3])
tests = []
for gens, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((17, 27, 28), 68),
                ((18, 28, 29), 72), ((30, 44, 48, 49), 118), ((23, 39, 40, 42), 77)]:
    tests.append(with_conductor(gens, c))
tests.append(NS.from_generators([213, 216, 226, 227]))
while len(tests) < NT:
    m = rng.randint(6, MMAX); k = rng.randint(1, 15)
    if rng.random() < 0.3:
        gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4]) * m) for _ in range(rng.choice([3, 4]))]))
    elif rng.random() < 0.5:
        base = rng.randint(m + 1, 3 * m)
        gens = sorted(set([m] + [base + rng.randint(0, max(1, m // 3)) for _ in range(k)]))
    else:
        gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4, 6]) * m) for _ in range(k)]))
    if reduce(gcd, gens) != 1: continue
    s0 = NS.from_generators(gens)
    tests.append(s0)
    for f in (0.3, 0.6, 0.9):
        cc = int(s0.c * f)
        if cc > m: tests.append(with_conductor(gens, cc))
f = 0; worst = None
for s in tests:
    cells, d = tile_of(s); S = set(cells)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    nN = len(cells) - len(A)
    v = (d+1)*(nN - 1) - sum(2*(sum(y) - 1) for y in A)
    if v < 0:
        f += 1
        if f <= 5: print('count FAIL', s.P[:8], s.c, 'm', s.m, 'd', d, 'type', len(A), 'v', v)
    if worst is None or v < worst[0]: worst = (v, s.P[:6], s.c, len(A))
print(len(tests), 'tiles; count-condition fails', f, 'worst', worst)
