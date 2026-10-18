# Extremality test: for fixed p (fixed lattice + positions), is min over ALL tiles D of K_D(s) attained by a box tile?
# K_D(s) = ((d+1)M' - X_D(s))/m,  X_D(s) = sum_x sum_a r_s(t_a x).  Tile-CL for boxes is PROVED, so "box-min" => Tile-CL.
import sys
import numpy as np
from collections import defaultdict
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = int(sys.argv[1])
for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
    M = m*(m-1)//2
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    Kr = np.arange(m)
    best = {}            # p-index -> (min over tiles of K(s) vector, min over boxes)
    allmin = defaultdict(lambda: np.full(m, 10**9)); boxmin = defaultdict(lambda: np.full(m, 10**9))
    lexK = {}
    for D in downsets(m, d):
        Dl = sorted(D); C = np.array(Dl)
        pos = (P @ C.T) % m
        ok = np.nonzero(np.all(np.sort(pos, axis=1) == Kr, axis=1))[0]
        if len(ok) == 0: continue
        tau = tops(D, d)
        Ta = [np.array([tuple(x[:a]) + (tau[x][a],) + tuple(x[a+1:]) for x in Dl]) for a in range(d)]
        mx = C.max(axis=0) + 1
        isbox = int(np.prod(mx)) == m
        for pi in ok:
            pv = P[pi]
            X = np.zeros(m, dtype=np.int64)
            for a in range(d):
                tp = (Ta[a] @ pv) % m
                X += ((tp[None, :] - np.arange(m)[:, None]) % m).sum(axis=1)
            Kv = ((d+1)*M - X) // m
            allmin[pi] = np.minimum(allmin[pi], Kv)
            if isbox: boxmin[pi] = np.minimum(boxmin[pi], Kv)
    nps = len(allmin); nobox = 0; viol = 0; worst = 0; ex = None
    for pi in allmin:
        if pi not in boxmin: nobox += 1; continue
        diff = boxmin[pi] - allmin[pi]
        if diff.max() > 0:
            viol += 1
            if diff.max() > worst: worst = int(diff.max()); ex = (tuple(P[pi]), int(diff.argmax()), int(allmin[pi][diff.argmax()]), int(boxmin[pi][diff.argmax()]))
    print(f'd={d} m={m}: p-vectors {nps}, without box tile {nobox}, box-min violated for {viol} (worst gap {worst}, ex p,s,minK,boxK={ex}); global min K {min(v.min() for v in allmin.values())}', flush=True)
