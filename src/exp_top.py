"""Experiment E5: condition TOP (sufficient for Wilf, derived from Identity CH).
X_q = Ap cap [c, c+m); pi(u) = u - c + 1 in [1,m]; Lam(u) = sum_a (nu_a(u)+1).
TOP_E : sum_{u in X_q} pi(u) Lam(u) <= m((d+1)m + d - 1)/2 + E
TOP_0 : same without E."""
import sys
sys.path.insert(0, 'src')
from ns import all_by_genus
from chains import chain_data

def nu(s, w, p):
    k = 0
    while w - (k + 1) * p >= 0 and (w - (k + 1) * p) in s:
        k += 1
    return k

G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
fE = f0 = n = 0
exE, ex0 = [], []
for g, s in all_by_genus(G):
    if s.m <= 2:
        continue
    m, c = s.m, s.c
    Pp = [p for p in s.P if p != m]
    d = len(Pp)
    Xq = [w for w in s.apery() if w >= c]
    lhs = sum((u - c + 1) * sum(nu(s, u, p) + 1 for p in Pp) for u in Xq)
    rhs0 = m * ((d + 1) * m + d - 1)  # times 2
    E = chain_data(s)['E']
    n += 1
    if 2 * lhs > rhs0 + 2 * E:
        fE += 1
        if len(exE) < 8: exE.append((s.P, s.c, s.q, s.W, 2*lhs - rhs0 - 2*E))
    if 2 * lhs > rhs0:
        f0 += 1
        if len(ex0) < 5: ex0.append((s.P, s.c, s.q, s.W))
print(f'genus<={G}: {n} semigroups (m>=3); TOP_E fails {fE}; TOP_0 fails {f0}')
print('TOP_E failures', exE)
print('TOP_0 failures', ex0)
