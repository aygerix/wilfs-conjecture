# max T(A) - 2m by type |A| over ALL non-degenerate 3-D tile shapes (two-face included); also min CR slack by type.
import sys, time
import numpy as np
from collections import defaultdict
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
d = 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    t0 = time.time()
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    Kr = np.arange(m); best = defaultdict(lambda: [-10**9, 10**9, 0, None])
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(x[a] == 0 for x in Dl) for a in range(d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        if not np.all(np.sort(pos, axis=1) == Kr, axis=1).any(): continue
        A = [y for y in Dl if all(tuple(y[:a]) + (y[a]+1,) + tuple(y[a+1:]) not in D for a in range(d))]
        T = sorted([3 + sum(y) for y in A], reverse=True); TA = sum(T)
        cr = sum(i*t for i, t in enumerate(T)) - (m-1)*(TA - 2*m)
        b = best[len(A)]
        b[2] += 1
        if TA - 2*m > b[0]: b[0] = TA - 2*m; b[3] = A
        b[1] = min(b[1], cr)
    print(f'm={m} [{time.time()-t0:.0f}s]:', {t: (v[2], v[0], v[1]) for t, v in sorted(best.items())}, flush=True)
