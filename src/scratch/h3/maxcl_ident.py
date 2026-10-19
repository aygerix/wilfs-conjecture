"""Exact check of the column-top reformulation of MaxCL (lead, 2026-10-19), on Apery tiles of any height.
With delta_a = (rho_a - rho_0) mod m >= 0, l(x) = rho_0 + x.delta, K = floor(l/m), U_j = {l >= j m}:
  (I1) Phi_a = sum_A (d+|y|) y_a - (d+1) sum_D x_a <= 0;
  (I2) slack := (d+1) sum_D r - sum_A (d+|y|) r = m*Gamma - Lambda,  Lambda = -rho_0 (m+Dep) + sum_a delta_a Phi_a;
  (I3) Gamma = sum_j gamma(U_j), gamma(U) = sum_b (sh_b(U) - nm_b(U)) - |U|.
usage: python maxcl_ident.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile, in_semigroup
if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed); n = 0; bad = 0
    for t in range(T):
        m = rng.randint(mmin, mmax); d = rng.randint(2, 6)
        gens = sorted(set(rng.randint(m+1, 3*m) for _ in range(d)))
        gens = [x for x in gens if x % m]
        if len(gens) < 2 or len(set(x % m for x in gens)) < len(gens): continue
        if any(in_semigroup(gens[a], m, gens[:a]+gens[a+1:]) for a in range(len(gens))): continue
        best = apery_tile(m, gens)
        if len(best) != m: continue
        d = len(gens); D = {x: w for (w, x) in best.values()}
        if any(tuple(1 if i == a else 0 for i in range(d)) not in D for a in range(d)): continue
        def add(x, a): return tuple(x[i]+(i == a) for i in range(d))
        A = set(y for y in D if all(add(y, a) not in D for a in range(d)))
        # column tops: top of b-column through x
        def top(x, b):
            y = x
            while add(y, b) in D: y = add(y, b)
            return y
        X = [sum(x[a] for x in D) for a in range(d)]
        Phi = [sum((d+sum(y))*y[a] for y in A)-(d+1)*X[a] for a in range(d)]
        Dep = d*m-sum(d+sum(y) for y in A)
        for sig in rng.sample(range(m), min(m, 4)):
            r = {x: (w-sig) % m for x, w in D.items()}
            z = (0,)*d; r0 = r[z]; delta = [(r[tuple(1 if i == a else 0 for i in range(d))]-r0) % m for a in range(d)]
            l = {x: r0+sum(x[a]*delta[a] for a in range(d)) for x in D}
            assert all((l[x]-r[x]) % m == 0 for x in D)
            K = {x: l[x]//m for x in D}
            slack = (d+1)*sum(r.values())-sum((d+sum(y))*r[y] for y in A)
            Lam = -r0*(m+Dep)+sum(delta[a]*Phi[a] for a in range(d))
            Gam = sum((d+sum(y))*K[y] for y in A)-(d+1)*sum(K.values())
            G2 = 0
            for j in range(1, max(K.values())+1):
                U = set(x for x in D if K[x] >= j)
                g = -len(U)
                for b in range(d):
                    for x in D:
                        tb = top(x, b)
                        if x not in U and tb in U and tb in A: g += 1
                        if x in U and tb not in A: g -= 1
                G2 += g
            ok = (max(Phi) <= 0) and (slack == m*Gam-Lam) and (Gam == G2)
            n += 1
            if not ok:
                bad += 1
                if bad <= 5: print("MISMATCH", m, gens, sig, max(Phi), slack, m*Gam-Lam, Gam, G2)
    print("checked (tile,sigma) pairs", n, "mismatches", bad)
