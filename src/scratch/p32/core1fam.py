"""CORE1 = W0 + p on known negative-Eliahou families (lead, 2026-10-20): truncations <A>_c (T = <A> u [c, inf), c(T) = c
required). W0 = n*ell - q*d + rho with n = #left primitives, d = #decomposables in [c, c+m), p = m - d.
Families: Delgado S(p) = <mu, gamma, gamma+1>_{p*mu}; Fromentin's five; <30,44,48,49>_118; EF B3 family (random B3
sets in ((3m+1)/2, (5m-1)/3) at c = 4m). Usage: python core1fam.py"""
import itertools, random

def trunc(A, c):
    m = min(A)
    T = [False] * (c + 2 * m + 2)
    T[0] = True
    for x in range(1, c):
        T[x] = any(a <= x and T[x - a] for a in A)
    for x in range(c, len(T)): T[x] = True
    if T[c - 1]: return None
    ell = sum(T[:c])
    gaps = [x for x in range(c) if not T[x]]
    # primitives of T below c
    prim = [x for x in range(1, c) if T[x] and not any(T[y] and T[x - y] for y in range(1, x // 2 + 1))]
    n = len(prim)
    d = sum(1 for x in range(c, c + m) if any(T[y] and T[x - y] for y in range(1, x // 2 + 1)))
    q = -(-c // m); rho = q * m - c; p = m - d
    W0 = n * ell - q * d + rho
    W = (n + p) * ell - c
    return dict(m=m, c=c, q=q, n=n, ell=ell, d=d, p=p, W0=W0, CORE1=W0 + p, W=W)

out = []
for A, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((17, 27, 28), 68), ((18, 28, 29), 72), ((30, 44, 48, 49), 118)]:
    out.append(("known", A, trunc(list(A), c)))
worst = None; neg = 0; tot = 0
for mu in range(5, 60):
    for gam in range(mu + 1, 2 * mu):
        for pp in range(3, 12):
            r = trunc([mu, gam, gam + 1], pp * mu)
            if r is None: continue
            tot += 1
            if r['W0'] < 0: neg += 1
            if worst is None or r['CORE1'] < worst[1]['CORE1']: worst = ((mu, gam, gam + 1, pp), r)
out.append(("Delgado S(p) scan: %d truncations, %d with W0 < 0; min CORE1" % (tot, neg), worst[0], worst[1]))
rnd = random.Random(5); worstEF = None
for trial in range(400):
    m = rnd.randint(14, 90); K = rnd.randint(2, 5)
    lo, hi = (3 * m + 1 + 1) // 2, (5 * m - 1) // 3
    if hi - lo + 1 < K: continue
    A = sorted(rnd.sample(range(lo, hi + 1), K))
    sums = [sum(c) % m for c in itertools.combinations_with_replacement(A, 3)]
    if len(set(sums)) != len(sums): continue
    r = trunc([m] + A, 4 * m)
    if r is None: continue
    if worstEF is None or r['CORE1'] < worstEF[1]['CORE1']: worstEF = ([m] + A, r)
out.append(("EF B3 family (random B3 sets), min CORE1", worstEF[0], worstEF[1]))
for o in out: print(o)
