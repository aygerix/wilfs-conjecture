# zt1inj: ZT1 (e z >= m - t) via the injection M1 \ Q1' -> Z x A, c -> (sigma_c - a_k, k), a_k = largest part of rep(c).
# Q1' = {c in M1 : a_k <= c}.  Unused pairs >= N_< (pairs (z', a) with z' + a < m).  Test N_< >= |Q1'| and the slack.
import sys
from itertools import combinations_with_replacement as cwr
for fn in sys.argv[1:]:
    n = 0; st = {}; fails = 0
    for L in open(fn):
        tk = L.split()
        if tk[0] != 'DUMP': continue
        m = int(tk[1]); A = list(map(int, tk[15:])); d = len(A); e = d + 1; n += 1
        best = {}
        for k in range(4):
            for c in cwr(range(d), k):
                s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
                if cl not in best or key < best[cl][0]: best[cl] = (key, c)
        sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}; rep = {cl: best[cl][1] for cl in best}
        Z = sorted(c for c in range(m) if sg[c] < m); Zs = set(Z)
        M1 = [c for c in range(m) if m <= sg[c] < 2 * m]
        Q1p = [c for c in M1 if A[max(rep[c])] <= c]
        Nlt = sum(1 for x in Z for a in A if x + a < m)
        # injection check
        img = set()
        for c in M1:
            if c in Q1p: continue
            k = max(rep[c]); zz = sg[c] - A[k]; assert zz in Zs, (m, A, c); assert (zz, k) not in img; img.add((zz, k))
        hr = {c: len(set(l for l in rep[c] if A[l] > c)) for c in M1}
        extra = sum(hr[c] - 1 for c in M1 if hr[c] >= 2)
        sq = sum(1 for c in M1 if len(rep[c]) == 2 and rep[c][0] != rep[c][1])
        slR = Nlt + extra - len(Q1p)
        if slR < 0: print('Q1R FAIL', m, A, flush=True)
        for key, v in (('Q1R', slR), ('Q1R-noN', extra - len(Q1p)), ('sqd-Q1p', sq - len(Q1p))):
            if key not in st or v < st[key][0]: st[key] = (v, m, A, len(Q1p), Nlt, len(Z), len(M1))
        sl = Nlt - len(Q1p)
        if sl < 0: fails += 1
        for key, v in (('Nlt-Q1p', sl), ('Q1p', -len(Q1p))):
            if key not in st or v < st[key][0]: st[key] = (v, m, A, len(Q1p), Nlt, len(Z), len(M1))
    print(fn, n, 'S; N_< < |Q1\'| on', fails)
    for k in st: print('   min', k, '=', st[k][0], 'm', st[k][1], 'A', st[k][2], "|Q1'|,N_<,z,|M1| =", st[k][3:])
