"""WRAP-MAX payment anatomy (lead, 2026-10-19).  WRAP-MAX: canonical lift v = x.P (P_a = n_a mod m) has v < m on every
non-maximal cell.  Phase rho0 = r(0); window W = {r < rho0} (|W| = rho0); U1 = {y in A : v(y) >= m}.
Exact (asserted):  S/m = Lam_r/m + beta_N + sum_A tau(y),
  Lam_r = sum_{nonmax-top cols} |C| r(t);  beta_N = #{(x,b): x not in W, b-top of x is a nonmax cell of W};
  tau(y) = (|y|-1) K(y) + c_y - nb(y),  K = floor((rho0+v)/m), c = [y in W], nb = #column-below cells of y in W.
tau = -1 exactly on F = {y in U1 \\ W : all column-below cells in W}.  Reports the budget split on (tile, phase) with F != {}.
usage: python wm_pay.py seed trials mmin mmax dmin dmax"""
import sys, random
sys.path.insert(0, '../nowrap')
from pmin_tile import apery, minimal_gens, tile

def instances(m, n, D):
    d = len(n); P = [g % m for g in n]; Ds = set(D)
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
    v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    if any(v[x] >= m for x in D if x not in A): return None
    cols = []
    for b in range(d):
        for t in D:
            if up(t, b) in Ds: continue
            col = [t]; y = list(t)
            while y[b] > 0: y[b] -= 1; col.append(tuple(y))
            cols.append((b, t, col))
    res = []
    for r0 in range(1, m):
        r = {x: (v[x]+r0) % m for x in D}; W = set(x for x in D if r[x] < r0); K = {x: (v[x]+r0)//m for x in D}
        S = (d+1)*m*(m-1)//2-sum((d+sum(y))*r[y] for y in A)
        Lam = sum(len(col)*r[t] for (b, t, col) in cols if t not in A)
        beta = sum(1 for (b, t, col) in cols if t not in A and t in W for x in col if x not in W)
        nb = {y: 0 for y in A}
        for (b, t, col) in cols:
            if t in A: nb[t] += sum(1 for x in col[1:] if x in W)
        tau = {y: (sum(y)-1)*K[y]+(y in W)-nb[y] for y in A}
        assert S*1 == Lam+m*(beta+sum(tau.values())), (m, n, r0)
        F = [y for y in A if tau[y] < 0]
        assert all(tau[y] == -1 and v[y] >= m and y not in W and nb[y] == sum(y) for y in F)
        if F:
            AW = sum(1 for y in A if y in W)
            res.append(dict(m=m, n=n, P=P, d=d, r0=r0, S=S, F=F, beta=beta, Lam=Lam, tauplus=sum(t for t in tau.values() if t > 0),
                            AW=AW, nW=r0-AW, supp=[sum(1 for t in y if t) for y in F], rF=[r[y] for y in F], H=max(sum(x) for x in D)))
    return res

if __name__ == '__main__':
    seed, T, mmin, mmax, dmin, dmax = map(int, sys.argv[1:7]); rng = random.Random(seed)
    tot = 0; tiles = 0; nolam = 0; worst = None; bysupp = {}
    for tr in range(T):
        m = rng.randint(mmin, mmax); kk = rng.randint(dmin, dmax)
        mode = rng.random()
        if mode < 0.4: gens = [m+rng.randint(1, m-1) for _ in range(kk)]
        elif mode < 0.7: gens = [m+rng.randint(1, max(2, m//2)) for _ in range(kk)]
        else: gens = [rng.randint(m+1, 3*m) for _ in range(kk)]
        if None in apery(m, gens): continue
        n, ap = minimal_gens(m, gens)
        if len(n) < 2: continue
        d = len(n); P = [g % m for g in n]
        for key in (lambda x: (sum(x), tuple(-t for t in x)), lambda x: (sum(x[i]*P[i] for i in range(d)), sum(x), tuple(-t for t in x))):
            D = list(tile(m, n, ap, key).values())
            res = instances(m, n, D)
            if res is None: continue
            tiles += 1
            for R in res:
                tot += 1
                need = len(R['F'])-R['beta']-R['tauplus']
                for s in R['supp']: bysupp[s] = bysupp.get(s, 0)+1
                if need > 0:
                    nolam += 1
                    q = (R['S']/R['m'])/len(R['F'])
                    if worst is None or q < worst[0]: worst = (q, R)
    print("WRAP-MAX tiles", tiles, "(tile,phase) with F", tot, "F-cells by support", dict(sorted(bysupp.items())))
    print("instances needing Lam_r (|F| > beta_N + tau+; A_W is inside tau):", nolam)
    if worst: print("min (S/m)/|F| among those:", round(worst[0], 3), worst[1])
