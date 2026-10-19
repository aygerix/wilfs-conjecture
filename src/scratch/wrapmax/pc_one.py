"""PC (S >= Lam_r) on one semigroup, grlex tile, every phase.  usage: python pc_one.py m g1 g2 ..."""
import sys
sys.path.insert(0, '../nowrap')
from pmin_tile import apery, minimal_gens, tile
m = int(sys.argv[1]); n, ap = minimal_gens(m, list(map(int, sys.argv[2:]))); d = len(n); P = [g % m for g in n]
D = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values()); Ds = set(D)
up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
cols = []
for b in range(d):
    for t in D:
        if up(t, b) in Ds: continue
        col = [t]; y = list(t)
        while y[b] > 0: y[b] -= 1; col.append(tuple(y))
        cols.append((t, col))
for r0 in range(m):
    r = {x: (v[x]+r0) % m for x in D}
    S = (d+1)*m*(m-1)//2-sum((d+sum(y))*r[y] for y in A)
    Lam = sum(len(col)*r[t] for (t, col) in cols if t not in A)
    print("rho0", r0, "S", S, "Lam", Lam, "S-Lam", S-Lam, "FAIL" if S < Lam else "")
