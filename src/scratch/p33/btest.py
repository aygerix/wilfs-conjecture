"""Scaling test of (B): r >= 1 => E + (k - q) >= 0, on collision-free h-regular S with MANY left generators
(Bacher regime: E = E0 + l*omega + rho with E0 ~ -l * sum phi' s_i, while k - q ~ x s / l).
For h, n: Delta = greedy B_h set of size n containing 0; Gamma = base + Delta with base chosen so that Gamma fits
in a window of length < m/h; scan m (CF checked by brute force) and every valid c (h Gamma in [c, c+m), c-1 not in S).
Reports min (E + (k-q)), min E/(k-q), and CORE1 = E + r.  Usage: python btest.py H NLO NHI MSTEPS"""
import sys, itertools
from math import comb
H, NLO, NHI, MSTEPS = map(int, sys.argv[1:5])
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
h = H
for n in range(NLO, NHI + 1):
    D = greedy_Bh(h, n); delta = D[-1]
    s = comb(n + h, h); worst = None; worstC = None; cnt = 0
    for m in range(max(s, h * delta + 2), max(s, h * delta + 2) + MSTEPS):
        # Gamma = base + D, need h*(base+delta) - (h*base) = h*delta < m  (window), base > m
        for base in range(m + 1, 2 * m + 1):
            G = [base + d for d in D]
            if any(g % m == 0 for g in G): continue
            # CF: residues of all alpha.Gamma, |alpha| <= h, distinct mod m (and integers distinct)
            vals = {}
            ok = True
            for t in range(h + 1):
                for cc in itertools.combinations_with_replacement(range(n), t):
                    v = sum(G[i] for i in cc)
                    if v % m in vals: ok = False; break
                    vals[v % m] = (v, t)
                if not ok: break
            if not ok: continue
            for c in range(h * G[-1] - m + 1, h * G[0] + 1):
                if c <= (h - 1) * m: continue
                res = (c - 1) % m
                if res in vals and vals[res][1] < h: continue   # c-1 in S
                q = -(-c // m); rho = q * m - c; ell = n + 1
                k = sum(-(-(c - v) // m) for v, t in vals.values() if t < h)
                r = m - s; E = ell * k - q * s + rho; W = (ell + r) * k - c
                assert W >= 0, (m, G, c)
                B_ = E + (k - q); cnt += 1
                if worst is None or B_ < worst[0]: worst = (B_, E, k - q, r, m, c, G[:3] + ['...'])
                if worstC is None or E + r < worstC[0]: worstC = (E + r, E, r, m, c)
            break   # one base per m (smallest valid) keeps the scan cheap
    print("h=%d n=%d (Delta span %d, s=%d): %d S; min E+(k-q) = %s; min CORE1 = %s" % (h, n, delta, s, cnt, worst, worstC), flush=True)
