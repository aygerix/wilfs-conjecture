"""Heuristic check: for fixed e and generic generators m + P_a (P_a uniform in [1, m-1]), does e*ell/c -> 1 as m grows?
(volume heuristic: f_H ~ H^k/(k! prod(1+theta_a)) gives ell/c -> 1/e at leading order).  usage: python p18_asym.py seed"""
import sys, random, math
sys.path.insert(0, sys.argv[2] if len(sys.argv) > 2 else '../nowrap')
from pmin_tile import apery
rng = random.Random(int(sys.argv[1]))
for e in (3, 4, 5, 6):
    for m in (101, 401, 1601, 6401, 25601):
        rs = []
        for t in range(12 if m < 10000 else 4):
            P = sorted(rng.sample(range(1, m), e-1))
            if math.gcd(m, *P) != 1: continue
            ap = apery(m, [m+p for p in P]); c = max(ap)-m+1; g = sum(w//m for w in ap)
            rs.append(e*(c-g)/c)
        print("e=%d m=%6d  e*ell/c: mean %.4f  min %.4f  (n=%d)" % (e, m, sum(rs)/len(rs), min(rs), len(rs)), flush=True)
