"""max Omega/m over ALL 3-D lattice tiles (complete Groebner-fan enumeration, src/tile_enum.py), Omega = sum_A (d+|y|).
Omega-crude (Omega <= (d+1)m/2 = 2m for d = 3) implies MaxCL at every phase.  usage: python omega3.py mlo mhi"""
import sys
sys.path.insert(0, '.')
from tile_enum import enumerate_tiles
mlo, mhi = int(sys.argv[1]), int(sys.argv[2])
for m in range(mlo, mhi+1):
    best = 0; nt = 0; over = 0; arg = None
    for r, D, poly in enumerate_tiles(m):
        Ds = set(D); d = 3; nt += 1
        A = [y for y in D if all(tuple(y[i]+(i == a) for i in range(d)) not in Ds for a in range(d))]
        Om = sum(d+sum(y) for y in A)
        if Om > 2*m: over += 1
        if Om > best: best = Om; arg = (r, len(A), max(map(sum, D)))
    print("m=%d tiles=%d max_Omega/m=%.3f (r, |A|, height)=%s crude_fail=%d" % (m, nt, best/m, arg, over), flush=True)
