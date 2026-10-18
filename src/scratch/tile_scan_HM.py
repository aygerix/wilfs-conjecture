# COMPLETE scan of non-two-face 3-D tiles: HT (H >= m-1, LP certificate on failures, as tile_scan_H.py) AND
# MAXSUM: M3 := sum_{y in Max(D)} (|y|+3) <= 2m+1  (MAXSUM => HT since H = sum_y w(y) ht(y) >= 3m - M3).
# Flag HTONLY=0/1 via argv[3] = 'M' to skip H (MAXSUM only).   usage: tile_scan_HM.py m0 m1 [M]
import sys, time
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
from heightH import H_of
from tile_lp import wilf_certified
from tile_maxsum import parts
m0, m1 = map(int, sys.argv[1:3]); MONLY = len(sys.argv) > 3 and sys.argv[3] == 'M'
for m in range(m0, m1 + 1):
    t0 = time.time(); n = nn = 0; fails = []; worst = None; uncert = []; wms = None; msbad = []
    for r, D, poly in enumerate_tiles(m):
        n += 1
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        nn += 1; S = set(D)
        M3, E, k = parts(S); ms = 2*m + 1 - M3
        if ms < 0: msbad.append((ms, r))
        if wms is None or ms < wms[0]: wms = (ms, r, k)
        if MONLY: continue
        sl = H_of(S) - (m - 1)
        if sl < 0:
            ok, (kap, p) = wilf_certified(D, poly)
            fails.append((sl, r, ok, float(kap)))
            if not ok: uncert.append((r, sorted(D)))
        if worst is None or sl < worst[0]: worst = (sl, r)
    print(f'm={m}: tiles {n}, non-two-face {nn}, HT fails {len(fails)}, LP-uncertified {len(uncert)}; min H-(m-1) {worst}; '
          f'MAXSUM fails {len(msbad)}, min slack 2m+1-M3 {wms} [{time.time()-t0:.0f}s]', flush=True)
    for f in fails: print('    HT-fail', f, flush=True)
    for u in uncert: print('    UNCERTIFIED', u, flush=True)
    for b in msbad[:20]: print('    MAXSUM-fail', b, flush=True)
