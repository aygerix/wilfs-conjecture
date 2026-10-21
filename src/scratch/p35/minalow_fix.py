r"""Minimize the CASEB-WINDOW slack (d+1)|A_<| - (Sigma_supp - Dep) over semigroups with FIXED residues delta whose lex
tile is in case B and has a height-3 cell (lead, 2026-10-20; model as in minw_fix.py).  A_< = maximal tile cells with
w < c.  Prints the minimizer; check it with alow.py and verify_s.py.
Original minw_fix docstring follows.
Minimize the Wilf number over semigroups with FIXED residues delta whose lex tile is in case B (lead, 2026-10-20).
Gurobi.  Variables: tile D (multisets of size <= 3 of generator indices; one per residue; down-set), lifts k_a in
[1, K] (g_a = m k_a + delta_a) with strict domination of every multiset of size <= 4 outside D (so D is the
unique-factorization Apery tile), conductor c = max_{x in D} w(x) - m + 1 (selected top cell), and
mu_x = ceil((c - w(x))/m)^+ for x in D (so ell = sum mu_x).  Objective: W = (d+1) ell - c.
Constraints: case B (Sigma_supp - Dep >= MINMU), optionally >= H3 cubic cells, optionally c >= CMIN*m.
Usage: python3 minalow_fix.py m d1,..,dd K TL MINMU H3 CMIN"""
import sys, itertools
import gurobipy as gp
from gurobipy import GRB
m = int(sys.argv[1]); delta = [int(t) for t in sys.argv[2].split(',')]; d = len(delta); K = int(sys.argv[3])
TL, MINMU, H3, CMIN = map(int, sys.argv[4:8])
cells = {s: list(itertools.combinations_with_replacement(range(d), s)) for s in range(5)}
res = lambda c: sum(delta[i] for i in c) % m
val = lambda c: sum(delta[i] for i in c)
cnt = lambda c, a: sum(1 for i in c if i == a)
mdl = gp.Model(); mdl.Params.OutputFlag = 0; mdl.Params.TimeLimit = TL; mdl.Params.Threads = 2
X = {c: mdl.addVar(vtype=GRB.BINARY) for s in (2, 3) for c in cells[s]}
one = lambda c: 1 if len(c) <= 1 else (0 if len(c) == 4 else X[c])
k = mdl.addVars(d, vtype=GRB.INTEGER, lb=1, ub=K)
faces = {t: sorted(set(tuple(sorted(f)) for f in itertools.combinations(t, 2))) for t in cells[3]}
for t in cells[3]:
    for f in faces[t]: mdl.addConstr(X[t] <= X[f])
byres = {r: [] for r in range(m)}
for s in range(5):
    for c in cells[s]: byres[res(c)].append(c)
taken = {0} | {x % m for x in delta}; assert len(taken) == d + 1
for r in range(m):
    inD = [X[c] for c in byres[r] if len(c) in (2, 3)]
    mdl.addConstr(gp.quicksum(inD) == (0 if r in taken else 1))
if H3: mdl.addConstr(gp.quicksum(X[t] for t in cells[3]) >= H3)
Mbig = 4 * K + 6
for r in range(m):
    for x in byres[r]:
        if len(x) == 4: continue
        for y in byres[r]:
            if y == x: continue
            j = (val(y) - val(x)) // m
            lhs = gp.quicksum((cnt(y, a) - cnt(x, a)) * k[a] for a in range(d)) + j
            ix, iy = one(x), one(y)
            if isinstance(ix, int) and isinstance(iy, int):
                if ix == 1 and iy == 0: mdl.addConstr(lhs >= 1)
                continue
            mdl.addConstr(lhs >= 1 - Mbig * (1 - ix + iy))
# Dep / Sigma_supp (case B)
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
# nmU/nmP must be exact here (they are only bounded below otherwise); force upper bounds
for a in range(d): mdl.addConstr(nmU[a] <= gp.quicksum(X[p] for p in cells[2] if a in p))
for p in cells[2]: mdl.addConstr(nmP[p] <= gp.quicksum(X[t] for t in cells[3] if p in faces[t]))
# conductor and left elements
allD = cells[0] + cells[1] + cells[2] + cells[3]
w = {x: m * gp.quicksum(cnt(x, a) * k[a] for a in range(d)) + val(x) for x in allD}
WMAX = m * (3 * K + 3) + 3 * m
cv = mdl.addVar(vtype=GRB.INTEGER, lb=0, ub=WMAX)
z = {x: mdl.addVar(vtype=GRB.BINARY) for x in allD}
mdl.addConstr(gp.quicksum(z.values()) == 1)
for x in allD:
    mdl.addConstr(z[x] <= one(x)) if not isinstance(one(x), int) else (mdl.addConstr(z[x] <= one(x)))
    mdl.addConstr(cv <= w[x] - m + 1 + WMAX * (1 - z[x]))
    if isinstance(one(x), int): mdl.addConstr(cv >= w[x] - m + 1)
    else: mdl.addConstr(cv >= w[x] - m + 1 - WMAX * (1 - X[x]))
if CMIN: mdl.addConstr(cv >= CMIN * m + 1)
mu = {x: mdl.addVar(vtype=GRB.INTEGER, lb=0, ub=WMAX // m + 2) for x in allD}
for x in allD:
    ix = one(x)
    if isinstance(ix, int): mdl.addConstr(m * mu[x] >= cv - w[x])
    else:
        mdl.addConstr(m * mu[x] >= cv - w[x] - WMAX * (1 - ix)); mdl.addConstr(mu[x] <= (WMAX // m + 2) * ix)
ell = gp.quicksum(mu.values())
# A_< indicators: y in D, maximal, w(y) < c.  hi[y] = 1 is allowed only if w(y) >= c.
nmx = {}
for a in range(d): nmx[(a,)] = nmU[a]
for p in cells[2]: nmx[p] = nmP[p]
for t in cells[3]: nmx[t] = 0
bl, hi = {}, {}
for y in cells[1] + cells[2] + cells[3]:
    bl[y] = mdl.addVar(vtype=GRB.BINARY); hi[y] = mdl.addVar(vtype=GRB.BINARY)
    mdl.addConstr(w[y] >= cv - WMAX * (1 - hi[y]))
    mdl.addConstr(bl[y] >= one(y) - nmx[y] - hi[y])
alow = gp.quicksum(bl.values())
mdl.setObjective((d + 1) * alow - (supp - dep), GRB.MINIMIZE); mdl.optimize()
st = {GRB.OPTIMAL: 'OPTIMAL', GRB.TIME_LIMIT: 'TIME_LIMIT', GRB.INFEASIBLE: 'INFEASIBLE'}.get(mdl.Status, str(mdl.Status))
if mdl.SolCount == 0:
    print("m=%d delta=%s K=%d %s no solution" % (m, sys.argv[2], K, st)); sys.exit(0)
ks = [int(round(k[a].X)) for a in range(d)]; G = sorted(m * ks[a] + delta[a] for a in range(d))
# W and the weighted bound are recomputed exactly from the generators by alow.py / verify_s.py (mu is not tight here)
print("m=%d delta=%s K=%d MINMU=%d H3=%d CMIN=%d %s minslack=%d bound=%.1f |A_<|=%d mu=%d c=%d gens=%s" % (
      m, sys.argv[2], K, MINMU, H3, CMIN, st, round(mdl.ObjVal), mdl.ObjBound, round(alow.getValue()),
      round(supp.getValue() - dep.getValue()), round(cv.X), G), flush=True)
