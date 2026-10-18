# Hill-climb e = 4 semigroups to maximize tau / sqrt(m) (tau = #gaps in [c-m,c)); generators up to G*m.
import sys, random
from math import gcd, sqrt
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
def score(g):
    if reduce(gcd, g) != 1: return None
    s = NS.from_generators(g)
    if s.e != 4: return None
    c = s.c; tau = sum(1 for u in s.apery() if c <= u < c + s.m)
    return tau/sqrt(s.m), tau, s.t(), s.P
rng = random.Random(int(sys.argv[1])); R = int(sys.argv[2]); STEPS = int(sys.argv[3]); MLO, MHI, G = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
best_all = None
for r in range(R):
    m = rng.randint(MLO, MHI)
    while True:
        g = sorted(set([m] + [rng.randint(m + 1, G*m) for _ in range(3)]))
        if len(g) == 4 and score(g): break
    cur = score(g)
    for st in range(STEPS):
        h = list(g); i = rng.randint(1, 3); h[i] = max(m + 1, h[i] + rng.choice([-1, 1])*rng.randint(1, max(1, m//4)))
        if rng.random() < 0.1: h[0] = m  # keep m
        h = sorted(set(h))
        if len(h) != 4 or h[0] != m: continue
        sc = score(h)
        if sc and sc[0] >= cur[0]: g, cur = h, sc
    print(f'run {r}: m={m} tau/sqrt(m)={cur[0]:.3f} tau={cur[1]} t={cur[2]} P={cur[3]}', flush=True)
    if best_all is None or cur[0] > best_all[0]: best_all = cur
print('BEST', best_all)
