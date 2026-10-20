# Check of the top-residue identity (lead, 2026-10-20):
#   m*((m - e) - sum_x K_p(x)) = E + m*p + e*m*(m-3)/2 - sum_a sum_x res(top_a(x) - p)
# and T1(1) <=> sum_a sum_x (k(top_a x) - k(x)) >= g.  Random semigroups, Apery by Dijkstra.
import random, heapq, sys
def apery(m, gens):
    w = [None]*m; w[0] = 0; h = [(0, 0)]; dist = {0: 0}
    while h:
        d0, i = heapq.heappop(h)
        if dist.get(i) != d0: continue
        for n in gens:
            j = (i + n) % m; nd = d0 + n
            if j not in dist or nd < dist[j]: dist[j] = nd; heapq.heappush(h, (nd, j))
    return [dist.get(i) for i in range(m)]
def Cp(y, p, m): return 0 if y < p else (y - p)//m + 1
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
bad = 0; cnt = 0
for _ in range(3000):
    m = random.randint(3, 40); d = random.randint(1, min(6, m-1))
    gens = random.sample(range(m+1, 4*m), d)
    if len({g % m for g in gens}) < d or any(g % m == 0 for g in gens): continue
    w = apery(m, gens)
    if any(x is None for x in w): continue
    aps = set(w)
    P = [n for n in gens if w[n % m] == n and not any(w[i] + w[(n - i) % m] == n for i in range(1, m) if (n - i) % m)]
    e = len(P) + 1
    order = sorted(range(m), key=lambda i: w[i])
    nu = {n: {} for n in P}
    for n in P:
        for i in order:
            x = w[i]; y = x - n
            nu[n][x] = nu[n][y] + 1 if y in aps and y >= 0 and w[y % m] == y else 0
    top = {n: {} for n in P}
    for n in P:
        for i in sorted(range(m), key=lambda i: -w[i]):
            x = w[i]; y = x + n
            top[n][x] = top[n][y] if y in aps else x
    g = sum(x // m for x in w)
    E = sum(sum(nu[n][x]*n for n in P) - x for x in w)
    for p in range(1, m+1):
        sK = sum(Cp(x, p, m) - sum(nu[n][x]*(Cp(x, p, m) - Cp(x - n, p, m)) for n in P) for x in w)
        rhs = E + m*p + e*m*(m-3)//2*1 if (e*m*(m-3)) % 2 == 0 else None
        lhs = m*((m - e) - sK)
        R = E + m*p + (e*m*(m-3))/2 - sum((top[n][x] - p) % m for n in P for x in w)
        if abs(lhs - R) > 1e-9: bad += 1
        cnt += 1
    t1_1 = sum(top[n][x]//m - x//m for n in P for x in w) >= g
    sK1 = sum(Cp(x, 1, m) - sum(nu[n][x]*(Cp(x, 1, m) - Cp(x - n, 1, m)) for n in P) for x in w)
    if t1_1 != (sK1 <= m - e): bad += 1
print("checks", cnt, "identity failures", bad)
