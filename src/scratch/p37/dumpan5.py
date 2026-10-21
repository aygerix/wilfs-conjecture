# A1 vs the bonus (e - e_T) l_T (and its bound (e - mu)^+ l_T, e_T <= mu): ratios r1 = (e h_lo + h_hi)/D3,
# r2 = (e h_lo + h_hi - (e - mu)^+ l_T)/D3, r3 = (e h_lo + h_hi - (e - e_T) l_T)/D3; recompute c_T independently.
import sys
from fractions import Fraction as F
def Tdata(m, A):
    gens = sorted(A + [m]); N = 3 * m + 2
    inT = [False] * (N + 1); inT[0] = True
    for x in range(1, N + 1): inT[x] = any(x >= g and inT[x - g] for g in gens)
    lastgap = max(x for x in range(N + 1) if not inT[x]); cT = lastgap + 1
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
    e = R[0][1]; best = [None] * 4; mins = [None, None]
    for x in R:
        m, D3, hlo, hhi, cT, A = x[0], x[2], x[5], x[6], x[12], x[14]
        cT2, lT, eT = Tdata(m, A)
        assert cT2 == cT, (m, A, cT, cT2)
        mu = A[0]; assert eT <= mu
        cost = e * hlo + hhi
        rs = [F(cost, D3), F(cost - max(e - mu, 0) * lT, D3), F(cost - (e - eT) * lT, D3)]
        for i in range(3):
            if best[i] is None or rs[i] > best[i][0]: best[i] = (rs[i], m, A, D3, hlo, hhi, lT, eT)
        s2 = D3 + max(e - mu, 0) * lT - cost
        if mins[0] is None or s2 < mins[0][0]: mins[0] = (s2, m, A, mu, lT)
        nb = sum(1 for y in R[:0])
    print(fn, 'e', e, 'n', len(R))
    for i, nm in enumerate(['A1 ratio', 'A1mu ratio (bonus (e-mu)+ lT)', 'A1T ratio (bonus (e-eT) lT)']):
        b = best[i]; print(f"   max {nm} = {float(b[0]):.4f} at m={b[1]} A={b[2]} D3={b[3]} hlo={b[4]} hhi={b[5]} lT={b[6]} eT={b[7]}")
    print('   min A1mu slack =', mins[0])
    print('   #S with mu < e:', sum(1 for x in R if x[14][0] < e), ' max A1 ratio among mu >= e:', float(max((F(e * x[5] + x[6], x[2]) for x in R if x[14][0] >= e), default=0)))
