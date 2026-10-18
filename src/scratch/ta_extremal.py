# Extremal shapes for T(A) - m by type; print maximal cells and outer corners.
import sys
import numpy as np
from collections import defaultdict
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
d = 3; m = int(sys.argv[1]); per = int(sys.argv[2])
P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
Kr = np.arange(m); ex = defaultdict(list); best = defaultdict(lambda: -10**9)
for D in downsets(m, d):
    Dl = sorted(D)
    if any(all(x[a] == 0 for x in Dl) for a in range(d)): continue
    C = np.array(Dl); pos = (P @ C.T) % m
    ok = np.nonzero(np.all(np.sort(pos, axis=1) == Kr, axis=1))[0]
    if len(ok) == 0: continue
    A = [y for y in Dl if all(tuple(y[:a]) + (y[a]+1,) + tuple(y[a+1:]) not in D for a in range(d))]
    v = sum(3 + sum(y) for y in A) - m; t = len(A)
    two = any(tuple(int(a == i or b == i) for i in range(d)) not in D for a in range(d) for b in range(a+1, d))
    if v > best[t]: best[t] = v; ex[t] = []
    if v == best[t] and len(ex[t]) < per: ex[t].append((A, 'two-face' if two else 'non-two-face', tuple(int(u) for u in P[ok[0]])))
for t in sorted(best):
    print(f'type {t}: max T(A)-m = {best[t]}')
    for e in ex[t]: print('    ', e)
