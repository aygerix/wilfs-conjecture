r"""Height-3 case-B tiles that are Apery factorization tiles of a numerical semigroup (lead, 2026-10-20).  Gurobi.
For FIXED m, delta: choose the tile D (cells = multisets of size <= 3 of generator indices; one per residue; down-set;
>= 1 cubic cell) AND integer lifts k_a in [1, K] (generators g_a = m k_a + delta_a) such that every multiset y of size
<= 4 outside D is strictly dominated by the D-cell x of its residue: (y - x).k + j(x,y) >= 1, j = ((y-x).delta)/m.
Strict domination on all y of size <= 4 covers the outer boundary of D, so D is the (unique-factorization) Apery tile.
Maximizes mu = Sigma_supp - Dep subject to mu >= MINMU (default 1).  Prints S; verify independently with lifts.py.
Usage: python3 caseb_fixlift.py m d1,..,dd K [TL] [MINMU] [OUTJSON] [H3MIN]
  H3MIN: minimum number of cubic cells (default 1); -1 forbids cubic cells (flat tiles)."""
import sys, json, itertools
import gurobipy as gp
from gurobipy import GRB
m = int(sys.argv[1]); delta = [int(t) for t in sys.argv[2].split(',')]; d = len(delta); K = int(sys.argv[3])
TL = int(sys.argv[4]) if len(sys.argv) > 4 else 600; MINMU = int(sys.argv[5]) if len(sys.argv) > 5 else 1
OUT = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6] != '-' else None
H3MIN = int(sys.argv[7]) if len(sys.argv) > 7 else 1
cells = {s: list(itertools.combinations_with_replacement(range(d), s)) for s in range(5)}
res = lambda c: sum(delta[i] for i in c) % m
val = lambda c: sum(delta[i] for i in c)
mdl = gp.Model(); mdl.Params.OutputFlag = 0; mdl.Params.TimeLimit = TL; mdl.Params.Threads = 1
X = {}
for s in (2, 3):
    for c in cells[s]: X[c] = mdl.addVar(vtype=GRB.BINARY)
one = lambda c: 1 if len(c) <= 1 else (0 if len(c) == 4 else X[c])
k = mdl.addVars(d, vtype=GRB.INTEGER, lb=1, ub=K)
faces = {t: sorted(set(tuple(sorted(f)) for f in itertools.combinations(t, 2))) for t in cells[3]}
for t in cells[3]:
    for f in faces[t]: mdl.addConstr(X[t] <= X[f])
byres = {r: [] for r in range(m)}
for s in range(5):
    for c in cells[s]: byres[res(c)].append(c)
taken = {0} | {delta[a] % m for a in range(d)}
assert len(taken) == d + 1
for r in range(m):
    inD = [X[c] for c in byres[r] if len(c) in (2, 3)]
    if r in taken: mdl.addConstr(gp.quicksum(inD) == 0)
    else: mdl.addConstr(gp.quicksum(inD) == 1)
if H3MIN >= 0: mdl.addConstr(gp.quicksum(X[t] for t in cells[3]) >= H3MIN)
else: mdl.addConstr(gp.quicksum(X[t] for t in cells[3]) == 0)
cnt = lambda c, a: sum(1 for i in c if i == a)
for r in range(m):
    L = byres[r]
    for x in L:
        if len(x) == 4: continue
        for y in L:
            if y == x: continue
            j = (val(y) - val(x)) // m
            lhs = gp.quicksum((cnt(y, a) - cnt(x, a)) * k[a] for a in range(d)) + j
            ix = one(x); iy = one(y)
            if isinstance(ix, int) and isinstance(iy, int):
                if ix == 1 and iy == 0: mdl.addConstr(lhs >= 1)
                continue
            M = 4 * K + 6
            mdl.addConstr(lhs >= 1 - M * (1 - ix + iy))
nmU = mdl.addVars(d, lb=0, ub=1); nmP = {p: mdl.addVar(lb=0, ub=1) for p in cells[2]}
for p in cells[2]:
    for a in set(p): mdl.addConstr(nmU[a] >= X[p])
for t in cells[3]:
    for f in faces[t]: mdl.addConstr(nmP[f] >= X[t])
dep = gp.quicksum((d + 1) * nmU[a] for a in range(d)) - gp.quicksum(2 * X[p] for p in cells[2])
dep += gp.quicksum((d + 2) * nmP[p] for p in cells[2])
terms = []
for t in cells[3]:
    for f in faces[t]:
        u = list(t); u.remove(f[0]); u.remove(f[1]); terms.append((cnt(f, u[0]) + 1) * X[t])
dep -= gp.quicksum(terms)
supp = gp.quicksum(X[p] for p in cells[2] if p[0] != p[1]) + gp.quicksum((len(set(t)) - 1) * X[t] for t in cells[3])
mdl.addConstr(supp - dep >= MINMU)
mdl.setObjective(supp - dep, GRB.MAXIMIZE); mdl.optimize()
st = {GRB.OPTIMAL: 'OPTIMAL', GRB.TIME_LIMIT: 'TIME_LIMIT', GRB.INFEASIBLE: 'INFEASIBLE'}.get(mdl.Status, str(mdl.Status))
if mdl.SolCount == 0:
    print("m=%d delta=%s K=%d %s: no realizable height-3 tile with mu >= %d" % (m, sys.argv[2], K, st, MINMU)); sys.exit(0)
ks = [int(round(k[a].X)) for a in range(d)]; G = [m * ks[a] + delta[a] for a in range(d)]
D = [list(c) for c in cells[2] + cells[3] if X[c].X > 0.5]
print("m=%d delta=%s K=%d %s mu=%d bound=%.1f gens=%s cubic=%d  REALIZED-CASE-B-H3" % (m, sys.argv[2], K, st, round(mdl.ObjVal),
      mdl.ObjBound, sorted(G), sum(1 for c in D if len(c) == 3)), flush=True)
if OUT: json.dump({"m": m, "delta": delta, "cells": D, "gens": G}, open(OUT, 'w'))
