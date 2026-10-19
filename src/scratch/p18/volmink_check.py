"""VOL-MINK / VOL-CORNER checks (lead).
For random S (e = d+1 generators): Lambda = M + N (M = max Ap, N = sum of non-m gens), V = Lambda^d/(d! prod n),
mu = m/V, sigma = (1-mu)^(1/d), g(s) = 1/sum_{j=1..d} s^-j.
 (A) corner bound:  B_disc := d m M - (d+1) sum Ap  >=  m*Lambda*g(sigma) - (d-1) m N/2
 (B) Minkowski:     C(2d,d) * lambda0^d / (d! prod n) <= 2^d m, lambda0 = min v off the lex-min tile
 (C) criterion VOL-CORNER: g(sigma)*Lambda >= (d-1)(N+m-1)/2  ==> W >= 0 ; coverage statistics
usage: python volmink_check.py seed trials dmin dmax Kmax"""
import sys, heapq, random, math
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
def mingens(m, gens):
    w = apery(m, gens); ap = set(w)
    res = []
    for n in sorted(set(gens)):
        if n == m or n % m == 0: continue
        if n not in ap: continue
        # n minimal iff not a sum of two nonzero elements of S
        dec = False
        for a in sorted(ap):
            if 0 < a < n and (n - a) >= w[(n - a) % m] and n - a > 0: dec = True; break
        if not dec: res.append(n)
    return res, w
rng = random.Random(int(sys.argv[1])); T = int(sys.argv[2]); dmin = int(sys.argv[3]); dmax = int(sys.argv[4]); Kmax = int(sys.argv[5])
st = {}; bad = []
def bump(k): st[k] = st.get(k, 0)+1
worstA = 1e18; worstB = 0; minK = {}
for _ in range(T):
    d = rng.randint(dmin, dmax); m = rng.randint(max(d+2, 10), 300)
    gens = sorted(set(rng.randint(m+1, Kmax*m) for _ in range(d)))
    if len(gens) != d or math.gcd(m, *gens) != 1: continue
    n, w = mingens(m, [m]+gens)
    if len(n) != d: continue
    M = max(w); c = M - m + 1
    if c <= 0: continue
    bump('S_d%d' % d)
    inS = lambda x: x >= 0 and x >= w[x % m]
    ell = sum(1 for x in range(c) if inS(x)); W = (d+1)*ell - c
    N = sum(n); Lam = M + N
    logV = d*math.log(Lam) - math.lgamma(d+1) - sum(math.log(x) for x in n)
    mu = math.exp(math.log(m) - logV)
    if mu > 1: bad.append(('mu>1', m, n)); continue
    sig = (1-mu)**(1.0/d)
    g = 0.0 if sig == 0 else 1.0/sum(sig**(-j) for j in range(1, d+1))
    Bdisc = d*m*M - (d+1)*sum(w)
    rhsA = m*Lam*g - (d-1)*m*N/2
    worstA = min(worstA, (Bdisc - rhsA)/(m*Lam))
    if Bdisc < rhsA - 1e-6*m*Lam: bad.append(('A', m, n, Bdisc, rhsA))
    # lex-min tile
    order = sorted(range(m), key=lambda r: w[r]); fac = {0: (0,)*d}
    for r in order[1:]:
        best = None
        for i in range(d):
            u = w[r] - n[i]
            if u >= 0 and u in fac:
                y = list(fac[u]); y[i] += 1; y = tuple(y)
                if best is None or y < best: best = y
        fac[w[r]] = best
    Dset = set(fac.values())
    lam0 = min(sum((y[j]+(1 if j == i else 0))*n[j] for j in range(d)) for y in Dset for i in range(d)
               if tuple(y[j]+(1 if j == i else 0) for j in range(d)) not in Dset)
    lhsB = math.comb(2*d, d)*math.exp(d*math.log(lam0) - math.lgamma(d+1) - sum(math.log(x) for x in n))
    worstB = max(worstB, lhsB/(2**d*m))
    if lhsB > 2**d*m*(1+1e-9): bad.append(('B', m, n, lam0))
    crit = g*Lam >= (d-1)*(N+m-1)/2
    if crit:
        bump('VC_d%d' % d)
        if W < 0: bad.append(('C', m, n, W))
    q = -(-c//m)
    key = d
    ratio = Lam/(N+m)
    minK.setdefault(key, []).append((round(ratio,2), round(g,4), q))
print(sorted(st.items()))
print('worst (Bdisc-rhsA)/(m Lam) =', worstA, ' worst Minkowski ratio =', worstB)
print('bad:', bad[:10])
for d_ in sorted(minK):
    L = minK[d_]; L.sort()
    print('d=%d  Lam/(N+m) quantiles' % d_, [L[int(len(L)*f)][0] for f in (0, .25, .5, .75, .99)], ' g quantiles', sorted(x[1] for x in L)[::max(1,len(L)//6)])
