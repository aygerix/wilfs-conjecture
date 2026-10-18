# Grid-box decomposition of NON-two-face tiles.  Breakpoints in direction a: a-coordinates of all minimal non-elements
# and of all (cell + e_a) boundaries, i.e. values where membership can change.  D is a union of grid boxes; for a box
# with longest side W, Hs >= sum_Q |Q|(W_Q - 1)  (straight runs inside the top box of each column).
# Reports per m: max #boxes, max face inner corners, min of sum_Q |Q|(W_Q-1) - (m-1).   usage: m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles, min_nonelements
def boxes(D):
    G = min_nonelements(D)
    br = []
    for a in range(3):
        s = {0} | {q[a] for q in G}
        br.append(sorted(s))
    # intervals [s_i, s_{i+1})
    iv = [[(b[i], b[i+1]) for i in range(len(b) - 1)] for b in br]
    out = []
    for I in iv[0]:
        for J in iv[1]:
            for K in iv[2]:
                if (I[0], J[0], K[0]) in D:
                    out.append((I[1]-I[0], J[1]-J[0], K[1]-K[0]))
    return out, G
for m in map(int, sys.argv[1:]):
    mxB = mxI = None; worst = None
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        bx, G = boxes(set(D))
        assert sum(a*b*c for a, b, c in bx) == m, (r, bx)
        I = max(sum(1 for q in G if q[c] == 0 and sum(1 for i in range(3) if q[i] > 0) == 2) for c in range(3))
        val = sum(a*b*c*(max(a, b, c) - 1) for a, b, c in bx) - (m - 1)
        if mxB is None or len(bx) > mxB[0]: mxB = (len(bx), r)
        if mxI is None or I > mxI[0]: mxI = (I, r)
        if worst is None or val < worst[0]: worst = (val, r, len(bx))
    print(f'm={m}: max #boxes {mxB}; max face inner corners {mxI}; min box-bound - (m-1) {worst}', flush=True)
