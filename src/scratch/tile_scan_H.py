# COMPLETE scan (all tiles of all lattices, src/tile_enum.py) of the height criterion H(D) >= m - 1 for NON-two-face
# 3-D tiles; every HT-failing tile is passed to the exact LP certificate (src/tile_lp.py).
# Also records min H/m and the straight-run quantity Pi (H >= Pi/2).   usage: tile_scan_H.py m0 m1
import sys, time
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
from heightH import H_of
from tile_lp import wilf_certified
m0, m1 = map(int, sys.argv[1:3])
for m in range(m0, m1 + 1):
    t0 = time.time(); n = nn = 0; fails = []; worst = None; uncert = []
    for r, D, poly in enumerate_tiles(m):
        n += 1
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        nn += 1
        sl = H_of(set(D)) - (m - 1)
        if sl < 0:
            ok, (kap, p) = wilf_certified(D, poly)
            fails.append((sl, r, ok, float(kap)))
            if not ok: uncert.append((r, sorted(D)))
        if worst is None or sl < worst[0]: worst = (sl, r)
    print(f'm={m}: tiles {n}, non-two-face {nn}, HT fails {len(fails)}, LP-uncertified {len(uncert)}; min H-(m-1) {worst} [{time.time()-t0:.0f}s]', flush=True)
    for f in fails: print('    HT-fail', f, flush=True)
    for u in uncert: print('    UNCERTIFIED', u, flush=True)
