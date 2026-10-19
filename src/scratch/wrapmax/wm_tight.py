"""Print H1'-tight (slack 0, |V_theta| >= 2) WRAP-MAX instances from random semigroup tiles, with the cells in label order.
usage: python wm_tight.py seed trials mmin mmax dmin dmax want"""
import sys, random
sys.path.insert(0, '../nowrap')
from pmin_tile import apery, minimal_gens, tile
from wm_suff import check
seed, T, mmin, mmax, dmin, dmax, want = map(int, sys.argv[1:8]); rng = random.Random(seed); shown = 0
for tr in range(T):
    m = rng.randint(mmin, mmax); kk = rng.randint(dmin, dmax)
    gens = [m+rng.randint(1, m-1) for _ in range(kk)]
    if None in apery(m, gens): continue
    n, ap = minimal_gens(m, gens)
    if len(n) < 2: continue
    d = len(n); P = [g % m for g in n]
    D = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values()); Ds = set(D)
    res = check(m, P, D)
    if res is None: continue
    hit = [t for t in res if t[0] == 0 and t[4] >= want]
    if not hit: continue
    th = hit[0][3]; v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
    print("m", m, "n", n, "P", P, "theta", th, "|V_th|", hit[0][4])
    for x in sorted(D, key=lambda x: v[x] % m):
        tag = ("V" if v[x] >= m else ("MAX" if x in A else ""))
        print("   lab %2d v %2d %s %s%s" % (v[x] % m, v[x], x, tag, "  <theta" if v[x] % m < th else ""))
    shown += 1
    if shown >= 2: break
