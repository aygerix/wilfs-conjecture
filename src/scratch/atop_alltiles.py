# ATOP (X = A) on EVERY non-two-face 3-D lattice tile of index m (src/scratch/tile_enum.enumerate_tiles).
import sys, time; sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch'); sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from tile_enum import enumerate_tiles
from atop_shape import atop_shape
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    t0 = time.time(); n = bad = 0; worst = None; seen = set()
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a + 1, 3)): continue
        key = tuple(sorted(D))
        if key in seen: continue
        seen.add(key); lhs, rhs, *_ = atop_shape(list(key)); n += 1; sl = (rhs - lhs) / rhs
        if sl < -1e-9:
            bad += 1
            if bad <= 3: print('  FAIL m', m, 'r', r, f'slack {sl:+.4f}', key, flush=True)
        if worst is None or sl < worst[0]: worst = (round(sl, 4), r)
    print(f'm={m}: {n} distinct non-two-face tiles, ATOP fails {bad}, worst slack {worst}, {time.time()-t0:.0f}s', flush=True)
