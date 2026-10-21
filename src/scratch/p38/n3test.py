# n3test: sufficient conditions for Q3T (D3 >= |Q3| + t):  N3: D3 >= 2 n3;  L3: D3 >= 2 L3;  LT: D3 >= L3 + t.
import sys
from itertools import combinations_with_replacement as cwr
for fn in sys.argv[1:]:
    n = 0; st = {}
    for L in open(fn):
        tk = L.split()
        if tk[0] != 'DUMP': continue
        m = int(tk[1]); A = list(map(int, tk[15:])); d = len(A); e = d + 1; mu = A[0]; n += 1
        best = {}
        for k in range(4):
            for c in cwr(range(d), k):
                s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
                if cl not in best or key < best[cl]: best[cl] = key
        h = {cl: -best[cl][1] for cl in best}; sg = {cl: best[cl][0] - h[cl] * m for cl in best}
        D3 = 3 * (e - 1) * m - e * sum(h.values())
        n3 = sum(1 for c in h if h[c] == 3); L3 = sum(1 for c in h if h[c] == 3 and sg[c] >= m); t = sum(1 for c in h if sg[c] >= 2 * m)
        side = 'le' if mu <= e else 'gt'
        for key, v in (('2n3/D3', 2 * n3 / D3), ('2L3/D3', 2 * L3 / D3), ('(L3+t)/D3', (L3 + t) / D3)):
            kk = key + '_' + side
            if kk not in st or v > st[kk][0]: st[kk] = (v, m, A, D3, n3, L3, t)
    print(fn, n)
    for k in sorted(st): v = st[k]; print(f"   max {k} = {v[0]:.3f}  m={v[1]} A={v[2]} D3,n3,L3,t = {v[3:]}")
