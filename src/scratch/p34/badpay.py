r"""Who pays the negative carries at sigma = phi(0) (lead, 2026-10-21). For lex Apery tiles of random S and units u:
B = sum of |kappa| over cells with kappa < 0, P = sum of positive kappa, L = Lnm/m.  MaxCL(0): P + L >= B.
Reports min (P+L)/B, min P/B, and the share of L.  kappa(x) = sum_{b: delta_b > r(x)} x_b - floor(x.delta/m).
Usage: python badpay.py NS SEED MMIN MMAX"""
import sys, random
from math import gcd
sys.path.insert(0, '.')
from tile import build
from levels0 import levels
NS, SEED, MMIN, MMAX = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
cnt = 0; nb = 0; best = None; bestP = None; rows = []
while cnt < NS:
    m = rnd.randint(MMIN, MMAX); G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 4]) * m), rnd.randint(2, min(8, m - 2))))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; N = len(gens); D = list(M)
    if N < 2: continue
    for u in [u for u in range(1, m) if gcd(u, m) == 1][:4]:
        delta = [(u * g) % m for g in gens]; cnt += 1
        kap = []
        for x in D:
            v = sum(a * b for a, b in zip(x, delta)); r = v % m
            kap.append(sum(x[t] for t in range(N) if delta[t] > r) - v // m)
        B = -sum(k for k in kap if k < 0); P = sum(k for k in kap if k > 0)
        gam, L = levels(m, D, delta); L = float(L)
        assert P - B == sum(gam)
        if B == 0: continue
        nb += 1; q = (P + L) / B
        rows.append((q, P / B, L / B, m, gens, u, B))
rows.sort()
print("instances %d with bad cells %d" % (cnt, nb))
for z in rows[:12]: print("  (P+L)/B %.3f  P/B %.3f  L/B %.3f  m=%d gens=%s u=%d B=%d" % z)
rp = sorted(rows, key=lambda z: z[1])
print("min P/B rows:")
for z in rp[:6]: print("  (P+L)/B %.3f  P/B %.3f  L/B %.3f  m=%d gens=%s u=%d B=%d" % z)
