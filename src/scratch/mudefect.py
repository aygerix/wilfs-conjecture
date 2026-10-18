# Structure of the multiplicity defect of mu(x) = phi(x) + phi(tau x) on 3-D tiles.
import sys
import numpy as np
from collections import Counter
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    Kr = np.arange(m); shapes = Counter(); n = 0; shown = 0
    for D in downsets(m, d):
        Dl = sorted(D); C = np.array(Dl)
        if any(all(x[a] == 0 for x in Dl) for a in range(d)): continue
        pos = (P @ C.T) % m
        ok = np.nonzero(np.all(np.sort(pos, axis=1) == Kr, axis=1))[0]
        if len(ok) == 0: continue
        tau = tops(D, d); Tc = np.array([tau[x] for x in Dl])
        for pi in ok:
            pv = P[pi]
            mu = (pos[pi] + Tc @ pv) % m
            g = np.bincount(mu, minlength=m) - 1
            key = tuple(sorted(g[g != 0].tolist()))
            shapes[key] += 1; n += 1
            if key and shown < 4 and len(key) >= 2:
                shown += 1
                coll = {}
                for x, u in zip(Dl, mu): coll.setdefault(int(u), []).append((x, tau[x]))
                print('  D', Dl, 'p', tuple(int(v) for v in pv))
                print('     collisions', {u: v for u, v in coll.items() if len(v) > 1}, 'missing', [u for u in range(m) if g[u] == -1])
    print(f'm={m}: tiles {n}; defect multisets', dict(shapes.most_common(8)), flush=True)
