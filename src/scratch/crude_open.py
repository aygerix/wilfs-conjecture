# Crude rearrangement bound for MaxCL, targeted at the OPEN Wilf regime: q >= 4, 3e < m, t >= e, m >= 20.
# crude(D) = sum_i T_(i) (m-1-i) <= (d+1) M'  (T sorted decreasing)  ==> MaxCL for every p, sigma (residue-free).
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from math import gcd
from functools import reduce
def crude_ok(s):
    cells, d = tile_of(s); m = s.m; S = set(cells)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    T = sorted([d + sum(y) for y in A], reverse=True)
    M = m*(m-1)//2
    crude = sum(t*(m - 1 - i) for i, t in enumerate(T))
    return (d+1)*M - crude, d, len(A), sum(T)
def is_open(s):
    return s.q >= 4 and 3*s.e < s.m and s.t() >= s.e and s.m >= 20
if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2])
    cands = []
    # Backelin family: s = r(3n+2)+3; gens s, s+3, s+3n+1, s+3n+2
    for n in range(2, 7):
        for r in range(3*n + 2, 3*n + 6):
            s0 = r*(3*n + 2) + 3
            cands.append([s0, s0 + 3, s0 + 3*n + 1, s0 + 3*n + 2])
    tries = 0; cnt = 0; fails = 0; worst = None; nopen = 0
    while nopen < NT and tries < 200000:
        tries += 1
        if cands: gens = cands.pop()
        else:
            m = rng.randint(20, 70); e = rng.randint(4, max(4, m//3 - 1))
            mode = rng.random()
            if mode < 0.4:   # narrow band near a multiple of m -> deep, large type
                k = rng.choice([1, 2]); lo = k*m + rng.randint(1, m//2)
                gens = sorted(set([m] + [lo + rng.randint(0, m//(rng.choice([2, 3, 4]))) for _ in range(e - 1)]))
            elif mode < 0.7:
                gens = sorted(set([m] + [rng.randint(m + 1, 2*m - 1) for _ in range(e - 1)]))
            else:
                gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([3, 4, 5])*m) for _ in range(e - 1)]))
        if reduce(gcd, gens) != 1: continue
        s = NS.from_generators(gens)
        if not is_open(s): continue
        nopen += 1
        v, d, nA, TA = crude_ok(s)
        if v < 0:
            fails += 1
            if fails <= 8: print('CRUDE FAIL (open regime)', s.P, 'm', s.m, 'e', s.e, 'c', s.c, 'q', s.q, 't', s.t(), '|A|', nA, 'T(A)', TA, 'slack', v, flush=True)
        rel = v / ((d+1)*s.m*(s.m-1)/2)
        if worst is None or rel < worst[0]: worst = (round(rel, 4), s.P, s.c, s.t())
    print('open-regime semigroups tested', nopen, 'in', tries, 'tries; crude fails', fails, '; worst normalized crude slack', worst)
