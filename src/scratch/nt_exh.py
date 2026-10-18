# CONJ NT: non-two-face 3-D tile shapes have T(A) = sum_{y maximal}(3 + |y|) <= 2m.  T(A) depends only on the shape D.
import sys, time
import numpy as np
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
d = 3
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    t0 = time.time()
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    Kr = np.arange(m); res = {'nt': [0, -10**9, None], 'tf': [0, -10**9, None]}; viol = []
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(x[a] == 0 for x in Dl) for a in range(d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        ok = np.all(np.sort(pos, axis=1) == Kr, axis=1)
        if not ok.any(): continue
        A = [y for y in Dl if all(tuple(y[:a]) + (y[a]+1,) + tuple(y[a+1:]) not in D for a in range(d))]
        TA = sum(3 + sum(y) for y in A)
        two = any(tuple(int(a == i or b == i) for i in range(d)) not in D for a in range(d) for b in range(a+1, d))
        key = 'tf' if two else 'nt'
        res[key][0] += 1
        if TA - 2*m > res[key][1]: res[key][1] = TA - 2*m; res[key][2] = (Dl, tuple(int(v) for v in P[np.nonzero(ok)[0][0]]))
        if not two and TA > 2*m: viol.append(Dl)
    print(f'm={m}: non-two-face shapes {res["nt"][0]} max T(A)-2m {res["nt"][1]} (#>0: {len(viol)}); two-face shapes {res["tf"][0]} max T(A)-2m {res["tf"][1]}  [{time.time()-t0:.0f}s]', flush=True)
    if viol: print('    NT-violating example', res['nt'][2])
