r"""RT obstruction at Apery height <= 3 via explicit primal fakes (lead, 2026-10-21).
Hypothesis H (graded height <= 3): every Apery element is a sum of <= 3 minimal generators and all its factorizations have
the same length h(s), so every tight pair (i, j -> s) has h(i) + h(j) = h(s) (units U, |U| = d; pairs P = height 2;
cubics C = height 3).  Unique factorization is NOT needed; tight pairs need not be splits of a single tile.  Fakes (units / pairs / cubics):
  BASE    y = (2q+1)/3, (q-1)/3, 0          -> RT <= e(q + (2q+1)d/3 + (q-1)|P|/3) - qm + rho = (q-1)Gcap + rho - (m - e^2)
  WINDOW  y = 2q/3, q/3 - delta_p, 0  (q >= 3), delta_p = 1 iff every cubic above p lies in W_rho (or none does)
          -> RT <= e(q + 2qd/3 + sum_p (q/3 - delta_p)) - qm + rho
Both fakes are checked constraint by constraint against RT (and against RT2, which also uses the one-cell upper window
eps+_s = [r_s <= m - rho - 2]: tau = +1 needs r_i + r_j = m + rho + r_s).  LP values R, RT, RT2, UA, UA2 are printed.
usage: /usr/bin/python3 rtobs3.py m g1 g2 ...   |   -cov FILE KSET NCOV"""
import sys, re, itertools
sys.path.insert(0, '.')
import gurobipy as gp
from gurobipy import GRB
from kunz_face import apery
env = gp.Env(empty=True); env.setParam('OutputFlag', 0); env.setParam('Threads', 1); env.start()
def nfact(gens, top):
    F = [0] * (top + 1); F[0] = 1
    for g in gens:
        for x in range(g, top + 1): F[x] += F[x - g]
    return F
def lp(m, e, q, rho, tight, eps, epsp, fix, upper):
    M = gp.Model(env=env); y = M.addVars(range(1, m), lb=0)
    for (i, j, s) in tight:
        M.addConstr(y[i] + y[j] - y[s] >= q - eps[s])
        if upper == 1: M.addConstr(y[i] + y[j] - y[s] <= q + 1)
        elif upper == 2: M.addConstr(y[i] + y[j] - y[s] <= q + epsp[s])
    for g, v in fix.items(): M.addConstr(y[g] == v)
    M.setObjective(e * (q + gp.quicksum(y.values())) - q * m + rho, GRB.MINIMIZE); M.optimize()
    v = M.ObjVal if M.Status == GRB.OPTIMAL else None; M.dispose(); return v
def check(y, tight, q, eps, epsp):
    ok1 = all(q - eps[s] - 1e-9 <= y[i] + y[j] - y[s] <= q + 1 + 1e-9 for (i, j, s) in tight) and min(y[1:]) >= -1e-9
    ok2 = ok1 and all(y[i] + y[j] - y[s] <= q + epsp[s] + 1e-9 for (i, j, s) in tight)
    return ok1, ok2
def analyse(G, tag=''):
    m = min(G); w = apery(m, G); Ws = set(w)
    gens = [s for s in range(1, m) if not any(w[s] - w[i] in Ws and 0 < w[s] - w[i] for i in range(1, m) if w[i] < w[s])]
    e = len(gens) + 1; d = e - 1; c = max(w) - m + 1; q = -(-c // m); rho = q * m - c
    mu = [q] + [max(0, -((w[s] - c) // m)) for s in range(1, m)]; rp = [(w[s] - c) % m for s in range(m)]
    W = e * sum(mu) - c
    tight = [(i, j, (i + j) % m) for i in range(1, m) for j in range(i, m) if (i + j) % m and w[i] + w[j] == w[(i + j) % m]]
    F = nfact([w[g] for g in gens], max(w))
    hg = [0] * m; hn = [0] * m
    for s in sorted(range(1, m), key=lambda x: w[x]):
        hg[s] = 1 if s in gens else max(hg[i] + hg[j] for (i, j, t) in tight if t == s)
        hn[s] = 1 if s in gens else min(hn[i] + hn[j] for (i, j, t) in tight if t == s)
    H = max(hg) <= 3 and hg == hn
    uf = all(F[w[s]] == 1 for s in range(1, m))
    eps = [1 if rp[s] >= m - rho else 0 for s in range(m)]; epsp = [1 if rp[s] <= m - rho - 2 else 0 for s in range(m)]
    vals = {k: lp(m, e, q, rho, tight, eps, epsp, fx, up) for k, fx, up in (
        ('R', {}, 0), ('RT', {}, 1), ('RT2', {}, 2), ('UA', {g: mu[g] for g in gens}, 1), ('UA2', {g: mu[g] for g in gens}, 2))}
    out = dict(m=m, e=e, c=c, q=q, rho=rho, h=max(hg), W=W, H=H, UF=uf, **{k: round(v, 3) if v is not None else None for k, v in vals.items()})
    if H:
        P = [s for s in range(1, m) if hg[s] == 2]; C = [s for s in range(1, m) if hg[s] == 3]
        above = {p: [z for (i, j, z) in tight if hg[z] == 3 and p in (i, j)] for p in P}
        delta = {p: 1 if all(eps[z] for z in above[p]) else 0 for p in P}
        base = e * (q + (2 * q + 1) * d / 3 + (q - 1) * len(P) / 3) - q * m + rho
        Gcap = e * (len(P) + 2 * d + 3) / 3 - m
        assert abs(base - ((q - 1) * Gcap + rho - (m - e * e))) < 1e-6
        yb = [0.0] * m
        for s in range(1, m): yb[s] = (2 * q + 1) / 3 if hg[s] == 1 else ((q - 1) / 3 if hg[s] == 2 else 0.0)
        okb = check(yb, tight, q, eps, epsp)
        assert okb[0], "BASE fake infeasible"
        assert vals['RT'] <= base + 1e-6
        out.update(P=len(P), C=len(C), Gcap=round(Gcap, 3), base=round(base, 3), base_RT2=okb[1])
        if q >= 3:
            yw = [0.0] * m
            for s in range(1, m): yw[s] = 2 * q / 3 if hg[s] == 1 else ((q / 3 - delta[s]) if hg[s] == 2 else 0.0)
            okw = check(yw, tight, q, eps, epsp); assert okw[0], "WINDOW fake infeasible"
            win = e * (q + sum(yw[1:])) - q * m + rho; assert vals['RT'] <= win + 1e-6
            out.update(ndelta=sum(delta.values()), window=round(win, 3), window_RT2=okw[1])
    print(tag, out, flush=True); return out
if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == '-cov':
        KS = [int(t) for t in a[2].split(',')]; NC = int(a[3]); nc = 0
        for line in open(a[1]):
            mm = re.match(r'm=(\d+) d=(\d+) s=([0-9,]+)', line)
            if not mm: continue
            nc += 1
            if nc > NC: break
            m, d = int(mm.group(1)), int(mm.group(2)); s = [int(t) for t in mm.group(3).split(',')]
            for K in itertools.product(KS, repeat=d):
                G = [m] + [m * k + x for k, x in zip(K, s)]
                mm2 = min(G); w = apery(mm2, G); c = max(w) - mm2 + 1
                if c < 4 * m + 1: continue
                analyse(G, 's=%s K=%s' % (s, K))
    else: analyse(list(map(int, a)))
