# adversarial hill-climb: minimize H(D) - (m-1) over NON-two-face e = 4 tiles.  usage: seed runs steps mlo mhi K
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from cl import factorizations_down_set
from heightH import H_of
def score(g):
    if reduce(gcd, g) != 1 or len(set(g)) != 4: return None
    s = NS.from_generators(sorted(g))
    if s.e != 4 or s.m != min(g): return None
    p, best = factorizations_down_set(s, 'grlex'); D = set(best.values())
    if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): return None
    return H_of(D) - (s.m - 1)
seed, runs, steps, mlo, mhi, K = map(int, sys.argv[1:7]); rng = random.Random(seed); best = None
for run in range(runs):
    m = rng.randint(mlo, mhi); sc = None
    for _ in range(20000):
        g = [m] + [rng.randint(m + 1, K*m) for _ in range(3)]
        sc = score(g)
        if sc is not None: break
    if sc is None: continue
    for _ in range(steps):
        h = list(g); i = rng.randint(1, 3)
        h[i] = min(K*m, max(m + 1, h[i] + rng.choice([-3, -2, -1, 1, 2, 3, m, -m, rng.randint(-m, m)])))
        sc2 = score(h)
        if sc2 is not None and sc2 <= sc: g, sc = h, sc2
    print(f'run {run}: m={m} H-(m-1) = {sc}  gens {sorted(g)}', flush=True)
    if best is None or sc < best[0]: best = (sc, sorted(g))
print('BEST', best)
