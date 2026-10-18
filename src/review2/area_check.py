# Exact completeness certificate for the Groebner-fan traversal (project's src/tile_enum.py, copied read-only):
# for each canonical lattice, the open cones of distinct tiles are pairwise disjoint (a weight in two open cones would
# have two different standard sets), so the traversal found EVERY tile of the lattice iff the areas of the cone
# polygons (recomputed here from scratch with my own constraint/clipping code) sum to the area of the simplex.
# Also re-checks HT for non-two-face tiles (my own H) and counts, to compare with the logs.
import sys, time
from fractions import Fraction as Fr
D0 = __import__('os').path.dirname(__import__('os').path.abspath(__file__))  
sys.path.insert(0, D0 + '/../'); sys.path.insert(0, D0)  # the referee used a copy of src/tile_enum.py in proj_copy/
sys.dont_write_bytecode = True
from tile_enum import enumerate_lattice, canonical_residues
from shapes import open_cone, area2
from tk import H_of, two_face_pairs, is_downset

m0, m1 = int(sys.argv[1]), int(sys.argv[2])
step = int(sys.argv[3]) if len(sys.argv) > 3 else 1      # take every step-th lattice (sampling for large m)
for m in range(m0, m1 + 1):
    t0 = time.time(); nt = nn = 0; bad = []; htf = 0; nl = 0
    for li, r in enumerate(canonical_residues(m)):
        if li % step: continue
        nl += 1
        tiles = enumerate_lattice(m, r)
        tot = Fr(0)
        for D in tiles:
            S = set(D)
            assert len(S) == m and is_downset(S)
            assert len({sum(a*b for a, b in zip(r, x)) % m for x in S}) == m
            poly, cons = open_cone(S, m, r)
            if poly is None: bad.append(('empty cone', r)); continue
            tot += area2(poly)
            nt += 1
            if not two_face_pairs(S):
                nn += 1
                if H_of(S) - (m - 1) < 0: htf += 1
        if tot != 1: bad.append(('area', r, float(tot), len(tiles)))
    print(f'm={m}: lattices {nl} (step {step}), tiles {nt}, non-two-face {nn}, HT fails {htf}, '
          f'area defects {len(bad)} {bad[:3]} [{time.time()-t0:.0f}s]', flush=True)
