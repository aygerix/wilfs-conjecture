"""Targeted: h = 3, rho = 0, c = 4m, Gamma = base + Delta (greedy B_3 with 0), base in [4m/3, (5m - 3 span)/3):
collision-free S with E = E0 (Bacher, a'/b' = 3/2) and the test of (B): E + (k - q) >= 0.
Usage: python btest3.py NLO NHI MMULT NM"""
import sys, itertools
from math import comb
NLO, NHI, MMULT, NM = map(int, sys.argv[1:5]); h = 3
def greedy_Bh(h, k):
    D = [0]; x = 1
    while len(D) < k:
        cand = D + [x]; sums = set(); ok = True
        for cc in itertools.combinations_with_replacement(cand, h):
            v = sum(cc)
            if v in sums: ok = False; break
            sums.add(v)
        if ok: D = cand
        x += 1
    return D
for n in range(NLO, NHI + 1):
    D = greedy_Bh(h, n); delta = D[-1]; s = comb(n + h, h)
    monos = [cc for t in range(h + 1) for cc in itertools.combinations_with_replacement(range(n), t)]
    E0 = -(n + 1) * (1 + comb(n + 1, 2)) / 2 + s / 2
    found = []
    for m in range(MMULT * delta, MMULT * delta + NM):
        c = 4 * m
        for base in range(-(-4 * m // 3), (5 * m - 3 * delta) // 3 + 1):
            G = [base + d for d in D]
            if 3 * G[0] < c or 3 * G[-1] >= c + m or any(g % m == 0 for g in G): continue
            vals = {}; ok = True
            for cc in monos:
                v = sum(G[i] for i in cc)
                if v % m in vals: ok = False; break
                vals[v % m] = (v, len(cc))
            if not ok: continue
            res = (c - 1) % m
            if res in vals and vals[res][1] < h: continue
            q = 4; rho = 0; ell = n + 1
            k = sum(-(-(c - v) // m) for v, t in vals.values() if t < h)
            r = m - s; E = ell * k - q * s + rho; W = (ell + r) * k - c
            found.append((E + (k - q), E, k - q, r, W, m, base))
            if len(found) >= 3: break
        if len(found) >= 3: break
    found.sort()
    print("n=%d (s=%d, E0 formula %.1f): %s" % (n, s, E0, found[:3]), flush=True)
