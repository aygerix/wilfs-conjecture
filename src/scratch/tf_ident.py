# Two-face e = 4 identity (any t):  3 m W = (m - 4 L3) M + 4 Def2D + 4 sum_{k<L3} k p_c - 3 m (m-1),
# Def2D = sum over the 2-D runs (rows of F1, rows of F2, c-columns) of |run| (M - w(end)).
# Reports how often the parts without Def2D already give W >= 0, as a function of L3/m and M/m.
import sys, itertools, collections, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def parts(s):
    p, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}; D = set(cells); d = 3; m = s.m
    faces = [(a, b) for a in range(d) for b in range(a + 1, d) if tuple(int(i in (a, b)) for i in range(d)) not in D]
    if not faces: return None
    a, b = faces[0]; cx = 3 - a - b
    M = max(cells.values()); L3 = max(x[cx] for x in D) + 1
    def top(x, i):
        while True:
            y = x[:i] + (x[i] + 1,) + x[i+1:]
            if y not in D: return x
            x = y
    runs = []
    for k in range(L3):
        runs.append(top(tuple(k if i == cx else 0 for i in range(3)), a)); runs.append(top(tuple(k if i == cx else 0 for i in range(3)), b))
    bases = [x for x in D if x[cx] == 0]
    def runlen_c(x): t = top(x, cx); return t[cx] + 1, t
    def2 = 0
    for k in range(L3):
        for dirn in (a, b):
            t = top(tuple(k if i == cx else 0 for i in range(3)), dirn); def2 += (t[dirn] + 1)*(M - cells[t])
    for x in bases:
        t = top(x, cx); def2 += (t[cx] + 1)*(M - cells[t])
    ax = sum(k*p[cx] for k in range(L3))
    W = s.W if isinstance(s.W, int) else s.W()
    lhs = 3*m*W; rhs = (m - 4*L3)*M + 4*def2 + 4*ax - 3*m*(m - 1)
    assert lhs == rhs, (s.P, lhs, rhs)
    return dict(m=m, L3=L3, M=M, base=(m - 4*L3)*M + 4*ax - 3*m*(m - 1), def2=4*def2, W=W, c=s.c)
if __name__ == '__main__':
    R = []
    if sys.argv[1] == 'exh':
        for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
            for g3 in itertools.combinations(range(m + 1, int(sys.argv[4])*m), 3):
                if reduce(gcd, (m,) + g3) != 1: continue
                s = NS.from_generators([m, *g3])
                if s.e != 4: continue
                r = parts(s)
                if r: R.append(r)
    print('two-face semigroups', len(R), '(identity asserted for all)')
    good = [r for r in R if r['base'] >= 0]
    print('base part alone >= 0 (no Def2D needed):', len(good))
    bad = [r for r in R if r['base'] < 0]
    print('need Def2D:', len(bad), ' of which c <= 3m (Eliahou):', sum(r['c'] <= 3*r['m'] for r in bad))
    bb = [r for r in bad if r['c'] > 3*r['m']]
    print('need Def2D and c > 3m:', len(bb))
    for r in sorted(bb, key=lambda r: r['base']/(3*r['m']*(r['m'] - 1)))[:10]: print('   ', r, 'L3/m', round(r['L3']/r['m'], 2))
