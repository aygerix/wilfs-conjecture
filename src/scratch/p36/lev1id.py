r"""Identity check (lead, 2026-10-21): if every minimal generator other than m lies in (m, 2m), then for every s, with any
factorization of w_s of length h_s and integer residue sum sigma_s (w_s = h_s m + sigma_s),
    mu_s = q - h_s - #{j >= 0 : sigma_s > j m + r},       hence  l = qm - H - sum_{j>=0} N(jm + r),  N(t) = #{s : sigma_s > t}.
Random S (any depth q, any height).  usage: /usr/bin/python3 lev1id.py NS SEED"""
import sys, random, math
sys.path.insert(0, '.')
from kunz_face import apery
NS, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed); n = 0; qs = set()
while n < NS:
    m = rng.randint(5, 40); d = rng.randint(1, min(8, m - 2)); G = [m] + [m + x for x in rng.sample(range(1, m), d)]
    if math.gcd(*G) != 1: continue
    w = apery(m, G); c = max(w) - m + 1; q = -(-c // m); r = w.index(max(w))
    if c <= 0: continue
    mu = [max(0, -((w[s] - c) // m)) for s in range(m)]; mu[0] = q
    # one factorization per Apery element (greedy along w order)
    fac = {0: (0, 0)}
    for s in sorted(range(1, m), key=lambda x: w[x]):
        for g in G[1:]:
            t = (w[s] - g) % m
            if w[s] - g >= 0 and w[t] == w[s] - g and t in fac: fac[s] = (fac[t][0] + 1, fac[t][1] + g - m); break
    assert len(fac) == m
    for s in range(m):
        h, sig = fac[s]; assert w[s] == h * m + sig
        cnt = 0; j = 0
        while sig > j * m + r: cnt += 1; j += 1
        assert mu[s] == q - h - cnt, (G, s, mu[s], q, h, sig, r)
    n += 1; qs.add(q)
print("identity verified on %d random S generated in (m, 2m); depths q seen: %s" % (n, sorted(qs)[:12]))
