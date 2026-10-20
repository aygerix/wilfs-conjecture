"""CF-CORE1 check (lead, 2026-10-20). Collision-free h-regular S (Bacher 2604.25051): Delta_h(n) = {alpha in N^n :
|alpha| <= h} is injective mod m (n = ell - 1). Difference-body argument: H = {z in Z^n : |z+| <= k1, |z-| <= k2},
k1 + k2 = h, satisfies H - H in Delta_h - Delta_h, so H is injective mod m and m >= |H|, i.e. r = m - s >= |H| - s.
CORE1 (E + r >= 0) then follows wherever |H| - s >= -E0(h, a/b, ell) (E = E0 + ell*omega + rho, omega, rho >= 0).
Exact |H|: sum over (i <= k1, j <= k2) of #{z : |z+| = i, |z-| = j}
 = sum_{p,q} C(n,p) C(n-p,q) comp(i,p) comp(j,q), comp(i,p) = C(i-1,p-1) (p >= 1), comp(0,0) = 1.
Also checks Bacher Thm 3.5's hypothesis r >= ell. Usage: python cfcore.py HMAX NMAX"""
import sys
from fractions import Fraction as Fr
from math import comb
HMAX, NMAX = int(sys.argv[1]), int(sys.argv[2])
def comp(i, p): return 1 if (i == 0 and p == 0) else (comb(i - 1, p - 1) if p >= 1 and i >= p else 0)
def Hsize(n, k1, k2):
    tot = 0
    for i in range(k1 + 1):
        for j in range(k2 + 1):
            for p in range(0, min(n, i) + 1):
                for q in range(0, min(n - p, j) + 1):
                    tot += comb(n, p) * comb(n - p, q) * comp(i, p) * comp(j, q)
    return tot
def farey_pairs(h):
    fr = sorted({Fr(a, b) for b in range(1, h + 1) for a in range(b, 2 * b + 1)})
    return [(fr[i], fr[i + 1]) for i in range(len(fr) - 1)]
def E0(h, lo, ell):
    s = comb(ell + h - 1, h)
    ph = lambda i: (i * lo) - ((i * lo).numerator // (i * lo).denominator)
    return -ell * sum(ph(h - i) * comb(ell - 2 + i, i) for i in range(h)) + ph(h) * s, s
assert Hsize(2, 1, 2) == 12
bad = []; worst = None; worst35 = None
for h in range(3, HMAX + 1):
    k1, k2 = h // 2, h - h // 2
    for n in range(2, NMAX + 1):
        ell = n + 1; Hs = Hsize(n, k1, k2)
        for lo, hi in farey_pairs(h):
            if lo.denominator == 1 or hi.denominator == 1: continue
            e0, s = E0(h, lo, ell)
            assert s == comb(n + h, h)
            margin = Hs - s + e0           # >= 0 means CORE1 holds for every collision-free h-regular S here
            if worst is None or margin / s < worst[0]: worst = (float(margin / s), h, n, str(lo), str(hi), float(e0), s, Hs)
            if margin < 0: bad.append((h, n, str(lo), str(hi), float(e0), s, Hs))
            m35 = Hs - s - ell
            if worst35 is None or m35 < worst35[0]: worst35 = (m35, h, n)
print("parameter sets with |H| - s < -E0 (CORE1 not settled by the difference body):", len(bad))
for b in bad[:15]: print("   ", b)
print("worst relative margin (|H| - s + E0)/s:", worst)
print("min of |H| - s - ell (Bacher Thm 3.5 needs r >= ell):", worst35)
from collections import defaultdict
mx = defaultdict(int)
for b in bad: mx[b[0]] = max(mx[b[0]], b[1])
print("largest failing n (= ell - 1) per h:", dict(mx))
