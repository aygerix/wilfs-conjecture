"""Problem 1.8 class (all minimal generators < 2m): how small can e*ell/c get, by e?  Random + hill-climbing over
A* = {P_a} subset [1, m-1] (generators m + P_a), restricted to depth >= 4 (c > 3m).  Exact integer Apery sets.
usage: python p18_margin.py seed restarts steps mmin mmax emin emax"""
import sys, random, math
sys.path.insert(0, sys.argv[8] if len(sys.argv) > 8 else '../nowrap')
from pmin_tile import apery
seed, R, steps, mmin, mmax, emin, emax = map(int, sys.argv[1:8]); rng = random.Random(seed)
best = {}
def ratio(m, P):
    if math.gcd(m, *P) != 1 or len(set(P)) != len(P): return None
    ap = apery(m, [m+p for p in P]); c = max(ap)-m+1
    if c <= 3*m: return None
    g = sum(w//m for w in ap); ell = c-g; e = len(P)+1
    return e*ell/c, c
for rs in range(R):
    m = rng.randint(mmin, mmax); e = rng.randint(emin, emax); k = e-1
    if k >= m-1: continue
    mode = rng.random()
    if mode < 0.3: P = sorted(rng.sample(range(1, m), k))
    elif mode < 0.6:
        span = min(m-1, max(k, int(math.sqrt(m))+rng.randint(0, 5))); P = sorted(rng.sample(range(1, span+1), k))
    else:
        a = rng.randint(1, max(1, m//(2*k))); b = rng.randint(1, m-1); P = sorted(set((b+i*a) % m or 1 for i in range(k)))
        if len(P) != k: continue
    cur = ratio(m, P)
    if cur is None: continue
    for st in range(steps):
        Q = list(P); i = rng.randrange(k); Q[i] = rng.randint(1, m-1)
        if rng.random() < 0.5: Q[i] = max(1, min(m-1, P[i]+rng.randint(-3, 3)))
        Q = sorted(Q); r = ratio(m, Q)
        if r is None: continue
        if r[0] <= cur[0]: P, cur = Q, r
    if e not in best or cur[0] < best[e][0]: best[e] = (round(cur[0], 4), m, [m+p for p in P], cur[1], round(cur[1]/m, 2))
for e in sorted(best): print("e=%d min e*ell/c = %s" % (e, best[e]), flush=True)
