r"""Adversarial random search for small RT among genuine S with residues s_1..s_d mod m and generator levels K_b
(g_b = m K_b + s_b), lead, 2026-10-20.  For each S: W, Apery height h, RT (kunz_face.py), and the large-q slope
lead = min{ e(1 + sum v) - m : v >= 0, v_i + v_j - v_s = 1 on tight pairs }  (RT(q) >= q*lead - K0 for a fixed dual).
Keeps S with e = d+1 and c >= 4m+1.  Prints the NK smallest RT and the smallest RT/W ratios.
usage: /usr/bin/python3 h3rnd.py d MMIN MMAX KLIST NS SEED   (KLIST e.g. 1,2 : levels drawn from it)"""
import sys, random
sys.path.insert(0, '.')
import gurobipy as gp
from gurobipy import GRB
from kunz_face import apery
env = gp.Env(empty=True); env.setParam('OutputFlag', 0); env.setParam('Threads', 1); env.start()
def analyse(G):
    m = min(G); w = apery(m, G); Ws = set(w)
    gens = [s for s in range(1, m) if not any(w[s] - w[i] in Ws and 0 < w[s] - w[i] for i in range(1, m) if w[i] < w[s])]
    e = len(gens) + 1; c = max(w) - m + 1; q = -(-c // m); rho = q * m - c
    mu = [q] + [max(0, -((w[s] - c) // m)) for s in range(1, m)]; rp = [(w[s] - c) % m for s in range(m)]
    W = e * sum(mu) - c
    tight = [(i, j, (i + j) % m) for i in range(1, m) for j in range(i, m) if (i + j) % m and w[i] + w[j] == w[(i + j) % m]]
    hg = [0] * m
    for s in sorted(range(1, m), key=lambda x: w[x]):
        hg[s] = 1 if s in gens else max(hg[i] + hg[j] for (i, j, t) in tight if t == s)
    vals = []
    for mode in ('RT', 'lead'):
        M = gp.Model(env=env); y = M.addVars(range(1, m), lb=0)
        for (i, j, s) in tight:
            if mode == 'RT':
                M.addConstr(y[i] + y[j] - y[s] >= q - (1 if rp[s] >= m - rho else 0)); M.addConstr(y[i] + y[j] - y[s] <= q + 1)
            else: M.addConstr(y[i] + y[j] - y[s] == 1)
        if mode == 'RT': M.setObjective(e * (q + gp.quicksum(y.values())) - q * m + rho, GRB.MINIMIZE)
        else: M.setObjective(e * (1 + gp.quicksum(y.values())) - m, GRB.MINIMIZE)
        M.optimize(); vals.append(M.ObjVal if M.Status == GRB.OPTIMAL else None); M.dispose()
    return dict(m=m, e=e, c=c, q=q, rho=rho, h=max(hg), W=W, RT=vals[0], lead=vals[1], G=sorted(G))
if __name__ == '__main__':
    d, mmin, mmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    KL = [int(t) for t in sys.argv[4].split(',')]; NS, seed = int(sys.argv[5]), int(sys.argv[6])
    rng = random.Random(seed); res = []; tested = 0; neg = 0
    while tested < NS:
        m = rng.randint(mmin, mmax); s = rng.sample(range(1, m), d)
        G = [m] + [m * rng.choice(KL) + x for x in s]
        R = analyse(G)
        if R['e'] != d + 1 or R['c'] < 4 * m + 1: continue
        tested += 1; res.append(R)
        if R['RT'] is not None and R['RT'] < -1e-9:
            neg += 1; print("NEGATIVE RT:", R, flush=True)
    print("tested %d (e=%d, c>4m), RT<0: %d" % (tested, d + 1, neg))
    for R in sorted(res, key=lambda R: R['RT'])[:8]: print("  minRT", R)
    for R in sorted(res, key=lambda R: R['lead'])[:5]: print("  minlead", R)
    hs = {}
    for R in res: hs[R['h']] = hs.get(R['h'], 0) + 1
    print("  heights", sorted(hs.items()))
