# Inclusion-exclusion for 2-D L-shape Tile-CL:  X_D = X_{Om1} + X_{Om2} - X_Q  (Om1 = [0,a)x[0,b'), Om2 = [0,a')x[0,b),
# Q = Om1 cap Om2), X_B(s) = sum_{x in B} sum_a r(top^B_a x).  Per box: X_B - sum_B r = n_B rho_B + m * sum_B eps_B,
# rho_B = r(far corner of B), eps_B(x) in {-1,0,1}.  Tile-CL <=> U1 + U2 - UQ <= m(m-1), U_B = X_B - sum_B r.
import sys
sys.path.insert(0, 'src/scratch')
from lshape_tc import lshape_cells, valid_p
def box_data(B, k1, k2, r, m):
    kap = (k1 - 1, k2 - 1); rho = r[kap]
    eps = {}
    for (x1, x2) in B:
        v = r[(k1 - 1, x2)] + r[(x1, k2 - 1)] - r[(x1, x2)] - rho
        assert v % m == 0; eps[(x1, x2)] = v // m
    return rho, eps
def run(MMAX, verbose=False):
    n = 0; fails = 0; stats = {}
    for a in range(2, MMAX):
        for a2 in range(1, a):
            for b in range(2, MMAX):
                for b2 in range(1, b):
                    m = a*b2 + a2*(b - b2)
                    if m > MMAX: continue
                    cells = lshape_cells(a, a2, b, b2)
                    for p1, p2 in valid_p(cells, m):
                        for s in range(m):
                            r = {(x, y): (x*p1 + y*p2 - s) % m for (x, y) in cells}
                            O1 = [(x, y) for (x, y) in cells if y < b2]; O2 = [(x, y) for (x, y) in cells if x < a2]
                            Q = [(x, y) for (x, y) in cells if x < a2 and y < b2]
                            r1, e1 = box_data(O1, a, b2, r, m); r2, e2 = box_data(O2, a2, b, r, m); rq, eq = box_data(Q, a2, b2, r, m)
                            U = len(O1)*r1 + len(O2)*r2 - len(Q)*rq + m*(sum(e1.values()) + sum(e2.values()) - sum(eq.values()))
                            n += 1
                            if U > m*(m - 1): fails += 1
                            if verbose and U == m*(m-1):
                                print((a, a2, b, b2), (p1, p2), s, 'rho', r1, r2, rq, 'eps sums', sum(e1.values()), sum(e2.values()), sum(eq.values()),
                                      'sizes', len(O1), len(O2), len(Q))
    print('cases', n, 'fails', fails)
if __name__ == '__main__':
    run(int(sys.argv[1]), len(sys.argv) > 2)
