# q3t: Conjecture Q3T: D3 >= |Q3| + t  (Q3 = level-3 classes whose rep has all pairwise sums >= m = Q1' + M2').
# W = (D3 - |Q3| - t) + N_< + n3 + ov + (e-1)(r+1-t) asserted.  Also the rep-free Q3v (sigma - a not in Z2 for all a).
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
                if cl not in best or key < best[cl][0]: best[cl] = (key, c)
        w = {cl: best[cl][0][0] for cl in best}; rep = {cl: best[cl][1] for cl in best}; sg = {cl: w[cl] - len(rep[cl]) * m for cl in best}
        cS = max(w.values()) - m + 1; gS = sum(x // m for x in w.values()); W = e * (cS - gS) - cS
        D = set(rep.values()); val = lambda c: sum(A[i] for i in c)
        D3 = 3 * (e - 1) * m - e * sum(len(rep[cl]) for cl in best)
        Ds = [x for x in D if val(x) < m]; z = len(Ds); M2 = [c for c in range(m) if sg[c] >= 2 * m]; t = len(M2); r = max(M2)
        M1 = [c for c in range(m) if m <= sg[c] < 2 * m]
        Nlt = n3 = 0
        for x in Ds:
            for l in range(d):
                v = val(x) + A[l]
                if v < m: Nlt += 1
                elif not (tuple(sorted(x + (l,))) in D): n3 += 1
        hr = {c: len(set(l for l in rep[c] if A[l] > c)) for c in M1}
        Q1p = sum(1 for c in M1 if hr[c] == 0); ov = sum(hr[c] - 1 for c in M1 if hr[c] >= 2)
        Q3 = Q1p + t
        assert W == (D3 - Q3 - t) + Nlt + n3 + ov + (e - 1) * (r + 1 - t), (m, A)
        Z2 = set(val(x) for x in Ds if len(x) <= 2)
        Q3v = sum(1 for c in M1 if len(rep[c]) == 3 and not any(sg[c] - a in Z2 for a in A)) + t
        side = 'le' if mu <= e else 'gt'
        for key, v, mx in (('D3-Q3-t', D3 - Q3 - t, 0), ('(Q3+t)/D3', (Q3 + t) / D3, 1), ('(Q3v+t)/D3', (Q3v + t) / D3, 1)):
            kk = key + '_' + side
            if kk not in st or (v > st[kk][0] if mx else v < st[kk][0]): st[kk] = (v, m, A, D3, Q3, Q3v, t)
    print(fn, n, 'S (identity asserted)')
    for k in sorted(st): v = st[k]; print(f"   {k}: {v[0]:.3f}  m={v[1]} A={v[2]} D3,Q3,Q3v,t = {v[3:]}")
