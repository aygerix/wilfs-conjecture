"""Difference-body helpers (from cfcore.py): |H| for H = {z in Z^n : |z+| <= k1, |z-| <= k2}."""
from math import comb
def comp(i, p): return 1 if (i == 0 and p == 0) else (comb(i - 1, p - 1) if p >= 1 and i >= p else 0)
def Hsize(n, k1, k2):
    tot = 0
    for i in range(k1 + 1):
        for j in range(k2 + 1):
            for p in range(0, min(n, i) + 1):
                for q in range(0, min(n - p, j) + 1):
                    tot += comb(n, p) * comb(n - p, q) * comp(i, p) * comp(j, q)
    return tot
