# LOW-class probe (lead, 2026-10-20): random S = <m, gens>, Apery by Dijkstra; compute q, rho, Lambda, sumK (true shift),
# and check (i) T1: sumK <= m - e, (ii) LOW: rho + Lambda < m - e (Wilf then not implied by T1). Reports by q.
import random, sys, heapq
def apery(m, gens):
    INF = float('inf'); dist = [INF] * m; dist[0] = 0; pq = [(0, 0)]
    while pq:
        dd, r = heapq.heappop(pq)
        if dd > dist[r]: continue
        for g in gens:
            nr = (r + g) % m; nd = dd + g
            if nd < dist[nr]: dist[nr] = nd; heapq.heappush(pq, (nd, nr))
    return dist
def analyze(m, gens):
    w = apery(m, gens)
    if any(x == float('inf') for x in w): return None
    W = set(w)
    inS = lambda v: v >= 0 and w[v % m] <= v
    P = [g for g in sorted(set(gens)) if g % m and w[g % m] == g and not any(inS(g - h) and 0 < g - h for h in gens if h < g and w[h % m] == h)]
    # minimal generators other than m: Apery elements not sum of two nonzero Apery elements
    Aps = sorted(w)
    P = [x for x in Aps if x and not any(y and x - y > 0 and (x - y) in W and y in W for y in Aps if y < x)]
    d = len(P); e = d + 1
    M = max(w); c = M - m + 1; q = -(-c // m); rho = q * m - c
    lam = lambda v: (M - v) // m
    def nu(a, x):
        k = 0
        while inS(x - (k + 1) * a): k += 1
        return k
    Lam = 0; sumK = 0
    for x in w:
        L1 = 0
        for a in P:
            j = nu(a, x)
            if j: L1 += j * (lam(x - a) - lam(x))
            t = x
            while (t + a) in W: t += a
            Lam += lam(t)
        sumK += q - lam(x) - L1
    ell = sum(lam(x) for x in w)
    Wv = e * ell - c
    assert Wv == rho + Lam - sumK, (m, gens)
    return dict(m=m, e=e, q=q, rho=rho, Lam=Lam, sumK=sumK, W=Wv, P=P)
if __name__ == "__main__":
    random.seed(int(sys.argv[1])); mode = sys.argv[2]; N = int(sys.argv[3])
    stats = {}
    for it in range(N):
        m = random.randint(8, 60)
        if mode == 'p18':
            k = random.randint(2, max(2, m // 4)); B = random.sample(range(1, m), k); gens = [m] + [m + b for b in B]
        elif mode == 'wide':
            k = random.randint(2, 6); gens = [m] + random.sample(range(m + 1, 6 * m), k)
        else:
            k = random.randint(2, 5); gens = [m] + random.sample(range(m + 1, 3 * m), k)
        r = analyze(m, gens)
        if r is None or r['e'] < 3: continue
        q = r['q']; s = stats.setdefault(q, [0, 0, 0, None])
        s[0] += 1
        if r['sumK'] > r['m'] - r['e']: s[1] += 1; print("T1 FAIL", r)
        if r['rho'] + r['Lam'] < r['m'] - r['e']:
            s[2] += 1
            if s[3] is None or r['W'] < s[3]['W']: s[3] = r
    for q in sorted(stats):
        s = stats[q]; print("q=%d: %d S, T1 fails %d, LOW %d, min-W LOW example %s" % (q, s[0], s[1], s[2], s[3]))
