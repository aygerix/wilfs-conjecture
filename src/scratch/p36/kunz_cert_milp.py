r"""Backward search (lead, 2026-10-20): genuine numerical semigroups at fixed multiplicity m that minimize either the
Wilf number W or the value of a Kunz-face relaxation (R or RT of kunz_face.py), via one exact MILP per (e, r).

Exact semigroup part (audited from p26/kunz_milp.py): integer Kunz coordinates k_1..k_{m-1} in [1, K]; Kunz
inequalities k_i + k_j + [i+j>m] >= k_{(i+j) mod m}; tightness t_ij by indicators (t=1 <=> equality, else slack >= 1);
minimal generator g_s = 1 iff no tight pair sums to s; e = 1 + sum g_s fixed; conductor residue r fixed (w_r > w_s for
s != r), so c = m k_r + r - m + 1, q = k_r, rho = m - r - 1 and the positions r_s = (s - r - 1) mod m are constants.
Relaxation part (objective R or RT): continuous y_s >= 0; for each tight pair (t_ij = 1, s = i + j mod m):
    y_i + y_j - y_s >= k_r - [r_s >= m - rho]      (R and RT),      y_i + y_j - y_s <= k_r + 1      (RT only).
Objective:  W = (e-1)c - e*sum k   (obj W),   or   e(k_r + sum y) - k_r m + rho   (obj R/RT/RT2/UA/UA2/TX; = min over S of
the relaxation value, a lower bound for W).  TX: tight pairs y_i + y_j - y_s = k_r + tau_ij exactly, tau_ij =
(r_i + r_j - r_s - rho)/m with r_x = (x - r - 1) mod m (kunz_face.py TX).
Optional domain restrictions: --open (c >= 4m+1, 3e < m), --h3 (every Apery element is a sum of <= 3 generators and at
least one is not a sum of <= 2), --dense (m > e^2).
Every solution is decoded, re-verified from its Apery set, and its relaxation values recomputed by kunz_face.face.
usage: /usr/bin/python3 kunz_cert_milp.py m e OBJ [--K K] [--open] [--h3] [--dense] [--tl s] [--threads n] [--rlist ..]"""
import sys, time, argparse, io, contextlib
sys.path.insert(0, '.')
import gurobipy as gp
from gurobipy import GRB
from kunz_face import face
ap = argparse.ArgumentParser()
ap.add_argument("m", type=int); ap.add_argument("e", type=int); ap.add_argument("obj")
ap.add_argument("--K", type=int, default=30); ap.add_argument("--open", action="store_true")
ap.add_argument("--h3", action="store_true"); ap.add_argument("--dense", action="store_true")
ap.add_argument("--tl", type=float, default=300); ap.add_argument("--threads", type=int, default=2)
ap.add_argument("--rlist", default="")
args = ap.parse_args(); m, e = args.m, args.e
if args.dense: assert m > e * e
pairs = [(i, j) for i in range(1, m) for j in range(i, m) if (i + j) % m]
def solve(r):
    M = gp.Model(); M.Params.OutputFlag = 0; M.Params.Threads = args.threads; M.Params.TimeLimit = args.tl
    M.Params.IntFeasTol = 1e-9; M.Params.FeasibilityTol = 1e-9
    k = M.addVars(range(1, m), vtype=GRB.INTEGER, lb=1, ub=args.K)
    t = M.addVars(pairs, vtype=GRB.BINARY)
    to = {s: [] for s in range(1, m)}
    for (i, j) in pairs:
        s = (i + j) % m; expr = k[i] + k[j] + (1 if i + j > m else 0) - k[s]
        M.addConstr(expr >= 0)
        M.addGenConstrIndicator(t[i, j], True, expr, GRB.EQUAL, 0)
        M.addGenConstrIndicator(t[i, j], False, expr, GRB.GREATER_EQUAL, 1)
        to[s].append((i, j))
    g = M.addVars(range(1, m), vtype=GRB.BINARY)
    for s in range(1, m):
        for p in to[s]: M.addConstr(g[s] <= 1 - t[p])
        M.addConstr(g[s] >= 1 - gp.quicksum(t[p] for p in to[s]))
    M.addConstr(gp.quicksum(g.values()) == e - 1)
    for i in range(1, m):
        if i != r: M.addConstr(m * k[r] + r >= m * k[i] + i + 1)
    c = m * k[r] + r - m + 1; rho = m - r - 1
    if args.open:
        assert 3 * e < m; M.addConstr(c >= 4 * m + 1)
    if args.h3:
        # h_s >= max factorization length of w_s (a tight pair forces h_s >= h_i + h_j), capped at 3
        h = M.addVars(range(1, m), vtype=GRB.INTEGER, lb=1, ub=3)
        for (i, j) in pairs: M.addConstr(h[(i + j) % m] >= h[i] + h[j] - 5 * (1 - t[i, j]))
        # some w_s is neither a generator nor a sum of two generators (so the Apery height is exactly 3)
        u = M.addVars(pairs, vtype=GRB.BINARY); N2 = M.addVars(range(1, m), vtype=GRB.BINARY)
        for (i, j) in pairs: M.addConstr(u[i, j] >= t[i, j] + g[i] + g[j] - 2)
        for s in range(1, m):
            for p in to[s]: M.addConstr(N2[s] <= 1 - u[p])
            M.addConstr(N2[s] <= 1 - g[s])
        M.addConstr(gp.quicksum(N2.values()) >= 1)
    if args.obj == 'W':
        M.setObjective((e - 1) * c - e * gp.quicksum(k.values()), GRB.MINIMIZE)
    else:
        y = M.addVars(range(1, m), lb=0, ub=args.K + 2)
        for (i, j) in pairs:
            s = (i + j) % m; eps = 1 if (s - r - 1) % m >= m - rho else 0
            if args.obj == 'TX':   # exact tau from the positions r_x = (x - r - 1) mod m
                rp = lambda x: (x - r - 1) % m
                tau = (rp(i) + rp(j) - rp(s) - rho) // m; assert (rp(i) + rp(j) - rp(s) - rho) % m == 0
                M.addGenConstrIndicator(t[i, j], True, y[i] + y[j] - y[s] - k[r], GRB.EQUAL, tau)
                continue
            M.addGenConstrIndicator(t[i, j], True, y[i] + y[j] - y[s] - k[r], GRB.GREATER_EQUAL, -eps)
            if args.obj in ('RT', 'UA'): M.addGenConstrIndicator(t[i, j], True, y[i] + y[j] - y[s] - k[r], GRB.LESS_EQUAL, 1)
            if args.obj in ('RT2', 'UA2'):   # one-cell upper window: tau = +1 needs r_s <= m - rho - 2
                epsp = 1 if (s - r - 1) % m <= m - rho - 2 else 0
                M.addGenConstrIndicator(t[i, j], True, y[i] + y[j] - y[s] - k[r], GRB.LESS_EQUAL, epsp)
        if args.obj in ('UA', 'UA2'):   # generator levels exact: y_s = mu_s = k_r - k_s - [s > r] when s is a generator
            for s in range(1, m):
                M.addGenConstrIndicator(g[s], True, y[s] - k[r] + k[s], GRB.EQUAL, -(1 if s > r else 0))
        M.setObjective(e * (k[r] + gp.quicksum(y.values())) - k[r] * m + rho, GRB.MINIMIZE)
    t0 = time.time(); M.optimize(); dt = time.time() - t0
    st = {GRB.OPTIMAL: 'OPTIMAL', GRB.INFEASIBLE: 'INFEASIBLE', GRB.TIME_LIMIT: 'TIME_LIMIT'}.get(M.Status, str(M.Status))
    line = "m=%d e=%d r=%d obj=%s %s %.0fs" % (m, e, r, args.obj, st, dt)
    if M.SolCount:
        kv = [0] + [int(round(k[i].X)) for i in range(1, m)]
        G = [m] + [m * kv[s] + s for s in range(1, m)]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): W, out = face(G)
        line += " val=%.3f bound=%.3f | verify: %s" % (M.ObjVal, M.ObjBound, buf.getvalue().strip())
        assert out['e'] == e and out['r'] == r, (out['e'], out['r'])
        if args.open: assert out['c'] >= 4 * m + 1
        if args.h3: assert out['h'] == 3
        if args.obj == 'W': assert abs(M.ObjVal - W) < 1e-6, (M.ObjVal, W)
        elif args.obj in out: assert out[args.obj] <= M.ObjVal + 1e-6, (M.ObjVal, out[args.obj])
    print(line, flush=True)
rs = [int(x) for x in args.rlist.split(",")] if args.rlist else list(range(1, m))
for r in rs: solve(r)
