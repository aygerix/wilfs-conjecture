# d = 3: eps(x) = eps_ab(x) + eps'_c(x) for each c (a,b the other two):
#   eps_ab = (r(t_a)+r(t_b)-r(x)-r(tau_ab))/m  (slice face at x),  eps'_c = (r(tau_ab)+r(t_c)-r(x)-r(tau))/m (diagonal rect).
# Tile-CL <=> sum eps <= T(s) = sum_x (m-1-r(tau x))/m.  Collect: max over (tile,s) of
#   min_c [E_ab]  ,  max_c [E'_c - T],  and whether  for some c: E_ab <= 0 and E'_c <= T.
import sys
import numpy as np
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    K = np.arange(m)
    nt = 0; stats = {'minEab_max': -99, 'Eprime_minus_T_max': -99, 'no_good_c': 0, 'cases': 0, 'Eab_all_pos': 0}
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        ok = np.all(np.sort(pos, axis=1) == K, axis=1)
        if not ok.any(): continue
        tau = tops(D, d); Tau = np.array([tau[x] for x in Dl])
        Ta = [np.array([tuple(x[:a]) + (tau[x][a],) + tuple(x[a+1:]) for x in Dl]) for a in range(d)]
        Tab = {}
        for c in range(d):
            a, b = [i for i in range(d) if i != c]
            V = C.copy(); V[:, a] = Tau[:, a]; V[:, b] = Tau[:, b]; Tab[c] = V
        for pv in P[ok]:
            nt += 1
            for s in range(m):
                r = lambda Y: (Y @ pv - s) % m
                u = r(C); v = r(Tau); A = [r(Ta[a]) for a in range(d)]
                Tm = m*(m - 1) - v.sum()
                Eab = []; Ep = []
                for c in range(d):
                    a, b = [i for i in range(d) if i != c]
                    F = r(Tab[c])
                    e1 = A[a] + A[b] - u - F; e2 = F + A[c] - u - v
                    assert np.all(e1 % m == 0) and np.all(e2 % m == 0)
                    Eab.append(e1.sum()//m); Ep.append(e2.sum())
                stats['cases'] += 1
                stats['minEab_max'] = max(stats['minEab_max'], min(Eab))
                stats['Eprime_minus_T_max'] = max(stats['Eprime_minus_T_max'], (max(Ep) - Tm)/m)
                if all(e > 0 for e in Eab): stats['Eab_all_pos'] += 1
                if not any(Eab[c] <= 0 and Ep[c] <= Tm for c in range(d)): stats['no_good_c'] += 1
    print(f'm={m} tiles {nt}', stats, flush=True)
