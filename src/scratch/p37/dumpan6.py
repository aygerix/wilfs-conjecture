# DESC = W(S) - W(T) = PAY2 + (e - e_T) l_T on the residual; the e_T = e stratum (no bonus) in detail.
import sys
from fractions import Fraction as F
def Tdata(m, A):
    gens = sorted(A + [m]); N = 3 * m + 2
    inT = [False] * (N + 1); inT[0] = True
    for x in range(1, N + 1): inT[x] = any(x >= g and inT[x - g] for g in gens)
    cT = max(x for x in range(N + 1) if not inT[x]) + 1
    lT = sum(1 for x in range(cT) if inT[x])
    eT = sum(1 for g in gens if not any(inT[g - y] and inT[y] for y in range(1, g)))
    return cT, lT, eT
for fn in sys.argv[1:]:
    R = []
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            R.append(list(map(int, t[1:15])) + [list(map(int, t[15:]))])
    e = R[0][1]; d = e - 1
    full = []; desc = None; hist = {}
    for x in R:
        m, D3, h, hlo, hhi, dc, cT, A = x[0], x[2], x[4], x[5], x[6], x[9], x[12], x[14]
        _, lT, eT = Tdata(m, A)
        p2 = D3 + d * dc - e * h; ds = p2 + (e - eT) * lT
        hist[e - eT] = hist.get(e - eT, 0) + 1
        if desc is None or ds < desc[0]: desc = (ds, m, A, p2, eT, lT)
        if eT == e: full.append((D3 - e * hlo - hhi, F(e * hlo + hhi, D3), p2, m, A, D3, hlo, hhi, A[0]))
    print(fn, 'e', e, 'n', len(R), 'hist(e - e_T):', dict(sorted(hist.items())))
    print('   min DESC = W(S) - W(T) =', desc)
    if full:
        print('   e_T = e stratum:', len(full), 'S; min A1 slack', min(full)[0], 'at', min(full)[3:], '; max A1 ratio', float(max(f[1] for f in full)),
              '; min PAY2', min(f[2] for f in full), '; mu range', min(f[8] for f in full), max(f[8] for f in full))
