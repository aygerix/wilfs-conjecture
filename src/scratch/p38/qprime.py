# qprime: Q' = large standard values sigma_s >= m with (sigma_s - A) cap Z = empty;  Q3 = standard cubes whose pairwise
# sums are all >= m (superset of Q').  Compare with D3 (all mu / mu <= e).  Also the identity ZM: D3 + e z - m = D3 - |Q'| + N_< + N_ns + Ov.
import sys
from itertools import combinations_with_replacement as cwr
st = {}
for fn in sys.argv[1:]:
    for L in open(fn):
        t = L.split()
        if t[0] != 'DUMP': continue
        m = int(t[1]); A = list(map(int, t[15:])); d = len(A); e = d + 1; mu = A[0]
        best = {}
        for k in range(4):
            for c in cwr(range(d), k):
                s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
                if cl not in best or key < best[cl][0]: best[cl] = (key, c)
        assert len(best) == m
        sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}
        h = {cl: -best[cl][0][1] for cl in best}
        Z = set(v for v in sg.values() if v < m)
        D3 = 3 * (e - 1) * m - e * sum(h.values())
        Qp = [cl for cl in sg if sg[cl] >= m and not any(sg[cl] - a in Z for a in A)]
        Q3 = [cl for cl in sg if h[cl] == 3 and sg[cl] >= m and all(sum(A[best[cl][1][i]] for i in range(3) if i != j) >= m for j in range(3))]
        assert set(Qp) <= set(Q3) | set(cl for cl in sg if h[cl] == 3), (m, A)
        side = 'le' if mu <= e else 'gt'
        for key, val in (('D3-Qp_' + side, D3 - len(Qp)), ('D3-Q3_' + side, D3 - len(Q3)), ('ratioQp_' + side, len(Qp) / D3), ('ratioQ3_' + side, len(Q3) / D3)):
            if key not in st or ((val > st[key][0]) if key.startswith('ratio') else (val < st[key][0])): st[key] = (val, m, A, D3, len(Qp), len(Q3))
print(sys.argv[1])
for k in sorted(st): v = st[k]; print(f"  {k}: {v[0]:.3f}  m={v[1]} A={v[2]} D3={v[3]} |Q'|={v[4]} |Q3|={v[5]}")
