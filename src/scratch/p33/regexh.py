"""Exhaustive h-regular S = <m, Gamma>_c with depth q >= QMIN: all m in [MLO, MHI], h in [2, HMAX],
c in ((h-1)m, (h+EXTRA)m] with q >= QMIN, all nonempty Gamma in [ceil(c/h), floor((c+m-1)/h)] cap (m, inf), no
multiple of m. Computes W and the certificate BND = rho r/m + sum_t g(t) d_t + r(k-q), g(t) = (x n h - t l (x+1))/h,
x = c/m (PROOFS "Regular semigroups with collisions"). Reports W failures and uncertified S (BND < -1).
Usage: python regexh.py MLO MHI HMAX EXTRA QMIN"""
import sys
from fractions import Fraction as Fr
MLO, MHI, HMAX, EXTRA, QMIN = map(int, sys.argv[1:6])
tot = 0; wf = 0; unc = 0; ex = []; minW = None
for m in range(MLO, MHI + 1):
    for h in range(2, HMAX + 1):
        for c in range((h - 1) * m + 1, (h + EXTRA) * m + 1):
            q = -(-c // m)
            if q < QMIN: continue
            rho = q * m - c
            lo, hi = max(-(-c // h), m + 1), (c + m - 1) // h
            cand = [g for g in range(lo, hi + 1) if g % m]
            L = len(cand)
            for mask in range(1, 1 << L):
                G = [cand[i] for i in range(L) if mask >> i & 1]
                n = len(G); ell = n + 1; top = c + m
                T = bytearray(top); T[0] = 1; deg = [0] * top
                for x in range(1, top):
                    if x >= m and T[x - m]: T[x] = 1
                    for g in G:
                        if g <= x and T[x - g]:
                            T[x] = 1
                            if not (x >= m and T[x - m]): deg[x] = deg[x - g] + 1
                            break
                if T[c - 1]: continue
                tot += 1
                dt = [0] * (h + 1); k = 0; d = 0
                for x in range(top):
                    if T[x] and (x < m or not T[x - m]):
                        d += 1; dt[deg[x]] += 1
                        if x < c: k += -(-(c - x) // m)
                r = m - d; W = (ell + r) * k - c
                if minW is None or W < minW: minW = W
                if W < 0: wf += 1; print("WILF FAIL", m, c, G)
                xx = Fr(c, m)
                bnd = Fr(rho * r, m) + sum((xx * n * h - t * ell * (xx + 1)) / h * dt[t] for t in range(h)) - xx * dt[h] + r * (k - q)
                assert W > bnd, (m, c, G)
                if bnd < -1:
                    unc += 1
                    if len(ex) < 15: ex.append((m, h, c, G, r, W, float(bnd), dt))
print("m %d..%d, h <= %d, q >= %d: %d S, Wilf failures %d, min W %s, uncertified %d" % (MLO, MHI, HMAX, QMIN, tot, wf, minW, unc))
for e in ex: print("  UNC m=%d h=%d c=%d G=%s r=%d W=%d bnd=%.2f dt=%s" % e)
