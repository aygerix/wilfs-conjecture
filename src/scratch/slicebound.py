# H >= H^(c) + sum_k P(D_k^(c))  for each orientation c, where D_k^(c) = slice x_c = k (2-D down-set) and
# P(F) = sum_{row groups} rho*C(g,2) + sum_{col groups} kappa*C(g,2) is the 2-D plateau content (= in-slice heights of
# in-slice tops).  Report min over tiles of max_c [..] - (m-1).   usage: m0 m1 K
import sys, itertools
from math import gcd, comb
from functools import reduce
from collections import Counter
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def plateau(F):     # F: set of (i, j) 2-D down-set
    rows = Counter(); cols = Counter()
    for (i, j) in F: rows[j] += 1; cols[i] += 1
    return sum(r*comb(g, 2) for r, g in Counter(rows.values()).items()) + sum(c*comb(g, 2) for c, g in Counter(cols.values()).items())
def bound(D):
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    def top(x, i):
        while add(x, i) in D: x = add(x, i)
        return x
    Hc = [sum(ht[top(x, c)] for x in D) for c in range(3)]
    best = None
    for c in range(3):
        o = [i for i in range(3) if i != c]
        Pk = 0
        for k in range(max(x[c] for x in D) + 1):
            Pk += plateau({(x[o[0]], x[o[1]]) for x in D if x[c] == k})
        v = Hc[c] + Pk
        best = v if best is None else max(best, v)
    return best, sum(Hc)
if __name__ == '__main__':
    m0, m1, K = map(int, sys.argv[1:4])
    for m in range(m0, m1 + 1):
        worst = None; fails = 0; n = 0
        for g3 in itertools.combinations(range(m + 1, K*m), 3):
            if reduce(gcd, (m,) + g3) != 1: continue
            s = NS.from_generators([m, *g3])
            if s.e != 4: continue
            p, best = factorizations_down_set(s, 'grlex'); D = set(best.values())
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            HP, H = bound(D); n += 1; sl = HP - (m - 1); fails += sl < 0
            if worst is None or sl < worst[0]: worst = (sl, [m, *g3], H - m + 1)
        print(f'm={m}: {n}; min H_P-(m-1) {worst}; fails {fails}', flush=True)
