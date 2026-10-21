r"""Stage 2 of the CASEB-FLAT height-3 search (lead, 2026-10-20): exact best tile for a FIXED delta (Gurobi).
Cells: 0, the d units, and multisets of size 2 and 3 of generator indices (residue = sum of delta mod m); one cell per
residue; down-set; at least one cell of size 3 (H3MIN, default 1).  Maximizes mu = Sigma_supp - Dep exactly (same
linearization as caseb_milp.py, which was validated against the exhaustive enumeration).  Writes the best tile as JSON
(for lifts.py) when mu >= 1.
Usage: python3 caseb_fix.py m d1,d2,...,dd [TL] [H3MIN] [OUTJSON]"""
import sys, json, itertools
import gurobipy as gp
from gurobipy import GRB
m = int(sys.argv[1]); delta = [int(t) for t in sys.argv[2].split(',')]; d = len(delta)
TL = int(sys.argv[3]) if len(sys.argv) > 3 else 600; H3MIN = int(sys.argv[4]) if len(sys.argv) > 4 else 1
OUT = sys.argv[5] if len(sys.argv) > 5 else None
pairs = list(itertools.combinations_with_replacement(range(d), 2))
trips = list(itertools.combinations_with_replacement(range(d), 3))
res = lambda c: sum(delta[i] for i in c) % m
mdl = gp.Model(); mdl.Params.OutputFlag = 0; mdl.Params.TimeLimit = TL; mdl.Params.Threads = 1
P = mdl.addVars(pairs, vtype=GRB.BINARY); T = mdl.addVars(trips, vtype=GRB.BINARY)
faces = {t: sorted(set(tuple(sorted(f)) for f in itertools.combinations(t, 2))) for t in trips}
for t in trips:
    for f in faces[t]: mdl.addConstr(T[t] <= P[f])
cov = {r: [] for r in range(m)}
for p in pairs: cov[res(p)].append(P[p])
for t in trips: cov[res(t)].append(T[t])
taken = {0} | {delta[a] % m for a in range(d)}
assert len(taken) == d + 1, "delta has repeats or 0"
for r in range(m):
    if r in taken: mdl.addConstr(gp.quicksum(cov[r]) == 0)
    else: mdl.addConstr(gp.quicksum(cov[r]) == 1)
mdl.addConstr(T.sum() >= H3MIN)
nmU = mdl.addVars(d, lb=0, ub=1); nmP = mdl.addVars(pairs, lb=0, ub=1)
for p in pairs:
    for a in set(p): mdl.addConstr(nmU[a] >= P[p])
for t in trips:
    for f in faces[t]: mdl.addConstr(nmP[f] >= T[t])
mult = lambda u, c: sum(1 for x in c if x == u)
dep = gp.quicksum((d + 1) * nmU[a] for a in range(d)) - gp.quicksum(2 * P[p] for p in pairs)
dep += gp.quicksum((d + 2) * nmP[p] for p in pairs)
terms = []
for t in trips:
    for f in faces[t]:
        u = list(t); u.remove(f[0]); u.remove(f[1]); terms.append((mult(u[0], f) + 1) * T[t])
dep -= gp.quicksum(terms)
supp = gp.quicksum(P[p] for p in pairs if p[0] != p[1]) + gp.quicksum((len(set(t)) - 1) * T[t] for t in trips)
mdl.setObjective(supp - dep, GRB.MAXIMIZE); mdl.optimize()
st = {GRB.OPTIMAL: 'OPTIMAL', GRB.TIME_LIMIT: 'TIME_LIMIT', GRB.INFEASIBLE: 'INFEASIBLE'}.get(mdl.Status, str(mdl.Status))
if mdl.SolCount == 0:
    print("m=%d delta=%s %s no height-3 tile" % (m, sys.argv[2], st)); sys.exit(0)
mu = round(mdl.ObjVal); cells = [list(p) for p in pairs if P[p].X > 0.5] + [list(t) for t in trips if T[t].X > 0.5]
n3 = sum(1 for c in cells if len(c) == 3)
print("m=%d delta=%s %s mu=%d bound=%.1f cubic_cells=%d%s" % (m, sys.argv[2], st, mu, mdl.ObjBound, n3, "  CASE-B-H3" if mu >= 1 else ""))
if OUT and mu >= 1: json.dump({"m": m, "delta": delta, "cells": cells}, open(OUT, 'w'))
