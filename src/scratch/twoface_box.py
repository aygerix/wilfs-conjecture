# Two-face box family: D = psi^{-1}([0,a) x [0,b)), psi(i,j,k) = (i+k, j+k) on {x1 x2 = 0}, p = (p1, p2, p1+p2).
# For every a, b <= AMAX and every (p1, p2) making the box a tile of Z/m (m = ab):
#   (1) MaxCL for the 3-D tile at every sigma (exact check);
#   (2) the proof's ingredients: Tile-CL of the 2-D box (X <= 3M'), weight domination, and the final bound
#       X + 2 sum_A r - (dropped tops) <= 4M'; report which (a,b) need the finite check (analytic bound fails).
import sys
from math import gcd
def run(a, b):
    m = a*b; M = m*(m - 1)//2
    D = [(i, 0, k) for k in range(b) for i in range(a - k) if i + k < a] + [(0, j, k) for k in range(min(a, b)) for j in range(1, b - k)]
    D = sorted(set(D)); assert len(D) == m, (a, b, len(D))
    S = set(D)
    A = [y for y in D if all(tuple(y[:t] + (y[t]+1,) + y[t+1:]) not in S for t in range(3))]
    res = []; ntile = 0
    for p1 in range(m):
        for p2 in range(m):
            box = {(s*p1 + v*p2) % m for s in range(a) for v in range(b)}
            if len(box) != m: continue
            ntile += 1
            p = (p1, p2, (p1 + p2) % m)
            phi = {x: sum(xi*pi for xi, pi in zip(x, p)) % m for x in D}
            assert len(set(phi.values())) == m
            worst = None
            for sg in range(m):
                r = {x: (phi[x] - sg) % m for x in D}
                lhs = sum((3 + sum(y))*r[y] for y in A)
                rr = lambda s, v: ((s*p1 + v*p2) - sg) % m
                X = sum(a*rr(a - 1, v) for v in range(b)) + sum(b*rr(s, b - 1) for s in range(a))
                if X > 3*M: return ('TILE-CL FAIL', a, b, p1, p2, sg)
                if lhs > 4*M: return ('MAXCL FAIL', a, b, p1, p2, sg)
                sl = (4*M - lhs)/(4*M)
                worst = sl if worst is None else min(worst, sl)
            res.append(worst)
    return ntile, (round(min(res), 4) if res else None)
AMAX = int(sys.argv[1])
for a in range(2, AMAX + 1):
    for b in range(2, AMAX + 1):
        out = run(a, b)
        print('a', a, 'b', b, out, flush=True)
