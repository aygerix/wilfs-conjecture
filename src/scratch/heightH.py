# Shape-only criterion via heights: deficit(t) = M - w(t) >= p.(y - t) + (M - w(y)) >= (m+1)|y - t| + 1 for y >= t in D.
# ht(t) = max{|y - t| : y in D, y >= t};  H(D) = sum over incidences (x,a) of ht(t_a(x)).
# Def_all >= (m+1) H + 3m, so  (m+1) H + 3m >= m(m-1)  => Wilf  (any e = 4).   usage: heightH.py m0 m1 K
# CORRECTION (referee, 2026-10-18): the per-incidence '+1' above is FALSE (an incidence whose top is the Apery maximum has
# deficit 0), and the aggregate '+3m' is UNPROVED (it never failed in ~50k tests). The PROVED criterion is
# (m+1) H <= mW + m(m-1), i.e. H >= m-1 => Wilf, or H >= m-2 => Wilf by integrality (m >= 3). The slack 'sl' printed
# below still uses the unproved +3m; it is kept so that old logs reproduce. The e = 4 chain never uses it.
import sys, itertools
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def H_of(D):
    add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    def top(x, i):
        while add(x, i) in D: x = add(x, i)
        return x
    return sum(ht[top(x, i)] for x in D for i in range(3))
if __name__ == '__main__':
    m0, m1, K = map(int, sys.argv[1:4])
    for m in range(m0, m1 + 1):
        res = {True: None, False: None}; cnt = {True: 0, False: 0}; fails = {True: 0, False: 0}
        for g3 in itertools.combinations(range(m + 1, K*m), 3):
            if reduce(gcd, (m,) + g3) != 1: continue
            s = NS.from_generators([m, *g3])
            if s.e != 4: continue
            p, best = factorizations_down_set(s, 'grlex'); D = set(best.values())
            two = any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3))
            H = H_of(D); sl = (m + 1)*H + 3*m - m*(m - 1)
            cnt[two] += 1; fails[two] += sl < 0
            if res[two] is None or sl < res[two][0]: res[two] = (sl, [m, *g3], H)
        print(f'm={m}: non-two-face {cnt[False]} min slack {res[False]} fails {fails[False]} | two-face {cnt[True]} min slack {res[True]} fails {fails[True]}', flush=True)
