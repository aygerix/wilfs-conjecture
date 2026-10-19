"""Per-level anatomy of the pure-counting form at one phase:  S = Lam_r + m * sum_j (sh_j - |U_j|),
sh_j = sum_b |B_b(U'_j)|, U_j = {v >= jm}, U'_j = {v >= jm - rho0}.  usage: python pc_levels.py rho0 m g1 g2 ..."""
import sys
sys.path.insert(0, '../nowrap')
from pmin_tile import apery, minimal_gens, tile
r0 = int(sys.argv[1]); m = int(sys.argv[2]); n, ap = minimal_gens(m, list(map(int, sys.argv[3:]))); d = len(n); P = [g % m for g in n]
D = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values()); Ds = set(D)
up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}; r = {x: (v[x]+r0) % m for x in D}
cols = []
for b in range(d):
    for t in D:
        if up(t, b) in Ds: continue
        col = [t]; y = list(t)
        while y[b] > 0: y[b] -= 1; col.append(tuple(y))
        cols.append((b, t, col))
S = (d+1)*m*(m-1)//2-sum((d+sum(y))*r[y] for y in A); Lam = sum(len(col)*r[t] for (b, t, col) in cols if t not in A)
print("m", m, "n", n, "P", P, "d", d, "height", max(map(sum, D)), "rho0", r0, "S", S, "Lam_r", Lam, "S-Lam", S-Lam)
J = max(v.values())//m+1
for j in range(1, J+1):
    U = set(x for x in D if v[x] >= j*m); Up = set(x for x in D if v[x] >= j*m-r0)
    sh = sum(1 for (b, t, col) in cols if t in Up for x in col if x not in Up)
    print(" level", j, "|U_j|", len(U), "(max", sum(1 for x in U if x in A), ") |U'_j|", len(Up), "shadow", sh, "diff", sh-len(U))
print(" non-max tops with r>0:", sorted(((t, len(col), b, r[t]) for (b, t, col) in cols if t not in A and r[t] > 0), key=lambda z: -z[1]*z[3])[:12])
