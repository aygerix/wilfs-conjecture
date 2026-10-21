# idq: exact identity ID-Q  W = D3 + N - |Q1| + (e-1)(r+1) - (e+1) t   (N = N_< + N_ns + Ov = e z - m + |Q'|, |Q'| = t + |Q1|)
# asserted per S (W computed independently from the Apery set).  Reports min/max of the candidate sub-inequalities.
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
        w = {cl: best[cl][0] for cl in best}; h = {cl: -best[cl][1] for cl in best}; sg = {cl: w[cl] - h[cl] * m for cl in best}
        cS = max(w.values()) - m + 1; gS = sum(x // m for x in w.values()); W = e * (cS - gS) - cS
        D3 = 3 * (e - 1) * m - e * sum(h.values())
        Z = [c for c in range(m) if sg[c] < m]; z = len(Z); M2 = set(c for c in range(m) if sg[c] >= 2 * m); t = len(M2); r = max(M2)
        cover = set((x + a) % m for x in Z for a in [0] + A); Q = set(range(m)) - cover; assert M2 <= Q
        Q1 = len(Q) - t; N = e * z - m + len(Q)
        assert W == D3 + N - Q1 + (e - 1) * (r + 1) - (e + 1) * t, (m, A)
        E = (e + 1) * t - (e - 1) * (r + 1)
        side = 'le' if mu <= e else 'gt'
        for key, v, mx in (('t/(r+1)', t / (r + 1), 1), ('E/D3', E / D3, 1), ('N-Q1', N - Q1, 0), ('D3-Q1-2t', D3 - Q1 - 2 * t, 0), ('(Q1+2t)/D3', (Q1 + 2 * t) / D3, 1), ('(Q1+E)/D3', (Q1 + E) / D3, 1)):
            kk = key + '_' + side
            if kk not in st or (v > st[kk][0] if mx else v < st[kk][0]): st[kk] = (v, m, A, D3, t, r, Q1, N, z)
    print(fn, n, 'S (ID-Q asserted)')
    for k in sorted(st): v = st[k]; print(f"   {'max' if k.split('_')[0] in ('t/(r+1)','E/D3','(Q1+2t)/D3','(Q1+E)/D3') else 'min'} {k} = {v[0]:.3f}  m={v[1]} A={v[2]} D3,t,r,Q1,N,z = {v[3:]}")
