# qsplit: Q' = Z_m \ (Z + A') split by eta: Q1 = Q' cap M1 (m <= sigma < 2m), Q2 = Q' cap M2' (sigma >= 2m), t = |M2'|.
# Reports: max |Q1|, max |Q1|/D3, how often Q2 = M2', max (t - |Q2|), max t/D3, max (|Q1| + t)/D3.
import sys
from itertools import combinations_with_replacement as cwr
for fn in sys.argv[1:]:
    n = q2full = 0; st = {}
    for L in open(fn):
        tk = L.split()
        if tk[0] != 'DUMP': continue
        m = int(tk[1]); A = list(map(int, tk[15:])); d = len(A); e = d + 1; mu = A[0]; n += 1
        best = {}
        for k in range(4):
            for c in cwr(range(d), k):
                s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
                if cl not in best or key < best[cl]: best[cl] = key
        sg = {cl: best[cl][0] + best[cl][1] * m for cl in best}
        D3 = 3 * (e - 1) * m - e * sum(-best[cl][1] for cl in best)
        Z = [c for c in range(m) if sg[c] < m]; M2 = set(c for c in range(m) if sg[c] >= 2 * m); t = len(M2)
        cover = set((z + a) % m for z in Z for a in [0] + A); Q = set(range(m)) - cover
        Q2 = Q & M2; Q1 = Q - M2
        if Q2 == M2: q2full += 1
        side = 'le' if mu <= e else 'gt'
        for key, v in (('Q1', len(Q1)), ('Q1/D3', len(Q1) / D3), ('t-Q2', t - len(Q2)), ('t/D3', t / D3), ('(Q1+t)/D3', (len(Q1) + t) / D3)):
            kk = key + '_' + side
            if kk not in st or v > st[kk][0]: st[kk] = (v, m, A, len(Q1), len(Q2), t, D3)
    print(fn, n, 'S; Q2 = M2\' on', q2full)
    for k in sorted(st): v = st[k]; print(f"   max {k} = {v[0]:.3f} at m={v[1]} A={v[2]} |Q1|,|Q2|,t,D3 = {v[3:]}")
