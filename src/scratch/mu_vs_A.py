# mu-bijectivity vs number of maximal cells |A| (= type), all 3-D tiles.
import sys
import numpy as np
from collections import defaultdict
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    Kr = np.arange(m); st = defaultdict(lambda: [0, 0])
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(x[a] == 0 for x in Dl) for a in range(d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        ok = np.nonzero(np.all(np.sort(pos, axis=1) == Kr, axis=1))[0]
        if len(ok) == 0: continue
        nA = sum(1 for y in Dl if all(tuple(y[:a]) + (y[a]+1,) + tuple(y[a+1:]) not in D for a in range(d)))
        tau = tops(D, d); Tc = np.array([tau[x] for x in Dl])
        mu = (pos[ok] + (P[ok] @ Tc.T)) % m
        bij = np.all(np.sort(mu, axis=1) == Kr, axis=1)
        st[nA][0] += int(bij.sum()); st[nA][1] += len(bij)
    print(f'm={m}:', {k: f'{v[0]}/{v[1]}' for k, v in sorted(st.items())}, flush=True)
