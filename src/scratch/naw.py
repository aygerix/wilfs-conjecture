# m W = sum over all (cell x, direction a) of (M - w(t_a x)) - (d-1) m(m-1)/2    (CH', D-columns)
# split: ARM = incidences whose column top is in X (top layer), NA = the rest (top below c: M - w(t) >= m).
# NAW:  NA >= (d-1) m(m-1)/2   (non-arm Wilf; positions of top cells not needed)
# CRD:  crude arm bound: NA + sum_u (l(u)+d)*0 ... ; also test  NA - m*N >= m(m-1-N)  i.e. Depth >= crude deficit.
import sys, itertools, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS, all_by_genus
from cl import factorizations_down_set
def split(s):
    m, c = s.m, s.c; d = s.e - 1; M = c + m - 1
    _, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}
    S = set(cells)
    ARM = NA = N = 0
    for x in cells:
        for a in range(d):
            t = x
            while True:
                y = t[:a] + (t[a] + 1,) + t[a+1:]
                if y in S: t = y
                else: break
            v = M - cells[t]
            if cells[t] >= c: ARM += v
            else: NA += v; N += 1
    need = (d - 1)*m*(m - 1)//2
    assert m*(s.W if isinstance(s.W, int) else s.W()) == ARM + NA - need
    return dict(m=m, d=d, ARM=ARM, NA=NA, N=N, need=need)
if __name__ == '__main__':
    mode = sys.argv[1]; res = []
    if mode == 'genus':
        for g, s in all_by_genus(int(sys.argv[2])):
            if g and s.e == 4: res.append((s.P, split(s)))
    elif mode == 'box':
        m0, m1, K = map(int, sys.argv[2:5])
        for m in range(m0, m1 + 1):
            for a, b, cc in itertools.combinations(range(m + 1, K*m), 3):
                if gcd(gcd(m, a), gcd(b, cc)) != 1: continue
                s = NS.from_generators([m, a, b, cc])
                if s.e == 4: res.append((s.P, split(s)))
    fails = [(P, r) for P, r in res if r['NA'] < r['need']]
    print(mode, 'e=4 semigroups', len(res), 'NAW fails', len(fails), ' fails with m>=20:', sum(1 for P, r in fails if r['m'] >= 20))
    byM = {}
    for P, r in fails: byM.setdefault(r['m'], []).append(P)
    print('  fails by m:', {k: len(v) for k, v in sorted(byM.items())})
    for P, r in sorted(fails, key=lambda t: -t[1]['m'])[:8]: print('   ', P, r, 'NA/need', round(r['NA']/r['need'], 3))
