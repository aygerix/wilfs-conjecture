"""Criterion RC (lead): R := sum_{w in Ap} sum_a ((M - w) mod n_a) >= (d-1) m (m-1)/2  ==> W >= 0.
Proof: CH' gives mW + (d-1)m(m-1)/2 = sum_{(x,a)} (M - v(top_a x)), and M - v(top_a x) >= (M - v(x)) mod n_a.
Also checks the identity CH' (tile-free form: d m M - (d+1) sum Ap = mW + (d-1)m(m-1)/2) and R <= B.
usage: python rc_check.py seed trials dmin dmax Kmax"""
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
    w = apery(m, gens)
    inS = lambda x: x >= 0 and x >= w[x % m]
    res = []
    for n in sorted(set(gens)):
        if n == m or n % m == 0 or n != w[n % m]: continue
        if any(inS(a) and inS(n - a) for a in range(m, n - m + 1) if a != n): continue
        res.append(n)
    return res, w
rng = random.Random(int(sys.argv[1])); T = int(sys.argv[2]); dmin = int(sys.argv[3]); dmax = int(sys.argv[4]); Kmax = int(sys.argv[5])
st = {}; bad = []; worst = {}
for _ in range(T):
    d = rng.randint(dmin, dmax); m = rng.randint(max(d+2, 8), 250)
    gens = sorted(set(rng.randint(m+1, rng.randint(2, Kmax)*m) for _ in range(d)))
    if len(gens) != d or math.gcd(m, *gens) != 1: continue
    n, w = mingens(m, [m]+gens)
    if len(n) != d: continue
    M = max(w); c = M - m + 1
    if c <= 0: continue
    inS = lambda x: x >= 0 and x >= w[x % m]
    ell = sum(1 for x in range(c) if inS(x)); W = (d+1)*ell - c
    B = d*m*M - (d+1)*sum(w)
    if B != m*W + (d-1)*m*(m-1)//2 or ((d-1)*m*(m-1)) % 2: 
        if 2*B != 2*m*W + (d-1)*m*(m-1): bad.append(('CH', m, n))
    R = sum((M - x) % a for x in w for a in n)
    if R > B: bad.append(('R>B', m, n))
    need = (d-1)*m*(m-1)/2
    q = -(-c//m)
    k = (d, 'q<=4' if q <= 4 else 'q>=5')
    st[k] = st.get(k, [0, 0]); st[k][0] += 1
    if R >= need:
        st[k][1] += 1
        if W < 0: bad.append(('RC', m, n, W))
    rr = R/need
    if k not in worst or rr < worst[k][0]: worst[k] = (round(rr, 3), m, n, c, round((d+1)*ell/c, 3))
print('coverage (d, depth): [total, RC-covered]')
for k in sorted(st): print('  ', k, st[k], ' worst R/need:', worst[k])
print('bad:', bad[:10])
