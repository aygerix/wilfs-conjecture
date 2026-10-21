r"""Exhaustive small tiles at sigma = phi(0) (lead, 2026-10-20): for every down-set D in N^N (N = 2, 3) of size m and
every p with injective labels, gamma_j (levels0.py).  Tests SUF2: sum_{i>=j} gamma_i >= 0 for all j >= 2;
LOW1: gamma_1 + Lnm/m >= 0;  MaxCL(0): sum gamma + Lnm/m >= 0; and the cell identity
sum_j gamma_j = sum_x (h(x) - K(x)), h(x) = sum_{b: delta_b > r(x)} x_b.   Usage: python levels0c.py N MMIN MMAX"""
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from subadd_lp import downsets
from levels0 import levels
N, MMIN, MMAX = map(int, sys.argv[1:4])
for m in range(MMIN, MMAX + 1):
    tot = fs = fl = fm = 0; ex = []
    for D in downsets(N, m):
        for b in itertools.product(range(1, m), repeat=N):
            e = {a: sum(x * y for x, y in zip(a, b)) % m for a in D}
            if len(set(e.values())) != m: continue
            tot += 1
            gam, L = levels(m, D, list(b))
            cell = sum(sum(x[t] for t in range(N) if b[t] > e[x]) - sum(x[t] * b[t] for t in range(N)) // m for x in D)
            assert cell == sum(gam), (D, b)
            if any(sum(gam[j:]) < 0 for j in range(1, len(gam))):
                fs += 1
                if len(ex) < 3: ex.append(("SUF2", D, b, gam))
            if gam and gam[0] + L < 0:
                fl += 1
                if len(ex) < 6: ex.append(("LOW1", D, b, gam, float(L)))
            if sum(gam) + L < 0: fm += 1
    print("N=%d m=%d instances %d  SUF2 fails %d  LOW1 fails %d  MaxCL0 fails %d" % (N, m, tot, fs, fl, fm), flush=True)
    for z in ex: print("   ", z)
