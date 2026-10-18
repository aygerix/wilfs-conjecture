# Natural pairing for height<=3 tiles: y in level 3 -> uniform over its pairs (e_a, y-e_a) (weight 2 total);
# maximal y in level 2 -> its pair (e_a, e_b).  Exact identity: sum_A(|y|-1) r(y) = sum_z load(z) r(z) - H r(0) - m sum lam kappa.
# Test sufficient condition  S(sigma) := sum_z (load(z)-d-1) r(z) + m (B - P) <= (H+d+1) r(0)   for all sigma,
# and report max pointwise load / (d+1).  Sources: random semigroups with height-3 grlex tiles.
import sys, random
from fractions import Fraction as Fr
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from math import gcd
from functools import reduce
def unit(a, d): return tuple(int(i == a) for i in range(d))
def check(cells, d, m):
    S = set(cells)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    pairs = []   # (y, u, v, weight)
    for y in A:
        h = sum(y)
        if h == 2:
            a = [i for i in range(d) if y[i] > 0]
            u = unit(a[0], d); v = tuple(p - q for p, q in zip(y, u)); pairs.append((y, u, v, Fr(1)))
        elif h == 3:
            dirs = [a for a in range(d) if y[a] > 0]
            for a in dirs:
                u = unit(a, d); v = tuple(p - q for p, q in zip(y, u)); pairs.append((y, u, v, Fr(2, len(dirs))))
    load = {}
    for y, u, v, w in pairs:
        load[u] = load.get(u, 0) + w; load[v] = load.get(v, 0) + w
    H = sum(sum(y) - 1 for y in A)
    zero = tuple([0]*d)
    worst = None
    for sg in range(m):
        r = {x: (cells[x] - sg) % m for x in cells}
        val = sum((load.get(z, 0) - d - 1)*r[z] for z in cells if z not in A and z != zero)
        for y, u, v, w in pairs:
            k = (r[u] + r[v] - r[y] - r[zero]) // m
            val -= m*w*k
        slack = (H + d + 1)*r[zero] - val
        if worst is None or slack < worst[0]: worst = (slack, sg)
    maxload = max(load.values()) if load else 0
    return worst, Fr(maxload) / (d + 1)
rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2])
found = fails = 0; tries = 0; mlmax = 0; worst = None
while found < NT and tries < 1000000:
    tries += 1
    m = rng.randint(8, 60); e = rng.randint(3, max(4, m//3))
    lo = rng.choice([1, 2, 3])*m; spread = rng.choice([m//3, m//2, m, 2*m])
    gens = sorted(set([m] + [lo + rng.randint(1, spread) for _ in range(e - 1)]))
    if reduce(gcd, gens) != 1: continue
    s = NS.from_generators(gens)
    cells, d = tile_of(s)
    if max(sum(x) for x in cells) != 3: continue
    found += 1
    (sl, sg), ml = check(cells, d, s.m)
    mlmax = max(mlmax, ml)
    if sl < 0:
        fails += 1
        if fails <= 4: print('FAIL', s.P, 'm', s.m, 'd', d, 'sigma', sg, 'slack', sl, 'maxload/(d+1)', float(ml), flush=True)
    if worst is None or sl < worst[0]: worst = (sl, s.P[:6])
print('height-3 tiles', found, '; natural-scheme failures', fails, '; max load/(d+1)', float(mlmax), '; worst', worst)
