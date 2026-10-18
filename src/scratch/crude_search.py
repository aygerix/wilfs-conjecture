# Hill-climb within the open Wilf regime (q>=4, 3e<m, t>=e, m>=20) to minimize the normalized crude slack.
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from math import gcd
from functools import reduce
from crude_open import crude_ok, is_open
rng = random.Random(int(sys.argv[1])); ITER = int(sys.argv[2]); RESTARTS = int(sys.argv[3])
def score(gens):
    if reduce(gcd, gens) != 1 or len(set(gens)) != len(gens): return None
    try: s = NS.from_generators(sorted(gens))
    except Exception: return None
    if s.c > 3000 or not is_open(s): return None
    v, d, nA, TA = crude_ok(s)
    return v / ((d+1)*s.m*(s.m-1)/2), s
best_all = None
for rs in range(RESTARTS):
    while True:
        m = rng.randint(20, 60); e = rng.randint(4, max(4, m//3 - 1)); k = rng.choice([1, 2, 3])
        gens = sorted(set([m] + [k*m + rng.randint(1, m - 1) for _ in range(e - 1)]))
        sc = score(gens)
        if sc: break
    cur, s = sc; curg = gens
    for it in range(ITER):
        g = list(curg); op = rng.random()
        i = rng.randrange(1, len(g))
        if op < 0.5: g[i] += rng.choice([-2, -1, 1, 2])
        elif op < 0.65: g[i] += rng.choice([-1, 1]) * g[0]
        elif op < 0.8 and len(g) > 4: g.pop(i)
        else: g.append(rng.randint(g[0] + 1, 3*g[0]))
        if min(g[1:]) <= g[0]: continue
        sc = score(g)
        if sc and sc[0] <= cur:
            cur, s = sc; curg = sorted(g)
    print('restart', rs, 'best', round(cur, 4), s.P, 'c', s.c, 'q', s.q, 'e', s.e, 't', s.t(), flush=True)
    if best_all is None or cur < best_all[0]: best_all = (cur, s.P, s.c)
print('overall', best_all)
