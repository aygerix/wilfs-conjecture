"""Does H1' (degree/exit form) need the tile property?  Random partial structures: a down-set D = D0 + V in N^d,
v = x.P, v < m and pairwise distinct on D0; V = some maximal cells with v in [m, 2m), labels v - m distinct and disjoint
from v(D0).  Optionally require completeness (|D| = m).  Degree form of H1' for every theta:
  sum_{x in D0, v>=theta} (up(x) - supp(x)) <= sum_V (|supp y| - 1) + sum_{y in V, lambda>=theta} |y|.
usage: python wm_partial.py seed trials mmax dmax fill"""
import sys, random
seed, T, mmax, dmax, fill = map(int, sys.argv[1:6]); rng = random.Random(seed)
fails = 0; tested = 0; ex = None
for tr in range(T):
    m = rng.randint(6, mmax); d = rng.randint(2, dmax); P = [rng.randint(1, m-1) for _ in range(d)]
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    dn = lambda x, a: tuple(x[i]-(i == a) for i in range(d))
    D = {tuple([0]*d)}; used = {0}; V = set()
    target = rng.randint(2, m) if not fill else m
    for it in range(40*m):
        if len(D) >= target: break
        cand = set()
        for x in D:
            if x in V: continue
            for a in range(d):
                y = up(x, a)
                if y not in D and all(dn(y, b) in D and dn(y, b) not in V for b in range(d) if y[b] > 0): cand.add(y)
        cand = list(cand)
        if not cand: break
        y = rng.choice(cand); vy = sum(y[i]*P[i] for i in range(d))
        if vy >= 2*m or vy % m in used: continue
        if vy >= m and rng.random() < 0.5: continue
        D.add(y); used.add(vy % m)
        if vy >= m: V.add(y)
    if not V or (fill and len(D) < m): continue
    Ds = D; D0 = [x for x in D if x not in V]; vv = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    upc = {x: sum(1 for a in range(d) if up(x, a) in Ds) for x in D0}; sp = {x: sum(1 for t in x if t) for x in D}
    base = sum(sp[y]-1 for y in V); tested += 1
    for th in range(0, m+1):
        lhs = sum(upc[x]-sp[x] for x in D0 if vv[x] >= th)
        rhs = base+sum(sum(y) for y in V if vv[y]-m >= th)
        if lhs > rhs:
            fails += 1
            if ex is None: ex = (m, P, sorted(D), sorted(V), th, lhs, rhs)
            break
print("tested", tested, "failures", fails); print("first:", ex)
