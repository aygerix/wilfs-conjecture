"""(B) in Bacher's negative regime: h = 3, Gamma = base + Delta (Delta = greedy B_3 set with 0, size n),
base/m scanned over [1.0, 2.0) (all Farey intervals), every valid c (3 Gamma in [c, c+m), c-1 not in S).
Only CF S are kept (brute force). Prints min E, min E + (k - q), min CORE1 = E + r per n.
Usage: python btest2.py NLO NHI EXTRAS(comma; m = 3*span + 2 + extra) NBASE (base samples per m)"""
import sys, itertools
from math import comb
NLO, NHI = int(sys.argv[1]), int(sys.argv[2]); MS = [int(x) for x in sys.argv[3].split(',')]; NBASE = int(sys.argv[4])
h = 3
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
    best = {'E': None, 'B': None, 'C': None}; cnt = 0
    for ex in MS:
        m = h * delta + 2 + ex
        for base in sorted(set(m + 1 + (j * (m - 2)) // NBASE for j in range(NBASE))):
            G = [base + d for d in D]
            if any(g % m == 0 for g in G): continue
            vals = {}; ok = True
            for cc in monos:
                v = sum(G[i] for i in cc)
                if v % m in vals: ok = False; break
                vals[v % m] = (v, len(cc))
            if not ok: continue
            for c in range(max(h * G[-1] - m + 1, (h - 1) * m + 1), h * G[0] + 1):
                res = (c - 1) % m
                if res in vals and vals[res][1] < h: continue
                q = -(-c // m); rho = q * m - c; ell = n + 1
                k = sum(-(-(c - v) // m) for v, t in vals.values() if t < h)
                r = m - s; E = ell * k - q * s + rho; W = (ell + r) * k - c
                assert W >= 0
                cnt += 1
                rec = (E, E + (k - q), E + r, k - q, r, rho, m, c, base)
                for key, idx in (('E', 0), ('B', 1), ('C', 2)):
                    if best[key] is None or rec[idx] < best[key][idx]: best[key] = rec
    print("n=%d s=%d span=%d: %d CF S" % (n, s, delta, cnt))
    for key in 'EBC': print("   min %s: (E, E+(k-q), E+r, k-q, r, rho, m, c, base) = %s" % ({'E': 'E', 'B': 'E+(k-q)', 'C': 'CORE1'}[key], best[key]))
    sys.stdout.flush()
