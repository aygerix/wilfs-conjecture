r"""CASEB-FLAT at height <= 3 by MILP (lead, 2026-10-20).  Gurobi; run with /usr/bin/python3 on fejer.
Chooses delta (d residues in Z/m \ 0) AND a height-<=3 lattice tile of Z/m (cells = multisets of size <= 3 from delta,
residue = sum mod m, one cell per residue, down-set) and maximizes the case-B margin mu = Sigma_supp - Dep, with at
least one cubic cell (H3=1; H3=2 allows only cubes 3e_a) or none (H3=0).  Dep = sum over non-maximal cells x of sum_{b: x+e_b not in D} (x_b + 1).
Validation target: exhaustive caseb_h3.c optima (d = 4, 5).
Usage: python3 caseb_milp.py d m H3 TL THREADS [FIX1 [MINMU [FOCUS]]]
  FIX1 = 1 adds 1 in delta (WLOG only for prime m); MINMU adds the constraint mu >= MINMU (e.g. 1 = search case B);
  FOCUS = Gurobi MIPFocus (1 = feasibility)."""
import sys, itertools, time
import gurobipy as gp
from gurobipy import GRB
d, m, H3, TL, TH = map(int, sys.argv[1:6]); FIX1 = int(sys.argv[6]) if len(sys.argv) > 6 else 0
MINMU = int(sys.argv[7]) if len(sys.argv) > 7 else None; FOCUS = int(sys.argv[8]) if len(sys.argv) > 8 else 0
V = range(1, m)
mdl = gp.Model(); mdl.Params.OutputFlag = 0; mdl.Params.TimeLimit = TL; mdl.Params.Threads = TH; mdl.Params.MIPFocus = FOCUS
s = mdl.addVars(V, vtype=GRB.BINARY, name='s')
pairs = [(v, w) for v in V for w in V if v <= w]
trip = ([(u, v, w) for u in V for v in V for w in V if u <= v <= w] if H3 == 1 else [(v, v, v) for v in V]) if H3 else []
P = mdl.addVars(pairs, vtype=GRB.BINARY, name='P')
T = mdl.addVars(trip, vtype=GRB.BINARY, name='T') if H3 else {}
key2 = lambda a, b: (a, b) if a <= b else (b, a)
for (v, w) in pairs: mdl.addConstr(P[v, w] <= s[v]); mdl.addConstr(P[v, w] <= s[w])
faces = {}
for t in trip:
    fs = set(key2(t[i], t[j]) for i, j in ((0, 1), (0, 2), (1, 2))); faces[t] = fs
    for f in fs: mdl.addConstr(T[t] <= P[f])
mdl.addConstr(s.sum() == d)
if FIX1: mdl.addConstr(s[1] == 1)
cov = {r: [] for r in range(m)}
for v in V: cov[v].append(s[v])
for p in pairs: cov[sum(p) % m].append(P[p])
for t in trip: cov[sum(t) % m].append(T[t])
mdl.addConstr(gp.quicksum(cov[0]) == 0)
for r in V: mdl.addConstr(gp.quicksum(cov[r]) == 1)
if H3: mdl.addConstr(T.sum() >= 1)
nmU = mdl.addVars(V, lb=0, ub=1, name='nmU'); nmP = mdl.addVars(pairs, lb=0, ub=1, name='nmP') if H3 else None
for (v, w) in pairs: mdl.addConstr(nmU[v] >= P[v, w]); mdl.addConstr(nmU[w] >= P[v, w])
if H3:
    for t in trip:
        for f in faces[t]: mdl.addConstr(nmP[f] >= T[t])
mult = lambda u, cell: sum(1 for x in cell if x == u)
# unit v: (d+1) nmU_v - sum_u (1+[u=v]) P_{uv}; a mixed pair appears in two units (coefficient 1 each), a loop in one
# unit (coefficient 2): total coefficient 2 for every pair.
dep = gp.quicksum((d + 1) * nmU[v] for v in V) - gp.quicksum(2 * P[p] for p in pairs)
if H3:
    dep += gp.quicksum((d + 2) * nmP[p] for p in pairs)
    # pair f = (v,w) non-max: (d+2) nmP_f - sum_u (mult_u(f) + 1) T[f + u]
    terms = []
    for t in trip:
        for f in faces[t]:
            u = list(t); u.remove(f[0]); u.remove(f[1]); u = u[0]
            terms.append((mult(u, f) + 1) * T[t])
    dep -= gp.quicksum(terms)
supp = gp.quicksum(P[v, w] for (v, w) in pairs if v != w)
if H3: supp += gp.quicksum((len(set(t)) - 1) * T[t] for t in trip)
if MINMU is not None: mdl.addConstr(supp - dep >= MINMU)
mdl.setObjective(supp - dep, GRB.MAXIMIZE)
t0 = time.time(); mdl.optimize(); el = time.time() - t0
st = {GRB.OPTIMAL: 'OPTIMAL', GRB.TIME_LIMIT: 'TIME_LIMIT', GRB.INFEASIBLE: 'INFEASIBLE'}.get(mdl.Status, str(mdl.Status))
if mdl.SolCount:
    dl = [v for v in V if s[v].X > 0.5]
    cells = [p for p in pairs if P[p].X > 0.5] + ([t for t in trip if T[t].X > 0.5] if H3 else [])
    print("d=%d m=%d H3=%d FIX1=%d %s mu_best=%d bound=%.2f time=%.1fs delta=%s ncells2=%d ncells3=%d" % (d, m, H3, FIX1, st,
          round(mdl.ObjVal), mdl.ObjBound, el, dl, sum(1 for c in cells if len(c) == 2), sum(1 for c in cells if len(c) == 3)), flush=True)
    print("  cells:", cells, flush=True)
else:
    print("d=%d m=%d H3=%d FIX1=%d MINMU=%s %s (no solution) bound=%s time=%.1fs" % (d, m, H3, FIX1, MINMU, st, getattr(mdl, 'ObjBound', None), el), flush=True)
