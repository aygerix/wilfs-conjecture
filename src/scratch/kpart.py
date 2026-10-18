# k-part CL: partition [d] = S_1 ⊔ ... ⊔ S_k; tau_S(x) = x with coords in S replaced by tops t_a(x).
#   Y = sum_x sum_i r(tau_{S_i} x) <= (k+1) M'  ?   (k = d: Tile-CL; k = 2: P1)
import sys, itertools
import numpy as np
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
def set_partitions(lst):
    if not lst: yield []; return
    first, rest = lst[0], lst[1:]
    for p in set_partitions(rest):
        for i in range(len(p)): yield p[:i] + [[first] + p[i]] + p[i+1:]
        yield [[first]] + p
d = int(sys.argv[1])
parts = [p for p in set_partitions(list(range(d))) if len(p) >= 2]
for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
    M = m*(m-1)//2
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    K = np.arange(m)
    worst = {}; nt = 0
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        ok = np.all(np.sort(pos, axis=1) == K, axis=1)
        if not ok.any(): continue
        tau = tops(D, d); Tau = np.array([tau[x] for x in Dl])
        Pk = P[ok]; nt += len(Pk)
        for pa in parts:
            k = len(pa); tot = np.zeros((len(Pk), m), dtype=np.int64)
            for S in pa:
                V = C.copy(); V[:, S] = Tau[:, S]
                y = (Pk @ V.T) % m                       # (tiles, cells)
                for s in range(m): tot[:, s] += ((y - s) % m).sum(axis=1)
            w = (tot.max() - (k + 1)*M) / m
            key = tuple(sorted(len(S) for S in pa))
            worst[key] = max(worst.get(key, -10**9), w)
    print(f'd={d} m={m} tiles {nt}: max (Y-(k+1)M\')/m by part sizes', dict(sorted(worst.items())), flush=True)
