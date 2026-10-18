# Search height<=2 semigroups (Ap within {0} u P u (P+P)) not covered by any implemented known Wilf condition.
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from known import known_wilf
from math import gcd
from functools import reduce
rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2])
found = 0; new = []; tries = 0; cov = {}
while found < NT and tries < 2000000:
    tries += 1
    m = rng.randint(20, 70); e = rng.randint(max(4, int((2*m)**0.5)), max(5, m//3))
    lo = rng.choice([1, 2, 3])*m; spread = rng.choice([m//2, m, 2*m, 3*m])
    gens = sorted(set([m] + [lo + rng.randint(1, spread) for _ in range(e - 1)]))
    if reduce(gcd, gens) != 1: continue
    s = NS.from_generators(gens)
    if s.e < 4 or 3*s.e >= s.m: continue
    cells, d = tile_of(s)
    if max(sum(x) for x in cells) > 2: continue
    found += 1
    kw = known_wilf(s)
    for k in kw: cov[k] = cov.get(k, 0) + 1
    if not kw:
        new.append((s.P, s.c, s.q, s.e, s.t(), s.W))
        print('NOT COVERED:', s.P, 'm', s.m, 'c', s.c, 'q', s.q, 'e', s.e, 't', s.t(), 'g', s.g, 'W', s.W, flush=True)
print('height<=2 S with 3e<m:', found, 'tries', tries, '; not covered by known conditions:', len(new))
print('coverage counts:', sorted(cov.items(), key=lambda kv: -kv[1]))
