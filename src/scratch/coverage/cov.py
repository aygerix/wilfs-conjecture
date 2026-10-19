"""Coverage census (lead, 2026-10-19): which random numerical semigroups are covered by the Wilf classes proved so far
(or by H1', marked CONJ), and what the residual looks like.
Classes (each needs SOME factorization tile, or is intrinsic):
  LIT  : c <= 3m (Eliahou), 3e >= m (Eliahou), m <= 18 (BGOW)          [cited]
  OWN  : c <= 4m and e <= 19 (GW-26g); at most e-1 PF numbers >= 3m (GW-20)   [paper]
  H2   : grlex tile height <= 2 (Lean)        NOWRAP: P-min tile E = 0 (Lean)
  ONEC : grlex tile height <= 3 with <= 1 cubic (paper)
  WMAX : P-min or grlex tile WRAP-MAX (CONJ H1')
usage: python cov.py seed trials mmin mmax emin emax span"""
import sys, random
from pmin_tile import apery, minimal_gens, tile
seed, T, mmin, mmax, emin, emax, span = map(int, sys.argv[1:8]); rng = random.Random(seed)
cnt = {}; tot = 0; resid = []; nohcr = []
for tr in range(T):
    m = rng.randint(mmin, mmax); kk = rng.randint(emin-1, emax-1)
    gens = [rng.randint(m+1, span*m) for _ in range(kk)]
    ap = apery(m, gens)
    if None in ap: continue
    n, ap = minimal_gens(m, gens); d = len(n); e = d+1
    if e < emin or e > emax: continue
    tot += 1
    c = max(ap)-m+1; P = [g % m for g in n]
    inS = lambda z: z >= 0 and z >= ap[z % m]
    PF = [w-m for w in ap if w > 0 and all(not inS(w-m+g) or (w+g) in [] for g in []) ]  # placeholder
    # pseudo-Frobenius: w - m with w in Ap maximal w.r.t. <=_S on Ap
    apset = set(ap)
    PF = [w-m for w in ap if w != 0 and not any((w+g) in apset for g in n)] if True else []
    PF = [f for f in PF if f > 0] + ([c-1] if c-1 not in PF and c > 0 else [])
    lit = c <= 3*m or 3*e >= m or m <= 18
    own = (c <= 4*m and e <= 19) or sum(1 for f in PF if f >= 3*m) <= e-1
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    def info(D):
        Ds = set(D); A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
        v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
        H = max(map(sum, D)); E = sum(v[x]//m for x in D)
        wm = all(v[x] < m for x in D if x not in A); cub = sum(1 for x in D if sum(x) == 3)
        return H, E, wm, cub
    Dg = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values())
    Dp = list(tile(m, n, ap, lambda x: (sum(x[i]*P[i] for i in range(d)), sum(x), tuple(-t for t in x))).values())
    Hg, Eg, wmg, cubg = info(Dg); Hp, Ep, wmp, cubp = info(Dp)
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
        return num/((d-1)*m*(m-1)/2) if d > 1 else 9
    hc = max(hcr(Dg), hcr(Dp)) >= 1
    h2 = Hg <= 2; nowrap = Ep == 0; onec = Hg <= 3 and cubg <= 1; wmax = wmg or wmp
    proved = lit or own or h2 or nowrap or onec or hc
    key = ('LIT' if lit else '')+(' OWN' if own else '')+(' H2' if h2 else '')+(' NOWRAP' if nowrap else '')+(' ONEC' if onec else '')
    for name, val in (('LIT', lit), ('OWN', own), ('H2', h2), ('NOWRAP', nowrap), ('ONEC', onec), ('HCR', hc), ('WMAX(conj)', wmax), ('any proved', proved), ('proved or WMAX', proved or wmax)):
        cnt[name] = cnt.get(name, 0)+val
    if not (proved or wmax): resid.append((e, m, round(c/m, 2), Hg, Eg, cubg))
    if not hc: nohcr.append((e, m, round(c/m, 2), Hg, round(max(hcr(Dg), hcr(Dp)), 3), lit or own or h2 or nowrap or onec or wmax))
print("semigroups:", tot)
for k in cnt: print("  %-16s %6d  (%.1f%%)" % (k, cnt[k], 100*cnt[k]/tot))
import collections
print("residual by e:", sorted(collections.Counter(r[0] for r in resid).items()))
print("residual by grlex height:", sorted(collections.Counter(min(r[3], 8) for r in resid).items()))
print("residual c/m range:", min((r[2] for r in resid), default=None), max((r[2] for r in resid), default=None))
print("HCR failures:", len(nohcr), "of which covered by another class:", sum(1 for z in nohcr if z[5]), "sample:", nohcr[:10])
print("sample residual (e, m, c/m, height, E, cubics):", resid[:8])
