# Tile-CL for d = 3 (e = 4) grlex tiles:  X(sigma) = sum_{y in D} T(y) r(y) <= 4M',  T(y) = sum_{a: y+e_a notin D} (y_a+1).
# (Tile-CL => MaxCL by dropping non-maximal tops.)  Random sample + hill-climb minimizing the normalized min slack.
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from twoface_census import rand_gens, twoface_info
from math import gcd
from functools import reduce
def tcl(s):
    cells, d = tile_of(s); m = s.m; S = set(cells)
    T = {}
    for y in cells:
        t = sum(y[a] + 1 for a in range(d) if tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S)
        if t: T[y] = t
    M = m*(m-1)//2; best = None
    w = [0]*m
    for y, t in T.items(): w[cells[y] % m] += t
    for sg in range(m):
        X = sum(w[g]*((g - sg) % m) for g in range(m))
        sl = ((d+1)*M - X)/((d+1)*M)
        if best is None or sl < best[0]: best = (sl, sg)
    return best, cells
def score(g):
    if reduce(gcd, g) != 1 or len(set(g)) != 4: return None
    s = NS.from_generators(sorted(g))
    if s.e != 4: return None
    b, cells = tcl(s)
    return b[0], s, cells
if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); NR, RUNS, MMIN, MMAX, STEPS = map(int, sys.argv[2:7])
    f = 0; worst = None
    for _ in range(NR):
        g = rand_gens(rng, MMIN, MMAX); sc = score(g)
        if not sc: continue
        if sc[0] < 0: f += 1; print('random Tile-CL FAIL', sc[1].P, round(sc[0], 4), 'twoface', bool(twoface_info(sc[2], sc[1].m)), flush=True)
        if worst is None or sc[0] < worst[0]: worst = (round(sc[0], 4), sc[1].P)
    print('random e=4: Tile-CL fails', f, 'worst', worst, flush=True)
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
        print('climb', round(cur[0], 4), cur[1].P, 'm', cur[1].m, 'twoface', bool(twoface_info(cur[2], cur[1].m)), flush=True)
