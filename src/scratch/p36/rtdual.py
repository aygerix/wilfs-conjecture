r"""Optimal dual (signed split certificate) of the relaxation RT of kunz_face.py, aggregated by cell type (lead, 2026-10-20).
RT: min e(q + sum y) - qm + rho, y >= 0, tight pairs (i,j->s): y_i + y_j - y_s >= q - eps_s [lam],  <= q + 1 [nu].
Dual: max sum lam (q - eps) - sum nu (q + 1) + eq - qm + rho  s.t.  sum_p (lam_p - nu_p)(mult of x in parts - [s_p = x]) <= e.
Prints the net weight pi = lam - nu summed over pair types (h_i, h_j -> h_s, eps_s), the loads e - (L_x - beta_x) by height,
and the value decomposition  RT = q (sum pi - (m - e)) + rho - sum lam eps - sum nu.
Usage: /usr/bin/python3 rtdual.py m g1 g2 ..."""
import sys
from collections import defaultdict
sys.path.insert(0, '.')
import gurobipy as gp
from gurobipy import GRB
from kunz_face import apery
G = list(map(int, sys.argv[1:])); m = min(G); w = apery(m, G); Ws = set(w)
gens = [s for s in range(1, m) if not any(w[s] - w[i] in Ws and 0 < w[s] - w[i] for i in range(1, m) if w[i] < w[s])]
e = len(gens) + 1; c = max(w) - m + 1; r = w.index(max(w)); q = -(-c // m); rho = q * m - c
mu = [q] + [max(0, -((w[s] - c) // m)) for s in range(1, m)]; rp = [(w[s] - c) % m for s in range(m)]
tight = [(i, j, (i + j) % m) for i in range(1, m) for j in range(i, m) if (i + j) % m and w[i] + w[j] == w[(i + j) % m]]
hgt = [0] * m
for s in sorted(range(1, m), key=lambda x: w[x]):
    hgt[s] = 1 if s in gens else max(hgt[i] + hgt[j] for (i, j, t) in tight if t == s)
eps = [1 if rp[s] >= m - rho else 0 for s in range(m)]
M = gp.Model(); M.Params.OutputFlag = 0; M.Params.Threads = 2
y = M.addVars(range(1, m), lb=0)
lo, up = {}, {}
for (i, j, s) in tight:
    lo[i, j] = M.addConstr(y[i] + y[j] - y[s] >= q - eps[s]); up[i, j] = M.addConstr(y[i] + y[j] - y[s] <= q + 1)
M.setObjective(e * (q + gp.quicksum(y.values())) - q * m + rho, GRB.MINIMIZE); M.optimize()
W = e * sum(mu) - c
print("m=%d e=%d c=%d q=%d rho=%d h=%d W=%d RT=%.4f |tight|=%d |W_rho cells|=%d" % (
    m, e, c, q, rho, max(hgt), W, M.ObjVal, len(tight), sum(eps[1:])))
agg = defaultdict(lambda: [0.0, 0.0, 0]); net = {}
load = defaultdict(float)
for (i, j, s) in tight:
    la, nu = lo[i, j].Pi, -up[i, j].Pi
    assert la >= -1e-9 and nu >= -1e-9
    key = (min(hgt[i], hgt[j]), max(hgt[i], hgt[j]), hgt[s], eps[s])
    agg[key][0] += la; agg[key][1] += nu; agg[key][2] += 1
    p = la - nu; load[i] += p; load[j] += p; load[s] -= p
sl, sn = sum(lo[k].Pi for k in lo), sum(-up[k].Pi for k in up)
le = sum(lo[k].Pi * eps[(k[0] + k[1]) % m] for k in lo)
print("  sum lam=%.3f sum nu=%.3f  Gamma=sum pi-(m-e)=%.3f  value = q*Gamma + rho - lam.eps - nu = %.3f*%d + %d - %.3f - %.3f" % (
    sl, sn, sl - sn - (m - e), sl - sn - (m - e), q, rho, le, sn))
print("  pair type (h_i,h_j->h_s,eps): lam, nu, count")
for key in sorted(agg): print("   ", key, "lam=%.3f nu=%.3f n=%d" % tuple(agg[key]))
byh = defaultdict(list)
for s in range(1, m): byh[hgt[s]].append(round(e - load[s], 3))
for h in sorted(byh): print("  height %d: slack e-(L-beta) = %s  (y, mu) gens: %s" % (h, sorted(byh[h]),
    [(round(y[s].X, 2), mu[s]) for s in range(1, m) if hgt[s] == h][:12] if h <= 1 else ''))
