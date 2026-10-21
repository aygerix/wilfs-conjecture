r"""Relaxations of Wilf on the Kunz face of a given S, and their LP duals (lead, 2026-10-20).

S has multiplicity m, Apery set w_s = m k_s + s (s = 1..m-1), conductor c = qm - rho, conductor residue r (w_r = max).
Levels mu_s = ceil((c - w_s)/m)^+ = k_r - k_s - [s > r]; positions r_s = <w_s - c> = (s - r - 1) mod m; mu_0 = q.
W = e(q + sum_s mu_s) - qm + rho.  For every pair {i, j} of nonzero residues with i + j != 0 (mod m), s = i + j mod m:
    w_i + w_j = w_s + J m  (J >= 0; J = 0 iff the pair is TIGHT),  hence  mu_i + mu_j - mu_s = q - J + tau_ij,
    tau_ij = (r_i + r_j - r_s - rho)/m in {-1, 0, 1}  (a constant once r is fixed).
Relaxations: minimize the Wilf functional  Wf(y) = e(q + sum_s y_s) - qm + rho  over real y >= 0 with q fixed and
  R    (robust split certificate, = splitlp.py on all tight pairs): tight pairs y_i + y_j - y_s >= q - [r_s >= m - rho];
  RT   R plus the upper side y_i + y_j - y_s <= q + 1 on tight pairs;
  UA   RT plus y_g = mu_g exactly for every minimal generator g (generator sizes);
  AM   UA plus Apery minimality on non-tight pairs: y_i + y_j - y_s <= q - 1 + tau_ij;
  FX   exact face at fixed q: tight pairs y_i + y_j - y_s = q + tau_ij, non-tight <= q - 1 + tau_ij, generators free.
Each value is a lower bound for W (the true mu is feasible), and by LP duality value >= 0 IS a certificate (the dual
multipliers).  The script prints the values, W, and for the weakest relaxation that is >= 0 nothing; for R it prints
the primal optimum y (the fractional 'fake semigroup' obstruction) when R < 0.
Usage: /usr/bin/python3 kunz_face.py m g1 g2 ...  [-v]"""
import sys
import gurobipy as gp
from gurobipy import GRB
def apery(m, G):
    INF = 10**18; w = [INF] * m; w[0] = 0; done = [False] * m
    for _ in range(m):
        u = min((x for x in range(m) if not done[x] and w[x] < INF), key=lambda x: w[x], default=None)
        if u is None: break
        done[u] = True
        for g in G:
            v = w[u] + g
            if v < w[v % m]: w[v % m] = v
    return w
def face(G, verbose=False):
    m = min(G); w = apery(m, G); Ws = set(w)
    gens = [s for s in range(1, m) if not any(w[s] - w[i] in Ws and 0 < w[s] - w[i] for i in range(1, m) if w[i] < w[s])]
    e = len(gens) + 1; c = max(w) - m + 1; r = w.index(max(w)); q = -(-c // m); rho = q * m - c
    k = [x // m for x in w]
    mu = [q] + [max(0, -((w[s] - c) // m)) for s in range(1, m)]
    assert all(mu[s] == k[r] - k[s] - (1 if s > r else 0) for s in range(1, m)) and q == k[r]
    rp = [(w[s] - c) % m for s in range(m)]
    W = e * sum(mu) - c; assert W == e * (c - sum(k)) - c
    pairs = []
    for i in range(1, m):
        for j in range(i, m):
            s = (i + j) % m
            if s == 0: continue
            J = (w[i] + w[j] - w[s]) // m; tau = (rp[i] + rp[j] - rp[s] - rho) // m
            assert (w[i] + w[j] - w[s]) % m == 0 and J >= 0 and (rp[i] + rp[j] - rp[s] - rho) % m == 0
            assert mu[i] + mu[j] - mu[s] == q - J + tau and tau in (-1, 0, 1)
            pairs.append((i, j, s, J, tau))
    out = {}
    for name in ('R', 'RT', 'UA', 'AM', 'FX'):
        M = gp.Model(); M.Params.OutputFlag = 0; M.Params.Threads = 2
        y = M.addVars(range(1, m), lb=0)
        for (i, j, s, J, tau) in pairs:
            lhs = y[i] + y[j] - y[s]
            if J == 0:
                if name == 'FX': M.addConstr(lhs == q + tau)
                else:
                    M.addConstr(lhs >= q - (1 if rp[s] >= m - rho else 0))
                    if name != 'R': M.addConstr(lhs <= q + 1)
            elif name in ('AM', 'FX'): M.addConstr(lhs <= q - 1 + tau)
        if name in ('UA', 'AM'):
            for g in gens: M.addConstr(y[g] == mu[g])
        M.setObjective(e * (q + gp.quicksum(y.values())) - q * m + rho, GRB.MINIMIZE); M.optimize()
        out[name] = M.ObjVal if M.Status == GRB.OPTIMAL else None
        if name == 'R' and verbose and M.Status == GRB.OPTIMAL:
            yv = [round(y[s].X, 3) for s in range(1, m)]
            out['R_y_gens'] = {w[g]: (round(y[g].X, 3), mu[g]) for g in gens}
    hgt = [0] * m   # max factorization length of w_s (longest chain of tight splits)
    for s in sorted(range(1, m), key=lambda x: w[x]):
        hgt[s] = 1 if s in gens else max(hgt[i] + hgt[j] for (i, j, t, J, tau) in pairs if t == s and J == 0)
    out.update(e=e, c=c, r=r, h=max(hgt))
    print("m=%d e=%d c=%d q=%d rho=%d r=%d h=%d W=%d | R=%s RT=%s UA=%s AM=%s FX=%s | gens=%s" % (
        m, e, c, q, rho, r, max(hgt), W,
        *[('%.3f' % out[n]) if out[n] is not None else 'inf' for n in ('R', 'RT', 'UA', 'AM', 'FX')],
        sorted(w[g] for g in gens)), flush=True)
    if verbose and 'R_y_gens' in out: print("   R optimum on generators (y, true mu):", out['R_y_gens'], flush=True)
    return W, out
if __name__ == '__main__':
    a = [t for t in sys.argv[1:] if t != '-v']; face(list(map(int, a)), '-v' in sys.argv)
