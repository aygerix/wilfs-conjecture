"""Per-generator structure of RC at q = 4: Term_a = R_a - m(m-1)/2 = m*ell - n_a*Phi_a.
RC <=> sum_a Term_a >= -m(m-1)/2. Test: (i) Term_a >= 0 for all a? (ii) by generator level; (iii) min over S of sum.
usage: python rc_pergen.py seed trials mlo mhi"""
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
cnt = 0; neg = {1: 0, 2: 0, 3: 0, 4: 0}; tot = {1: 0, 2: 0, 3: 0, 4: 0}; worst = {1: (0, None), 2: (0, None), 3: (0, None), 4: (0, None)}
for _ in range(T):
    m = rng.randint(mlo, mhi)
    gens = set(rng.randint(m+1, (3*m)//2) for _ in range(rng.randint(4, 12))) | set(rng.randint((3*m)//2, 2*m-1) for _ in range(rng.randint(0, 25))) | set(rng.randint(2*m+1, 4*m) for _ in range(rng.randint(0, 25)))
    gens = sorted(gens)
    if math.gcd(m, *gens) != 1: continue
    w = apery(m, [m]+gens); ap = set(w); M = max(w); c = M - m + 1; q = -(-c//m)
    if q != 4: continue
    inS = lambda x: x >= 0 and x >= w[x % m]
    n = [x for x in sorted(ap) if x > 0 and not any(inS(y) and inS(x-y) for y in range(m, x-m+1))]
    e = len(n) + 1
    if e < 20 or 3*e >= m: continue
    cnt += 1
    ell = sum(1 for x in range(c) if inS(x))
    for a in n:
        lev = a // m
        Phi = sum((M - x)//a for x in w)
        Ta = m*ell - a*Phi
        tot[lev] += 1
        if Ta < 0:
            neg[lev] += 1
            rel = Ta/(m*(m-1)/2)
            if rel < worst[lev][0]: worst[lev] = (round(rel, 3), (m, a, ell, Phi, e, c))
print('q=4, e>=20, 3e<m: %d semigroups' % cnt)
for lev in (1, 2, 3, 4): print('  level %d generators: %d, Term_a < 0: %d, worst Term_a/(m(m-1)/2): %s' % (lev, tot[lev], neg[lev], worst[lev]))
