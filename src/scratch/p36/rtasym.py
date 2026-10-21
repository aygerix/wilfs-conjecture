r"""Asymptotics of RT in q (lead, 2026-10-20).  With the tight graph, rho and the window eps of S fixed, the RT dual
    RT(q) = max { q*Gamma(pi) + rho - sum lam*eps - sum nu :  lam, nu >= 0 dual-feasible },  pi = lam - nu,
    Gamma = sum pi - (m - e),  dual-feasible: for every residue x != 0,  sum_p pi_p (mult of x in parts of p) - sum_{p -> x} pi_p <= e,
is convex piecewise linear in q with final slope lead = max Gamma.  Lexicographically: lead = max Gamma, then
K_inf = min {sum lam*eps + sum nu - rho : Gamma = lead}.  Then RT(q') >= q'*lead - K_inf for EVERY q' (the dual point is
q-independent), so RT >= 0 at the actual q whenever q >= K_inf/lead.  Prints q, lead, K_inf, K_inf/lead, RT(q), W.
usage: /usr/bin/python3 rtasym.py m g1 g2 ...   |   -f FILE (lines with 'G': [...] or gens lists)"""
import sys, re, ast
sys.path.insert(0, '.')
import gurobipy as gp
from gurobipy import GRB
from kunz_face import apery
env = gp.Env(empty=True); env.setParam('OutputFlag', 0); env.setParam('Threads', 1); env.start()
def asym(G):
    m = min(G); w = apery(m, G); Ws = set(w)
    gens = [s for s in range(1, m) if not any(w[s] - w[i] in Ws and 0 < w[s] - w[i] for i in range(1, m) if w[i] < w[s])]
    e = len(gens) + 1; c = max(w) - m + 1; q = -(-c // m); rho = q * m - c
    mu = [q] + [max(0, -((w[s] - c) // m)) for s in range(1, m)]; rp = [(w[s] - c) % m for s in range(m)]
    W = e * sum(mu) - c; eps = [1 if rp[s] >= m - rho else 0 for s in range(m)]
    tight = [(i, j, (i + j) % m) for i in range(1, m) for j in range(i, m) if (i + j) % m and w[i] + w[j] == w[(i + j) % m]]
    M = gp.Model(env=env)
    lam = M.addVars(len(tight), lb=0); nu = M.addVars(len(tight), lb=0)
    load = {x: gp.LinExpr() for x in range(1, m)}
    for k, (i, j, s) in enumerate(tight):
        load[i] += lam[k] - nu[k]; load[j] += lam[k] - nu[k]; load[s] -= lam[k] - nu[k]
    for x in range(1, m): M.addConstr(load[x] <= e)
    Gam = gp.quicksum(lam[k] - nu[k] for k in range(len(tight))) - (m - e)
    cost = gp.quicksum(lam[k] * eps[s] + nu[k] for k, (i, j, s) in enumerate(tight)) - rho
    M.setObjective(Gam, GRB.MAXIMIZE); M.optimize(); lead = M.ObjVal
    M.addConstr(Gam >= lead - 1e-9); M.setObjective(cost, GRB.MINIMIZE); M.optimize(); K = M.ObjVal
    M.remove(M.getConstrs()[-1]); M.setObjective(q * Gam - cost, GRB.MAXIMIZE); M.optimize(); RTq = M.ObjVal
    return dict(m=m, e=e, c=c, q=q, rho=rho, W=W, RT=round(RTq, 4), lead=round(lead, 4), Kinf=round(K, 4),
                ratio=round(K / lead, 3) if lead > 1e-9 else None, G=sorted(G))
if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == '-f':
        for line in open(a[1]):
            mm = re.search(r"'G': (\[[0-9, ]+\])", line) or re.search(r'gens=(\[[0-9, ]+\])', line)
            if not mm: continue
            G = ast.literal_eval(mm.group(1))
            mq = re.search(r'^m=(\d+)', line)
            if mq and int(mq.group(1)) not in G: G = [int(mq.group(1))] + G
            print(asym(G), flush=True)
    else: print(asym(list(map(int, a))))
