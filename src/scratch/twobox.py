# 3-D tiles with exactly 2 maximal cells (union of two boxes): bijectivity of corner maps, tightness, K structure.
import sys
import numpy as np
from collections import Counter
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    Kr = np.arange(m); M = m*(m-1)//2; st = Counter(); shapes = set()
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(x[a] == 0 for x in Dl) for a in range(d)): continue
        A = [y for y in Dl if all(tuple(y[:a]) + (y[a]+1,) + tuple(y[a+1:]) not in D for a in range(d))]
        if len(A) != 2: continue
        C = np.array(Dl); pos = (P @ C.T) % m
        ok = np.nonzero(np.all(np.sort(pos, axis=1) == Kr, axis=1))[0]
        if len(ok) == 0: continue
        shapes.add(tuple(A))
        tau = tops(D, d); Tc = np.array([tau[x] for x in Dl])
        Ta = [np.array([tuple(x[:a]) + (tau[x][a],) + tuple(x[a+1:]) for x in Dl]) for a in range(d)]
        for pi in ok:
            pv = P[pi]
            mu = (pos[pi] + Tc @ pv) % m
            st['tiles'] += 1
            st['mu bij'] += bool(np.all(np.sort(mu) == Kr))
            X = np.zeros(m, dtype=np.int64)
            for a in range(d):
                tp = (Ta[a] @ pv) % m
                X += ((tp[None, :] - np.arange(m)[:, None]) % m).sum(axis=1)
            K = (4*M - X)//m
            st['tight'] += int(K.min() == 0)
            # pair slacks
            for c in range(d):
                a, b = [i for i in range(d) if i != c]
                Xab = np.zeros(m, dtype=np.int64)
                for e in (a, b):
                    tp = (Ta[e] @ pv) % m
                    Xab += ((tp[None, :] - np.arange(m)[:, None]) % m).sum(axis=1)
                if (3*M - Xab).min() < 0: st['some pair slack <0'] += 1; break
    print(f'm={m}: 2-box shapes {len(shapes)}', dict(st), flush=True)
