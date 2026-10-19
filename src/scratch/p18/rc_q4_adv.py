"""Annealing for RC (and CHAIN-WILF) failures inside the open c <= 4m residual:
q = 4 (3m < c <= 4m), alpha = #min gens in (m, (c-m)/2) >= 6, a = #min gens in (m, c-2m) >= 19.
State: a set of offsets; S = <m, gens>. Minimize RC ratio 2R/((d-1)m(m-1)).
usage: python rc_q4_adv.py seed chains steps mlo mhi"""
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
def ev(m, gens):
    gens = sorted(set(gens))
    if not gens or min(gens) <= m or math.gcd(m, *gens) != 1: return None
    w = apery(m, [m]+gens); ap = set(w); M = max(w); c = M - m + 1; q = -(-c//m)
    if q != 4: return None
    inS = lambda x: x >= 0 and x >= w[x % m]
    n = [x for x in sorted(ap) if x > 0 and not any(inS(y) and inS(x-y) for y in range(m, x-m+1))]
    alpha = sum(1 for x in n if 2*x < c - m + 0 and x > m)  # x < (c-m)/2
    a = sum(1 for x in n if x < c - 2*m)
    if alpha < 6 or a < 19: return None
    d = len(n); need2 = (d-1)*m*(m-1)
    R = sum((M-x) % g for x in w for g in n)
    Bc = 0
    for g in n:
        for x in w:
            t = x
            while t + g in ap: t += g
            Bc += M - t
    ell = sum(1 for x in range(c) if inS(x)); W = (d+1)*ell - c
    return 2*R/need2, 2*Bc/need2, W, c, d+1, alpha, a, n
rng = random.Random(int(sys.argv[1])); C = int(sys.argv[2]); STEPS = int(sys.argv[3]); mlo, mhi = int(sys.argv[4]), int(sys.argv[5])
res = []
for ch in range(C):
    m = rng.randint(mlo, mhi); cur = None
    for _ in range(400):
        al = rng.randint(6, 14); aa = rng.randint(19 - al, 40)
        g = [rng.randint(m+1, (3*m)//2 - 1) for _ in range(al)] + [rng.randint((3*m)//2, 2*m - 1) for _ in range(aa)]
        g += [rng.randint(2*m+1, 4*m) for _ in range(rng.randint(0, 20))]
        r = ev(m, g)
        if r: cur = (r, sorted(set(g))); break
    if not cur: continue
    T = 0.05
    for it in range(STEPS):
        g = list(cur[1]); mv = rng.random()
        if mv < 0.5:
            i = rng.randrange(len(g)); g[i] += rng.choice([-1, 1]) * rng.randint(1, max(1, m//20))
        elif mv < 0.7: g.append(rng.randint(m+1, 4*m))
        elif mv < 0.85 and len(g) > 20: g.pop(rng.randrange(len(g)))
        else:
            i = rng.randrange(len(g)); g[i] = rng.randint(m+1, 2*m)
        r = ev(m, g)
        if not r: continue
        if r[0] < cur[0][0] or rng.random() < math.exp(-(r[0] - cur[0][0])/T): cur = (r, sorted(set(g)))
        T *= 0.99
    r = cur[0]
    res.append((round(r[0], 4), round(r[1], 4), m, r[4], r[5], r[6], r[2], r[3]))
res.sort()
print('q=4 residual annealing (RC, CHAIN, m, e, alpha, a, W, c):')
for x in res[:12]: print('  ', x)
print('RC failures:', sum(1 for x in res if x[0] < 1), ' CHAIN failures:', sum(1 for x in res if x[1] < 1), ' of', len(res))
