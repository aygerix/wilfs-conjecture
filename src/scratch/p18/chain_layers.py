"""Layer decomposition of the CHAIN deficit at q = 4 (lead, 2026-10-19).
contribution(w) = sum_a (s_w - y_{w,a}), s_w = (M-w) mod m, y_{w,a} = M - top_a(w); CHAIN-WILF <=> sum_w contribution(w) <= C(m,2).
Groups w by co-level lambda(w) = floor((M-w)/m) (lambda = 4 only for w = 0 at q = 4) and reports, over random q = 4 semigroups
with many low generators (3e < m), the max of each layer sum / C(m,2) and the max single contribution / C(m,2).
usage: python chain_layers.py seed trials mlo mhi emin emax"""
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
rng = random.Random(int(sys.argv[1])); T = int(sys.argv[2]); mlo, mhi, emin, emax = map(int, sys.argv[3:7])
stat = {}; tot = 0; worst = None
for _ in range(T):
    m = rng.randint(mlo, mhi); k = rng.randint(emin - 1, emax - 1)
    # low generators clustered in (m, 2m) with a spread controlling the depth, plus high fill-in to reach q = 4
    width = rng.randint(max(k, 3), m - 1)
    lo = rng.randint(1, m - width) if m - width >= 1 else 1
    A = sorted(rng.sample(range(m + lo, m + lo + width), min(k, width)))
    if any(w_ is None for w_ in apery(m, [m] + A)): continue
    base = apery(m, [m] + A)
    K = rng.randint(3*m + 1, 4*m)   # conductor target in (3m, 4m]
    w = [0] + [min(base[i], K + ((i - K) % m)) for i in range(1, m)]
    M = max(w); c = M - m + 1; q = -(-c//m)
    if q != 4: continue
    gens = [x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m)]
    d = len(gens); e = d + 1
    if 3*e >= m or e < emin: continue
    tot += 1
    ap = set(w); C2 = m*(m - 1)//2
    lay = [0]*5; mx = [0]*5
    for x in w:
        s = (M - x) % m; lam = (M - x)//m; con = 0
        for g in gens:
            t = x
            while t + g in ap: t += g
            con += s - (M - t)
        lay[lam] += con; mx[lam] = max(mx[lam], con)
    D = sum(lay)
    for L in range(5):
        key = ('layer', L); v = lay[L]/C2
        if key not in stat or v > stat[key][0]: stat[key] = (v, m, e, c)
        key = ('single', L); v = mx[L]/C2
        if key not in stat or v > stat[key][0]: stat[key] = (v, m, e, c)
    key = ('Delta',); v = D/C2
    if key not in stat or v > stat[key][0]: stat[key] = (v, m, e, c, A, K)
    key = ('L1+L2+L3',); v = (lay[1] + lay[2] + lay[3])/C2
    if key not in stat or v > stat[key][0]: stat[key] = (v, m, e, c, A, K)
print('q=4, 3e<m semigroups tested:', tot)
for k_, v in sorted(stat.items(), key=lambda z: str(z[0])): print(k_, round(v[0], 4), v[1:])
