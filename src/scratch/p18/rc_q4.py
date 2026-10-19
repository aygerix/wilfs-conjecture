"""RC and CHAIN-WILF at depth q = 4 with many generators (the c <= 4m residual: e large, alpha >= 6 low gens).
Random S = <m, generators in (m, 4m)> built as: A low gens in (m, 1.5m), others in (1.5m, 2m) and (2m, 4m); keep q == 4.
usage: python rc_q4.py seed trials mlo mhi"""
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
rng = random.Random(int(sys.argv[1])); T = int(sys.argv[2]); mlo, mhi = int(sys.argv[3]), int(sys.argv[4])
st = {}; worst = {}
for _ in range(T):
    m = rng.randint(mlo, mhi)
    alpha = rng.randint(4, 12); a2 = rng.randint(0, 30); hi = rng.randint(0, 30)
    gens = set(rng.randint(m+1, (3*m)//2) for _ in range(alpha)) | set(rng.randint((3*m)//2, 2*m-1) for _ in range(a2)) | set(rng.randint(2*m+1, 4*m) for _ in range(hi))
    gens = sorted(gens)
    if not gens or math.gcd(m, *gens) != 1: continue
    w = apery(m, [m]+gens); ap = set(w); M = max(w); c = M - m + 1; q = -(-c//m)
    if q != 4: continue
    inS = lambda x: x >= 0 and x >= w[x % m]
    n = [x for x in sorted(ap) if x > 0 and not any(inS(y) and inS(x-y) for y in range(m, x-m+1))]  # minimal gens = indecomposable Apery elems
    d = len(n); e = d+1
    if d < 2: continue
    ell = sum(1 for x in range(c) if inS(x)); W = e*ell - c
    need2 = (d-1)*m*(m-1)
    R = sum((M-x) % a for x in w for a in n)
    Bc = 0
    for a in n:
        for x in w:
            t = x
            while t + a in ap: t += a
            Bc += M - t
    alow = sum(1 for x in n if 2*x - m < c - 2*m)   # generators in (m, (c-m)/2)
    acount = sum(1 for x in n if x < c - 2*m)        # generators in (m, c-2m)
    key = ('e>=20' if e >= 20 else 'e<20', 'alpha>=6' if alow >= 6 else 'alpha<6')
    s = st.setdefault(key, [0, 0, 0, 0]); s[0] += 1; s[1] += 2*R >= need2; s[2] += 2*Bc >= need2; s[3] += W < 0
    r1, r2 = 2*R/need2, 2*Bc/need2
    if key not in worst or r1 < worst[key][0]: worst[key] = (round(r1, 3), round(r2, 3), m, e, alow, acount, W, c)
print('q = 4 classes: [count, RC covered, CHAIN covered, Wilf failures]')
for k in sorted(st): print('  ', k, st[k], ' worst RC (RC, CHAIN, m, e, alpha, a, W, c):', worst[k])
