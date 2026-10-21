"""Which simplices Delta_h (d generators) tile Z/m with m = C(d+h, h)?  I.e. residues s_1..s_d with
{z.s mod m : |z| <= h} = Z/m.  Brute force over s up to symmetry (lead, 2026-10-20)."""
import sys, itertools
from math import comb
def cells(d, h): return [z for z in itertools.product(range(h + 1), repeat=d) if sum(z) <= h]
for d in range(2, 5):
    for h in range(2, 5):
        m = comb(d + h, h)
        if m > 60: continue
        C = cells(d, h); sols = []
        for s in itertools.combinations(range(1, m), d):
            if len({sum(a * b for a, b in zip(z, s)) % m for z in C}) == m: sols.append(s)
        print("d=%d h=%d m=%d tilings(sorted s)=%d %s" % (d, h, m, len(sols), sols[:4]), flush=True)
