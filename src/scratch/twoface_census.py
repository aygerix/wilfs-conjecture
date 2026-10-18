# (1) hill-climb CR slack over e=4 semigroups whose grlex tile is NOT two-face (all e_a+e_b in D);
# (2) census of two-face tiles: type of z* (cell congruent to e_a+e_b) and whether psi(D) is a 2-D down-set,
#     psi(x) = (x_a + x_c, x_b + x_c) when z* = e_c.
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from crude_e4 import crslack
from math import gcd
from functools import reduce
def unit(a, d=3): return tuple(1 if i == a else 0 for i in range(d))
def twoface_info(cells, m):
    S = set(cells); out = []
    for a in range(3):
        for b in range(a + 1, 3):
            if tuple(x + y for x, y in zip(unit(a), unit(b))) in S: continue
            v = (cells[unit(a)] + cells[unit(b)]) % m
            z = [x for x in cells if cells[x] % m == v][0]
            c = 3 - a - b
            info = dict(pair=(a, b), z=z)
            if z == unit(c):
                img = {(x[a] + x[c], x[b] + x[c]) for x in cells}
                info['psi_inj'] = len(img) == len(cells)
                info['psi_down'] = all((u - 1, v_) in img for (u, v_) in img if u > 0) and all((u, v_ - 1) in img for (u, v_) in img if v_ > 0)
            out.append(info)
    return out
def rand_gens(rng, MMIN, MMAX):
    m = rng.randint(MMIN, MMAX)
    while True:
        g = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4, 6])*m) for _ in range(3)]))
        if len(g) == 4 and reduce(gcd, g) == 1: return g
def score(g):
    if reduce(gcd, g) != 1 or len(set(g)) != 4: return None
    s = NS.from_generators(sorted(g))
    if s.e != 4: return None
    cells, d = tile_of(s)
    if twoface_info(cells, s.m): return None
    return crslack(list(cells), 3, s.m) / (2*s.m*(s.m - 1)), s
if __name__ == '__main__':
    mode = sys.argv[1]; rng = random.Random(int(sys.argv[2]))
    if mode == 'climb':
        RUNS, MMIN, MMAX, STEPS = map(int, sys.argv[3:7]); best = None; fails = 0
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
                if sc and sc[0] <= cur[0]: g, cur = h, sc
            if cur[0] < 0: fails += 1; print('NON-TWO-FACE CR FAIL', cur[1].P, cur[1].c, round(cur[0], 4), flush=True)
            if best is None or cur[0] < best[0]: best = (round(cur[0], 4), cur[1].P, cur[1].m)
        print('non-two-face climb runs', RUNS, 'CR fails', fails, 'min normalized CR slack', best)
    else:
        N, MMIN, MMAX = map(int, sys.argv[3:6]); from collections import Counter
        cnt = Counter(); ex = {}
        for _ in range(N):
            s = NS.from_generators(rand_gens(rng, MMIN, MMAX))
            if s.e != 4: continue
            cells, d = tile_of(s)
            for info in twoface_info(cells, s.m):
                c = 3 - sum(info['pair'])
                key = ('z=e_c' if info['z'] == unit(c) else 'z other', info.get('psi_down'))
                cnt[key] += 1; ex.setdefault(key, (s.P, info['z']))
        print(cnt); print(ex)
