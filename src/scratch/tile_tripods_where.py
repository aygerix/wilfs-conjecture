# For tiles (non-two-face) at given m: list tiles with max #tripods, their q*, tripod cells, and tops.
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_cone_peel import qstars
from cone_tile_forest import analyze
from cht_corners import corners
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    m = int(sys.argv[1]); thr = int(sys.argv[2]); shown = 0
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        D = set(D); Q = qstars(D)
        t, tr, qu, qo, fl, sv, tri = analyze(D, Q[0] if Q else (999, 999, 999))
        if tr >= thr:
            L = [max(x[a] for x in D) + 1 for a in range(3)]
            print('r', r, 'q*', Q, 'ext', L, 't', t, 'Tri', tr, 'C', corners(D), 'tripods', sorted(x for x, tp in tri), 'tops', [tp for x, tp in sorted(tri)][:4])
            shown += 1
            if shown >= 12: break
