"""Deep-slack identity (lead, 2026-10-19).  For a numerical semigroup S with factorization tile D (grlex), Wilf phase
r(x) = (w(x) - c) mod m, MaxCL slack S_W = (d+1)m(m-1)/2 - sum_A (d+|y|) r(y), Lam_r = sum_{nonmax tops} |C| r(t),
G(x) = #left elements in the class of w(x) = ceil((c - w(x))/m)_+.  Claim (exact):
    S_W/m = e*ell - c + Lam_r/m - sum_x T(x) G(x),     T(x) = sum_{b: x b-top} (x_b + 1).
Also reports Wilf margin vs MaxCL margin and the class split A = Top (every maximal cell has w >= c) vs A != Top.
usage: python ds_ident.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '../nowrap')
from fractions import Fraction
from pmin_tile import apery, minimal_gens, tile
seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
ok = 0; topall = 0; tot = 0; worst_top = None; worst_deep = None
for tr in range(T):
    m = rng.randint(mmin, mmax); kk = rng.randint(2, 7)
    gens = [rng.randint(m+1, rng.choice([2, 3, 4])*m) for _ in range(kk)]
    if None in apery(m, gens): continue
    n, ap = minimal_gens(m, gens)
    if len(n) < 2: continue
    d = len(n); e = d+1
    D = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values()); Ds = set(D)
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
    w = {x: sum(x[i]*n[i] for i in range(d)) for x in D}
    c = max(w.values())-m+1; g = sum((w[x]-(w[x] % m))//m for x in D); ell = c-g
    Tw = {x: sum(x[b]+1 for b in range(d) if up(x, b) not in Ds) for x in D}
    r = {x: (w[x]-c) % m for x in D}
    G = {x: max(0, -((w[x]-c)//m)) for x in D}
    SW = (d+1)*m*(m-1)//2-sum((d+sum(y))*r[y] for y in A)
    Lam = sum(Tw[t]*r[t] for t in D if t not in A)   # Tw[t] = total length of columns topped by t
    lhs = Fraction(SW, m); rhs = e*ell-c+Fraction(Lam, m)-sum(Tw[x]*G[x] for x in D)
    assert lhs == rhs, (m, n, lhs, rhs)
    ok += 1; tot += 1
    isTop = all(w[y] >= c for y in A); topall += isTop
    W = e*ell-c; norm = SW/((d+1)*m*(m-1)/2)
    rec = (round(norm, 4), W, m, n)
    if isTop:
        if worst_top is None or rec < worst_top: worst_top = rec
    else:
        if worst_deep is None or rec < worst_deep: worst_deep = rec
print("identity checked on", ok, "semigroups; A = Top (no deep maximal cell):", topall)
print("min normalized MaxCL slack at Wilf phase, A = Top:", worst_top)
print("min normalized MaxCL slack at Wilf phase, A != Top:", worst_deep)
