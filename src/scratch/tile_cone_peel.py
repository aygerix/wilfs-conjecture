# For non-two-face tiles T = Cyl \ (q* + N^3): peeling T along c for k = 0..q*_c - 1 lands in the cone-free class C.
# delta(T) = S_c + delta(T_{q*_c}),  S_c = sum_{k < q*_c} Psi_c(T_k).  Report per m: #tiles with q*, min max_c S_c,
# min over tiles of max_c [S_c + (0 if |T_{q*_c}| >= 31 else -7)] (the C-induction requirement), and examples.
# usage: tile_cone_peel.py m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
from peel_test import psis, peel
def cyl_hull(D):
    return {(i, j, k) for (i, j, _) in D if _ == 0 for k in range(0, 200)
            if (i, 0, k) in D and (0, j, k) in D}
def qstars(D):
    C = cyl_hull(D); R = C - D
    return [q for q in R if all(tuple(q[t] - (t == s) for t in range(3)) not in R for s in range(3))]
for m in (map(int, sys.argv[1:]) if __name__ == "__main__" else []):
    nq = 0; worst = None; worst2 = None; multi = 0; neg_layer = 0
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        D = set(D); Q = qstars(D)
        if not Q: continue
        nq += 1
        if len(Q) > 1: multi += 1; continue
        q = Q[0]; best = None; best2 = None
        for c in range(3):
            T = D; S = 0; allnn = True
            for k in range(q[c]):
                p = psis(T)[c]; S += p; allnn &= p >= 0; T = peel(T, c)
            req = S + (0 if len(T) >= 31 else -7)
            if best is None or S > best[0]: best = (S, c, len(T))
            if best2 is None or req > best2[0]: best2 = (req, c, len(T))
        if worst is None or best[0] < worst[0]: worst = best + (r, q)
        if worst2 is None or best2[0] < worst2[0]: worst2 = best2 + (r, q)
    print(f'm={m}: tiles with q* {nq} (multi {multi}); min_T max_c S_c {worst}; min_T max_c req {worst2}', flush=True)
