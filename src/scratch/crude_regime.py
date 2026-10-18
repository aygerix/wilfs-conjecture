# Regime split for MaxCL: crude rearrangement bound  sum_i T_(i) (m - i) <= (d+1)M'  (T sorted decreasing) proves MaxCL
# without residues.  Report how often it fails, and for failures: T(A)/(dm), |A|, Dep, actual MaxCL slack, Wilf-known flags.
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from exp_cl_adv import with_conductor
from srcl import tile_of
from math import gcd
from functools import reduce
rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); MMAX = int(sys.argv[3])
tests = []
while len(tests) < NT:
    m = rng.randint(6, MMAX); k = rng.randint(2, 12)
    if rng.random() < 0.5:
        base = rng.randint(m + 1, 3*m); gens = sorted(set([m] + [base + rng.randint(0, max(1, m//3)) for _ in range(k)]))
    else:
        gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4])*m) for _ in range(k)]))
    if reduce(gcd, gens) != 1: continue
    s0 = NS.from_generators(gens); tests.append(s0)
    for fr in (0.4, 0.7):
        if int(s0.c*fr) > m: tests.append(with_conductor(gens, int(s0.c*fr)))
n = crude_fail = 0; hard = []
for s in tests:
    cells, d = tile_of(s); m = s.m; S = set(cells)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    T = sorted([d + sum(y) for y in A], reverse=True)
    M = m*(m-1)//2
    crude = sum(t*(m - 1 - i) for i, t in enumerate(T))
    n += 1
    if crude > (d+1)*M:
        crude_fail += 1
        tr = [(d + sum(y), cells[y] % m) for y in A]
        w = max(sum(t*((r - sg) % m) for t, r in tr) for sg in range(m))
        e = d + 1; q = -(-s.c // m)
        known = (3*e >= m) or (q <= 3) or (len(A) <= d) or m <= 19
        hard.append(((d+1)*M - w, round(((d+1)*M - w)/((d+1)*M), 3), s.P[:7], s.c, m, d, len(A), sum(T), d*m - sum(T), 'known' if known else 'OPEN-regime'))
print(n, 'tiles; crude bound fails on', crude_fail)
open_ = [h for h in hard if h[-1] == 'OPEN-regime']
print('of which in open Wilf regime (q>=4, 3e<m, |A|>d, m>=20):', len(open_))
for h in sorted(open_, key=lambda t: t[1])[:12]: print(h)
