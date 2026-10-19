"""Anatomy of the unit form on the E47 tile <14,22,23,57,61,62,63> (lead, 2026-10-19): for each sigma print
rho_0, every carry K != 0 with its cell, the bracket Br_0, and the linear slack L_+ split by cell, and the MaxCL slack.
usage: python e47_anatomy.py [m gens...]"""
import sys
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile

m = int(sys.argv[1]) if len(sys.argv) > 1 else 14
gens = [int(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else [22, 23, 57, 61, 62, 63]
best = apery_tile(m, gens); d = len(gens)
D = {x: w for (w, x) in best.values()}
E = [tuple(1 if i == a else 0 for i in range(d)) for a in range(d)]
def add(x, a): return tuple(x[i]+(i == a) for i in range(d))
A = set(y for y in D if all(add(y, a) not in D for a in range(d)))
prs = [x for x in D if sum(x) == 2]; cub = [x for x in D if sum(x) == 3]
A2 = [x for x in prs if x in A]; N2 = [x for x in prs if x not in A]
psi = {z: sum(z[c]+1 for c in range(d) if add(z, c) in D) for z in N2}
deg = [sum(z[a] for z in prs) for a in range(d)]
print("m", m, "d", d, "cells", sorted(D.items(), key=lambda t: t[1]))
print("A2", A2, "N2", N2, "psi", psi, "deg", deg, "max units", [a for a in range(d) if E[a] in A])
for sig in range(m):
    r = {x: (w-sig) % m for x, w in D.items()}; r0 = r[(0,)*d]; ru = [r[E[a]] for a in range(d)]
    l = {x: (1-sum(x))*r0+sum(x[a]*ru[a] for a in range(d)) for x in D}
    K = {x: (l[x]-r[x])//m for x in D}
    Lu = {a: (d+1-deg[a])*ru[a] for a in range(d) if E[a] not in A}
    Lp = {z: (d+2-psi[z])*r[z] for z in N2}
    br = sum(K[z] for z in A2)+2*sum(K[y] for y in cub)-sum((psi[z]-1)*K[z] for z in N2)
    slack = (d+1)*sum(r[x] for x in D if x not in A)-sum((sum(y)-1)*r[y] for y in A)
    Lplus = sum(Lu.values())+sum(Lp.values())
    assert slack == Lplus+m*(r0+br)
    carr = [(x, K[x], r[x]) for x in D if K[x] != 0 and sum(x) >= 2]
    print(f"sigma={sig:2d} rho0={r0:2d} Br0={br:3d} rho0+Br0={r0+br:3d} L+={Lplus:4d} slack={slack:4d}  units L+ {Lu}  pairs L+ {Lp}  carries {carr}")
