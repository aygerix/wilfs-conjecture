"""E14: which hypotheses does CL need?  Replace M by another element mu of D:
  V1: mu ranges over maximal elements of D (Apery-poset maximal = PF + m)
  V2: mu ranges over all elements of D."""
import sys
sys.path.insert(0, 'src')
from ns import all_by_genus
from cl import factorizations_down_set

def cl_mu(val, d, m, mu_w):
    lhs = 0
    for a in range(d):
        for n, w in val.items():
            up = list(n); up[a] += 1
            if tuple(up) not in val:
                lhs += (n[a] + 1) * ((mu_w - w) % m)
    return lhs

G = int(sys.argv[1]) if len(sys.argv) > 1 else 14
n = f1 = f2 = 0; ex1 = []; ex2 = []
for g, s in all_by_genus(G):
    if s.m == 1: continue
    m = s.m
    Pp, best = factorizations_down_set(s)
    d = len(Pp)
    val = {nn: w for w, nn in best.items()}
    target = (d - 1) * m * (m - 1) // 2
    maxels = [w for nn, w in val.items() if all(tuple(nn[:a] + (nn[a] + 1,) + nn[a+1:]) not in val for a in range(d))]
    n += 1
    bad1 = [w for w in maxels if cl_mu(val, d, m, w) < target]
    if bad1:
        f1 += 1
        if len(ex1) < 5: ex1.append((s.P, max(val.values()), bad1))
    bad2 = [w for w in val.values() if cl_mu(val, d, m, w) < target]
    if bad2:
        f2 += 1
        if len(ex2) < 3: ex2.append((s.P, max(val.values()), bad2))
print(f'genus<={G}: {n}; V1 (any maximal mu) fails in {f1}; V2 (any mu) fails in {f2}')
print('V1 ex', ex1); print('V2 ex', ex2)
