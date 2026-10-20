"""Bacher (arXiv:2604.25051, Thm 3.3 (5)): for collision-free h-regular S with Farey interval (a'/b', a/b] and ell left
generators, E = E0(h, a/b, ell) + ell*omega + rho, with E0 = -ell * sum_{i<h} phi'_{h-i} s_i + phi'_h s,
s_i = C(ell-2+i, i), s = C(ell+h-1, h), phi'_i = {i a'/b'}; r = m - s. CORE1 (E + r >= 0) at omega = rho = 0 needs
m >= s + |E0|, i.e. packing density s/m <= s/(s + |E0|) =: dens*. A collision-free h-regular S with density above
dens* would refute CORE1. Checks the formula on <14,22,23>_56 (E = -1). Usage: python bacher_e0.py HMAX LMAX"""
import sys
from fractions import Fraction as Fr
from math import comb
HMAX, LMAX = int(sys.argv[1]), int(sys.argv[2])
def farey_pairs(h):
    fr = sorted({Fr(a, b) for b in range(1, h + 1) for a in range(b, 2 * b + 1)})   # fractions in [1, 2]
    return [(fr[i], fr[i + 1]) for i in range(len(fr) - 1)]
def E0(h, lo, hi, ell):
    s = comb(ell + h - 1, h)
    ph = lambda i: (i * lo) - ((i * lo).numerator // (i * lo).denominator)     # {i a'/b'}
    val = -ell * sum(ph(h - i) * comb(ell - 2 + i, i) for i in range(h)) + ph(h) * s
    return val, s
print("check <14,22,23>_56:", E0(3, Fr(3, 2), Fr(5, 3), 3))
for h in range(3, HMAX + 1):
    rows = []
    for lo, hi in farey_pairs(h):
        if lo.denominator == 1 or hi.denominator == 1: continue   # Thm 5.1 (b' != 1); Thm 5.3 (b = 1 forces E >= 0 at omega = 0 or rho = 0)
        for ell in range(3, LMAX + 1):
            e0, s = E0(h, lo, hi, ell)
            if e0 < 0: rows.append((float(s / (s - e0)), str(lo), str(hi), ell, str(e0), s, int(s - e0)))
    rows.sort()
    print("h=%d (depth %d): lowest critical densities dens* = s/(s+|E0|):" % (h, h + 1))
    for row in rows[:6]: print("   dens* %.4f  (a'/b', a/b] = (%s, %s]  ell=%d  E0=%s  s=%d  CORE1 needs m >= %d" % row)
