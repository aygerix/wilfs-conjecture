"""Lead's independent check of codex P10 lemmas on actual e=5 lex Apery tiles (own code).
Tile: lexmin factorization of each Apery element (DP lexmin(w) = min_a lexmin(w - n_a) + e_a; a down-set).
Checks (whenever hypotheses hold): HC  mW >= (m+1)H + R - 3m(m-1)/2 ;  BH2 (N4=0); BH3 (N3=N4=0); G3-CONT (N4=0);
AXIS-FACE (N3=N4=0) with f faces; FACE-TYPE; GAUSS/LYM on max D.  Also reports intrinsic-corollary coverage.
usage: python p10_tiles.py seed trials mlo mhi"""
import sys, heapq, random, math
from math import comb
def apery(m, gens):
    w = [None]*m; w[0] = 0; pq = [(0, 0)]
    while pq:
        dd, r = heapq.heappop(pq)
        if dd > w[r]: continue
        for n in gens:
            r2 = (r+n) % m
            if w[r2] is None or dd+n < w[r2]:
                w[r2] = dd+n; heapq.heappush(pq, (dd+n, r2))
    return w
def D2(n, f):
    s, j = 0, 0
    while n > 0:
        cap = f*(j+1); take = min(cap, n); s += take*j; n -= take; j += 1
    return s
def J(q, S):
    if S < 0: return 0
    u, r = divmod(S, q); return q*comb(u, 2) + r*u
def analyse(m, g):
    w = apery(m, [m] + g)
    if any(x is None for x in w): return None
    ap = set(w)
    inS = lambda x: x >= 0 and x >= w[x % m]
    for n in g:
        if n != w[n % m] or any(inS(a) and inS(n - a) for a in range(m, n - m + 1)): return None
    order = sorted(w)
    lex = {0: (0, 0, 0, 0)}
    for x in order[1:]:
        cands = []
        for a in range(4):
            y = x - g[a]
            if y in ap and y in lex:
                f = list(lex[y]); f[a] += 1; cands.append(tuple(f))
        lex[x] = min(cands)
    D = set(lex.values()); assert len(D) == m
    for x in D:   # down-set check
        for a in range(4):
            if x[a] > 0:
                y = list(x); y[a] -= 1; assert tuple(y) in D
    M = max(w); c = M - m + 1
    ell = sum((c - 1 - x)//m + 1 for x in w if x < c); W = 5*ell - c
    deg = lambda x: sum(x)
    up = lambda x, a: tuple(x[i] + (1 if i == a else 0) for i in range(4))
    maxD = [x for x in D if all(up(x, a) not in D for a in range(4))]
    h = {}
    for x in sorted(D, key=deg, reverse=True):
        h[x] = max([0] + [h[up(x, a)] + 1 for a in range(4) if up(x, a) in D])
    def top(x, a):
        while up(x, a) in D: x = up(x, a)
        return x
    H = sum(h[top(x, a)] for x in D for a in range(4))
    wts = sorted([4 + deg(y) for y in maxD], reverse=True)
    R = sum(i*v for i, v in enumerate(wts))
    supp = lambda x: sum(1 for v in x if v > 0)
    N = [0]*5; t = [0]*5
    for x in D: N[supp(x)] += 1
    for y in maxD: t[supp(y)] += 1
    out = dict(m=m, c=c, W=W, q=-(-c//m), N=N, t=t, H=H, R=R)
    out['HC'] = 2*m*W - (2*(m + 1)*H + 2*R - 3*m*(m - 1))   # >= 0
    if N[4] == 0:
        out['BH2'] = 30*H - (60*m - 75*t[1] - 100*t[2] - 180*t[3])
        rho = (1.5*N[3])**(1/3)
        out['G3C'] = H - (N[3]/4*rho - N[3]/2) + 1e-9
        # G3 exact: 3H >= D3(N3;4)
        n3, s, j = N[3], 0, 0
        while n3 > 0:
            cap = 4*comb(j + 2, 2); take = min(cap, n3); s += take*j; n3 -= take; j += 1
        out['G3'] = 3*H - s
    if N[3] == 0 and N[4] == 0:
        out['BH3'] = 4*H - (12*m - 15*t[1] - 24*t[2])
        f = 0; faces = {}
        for x in D:
            if supp(x) == 2: faces.setdefault(tuple(i for i in range(4) if x[i] > 0), []).append(x)
        f = len(faces)
        out['AXF'] = H - (D2(N[2], f) + J(12, 3*N[1] - N[2] - f))
    out['FT2'] = 12*N[2] - (t[2]**2 + 6*t[2])
    out['FT3'] = 6*N[3] - t[3]*(math.sqrt(2*t[3] + 1) + 3) + 1e-9
    out['GAUSS'] = 4*m - sum(4 + deg(y) for y in maxD)
    out['LYM'] = 1 - sum(1/comb(deg(y) + 3, 3) for y in maxD) + 1e-12
    out['sum4'] = sum(g) >= c + m; out['sum3'] = g[0] + g[1] + g[2] >= c + m
    return out
rng = random.Random(int(sys.argv[1])); T = int(sys.argv[2]); mlo, mhi = int(sys.argv[3]), int(sys.argv[4])
N_L = 3; viol = {}; cnt = {}; mins = {}; tot = 0; cov = {'N4=0': 0, 'N3=N4=0': 0, 'sum4': 0, 'sum3': 0}
for it in range(T):
    m = rng.randint(mlo, mhi)
    mode = it % 5
    if mode == 0: g = sorted(rng.sample(range(m + 1, 2*m), 4))
    elif mode == 1: g = sorted(rng.sample(range(m + 1, 4*m), 4))
    elif mode == 2:   # two small, two large (B2-like: big far generators)
        g = sorted(rng.sample(range(m + 1, 2*m), 2) + rng.sample(range(3*m, 8*m), 2))
    elif mode == 3:   # near-progression + outlier
        a0 = rng.randint(m + 1, 3*m); st = rng.randint(1, max(1, m//8)); g = sorted([a0, a0 + st, a0 + 2*st, rng.randint(m + 1, 6*m)])
    else:             # PF adjunction: T = <m,a,b>, S = T u {p1,p2} with p1<p2 pseudo-Frobenius, 2p1 > F(T), p2-p1 notin T
        a_, b_ = sorted(rng.sample(range(m + 1, rng.choice([2, 3, 5])*m), 2))
        if math.gcd(m, a_, b_) != 1: continue
        wt = apery(m, [m, a_, b_]); FT = max(wt) - m
        inT = lambda x: x >= 0 and x >= wt[x % m]
        PF = [x for x in range(1, FT + 1) if not inT(x) and inT(x + m) and inT(x + a_) and inT(x + b_)]
        PF = [p for p in PF if 2*p > FT]
        pairs = [(p, q_) for p in PF for q_ in PF if p < q_ and not inT(q_ - p)]
        if not pairs: continue
        p1, p2 = rng.choice(pairs); g = sorted([a_, b_, p1, p2])
        if it % 10 == 4 and N_L <= 40:   # also the exact codex L-family S_N
            NN = N_L; mm = NN*(NN + 2); m = mm
            g = [2*mm - NN - 1, 2*mm - 1, (4*NN - 4)*mm + 1, (4*NN - 4)*mm + 1 + NN]; N_L += 1
    if len(set(g)) < 4 or math.gcd(m, *g) != 1: continue
    r = analyse(m, g)
    if not r: continue
    tot += 1
    if r['N'][4] == 0: cov['N4=0'] += 1
    if r['N'][3] == 0 and r['N'][4] == 0: cov['N3=N4=0'] += 1
    if r['sum4']: cov['sum4'] += 1
    if r['sum3']: cov['sum3'] += 1
    if r['sum4']: assert r['N'][4] == 0
    if r['sum3']: assert r['N'][3] == 0 and r['N'][4] == 0
    for k in ('HC', 'BH2', 'G3C', 'G3', 'BH3', 'AXF', 'FT2', 'FT3', 'GAUSS', 'LYM'):
        if k in r:
            cnt[k] = cnt.get(k, 0) + 1
            if k not in mins or r[k] < mins[k][0]: mins[k] = (r[k], m, g, r['N'], r['t'], r['H'])
            if r[k] < 0: viol.setdefault(k, []).append((m, g, r))
    if r['W'] < 0: print('WILF FAIL', m, g, r)
print('e=5 semigroups analysed:', tot, ' coverage:', cov)
for k in sorted(cnt): print('%-6s tested %6d  violations %d  min slack %s' % (k, cnt[k], len(viol.get(k, [])), mins[k][:2] + (mins[k][2],)))
for k, v in viol.items(): print('VIOL', k, v[:2])
