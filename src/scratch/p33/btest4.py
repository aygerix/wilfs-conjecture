"""Decisive test of (B): h = 3, c = 4m (rho = 0), Gamma = base + Delta inside (1.5m, 5m/3) so that kappa_1 = 3,
kappa_2 = 1, 3-sums in [4m, 5m): k - q = 3n + C(n+1,2) and E = (n+1)(4 + 3n + C(n+1,2)) - 4 C(n+3,3) = E0.
Search m in [6 span + 6, 6 span + 6 + NM), base in (1.5m, 5m/3 - span), keep collision-free S with c - 1 not in S.
Usage: python btest4.py N NM"""
import sys, itertools
from math import comb
N, NM = int(sys.argv[1]), int(sys.argv[2]); h = 3
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
n = N; D = greedy_Bh(h, n); delta = D[-1]; s = comb(n + h, h)
monos = [cc for t in range(h + 1) for cc in itertools.combinations_with_replacement(range(n), t)]
pred = (n + 1) * (4 + 3 * n + comb(n + 1, 2)) - 4 * comb(n + 3, 3)
print("n=%d span=%d s=%d predicted E=%d, k-q=%d, E+(k-q)=%d" % (n, delta, s, pred, 3 * n + comb(n + 1, 2), pred + 3 * n + comb(n + 1, 2)), flush=True)
hits = 0
for m in range(6 * delta + 6, 6 * delta + 6 + NM):
    c = 4 * m
    for base in range(3 * m // 2 + 1, (5 * m) // 3 - delta):
        G = [base + d for d in D]
        if not (2 * G[0] > 3 * m and 3 * G[-1] < 5 * m and 3 * G[0] >= 4 * m): continue
        vals = {}; ok = True
        for cc in monos:
            v = sum(G[i] for i in cc)
            if v % m in vals: ok = False; break
            vals[v % m] = (v, len(cc))
        if not ok: continue
        if ((c - 1) % m) in vals and vals[(c - 1) % m][1] < h: continue
        # brute-force recomputation of the semigroup S = <m, G> u [c, inf)
        top = c + m; T = bytearray(top); T[0] = 1
        for x in range(1, top):
            if (x >= m and T[x - m]) or any(g <= x and T[x - g] for g in G): T[x] = 1
        assert not T[c - 1]
        k = sum(T[:c]); q = 4; rho = 0
        gens = [m] + G + [x for x in range(c, c + m) if not any(g <= x and T[x - g] and (x - g == 0 or x - g >= m) for g in [m] + G)]
        # right primitives: x in [c, c+m) not a sum of two nonzero elements of S
        rp = [x for x in range(c, c + m) if not any(T[y] and (x - y >= c or T[x - y]) for y in range(m, x - m + 1))]
        r = len(rp); e = n + 1 + r; W = e * k - c; E = (n + 1) * k - q * (m - r) + rho
        print("  HIT m=%d c=%d Gamma=%s r=%d k=%d E=%d k-q=%d E+(k-q)=%d E+r=%d W=%d" % (m, c, G, r, k, E, k - q, E + k - q, E + r, W), flush=True)
        hits += 1
        if hits >= 3: sys.exit(0)
print("no hit")
