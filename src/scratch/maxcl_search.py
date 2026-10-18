# Hill-climb within the open Wilf regime (q>=4, 3e<m, t>=e, m>=20) to minimize normalized MaxCL slack (min over sigma)
# and, separately, MaxCL slack at sigma = c (the Wilf-relevant rotation).
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from math import gcd
from functools import reduce
from crude_open import is_open
rng = random.Random(int(sys.argv[1])); ITER = int(sys.argv[2]); RESTARTS = int(sys.argv[3]); MLO, MHI = int(sys.argv[4]), int(sys.argv[5])
MODE = sys.argv[6]  # 'min' or 'ref'
def maxcl(s):
    cells, d = tile_of(s); m = s.m; S = set(cells)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    M = m*(m-1)//2; tr = [(d + sum(y), cells[y] % m) for y in A]
    if MODE == 'ref': sigs = [s.c % m]
    else: sigs = range(m)
    v = min((d+1)*M - sum(t*((r - sg) % m) for t, r in tr) for sg in sigs)
    return v / ((d+1)*M)
def score(gens):
    gens = sorted(set(gens))
    if len(gens) < 4 or reduce(gcd, gens) != 1 or gens[1] <= gens[0]: return None
    try: s = NS.from_generators(gens)
    except Exception: return None
    if s.c > 4000 or not is_open(s): return None
    return maxcl(s), s
best_all = None
for rs in range(RESTARTS):
    while True:
        m = rng.randint(MLO, MHI); e = rng.randint(4, max(4, m//3 - 1)); k = rng.choice([1, 2, 3])
        gens = sorted(set([m] + [k*m + rng.randint(1, m - 1) for _ in range(e - 1)]))
        sc = score(gens)
        if sc: break
    cur, s = sc; curg = list(s.P)
    for it in range(ITER):
        g = list(curg); op = rng.random(); i = rng.randrange(1, len(g))
        if op < 0.5: g[i] += rng.choice([-2, -1, 1, 2])
        elif op < 0.65: g[i] += rng.choice([-1, 1]) * g[0]
        elif op < 0.8 and len(g) > 4: g.pop(i)
        else: g.append(rng.randint(g[0] + 1, 3*g[0]))
        if min(g[1:]) <= g[0]: continue
        sc = score(g)
        if sc and sc[0] <= cur: cur, s = sc; curg = list(s.P)
    print('restart', rs, 'best', round(cur, 4), s.P, 'c', s.c, 'q', s.q, 'e', s.e, 't', s.t(), 'W', s.W, flush=True)
    if best_all is None or cur < best_all[0]: best_all = (cur, s.P, s.c)
print('overall', best_all)
