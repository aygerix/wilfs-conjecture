"""E47: Tile-CL (all reference residues s) for the Apery tiles of adversarial / random large semigroups.
Tile = grlex-min factorization down-set D of Ap(S,m) over the non-multiplicity generators, p_a = n_a mod m.
slack(s) = (sum_y T(y) <s - phi(y)> - (d-1) m(m-1)/2) / m must lie in [0, m-1] for every s (Tile-CL)."""
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set

def with_conductor(gens, c):
    return NS.from_generators(list(gens) + list(range(c, c + min(gens))))

def tile_slack(s, order='grlex'):
    m = s.m
    Pp, best = factorizations_down_set(s, order)
    d = len(Pp)
    cells = {n: w for w, n in best.items()}
    w_res = [0] * m
    for n, w in cells.items():
        T = 0
        for a in range(d):
            up = list(n); up[a] += 1
            if tuple(up) not in cells:
                T += n[a] + 1
        w_res[w % m] += T
    M = m * (m - 1) // 2
    out = []
    for sr in range(m):
        f = sum(w_res[r] * ((sr - r) % m) for r in range(m))
        num = f - (d - 1) * M
        assert num % m == 0
        out.append(num // m)
    return d, out

if __name__ == '__main__':
    tests = []
    for gens, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((17, 27, 28), 68),
                    ((18, 28, 29), 72), ((30, 44, 48, 49), 118), ((23, 39, 40, 42), 77)]:
        tests.append(('W0<0', with_conductor(gens, c)))
    tests.append(('Backelin', NS.from_generators([213, 216, 226, 227])))
    for mu, gam, p in [(10, 13, 5), (12, 17, 6), (15, 19, 7), (20, 27, 8), (25, 32, 9)]:
        tests.append(('Delgado', with_conductor((mu, gam, gam + 1), p * mu)))
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    MMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 80
    while len(tests) < N:
        m = rng.randint(5, MMAX)
        k = rng.randint(1, 12)
        hi = rng.choice([2 * m, 3 * m, 5 * m, 10 * m])
        gens = sorted(set([m] + [rng.randint(m + 1, hi) for _ in range(k)]))
        if reduce(gcd, gens) != 1:
            continue
        s = NS.from_generators(gens)
        tests.append(('rand', s))
        for frac in (0.3, 0.5, 0.7, 0.9):
            cc = int(s.c * frac)
            if cc > m:
                tests.append(('trunc', with_conductor(gens, cc)))
    fails = 0; minrel = None; maxd = 0; maxm = 0
    for name, s in tests:
        if s.m == 1:
            continue
        d, sl = tile_slack(s)
        maxd = max(maxd, d); maxm = max(maxm, s.m)
        lo, hi = min(sl), max(sl)
        if lo < 0 or hi > s.m - 1:
            fails += 1
            print('FAIL', name, s.P, s.c, sl)
        if s.m > 2:
            rel = lo / (s.m - 1)
            if minrel is None or rel < minrel[0]:
                minrel = (rel, name, s.P, s.c)
    print(len(tests), 'tests; max d', maxd, 'max m', maxm, '; Tile-CL fails', fails, '; min (min slack)/(m-1):', minrel)
