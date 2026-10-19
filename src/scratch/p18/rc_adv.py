"""Adversarial search for RC failures (lead): minimize 2R/((d-1)m(m-1)) over semigroups with q >= QMIN.
Moves: perturb one generator by +-1..+-delta, replace a generator, shift all; keep e fixed (minimal generators).
usage: python rc_adv.py seed chains steps e mlo mhi QMIN"""
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
def evaluate(m, gens, QMIN):
    if len(set(gens)) != len(gens) or min(gens) <= m or math.gcd(m, *gens) != 1: return None
    w = apery(m, [m]+gens)
    inS = lambda x: x >= 0 and x >= w[x % m]
    for n in gens:   # minimality
        if n != w[n % m]: return None
        if any(inS(a) and inS(n-a) for a in range(m, n-m+1)): return None
    d = len(gens); M = max(w); c = M - m + 1; q = -(-c//m)
    if q < QMIN: return None
    R = sum((M - x) % a for x in w for a in gens)
    ell = sum(1 for x in range(c) if inS(x)); W = (d+1)*ell - c
    return 2*R/((d-1)*m*(m-1)), W, c, q
rng = random.Random(int(sys.argv[1])); C = int(sys.argv[2]); STEPS = int(sys.argv[3]); e = int(sys.argv[4])
mlo, mhi, QMIN = int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]); d = e-1
best_all = []
for ch in range(C):
    m = rng.randint(mlo, mhi)
    cur = None
    for _ in range(200):
        K = rng.choice([2, 3, 4, 6])
        g = sorted(rng.sample(range(m+1, K*m), d))
        if rng.random() < 0.3:  # arithmetic-like start
            a0 = rng.randint(m+1, 3*m); st = rng.randint(1, 5); g = [a0 + st*i for i in range(d)]
        r = evaluate(m, g, QMIN)
        if r: cur = (r, g); break
    if not cur: continue
    T = 0.05
    for it in range(STEPS):
        g = list(cur[1]); mv = rng.random()
        if mv < 0.6:
            i = rng.randrange(d); g[i] += rng.choice([-1, 1]) * rng.randint(1, max(1, m//10))
        elif mv < 0.8:
            i = rng.randrange(d); g[i] = rng.randint(m+1, 5*m)
        else:
            s = rng.choice([-1, 1]); g = [x + s for x in g]
        g = sorted(g)
        r = evaluate(m, g, QMIN)
        if not r: continue
        if r[0] < cur[0][0] or rng.random() < math.exp(-(r[0]-cur[0][0])/T):
            cur = (r, g)
        T *= 0.995
        if r[0] < 1: best_all.append((round(r[0], 4), m, g, r[1], r[2], r[3]))
    best_all.append((round(cur[0][0], 4), m, cur[1], cur[0][1], cur[0][2], cur[0][3]))
best_all.sort()
seen = set(); out = []
for b in best_all:
    key = (b[1], tuple(b[2]))
    if key in seen: continue
    seen.add(key); out.append(b)
print('e=%d m in [%d,%d] q>=%d: lowest 2R/need (ratio, m, gens, W, c, q):' % (e, mlo, mhi, QMIN))
for b in out[:15]: print('  ', b)
print('failures (ratio<1):', sum(1 for b in out if b[0] < 1))
