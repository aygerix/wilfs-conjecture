# Ratio test: K' := (2t + 2Tri + Q') / C, C = c(A1) + c(A2) + c(A3) (outer corners of the three coordinate faces).
# Lemma (proved for q*-free cylindrical sets): t <= C + 2.  If 2t + 2Tri + Q' <= K' C and C <= sqrt(12 m), CHT holds for
# m >= 12 K'^2.  Reports per m: max K', max t - C, and C/sqrt(m).  usage: cht_corners.py m...  (tiles)
import sys, math
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_cht import cht
from tile_cone_peel import qstars
def corners(D):
    tot = 0
    for c in range(3):
        a, b = [i for i in range(3) if i != c]
        F = {(x[a], x[b]) for x in D if x[c] == 0}
        tot += sum(1 for (i, j) in F if (i+1, j) not in F and (i, j+1) not in F)
    return tot
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        wk = [0, None]; wt = [-99, None]; wc = 0; wkq = [0, None]
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            S = set(D); t, tri, q0, q1 = cht(S); C = corners(S); hq = bool(qstars(S))
            K = (2*t + 2*tri + q0 + q1) / C
            if not hq and K > wk[0]: wk = [K, (r, t, tri, q0, q1, C)]
            if hq and K > wkq[0]: wkq = [K, (r, t, tri, q0, q1, C)]
            if t - C > wt[0]: wt = [t - C, (r, hq)]
            wc = max(wc, C / math.sqrt(m))
        print(f'm={m}: max K\' q*-free {wk[0]:.2f} {wk[1]}; with q* {wkq[0]:.2f} {wkq[1]}; max t-C {wt}; max C/sqrt(m) {wc:.2f}', flush=True)
