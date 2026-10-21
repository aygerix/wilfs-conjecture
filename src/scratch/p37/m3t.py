import sys
from fractions import Fraction as F
for fn in sys.argv[1:]:
    best = None; cnt = 0
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            v = list(map(int, t[1:15])); m, e, ne2, ne3, n3eq = v[0], v[1], v[7], v[8], v[11]; d = e - 1
            if ne3 == 0: continue
            cnt += 1
            M3T = d * (d + 1) * (d + 2) // 6 - n3eq
            r = F(M3T - ne3, ne3)
            if best is None or r < best[0]: best = (r, m, list(map(int, t[15:])), M3T, ne3, ne2)
    print(fn, 'S with NE3:', cnt, 'min (M3T - |NE3|)/|NE3| =', float(best[0]), best[1:])
