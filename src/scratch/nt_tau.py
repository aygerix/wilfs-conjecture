# NON-two-face e = 4: does the sharp tau-criterion m + 1 >= 2 tau + P2 hold for m >= 20?
#   exh m0 m1 K : all <m,a,b,c>, m < a < b < c < K m
#   climb seed runs steps mlo mhi K : hill-climb max (2 tau + P2 - m - 1), generators < K m
import sys, itertools, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from tau_residual import analyse
def score(g):
    if reduce(gcd, g) != 1 or len(set(g)) != 4: return None
    s = NS.from_generators(sorted(g))
    if s.e != 4 or s.m != min(g): return None
    r = analyse(s)
    if r['two']: return None
    return 2*r['tau'] + r['P2'] - r['m'] - 1, r
if sys.argv[1] == 'exh':
    m0, m1, K = map(int, sys.argv[2:5])
    for m in range(m0, m1 + 1):
        worst = None; n = 0
        for g3 in itertools.combinations(range(m + 1, K*m), 3):
            sc = score((m,) + g3)
            if sc is None: continue
            n += 1
            if worst is None or sc[0] > worst[0]: worst = (sc[0], g3, sc[1]['tau'], sc[1]['P2'])
        print(f'm={m}: non-two-face e=4 {n}; max (2tau+P2-m-1) = {worst}', flush=True)
else:
    seed, runs, steps, mlo, mhi, K = map(int, sys.argv[2:8]); rng = random.Random(seed); best = None
    for run in range(runs):
        m = rng.randint(mlo, mhi); sc = None
        for _ in range(5000):
            g = [m] + [rng.randint(m + 1, K*m) for _ in range(3)]
            sc = score(g)
            if sc: break
        if not sc: continue
        for _ in range(steps):
            h = list(g); i = rng.randint(1, 3)
            h[i] = min(K*m, max(m + 1, h[i] + rng.choice([-3, -2, -1, 1, 2, 3, m, -m, rng.randint(-m, m)])))
            sc2 = score(h)
            if sc2 and sc2[0] >= sc[0]: g, sc = h, sc2
        print(f'run {run}: m={m} max(2tau+P2-m-1) {sc[0]} gens {sorted(g)} tau {sc[1]["tau"]} P2 {sc[1]["P2"]}', flush=True)
        if best is None or sc[0] > best[0]: best = (sc[0], sorted(g))
    print('BEST', best)
