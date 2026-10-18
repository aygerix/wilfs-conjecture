# Uniform ordered-split scheme on semigroup (grlex) tiles: test
#  (WL)  B <= r(0)   and   (LD)  sum_{N\0} (load-d-1) r - m P <= (H+d+1-m) r(0)      for all sigma.
# WL + LD  =>  MaxCL (identity).  Random semigroups, m <= MMAX.
import sys, random, itertools
from fractions import Fraction as Fr
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
def box(y): return list(itertools.product(*[range(k+1) for k in y]))
def scheme(cells, d):
    S = set(cells); zero = tuple([0]*d)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    pairs = []
    for y in A:
        if sum(y) < 2: continue
        us = [u for u in box(y) if u != zero and u != y]; w = Fr(sum(y) - 1, len(us))
        for u in us: pairs.append((y, u, tuple(a - b for a, b in zip(y, u)), w))
    load = {}
    for y, u, v, w in pairs: load[u] = load.get(u, 0) + w
    for y, u, v, w in pairs: pass
    # ordered pairs: each ordered split loads u once; the reverse split loads v once -> load(u) counts both roles
    H = sum(sum(y) - 1 for y in A)
    Aset = set(A)
    return A, Aset, pairs, load, H
def run(cells, d, m):
    zero = tuple([0]*d)
    A, Aset, pairs, load, H = scheme(cells, d)
    wl = ld = None
    for sg in range(m):
        r = {x: (cells[x] - sg) % m for x in cells}; r0 = r[zero]
        B = P = Fr(0)
        for y, u, v, w in pairs:
            s = r[u] + r[v] - r[y] - r0
            if s < 0: B += w
            elif s >= m: P += w
        # each ordered pair contributes w*(r(u)+r(v)): loads must count u and v; ordered splits (u,v),(v,u) both present
        tot = {}
        for y, u, v, w in pairs:
            tot[u] = tot.get(u, 0) + w; tot[v] = tot.get(v, 0) + w
        Lsum = sum((tot.get(z, 0) - d - 1)*r[z] for z in cells if z not in Aset and z != zero)
        e1 = B - r0; e2 = Lsum - m*P - (H + d + 1 - m)*r0
        if wl is None or e1 > wl[0]: wl = (e1, sg)
        if ld is None or e2 > ld[0]: ld = (e2, sg)
        # sanity: identity
        lhs = sum((sum(y) - 1)*r[y] for y in A)
        assert lhs == sum((tot.get(z, 0))*r[z] for z in cells) - Fr(H)*r0 - m*(P - B)
    return wl, ld
if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); MMAX = int(sys.argv[3])
    n = fw = fl = 0; ww = wd = None; tries = 0
    while n < NT and tries < 100000:
        tries += 1
        m = rng.randint(6, MMAX); k = rng.randint(2, max(2, m // 3))
        mode = rng.random()
        if mode < 0.4:
            base = rng.randint(m + 1, 3*m); gens = sorted(set([m] + [base + rng.randint(0, max(1, m//3)) for _ in range(k)]))
        elif mode < 0.7:
            gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 5])*m) for _ in range(k)]))
        else:
            kk = rng.randint(2, 6); gens = sorted(set([m] + [kk*m + rng.randint(1, m-1) for _ in range(k)]))
        if reduce(gcd, gens) != 1: continue
        s = NS.from_generators(gens)
        cells, d = tile_of(s)
        if max(sum(x) for x in cells) < 3: continue
        n += 1
        wl, ld = run(cells, d, s.m)
        if wl[0] > 0:
            fw += 1
            if ww is None or wl[0] > ww[0]: ww = (wl[0], s.P, wl[1])
        if ld[0] > 0:
            fl += 1
            if wd is None or ld[0]/s.m**2 > wd[0]: wd = (ld[0]/s.m**2, s.P[:8], ld[1])
    print('tiles', n, '| WL fails', fw, ww, '| LD fails', fl, wd)
