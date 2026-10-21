r"""RT3 at graded height 3 on dense covers (lead, 2026-10-21).  Under H (graded height <= 3) the exact reduction gives
RTx = q*Gcap + rho - e*K_x  (x = 2, 3), Gcap = e(|P| + 2d + 3)/3 - m.  Prints K2, K3, and the TYPE-respecting window fake
FAKE3(d): Delta = pairs p with every factorization a + b HIGH-HIGH, eps+_p = 1, p LOW, and every tight pair (p, c -> z)
with c LOW and z in W_rho; y = 2q/3 (gens), q/3 - [p in Delta] (pairs), 0 (cubics) is RT3-feasible (asserted), so
RT3 <= q*Gcap + rho - e|Delta|.  Also nH = #HIGH generators.
usage: /usr/bin/python3 rt3cov.py KSET NCOV FILE [FILE ..]"""
import sys, re, itertools
sys.path.insert(0, '.')
from rt2lib import data, relax
KS = [int(t) for t in sys.argv[1].split(',')]; NC = int(sys.argv[2])
rows = []
for fn in sys.argv[3:]:
    nc = 0
    for line in open(fn):
        mm = re.match(r'm=(\d+) d=(\d+) s=([0-9,]+)', line)
        if not mm: continue
        nc += 1
        if nc > NC: break
        m, d = int(mm.group(1)), int(mm.group(2)); s = [int(t) for t in mm.group(3).split(',')]
        for K in itertools.product(KS, repeat=d):
            G = [m] + [m * k + x for k, x in zip(K, s)]
            D = data(G); w = D['w']
            if D['e'] != d + 1 or D['c'] < 4 * m + 1: continue
            e, q, rho, rp, T = D['e'], D['q'], D['rho'], D['rp'], D['tight']; gens = set(D['gens'])
            hg = [0] * m; hn = [0] * m
            for x in sorted(range(1, m), key=lambda t: w[t]):
                if x in gens: hg[x] = hn[x] = 1
                else:
                    hg[x] = max(hg[i] + hg[j] for (i, j, t) in T if t == x); hn[x] = min(hn[i] + hn[j] for (i, j, t) in T if t == x)
            if not (max(hg) <= 3 and hg == hn): continue
            LOW = lambda x: rp[x] < rho; HIGH = lambda x: rp[x] > rho
            P = [x for x in range(1, m) if hg[x] == 2]
            Gcap = e * (len(P) + 2 * d + 3) / 3 - m
            Dl = []
            for p in P:
                facs = [(i, j) for (i, j, t) in T if t == p]; ups = [(i, j, z) for (i, j, z) in T if p in (i, j)]
                ok = all(HIGH(i) and HIGH(j) for (i, j) in facs) and rp[p] <= m - rho - 2 and LOW(p)
                ok = ok and all(LOW(j if i == p else i) and rp[z] >= m - rho for (i, j, z) in ups)
                if ok: Dl.append(p)
            Ds = set(Dl); y = [0.0] * m
            for x in range(1, m): y[x] = 2 * q / 3 if hg[x] == 1 else ((q / 3 - (1 if x in Ds else 0)) if hg[x] == 2 else 0.0)
            for (i, j, z) in T:
                v = y[i] + y[j] - y[z]
                lo = (1 if rp[z] >= m - rho else 0) if (LOW(i) and LOW(j)) else 0
                up = (1 if rp[z] <= m - rho - 2 else 0) if (HIGH(i) and HIGH(j)) else 0
                assert q - lo - 1e-9 <= v <= q + up + 1e-9, "FAKE3(d) infeasible"
            fake = q * Gcap + rho - e * len(Dl)
            R = relax(D, ('RT2', 'RT3', 'UA3'))
            import gurobipy as gp
            from gurobipy import GRB
            from rt2lib import env
            Mh = gp.Model(env=env); yh = Mh.addVars(range(1, m), lb=0)
            for (i, j, z) in T:
                lo = (1 if rp[z] >= m - rho else 0) if (LOW(i) and LOW(j)) else 0
                up = (1 if rp[z] <= m - rho - 2 else 0) if (HIGH(i) and HIGH(j)) else 0
                if hg[z] == 2: Mh.addConstr(yh[i] + yh[j] - yh[z] <= q + up)
                else: Mh.addConstr(yh[i] + yh[j] - yh[z] >= q - lo)
            Mh.setObjective(e * (q + gp.quicksum(yh.values())) - q * m + rho, GRB.MINIMIZE); Mh.optimize()
            R['RT3H'] = Mh.ObjVal if Mh.Status == GRB.OPTIMAL else -1e9; Mh.dispose()
            assert R['RT3'] <= fake + 1e-6
            rec = dict(m=m, d=d, K=K, q=q, rho=rho, W=D['W'], P=len(P), Gcap=round(Gcap, 2), nH=sum(1 for g in gens if HIGH(g)),
                       K2=round((q * Gcap + rho - R['RT2']) / e, 3), K3=round((q * Gcap + rho - R['RT3']) / e, 3), nDelta=len(Dl),
                       fake=round(fake, 2), **{k: round(v, 3) for k, v in R.items()})
            rows.append(rec)
            if R['RT3'] < 1e-9: print("NONPOSITIVE RT3", rec, flush=True)
print("graded height-3 S tested:", len(rows))
for key in ('RT2', 'RT3', 'UA3'):
    for r in sorted(rows, key=lambda r: r[key])[:3]: print("min", key, r)
for r in sorted(rows, key=lambda r: r['RT3'] / r['W'])[:3]: print("min RT3/W %.3f" % (r['RT3'] / r['W']), r)
print("RT3H = RT3 on", sum(1 for r in rows if abs(r['RT3H'] - r['RT3']) < 1e-6), "of", len(rows), "; min RT3H", min((r['RT3H'] for r in rows), default=None))
for r in sorted(rows, key=lambda r: r['RT3H'] - r['RT3'])[:3]: print("max gap RT3 - RT3H", r)
print("RT3 = FAKE3(d) on", sum(1 for r in rows if abs(r['RT3'] - r['fake']) < 1e-6), "; nDelta>0 on", sum(1 for r in rows if r['nDelta'] > 0),
      "; max nDelta", max((r['nDelta'] for r in rows), default=0), "; max K3", max((r['K3'] for r in rows), default=0),
      "; max K2", max((r['K2'] for r in rows), default=0))
