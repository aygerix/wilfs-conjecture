# min D3/h overall and by e_T (mu) stratum; D3 >= c*h candidates; A1-eT0 (D3 >= e_T h_lo + h_hi) ratio
import sys
from fractions import Fraction as F
for fn in sys.argv[1:]:
    R = []
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            R.append(list(map(int, t[1:15])) + [list(map(int, t[15:]))])
    e = R[0][1]
    mn = min(R, key=lambda x: F(x[2], x[4]))
    bymu = {}
    for x in R:
        mu = x[14][0]; r = F(x[2], x[4]); bymu[mu] = min(bymu.get(mu, r), r)
    a0 = max(R, key=lambda x: F(min(e, x[14][0]) * x[5] + x[6], x[2]))
    print(fn, 'e', e, 'min D3/h =', round(float(F(mn[2], mn[4])), 3), 'at m', mn[0], 'A', mn[14], 'D3', mn[2], 'h', mn[4], 'ne2/ne3', mn[7], mn[8])
    print('   min D3/h by mu:', {k: round(float(v), 2) for k, v in sorted(bymu.items())})
    print('   max (min(e,mu) h_lo + h_hi)/D3 =', round(float(F(min(e, a0[14][0]) * a0[5] + a0[6], a0[2])), 4), 'at m', a0[0], 'A', a0[14])
