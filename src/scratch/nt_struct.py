# Structure of non-two-face 3-D tile shapes with large T(A): maximal cells, CR slack, nu-distribution.
import sys
import numpy as np
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
d = 3
def info(Dl, m):
    D = set(Dl)
    A = [y for y in Dl if all(tuple(y[:a]) + (y[a]+1,) + tuple(y[a+1:]) not in D for a in range(d))]
    T = sorted([3 + sum(y) for y in A], reverse=True)
    TA = sum(T); cr = sum(i*t for i, t in enumerate(T)) - (m-1)*(TA - 2*m)
    return A, TA, cr
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    Kr = np.arange(m); rows = []
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(x[a] == 0 for x in Dl) for a in range(d)): continue
        if any(tuple(int(a == i or b == i) for i in range(d)) not in D for a in range(d) for b in range(a+1, d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        if not np.all(np.sort(pos, axis=1) == Kr, axis=1).any(): continue
        A, TA, cr = info(Dl, m)
        rows.append((TA - 2*m, cr, len(A), Dl, A))
    rows.sort(key=lambda r: -r[0])
    print(f'm={m}: non-two-face shapes {len(rows)}; max T(A)-2m {rows[0][0]}; min CR slack {min(r[1] for r in rows)}; max |A| {max(r[2] for r in rows)}')
    for r in rows[:2]:
        print('   T(A)-2m', r[0], 'CRslack', r[1], '|A|', r[2], 'A', r[4])
