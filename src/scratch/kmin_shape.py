# For fixed unit-generic p and each s: min over tiles of K_D(s), and the minimizing tiles.
import sys
import numpy as np
from collections import defaultdict
from math import gcd
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = int(sys.argv[1]); m = int(sys.argv[2]); show = int(sys.argv[3]) if len(sys.argv) > 3 else 0
M = m*(m-1)//2
P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
Kr = np.arange(m)
data = defaultdict(list)   # p-index -> list of (D, Kvector)
for D in downsets(m, d):
    Dl = sorted(D); C = np.array(Dl)
    pos = (P @ C.T) % m
    ok = np.nonzero(np.all(np.sort(pos, axis=1) == Kr, axis=1))[0]
    if len(ok) == 0: continue
    tau = tops(D, d)
    Ta = [np.array([tuple(x[:a]) + (tau[x][a],) + tuple(x[a+1:]) for x in Dl]) for a in range(d)]
    for pi in ok:
        pv = P[pi]; X = np.zeros(m, dtype=np.int64)
        for a in range(d):
            tp = (Ta[a] @ pv) % m
            X += ((tp[None, :] - np.arange(m)[:, None]) % m).sum(axis=1)
        data[pi].append((Dl, ((d+1)*M - X)//m))
hist = defaultdict(int); ntight_tiles = defaultdict(int)
for pi, lst in data.items():
    pv = P[pi]
    if any(gcd(int(v), m) != 1 for v in pv): continue
    Ks = np.array([k for _, k in lst])
    mn = Ks.min(axis=0)
    for s in range(m): hist[int(mn[s])] += 1
    if show and pi == list(data)[show]:
        print('p', pv, 'num tiles', len(lst)); print('min K by s', mn.tolist())
        for s in range(m):
            arg = [lst[i][0] for i in np.nonzero(Ks[:, s] == mn[s])[0]]
            print(' s', s, 'minK', mn[s], 'minimizers', len(arg), 'e.g.', arg[0])
print(f'd={d} m={m}: distribution of min_D K_D(s) over unit p and s:', dict(sorted(hist.items())))
