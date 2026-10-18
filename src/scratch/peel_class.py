# Exhaustive over the class C = all q*-free cylindrical sets D = {x2 < h(x1), x3 < min(f(x1), g(x2))} (any L >= 1,
# two-face and degenerate allowed), |D| <= M.  Per size m: min defect H-(m-1), min max_c Psi_c, min sum_c Psi_c.
# (C is closed under peeling D -> {x : x + e_c in D}.)   usage: peel_class.py M
import sys
sys.path.insert(0, 'src/scratch')
from heightH import H_of
from peel_test import psis
def stairs(L, top):
    def rec(prefix):
        if len(prefix) == L: yield tuple(prefix); return
        for v in range(prefix[-1], 0, -1): yield from rec(prefix + [v])
    yield from rec([top])
M = int(sys.argv[1]); res = {}
for L1 in range(1, M + 1):
    for L2 in range(1, M + 1):
        if L1 + L2 - 1 > M: break
        for L3 in range(1, M + 1):
            if L1 + L2 + L3 - 2 > M: break
            for h in stairs(L1, L2):
                if sum(h) + L3 - 1 > M: continue
                for f in stairs(L1, L3):
                    for g in stairs(L2, L3):
                        m = sum(min(f[i], g[j]) for i in range(L1) for j in range(h[i]))
                        if m > M: continue
                        D = {(i, j, k) for i in range(L1) for j in range(h[i]) for k in range(min(f[i], g[j]))}
                        dfc = H_of(D) - (m - 1); ps = psis(D)
                        r = res.get(m, [0, None, None, None])
                        r[0] += 1
                        if r[1] is None or dfc < r[1][0]: r[1] = (dfc, (h, f, g))
                        if r[2] is None or max(ps) < r[2][0]: r[2] = (max(ps), (h, f, g))
                        if r[3] is None or sum(ps) < r[3][0]: r[3] = (sum(ps), (h, f, g))
                        res[m] = r
for m in sorted(res):
    r = res[m]; print(m, 'count', r[0], 'min defect', r[1][0], 'min maxPsi', r[2][0], r[2][1], 'min sumPsi', r[3][0], flush=True)
