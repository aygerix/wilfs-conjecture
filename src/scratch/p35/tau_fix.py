r"""Leading-order test of CONJ CASEB-U, lift-free (lead, 2026-10-20).  For FIXED residues delta (one tile cell per
residue, cells = multisets of size <= 3, down-set), minimize tau*_D = min{sum_b v_b : y.v >= |y| - 1 for all y in D, v >= 0}
subject to case B (Sigma_supp - Dep >= MINMU) and >= H3 cubic cells.  The unit truncation satisfies
U >~ q (e (1 + tau*_D) - m), so a positive minimum of e(1 + tau*) - m means CASEB-U holds at leading order for EVERY lift
vector on this delta.  Usage: python3 tau_fix.py m d1,..,dd TL MINMU H3"""
import sys, itertools
import gurobipy as gp
from gurobipy import GRB
m = int(sys.argv[1]); delta = [int(t) for t in sys.argv[2].split(',')]; d = len(delta); TL, MINMU, H3 = map(int, sys.argv[3:6])
cells = {s: list(itertools.combinations_with_replacement(range(d), s)) for s in range(4)}
res = lambda c: sum(delta[i] for i in c) % m
cnt = lambda c, a: sum(1 for i in c if i == a)
mdl = gp.Model(); mdl.Params.OutputFlag = 0; mdl.Params.TimeLimit = TL; mdl.Params.Threads = 2
X = {c: mdl.addVar(vtype=GRB.BINARY) for s in (2, 3) for c in cells[s]}
faces = {t: sorted(set(tuple(sorted(f)) for f in itertools.combinations(t, 2))) for t in cells[3]}
for t in cells[3]:
    for f in faces[t]: mdl.addConstr(X[t] <= X[f])
byres = {r: [] for r in range(m)}
for s in (2, 3):
    for c in cells[s]: byres[res(c)].append(c)
taken = {0} | {x % m for x in delta}; assert len(taken) == d + 1
for r in range(m): mdl.addConstr(gp.quicksum(X[c] for c in byres[r]) == (0 if r in taken else 1))
if H3: mdl.addConstr(gp.quicksum(X[t] for t in cells[3]) >= H3)
nmU = mdl.addVars(d, lb=0, ub=1); nmP = {p: mdl.addVar(lb=0, ub=1) for p in cells[2]}
for p in cells[2]:
    for a in set(p): mdl.addConstr(nmU[a] >= X[p])
for t in cells[3]:
    for f in faces[t]: mdl.addConstr(nmP[f] >= X[t])
for a in range(d): mdl.addConstr(nmU[a] <= gp.quicksum(X[p] for p in cells[2] if a in p))
for p in cells[2]: mdl.addConstr(nmP[p] <= gp.quicksum(X[t] for t in cells[3] if p in faces[t]))
dep = gp.quicksum((d + 1) * nmU[a] for a in range(d)) - gp.quicksum(2 * X[p] for p in cells[2])
dep += gp.quicksum((d + 2) * nmP[p] for p in cells[2])
terms = []
for t in cells[3]:
    for f in faces[t]:
        u = list(t); u.remove(f[0]); u.remove(f[1]); terms.append((cnt(f, u[0]) + 1) * X[t])
dep -= gp.quicksum(terms)
supp = gp.quicksum(X[p] for p in cells[2] if p[0] != p[1]) + gp.quicksum((len(set(t)) - 1) * X[t] for t in cells[3])
mdl.addConstr(supp - dep >= MINMU)
v = mdl.addVars(d, lb=0, ub=1)
for s in (2, 3):
    for y in cells[s]: mdl.addConstr(gp.quicksum(cnt(y, a) * v[a] for a in range(d)) >= (s - 1) * X[y])
mdl.setObjective(gp.quicksum(v.values()), GRB.MINIMIZE); mdl.optimize()
st = {GRB.OPTIMAL: 'OPTIMAL', GRB.TIME_LIMIT: 'TIME_LIMIT', GRB.INFEASIBLE: 'INFEASIBLE'}.get(mdl.Status, str(mdl.Status))
if mdl.SolCount == 0: print("m=%d delta=%s %s no solution" % (m, sys.argv[2], st)); sys.exit(0)
tau = mdl.ObjVal; nc = sum(1 for t in cells[3] if X[t].X > 0.5)
print("m=%d d=%d delta=%s MINMU=%d H3=%d %s tau*=%.4f (bound %.4f) e(1+tau*)-m=%.3f cubics=%d mu=%d v=%s" % (
    m, d, sys.argv[2], MINMU, H3, st, tau, mdl.ObjBound, (d + 1) * (1 + tau) - m, nc, round(supp.getValue() - dep.getValue()),
    [round(v[a].X, 3) for a in range(d)]), flush=True)
