# Find small tiles where geometric splits cannot certify MaxCL(0) (geo-only LP fails) and print a GCL certificate:
#   c = sum_rel lam_rel (e_g + e_h - e_{g+h}) + mu,  c = d+1 on N, -(|y|-1) on A  (positions g = phi mod m, sigma = 0).
# Objective: minimize total wrap weight sum lam [g + h >= m] (then total lam), to get the 'most identity-tight' certificate.
import sys, itertools
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from rgcl0 import rgcl0
def gcl_cert(cells, d, m, sigma=0):
    S = set(cells)
    A = {y for y in cells if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))}
    inv = {(cells[x] - sigma) % m: x for x in cells}
    c = np.zeros(m)
    for g in range(1, m):
        x = inv[g]; c[g] = -(sum(x) - 1) if x in A else d + 1
    rels = [(g, h) for g in range(1, m) for h in range(g, m) if (g + h) % m != 0]
    nR = len(rels); Aeq = np.zeros((m - 1, nR + m - 1))
    for k, (g, h) in enumerate(rels):
        Aeq[g - 1, k] += 1; Aeq[h - 1, k] += 1; Aeq[(g + h) % m - 1, k] -= 1
    for g in range(1, m): Aeq[g - 1, nR + g - 1] = 1
    cost = np.array([1000.0*((g + h) >= m) + 1.0 for g, h in rels] + [0.0]*(m - 1))
    res = linprog(cost, A_eq=Aeq, b_eq=c[1:], bounds=[(0, None)]*(nR + m - 1), method='highs')
    if res.status != 0: return None
    out = []
    for k, (g, h) in enumerate(rels):
        if res.x[k] > 1e-7:
            u, v, y = inv[g], inv[h], inv[(g + h) % m]
            lat = tuple(a + b - e for a, b, e in zip(u, v, y))
            out.append((round(res.x[k], 4), u, v, y, g, h, (g + h) % m, lat))
    return out, A, inv
if __name__ == '__main__':
    from ns import NS
    from srcl import tile_of
    from math import gcd
    from functools import reduce
    found = []
    for m in range(5, int(sys.argv[1]) + 1):
        for n1 in range(m + 1, 3*m):
            for n2 in range(n1 + 1, 3*m):
                for n3 in range(n2 + 1, 3*m):
                    g = [m, n1, n2, n3]
                    if reduce(gcd, g) != 1: continue
                    s = NS.from_generators(g)
                    if s.e != 4: continue
                    cells, d = tile_of(s)
                    if rgcl0(cells, d, m, succ=False) > 1e-9:
                        found.append(g)
        if found: print('m', m, 'geo-only fails at sigma=0 for', found[:10], flush=True); break
    s = NS.from_generators(found[0]); cells, d = tile_of(s)
    out, A, inv = gcl_cert(cells, d, s.m)
    print('tile', found[0], 'cells by position:', [(g, inv[g], 'A' if inv[g] in A else 'N') for g in range(s.m)])
    for row in sorted(out, key=lambda t: -t[0]): print('  lam', row[0], 'u', row[1], '+ v', row[2], '-> y', row[3], ' pos', row[4:7], ' u+v-y', row[7])
