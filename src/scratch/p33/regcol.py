"""h-regular semigroups WITH collisions: S = <m, Gamma>_c, h Gamma in [c, c+m) (Bacher Def 3.1), any n.
For each S (brute force): Apery elements w_i of <m,Gamma> (residues with w_i < c+m are the non-primitive ones),
their degrees t_i (well defined below c+m since c > (h-1)m), d_t = #{i : t_i = t}, d = sum d_t, r = m - d,
k = sum_{w_i < c} ceil((c - w_i)/m), W, E.  Checks:
  CENT: X = l*sum_t d_t (1 - t/h) - d >= 0 and the Abel form X = sum_t (u_t - u_{t-1}) T_t,
        u_t = 1 - d_t/N_t (N_t = C(n+t-1,t)) nondecreasing (normalized matching in the chain product)
  BND : W > rho r/m + (c/m) X - B + r (k - q),  B = (l/h) sum_{t<h} t d_t
  and reports how often BND alone certifies Wilf (BND >= -1).
Usage: python regcol.py NS SEED"""
import sys, random
from math import comb, ceil
from fractions import Fraction as Fr
NS, SEED = int(sys.argv[1]), int(sys.argv[2]); random.seed(SEED)
found = 0; tried = 0; bad = {'CENT': 0, 'MONO': 0, 'BND': 0, 'WILF': 0}; cert = 0; unc = []
byh = {}
while found < NS:
    tried += 1
    h = random.randint(2, 6); n = random.randint(1, 9); m = random.randint(4, 120)
    c = random.randint((h - 1) * m + 1, (h + 4) * m)
    lo, hi = max(-(-c // h), m + 1), (c + m - 1) // h
    if hi - lo + 1 < n: continue
    G = sorted(random.sample(range(lo, hi + 1), n))
    if any(g % m == 0 for g in G): continue   # not a minimal generator
    top = c + m
    T = [False] * top; T[0] = True; deg = [0] * top
    for x in range(1, top):
        best = None
        for g in [m] + G:
            if g <= x and T[x - g]:
                T[x] = True
                if g != m:
                    dd = deg[x - g] + 1
                    if best is None or dd < best: best = dd
        if T[x] and best is not None: deg[x] = best
    if T[c - 1]: continue
    found += 1
    q = -(-c // m); rho = q * m - c; ell = n + 1
    # Apery elements of <m,Gamma> below c+m
    w = {}
    for x in range(top):
        if T[x] and (x < m or not T[x - m]): w[x % m] = x
    d = len(w); r = m - d
    dt = [0] * (h + 1)
    for i, x in w.items():
        # degree: number of Gamma-summands (Apery => no m); all factorizations below c+m have the same degree
        t = deg[x] if x else 0
        assert t <= h
        dt[t] += 1
    k = sum(-(-(c - x) // m) for x in w.values() if x < c)
    W = (ell + r) * k - c; E = ell * k - q * d + rho
    assert W == E + r * (k - q)
    X = Fr(ell) * sum(dt[t] * (1 - Fr(t, h)) for t in range(h + 1)) - d
    N = [comb(n + t - 1, t) for t in range(h + 1)]
    u = [1 - Fr(dt[t], N[t]) for t in range(h + 1)]
    f = [1 - Fr((n + 1) * (h - t), h) for t in range(h + 1)]
    Tt = [sum(f[s] * N[s] for s in range(t, h + 1)) for t in range(h + 1)]
    Xab = sum((u[t] - (u[t - 1] if t else 0)) * Tt[t] for t in range(h + 1))
    if X < 0 or X != Xab: bad['CENT'] += 1
    if any(u[t] < u[t - 1] for t in range(1, h + 1)): bad['MONO'] += 1
    B = Fr(ell, h) * sum(t * dt[t] for t in range(h))
    bnd = Fr(rho * r, m) + Fr(c, m) * X - B + r * (k - q)
    if not W > bnd:
        bad['BND'] += 1; print('BNDFAIL', h, n, m, c, G, r, W, float(bnd))
    if W < 0: bad['WILF'] += 1
    key = h; st = byh.setdefault(key, [0, 0, 0])
    st[0] += 1
    if bnd >= -1: cert += 1; st[1] += 1
    else:
        st[2] += 1
        if len(unc) < 12: unc.append((h, n, m, c, G, r, float(X), float(B), float(bnd), W, dt))
print("tried %d, h-regular S %d; failures %s; certified by BND alone %d" % (tried, found, bad, cert))
for h in sorted(byh): print("  h=%d: %d S, certified %d, uncertified %d" % (h, *byh[h]))
for x in unc: print("  UNC h=%d n=%d m=%d c=%d G=%s r=%d X=%.2f B=%.2f bnd=%.2f W=%d dt=%s" % x)
