"""h-regular S with many collisions (m small relative to C(n+h,h)): difference body with collisions.
For each S: M (lex-least factorizations of Apery elements < c+m), U = Delta_h \\ M, r, X = sum_U f, B, k,
|phi(H)| (residues of H = A_{k1} - A_{k2}), coinc = |H| - |phi(H)|, the REG-BND value, W.
Reports correlations: is coinc <= C * X, is r >= |H| - s + |U| - coinc (DB, always), and the minimum of
REG-BND over S with q >= 5.  Usage: python regdb.py NS SEED"""
import sys, random, itertools
from math import comb
from fractions import Fraction as Fr
NS, SEED = int(sys.argv[1]), int(sys.argv[2]); random.seed(SEED)
def monos(n, t):
    for c in itertools.combinations_with_replacement(range(n), t):
        a = [0] * n
        for i in c: a[i] += 1
        yield tuple(a)
found = 0; worst = []; ratio = []; keyrows = []
while found < NS:
    h = random.choice([2, 3, 3, 4, 4, 5]); n = random.randint(2, 7)
    s = comb(n + h, h)
    m = random.randint(max(n * h + 2, 5), max(n * h + 3, s + 5))
    c = random.randint(max((h - 1) * m + 1, 4 * m + 1), (h + 3) * m)
    lo, hi = max(-(-c // h), m + 1), (c + m - 1) // h
    cand = [g for g in range(lo, hi + 1) if g % m]
    if len(cand) < n: continue
    G = sorted(random.sample(cand, n))
    top = c + m
    T = bytearray(top); T[0] = 1
    for x in range(1, top):
        for g in [m] + G:
            if g <= x and T[x - g]: T[x] = 1; break
    if T[c - 1]: continue
    found += 1
    q = -(-c // m); rho = q * m - c; ell = n + 1
    # residue -> minimal value, via all monomials of degree <= h (values < c+m)
    best = {}
    allm = [a for t in range(h + 1) for a in monos(n, t)]
    val = {a: sum(ai * g for ai, g in zip(a, G)) for a in allm}
    for a in sorted(allm, key=lambda a: (val[a], [-x for x in a])):
        res = val[a] % m
        if res not in best: best[res] = a
    M = set(best.values()); U = [a for a in allm if a not in M]
    d = len(M); r = m - d
    k = sum(-(-(c - val[a]) // m) for a in M if val[a] < c)
    W = (ell + r) * k - c
    f = lambda t: 1 - Fr((n + 1) * (h - t), h)
    X = sum(f(sum(a)) for a in U)
    B = Fr(ell, h) * sum(sum(a) for a in M if sum(a) < h)
    x = Fr(c, m)
    bnd = Fr(rho * r, m) + x * X - B + r * (k - q)
    k1, k2 = h // 2, h - h // 2
    A1 = [a for t in range(k1 + 1) for a in monos(n, t)]; A2 = [a for t in range(k2 + 1) for a in monos(n, t)]
    Hset = {tuple(p - q_ for p, q_ in zip(a, b)) for a in A1 for b in A2}
    img = {sum(z_ * g for z_, g in zip(z, G)) % m for z in Hset}
    coinc = len(Hset) - len(img)
    assert len(img) <= m and W > bnd
    # REG-KEY bookkeeping: W > rho r/m - A + sum_U psi + r K,  K = k - q
    A = Fr(n * (h - 1) * comb(n + h - 1, h - 1), h)
    psi = lambda t: x * f(t) + (Fr(ell * t, h) if t < h else 0)
    SU = sum(psi(sum(a)) for a in U); K = k - q
    assert W > Fr(rho * r, m) - A + SU + r * K
    rneed = (A - 1 - SU) / K if K else Fr(10 ** 9)
    rdb = len(Hset) - comb(n + h, h) + len(U) - coinc
    keyrows.append((float(SU / A), float(rneed), r, rdb, h, n, m, c, G))
    ratio.append((coinc, float(X), len(U), r, float(bnd), W, h, n, m, c, G))
print("S tested:", found)
for h in sorted({t[6] for t in ratio}):
    R = [t for t in ratio if t[6] == h]
    unc = [t for t in R if t[4] < -1]
    cx = [t[0] / t[1] for t in R if t[1] > 0]
    print("h=%d: %d S, r=0: %d, uncertified %d, max coinc/X %.2f, min W %d" % (h, len(R), sum(1 for t in R if t[3] == 0), len(unc), max(cx) if cx else 0, min(t[5] for t in R)))
    for t in unc[:6]: print("   UNC coinc=%d X=%.2f |U|=%d r=%d bnd=%.2f W=%d h=%d n=%d m=%d c=%d G=%s" % t)

few = [t for t in keyrows if t[0] < 1]
print("S with sum_U psi < A (collisions do not pay alone): %d of %d" % (len(few), len(keyrows)))
print("  among them: r >= rneed always? %s;  coinc-DB bound >= rneed: %d of %d" % (all(t[2] >= t[1] for t in few), sum(1 for t in few if t[3] >= t[1]), len(few)))
bad = [t for t in few if t[3] < t[1]]
for t in sorted(bad, key=lambda t: t[3] - t[1])[:8]: print("   coincDB fails: SU/A=%.2f rneed=%.2f r=%d rdb=%d h=%d n=%d m=%d c=%d G=%s" % t)
mx = max((t[1] for t in few), default=0); print("  max rneed among them %.2f" % mx)
