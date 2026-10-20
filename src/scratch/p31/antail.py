r"""Annealer against TAIL := (e-1)L - G - 3*D4 >= 0 for P18 S = <m, m+B> at depth >= 5 (c > 4m), e >= 3
(lead, 2026-10-20).  L = |S n [3m, c)|, G = #([3m, c) \ S), D4 = #{residues of Kunz level >= 4}.  W = Q3 + TAIL.
OBJ: TAIL (raw) or TAILr = TAIL / (e*L + 1).  usage: antail.py OBJ seed mlo mhi kmin kmax iters restarts"""
import sys, random, math, heapq
obj = sys.argv[1]; seed, mlo, mhi, kmin, kmax, iters, restarts = map(int, sys.argv[2:9]); random.seed(seed)
def ev(m, B):
    if len(set(B)) != len(B) or min(B) < 1 or max(B) >= m or len(B) < 2: return None, 1e9
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in B:
            v = d0 + m + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None, 1e9
    c = max(w) - m + 1
    if c <= 4 * m: return None, 1e9
    e = len(B) + 1; lv = [x // m for x in w]
    L = sum(1 for x in range(3 * m, c) if w[x % m] <= x); Gp = (c - 3 * m) - L
    D4 = sum(1 for l in lv if l >= 4); tail = (e - 1) * L - Gp - 3 * D4
    W = e * (c - sum(lv)) - c
    d = dict(m=m, B=tuple(sorted(B)), e=e, c=c, depth=-(-c // m), W=W, TAIL=tail, L=L, G=Gp, D4=D4)
    return d, (tail / (e * L + 1) if obj == "TAILr" else tail)
best = 1e9
for rs in range(restarts):
    m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); cur = None
    for _ in range(4000):
        B = random.sample(range(1, m), k); d, v = ev(m, B)
        if d: cur = (v, m, sorted(B), d); break
    if not cur: continue
    T0 = 3.0 if obj == "TAIL" else 0.3
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.005
        v0, m0, B0, d0 = cur; m1, B1 = m0, list(B0); mv = random.random()
        if mv < 0.6: i = random.randrange(len(B1)); B1[i] = max(1, min(m1 - 1, B1[i] + random.choice([-3, -2, -1, 1, 2, 3])))
        elif mv < 0.75: i = random.randrange(len(B1)); B1[i] = random.randint(1, m1 - 1)
        elif mv < 0.85 and len(B1) < kmax: B1.append(random.randint(1, m1 - 1))
        elif mv < 0.92 and len(B1) > kmin: B1.pop(random.randrange(len(B1)))
        else: m1 = max(mlo, min(mhi, m0 + random.choice([-2, -1, 1, 2]))); B1 = [min(b, m1 - 1) for b in B1]
        d1, v1 = ev(m1, B1)
        if d1 is None: continue
        if v1 <= v0 or random.random() < math.exp(-(v1 - v0) / T):
            cur = (v1, m1, sorted(B1), d1)
            if v1 < best:
                best = v1; print("best", round(v1, 4), d1, flush=True)
print("final best", best)
