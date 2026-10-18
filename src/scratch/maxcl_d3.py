# MaxCL / Tile-TOP'' on Apery tiles of random 4- and 5-generated semigroups with large m, recording type.
# MaxCL slack (r-form):  (d+1) sum_N r - sum_A (|y|-1) r   minimized over rotations.
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); MLO, MHI = int(sys.argv[3]), int(sys.argv[4]); K = int(sys.argv[5])
f = 0; worst = None; maxt = 0; cnt = 0
while cnt < N:
    m = rng.randint(MLO, MHI)
    gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4]) * m) for _ in range(K)]))
    if len(gens) != K + 1 or reduce(gcd, gens) != 1: continue
    s = NS.from_generators(gens)
    if s.e != K + 1: continue
    cnt += 1
    cells, d = tile_of(s); S = set(cells)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    Nn = [z for z in cells if z not in A]
    t = len(A); maxt = max(maxt, t)
    rA = [(sum(y) - 1, cells[y] % m) for y in A]; rN = [cells[z] % m for z in Nn]
    v = min((d+1)*sum((r - sg) % m for r in rN) - sum(w*((r - sg) % m) for w, r in rA) for sg in range(m))
    if v < 0:
        f += 1
        if f <= 5: print('MaxCL FAIL', gens, 'type', t, 'v', v, flush=True)
    rel = v / (m*m)
    if worst is None or rel < worst[0]: worst = (rel, v, gens, t)
print(cnt, 'semigroups, e =', K + 1, 'm in', (MLO, MHI), '; MaxCL fails', f, '; max type', maxt, '; worst normalized slack', worst)
