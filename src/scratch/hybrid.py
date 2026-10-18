# Hybrid criterion (any e = 4):  Def_all >= m * sum_{(x,a): t not in X} max(1, ht(t))  =>  Wilf if  T(X) <= 2m + 1 + H2,
# H2 = sum_{(x,a)} (ht(t_a x) - 1)^+ (shape-only).  Report min slack 2m+1+H2-T(X) for NON-two-face.  usage: m0 m1 K
import sys, itertools
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
m0, m1, K = map(int, sys.argv[1:4])
for m in range(m0, m1 + 1):
    worst = None; n = 0; fails = 0
    for g3 in itertools.combinations(range(m + 1, K*m), 3):
        if reduce(gcd, (m,) + g3) != 1: continue
        s = NS.from_generators([m, *g3])
        if s.e != 4: continue
        p, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}; D = set(cells)
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        ht = {}
        for x in sorted(D, key=lambda x: -sum(x)):
            ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
        def top(x, i):
            while add(x, i) in D: x = add(x, i)
            return x
        H2 = sum(max(0, ht[top(x, i)] - 1) for x in D for i in range(3))
        TX = sum(sum(y) + 3 for y in D if cells[y] >= s.c)
        sl = 2*m + 1 + H2 - TX; n += 1; fails += sl < 0
        if worst is None or sl < worst[0]: worst = (sl, [m, *g3], H2, TX - 2*m - 1)
    print(f'm={m}: non-two-face {n}; min slack {worst}; fails {fails}', flush=True)
