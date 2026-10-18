# Two-face 3-D tiles (x1*x2 = 0 on D): face-wise corner sum mu'(x) = phi(x) + phi(face corner of x).
# Right face R = {x2 = 0} (dirs 1,3; axis cells assigned here), left face L = {x1 = 0} (dirs 2,3).
import sys
import numpy as np
from collections import Counter
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    Kr = np.arange(m); st = Counter(); M = m*(m-1)//2
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(x[a] == 0 for x in Dl) for a in range(d)): continue
        if any(x[0] > 0 and x[1] > 0 for x in Dl) is True: continue      # need x1*x2 = 0
        C = np.array(Dl); pos = (P @ C.T) % m
        ok = np.nonzero(np.all(np.sort(pos, axis=1) == Kr, axis=1))[0]
        if len(ok) == 0: continue
        tau = tops(D, d)
        for side in ('R', 'L'):
            corner = []
            for x in Dl:
                t = tau[x]
                useR = (x[1] == 0) if side == 'R' else not (x[0] == 0)
                corner.append((t[0], 0, t[2]) if useR else (0, t[1], t[2]))
            Cc = np.array(corner)
            for pi in ok:
                pv = P[pi]
                mu = (pos[pi] + Cc @ pv) % m
                st[(side, bool(np.all(np.sort(mu) == Kr)))] += 1
    print(f'm={m}:', dict(st), flush=True)
