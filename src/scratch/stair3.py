# 3-D staircase inequality candidates on all 3-D tile SHAPES (some p makes D a tile), m in [m0, m1]:
#   S1:  sum_{y in A} (|y| + 2) <= 2m          (<=> T(A) <= 2m + |A|)
#   NT:  T(A) <= 2m  (non-two-face only)
import sys
import numpy as np
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
d = 3
def up(x, a): return x[:a] + (x[a] + 1,) + x[a+1:]
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T; K = np.arange(m)
    n = f1 = fnt = nnt = 0; w1 = wnt = -10**9; ex1 = exnt = None
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(x[a] == 0 for x in Dl) for a in range(d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        if not np.all(np.sort(pos, axis=1) == K, axis=1).any(): continue
        S = set(Dl); n += 1
        A = [y for y in Dl if all(up(y, a) not in S for a in range(d))]
        s1 = sum(sum(y) + 2 for y in A) - 2*m
        if s1 > 0: f1 += 1
        if s1 > w1: w1, ex1 = s1, Dl
        two = any(tuple(int(i in (a, b)) for i in range(3)) not in S for a in range(3) for b in range(a+1, 3))
        if not two:
            nnt += 1; nt = sum(sum(y) + 3 for y in A) - 2*m
            if nt > 0: fnt += 1
            if nt > wnt: wnt, exnt = nt, Dl
    print(f'm={m}: tile shapes {n}; S1 fails {f1} (max excess {w1}); non-two-face {nnt}, NT fails {fnt} (max excess {wnt})', flush=True)
    if f1 and m <= 9: print('    S1 worst', ex1)
