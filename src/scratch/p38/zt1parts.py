# zt1parts: ZT1 slack = e z + t - m = N_< + n3 + sum_{c in M1}(hit_rep(c) - 1)  (identity; n3 = #(x in D_s, l) with
# sigma(x)+a_l >= m and x + e_l not standard-in-D_1).  Lists the tightest S with the pieces.
import sys
from itertools import combinations_with_replacement as cwr
rows = []
for fn in sys.argv[1:]:
    for L in open(fn):
        tk = L.split()
        if tk[0] != 'DUMP': continue
        m = int(tk[1]); A = list(map(int, tk[15:])); d = len(A); e = d + 1
        best = {}
        for k in range(4):
            for c in cwr(range(d), k):
                s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
                if cl not in best or key < best[cl][0]: best[cl] = (key, c)
        sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}; rep = {cl: best[cl][1] for cl in best}
        D = set(rep.values()); val = lambda c: sum(A[i] for i in c)
        Ds = [x for x in D if val(x) < m]; z = len(Ds); t = sum(1 for c in sg if sg[c] >= 2 * m)
        M1 = [c for c in range(m) if m <= sg[c] < 2 * m]
        Nlt = n2 = n3 = 0
        for x in Ds:
            for l in range(d):
                v = val(x) + A[l]
                if v < m: Nlt += 1
                else:
                    y = tuple(sorted(x + (l,)))
                    if len(y) <= 3 and y in D: n2 += 1
                    else: n3 += 1
        hr = {c: len(set(l for l in rep[c] if A[l] > c)) for c in M1}
        assert n2 == sum(hr.values()), (m, A)
        Q1p = sum(1 for c in M1 if hr[c] == 0); ov = sum(hr[c] - 1 for c in M1 if hr[c] >= 2)
        sl = e * z + t - m; assert sl == Nlt + n3 + ov - Q1p, (m, A)
        rows.append((sl, m, A, Nlt, n3, ov, Q1p, z, len(M1), t))
rows.sort()
print(sys.argv[1], len(rows), 'S (identity asserted). tightest: slack, m, A, N_<, n3, ov, |Q1p|, z, |M1|, t')
for r in rows[:6]: print('  ', r)
