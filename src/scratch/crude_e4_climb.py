# Hill-climb over 4-generated semigroups (m >= MMIN) to minimize the normalized crude slack CR/(4M').
# Moves: perturb one generator by +-1..+-m/3, or replace it.  Also tracks the true MaxCL slack at sigma = c mod m and min sigma.
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from math import gcd
from functools import reduce
from crude_e4 import crslack
def score(gens):
    if reduce(gcd, gens) != 1 or len(set(gens)) != 4: return None
    s = NS.from_generators(sorted(gens))
    if s.e != 4: return None
    cells, d = tile_of(s)
    if d != 3: return None
    sl = crslack(cells, d, s.m)
    return sl / (4*s.m*(s.m-1)/2), s, cells
rng = random.Random(int(sys.argv[1])); RUNS = int(sys.argv[2]); MMIN, MMAX = int(sys.argv[3]), int(sys.argv[4]); STEPS = int(sys.argv[5])
best_all = None; fails = []
for run in range(RUNS):
    m = rng.randint(MMIN, MMAX)
    while True:
        g = [m] + [rng.randint(m + 1, rng.choice([2, 3, 4])*m) for _ in range(3)]
        sc = score(g)
        if sc: break
    cur = sc
    for st in range(STEPS):
        h = list(g); i = rng.randint(1, 3)
        if rng.random() < 0.7: h[i] = max(m + 1, h[i] + rng.choice([-1, 1])*rng.randint(1, max(1, m//3)))
        else: h[i] = rng.randint(m + 1, 4*m)
        sc = score(h)
        if sc and sc[0] <= cur[0]: g, cur = h, sc
    s = cur[1]; cells = cur[2]
    S = set(cells); d = 3
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    tr = [(d + sum(y), cells[y] % s.m) for y in A]; M = s.m*(s.m-1)//2
    mx = [4*M - sum(t*((r - sg) % s.m) for t, r in tr) for sg in range(s.m)]
    row = (round(cur[0], 4), s.P, s.c, s.m, 'MaxCL min', round(min(mx)/(4*M), 4), 'at c', round(mx[s.c % s.m]/(4*M), 4))
    print(row, flush=True)
    if cur[0] < 0: fails.append(row)
    if best_all is None or cur[0] < best_all[0]: best_all = row
print('runs', RUNS, 'CR fails found', len(fails), 'best', best_all)
