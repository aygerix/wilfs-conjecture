r"""MD on hard families (lead, 2026-10-20): e = 2 (perfect matching forced), near-sharp intervals <m, a..a+d>, and the
Wilf-equality family.  usage: mdhard.py e2 mlo mhi | ivl m1 m2 | eq"""
import sys, math
sys.path.insert(0, ".")
from md import analyse
a = sys.argv[1:]
bad = 0; n = 0
if a[0] == "e2":
    for m in range(int(a[1]), int(a[2]) + 1):
        for g in range(m + 1, 4 * m):
            if math.gcd(m, g) != 1: continue
            r = analyse([m, g])
            if r is None: continue
            n += 1
            if r["MD"] < 0 or r["TMD"] < 0: bad += 1; print("FAIL", r) if bad < 5 else None
elif a[0] == "ivl":
    for m in range(int(a[1]), int(a[2]) + 1):
        best = None
        for aa in range(m + 1, 2 * m + 1):
            for d in range(1, m):
                if aa + d >= 2 * m + m: continue
                r = analyse([m] + list(range(aa, aa + d + 1)))
                if r is None: continue
                n += 1
                if r["MD"] < 0 or r["TMD"] < 0: bad += 1; print("FAIL", r) if bad < 5 else None
else:
    for m in range(3, 12):
        for k in range(1, 6):
            r = analyse([m] + list(range(k * m + 1, k * m + m)))
            if r is None: continue
            n += 1
            if r["MD"] < 0 or r["TMD"] < 0: bad += 1; print("FAIL", r)
print(a, "S", n, "fails", bad)
