r"""Split certificates for Wilf (lead, 2026-10-20).  S, factorization tile D (tile.build), e = d+1, c = q m - rho,
mu_x = ceil((c - w(x))/m)^+, r_x = <w(x) - c>.  For a split s: z = x_1 + ... + x_k (k >= 2, nonzero cells of D),
    sum_i mu_{x_i} = (k-1) q + mu_z + tau_s,   tau_s = (sum_i r_{x_i} - r_z - (k-1) rho)/m >= -floor((r_z + (k-1) rho)/m),
and for ANY weights pi >= 0 (loads L_x = sum_s pi_s mult_s(x), beta_z = sum_{s: z_s = z} pi_s) the exact identity
    W = q Gamma + rho + sum_s pi_s tau_s + sum_{x != 0} (e + beta_x - L_x) mu_x,   Gamma = sum_s (k_s - 1) pi_s - (m - e).
A certificate is pi with L_x <= e + beta_x for every x != 0 (all parts lie below c) and
    T(pi) := q Gamma + rho - sum_s pi_s wloss_s >= 0,   wloss_s = floor((r_z + (k-1) rho)/m)  (worst-case tau),
which gives W >= T >= 0.  This script maximizes T by LP (Gurobi), checks the identity at the optimum, and prints T and W.
-unit: unit-aware certificate (exact unit levels mu_b; overload of a cell x of height >= 2 costs the Kunz bound
ubar_x = (sum_b x_b mu_b - (|x|-1)(q-1))^+; units pay (e - L_b) mu_b exactly); it contains the unit truncation U (pi = 0).
Usage: /usr/bin/python3 splitlp.py [-k3] [-unit] m g1 g2 ...   |   /usr/bin/python3 splitlp.py [-k3] -f FILE (lines 'm g..' or 'gens=[..]')"""
import sys, re, itertools
sys.path.insert(0, '../p34')
from tile import build
import gurobipy as gp
from gurobipy import GRB
def cert(G, K3=False, tag='', UNIT=False):
    m = min(G); res = build(m, G)
    if res is None: return None
    c, gens, M = res; D = list(M); d = len(gens); e = d + 1; Ds = set(D)
    if c <= 0: return None
    w = {x: sum(a * b for a, b in zip(x, gens)) for x in D}
    mu = {x: max(0, -((w[x] - c) // m)) for x in D}; r = {x: (w[x] - c) % m for x in D}
    q = -(-c // m); rho = q * m - c; W = e * sum(mu.values()) - c
    nz = [x for x in D if any(x)]
    sub = lambda z: [x for x in nz if x != z and all(a <= b for a, b in zip(x, z))]
    splits = []
    for z in D:
        if sum(z) < 2: continue
        S1 = sub(z)
        for x in S1:
            y = tuple(b - a for a, b in zip(x, z))
            if x <= y: splits.append((z, (x, y)))
        if K3:
            for x in S1:
                for y in S1:
                    if not (x <= y): continue
                    u = tuple(b - a - t for a, t, b in zip(x, y, z))
                    if min(u) < 0 or not any(u) or not (y <= u) or u not in Ds: continue
                    splits.append((z, (x, y, u)))
    mdl = gp.Model(); mdl.Params.OutputFlag = 0; mdl.Params.Threads = 2
    pi = [mdl.addVar(lb=0) for _ in splits]
    L = {x: gp.LinExpr() for x in nz}; B = {x: gp.LinExpr() for x in nz}
    tau, wl = [], []
    for v, (z, parts) in zip(pi, splits):
        for x in parts: L[x] += v
        B[z] += v; k = len(parts)
        tau.append((sum(r[x] for x in parts) - r[z] - (k - 1) * rho) // m)
        wl.append((r[z] + (k - 1) * rho) // m)
        assert sum(mu[x] for x in parts) == (k - 1) * q + mu[z] + tau[-1] and tau[-1] >= -wl[-1]
    Gam = gp.quicksum((len(p) - 1) * v for v, (z, p) in zip(pi, splits)) - (m - e)
    T = q * Gam + rho - gp.quicksum(wl[i] * pi[i] for i in range(len(splits)))
    if not UNIT:
        for x in nz: mdl.addConstr(L[x] <= e + B[x])
    else:
        # unit-aware: exact unit levels mu_b (generator sizes); a higher cell may be overloaded at the Kunz upper bound
        # ubar_x = (sum_b x_b mu_b - (|x|-1)(q-1))^+ >= mu_x (|x|-ary split into units, tau >= -(|x|-1)).
        for x in nz:
            if sum(x) == 1: T += (e - L[x]) * mu[x]
            else:
                ub = max(0, sum(x[b] * mu[tuple(int(t == b) for t in range(d))] for b in range(d)) - (sum(x) - 1) * (q - 1))
                assert ub >= mu[x]
                o = mdl.addVar(lb=0); mdl.addConstr(L[x] - e - B[x] <= o); T -= ub * o
    mdl.setObjective(T, GRB.MAXIMIZE); mdl.optimize()
    Tv = mdl.ObjVal; Gv = Gam.getValue()
    if UNIT: Tv -= 0  # objective already includes the unit terms
    ident = q * Gv + rho + sum(tau[i] * pi[i].X for i in range(len(splits))) + sum(
        (e + B[x].getValue() - L[x].getValue()) * mu[x] for x in nz)
    assert abs(ident - W) < 1e-6, (G, ident, W)
    h = max(sum(x) for x in D)
    print("%s m=%d d=%d c=%d q=%d rho=%d h=%d W=%d | maxT=%.3f Gamma=%.3f splits=%d %s" % (
        tag, m, d, c, q, rho, h, W, Tv, Gv, len(splits), 'CERT' if Tv >= -1e-9 else 'NOCERT'), flush=True)
    return Tv
if __name__ == '__main__':
    a = sys.argv[1:]; K3 = UNIT = False
    while a[0] in ('-k3', '-unit'):
        if a[0] == '-k3': K3 = True
        else: UNIT = True
        a = a[1:]
    if a[0] == '-f':
        for line in open(a[1]):
            mm = re.search(r'gens=\[([0-9, ]+)\]', line)
            if mm:
                G = [int(t) for t in mm.group(1).split(',')]; mq = re.search(r'm=(\d+)', line); G = [int(mq.group(1))] + G
            elif line.strip() and line.split()[0].isdigit(): G = list(map(int, line.split()))
            else: continue
            cert(G, K3, a[1], UNIT)
    else: cert(list(map(int, a)), K3, '', UNIT)
