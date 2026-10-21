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
    best = max(R, key=lambda x: F(e * x[5] + x[6], x[2]))
    bl = max(R, key=lambda x: F(e * x[5], x[2]))
    print(fn, 'e', e, 'n', len(R), 'max (e hlo + hhi)/D3 =', round(float(F(e * best[5] + best[6], best[2])), 4), 'at m', best[0], 'A', best[14], 'D3', best[2], 'hlo', best[5], 'hhi', best[6],
          '| max e hlo/D3 =', round(float(F(e * bl[5], bl[2])), 4), 'hlo', bl[5], 'D3', bl[2], '| max hlo', max(x[5] for x in R), '| min D3', min(x[2] for x in R),
          '| max h', max(x[4] for x in R), '| min A1', min(x[2] - e * x[5] - x[6] for x in R))
