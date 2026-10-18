# Hill-climb max T(A)/m over e=4 grlex tiles that are NOT two-face (all e_a+e_b in D); report also CR slack.
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from crude_e4 import crslack
from twoface_census import twoface_info, rand_gens
from heavy3 import shape
from math import gcd
from functools import reduce
def score(g):
    if reduce(gcd, g) != 1 or len(set(g)) != 4: return None
    s = NS.from_generators(sorted(g))
    if s.e != 4: return None
    cells, d = tile_of(s)
    if twoface_info(cells, s.m): return None
    sh = shape(list(cells), 3, s.m)
    return sh['TA'] / s.m, s, sh, crslack(list(cells), 3, s.m)
rng = random.Random(int(sys.argv[1])); RUNS, MMIN, MMAX, STEPS = map(int, sys.argv[2:6])
for run in range(RUNS):
    while True:
        g = rand_gens(rng, MMIN, MMAX); cur = score(g)
        if cur: break
    m = g[0]
    for st in range(STEPS):
        h = list(g); i = rng.randint(1, 3)
        if rng.random() < 0.7: h[i] = max(m + 1, h[i] + rng.choice([-1, 1])*rng.randint(1, max(1, m//3)))
        else: h[i] = rng.randint(m + 1, 4*m)
        sc = score(h)
        if sc and sc[0] >= cur[0]: g, cur = h, sc
    s, sh = cur[1], cur[2]
    print('T(A)/m', round(cur[0], 3), s.P, 'm', s.m, 'nA', sh['nA'], 'h', sh['h'], 'ext', sh['ext'], 'CR norm', round(cur[3]/(2*s.m*(s.m-1)), 4), flush=True)
