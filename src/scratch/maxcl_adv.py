# MaxCL on adversarial Apery tiles (same suite as tiletop_adv.py / E49)
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from exp_cl_adv import with_conductor
from srcl import tile_of
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); MMAX = int(sys.argv[3])
tests = []
for gens, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((17, 27, 28), 68),
                ((18, 28, 29), 72), ((30, 44, 48, 49), 118), ((23, 39, 40, 42), 77)]:
    tests.append(with_conductor(gens, c))
tests.append(NS.from_generators([213, 216, 226, 227]))
seen = set()
while len(tests) < N:
    m = rng.randint(6, MMAX); k = rng.randint(1, 15)
    if rng.random() < 0.5:
        base = rng.randint(m + 1, 3 * m)
        gens = sorted(set([m] + [base + rng.randint(0, max(1, m // 3)) for _ in range(k)]))
    else:
        gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4, 6]) * m) for _ in range(k)]))
    if reduce(gcd, gens) != 1: continue
    s0 = NS.from_generators(gens)
    for cc in sorted(set([s0.c] + [int(s0.c * f) for f in (0.2, 0.35, 0.5, 0.65, 0.8, 0.95)])):
        if cc <= m: continue
        s = s0 if cc == s0.c else with_conductor(gens, cc)
        key = (tuple(s.P), s.c)
        if key in seen: continue
        seen.add(key); tests.append(s)
f = 0; worst = None
for s in tests:
    cells, d = tile_of(s); m = s.m; S = set(cells)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    tr = [(d + sum(y), cells[y] % m) for y in A]
    w = max(sum(t*((r - sg) % m) for t, r in tr) for sg in range(m))
    v = (d+1)*m*(m-1)//2 - w
    if v < 0:
        f += 1
        if f <= 5: print('MaxCL FAIL', s.P[:10], s.c, 'm', m, 'd', d, 'v', v, 'Dep', d*m - sum(t for t, _ in tr))
    if worst is None or v/m**2 < worst[0]: worst = (v/m**2, v, s.P[:8], s.c)
print(len(tests), 'tiles; MaxCL fails', f, 'worst normalized', worst)
