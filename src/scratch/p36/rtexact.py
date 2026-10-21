r"""Exact certification of relaxation values (lead, 2026-10-21).
(1) W recomputed WITHOUT the Apery code: membership of S in [0, N] by dynamic programming over the given generators,
    c = 1 + (largest gap), g = #gaps, e = #minimal generators (nonzero elements of S that are not a sum of two nonzero
    elements of S), W = e(c - g) - c.
(2) For each relaxation (rt2lib definitions), the Gurobi primal y and the dual multipliers are rationalized
    (Fraction.limit_denominator) and checked EXACTLY: primal feasibility and value P, dual feasibility and value D.
    P == D certifies the optimum exactly.  The tau formula tau = [i+j>m] + [s>r] - [i>r] - [j>r] and the type rule
    (r_x < rho  <=>  x > r) are asserted on every tight pair.
usage: /usr/bin/python3 rtexact.py NAME[,NAME..] m g1 g2 ...     (NAME in RT, RT2, RT3, UA, UA2, UA3, TX)"""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, '.')
import gurobipy as gp
from gurobipy import GRB
from rt2lib import data
def indep_W(G):
    m = min(G); N = max(G) * m + m
    inS = [False] * (N + 1); inS[0] = True
    for x in range(1, N + 1): inS[x] = any(x >= g and inS[x - g] for g in G)
    gaps = [x for x in range(N + 1) if not inS[x]]
    assert all(inS[x] for x in range(gaps[-1] + 1, N + 1)) and N - gaps[-1] > m
    c = gaps[-1] + 1; g = len(gaps)
    els = [x for x in range(1, c + m + max(G)) if inS[x]]; Sset = set(els)
    mingens = [x for x in els if x <= max(G) and not any(y in Sset and (x - y) in Sset for y in els if 0 < y < x)]
    e = len(mingens); return e * (c - g) - c, dict(c=c, g=g, e=e, mingens=mingens)
def build(D, name):
    m, e, q, rho, mu, rp = D['m'], D['e'], D['q'], D['rho'], D['mu'], D['rp']
    rows = []   # (coef dict, sense, rhs)
    r = D['w'].index(max(D['w']))
    for (i, j, s) in D['tight']:
        t = (rp[i] + rp[j] - rp[s] - rho) // m
        assert t == (1 if i + j > m else 0) + (1 if s > r else 0) - (1 if i > r else 0) - (1 if j > r else 0)
        for x in (i, j, s): assert (rp[x] < rho) == (x > r)
        cf = {}
        for x, a in ((i, 1), (j, 1), (s, -1)): cf[x] = cf.get(x, 0) + a
        if name == 'TX': rows.append((cf, '=', q + t)); continue
        lo = 1 if rp[s] >= m - rho else 0; up = 1 if (rp[s] <= m - rho - 2 or name in ('RT', 'UA')) else 0
        if name in ('RT3', 'UA3'):
            lo = lo if (rp[i] < rho and rp[j] < rho) else 0; up = up if (rp[i] > rho and rp[j] > rho) else 0
        rows.append((cf, '>', q - lo)); rows.append((cf, '<', q + up))
    if name in ('UA', 'UA2', 'UA3'):
        for g in D['gens']: rows.append(({g: 1}, '=', mu[g]))
    return rows
def certify(D, name):
    m, e, q, rho = D['m'], D['e'], D['q'], D['rho']; rows = build(D, name)
    M = gp.Model(); M.Params.OutputFlag = 0; M.Params.Threads = 1; M.Params.FeasibilityTol = 1e-9; M.Params.OptimalityTol = 1e-9
    y = M.addVars(range(1, m), lb=0); cons = []
    for cf, sn, b in rows:
        ex = gp.quicksum(a * y[x] for x, a in cf.items())
        cons.append(M.addConstr(ex >= b) if sn == '>' else (M.addConstr(ex <= b) if sn == '<' else M.addConstr(ex == b)))
    const = e * q - q * m + rho
    M.setObjective(e * gp.quicksum(y.values()) + const, GRB.MINIMIZE); M.optimize()
    assert M.Status == GRB.OPTIMAL
    Y = {x: Fr(y[x].X).limit_denominator(10000) for x in range(1, m)}
    for x in Y:
        if Y[x] < 0: Y[x] = Fr(0)
    for cf, sn, b in rows:
        v = sum(a * Y[x] for x, a in cf.items())
        assert (v >= b) if sn == '>' else ((v <= b) if sn == '<' else (v == b)), "primal infeasible after rounding"
    P = e * sum(Y.values()) + const
    Pi = [Fr(cn.Pi).limit_denominator(10000) for cn in cons]
    red = {x: Fr(e) for x in range(1, m)}
    Dv = Fr(const)
    for (cf, sn, b), p in zip(rows, Pi):
        if sn == '>': assert p >= 0
        if sn == '<': assert p <= 0
        for x, a in cf.items(): red[x] -= p * a
        Dv += p * b
    assert all(v >= 0 for v in red.values()), "dual infeasible after rounding"
    return P, Dv, M.ObjVal
if __name__ == '__main__':
    names = sys.argv[1].split(','); G = list(map(int, sys.argv[2:]))
    Wi, info = indep_W(G); D = data(G)
    assert Wi == D['W'] and info['e'] == D['e'] and info['c'] == D['c'], (Wi, D['W'], info)
    out = []
    for nm in names:
        P, Dv, f = certify(D, nm)
        out.append("%s=%s%s" % (nm, P, "" if P == Dv else " (NOT CERTIFIED: dual %s)" % Dv))
    print("G=%s m=%d e=%d c=%d g=%d q=%d rho=%d h=%d W=%d (independent) |" % (sorted(G), D['m'], D['e'], info['c'], info['g'],
          D['q'], D['rho'], D['h'], Wi), " ".join(out), flush=True)
