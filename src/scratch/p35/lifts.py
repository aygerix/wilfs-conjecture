r"""Realize a lattice tile as the Apery factorization tile of a numerical semigroup (lead, 2026-10-20).
Given m, delta (residues of the d generators) and the tile cells D (multisets of generator indices, size <= 3, plus
0 and the units), find integer lifts k_a in [1, K] with generators g_a = m k_a + delta_a such that every outer-boundary
point y of D (y not in D, y - e_i in D) is strictly dominated: y.g >= x.g + m, where x in D has the residue of y.
Strict domination on the boundary implies it for every y outside D (y = y' + z with y' on the boundary), so D is the
set of (unique) factorizations of Ap(S, m), the g_a are minimal generators, and D is the lex tile.
Optional objective: maximize the conductor (to reach c > 4m).  Then rebuilds S with ../p34/tile.py and reports
c, W, Dep, Sigma_supp, height, case.  Run with /usr/bin/python3 (Gurobi).
Usage: python3 lifts.py JSONFILE K [MAXC]   (JSONFILE: {"m":..,"delta":[..],"cells":[[i,j],[i,j,k],..]})"""
import sys, json, itertools
import gurobipy as gp
from gurobipy import GRB
sys.path.insert(0, '../p34')
from tile import build
from tcldich import stats
spec = json.load(open(sys.argv[1])); K = int(sys.argv[2]); MAXC = int(sys.argv[3]) if len(sys.argv) > 3 else 0
m, delta = spec['m'], spec['delta']; d = len(delta)
def vec(cell):
    v = [0] * d
    for i in cell: v[i] += 1
    return tuple(v)
D = {(0,) * d} | {vec([a]) for a in range(d)} | {vec(c) for c in spec['cells']}
assert len(D) == m, (len(D), m)
res = {x: sum(a * b for a, b in zip(x, delta)) % m for x in D}
assert len(set(res.values())) == m, "not a tile"
byres = {r: x for x, r in res.items()}
add = lambda x, a: tuple(v + (i == a) for i, v in enumerate(x))
bd = {add(x, a) for x in D for a in range(d)} - D
mdl = gp.Model(); mdl.Params.OutputFlag = 0
k = mdl.addVars(d, vtype=GRB.INTEGER, lb=1, ub=K)
for y in bd:
    ry = sum(a * b for a, b in zip(y, delta)); x = byres[ry % m]
    j = (ry - sum(a * b for a, b in zip(x, delta))) // m
    mdl.addConstr(gp.quicksum((y[a] - x[a]) * k[a] for a in range(d)) + j >= 1)
if MAXC:
    z = mdl.addVar(lb=0); top = {x: mdl.addVar(vtype=GRB.BINARY) for x in D}
    mdl.addConstr(gp.quicksum(top.values()) == 1)
    for x in D:
        val = gp.quicksum(x[a] * k[a] for a in range(d)) + sum(a * b for a, b in zip(x, delta)) / m
        mdl.addConstr(z <= val + (1 - top[x]) * (3 * K + 3))
    mdl.setObjective(z, GRB.MAXIMIZE)
mdl.optimize()
if mdl.Status != GRB.OPTIMAL:
    print("no lifts in [1,%d] (status %d)" % (K, mdl.Status)); sys.exit(0)
g0 = [m * int(round(k[a].X)) + delta[a] for a in range(d)]; G = sorted(g0)
R = build(m, G); c, gens, M = R; Dt = list(M)
v, dep, ss = stats(m, Dt, [g % m for g in gens])
# genus via the Apery set (Selmer): g = sum of floor(w/m)
w = sorted(sum(x[a] * gens[a] for a in range(len(gens))) for x in Dt)
apD = sorted(sum(x[a] * g0[a] for a in range(d)) for x in D)
genus = sum(x // m for x in w); ell = c - genus; e = len(gens) + 1
print("S = <%d, %s>  c=%d  c/m=%.2f  e=%d  W=%d  Dep=%d  Sigma_supp=%d  mu=%d  height=%d  open=%d  tile_matches=%d" % (
    m, gens, c, c / m, e, e * ell - c, dep, ss, ss - dep, max(sum(x) for x in Dt), int(3 * e < m and c > 4 * m),
    int(w == apD and gens == G)))
