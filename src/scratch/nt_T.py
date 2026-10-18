# NON-two-face e = 4: T(X) = sum_{u in X}(|y_u| + 3) vs 2m + 1  (T(X) <= 2m+1  <=>  N >= m-1  =>  Wilf),
# and the shape-only version T(A) over all maximal cells A of D.   usage: nt_T.py m0 m1 K [all]
import sys, itertools
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
m0, m1, K = map(int, sys.argv[1:4]); ALL = len(sys.argv) > 4
for m in range(m0, m1 + 1):
    n = 0; wX = wA = None; fX = fA = 0
    for g3 in itertools.combinations(range(m + 1, K*m), 3):
        if reduce(gcd, (m,) + g3) != 1: continue
        s = NS.from_generators([m, *g3])
        if s.e != 4 or (not ALL and s.c <= 3*m): continue
        p, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}; D = set(cells)
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        n += 1; c = s.c
        A = [x for x in D if all(x[:i] + (x[i]+1,) + x[i+1:] not in D for i in range(3))]
        TX = sum(sum(x) + 3 for x in A if cells[x] >= c); TA = sum(sum(x) + 3 for x in A)
        eX, eA = TX - 2*m - 1, TA - 2*m - 1
        if wX is None or eX > wX[0]: wX = (eX, [m, *g3])
        if wA is None or eA > wA[0]: wA = (eA, [m, *g3])
        fX += eX > 0; fA += eA > 0
    print(f'm={m}: non-two-face {n}; max T(X)-2m-1 = {wX} (fails {fX}); max T(A)-2m-1 = {wA} (fails {fA})', flush=True)
