# d = 3 tiles: per-cell carry eps(x) = (sum_a r(t_a x) - 2 r(x) - r(tau x))/m in [-2,2];
# Tile-CL <=> sum_x eps <= T(s) := sum_x (m-1-r(tau x))/m.  Tabulate joint law of (eps, [u+v<=m-2]) and the
# mu-discrepancy A(s) = sum_x [u+v<=m-2] - T(s).
import sys
from collections import Counter
import numpy as np
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    K = np.arange(m)
    joint = Counter(); Adist = Counter(); nt = 0; pos_eps2 = 0
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        ok = np.all(np.sort(pos, axis=1) == K, axis=1)
        if not ok.any(): continue
        tau = tops(D, d); Tau = np.array([tau[x] for x in Dl])
        tops_idx = [[Dl.index(tuple(x[:a]) + (tau[x][a],) + tuple(x[a+1:])) for x in Dl] for a in range(d)]
        for pv in P[ok]:
            nt += 1
            ph = (C @ pv) % m; pt = (Tau @ pv) % m
            for s in range(m):
                u = (ph - s) % m; v = (pt - s) % m
                S = sum(u[tops_idx[a]] for a in range(d))
                q = S - 2*u - v; assert np.all(q % m == 0); e = q // m
                ind = (u + v <= m - 2).astype(int)
                for ee, ii in zip(e, ind): joint[(int(ee), int(ii))] += 1
                Tm = (m*(m - 1) - v.sum())          # m*T
                A = m*ind.sum() - Tm
                Adist[A / m] += 1
                assert m*e.sum() <= Tm
    print(f'm={m} tiles {nt}: joint (eps,[u+v<=m-2]) {dict(sorted(joint.items()))}')
    print('   A(s) distribution (min, max):', min(Adist), max(Adist), flush=True)
