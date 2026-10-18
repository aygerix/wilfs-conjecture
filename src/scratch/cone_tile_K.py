# cone tiles: size of Cyl ∩ K (K = q* + N^3), whether Cyl ∩ K ⊆ D + q*, LHS(D) - LHS(Cyl), t(D)-t(Cyl), Tri, Q' differences.
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_cone_peel import qstars, cyl_hull
from cone_tile_forest import analyze
from collections import Counter
def lhs(D, q):
    t, tr, qu, qo, fl, sv, tri = analyze(D, q)
    return 2*t + 2*tr + qu + qo, t, tr, qu, qo
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        ksz = Counter(); sub = 0; n = 0; dl = Counter(); mx = None
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            D = set(D); Q = qstars(D)
            if not Q: continue
            n += 1; q = Q[0]; Cy = set(cyl_hull(D)); KC = Cy - D
            ksz[len(KC)] += 1
            if all(tuple(z[i] - q[i] for i in range(3)) in D for z in KC): sub += 1
            a = lhs(D, q); b = lhs(Cy, None if False else (10**6,)*3)
            d = tuple(x - y for x, y in zip(a, b)); dl[d[0]] += 1
            if mx is None or d[0] > mx[0]: mx = (d[0], d, r, q, len(KC))
        print(f'm={m} n={n} |Cyl∩K| dist {dict(sorted(ksz.items()))}; Cyl∩K ⊆ D+q*: {sub}/{n}; LHS(D)-LHS(Cyl) dist {dict(sorted(dl.items()))}; max {mx}', flush=True)
