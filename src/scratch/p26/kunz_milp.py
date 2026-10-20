r"""Kunz-coordinate MILP for Wilf at fixed multiplicity m (lead, 2026-10-20; advisor's proposal).
Variables: Kunz coordinates k_1..k_{m-1} >= 1 (w_i = m k_i + i in Ap(S, m)), unbounded unless --K is given.
Constraints (exact): k_i + k_j + [i+j>m] >= k_{(i+j) mod m} for 1 <= i <= j <= m-1, i+j != m (Kunz).
Tightness t_ij (indicator: t=1 => equality, t=0 => slack >= 1); generator g_s = 1 iff no pair summing to s is tight;
e = 1 + sum g_s (fixed per model); conductor residue r fixed: w_r = max_i w_i; c = m k_r + r - m + 1; g = sum k_i.
Wilf number W = (e-1)c - e g (linear for fixed e, r).
mode feas: is W <= thr feasible (thr default -1)?  mode min: minimize W.
Options: --skipknown: only e with 3e < m and require c >= 3m + e + 1 (Eliahou c <= 3m, DEPTH4-EH c <= 3m+e).
Each solution is decoded and re-verified independently (generators recomputed from the Apery set).
usage: /usr/bin/python3 kunz_milp.py m mode [--thr T] [--K K] [--skipknown] [--tl secs] [--threads n] [--elist a,b] [--rlist ...]"""
import sys, time, argparse
import gurobipy as gp
from gurobipy import GRB
ap = argparse.ArgumentParser()
ap.add_argument("m", type=int); ap.add_argument("mode")
ap.add_argument("--thr", type=int, default=-1); ap.add_argument("--K", type=int, default=0)
ap.add_argument("--skipknown", action="store_true"); ap.add_argument("--tl", type=float, default=600)
ap.add_argument("--threads", type=int, default=2); ap.add_argument("--elist", default=""); ap.add_argument("--rlist", default="")
args = ap.parse_args(); m = args.m
def decode_verify(k):
    w = [0] + [m * k[i] + i for i in range(1, m)]
    Ws = set(w)
    gens = [m] + [w[s] for s in range(1, m) if not any((w[s] - w[i]) in Ws and (w[s] - w[i]) > 0 for i in range(1, m) if w[i] < w[s])]
    # sanity: Kunz validity (Ap set closed: w_i + w_j >= w_{i+j})
    ok = all(w[i] + w[j] >= w[(i + j) % m] for i in range(1, m) for j in range(1, m) if (i + j) % m)
    c = max(w) - m + 1; g = sum(k[1:]); e = len(gens)
    return dict(ok=ok, e=e, c=c, g=g, W=e * (c - g) - c, gens=sorted(gens))
pairs = [(i, j) for i in range(1, m) for j in range(i, m) if i + j != m]
def solve(e, r):
    M = gp.Model(); M.Params.OutputFlag = 0; M.Params.Threads = args.threads; M.Params.TimeLimit = args.tl
    M.Params.IntFeasTol = 1e-9; M.Params.FeasibilityTol = 1e-9
    ub = args.K if args.K else GRB.INFINITY
    k = M.addVars(range(1, m), vtype=GRB.INTEGER, lb=1, ub=ub, name="k")
    t = M.addVars(pairs, vtype=GRB.BINARY, name="t")
    to = {s: [] for s in range(1, m)}
    for (i, j) in pairs:
        s = (i + j) % m; cr = 1 if i + j > m else 0
        expr = k[i] + k[j] + cr - k[s]
        M.addConstr(expr >= 0)
        M.addGenConstrIndicator(t[i, j], True, expr, GRB.EQUAL, 0)
        M.addGenConstrIndicator(t[i, j], False, expr, GRB.GREATER_EQUAL, 1)
        to[s].append(t[i, j])
    gv = M.addVars(range(1, m), vtype=GRB.BINARY, name="g")
    for s in range(1, m):
        for tt in to[s]: M.addConstr(gv[s] <= 1 - tt)
        M.addConstr(gv[s] >= 1 - gp.quicksum(to[s]))
    M.addConstr(gp.quicksum(gv.values()) == e - 1)
    for i in range(1, m):
        if i != r: M.addConstr(m * k[r] + r >= m * k[i] + i + 1)
    c = m * k[r] + r - m + 1; g = gp.quicksum(k.values())
    Wexpr = (e - 1) * c - e * g
    if args.skipknown: M.addConstr(c >= 3 * m + e + 1)
    if args.mode == "feas": M.addConstr(Wexpr <= args.thr); M.setObjective(0)
    else: M.setObjective(Wexpr, GRB.MINIMIZE)
    t0 = time.time(); M.optimize(); dt = time.time() - t0
    out = dict(status=M.Status, time=dt, nodes=M.NodeCount)
    if M.SolCount > 0:
        kv = [0] + [int(round(k[i].X)) for i in range(1, m)]
        out["sol"] = kv; out["ver"] = decode_verify(kv); out["obj"] = M.ObjVal
        if args.mode == "min": out["bound"] = M.ObjBound
    return out
es = [int(x) for x in args.elist.split(",")] if args.elist else list(range(2, m + 1))
if args.skipknown: es = [e for e in es if 3 * e < m]
rs = [int(x) for x in args.rlist.split(",")] if args.rlist else list(range(1, m))
names = {GRB.OPTIMAL: "OPTIMAL", GRB.INFEASIBLE: "INFEASIBLE", GRB.TIME_LIMIT: "TIME_LIMIT", GRB.INF_OR_UNBD: "INF_OR_UNBD", GRB.UNBOUNDED: "UNBOUNDED"}
T0 = time.time(); summary = {}
for e in es:
    for r in rs:
        o = solve(e, r); st = names.get(o["status"], str(o["status"]))
        summary[st] = summary.get(st, 0) + 1
        line = f"m={m} e={e} r={r}: {st} {o['time']:.1f}s nodes={o['nodes']:.0f}"
        if "sol" in o: line += f" obj={o['obj']:.0f}" + (f" bound={o.get('bound', 0):.1f}" if args.mode == "min" else "") + f" ver={o['ver']}"
        print(line, flush=True)
print(f"m={m} mode={args.mode} summary {summary} total {time.time() - T0:.1f}s", flush=True)
