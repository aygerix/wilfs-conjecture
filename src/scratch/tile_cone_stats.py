# Cone-layer statistics for non-two-face tiles with q*: per direction c, S_c = sum_{k<q*_c} Psi_c(T_k) (T_k = k-fold peel);
# reports min over tiles of max_c S_c, sum_c S_c, S at argmin q*, min single-layer Psi, max first-layer Psi.  usage: m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
from peel_test import psis, peel
from tile_cone_peel import qstars
for m in map(int, sys.argv[1:]):
    stats = {}
    def upd(k, v, ex):
        if k not in stats or v < stats[k][0]: stats[k] = (v, ex)
    qdist = {}
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        D = set(D); Q = qstars(D)
        if not Q: continue
        q = Q[0]; qdist[tuple(sorted(q))] = qdist.get(tuple(sorted(q)), 0) + 1
        S = []; first = []; layers = []
        for c in range(3):
            T = D; s = 0; lay = []
            for k in range(q[c]):
                p = psis(T)[c]; s += p; lay.append(p); T = peel(T, c)
            S.append(s); first.append(lay[0]); layers.append(lay)
        cmin = min(range(3), key=lambda c: (q[c], -S[c]))
        upd('max S', max(S), (r, q, S)); upd('sum S', sum(S), (r, q, S)); upd('S at argmin q', S[cmin], (r, q, S))
        upd('min layer psi (all c)', min(min(l) for l in layers), (r, q, layers))
        upd('max first-layer psi', max(first), (r, q, first))
    print('m', m, 'q* dist', dict(sorted(qdist.items())))
    for k, v in stats.items(): print('   ', k, v)
