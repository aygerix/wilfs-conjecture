"""Census of PC failures (S < Lam_r) on random semigroup tiles (grlex), every phase.  Reports failure rate by d and
height, the worst (S - Lam_r)/m, and whether failing tiles are WRAP-MAX (they should never be, by H1').
usage: python pc_census.py seed trials mmin mmax dmin dmax"""
import sys, random
from pmin_tile import apery, minimal_gens, tile
seed, T, mmin, mmax, dmin, dmax = map(int, sys.argv[1:7]); rng = random.Random(seed)
stat = {}; ex = []
for tr in range(T):
    m = rng.randint(mmin, mmax); kk = rng.randint(dmin, dmax); mode = rng.random()
    if mode < 0.5: gens = [m+rng.randint(1, m-1) for _ in range(kk)]
    else: gens = [rng.randint(m+1, 3*m) for _ in range(kk)]
    if None in apery(m, gens): continue
    n, ap = minimal_gens(m, gens)
    if len(n) < 2: continue
    d = len(n); P = [g % m for g in n]
    D = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values()); Ds = set(D)
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
    v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    Tw = {x: sum(x[b]+1 for b in range(d) if up(x, b) not in Ds) for x in D}
    H = max(map(sum, D)); key = (d, min(H, 6))
    wm = all(v[x] < m for x in D if x not in A)
    nwrapN = sum(v[x]//m for x in D if x not in A)
    worst = None
    for r0 in range(m):
        r = {x: (v[x]+r0) % m for x in D}
        S = (d+1)*m*(m-1)//2-sum((d+sum(y))*r[y] for y in A)
        Lam = sum(Tw[t]*r[t] for t in D if t not in A)
        q = (S-Lam)/m
        if worst is None or q < worst[0]: worst = (q, r0, S, Lam)
    st = stat.setdefault(key, [0, 0, 0])
    st[0] += 1
    if worst[0] < 0:
        st[1] += 1; st[2] += wm
        if len(ex) < 6: ex.append((m, n, worst, "wrapmax" if wm else "nonmax-wrap-mass %d" % nwrapN))
for key in sorted(stat): print("d=%d height%s%d tiles=%d PC_fail=%d (wrapmax among them %d)" % (key[0], '>=' if key[1] == 6 else '=', key[1], *stat[key]))
for e in ex: print("EX", e)
