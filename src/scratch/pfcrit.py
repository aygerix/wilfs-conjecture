# PF-length criterion: Wilf holds if T(A) := sum_{y maximal in grlex tile}(d + |y|) <= (d+1) m / 2  (trivial MaxCL).
# Coverage vs known_wilf and Eliahou's W0 on random semigroups in the open regime.
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from known import known_wilf
from srcl import tile_of
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); E = int(sys.argv[3]); MLO, MHI = int(sys.argv[4]), int(sys.argv[5])
stats = dict(sampled=0, open_q4=0, uncovered=0, W0neg=0, crit=0, crit_uncov=0, crit_W0neg_uncov=0)
ex = []
while stats['sampled'] < N:
    m = rng.randint(MLO, MHI)
    k = rng.choice([2, 3, 4, 5, 6, 8])
    gens = sorted(set([m] + [rng.randint(m + 1, k*m) for _ in range(E - 1)]))
    if len(gens) != E or reduce(gcd, gens) != 1: continue
    s = NS.from_generators(gens)
    if s.e != E or s.m != m: continue
    stats['sampled'] += 1
    if s.q < 4: continue
    stats['open_q4'] += 1
    cells, d = tile_of(s)
    A = [y for y in cells if all(tuple(y[:a]) + (y[a]+1,) + tuple(y[a+1:]) not in cells for a in range(d))]
    TA = sum(d + sum(y) for y in A)
    ok = 2*TA <= (d+1)*m
    w0 = s.W0()
    kw = [k for k in known_wilf(s) if not k.startswith('c<=4n')] + (['W0>=0 (Eliahou)'] if w0 >= 0 else [])
    stats['crit'] += ok
    if w0 < 0: stats['W0neg'] += 1
    if not kw:
        stats['uncovered'] += 1
        if ok: stats['crit_uncov'] += 1
        if ok and w0 < 0:
            stats['crit_W0neg_uncov'] += 1
            if len(ex) < 5: ex.append((s.P, s.m, s.c, s.g, s.t(), TA))
print(stats)
for e_ in ex: print('  new (uncovered, W0<0, criterion holds):', e_)
