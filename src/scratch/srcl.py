# SR-CL: for every tile (D,p) and every s: slack(s) >= -sigma(D), sigma(D) = # spike directions
# (directions b with {x in D : x_b >= 1} = {e_b}).  Also record min over tiles of (min slack + sigma) and of
# (min slack + sigma) restricted to sigma = 0, and the analogous upper bound.
# Part 1: Apery tiles of the seeded adversarial suite (as in E49).  Part 2 (exhaustive) in srcl_exh.py.
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from exp_cl_adv import with_conductor
from cl import factorizations_down_set

def tile_of(s):
    Pp, best = factorizations_down_set(s, 'grlex')
    cells = {n: w for w, n in best.items()}
    return cells, len(Pp)

def slack_vec(cells, d, m):
    w_res = [0] * m
    for n, w in cells.items():
        T = 0
        for a in range(d):
            up = list(n); up[a] += 1
            if tuple(up) not in cells: T += n[a] + 1
        w_res[w % m] += T
    M = m * (m - 1) // 2
    return [(sum(w_res[r] * ((s - r) % m) for r in range(m)) - (d - 1) * M) // m for s in range(m)]

def spikes(cells, d):
    sig = 0
    for b in range(d):
        if all(n[b] == 0 or (n[b] == 1 and sum(n) == 1) for n in cells): sig += 1
    return sig

if __name__ == '__main__':
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
    lowf = upf = 0; tilef0 = 0; worst = None; worst0 = None
    for s in tests:
        cells, d = tile_of(s)
        sl = slack_vec(cells, d, s.m); sg = spikes(cells, d)
        lo, hi = min(sl), max(sl)
        if lo < 0 and sg == 0: tilef0 += 1; print('Tile-CL low fail with NO spikes', s.P, s.c, sl)
        if lo + sg < 0: lowf += 1; print('SR-CL FAIL', s.P, s.c, 'sigma', sg, 'min', lo)
        if hi - sg > s.m - 1: upf += 1
        v = (lo + sg, lo, sg)
        if lo < 0 and (worst is None or lo / max(sg, 1) < worst[0]): worst = (lo / max(sg, 1), lo, sg, s.P[:8], s.c)
    print(len(tests), 'tiles; SR-CL lower fails', lowf, '; upper (hi <= m-1+sigma) fails', upf,
          '; spike-free Tile-CL lower fails', tilef0, '; worst min/sigma among failures', worst)
