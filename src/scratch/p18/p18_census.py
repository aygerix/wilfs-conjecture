"""Problem 1.8 of Delgado-Kumar-Marion (arXiv 2501.04417v3): if every minimal generator is < 2m, does Wilf hold?
Census of the OPEN part (depth >= 4 and |S cap (m,2m)| = e-1 < sqrt(dm/(d-2)), d = depth = ceil(c/m)) against our
proved criteria. Generators n_a = m + P_a, P_a in [1, m-1] (all automatically minimal).  For fixed w, x.P = w - |x|m,
so the P-min tile is the LONGEST-factorization tile; NO-WRAP (E = 0 on it) <=> every Apery element has a factorization
of length exactly floor(w/m) (Kunz coordinate = max factorization length).
Criteria: LIT (c <= 3m, 3e >= m, m <= 18), DKM (Thm 1.5), H2/ONEC (grlex height), NOWRAP (Lean), HCR (shape),
MaxCL at the Wilf phase on either tile (computed; implies Wilf via Lean chain).
usage: python p18_census.py seed trials mmin mmax mode   (mode: rand | low | mixed)"""
import sys, random, math, collections
sys.path.insert(0, sys.argv[6] if len(sys.argv) > 6 else '../nowrap')
from pmin_tile import apery, tile

seed, T, mmin, mmax = map(int, sys.argv[1:5]); mode = sys.argv[5]; rng = random.Random(seed)
cnt = collections.Counter(); tot = 0; resid = []; worst = None
for tr in range(T):
    m = rng.randint(mmin, mmax)
    kmax = max(3, int(math.isqrt(2*m)))
    k = rng.randint(3, kmax)
    if mode == 'low' or (mode == 'mixed' and rng.random() < 0.5):
        span = rng.randint(k+1, max(k+2, int(rng.choice([1, 2, 4])*math.sqrt(m))+k))
        span = min(span, m-1)
        if span < k: continue
        P = sorted(rng.sample(range(1, span+1), k))
    else:
        P = sorted(rng.sample(range(1, m), k))
    if math.gcd(m, *P) != 1: continue
    n = [m+p for p in P]
    ap = apery(m, n); c = max(ap)-m+1
    if c <= 3*m: continue
    dep = -(-c//m); e = k+1
    if e-1 >= math.sqrt(dep*m/(dep-2)): continue          # DKM Thm 1.5 covers it
    tot += 1
    g = sum(w//m for w in ap); ell = c-g; W = e*ell-c
    assert W >= 0
    lit = 3*e >= m or m <= 18
    d = k
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    res = {}
    for name, key in (('grlex', lambda x: (sum(x), tuple(-t for t in x))), ('long', lambda x: (-sum(x), tuple(-t for t in x)))):
        tb = tile(m, n, ap, key); D = list(tb.values()); Ds = set(D)
        A = [y for y in D if all(up(y, a) not in Ds for a in range(d))]
        v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
        H = max(map(sum, D)); E = sum(v[x]//m for x in D)
        sig = c % m; M1 = m*(m-1)//2
        Sw = (d+1)*M1-sum((d+sum(y))*((v[y]-sig) % m) for y in A)
        ht = {}
        for x in sorted(D, key=lambda x: -sum(x)):
            ht[x] = max([ht[up(x, a)]+1 for a in range(d) if up(x, a) in Ds], default=0)
        num = 0
        for x in D:
            for a in range(d):
                t = x
                while up(t, a) in Ds: t = up(t, a)
                if t not in set(A): num += (m+1)*ht[t]
        Tw = sorted((d+sum(y) for y in A), reverse=True)
        num += sum(i*w for i, w in enumerate(Tw))
        hcr = num/((d-1)*M1)
        wm = all(v[x] < m for x in D if x not in set(A))
        res[name] = dict(H=H, E=E, Sw=Sw, hcr=hcr, wm=wm)
    h2 = res['grlex']['H'] <= 2
    nowrap = res['long']['E'] == 0
    hc = max(res['grlex']['hcr'], res['long']['hcr']) >= 1
    mx = res['grlex']['Sw'] >= 0 or res['long']['Sw'] >= 0
    proved = lit or h2 or nowrap or hc
    for nm, val in (('LIT', lit), ('H2', h2), ('NOWRAP', nowrap), ('HCR', hc), ('MaxCL@Wilf (computed)', mx),
                    ('WRAP-MAX', res['long']['wm'] or res['grlex']['wm']), ('proved (LIT/H2/NOWRAP/HCR)', proved)):
        cnt[nm] += val
    if not proved: resid.append((e, m, round(c/m, 2), res['grlex']['H'], res['long']['E'], round(max(res['grlex']['hcr'], res['long']['hcr']), 3)))
    r = W/c
    if worst is None or r < worst[0]: worst = (round(r, 4), m, n, c)
print("open-part semigroups (gens < 2m, c > 3m, outside DKM 1.5):", tot)
for k_ in cnt: print("  %-28s %6d (%.1f%%)" % (k_, cnt[k_], 100*cnt[k_]/max(tot, 1)))
print("by e:", sorted(collections.Counter(min(x, 12) for x in [0]).items()) if False else "")
print("residual (not proved):", len(resid), "sample (e, m, c/m, grlex H, E_long, max HCR):", resid[:10])
print("min Wilf ratio W/c:", worst)
