r"""Exhaustive census of case B (Dep < Sigma_supp) over all lattice tiles (lead, 2026-10-21): d = 3 (all down-sets of
size m, all delta) and d = 4 (chains).  Case B depends on the shape only; for each case-B shape that is a tile, report
its height and Tile-CL min V over all delta and phases.  Usage: python casebx.py d MMIN MMAX"""
import sys, itertools
sys.path.insert(0, '.')
from subadd_lp import downsets
from kdep import ds4
from tcldich import stats
N, MMIN, MMAX = map(int, sys.argv[1:4])
for m in range(MMIN, MMAX + 1):
    gen = ds4(m) if N == 4 else downsets(N, m)
    shapes = tiles = caseb = 0; byh = {}; worst = None
    for D in gen:
        if any(all(x[b] == 0 for x in D) for b in range(N)): continue
        Ds = set(D); up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
        om = {x: 0 for x in D}
        for b in range(N):
            for x in D:
                if up(x, b) not in Ds: om[x] += x[b] + 1
        mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
        dep = sum(v for x, v in om.items() if x not in mx)
        ss = sum(max(0, sum(1 for t in x if t) - 1) for x in D)
        shapes += 1
        if dep >= ss: continue
        isT = False; vmin = None
        for b in itertools.product(range(1, m), repeat=N):
            if len({sum(x * y for x, y in zip(a, b)) % m for a in D}) != m: continue
            isT = True; v = stats(m, D, list(b))[0]
            vmin = v if vmin is None else min(vmin, v)
        if not isT: continue
        caseb += 1; h = max(sum(x) for x in D); byh[h] = byh.get(h, 0) + 1
        if worst is None or vmin < worst[0]: worst = (vmin, h, dep, ss, sorted(D))
    print("d=%d m=%d shapes %d  case-B tiles %d  by height %s  min Tile-CL over them %s" % (N, m, shapes, caseb, byh, worst), flush=True)
