# rayU0b: rayU0 with c_T unrestricted (c up to CMAX*mu) and random (Sidon-like) completion order;
# rayU0: explicit construction in the ray case with U' = 0 (T cap [0,c_T) = mu*N).
# A = {mu} u N u O, N = non-multiples of mu in [c, c+mu), O = extra elements chosen to cover the classes mod m.
# For each (mu, c, m) a randomized greedy picks O; every candidate is checked exactly for Q5 membership and
# all W-mu quantities are recomputed from scratch (Qa, Qb, theta, W, Delta3, h, h_lo^mu, h_hi).
import sys, random
INF = 10 ** 9
def apery(m, gens):
    w = [INF] * m; w[0] = 0; done = [False] * m; order = []
    for _ in range(m):
        u = min((x for x in range(m) if not done[x]), key=lambda x: w[x])
        done[u] = True; order.append(u)
        for g in gens:
            v = w[u] + g; t = v % m
            if v < w[t]: w[t] = v
    return w, order
def evalS(m, A):
    A = sorted(A); d = len(A); e = d + 1; G = [m + a for a in A]
    w, order = apery(m, G)
    if max(w) >= INF: return None
    for i, a in enumerate(A):
        if w[a] != G[i]: return None
    if not (5 * m <= max(w) < 6 * m): return None
    hmx = {0: 0}
    for x in order[1:]:
        best = -1
        for i, a in enumerate(A):
            t = (x - a) % m
            if w[t] == w[x] - G[i]: best = max(best, hmx[t] + 1)
        if best > 3: return None
        hmx[x] = best
    sg = [w[x] - hmx[x] * m for x in range(m)]
    tau, _ = apery(m, A)
    mu = A[0]; cT = max(tau) - m + 1
    c = max(w) - m + 1; g = sum(x // m for x in w); W = e * (c - g) - c
    D3 = 3 * (e - 1) * m - e * sum(hmx.values())
    NE = [x for x in range(m) if tau[x] < sg[x]]
    for x in NE: assert sg[x] == tau[x] + m
    T_lt = [z for z in range(cT) if z >= tau[z % m]]
    U_lt = [z for z in range(cT) if z >= sg[z % m]]
    hlo_mu = sum(1 for z in T_lt if z % mu == 0 and z < sg[z % m])
    hlo = len(T_lt) - len(U_lt); hhi = len(NE) - hlo
    Umu = sum(1 for z in U_lt if z % mu == 0); Up = len(U_lt) - Umu
    cU = max(sg) - m + 1; up = sum(1 for z in range(cT, cU) if z >= sg[z % m])
    lmu = -(-cT // mu); th = mu * lmu - cT
    Qa = (e - mu) * Umu + e * Up - mu * hlo_mu; Qb = D3 + (e - 1) * up - hhi
    assert W == Qa + Qb + th, (W, Qa, Qb, th)
    return dict(e=e, mu=mu, m=m, cT=cT, h=len(NE), hlo_mu=hlo_mu, hhi=hhi, Umu=Umu, Up=Up, Qa=Qa, Qb=Qb, th=th, W=W, D3=D3,
                P1=e * len(U_lt) - cT, ratio=(mu * hlo_mu + hhi) / D3 if D3 > 0 else None)
def covered(m, A):
    Ap = [0] + list(A); cov = set()
    for i in range(len(Ap)):
        for j in range(i, len(Ap)):
            for k in range(j, len(Ap)): cov.add((Ap[i] + Ap[j] + Ap[k]) % m)
    return cov
def search(mu, c, m, tries, rng):
    N = [x for x in range(c, c + mu) if x % mu]
    if max(N) >= m: return None
    base = [mu] + N; best = None
    cands = [x for x in range(c, m) if x % mu and x not in N] + [j * mu for j in range(4, m // mu + 1) if c <= j * mu < m]
    for _ in range(tries):
        A = list(base)
        while True:
            unc = m - len(covered(m, A))
            if unc == 0: break
            sc = []
            for b in cands:
                if b in A: continue
                gain = unc - (m - len(covered(m, A + [b])))
                if gain > 0: sc.append((gain + rng.random() * 2, b))
            if not sc: A = None; break
            sc.sort(reverse=True); A.append(sc[rng.randrange(min(KTOP, len(sc)))][1])
        if A is None: continue
        r = evalS(m, A)
        if r and r['h'] > 0 and (best is None or r['P1'] < best[0]['P1']): best = (r, sorted(A))
    return best
rng = random.Random(int(sys.argv[4])); KTOP = int(sys.argv[6]); CMAX = int(sys.argv[5])
for mu in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    bestmu = None
    for c in range(4 * mu + 1, CMAX * mu + 1):
        if (c - 1) % mu == 0: continue
        for m in range(c + mu, 3 * c):
            b = search(mu, c, m, int(sys.argv[3]), rng)
            if b and (bestmu is None or b[0]['P1'] < bestmu[0]['P1']): bestmu = b
            if b and b[0]['P1'] < 0: print('P1<0', b[0], b[1], flush=True)
            if b and b[0]['W'] < 0: print('W<0 !!!', b[0], b[1], flush=True)
        if bestmu: print('  c', c, 'running best P1', bestmu[0]['P1'], 'e', bestmu[0]['e'], 'cT', bestmu[0]['cT'], bestmu[1], flush=True)
    print('mu', mu, 'best', bestmu, flush=True)
