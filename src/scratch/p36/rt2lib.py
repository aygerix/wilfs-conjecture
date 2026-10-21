r"""Exact semigroup data and the relaxations RT, RT2, UA, UA2 (kunz_face.py definitions) for search loops (lead, 2026-10-21).
analyse(G) -> dict(m, e, c, q, rho, h, W, RT, RT2, UA, UA2, G).  W is exact (integers); LP values are Gurobi floats.
RT3 (2026-10-21): RT2 plus the one-bit part types: tau = -1 forces both parts LOW (r < rho), tau = +1 forces both parts
HIGH (r > rho) [tau = -1 needs r_i + r_j = r_s + rho - m <= rho - 1; tau = +1 needs r_i + r_j = m + rho + r_s >= m + rho].
UA3 = RT3 + generator levels."""
import sys
sys.path.insert(0, '.')
import gurobipy as gp
from gurobipy import GRB
from kunz_face import apery
env = gp.Env(empty=True); env.setParam('OutputFlag', 0); env.setParam('Threads', 1); env.start()
def data(G):
    m = min(G); w = apery(m, G); Ws = set(w)
    gens = [s for s in range(1, m) if not any(w[s] - w[i] in Ws and 0 < w[s] - w[i] for i in range(1, m) if w[i] < w[s])]
    e = len(gens) + 1; c = max(w) - m + 1; q = -(-c // m); rho = q * m - c
    mu = [q] + [max(0, -((w[s] - c) // m)) for s in range(1, m)]; rp = [(w[s] - c) % m for s in range(m)]
    W = e * sum(mu) - c
    tight = [(i, j, (i + j) % m) for i in range(1, m) for j in range(i, m) if (i + j) % m and w[i] + w[j] == w[(i + j) % m]]
    hg = [0] * m
    for s in sorted(range(1, m), key=lambda x: w[x]):
        hg[s] = 1 if s in gens else max(hg[i] + hg[j] for (i, j, t) in tight if t == s)
    return dict(m=m, e=e, c=c, q=q, rho=rho, W=W, mu=mu, rp=rp, tight=tight, gens=gens, h=max(hg), w=w)
def relax(D, which=('RT', 'RT2', 'UA', 'UA2')):
    m, e, q, rho, mu, rp = D['m'], D['e'], D['q'], D['rho'], D['mu'], D['rp']
    out = {}
    for name in which:
        M = gp.Model(env=env); y = M.addVars(range(1, m), lb=0)
        for (i, j, s) in D['tight']:
            if name == 'TX':
                M.addConstr(y[i] + y[j] - y[s] == q + (rp[i] + rp[j] - rp[s] - rho) // m); continue
            lo = 1 if rp[s] >= m - rho else 0; up = 1 if (rp[s] <= m - rho - 2 or name in ('RT', 'UA')) else 0
            if name in ('RT3', 'UA3'):
                lo = lo if (rp[i] < rho and rp[j] < rho) else 0; up = up if (rp[i] > rho and rp[j] > rho) else 0
            M.addConstr(y[i] + y[j] - y[s] >= q - lo); M.addConstr(y[i] + y[j] - y[s] <= q + up)
        if name in ('UA', 'UA2', 'UA3'):
            for g in D['gens']: M.addConstr(y[g] == mu[g])
        M.setObjective(e * (q + gp.quicksum(y.values())) - q * m + rho, GRB.MINIMIZE); M.optimize()
        out[name] = M.ObjVal if M.Status == GRB.OPTIMAL else None; M.dispose()
    return out
def analyse(G, which=('RT', 'RT2', 'UA', 'UA2')):
    D = data(G); R = relax(D, which)
    return dict(m=D['m'], e=D['e'], c=D['c'], q=D['q'], rho=D['rho'], h=D['h'], W=D['W'], G=sorted(set(G)), **R)
