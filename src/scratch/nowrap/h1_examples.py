"""Print tight WRAP-MAX examples (beta = |F| >= 1, prefer |F| >= 2) with full data (lead, 2026-10-19)."""
import sys, random
from pmin_tile import apery, minimal_gens, tile
seed, T, mmin, mmax, want = map(int, sys.argv[1:6]); rng = random.Random(seed); shown = 0
for tr in range(T):
    m = rng.randint(mmin, mmax); kk = rng.randint(2, 6)
    gens = [rng.randint(m+1, rng.choice([2, 3])*m) for _ in range(kk)]
    if None in apery(m, gens): continue
    n, ap = minimal_gens(m, gens)
    if len(n) < 2: continue
    d = len(n); P = [g % m for g in n]
    D = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values()); Ds = set(D)
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
    v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    if any(v[x] >= m for x in D if x not in A): continue
    def top(x, b):
        y = x
        while up(y, b) in Ds: y = up(y, b)
        return y
    for sg in range(m):
        r0 = (-sg) % m; c = {x: int(v[x] % m >= m-r0) for x in D}
        F = [y for y in A if v[y]//m == 1 and c[y] == 0 and all(c[tuple(y[j]-(j == b)*i for j in range(d))] for b in range(d) for i in range(1, y[b]+1))]
        pairs = [(x, b) for x in D for b in range(d) if c[x] == 0 and top(x, b) != x and c[top(x, b)] == 1]
        if len(F) >= want and len(pairs) == len(F):
            print("m", m, "n", n, "P", P, "rho0", r0, "window labels [%d,%d)" % (m-r0, m))
            for x in sorted(D, key=lambda x: v[x]): print("   ", x, "v", v[x], "lab", v[x] % m, "MAX" if x in A else "", "WIN" if c[x] else "", "F" if x in F else "")
            print("  beta pairs (x, b, top):", [(x, b, top(x, b)) for (x, b) in pairs]); shown += 1
            break
    if shown >= 3: break
