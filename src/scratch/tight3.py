# Genuinely 3-D, non-box tiles where Tile-CL is tight (K(s)=0); print the cell data.
import sys
import numpy as np
from math import gcd
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from corner_bij import tops
d = 3; m = int(sys.argv[1]); lim = int(sys.argv[2])
M = m*(m-1)//2
P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
Kr = np.arange(m); shown = 0; cnt = 0; tot = 0
for D in sorted(downsets(m, d), key=lambda D: sorted(D)):
    Dl = sorted(D); C = np.array(Dl)
    if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
    if int(np.prod(C.max(axis=0) + 1)) == m: continue
    if all(sum(1 for v in x if v) <= 1 for x in Dl): continue   # skip pure tripods
    pos = (P @ C.T) % m
    ok = np.nonzero(np.all(np.sort(pos, axis=1) == Kr, axis=1))[0]
    if len(ok) == 0: continue
    tau = tops(D, d)
    for pi in ok:
        pv = P[pi]
        if any(gcd(int(v), m) != 1 for v in pv): continue
        phi = {x: int(np.dot(x, pv) % m) for x in Dl}
        for s in range(m):
            r = lambda y: (int(np.dot(y, pv)) - s) % m
            X = sum(r(tuple(x[:a]) + (tau[x][a],) + tuple(x[a+1:])) for x in Dl for a in range(d))
            tot += 1
            if X == 4*M:
                cnt += 1
                if shown < lim:
                    shown += 1
                    print('D', Dl, 'p', tuple(int(v) for v in pv), 's', s)
                    for x in Dl:
                        ts = [tuple(x[:a]) + (tau[x][a],) + tuple(x[a+1:]) for a in range(d)]
                        print('   x', x, 'r', r(x), 'tops r', [r(t) for t in ts], 'sum', sum(r(t) for t in ts), 'tau', tau[x], 'r(tau)', r(tau[x]))
print('tight', cnt, 'of', tot, '(tile,s) pairs')
