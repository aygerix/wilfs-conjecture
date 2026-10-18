# Diagnostics for height-3 tiles at the worst sigma: split MaxCL slack into
#   unit term U = sum_units (load-d-1) r, level-2 term V = sum_{L2 nonmax} (load-d-1) r, wraps m*B, carries m*P.
# MaxCL slack = (H+d+1) r0 - U - V - m(B-P).
import sys, random
from fractions import Fraction as Fr
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from math import gcd
from functools import reduce
def unit(a, d): return tuple(int(i == a) for i in range(d))
def terms(cells, d, m, sg):
    S = set(cells); zero = tuple([0]*d)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    pairs = []
    for y in A:
        h = sum(y); dirs = [a for a in range(d) if y[a] > 0]
        if h == 2:
            u = unit(dirs[0], d); pairs.append((y, u, tuple(p-q for p, q in zip(y, u)), Fr(1)))
        elif h == 3:
            for a in dirs:
                u = unit(a, d); pairs.append((y, u, tuple(p-q for p, q in zip(y, u)), Fr(2, len(dirs))))
    load = {}
    for y, u, v, w in pairs: load[u] = load.get(u, 0) + w; load[v] = load.get(v, 0) + w
    H = sum(sum(y) - 1 for y in A)
    r = {x: (cells[x] - sg) % m for x in cells}
    U = sum((load.get(z, 0) - d - 1)*r[z] for z in cells if sum(z) == 1 and z not in A)
    V = sum((load.get(z, 0) - d - 1)*r[z] for z in cells if sum(z) == 2 and z not in A)
    B = sum(w for y, u, v, w in pairs if r[u] + r[v] - r[y] - r[zero] < 0)
    P = sum(w for y, u, v, w in pairs if r[u] + r[v] - r[y] - r[zero] >= m)
    slack = (H + d + 1)*r[zero] - U - V - m*(B - P)
    return dict(r0=r[zero], H=H, U=U, V=V, B=B, P=P, slack=slack, n2=sum(1 for x in cells if sum(x)==2),
                n3=sum(1 for x in cells if sum(x)==3), A2=sum(1 for y in A if sum(y)==2),
                maxload=max(load.get(unit(a,d),0) for a in range(d)),
                unitr=sorted(r[unit(a,d)] for a in range(d)), L2r_mean=None)
if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); DLO, DHI = int(sys.argv[3]), int(sys.argv[4])
    found = 0; tries = 0; rows = []
    while found < NT and tries < 20000:
        tries += 1
        d = rng.randint(DLO, DHI); m = rng.randint(max(d + 2, d**3 // 10), d**3 // 4 + d)
        k = rng.randint(4, 7); res = rng.sample(range(1, m), d)
        gens = sorted([m] + [k*m + r for r in res])
        if reduce(gcd, gens) != 1: continue
        s = NS.from_generators(gens)
        if s.e != d + 1: continue
        cells, dd = tile_of(s)
        if max(sum(x) for x in cells) != 3: continue
        found += 1
        best = None
        for sg in range(s.m):
            t = terms(cells, dd, s.m, sg)
            if best is None or t['slack'] < best['slack']: best = t; best['sg'] = sg
        best['m'] = s.m; best['d'] = dd; best['P_'] = s.P[:4]
        rows.append(best)
    rows.sort(key=lambda t: t['slack'] / (t['m']**2 * (t['d']+1)))
    for t in rows[:8]:
        print({k: (float(v) if isinstance(v, Fr) else v) for k, v in t.items() if k not in ('unitr', 'L2r_mean')})
        print('   unit positions', t['unitr'], ' m-r0 =', t['m'] - t['r0'])
