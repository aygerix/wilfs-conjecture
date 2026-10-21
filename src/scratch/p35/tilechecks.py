r"""MaxCL, Tile-CL and DEP slacks of the lex tile of S at every phase (lead, 2026-10-20).
MaxCL(sigma):  (d+1) M' - sum_{y in A} (d + |y|) r(y) >= 0,  r = <phi - sigma>, M' = m(m-1)/2.
Tile-CL(sigma): V = ((d+1) M' - sum_x om(x) r(x)) / m >= 0, om(x) = total length of the columns topped at x.
DEP(sigma): V + Dep >= 0 (DEP-ALL).  Conductor phase sigma = c mod m is the one Wilf needs.
Usage: python tilechecks.py m g1 g2 ..."""
import sys
sys.path.insert(0, '../p34')
from tile import build
G = list(map(int, sys.argv[1:])); m = min(G)
c, gens, M = build(m, G); D = list(M); d = len(gens); Ds = set(D)
up = lambda x, b: tuple(x[t] + (t == b) for t in range(d))
phi = {x: sum(a * b for a, b in zip(x, gens)) for x in D}
A = [x for x in D if all(up(x, b) not in Ds for b in range(d))]
om = {x: sum(x[b] + 1 for b in range(d) if up(x, b) not in Ds) for x in D}
dep = sum(om[x] for x in D if x not in set(A)); Mp = m * (m - 1) // 2
mc = []; tv = []
for s in range(m):
    r = {x: (phi[x] - s) % m for x in D}
    mc.append((d + 1) * Mp - sum((d + sum(y)) * r[y] for y in A))
    tv.append(((d + 1) * Mp - sum(om[x] * r[x] for x in D)) // m)
sc = c % m
print("d=%d m=%d c=%d |A|=%d Dep=%d height=%d" % (d, m, c, len(A), dep, max(sum(x) for x in D)))
print("MaxCL slack: min over phases %d (at conductor phase %d)" % (min(mc), mc[sc]))
print("Tile-CL V:   min over phases %d (at conductor phase %d); DEP min V+Dep = %d" % (min(tv), tv[sc], min(tv) + dep))
