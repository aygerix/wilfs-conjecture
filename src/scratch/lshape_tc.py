# 2-D Tile-CL on L-shapes Omega = [0,a)x[0,b') u [0,a')x[0,b) (a' < a, b' < b) for every valid (p1,p2), every sigma:
#   X(sigma) = a sum_{v<b'} r(a-1,v) + a' sum_{b'<=v<b} r(a'-1,v) + b sum_{s<a'} r(s,b-1) + b' sum_{a'<=s<a} r(s,b'-1) <= 3M'.
# Also the 3-D two-face tile D = psi^{-1}(Omega) (p3 = p1+p2): MaxCL slack and the crude bracket
#   K(sigma) = M' - (2 sum_A r - dropped) (MaxCL slack = (3M' - X) + K).
import sys, random
def lshape_cells(a, a2, b, b2):
    return [(s, v) for s in range(a) for v in range(b) if v < b2 or s < a2]
def valid_p(cells, m):
    out = []
    for p1 in range(1, m):
        for p2 in range(1, m):
            if len({(s*p1 + v*p2) % m for s, v in cells}) == m: out.append((p1, p2))
    return out
def check(a, a2, b, b2, allp=True):
    cells = lshape_cells(a, a2, b, b2); m = len(cells); M = m*(m-1)//2
    Om = set(cells)
    rows = {}; cols = {}
    for (s, v) in cells:
        if (s + 1, v) not in Om: rows[(s, v)] = s + 1
        if (s, v + 1) not in Om: cols[(s, v)] = v + 1
    # 3-D maximal cells in the picture
    A = []
    for (s, v) in cells:
        if s > v and (s + 1, v) not in Om: A.append((s, v))
        elif s < v and (s, v + 1) not in Om: A.append((s, v))
        elif s == v and (s + 1, v) not in Om and (s, v + 1) not in Om: A.append((s, v))
    worst_tc = worst_k = worst_mx = 1.0
    ps = valid_p(cells, m)
    for p1, p2 in ps:
        for sg in range(m):
            r = {(s, v): (s*p1 + v*p2 - sg) % m for (s, v) in cells}
            X = sum(L*r[e] for e, L in rows.items()) + sum(L*r[t] for t, L in cols.items())
            lhs = sum((3 + max(s, v))*r[(s, v)] for (s, v) in A)
            worst_tc = min(worst_tc, (3*M - X)/(4*M)); worst_mx = min(worst_mx, (4*M - lhs)/(4*M))
            worst_k = min(worst_k, (4*M - lhs - (3*M - X))/(4*M))
    return m, len(ps), round(worst_tc, 4), round(worst_k, 4), round(worst_mx, 4)
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'exh':
        MMAX = int(sys.argv[2]); fails = 0; n = 0; mins = [1, 1, 1]
        for a in range(2, MMAX):
            for a2 in range(1, a):
                for b in range(2, MMAX):
                    for b2 in range(1, b):
                        m = a*b2 + a2*(b - b2)
                        if m > MMAX: continue
                        res = check(a, a2, b, b2)
                        if res[1] == 0: continue
                        n += 1
                        mins = [min(mins[0], res[2]), min(mins[1], res[3]), min(mins[2], res[4])]
                        if res[2] < 0: fails += 1; print('TILE-CL FAIL', (a, a2, b, b2), res, flush=True)
        print('L-shape tiles (shapes)', n, 'Tile-CL fails', fails, 'min [tc, crude bracket, maxcl3]', mins)
    else:
        rng = random.Random(int(sys.argv[2])); N = int(sys.argv[3]); MLO, MHI = int(sys.argv[4]), int(sys.argv[5]); n = 0; mins = [1, 1, 1]
        while n < N:
            a = rng.randint(2, 14); a2 = rng.randint(1, a - 1); b = rng.randint(2, 14); b2 = rng.randint(1, b - 1)
            m = a*b2 + a2*(b - b2)
            if not (MLO <= m <= MHI): continue
            res = check(a, a2, b, b2)
            if res[1] == 0: continue
            n += 1; mins = [min(mins[0], res[2]), min(mins[1], res[3]), min(mins[2], res[4])]
            if res[2] < 0: print('TILE-CL FAIL', (a, a2, b, b2), res, flush=True)
            if res[3] < 0: print('  crude bracket < 0', (a, a2, b, b2), res, flush=True)
        print('random L-shapes', n, 'min [tc, crude bracket, maxcl3]', mins)
