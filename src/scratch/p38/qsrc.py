# qsrc: which part of D3 = 4 M2 + sum_{small std squares} P + sum_{large std squares} P pays |Q'|, Q' = Z_m \ (Z + A').
# Asserts Q' (class form) = Q' (value form).  Reports max |Q'| / PL (PL = sum_{large sq} P) and |Q'| / (4M2 + PL).
import sys
from itertools import combinations_with_replacement as cwr
for fn in sys.argv[1:]:
    st = {}; n = 0
    for L in open(fn):
        t = L.split()
        if t[0] != 'DUMP': continue
        m = int(t[1]); A = list(map(int, t[15:])); d = len(A); e = d + 1; n += 1
        best = {}
        for k in range(4):
            for c in cwr(range(d), k):
                s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
                if cl not in best or key < best[cl][0]: best[cl] = (key, c)
        sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}
        D = set(best[cl][1] for cl in best); val = lambda c: sum(A[i] for i in c)
        Z = set(v for v in sg.values() if v < m)
        cover = set((z + a) % m for z in Z for a in [0] + A)
        Qc = set(range(m)) - cover
        Qv = set(cl for cl in sg if sg[cl] >= m and not any(sg[cl] - a in Z for a in A))
        assert Qc == Qv, (m, A)
        M2 = sum(1 for c in cwr(range(d), 2) if c not in D)
        PS = PL = 0
        for x in D:
            if len(x) != 2: continue
            p = sum(x.count(i) + 1 for i in range(d) if tuple(sorted(x + (i,))) not in D)
            if val(x) < m: PS += p
            else: PL += p
        D3 = 3 * (e - 1) * m - e * sum(len(best[cl][1]) for cl in best); assert D3 == 4 * M2 + PS + PL
        q = len(Qc)
        for key, num, den in (('Q/PL', q, PL), ('Q/(4M2+PL)', q, 4 * M2 + PL), ('Q/PS', q, PS), ('Q/D3', q, D3)):
            r = num / den if den else (99 if num else 0)
            if key not in st or r > st[key][0]: st[key] = (r, m, A, q, M2, PS, PL)
    print(fn, n)
    for k in st: print('   max', k, '= %.3f' % st[k][0], 'at m', st[k][1], 'A', st[k][2], "|Q'|,M2,PS,PL =", st[k][3:])
