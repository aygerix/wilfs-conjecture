"""Who pays the top loss? (lead, 2026-10-20). Ray identity W = rho r/m + G + Pt - Lam + r(k-q) on random S (c > DMIN*m,
n >= 2 left generators). Reports the fraction with Lam > G, Lam > G + Pt, and the r = 0 subclass. Also the box bound
G_box := (n+1) * sum_{beta in B(omega), phi(beta) < c} theta'(beta) (omega = factorization of F+m when in M).
Usage: python payers.py NS SEED MMAX DMIN"""
import sys, random
from fractions import Fraction as Fr
sys.path.insert(0, '/home/jmercedes/wilf/p32'); sys.path.insert(0, '.')
def stats(m, G, c):
    n = len(G); T = c + m
    S = bytearray(T); S[0] = 1
    for x in range(1, T):
        if (x >= m and S[x - m]) or any(g <= x and S[x - g] for g in G): S[x] = 1
    if S[c - 1]: return None
    fac = {0: (0,) * n}
    for x in range(1, T):
        if not S[x] or (x >= m and S[x - m]): continue
        best = None
        for i, g in enumerate(G):
            if g <= x and (x - g) in fac:
                a = list(fac[x - g]); a[i] += 1; a = tuple(a)
                if best is None or a[::-1] < best[::-1]: best = a
        fac[x] = best
    M = {a: x for x, a in fac.items()}
    q = -(-c // m); rho = q * m - c; ell = n + 1; d = len(M); r = m - d
    k = sum(-(-(c - x) // m) for x in M.values() if x < c)
    W = (ell + r) * k - c
    th = lambda x: Fr((x - c) % m, m)
    Gn = ell * sum(th(x) for x in M.values() if x < c)
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(n))
    Pt = sum(Fr((a[i] + 1) * (c - x), m) for a, x in M.items() if x < c for i in range(n) if up(a, i) not in M)
    Lam = sum(Fr((sum(a) - 1) * (x - c), m) for a, x in M.items() if x >= c)
    assert W == Fr(rho * r, m) + Gn + Pt - Lam + r * (k - q)
    return W, r, Gn, Pt, Lam, Fr(rho * r, m) + r * (k - q)
NS, SEED, MMAX, DMIN = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
tot = lg = lgp = r0 = r0lg = 0; worst = None
for _ in range(NS):
    m = rnd.randint(6, MMAX); n = rnd.randint(2, 6); c = rnd.randint(DMIN * m + 1, 10 * m)
    hi = rnd.choice([2 * m, 3 * m, c])
    if min(hi, c) - m - 1 < n: continue
    G = sorted(rnd.sample(range(m + 1, min(hi, c)), n))
    if any(g % m == 0 for g in G): continue
    # minimality of G among left generators
    if any(any((g - h) > 0 and any((g - h - j * m) >= 0 and (g - h - j * m) in (0,) for j in range(g // m + 1)) for h in G if h < g) for g in G): pass
    v = stats(m, G, c)
    if v is None: continue
    W, r, Gn, Pt, Lam, Rr = v; tot += 1
    if Lam > Gn: lg += 1
    if Lam > Gn + Pt: lgp += 1
    if r == 0:
        r0 += 1
        if Lam > Gn: r0lg += 1
    rat = (Lam - Gn) / (Pt + Rr + 1)
    if worst is None or rat > worst[0]: worst = (float(rat), m, G, c, float(Gn), float(Pt), float(Lam), float(Rr), W, r)
print("S", tot, " Lam>G:", lg, " Lam>G+Pt:", lgp, " r=0:", r0, " r=0 & Lam>G:", r0lg)
print("max (Lam-G)/(Pt+rterms+1):", worst)
