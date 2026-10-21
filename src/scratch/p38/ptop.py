# ptop: P_top = sum over standard squares x of sum_{l : sigma(x) + a_l > Lambda} (x_l + 1)  (children above max sigma,
# all missing; a part of D3).  Compare with 2t and with E = (e+1)t - (e-1)(r+1).  Also P_top restricted to the
# parents of the top-layer reps (P_par).
import sys
from itertools import combinations_with_replacement as cwr
for fn in sys.argv[1:]:
    n = 0; st = {}
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
        D = set(rep.values()); val = lambda c: sum(A[i] for i in c)
        D3 = 3 * (e - 1) * m - e * sum(len(rep[cl]) for cl in best)
        Lam = max(sg.values()); r = Lam - 2 * m; M2 = [c for c in range(m) if sg[c] >= 2 * m]; t = len(M2)
        Ptop = 0; Ppar = 0; par = set()
        for c in M2:
            y = rep[c]
            for j in range(3): par.add(tuple(sorted(y[:j] + y[j + 1:])))
        for x in D:
            if len(x) != 2: continue
            p = sum(x.count(l) + 1 for l in range(d) if val(x) + A[l] > Lam)
            Ptop += p
            if x in par: Ppar += p
        E = (e + 1) * t - (e - 1) * (r + 1)
        for key, v in (('2t/Ptop', 2 * t / Ptop if Ptop else 99), ('2t/Ppar', 2 * t / Ppar if Ppar else 99), ('E/Ptop', E / Ptop if Ptop else (99 if E > 0 else 0)), ('Ptop/D3', Ptop / D3)):
            if key not in st or v > st[key][0]: st[key] = (v, m, A, t, r, Ptop, Ppar, D3)
    print(fn, n)
    for k in st: print('   max', k, '= %.3f' % st[k][0], 'm', st[k][1], 'A', st[k][2], 't,r,Ptop,Ppar,D3 =', st[k][3:])
