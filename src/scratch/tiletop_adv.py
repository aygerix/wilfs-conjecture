# Tile-TOP'' (all s) and R-TOP (rearranged, residue-free: weights d+|y| of maximal cells sorted decreasingly,
# paired with m, m-1, ...) on Apery tiles of the seeded adversarial suite.
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from srcl import tile_of
import random
from math import gcd
from functools import reduce
from ns import NS
from exp_cl_adv import with_conductor
def check(cells, d, m):
    S = set(cells)
    res = {y: w % m for y, w in cells.items()}
    maxc = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    rhs2 = m*((d+1)*m + d - 1)
    best = None
    for s in range(m):
        lhs = sum((d + sum(y))*(m - (s - res[y]) % m) for y in maxc)
        v = rhs2 - 2*lhs
        best = v if best is None or v < best else best
    w = sorted((d + sum(y) for y in maxc), reverse=True)
    rl = sum(wi*(m - i) for i, wi in enumerate(w))
    return best, rhs2 - 2*rl, len(maxc)
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); MMAX = int(sys.argv[3])
tests = []
for gens, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((17, 27, 28), 68),
                ((18, 28, 29), 72), ((30, 44, 48, 49), 118), ((23, 39, 40, 42), 77)]:
    tests.append(with_conductor(gens, c))
tests.append(NS.from_generators([213, 216, 226, 227]))
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
ft = fr = 0; wt = wr = None
for s in tests:
    cells, d = tile_of(s)
    a, b, na = check(cells, d, s.m)
    ft += a < 0; fr += b < 0
    if wt is None or a/s.m**2 < wt[0]: wt = (a/s.m**2, a, s.P[:6], s.c, na)
    if wr is None or b/s.m**2 < wr[0]: wr = (b/s.m**2, b, s.P[:6], s.c, na)
    if b < 0 and fr <= 3: print('R-TOP fail', s.P, s.c, 'maxcells', na, 'v', b)
print(len(tests), 'tiles; Tile-TOP2 fails', ft, 'worst', wt, '; R-TOP fails', fr, 'worst', wr)
