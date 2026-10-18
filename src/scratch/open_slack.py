# Slack of Wilf in the open range 3e < m, c > 3m: min e*ell/c, min W/m, and how often the tau-criterion already applies.
import sys, random, time
sys.path.insert(0, 'src')
from math import gcd
from functools import reduce
from ns import NS
e0, e1, seed, budget = map(int, sys.argv[1:5])
rnd = random.Random(seed); t0 = time.time(); st = {}
while time.time() - t0 < budget:
    e = rnd.randint(e0, e1); m = rnd.randint(3 * e + 1, max(3 * e + 2, 90)); K = rnd.choice((2, 3, 4, 6, 10))
    g = sorted(rnd.sample(range(m + 1, K * m), e - 1))
    if reduce(gcd, [m] + g) != 1: continue
    s = NS.from_generators([m] + g)
    if s.e != e or s.m != m or s.c <= 3 * s.m: continue
    ap = s.apery(); c = s.c; tau = sum(1 for w in ap if w >= c)
    tauok = (e - 2) * (m + 1) >= tau * (tau + 2 * e - 5)
    r = st.setdefault(e, [0, 0, None, None])
    r[0] += 1; r[1] += tauok
    q = e * s.ell / c
    if r[2] is None or q < r[2][0]: r[2] = (round(q, 3), [m] + g, c, tau)
    if r[3] is None or s.W / m < r[3][0]: r[3] = (round(s.W / m, 2), [m] + g, c, tau)
print(f'seed {seed} {time.time()-t0:.0f}s')
for e in sorted(st):
    n, k, a, b = st[e]
    print(f' e={e}: {n} S; tau-criterion applies {k}; min e*ell/c {a}; min W/m {b}')
