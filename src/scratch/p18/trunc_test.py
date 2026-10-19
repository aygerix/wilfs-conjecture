"""CHAIN-WILF / RC / PACK-W on truncations S = <m, A> u [K, oo) (lead, 2026-10-19).
T_{m,q} is A = {} with K = qm (CHAIN equality). Random A of size k, K in [4m, 9m]; reports the minimum CHAIN ratio
2B_chain/((d-1)m(m-1)) over q >= 4, split by 3e < m, and the maximum PW/C2.
usage: python trunc_test.py seed trials mlo mhi kmax"""
import sys, heapq, random
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
def analyse(m, w):
    M = max(w); c = M - m + 1; q = -(-c//m)
    pos = {x: i for i, x in enumerate(w)}
    gens = [x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m)]
    d = len(gens)
    if d < 2: return None
    ap = set(w); Bc = 0; R = 0; cw = [0]*m
    for g in gens:
        for i, x in enumerate(w):
            t = x
            while t + g in ap: t += g
            Bc += M - t; R += (M - x) % g; cw[i] += (M - x) % m - (M - t)
    need2 = (d - 1)*m*(m - 1); C2 = m*(m - 1)//2
    ell = sum((c - 1 - x)//m + 1 for x in w if x < c); W = (d + 1)*ell - c
    PW = sum(v for v in cw if v > 0)
    return dict(e=d+1, c=c, q=q, W=W, chain=2*Bc/need2, rc=2*R/need2, pw=PW/C2, pw0=sum(v for v in cw[1:] if v > 0)/C2)
rng = random.Random(int(sys.argv[1])); T = int(sys.argv[2]); mlo, mhi, kmax = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
best = {}; nfail = 0; tot = 0
for _ in range(T):
    m = rng.randint(mlo, mhi); k = rng.randint(1, kmax)
    span = rng.choice([2, 3, 4, 6])
    A = sorted(rng.sample(range(m + 1, span*m), k))
    base = apery(m, [m] + A)
    K = rng.randint(4*m, 9*m)
    w = [0] + [min(base[i] if base[i] is not None else 10**9, K + ((i - K) % m)) for i in range(1, m)]
    r = analyse(m, w)
    if not r or r['q'] < 4: continue
    tot += 1
    cls = '3e<m' if 3*r['e'] < m else '3e>=m'
    key = (cls,)
    if r['chain'] < 1 - 1e-12:
        nfail += 1; print('CHAINFAIL', m, A, K, r)
    if key not in best or r['chain'] < best[key][0]: best[key] = (r['chain'], m, A, K, r)
    k2 = (cls, 'pw')
    if k2 not in best or r['pw'] > best[k2][0]: best[k2] = (r['pw'], m, A, K, r)
print('tested (q>=4):', tot, 'CHAIN failures:', nfail)
for k_, v in sorted(best.items()): print(k_, round(v[0], 4), 'm=%d A=%s K=%d' % (v[1], v[2], v[3]), {x: (round(y, 4) if isinstance(y, float) else y) for x, y in v[4].items()})
