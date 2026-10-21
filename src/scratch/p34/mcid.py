r"""Carry identity for Wilf when m | c (lead, 2026-10-20). Lex tile D (all generators except m), delta = gens mod m,
kappa(x) = sum_{b: delta_b > r(x)} x_b - floor(x.delta/m), K = Kunz coordinate floor(w/m), q = c/m. Claim (exact):
    W = sum_x kappa(x) + sum_{all column tops t (every direction)} |C_t| (q - K(t)).
Also reports DEP-CARRY: sum kappa + Dep >= 0 (Dep = sum over non-maximal tops of |C|), and DEP0: sum kappa >= 0 when
Dep = 0.  Usage: python mcid.py NS SEED MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
def carry_data(m, D, delta):
    N = len(delta); Ds = set(D)
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    kap = 0
    for x in D:
        v = sum(a * b for a, b in zip(x, delta)); r = v % m
        kap += sum(x[t] for t in range(N) if delta[t] > r) - v // m
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    tops = []   # (top, length)
    for b in range(N):
        for x in D:
            if x[b] == 0:
                y = x
                while up(y, b) in Ds: y = up(y, b)
                tops.append((y, y[b] + 1))
    dep = sum(L for t, L in tops if t not in mx)
    return kap, tops, dep, mx
if __name__ == '__main__':
    NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED)
    cnt = bad = 0; mind = None; dep0 = 0; mink0 = None; mism = 0
    while cnt < NS:
        m = rnd.randint(5, MMAX); q = rnd.randint(2, 8); c = q * m
        G = sorted(rnd.sample(range(m + 1, c + m), rnd.randint(2, min(8, c - 2))))
        R = build(m, G)
        if R is None or R[0] != c: continue
        c, gens, M = R; N = len(gens)
        if N < 2: continue
        cnt += 1; delta = [g % m for g in gens]
        kap, tops, dep, mx = carry_data(m, list(M), delta)
        g = sum(w // m for w in M.values()); W = (N + 1) * (c - g) - c
        rhs = kap + sum(L * (q - M[t] // m) for t, L in tops)
        if rhs != W: mism += 1
        if kap + dep < 0: bad += 1
        if mind is None or kap + dep < mind[0]: mind = (kap + dep, kap, dep, m, gens, c)
        if dep == 0:
            dep0 += 1
            if mink0 is None or kap < mink0[0]: mink0 = (kap, m, gens, c)
    print("S with m|c: %d  identity mismatches %d  DEP-CARRY fails %d  min(kap+Dep) %s" % (cnt, mism, bad, mind))
    print("Dep = 0 tiles: %d  min sum kappa %s" % (dep0, mink0))
