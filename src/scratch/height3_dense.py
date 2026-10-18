# Dense height-3 tiles: generators k*m + random residues with large k, m ~ d^3/6, so that Ap = sums of <= 3 generators
# with many level-3 cells.  Test the natural height-3 scheme and MaxCL itself.
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from math import gcd
from functools import reduce
src = open('src/scratch/height3.py').read().split('rng = random.Random')[0]
ns = {}; exec(src, ns); check = ns['check']
rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); DLO, DHI = int(sys.argv[3]), int(sys.argv[4])
found = fails = mfails = 0; tries = 0; worst = None; densest = 0
while found < NT and tries < 20000:
    tries += 1
    d = rng.randint(DLO, DHI); m = rng.randint(max(d + 2, d**3 // 10), d**3 // 4 + d)
    k = rng.randint(4, 7)
    res = rng.sample(range(1, m), d)
    gens = sorted([m] + [k*m + r for r in res])
    if reduce(gcd, gens) != 1: continue
    s = NS.from_generators(gens)
    if s.e != d + 1: continue
    cells, dd = tile_of(s)
    if max(sum(x) for x in cells) != 3: continue
    found += 1
    S = set(cells); A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(dd))]
    L3 = sum(1 for y in A if sum(y) == 3); densest = max(densest, L3 / dd**2)
    (sl, sg), ml = check(cells, dd, s.m)
    M = s.m*(s.m-1)//2; tr = [(dd + sum(y), cells[y] % s.m) for y in A]
    mx = min((dd+1)*M - sum(t*((r - g) % s.m) for t, r in tr) for g in range(s.m))
    if mx < 0: mfails += 1; print('MaxCL FAIL', s.P, flush=True)
    if sl < 0:
        fails += 1
        if fails <= 4: print('scheme FAIL', s.P, 'm', s.m, 'd', dd, '|L3|', L3, 'sigma', sg, 'slack', sl, 'maxload/(d+1)', float(ml), flush=True)
    if worst is None or sl / ((dd + 1)*M) < worst[0]: worst = (sl / ((dd+1)*M), s.P[:5], L3, dd)
print('dense height-3 tiles', found, 'tries', tries, '; scheme fails', fails, '; MaxCL fails', mfails, '; max |L3|/d^2', round(densest, 3), '; worst normalized scheme slack', worst)
