# over all NON-two-face tiles of size m: max |A|, max |Z3'| (non-maximal cells whose three column tops are maximal),
# min surplus Sigma (phi-1)^+, and relation to sum L.   usage: m0 m1
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
m0, m1 = map(int, sys.argv[1:3])
for m in range(m0, m1 + 1):
    mxA = mxZ = None; mnS = None; mxratio = None
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        ht = {}
        for x in sorted(D, key=lambda x: -sum(x)):
            ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
        def top(x, i):
            while add(x, i) in D: x = add(x, i)
            return x
        phi = {x: sum(ht[top(x, i)] for i in range(3)) for x in D}
        A = [x for x in D if ht[x] == 0]; Z = [x for x in D if phi[x] == 0 and ht[x] > 0]
        S = sum(max(0, v - 1) for v in phi.values()); sL = sum(max(x[i] for x in D) + 1 for i in range(3))
        if mxA is None or len(A) > mxA[0]: mxA = (len(A), r, sL)
        if mxZ is None or len(Z) > mxZ[0]: mxZ = (len(Z), r)
        if mnS is None or S < mnS[0]: mnS = (S, r, len(A), len(Z))
        rt = (len(A) + len(Z)) / sL
        if mxratio is None or rt > mxratio[0]: mxratio = (round(rt, 2), r, len(A), len(Z), sL)
    print(f'm={m}: max|A| {mxA}; max|Z3\'| {mxZ}; min surplus {mnS}; max (|A|+|Z3\'|)/sumL {mxratio}', flush=True)
