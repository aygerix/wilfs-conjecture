# max number of maximal cells |A| (and generators mu) over all NON-two-face tiles of size m; Cross-Lemma consequence:
# H >= 2m - P2(A) - 2|A| + H2 >= m - 1 whenever P2(A) + 2|A| <= m + 1.   usage: tile_maxA.py m...
import sys, itertools
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles, min_nonelements
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
for m in map(int, sys.argv[1:]):
    mxA = None; worstSC = None; n = 0
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        n += 1
        A = [x for x in D if all(add(x, i) not in D for i in range(3))]
        P2 = sum(1 for y, z in itertools.combinations(A, 2) if sum(y[i] != z[i] for i in range(3)) == 2)
        if mxA is None or len(A) > mxA[0]: mxA = (len(A), r, len(min_nonelements(set(D))))
        v = P2 + 2*len(A) - m - 1
        if worstSC is None or v > worstSC[0]: worstSC = (v, r, len(A), P2)
    print(f'm={m}: non-two-face {n}; max |A| {mxA}; max (P2(A)+2|A|-m-1) {worstSC}', flush=True)
