# Height-3 tiles: is |T| + |E^A| <= d(d+1)/2 (necessary for a one-level geometric Load scheme at height 3)?
# T = level-3 cells, E^A = maximal level-2 cells, d counts all directions (spikes included).
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from math import gcd
from functools import reduce
rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); DLO, DHI = int(sys.argv[3]), int(sys.argv[4])
found = 0; tries = 0; worst = None; over = 0
while found < NT and tries < 40000:
    tries += 1
    d = rng.randint(DLO, DHI); m = rng.randint(max(d + 2, d**3 // 10), d**3 // 4 + d)
    k = rng.randint(4, 7); res = rng.sample(range(1, m), d)
    gens = sorted([m] + [k*m + r for r in res])
    if reduce(gcd, gens) != 1: continue
    s = NS.from_generators(gens)
    if s.e != d + 1: continue
    cells, dd = tile_of(s)
    if max(sum(x) for x in cells) != 3: continue
    found += 1
    S = set(cells)
    A = set(y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(dd)))
    T = sum(1 for x in cells if sum(x) == 3); EA = sum(1 for x in A if sum(x) == 2)
    ratio = (T + EA) / (dd*(dd+1)/2)
    if ratio > 1: over += 1
    if worst is None or ratio > worst[0]: worst = (round(ratio, 3), dd, s.m, T, EA, s.P[:4])
print('height-3 tiles', found, 'with |T|+|E^A| > d(d+1)/2:', over, 'max ratio', worst)
