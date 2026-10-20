"""Ray identity (every numerical semigroup), canonical down-set M (lex-least factorizations over Gamma = left
generators other than m of the Apery elements of <m,Gamma> below c+m), phi(alpha) = alpha.Gamma:
   E = rho r/m + G + Ptil - Lam,
   G    = l * sum_{beta in M, phi < c} (ceil((c - phi)/m) - (c - phi)/m)          (ceiling gains, >= 0)
   Ptil = sum_{beta in M, i : end of the i-ray from beta has phi < c} (c - phi(end))/m   (early ray ends, >= 0)
   Lam  = sum_{y in M, c <= phi(y) < c+m} (|y| - 1)(phi(y) - c)/m                   (top loss)
and W = E + r (k - q).  Checks the identity exactly (Fractions) on random S and on given families; reports who pays Lam.
Usage: python rays.py rnd NS SEED | list m g1 g2 ... c"""
import sys, random
from fractions import Fraction as Fr
def analyse(m, G, c):
    n = len(G); T = c + m
    S = bytearray(T); S[0] = 1
    for x in range(1, T):
        if (x >= m and S[x - m]) or any(g <= x and S[x - g] for g in G): S[x] = 1
    if S[c - 1]: return None
    # canonical lex-least factorization of each Apery element of <m,G> below c+m
    fac = {0: (0,) * n}
    for x in range(1, T):
        if not S[x] or (x >= m and S[x - m]): continue
        best = None
        for i, g in enumerate(G):
            if g <= x and (x - g) in fac:
                a = list(fac[x - g]); a[i] += 1; a = tuple(a)
                if best is None or a[::-1] < best[::-1]: best = a
        if best is None: return None
        fac[x] = best
    M = {a: x for x, a in fac.items()}
    # down-set check
    for a in M:
        for i in range(n):
            if a[i] > 0:
                b = list(a); b[i] -= 1
                if tuple(b) not in M: return 'notdown'
    q = -(-c // m); rho = q * m - c; ell = n + 1; d = len(M); r = m - d
    k = sum(-(-(c - x) // m) for x in M.values() if x < c)
    E = ell * k - q * d + rho; W = (ell + r) * k - c
    Gn = ell * sum(Fr(-(-(c - x) // m)) - Fr(c - x, m) for x in M.values() if x < c)
    Pt = Fr(0); Lam = Fr(0)
    for a, x in M.items():
        for i in range(n):
            e = list(a)
            while True:
                e[i] += 1
                if tuple(e) not in M: e[i] -= 1; break
            xe = M[tuple(e)]
            if xe < c: Pt += Fr(c - xe, m)
        if c <= x < T: Lam += Fr((sum(a) - 1) * (x - c), m)
    assert E == Fr(rho * r, m) + Gn + Pt - Lam, (m, G, c)
    # universal difference bodies: M_j = {beta : beta + Delta_j in M}, Delta_j in M; |M_j - Delta_j| <= m
    def simplex(j):
        out = [(0,) * n]
        for _ in range(j):
            out = list({tuple(a[t] + (t == i) for t in range(n)) for a in out for i in range(n)} | set(out))
        return out
    rj = []
    for j in range(1, 6):
        Dj = simplex(j)
        if any(a not in M for a in Dj): break
        Mj = [b for b in M if all(tuple(x + y for x, y in zip(b, a)) in M for a in Dj)]
        Z = {tuple(x - y for x, y in zip(b, a)) for b in Mj for a in Dj}
        assert len(Z) <= m, (m, G, c, j)
        rj.append(len(Z) - d)
    rdb = max([0] + rj)
    # P~ = 0 regime: r >= R = sum_{top y} (|supp y| - 1)  (one-step DB + ray-exit bijection)
    Y = [a for a, x in M.items() if c <= x < T]
    R = sum(sum(1 for t in a if t) - 1 for a in Y)
    if Pt == 0 and n >= 2 and c > 4 * m:
        # Theorem P0-WILF, each step asserted
        K = [a for a, x in M.items() if x < c]
        Ksupp = sum(sum(1 for t in a if t) for a in K)
        D = max(sum(a) for a in Y)
        assert R >= 1
        assert (n - 1) * Ksupp <= D * R                          # step 5
        assert (k - q) - 1 >= Fr(D, n - 1)                        # step 6
        assert R * (k - q) >= sum(sum(a) - 1 for a in Y)          # crude P0 inequality
        assert W >= R * (k - q) - Lam >= 0
    if Pt == 0:
        assert r >= R, (m, G, c, r, R)
        # identities of the P~ = 0 regime
        K = [a for a, x in M.items() if x < c]
        assert sum(sum(a) - 1 for a in Y) == sum(sum(1 for t in a if t) for a in K) + R
    # general one-step DB: M_1 = interior, dM = M \ M_1, r >= R_gen = sum_{z in dM} (deg^-_{M_1}(z) - 1)
    M1 = {a for a in M if all(tuple(a[t] + (t == i) for t in range(n)) in M for i in range(n))}
    Rgen = 0
    for a in M:
        if a in M1: continue
        dg = sum(1 for i in range(n) if a[i] >= 1 and tuple(a[t] - (t == i) for t in range(n)) in M1)
        Rgen += dg - 1
    assert r >= Rgen, (m, G, c, r, Rgen)
    Rg = max(Rgen, 1 if r >= 1 else 0)
    certG = Fr(rho * Rg, m) + Gn + Pt - Lam + Rg * (k - q)
    RR = max(R, 1) if (Pt == 0 and n >= 2) else 0
    crude = None
    if Pt == 0:
        Ksupp = sum(sum(1 for t in a if t) for a, x in M.items() if x < c)
        crude = RR * (k - q) - (Ksupp + R)      # crude P0 inequality: sum_Y(|y|-1) <= R'(k-q)
    certR = Fr(rho * RR, m) + Gn + Pt - Lam + RR * (k - q)
    cert = Fr(rho * rdb, m) + Gn + Pt - Lam + rdb * (k - q)
    return dict(E=E, W=W, r=r, kq=k - q, G=Gn, P=Pt, L=Lam, rho=rho, m=m, n=n, d=d, rj=rj, rdb=rdb, cert=cert, R=R, certR=certR, crude=crude, Rgen=Rgen, certG=certG)
if __name__ == '__main__':
    if sys.argv[1] == 'list':
        v = list(map(int, sys.argv[2:])); res = analyse(v[0], v[1:-1], v[-1])
        print({k_: (float(x) if isinstance(x, Fr) else x) for k_, x in res.items()})
    else:
        NS, SEED = int(sys.argv[2]), int(sys.argv[3]); random.seed(SEED); cnt = 0; nd = 0
        while cnt < NS:
            n = random.randint(1, 5); m = random.randint(5, 60); c = random.randint(m + 1, 9 * m)
            G = sorted(random.sample(range(m + 1, c), min(n, c - m - 1)))
            if any(g % m == 0 for g in G): continue
            res = analyse(m, G, c)
            if res is None: continue
            if res == 'notdown': nd += 1; continue
            cnt += 1
        print("identity verified on %d random S (non-down-set canonical sets: %d)" % (cnt, nd))
