# Crude rearrangement bound CR for d = 3 (e = 4):  sum_i T_(i) (m-1-i) <= 4 m(m-1)/2,  T sorted decreasing.
# CR => MaxCL (any residues) => Wilf.  Test: (a) all d=3 tiles with m <= MMAX_EX (exhaustive), (b) random 4-generated
# semigroups (grlex tiles) incl. prescribed-conductor variants, (c) hill-climb on generators to minimize CR slack.
import sys, random, itertools
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from exp_cl_adv import with_conductor
from math import gcd
from functools import reduce
def crslack(cells, d, m):
    S = set(cells)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    T = sorted([d + sum(y) for y in A], reverse=True)
    return (d+1)*m*(m-1)//2 - sum(t*(m - 1 - i) for i, t in enumerate(T))
if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); MMAX = int(sys.argv[3])
    n = f = 0; worst = None
    for _ in range(NT):
        m = rng.randint(5, MMAX)
        while True:
            gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 5, 10])*m) for _ in range(3)]))
            if len(gens) == 4 and reduce(gcd, gens) == 1: break
        s0 = NS.from_generators(gens)
        if s0.e != 4: continue
        for s in [s0] + [with_conductor(gens, int(s0.c*fr)) for fr in (0.3, 0.6, 0.85) if int(s0.c*fr) > m]:
            cells, d = tile_of(s)
            if d != 3: continue
            n += 1; sl = crslack(cells, d, s.m)
            key = sl / (4*s.m*(s.m-1)/2)
            if sl < 0: f += 1
            if worst is None or key < worst[0]: worst = (round(key, 4), sl, s.P, s.c, s.m)
    print('random e=4 tiles', n, 'CR fails', f, 'worst normalized', worst, flush=True)
