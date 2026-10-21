# DESC decomposition: W(S) - W(T) = D3 + (e-1)u' + rho*|U n [0,cT)| - e_T*h_lo - h_hi  (rho = e - e_T).
# A1-eT: D3 + rho*|U n [0,cT)| >= e_T*h_lo + h_hi (drops (e-1)u').  Reports min slack, max ratio, and the identity check.
import sys
from fractions import Fraction as F
def data(m, A):
    gens = sorted(A + [m]); N = 3 * m + 2
    inT = [False] * (N + 1); inT[0] = True
    for x in range(1, N + 1): inT[x] = any(x >= g and inT[x - g] for g in gens)
    cT = max(x for x in range(N + 1) if not inT[x]) + 1
    lT = sum(1 for x in range(cT) if inT[x])
    eT = sum(1 for g in gens if not any(inT[g - y] and inT[y] for y in range(1, g)))
    # U = 3A' + mN : sigma per class
    from itertools import combinations_with_replacement as cwr
    sig = {}
    for k in range(4):
        for c in cwr(A, k):
            v = sum(c); s = v % m
            if s not in sig or v < sig[s]: sig[s] = v
    inU = lambda x: x >= sig[x % m]
    lUlo = sum(1 for x in range(cT) if inU(x))
    return cT, lT, eT, lUlo, sig
for fn in sys.argv[1:]:
    R = []
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            R.append(list(map(int, t[1:15])) + [list(map(int, t[15:]))])
    e = R[0][1]; d = e - 1; best = None; mins = None; dmin = None
    for x in R:
        m, D3, h, hlo, hhi, dc, cT, r, A = x[0], x[2], x[4], x[5], x[6], x[9], x[12], x[13], x[14]
        cT2, lT, eT, lUlo, sig = data(m, A); assert cT2 == cT
        rho = e - eT; up = dc - hhi
        desc = D3 + d * dc - e * h + rho * lT
        assert desc == D3 + d * up + rho * lUlo - eT * hlo - hhi, (m, A)
        sl = D3 + rho * lUlo - eT * hlo - hhi; rat = F(eT * hlo + hhi - rho * lUlo, D3)
        if mins is None or sl < mins[0]: mins = (sl, m, A, D3, eT, hlo, hhi, lUlo)
        if best is None or rat > best[0]: best = (rat, m, A, D3, eT, hlo, hhi, lUlo)
        if dmin is None or desc < dmin[0]: dmin = (desc, m, A)
    print(fn, 'e', e, 'n', len(R), '| min DESC', dmin, '| min A1-eT slack', mins, '| max A1-eT ratio', round(float(best[0]), 4), best[1:])
