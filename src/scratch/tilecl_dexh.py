# Exhaustive Tile-CL for d = 3: all non-degenerate down-sets D of size m in N^3, all p in (Z/m)^3 bijective on D, all s.
# Tile-CL: min_s sum_k k * w[(s - k) mod m] >= (d-1) M'  (w[r] = T of the cell at residue r).  numpy-vectorized over p.
import sys, time
import numpy as np
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets, Tvals
d = int(sys.argv[3]) if len(sys.argv) > 3 else 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    t0 = time.time(); target = (d - 1)*m*(m - 1)//2
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T  # (m^3, 3)
    K = np.arange(m)
    nD = nP = fails = 0; tight = 0; ex = []
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
        nD += 1
        C = np.array(Dl)
        pos = (P @ C.T) % m                                  # (m^3, m)
        ok = np.all(np.sort(pos, axis=1) == K, axis=1)
        if not ok.any(): continue
        T = Tvals(D, d); Tv = np.array([T[n] for n in Dl])
        for row in pos[ok]:
            nP += 1
            w = np.zeros(m, dtype=np.int64); w[row] = Tv
            # f(s) = sum_k k * w[(s-k) mod m] for all s
            f = np.array([np.dot(K, w[(s - K) % m]) for s in range(m)])
            mn = f.min()
            if mn < target:
                fails += 1
                if len(ex) < 3: ex.append((Dl, mn, target))
            elif mn == target: tight += 1
    print(f'd={d} m={m}: downsets {nD}, tiles (D,p) {nP}, Tile-CL failures {fails}, tight {tight}', ex[:1], f'{time.time()-t0:.0f}s', flush=True)
