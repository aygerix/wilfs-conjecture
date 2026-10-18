# Real tiles: tripod elimination excess (decreasing |x|), qO elimination excess (increasing |x|), qU cycles.
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch'); sys.path.insert(0, 'src/scratch/forest')
from tile_cone_peel import qstars
from cone_defects import structure, elim
from collections import Counter
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        st = Counter(); ex = {}
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            D = set(D); Q = qstars(D); kind = 'cone' if Q else 'C'
            ht, Max, floor, tri, qO, qU = structure(D, Q[0] if Q else (999, 999, 999))
            eT, badT, nT = elim([(x, tp) for x, tp in tri], lambda e: -sum(e[0]), 3)
            eO, badO, nO = elim([(x, [tp[a] for a in range(3) if a != c]) for x, tp, c in qO], lambda e: sum(e[0]), 2)
            par = {}
            def f(u):
                while par.setdefault(u, u) != u: par[u] = par[par[u]]; u = par[u]
                return u
            cyc = 0
            for x, tp, c in qU:
                u, v = [tuple(x[i] + (i == a) for i in range(3)) for a in range(3) if a != c]
                if f(u) == f(v): cyc += 1
                else: par[f(u)] = f(v)
            st[(kind, 'n')] += 1
            for nm, v in (('eT', eT), ('eO', eO), ('qUcyc', cyc)):
                if v: st[(kind, nm)] += 1; ex.setdefault((kind, nm), (r, Q, v))
        print(f'm={m}', dict(st), ex, flush=True)
