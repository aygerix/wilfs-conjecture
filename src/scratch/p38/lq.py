# lq: local test of D3 >= |Q3|.  For each standard square x (tile D), P(x) = sum_{i: x+e_i not in D} (x_i+1),
# c(x) = sum_{i: x+e_i in Q3} (x_i+1)  (Q3 = standard cubes with all pairwise sums >= m).  sum_x c(x) = 3|Q3|.
# LQ:  3 P(x) >= c(x) for every standard square x.   Report failures and the global numbers.
import sys
from itertools import combinations_with_replacement as cwr
tot = fails = 0; worst = None; gl = None
for fn in sys.argv[1:]:
    for L in open(fn):
        t = L.split()
        if t[0] != 'DUMP': continue
        m = int(t[1]); A = list(map(int, t[15:])); d = len(A); e = d + 1
        best = {}
        for k in range(4):
            for c in cwr(range(d), k):
                s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
                if cl not in best or key < best[cl][0]: best[cl] = (key, c)
        D = set(best[cl][1] for cl in best)
        h = {cl: len(best[cl][1]) for cl in best}
        D3 = 3 * (e - 1) * m - e * sum(h.values())
        val = lambda c: sum(A[i] for i in c)
        Q3 = set(c for c in D if len(c) == 3 and val(c) >= m and all(val(c) - A[i] >= m for i in c))
        P = {}; C = {}
        for x in D:
            if len(x) != 2: continue
            P[x] = C[x] = 0
            for i in range(d):
                y = tuple(sorted(x + (i,))); wgt = x.count(i) + 1
                if y not in D: P[x] += wgt
                elif y in Q3: C[x] += wgt
        assert sum(C.values()) == 3 * len(Q3)
        tot += 1
        bad = [(3 * P[x] - C[x], x) for x in P if 3 * P[x] < C[x]]
        if bad:
            fails += 1
            b = min(bad)
            if worst is None or b[0] < worst[0]: worst = (b[0], m, A, b[1], P[b[1]], C[b[1]], D3, len(Q3))
        r = len(Q3) / D3
        if gl is None or r > gl[0]: gl = (r, m, A, D3, len(Q3))
print(sys.argv[1], 'S', tot, 'LQ-fail S', fails, 'worst', worst, 'max |Q3|/D3', gl)
