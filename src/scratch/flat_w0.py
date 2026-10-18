# Height<=2 semigroups: distribution of W0 (Eliahou); find W0 < 0 and record coverage by known conditions.
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from known import known_wilf
from math import gcd
from functools import reduce
rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2])
found = 0; neg = []; tries = 0; uncovered = 0
while found < NT and tries < 3000000:
    tries += 1
    m = rng.randint(10, 70); e = rng.randint(4, max(5, m//2))
    lo = rng.choice([1, 2, 3, 4])*m; spread = rng.choice([m//3, m//2, m, 2*m, 3*m])
    gens = sorted(set([m] + [lo + rng.randint(1, spread) for _ in range(e - 1)]))
    if reduce(gcd, gens) != 1: continue
    s = NS.from_generators(gens)
    if s.e < 4 or s.q < 4: continue
    cells, d = tile_of(s)
    if max(sum(x) for x in cells) > 2: continue
    found += 1
    w0 = s.W0()
    kw = known_wilf(s)
    if not kw: uncovered += 1
    if w0 < 0:
        neg.append((s.P, s.c, s.q, s.e, s.t(), w0, s.W, kw))
        if len(neg) <= 6: print('W0<0:', s.P, 'm', s.m, 'c', s.c, 'q', s.q, 'e', s.e, 'W0', w0, 'W', s.W, 'known:', kw, flush=True)
print('height<=2, q>=4 semigroups:', found, '; W0<0:', len(neg), '; uncovered by known conditions:', uncovered)
