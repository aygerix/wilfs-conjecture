# d=3 coupling inequality.  Exact identity: X_a + X_b = sum_x H(w_ab x) - m*#{x : r(t_a x)+r(t_b x) <= m-2},
# w_ab = <r(t_a)+r(t_b)>, H(w) = w+m (w<=m-2), m-1 (w=m-1).  Tile-CL <=> X_c - m*Q_ab <= 4M' - sum H(w_ab).
# CI_c (the form when mu_ab is bijective):  E_c := X_c - M' <= m * Q_ab,  Q_ab = #{x : r(t_a x)+r(t_b x) <= m-2}.
import sys
import numpy as np
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    M = m*(m-1)//2
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    K = np.arange(m)
    nt = 0; ci_fail = 0; ci_worst = -10**9; extra_worst = -10**9
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        ok = np.all(np.sort(pos, axis=1) == K, axis=1)
        if not ok.any(): continue
        tau = tops(D, d)
        Ta = [np.array([tuple(x[:a]) + (tau[x][a],) + tuple(x[a+1:]) for x in Dl]) for a in range(d)]
        for pv in P[ok]:
            nt += 1
            tp = [(Ta[a] @ pv) % m for a in range(d)]
            for s in range(m):
                A = [(t - s) % m for t in tp]
                for c in range(d):
                    a, b = [i for i in range(d) if i != c]
                    Q = int((A[a] + A[b] <= m - 2).sum())
                    Ec = int(A[c].sum()) - M
                    v = (Ec - m*Q) / m
                    ci_worst = max(ci_worst, v)
                    if v > 0: ci_fail += 1
    print(f'm={m} tiles {nt}: CI_c failures {ci_fail}, max (E_c - mQ_ab)/m = {ci_worst}', flush=True)
