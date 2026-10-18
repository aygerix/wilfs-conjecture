# Height <= 2 tiles (reduction number <= 2: Ap(S,m) within {0} u P u (P+P)).  (1) verify the Flat-MaxCL proof steps
# (deg <= d+1, B <= r(0), MaxCL) for every sigma; (2) count how many such S lie in the open Wilf regime.
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from math import gcd
from functools import reduce
from crude_open import is_open
rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2])
found = nopen = bad = 0; ex = []
tries = 0
while found < NT and tries < 400000:
    tries += 1
    m = rng.randint(8, 60); k = rng.choice([1, 2, 3, 4]); e = rng.randint(3, max(3, m//2))
    gens = sorted(set([m] + [k*m + rng.randint(1, m - 1) for _ in range(e - 1)] + ([rng.randint(m+1, 2*m)] if rng.random() < 0.3 else [])))
    if reduce(gcd, gens) != 1: continue
    s = NS.from_generators(gens)
    cells, d = tile_of(s)
    if max(sum(x) for x in cells) > 2: continue
    found += 1
    S = set(cells); M = s.m*(s.m - 1)//2; m = s.m
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    deg = [sum((y[a] if sum(y) == 2 else 0) for y in A) for a in range(d)]
    assert max(deg) <= d + 1
    for sg in range(m):
        r = {x: (cells[x] - sg) % m for x in cells}
        B = sum(1 for y in A if sum(y) == 2 and
                sum(r[tuple(int(i == a) for i in range(d))] for a in range(d) for _ in range(y[a])) == r[y] + r[tuple([0]*d)] - m)
        assert B <= r[tuple([0]*d)], (gens, sg)
        v = (d+1)*sum(r[x] for x in cells if x not in A) - sum((sum(y)-1)*r[y] for y in A)
        if v < 0: bad += 1
    if is_open(s):
        nopen += 1
        if len(ex) < 6: ex.append((s.P, s.c, s.q, s.e, s.t(), s.W))
print('height<=2 semigroups', found, 'in', tries, 'tries; MaxCL violations', bad, '; in open Wilf regime:', nopen)
for x in ex: print('  open-regime example', x)
