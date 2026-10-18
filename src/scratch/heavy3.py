# d = 3 tiles with T(A) > 2m (equivalently Dep < m): the only d=3 tiles where the crude bound CR is not automatic.
# Shape census: pairs (a,b) with e_a+e_b notin D ("two-face"), height, |A|, Dep/m, CR slack.
import sys, random, itertools
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from crude_e4 import crslack
from math import gcd
from functools import reduce
def shape(cells, d, m):
    S = set(cells)
    A = [y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    TA = sum(d + sum(y) for y in A)
    unit = lambda a: tuple(1 if i == a else 0 for i in range(d))
    pairs = [(a, b) for a in range(d) for b in range(a+1, d)
             if tuple(x + y for x, y in zip(unit(a), unit(b))) not in S]
    return dict(TA=TA, Dep=d*m - TA, nA=len(A), h=max(sum(x) for x in cells), twoface=pairs,
                ext=tuple(max(x[a] for x in cells) for a in range(d)))
if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); NT = int(sys.argv[2]); MMAX = int(sys.argv[3])
    n = heavy = 0; nontwo = []; crf = 0
    for _ in range(NT):
        m = rng.randint(8, MMAX)
        while True:
            gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 5, 10])*m) for _ in range(3)]))
            if len(gens) == 4 and reduce(gcd, gens) == 1: break
        s = NS.from_generators(gens)
        if s.e != 4: continue
        cells, d = tile_of(s); n += 1
        sh = shape(list(cells), d, s.m)
        if sh['TA'] > 2*s.m:
            heavy += 1
            sl = crslack(list(cells), d, s.m)
            if sl < 0: crf += 1
            if not sh['twoface']: nontwo.append((s.P, s.m, sh['h'], sh['nA'], round(sh['Dep']/s.m, 3), sh['ext'], sl))
    print('e=4 tiles', n, 'with T(A) > 2m:', heavy, 'CR fails among them', crf, '; not two-face:', len(nontwo))
    for t in nontwo[:25]: print('  ', t)
