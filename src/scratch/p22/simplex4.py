# Perfect depth-four B_3 simplices (lead, 2026-10-20): B = {b_1 < ... < b_k} subset [1, m-1], m = C(k+3,3), such that
# {0} u B u 2B u 3B (multisets of size <= 3, as integers) are distinct mod m (so Ap = this simplex, levels 0..3),
# pairs at co-level 1 and cubics at co-level 0: with h = 3 b_k - m + 1, need 2 b_1 >= h, b_k < h (A-class), h >= 1.
# Model identity: W = rho - C(k+1,3). Search all B for k = 2, 3 (m = 10, 20) and k = 4 (m = 35).
import itertools, sys
from math import comb
for k in (2, 3, 4):
    m = comb(k + 3, 3); found = 0
    for B in itertools.combinations(range(1, m), k):
        h = 3 * B[-1] - m + 1
        if h < 1 or 2 * B[0] < h or B[-1] >= h: continue
        vals = [0] + [s for j in (1, 2, 3) for s in map(sum, itertools.combinations_with_replacement(B, j))]
        if len({v % m for v in vals}) != m: continue
        rho = m - h; found += 1
        if found <= 5: print("k=%d m=%d B=%s h=%d rho=%d C(k+1,3)=%d C(k+2,3)=%d" % (k, m, B, h, rho, comb(k + 1, 3), comb(k + 2, 3)))
    print("k=%d m=%d perfect depth-4 simplices: %d" % (k, m, found))
