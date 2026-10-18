# Uniform box load: L(z) = sum_{y in A, y > z} 2(|y|-1) / (prod(y_a+1) - 2).  Is L(z) <= d+1 for all nonzero non-max z?
# (If yes, the Load Lemma holds with the uniform pairing; residue-free.)
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from math import prod
def boxload(cells, d):
    S = set(cells)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    A2 = [(y, Fr(2*(sum(y)-1), prod(v+1 for v in y) - 2)) for y in A if sum(y) >= 2]
    worst = None
    for z in cells:
        if sum(z) == 0 or z in A: continue
        L = sum(w for y, w in A2 if y != z and all(a <= b for a, b in zip(z, y)))
        if worst is None or L > worst[0]: worst = (L, z)
    return worst
if __name__ == '__main__':
    if sys.argv[1] == 'exh':
        from exp_cl_tiling import downsets
        for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
            for m in range(3, mmax + 1):
                f = 0; mx = None
                for D in downsets(m, d):
                    if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                    if not any(len({sum(i*j for i, j in zip(y, p)) % m for y in D}) == m for p in itertools.product(range(1, m), repeat=d)): continue
                    w = boxload(list(D), d)
                    if w is None: continue
                    if w[0] > d + 1:
                        f += 1
                    if mx is None or w[0] > mx[0]: mx = (w[0], w[1], sorted(D))
                print('d', d, 'm', m, 'box-load fails', f, 'max load', mx and (str(mx[0]), mx[1]), flush=True)
    else:
        import random
        from ns import NS
        from exp_cl_adv import with_conductor
        from srcl import tile_of
        from math import gcd
        from functools import reduce
        rng = random.Random(int(sys.argv[2])); NT = int(sys.argv[3]); MMAX = int(sys.argv[4])
        f = 0; cnt = 0; worst = None
        while cnt < NT:
            m = rng.randint(6, MMAX); k = rng.randint(2, 12)
            if rng.random() < 0.5:
                base = rng.randint(m + 1, 3*m); gens = sorted(set([m] + [base + rng.randint(0, max(1, m//3)) for _ in range(k)]))
            else:
                gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 4])*m) for _ in range(k)]))
            if reduce(gcd, gens) != 1: continue
            s0 = NS.from_generators(gens)
            for s in [s0] + [with_conductor(gens, int(s0.c*fr)) for fr in (0.4, 0.7) if int(s0.c*fr) > m]:
                cnt += 1
                cells, d = tile_of(s)
                w = boxload(list(cells), d)
                if w is None: continue
                rel = w[0] / (d + 1)
                if w[0] > d + 1:
                    f += 1
                    if f <= 3: print('FAIL', s.P[:8], s.c, 'd', d, str(w[0]), w[1])
                if worst is None or rel > worst[0]: worst = (float(rel), s.P[:6], s.c, d)
        print(cnt, 'tiles; box-load fails', f, 'max load/(d+1)', worst)
