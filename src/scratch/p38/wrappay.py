# wrappay: WP := (missing wrap slots of large standard squares) - (2t + |Q1'|)  [wrap slot = (x, l), sigma(x) + a_l >= 2m,
# weight x_l + 1; standard wrap slots = 3t exactly (asserted)].  Also K2 = #cube monomials with value >= 2m vs t.
import sys
from itertools import combinations_with_replacement as cwr
for fn in sys.argv[1:]:
    n = 0; st = {}; fails = 0
    for L in open(fn):
        tk = L.split()
        if tk[0] != 'DUMP': continue
        m = int(tk[1]); A = list(map(int, tk[15:])); d = len(A); e = d + 1; mu = A[0]; n += 1
        best = {}
        for k in range(4):
            for c in cwr(range(d), k):
                s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
                if cl not in best or key < best[cl][0]: best[cl] = (key, c)
        sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}; rep = {cl: best[cl][1] for cl in best}
        D = set(rep.values()); val = lambda c: sum(A[i] for i in c)
        D3 = 3 * (e - 1) * m - e * sum(len(rep[c]) for c in rep)
        t = sum(1 for c in sg if sg[c] >= 2 * m)
        M1 = [c for c in range(m) if m <= sg[c] < 2 * m]
        Q1p = sum(1 for c in M1 if not any(A[l] > c for l in rep[c]))
        ws = wm = 0
        for x in D:
            if len(x) != 2 or val(x) < m: continue
            for l in range(d):
                if val(x) + A[l] < 2 * m: continue
                wt = x.count(l) + 1
                if tuple(sorted(x + (l,))) in D: ws += wt
                else: wm += wt
        assert ws == 3 * t, (m, A, ws, t)
        K2 = sum(1 for c in cwr(range(d), 3) if val(c) >= 2 * m)
        wp = wm - 2 * t - Q1p
        if wp < 0: fails += 1
        side = 'le' if mu <= e else 'gt'
        for key, v, mx in (('K2-2t', K2 - 2 * t, 0), ('wm-2t', wm - 2 * t, 0), ('WP', wp, 0), ('(2t+Q1p)/wm', (2 * t + Q1p) / wm if wm else (99 if t else 0), 1), ('t/K2', t / K2 if K2 else 0, 1)):
            kk = key + '_' + side
            if kk not in st or (v > st[kk][0] if mx else v < st[kk][0]): st[kk] = (v, m, A, wm, t, Q1p, K2, D3)
    print(fn, n, 'S; WP < 0 on', fails)
    for k in sorted(st): v = st[k]; print(f"   {k}: {v[0]:.3f}  m={v[1]} A={v[2]} wm,t,Q1p,K2,D3 = {v[3:]}")
