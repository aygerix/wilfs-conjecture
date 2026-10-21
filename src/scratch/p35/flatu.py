r"""FLAT-U identity check (lead, 2026-10-20).  For S whose lex tile D has height <= 2 (cells 0, units e_b, pairs P):
    W = (e+1) sum_P mu_p + sum_b (e - deg b) mu_b + rho + sum_P tau_p,
with mu_x = ceil((c - w(x))/m)^+, r = <w - c>, c = q m - rho, deg b = sum_{p in P} p_b (loop counts 2) <= e, and
tau_p = (r_a + r_b - r_p - rho)/m in {-1, 0, 1} (exact Kunz relation mu_a + mu_b = q + mu_p + tau_p); tau_p = -1 only if
r_p >= m - rho (at most rho such cells).  Hence W >= 0.  Also checks the binary-split relation on every split of every cell
of every tested tile (any height).  Usage: python flatu.py NS SEED MMAX"""
import sys, random
sys.path.insert(0, '../p34')
from tile import build
NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED); nflat = nall = nsplit = 0; minW = None
while nall < NS:
    m = rnd.randint(3, MMAX); n = rnd.randint(1, max(1, m - 1)); K = rnd.randint(2, 5)
    G = [m] + rnd.sample(range(m + 1, K * m), min(n, K * m - m - 1))
    res = build(m, G)
    if res is None: continue
    c, gens, M = res; D = list(M); d = len(gens); e = d + 1
    if c <= 0: continue
    nall += 1; Ds = set(D)
    w = {x: sum(a * b for a, b in zip(x, gens)) for x in D}
    mu = {x: max(0, -((w[x] - c) // m)) for x in D}; r = {x: (w[x] - c) % m for x in D}
    q = -(-c // m); rho = q * m - c
    W = e * sum(mu.values()) - c
    for z in D:
        if sum(z) < 2: continue
        for x in D:
            if x == z or not any(x) or any(a > b for a, b in zip(x, z)): continue
            y = tuple(b - a for a, b in zip(x, z)); assert y in Ds
            t = mu[x] + mu[y] - q - mu[z]
            assert t * m == r[x] + r[y] - r[z] - rho and t in (-1, 0, 1), (G, z, x, t)
            if t == -1: assert r[z] >= m - rho
            nsplit += 1
    if max(sum(x) for x in D) > 2: continue
    nflat += 1
    P = [x for x in D if sum(x) == 2]
    deg = [sum(p[b] for p in P) for b in range(d)]; assert max(deg, default=0) <= e
    unit = lambda b: tuple(int(t == b) for t in range(d))
    tau = {}
    for p in P:
        a = [b for b in range(d) if p[b]]; a, b = (a[0], a[0]) if len(a) == 1 else (a[0], a[1])
        tau[p] = (r[unit(a)] + r[unit(b)] - r[p] - rho) // m
    rhs = (e + 1) * sum(mu[p] for p in P) + sum((e - deg[b]) * mu[unit(b)] for b in range(d)) + rho + sum(tau.values())
    assert rhs == W, (G, W, rhs)
    assert sum(1 for p in P if tau[p] == -1) <= rho
    minW = W if minW is None else min(minW, W)
print("tested %d S (%d flat), %d splits: identity and split relation hold; min W on flat = %s" % (nall, nflat, nsplit, minW))
