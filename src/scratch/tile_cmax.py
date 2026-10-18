# max corner count C and C^2/m over non-two-face tiles, split C / cone, per m
import sys, math
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from cht_corners import corners
from tile_cone_peel import qstars
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        best = {'C': (0, None), 'cone': (0, None)}
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            D = set(D); k = 'cone' if qstars(D) else 'C'; c = corners(D)
            if c > best[k][0]: best[k] = (c, r)
        print(f"m={m} maxC: C-tiles {best['C'][0]} (C^2/m {best['C'][0]**2/m:.2f}, r={best['C'][1]}), cone {best['cone'][0]} (C^2/m {best['cone'][0]**2/m:.2f}, r={best['cone'][1]}); Lemma B bound {math.floor(1.5+math.sqrt(6*m-3.75))}", flush=True)
