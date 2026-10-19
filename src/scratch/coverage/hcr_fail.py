"""Where does HCR fail?  Random semigroups with generators in (m, (1+f)m) (shallow tiles), many e.  For each HCR failure
(on both the grlex and P-min tiles), report e, m, height, cubic count, and which proved/conjectured MaxCL class covers it.
usage: python hcr_fail.py seed trials mmin mmax emin emax fmax"""
import sys, random, collections
from pmin_tile import apery, minimal_gens, tile
seed, T, mmin, mmax, emin, emax = map(int, sys.argv[1:7]); fmax = float(sys.argv[7]); rng = random.Random(seed)
tot = 0; fails = []
for tr in range(T):
    m = rng.randint(mmin, mmax); kk = rng.randint(emin-1, emax-1); f = rng.uniform(0.05, fmax)
    gens = [rng.randint(m+1, int(m*(1+f))+1) for _ in range(kk)]
    ap = apery(m, gens)
    if None in ap: continue
    n, ap = minimal_gens(m, gens); d = len(n); e = d+1
    if e < emin or d < 2: continue
    tot += 1; P = [g % m for g in n]
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    def hcr(D):
        Ds = set(D); A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
        ht = {}
        for x in sorted(D, key=lambda x: -sum(x)):
            ht[x] = max([ht[up(x, a)]+1 for a in range(d) if up(x, a) in Ds], default=0)
        num = 0
        for x in D:
            for a in range(d):
                t = x
                while up(t, a) in Ds: t = up(t, a)
                if t not in A: num += (m+1)*ht[t]
        Tw = sorted((d+sum(y) for y in A), reverse=True)
        num += sum(i*w for i, w in enumerate(Tw))
        return num/((d-1)*m*(m-1)/2)
    Dg = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values())
    Dp = list(tile(m, n, ap, lambda x: (sum(x[i]*P[i] for i in range(d)), sum(x), tuple(-t for t in x))).values())
    h = max(hcr(Dg), hcr(Dp))
    if h < 1:
        Ds = set(Dg); A = set(y for y in Dg if all(up(y, a) not in Ds for a in range(d)))
        v = {x: sum(x[i]*P[i] for i in range(d)) for x in Dg}
        H = max(map(sum, Dg)); cub = sum(1 for x in Dg if sum(x) == 3)
        wm = all(v[x] < m for x in Dg if x not in A); E = sum(v[x]//m for x in Dg)
        cls = 'H2' if H <= 2 else ('ONEC' if H == 3 and cub <= 1 else ('NOWRAP' if E == 0 else ('WMAX' if wm else 'NONE')))
        fails.append((e, m, H, cub, round(h, 3), cls))
print("semigroups", tot, "HCR failures", len(fails))
print("by class:", collections.Counter(z[5] for z in fails))
print("by height:", sorted(collections.Counter(z[2] for z in fails).items()))
print("uncovered sample (e, m, height, cubics, HCR):", [z for z in fails if z[5] == 'NONE'][:12])
