# Decompose FWx = C(m,2) + Dp - F  (Dp = sum_deep (m + C(L,2)), F = sum_final R_j(L)); test candidate sub-claims on c > 3m.
import sys, time
sys.path.insert(0, 'src')
from math import comb
from ns import NS, all_by_genus
from cl import factorizations_down_set
def dec(s, order='grlex'):
    m, c = s.m, s.c
    Pp, best = factorizations_down_set(s, order)
    d = len(Pp); T = set(best.values()); lam = {x: w for w, x in best.items()}
    Dp = 0; F = 0; nfinal = 0; ndeep = 0
    for j in range(d):
        a = Pp[j]
        for x in T:
            if tuple(x[i] + (i == j) for i in range(d)) in T: continue
            L = x[j] + 1
            if lam[x] >= c: F += sum((r * a) % m for r in range(L)); nfinal += 1
            else: Dp += m + comb(L, 2); ndeep += 1
    return dict(m=m, c=c, d=d, C2=comb(m, 2), Dp=Dp, F=F, nf=nfinal, nd=ndeep, tau=nfinal // d)
G = int(sys.argv[1]); t0 = time.time()
n = 0; worstA = None; worstX = None; cnt = 0
for g, s in all_by_genus(G):
    if s.m < 3 or s.c <= 3 * s.m: continue
    r = dec(s); n += 1
    a = r['F'] / r['C2']; x = (r['C2'] + r['Dp'] - r['F']) / r['m']
    if worstA is None or a > worstA[0]: worstA = (round(a, 3), s.P, r)
    if worstX is None or x < worstX[0]: worstX = (round(x, 3), s.P, r)
    cnt += r['F'] > r['C2']
print(f'genus <= {G}, c > 3m: {n} S; #(F > C(m,2)) = {cnt}; max F/C(m,2) = {worstA}; min FWx/m = {worstX}; {time.time()-t0:.0f}s')
