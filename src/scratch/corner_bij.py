# Is the "corner sum" map  mu(x) = phi(x) + phi(tau(x))  a bijection D -> Z/m ?  tau(x) = (t_1(x),...,t_d(x)),
# t_a(x) = a-coordinate of the top of the a-column through x (tau(x) may lie outside D).
# Also the general-d variant  mu_k(x) = k*phi(x) + phi(tau(x))  for k = 1..d-1  (d-1 is what the eps-identity uses).
import sys, itertools
import numpy as np
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
def tops(D, d):
    tau = {}
    for x in D:
        t = []
        for a in range(d):
            y = list(x)
            while tuple(y[:a] + [y[a] + 1] + y[a+1:]) in D: y[a] += 1
            t.append(y[a])
        tau[x] = tuple(t)
    return tau
if __name__ == '__main__':
    d = int(sys.argv[1]); M0, M1 = int(sys.argv[2]), int(sys.argv[3])
    for m in range(M0, M1 + 1):
        P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
        K = np.arange(m)
        stats = {k: [0, 0] for k in range(1, d)}; nt = 0
        for D in downsets(m, d):
            Dl = sorted(D)
            if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
            C = np.array(Dl); pos = (P @ C.T) % m
            ok = np.all(np.sort(pos, axis=1) == K, axis=1)
            if not ok.any(): continue
            tau = tops(D, d); Tc = np.array([tau[x] for x in Dl])
            tpos = (P[ok] @ Tc.T) % m
            for k in range(1, d):
                mu = (k*pos[ok] + tpos) % m
                bij = np.all(np.sort(mu, axis=1) == K, axis=1)
                stats[k][0] += bij.sum(); stats[k][1] += len(bij)
            nt += ok.sum()
        print(f'd={d} m={m} tiles {nt}', {k: f'{v[0]}/{v[1]} bijective' for k, v in stats.items()}, flush=True)
