# famN: probe P1 = e|U cap [0,c_T)| - c_T (= Qa + theta) on the family A = {mu} u ([c, c+mu) minus mu*N) u O
# (O = extra elements), the shape forced when U cap [0,c_T) = {0, mu, 2mu, 3mu}.  Q5 membership is tested exactly
# (level 1, every factorization of every Apery element of length <= 3, max Apery in [5m, 6m)).
import sys, itertools
def q5(m, A):
    d = len(A); G = [m + a for a in A]; INF = 10 ** 9
    w = [INF] * m; w[0] = 0; done = [False] * m; order = []
    for _ in range(m):
        u = min((x for x in range(m) if not done[x]), key=lambda x: w[x])
        if w[u] >= 6 * m: return None
        done[u] = True; order.append(u)
        for g in G:
            v = w[u] + g; t = v % m
            if v < w[t]: w[t] = v
    for i, a in enumerate(A):
        if w[a] != G[i]: return None
    if max(w) < 5 * m: return None
    hmx = {0: 0}
    for x in order[1:]:
        best = -1
        for i, a in enumerate(A):
            t = (x - a) % m
            if w[t] == w[x] - G[i]:
                if t not in hmx: return None
                best = max(best, hmx[t] + 1)
        if best < 0 or best > 3: return None
        hmx[x] = best
    sg = [w[x] - hmx[x] * m for x in range(m)]
    tau = [INF] * m; tau[0] = 0; dn = [False] * m
    for _ in range(m):
        u = min((x for x in range(m) if not dn[x]), key=lambda x: tau[x]); dn[u] = True
        for a in A:
            v = tau[u] + a; t = v % m
            if v < tau[t]: tau[t] = v
    cT = max(tau) - m + 1; e = d + 1
    res = any(sg[x] > tau[x] for x in range(m))
    Ulo = sum(1 for z in range(cT) if z >= sg[z % m])
    c = max(w) - m + 1; g = sum(x // m for x in w); W = e * (c - g) - c
    return dict(res=res, P1=e * Ulo - cT, W=W, cT=cT, Ulo=Ulo, e=e)
worst = None; cnt = 0
for mu in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    for extra in range(0, int(sys.argv[3]) + 1):
        for c in range(4 * mu + 1, 14 * mu):
            N = [x for x in range(c, c + mu) if x % mu]
            for m in range(c + mu, 3 * c + 3 * mu):
                cands = [x for x in range(c + mu, m) if x % mu] if extra else [()]
                for O in (itertools.combinations(cands, extra) if extra else [()]):
                    A = sorted(set([mu] + N + list(O)))
                    if max(A) >= m: continue
                    r = q5(m, A)
                    if not r or not r['res']: continue
                    cnt += 1
                    if worst is None or r['P1'] < worst[0]: worst = (r['P1'], m, A, r)
                    if r['P1'] < 0 or r['W'] < 0: print('NEG', r, m, A, flush=True)
print('residual S in family:', cnt, ' worst P1:', worst)
