# NON-two-face e = 4: (a) shape-only H(D) - (m-1)   [H >= m-1 => Wilf, since Def_all >= (m+1)H];
# (b) B1 = sum_{(x,a)} max_{y in A, y >= t}[(m+1)|y-t| + dhat(y)],  dhat(y) = m if y not in X else m - pi(y)
#     (valid lower bound for Def_all = mW + m(m-1));  report min (B1 - m(m-1))/m.   usage: heightB.py m0 m1 K
import sys, itertools
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def stats(s):
    p, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}; D = set(cells)
    if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): return None
    m, c = s.m, s.c
    A = [x for x in D if all(add(x, i) not in D for i in range(3))]
    dh = {y: (m if cells[y] < c else m - (cells[y] - c + 1)) for y in A}
    order = sorted(D, key=lambda x: -sum(x)); ht = {}; bb = {}
    for x in order:
        up = [add(x, i) for i in range(3) if add(x, i) in D]
        ht[x] = max([ht[u] + 1 for u in up], default=0)
        bb[x] = max([bb[u] + m + 1 for u in up], default=None) if up else dh[x]
    def top(x, i):
        while add(x, i) in D: x = add(x, i)
        return x
    H = sum(ht[top(x, i)] for x in D for i in range(3)); B1 = sum(bb[top(x, i)] for x in D for i in range(3))
    return H - (m - 1), (B1 - m*(m - 1))/m
m0, m1, K = map(int, sys.argv[1:4])
for m in range(m0, m1 + 1):
    n = 0; wH = wB = None; fH = fB = 0
    for g3 in itertools.combinations(range(m + 1, K*m), 3):
        if reduce(gcd, (m,) + g3) != 1: continue
        s = NS.from_generators([m, *g3])
        if s.e != 4: continue
        r = stats(s)
        if r is None: continue
        n += 1; fH += r[0] < 0; fB += r[1] < 0
        if wH is None or r[0] < wH[0]: wH = (r[0], [m, *g3])
        if wB is None or r[1] < wB[0]: wB = (round(r[1], 2), [m, *g3])
    print(f'm={m}: non-two-face {n}; min H-(m-1) {wH} (fails {fH}); min (B1-m(m-1))/m {wB} (fails {fB})', flush=True)
