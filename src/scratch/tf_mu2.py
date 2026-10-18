# Defect of the face-wise corner sum on two-face tiles; where are the collisions?
import sys
import numpy as np
from collections import Counter
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = 3; m = int(sys.argv[1]); shown = 0; kinds = Counter()
P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
Kr = np.arange(m)
for D in downsets(m, d):
    Dl = sorted(D)
    if any(all(x[a] == 0 for x in Dl) for a in range(d)): continue
    if any(x[0] > 0 and x[1] > 0 for x in Dl): continue
    C = np.array(Dl); pos = (P @ C.T) % m
    ok = np.nonzero(np.all(np.sort(pos, axis=1) == Kr, axis=1))[0]
    if len(ok) == 0: continue
    tau = tops(D, d)
    corner = [(tau[x][0], 0, tau[x][2]) if x[1] == 0 else (0, tau[x][1], tau[x][2]) for x in Dl]
    for pi in ok:
        pv = P[pi]
        mu = (pos[pi] + np.array(corner) @ pv) % m
        g = np.bincount(mu, minlength=m) - 1
        coll = {}
        for x, u in zip(Dl, mu): coll.setdefault(int(u), []).append(x)
        dup = [v for v in coll.values() if len(v) > 1]
        kind = tuple(sorted(('ax' if (x[0] == 0 and x[1] == 0) else ('R' if x[1] == 0 else 'L')) for v in dup for x in v))
        kinds[(tuple(sorted(g[g != 0].tolist())), kind)] += 1
        if shown < 3:
            shown += 1; print('D', Dl, 'p', tuple(int(v) for v in pv), 'dups', dup, 'missing', [u for u in range(m) if g[u] < 0])
for k, v in kinds.most_common(12): print(v, k)
