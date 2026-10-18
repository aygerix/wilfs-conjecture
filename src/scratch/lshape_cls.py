# 3-class form of 2-D Tile-CL for L-shapes: classes Q=[0,a')x[0,b') (corner (a-1,b-1), outside D), R1=[a',a)x[0,b')
# (corner (a-1,b'-1)), R2=[0,a')x[b',b) (corner (a'-1,b-1)).  For x in class tau: r(t1)+r(t2)-r(x) = rho_tau + m eps(x).
# Tile-CL <=> sum_tau n_tau rho_tau + m sum eps <= m(m-1).
# CRUDE: eps = 1 => r(x) <= m-2-rho_tau.  Test  CC: sum_tau [n_tau rho_tau + m F_tau(m-2-rho_tau)] <= m(m-1).
import sys
sys.path.insert(0, 'src/scratch')
from lshape_tc import lshape_cells, valid_p
def run(MMAX):
    n = fails_cc = fails_tc = 0; worst = None
    for a in range(2, MMAX):
        for a2 in range(1, a):
            for b in range(2, MMAX):
                for b2 in range(1, b):
                    m = a*b2 + a2*(b - b2)
                    if m > MMAX: continue
                    cells = lshape_cells(a, a2, b, b2)
                    def corner(x, y):
                        return ((a - 1) if y < b2 else (a2 - 1), (b - 1) if x < a2 else (b2 - 1))
                    for p1, p2 in valid_p(cells, m):
                        for s in range(m):
                            R = lambda x, y: (x*p1 + y*p2 - s) % m
                            tot = 0; cc = 0; F = {}
                            for (x, y) in cells:
                                t = corner(x, y); rho = R(*t)
                                v = R(t[0], y) + R(x, t[1]) - R(x, y) - rho
                                assert v % m == 0
                                e = v // m
                                tot += rho + m*e
                                cc += rho + m*(R(x, y) <= m - 2 - rho)
                            n += 1
                            if tot > m*(m - 1): fails_tc += 1
                            if cc > m*(m - 1):
                                fails_cc += 1
                                ex = (cc - m*(m-1), m, (a, a2, b, b2), (p1, p2), s)
                                if worst is None or ex[0]/m > worst[0]/worst[1]: worst = ex
    print('MMAX', MMAX, 'cases', n, 'Tile-CL fails', fails_tc, 'CC fails', fails_cc, 'worst CC excess', worst)
run(int(sys.argv[1]))
