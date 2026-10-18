# Is every tile coherent (D = set of w-minimal representatives of Lambda-classes in N^d for some w > 0)?
# Necessary+sufficient test: LP  w >= 1,  w.(z - f(z)) >= 1 for every z in N^d \ D with z <= bound (f(z) = rep in D).
import sys, itertools
import numpy as np
from scipy.optimize import linprog
from math import gcd
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
d = int(sys.argv[1])
for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    Kr = np.arange(m); ntile = 0; ncoh = 0; ex = []
    for D in downsets(m, d):
        Dl = sorted(D); C = np.array(Dl)
        pos = (P @ C.T) % m
        ok = np.nonzero(np.all(np.sort(pos, axis=1) == Kr, axis=1))[0]
        if len(ok) == 0: continue
        mx = C.max(axis=0)
        # minimal non-elements (generators of the monomial ideal) suffice for the necessary condition; use all z in box for sufficiency
        box = [z for z in itertools.product(*[range(int(v) + 3) for v in mx]) if z not in D]
        for pi in ok:
            pv = P[pi]; ntile += 1
            rep = {int(np.dot(x, pv) % m): x for x in Dl}
            rows = [-(np.array(z) - np.array(rep[int(np.dot(z, pv) % m)])) for z in box]
            res = linprog(np.zeros(d), A_ub=np.array(rows), b_ub=-np.ones(len(rows)), bounds=[(1, None)]*d, method='highs')
            if res.status == 0: ncoh += 1
            elif len(ex) < 3: ex.append((Dl, tuple(int(v) for v in pv)))
    print(f'd={d} m={m}: tiles {ntile}, coherent {ncoh}, non-coherent {ntile - ncoh}', flush=True)
    for e in ex: print('   non-coherent example', e)
