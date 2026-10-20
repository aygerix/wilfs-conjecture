"""Random collision-free h-regular semigroups S = <m, Gamma>_c (Bacher, arXiv:2604.25051, Defs 3.1-3.2):
h Gamma in [c, c+m), every element < c+m has a unique factorization over {m} u Gamma.
Brute force (independent of ID-q and of Bacher's E0): checks
  (DB)  r >= |H_h(n)| - C(n+h,h)               (difference body of the B_h tile)
  (EA)  E > rho r/m - n(h-1)s'/h,  s' = C(n+h-1,h-1)
  (WA)  W > (s'-1) r - n(h-1)s'/h
  (PI)  |H| - s >= n(n^2-1)/3 for h >= 3 (p=1 Vandermonde term), = n(n-1)/2 for h = 2
Usage: python cfwilf.py NS SEED"""
import sys, random
from math import comb
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from cfcore_lib import Hsize
NS, SEED = int(sys.argv[1]), int(sys.argv[2]); random.seed(SEED)
def Hform(n, h):  # Vandermonde form sum_p C(n,p) C(k1,p) C(n-p+k2,k2)
    k1, k2 = h // 2, h - h // 2
    return sum(comb(n, p) * comb(k1, p) * comb(n - p + k2, k2) for p in range(n + 1))
stats = {}; worst = {}
tried = 0; found = 0
while found < NS:
    tried += 1
    h = random.randint(2, 6); n = random.randint(1, 5); m = random.randint(5, 260)
    c = random.randint((h - 1) * m + 1, (h + 3) * m)
    lo, hi = -(-c // h), (c + m - 1) // h   # gamma with h*gamma in [c, c+m)
    lo = max(lo, m + 1)
    if hi - lo + 1 < n: continue
    G = sorted(random.sample(range(lo, hi + 1), n))
    gens = [m] + G; top = c + m
    cnt = [0] * top; cnt[0] = 1
    for g in gens:
        for x in range(g, top): cnt[x] += cnt[x - g]
    if any(v > 1 for v in cnt): continue
    if cnt[c - 1]: continue            # c must be the conductor of <m,Gamma> u [c, inf)
    # minimality of Gamma: unique factorization already implies each gamma is not a sum of others
    T = [v > 0 for v in cnt]
    k = sum(T[:c]); q = -(-c // m); rho = q * m - c
    s = sum(1 for x in range(c, c + m) if T[x]); r = m - s
    ell = n + 1; e = ell + r; g_ = c - k; W = e * k - c; E = ell * k - q * s + rho
    assert s == comb(n + h, h), (m, G, c, s)
    sp = comb(n + h - 1, h - 1); A = n * (h - 1) * sp / h
    H = Hsize(n, h // 2, h - h // 2); assert H == Hform(n, h)
    found += 1
    key = (h, n)
    ok = (r >= H - s, E > rho * r / m - A, W > (sp - 1) * r - A, W >= 0)
    st = stats.setdefault(key, [0, 0, 0, 0, 0]); st[0] += 1
    for i in range(4):
        if not ok[i]: st[i + 1] += 1
    sl = (r - (H - s), E - (rho * r / m - A), W - ((sp - 1) * r - A), W)
    w = worst.setdefault(key, list(sl))
    for i in range(4): w[i] = min(w[i], sl[i])
print("tried %d, CF h-regular found %d" % (tried, found))
for key in sorted(stats):
    h, n = key; H = Hform(n, h); s = comb(n + h, h)
    pi = n * (n * n - 1) // 3 if h >= 3 else n * (n - 1) // 2
    print("h=%d n=%d: %6d S; fails DB/EA/WA/Wilf = %s; min slacks DB %d EA %.2f WA %.2f W %d; |H|-s=%d PI-bound=%d"
          % (h, n, stats[key][0], stats[key][1:], worst[key][0], worst[key][1], worst[key][2], worst[key][3], H - s, pi))
