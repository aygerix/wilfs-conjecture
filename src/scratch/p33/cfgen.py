"""Collision-free S WITHOUT regularity (unique factorization below c+m over {m} u Gamma, generators at any heights).
K = {alpha : alpha.Gamma < c+m} is injective mod m, d = |K|, r = m - d.  For each random CF S compute
  E, W, the centroid bound Ecent = rho r/m + [n c d - l sum_{K} phi]/m + (l/m) sum_{phi >= c} (phi - c)
  (exact: E = Ecent + l * sum_{phi<c} (ceil - frac) gains >= Ecent),
  the half-knapsack difference body DB = |K_half - K_half| - |K|, K_half = {phi < (c+m)/2},
  and whether Ecent + max(DB, 0) (k - q) >= -1 certifies Wilf.
Also tests the discrete centroid inequality (n+1) sum_K phi <= n (c+m) |K| (knapsack down-set).
Usage: python cfgen.py NS SEED"""
import sys, random, itertools
NS, SEED = int(sys.argv[1]), int(sys.argv[2]); random.seed(SEED)
def knap(G, T):
    """all alpha in N^n with alpha.G < T"""
    out = []
    def rec(i, a, v):
        if i == len(G): out.append(tuple(a)); return
        x = 0
        while v + x * G[i] < T:
            a.append(x); rec(i + 1, a, v + x * G[i]); a.pop(); x += 1
    rec(0, [], 0); return out
found = 0; tried = 0; cert = 0; cfail = 0; unc = []; minW = None
while found < NS:
    tried += 1
    n = random.randint(2, 4); m = random.randint(8, 150)
    c = random.randint(2 * m + 1, 8 * m)
    G = sorted(random.sample(range(m + 1, c), n))
    if any(g % m == 0 for g in G): continue
    T = c + m
    K = knap(G, T)
    if len(K) > m: continue
    vals = [sum(a * g for a, g in zip(al, G)) for al in K]
    if len({v % m for v in vals}) != len(vals): continue          # collision below c+m (CF fails)
    # minimality of generators and conductor
    S = bytearray(T); S[0] = 1
    for x in range(1, T):
        if (x >= m and S[x - m]) or any(g <= x and S[x - g] for g in G): S[x] = 1
    if S[c - 1]: continue
    if any(any(h_ != g and h_ <= g and S[g - h_] for h_ in [m] + G if h_ < g and (g - h_) % 1 == 0 and (g - h_ == 0 or True)) and False for g in G): continue
    # a generator g is non-minimal iff g - h in S for some other generator h (g - h > 0)
    bad = False
    for g in G:
        for h_ in [m] + G:
            if h_ < g and S[g - h_] and g - h_ > 0 and not (g - h_ < m and g - h_ != 0):
                bad = True
    if bad: continue
    found += 1
    q = -(-c // m); rho = q * m - c; ell = n + 1; d = len(K); r = m - d
    k = sum(-(-(c - v) // m) for v in vals if v < c)
    W = (ell + r) * k - c; E = ell * k - q * d + rho
    if minW is None or W < minW: minW = W
    phisum = sum(vals)
    Ecent = (rho * r + n * c * d - ell * phisum + ell * sum(v - c for v in vals if v >= c)) / m
    assert E >= Ecent - 1e-9
    if (n + 1) * phisum > n * T * d: cfail += 1
    half = [al for al, v in zip(K, vals) if 2 * v < T]
    D = {tuple(x - y for x, y in zip(a, b)) for a in half for b in half}
    DB = len(D) - d
    assert len(D) <= m
    if Ecent + max(DB, 0) * (k - q) >= -1: cert += 1
    elif len(unc) < 10: unc.append((m, c, G, r, DB, round(Ecent, 2), E, k - q, W))
print("tried %d, CF S %d, min W %s; discrete centroid failures %d; certified by Ecent + DB(k-q) %d" % (tried, found, minW, cfail, cert))
for u in unc: print("  UNC m=%d c=%d G=%s r=%d DB=%d Ecent=%s E=%d k-q=%d W=%d" % u)
