# Face staircase statistics over complete enumeration (non-two-face): per face, inner corners (non-axis minimal
# non-elements with that coordinate 0) sorted; count consecutive pairs with (d_alpha, d_beta) = (1,1) ("unit steps"),
# and steps with min(d_alpha, d_beta) = 1.  Report max over tiles.   usage: m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles, min_nonelements
for m in map(int, sys.argv[1:]):
    mx = {'corners': (0,), 'unit11': (0,), 'thin': (0,)}
    hist = {}
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        G = min_nonelements(set(D))
        for c in range(3):
            a, b = [i for i in range(3) if i != c]
            Q = sorted((q[a], q[b]) for q in G if q[c] == 0 and q[a] > 0 and q[b] > 0)
            u11 = sum(1 for i in range(len(Q) - 1) if Q[i+1][0] - Q[i][0] == 1 and Q[i][1] - Q[i+1][1] == 1)
            thin = sum(1 for i in range(len(Q) - 1) if min(Q[i+1][0] - Q[i][0], Q[i][1] - Q[i+1][1]) == 1)
            hist[u11] = hist.get(u11, 0) + 1
            for k, v in (('corners', len(Q)), ('unit11', u11), ('thin', thin)):
                if v > mx[k][0]: mx[k] = (v, r, c, Q)
    print(f'm={m}:', {k: v[:3] for k, v in mx.items()}, 'hist unit11 per face', sorted(hist.items()), flush=True)
