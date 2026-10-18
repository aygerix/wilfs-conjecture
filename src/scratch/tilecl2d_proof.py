# Verify the 2-D Tile-CL proof ingredients on ALL 2-D down-set tiles (exhaustive by m):
#  (i)  mu(x) = phi(x) + phi(tau(x)) is a bijection D -> Z/m        (corner-sum lemma)
#  (ii) eps(x) = (r(t1)+r(t2)-r(x)-r(tau))/m in {-1,0,1}, eps = 1 => r(x)+r(tau) <= m-2
#  (iii) exact slack formula  3M' - X(s) = m * sum_x ( [r(x)+r(tau x) <= m-2] - eps(x) )
#  (iv) only rectangles and L-shapes occur (<= 2 outer corners)
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
def run(M0, M1):
    for m in range(M0, M1 + 1):
        M = m*(m - 1)//2; nt = bad = 0; shapes = set()
        for D in downsets(m, 2):
            Dl = sorted(D)
            if any(all(n[a] == 0 for n in Dl) for a in range(2)): continue
            tau = tops(D, 2)
            corners = sum(1 for x in D if (x[0]+1, x[1]) not in D and (x[0], x[1]+1) not in D)
            for p1 in range(m):
                for p2 in range(m):
                    ph = {x: (x[0]*p1 + x[1]*p2) % m for x in D}
                    if len(set(ph.values())) != m: continue
                    nt += 1; shapes.add(corners)
                    mu = {(ph[x] + tau[x][0]*p1 + tau[x][1]*p2) % m for x in D}
                    if len(mu) != m: bad += 1; print('mu not bijective', Dl, p1, p2); continue
                    for s in range(m):
                        r = lambda y: (y[0]*p1 + y[1]*p2 - s) % m
                        X = 0; rhs = 0
                        for x in D:
                            t1 = (tau[x][0], x[1]); t2 = (x[0], tau[x][1]); T = tau[x]
                            v = r(t1) + r(t2) - r(x) - r(T); assert v % m == 0; e = v // m
                            assert e in (-1, 0, 1) and (e < 1 or r(x) + r(T) <= m - 2)
                            X += r(t1) + r(t2); rhs += (r(x) + r(T) <= m - 2) - e
                        assert 3*M - X == m*rhs, (Dl, p1, p2, s)
        print(f'm={m}: 2-D tiles {nt}, mu non-bijective {bad}, outer-corner counts {sorted(shapes)}: identities OK', flush=True)
if __name__ == '__main__':
    run(int(sys.argv[1]), int(sys.argv[2]))
