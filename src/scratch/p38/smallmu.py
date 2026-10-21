# smallmu: on residual S with mu <= (e+1)/2: max |Q1'|, max |Q1'|/D3, and the slack W - (D3 - |Q1'|) decomposition check.
import sys
from itertools import combinations_with_replacement as cwr
for fn in sys.argv[1:]:
    n = 0; worst = None; nz = 0; mx = 0
    for L in open(fn):
        tk = L.split()
        if tk[0] != 'DUMP': continue
        m = int(tk[1]); A = list(map(int, tk[15:])); d = len(A); e = d + 1; mu = A[0]
        if 2 * mu > e + 1: continue
        n += 1
        best = {}
        for k in range(4):
            for c in cwr(range(d), k):
                s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
                if cl not in best or key < best[cl][0]: best[cl] = (key, c)
        sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}; rep = {cl: best[cl][1] for cl in best}
        D3 = 3 * (e - 1) * m - e * sum(len(rep[c]) for c in rep)
        M1 = [c for c in range(m) if m <= sg[c] < 2 * m]
        Q1p = [c for c in M1 if not any(A[l] > c for l in rep[c])]
        if Q1p: nz += 1
        mx = max(mx, len(Q1p))
        if worst is None or len(Q1p) / D3 > worst[0]: worst = (len(Q1p) / D3, m, A, D3, [(c, tuple(A[i] for i in rep[c])) for c in Q1p])
    print(fn, 'mu <= (e+1)/2:', n, 'S; Q1p nonempty on', nz, '; max |Q1p| =', mx, '; worst', worst)
