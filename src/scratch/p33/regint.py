"""Integer certificate for h-regular S (PROOFS 'Regular semigroups with collisions'):
  W >= BND_int := (l + r) * sum_{1<=t<h} d_t kappa_t - q (d - l) + rho,   kappa_t = floor((x(h-t) - t)/h) + 1, x = c/m,
which uses only the degree profile d_t of M, r, and (c, m). Checks W >= BND_int on every S and reports the S with
BND_int < 0. Modes: rnd NS SEED (random, collisions encouraged) | exh MLO MHI HMAX EXTRA QMIN"""
import sys, random
from math import comb, floor
from fractions import Fraction as Fr
def profile(m, c, h, G):
    top = c + m
    T = bytearray(top); T[0] = 1; deg = [0] * top
    for x in range(1, top):
        if x >= m and T[x - m]: T[x] = 1
        for g in G:
            if g <= x and T[x - g]:
                T[x] = 1
                if not (x >= m and T[x - m]): deg[x] = deg[x - g] + 1
                break
    if T[c - 1]: return None
    dt = [0] * (h + 1); k = 0; d = 0
    for x in range(top):
        if T[x] and (x < m or not T[x - m]):
            d += 1; dt[deg[x]] += 1
            if x < c: k += -(-(c - x) // m)
    return dt, d, k
def bndint(m, c, h, n, dt, r):
    q = -(-c // m); rho = q * m - c; ell = n + 1; d = sum(dt)
    kap = [((c * (h - t) - t * m) // (h * m)) + 1 for t in range(h + 1)]   # floor((x(h-t)-t)/h)+1, exact
    return (ell + r) * sum(dt[t] * kap[t] for t in range(1, h)) - q * (d - ell) + rho
tot = 0; neg = []; minslack = None
def test(m, c, h, G):
    global tot, minslack
    pr = profile(m, c, h, G)
    if pr is None: return
    dt, d, k = pr; n = len(G); r = m - d; ell = n + 1
    W = (ell + r) * k - c; b = bndint(m, c, h, n, dt, r)
    assert W >= b, (m, c, G, W, b)
    tot += 1
    if n >= 2 and (minslack is None or b < minslack[0]): minslack = (b, m, c, h, G, dt, r, W)
    if b < 0: neg.append((m, c, h, G, dt, r, W, b))
if sys.argv[1] == 'rnd':
    NS, SEED = int(sys.argv[2]), int(sys.argv[3]); random.seed(SEED)
    while tot < NS:
        h = random.choice([2, 3, 3, 4, 4, 5, 6]); n = random.randint(1, 7); s = comb(n + h, h)
        m = random.randint(max(n * h + 2, 5), max(n * h + 3, s + 5))
        c = random.randint(max((h - 1) * m + 1, 4 * m + 1), (h + 4) * m)
        lo, hi = max(-(-c // h), m + 1), (c + m - 1) // h
        cand = [g for g in range(lo, hi + 1) if g % m]
        if len(cand) < n: continue
        test(m, c, h, sorted(random.sample(cand, n)))
else:
    MLO, MHI, HMAX, EXTRA, QMIN = map(int, sys.argv[2:7])
    for m in range(MLO, MHI + 1):
        for h in range(2, HMAX + 1):
            for c in range((h - 1) * m + 1, (h + EXTRA) * m + 1):
                if -(-c // m) < QMIN: continue
                lo, hi = max(-(-c // h), m + 1), (c + m - 1) // h
                cand = [g for g in range(lo, hi + 1) if g % m]
                for mask in range(1, 1 << len(cand)):
                    test(m, c, h, [cand[i] for i in range(len(cand)) if mask >> i & 1])
print("S tested %d; BND_int < 0: %d (n=1: %d); min BND_int over n >= 2: %s" % (tot, len(neg), sum(1 for t in neg if len(t[3]) == 1), minslack))
for t in [t for t in neg if len(t[3]) > 1][:10]: print("  NEG m=%d c=%d h=%d G=%s dt=%s r=%d W=%d bnd=%d" % t)
