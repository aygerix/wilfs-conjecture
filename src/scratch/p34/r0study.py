"""r = 0 study (lead, 2026-10-20): S = <m, Gamma> with every minimal generator < c (no right primitives).
Then the canonical down-set M tiles Z^n by L = ker(phi mod m) and Wilf reads
    Xi_T := n T m - (n+1) sum_M phi  >=  m((n-1)m + n + 1)/2,   T = c + m = max_M phi + 1,
equivalently W = (n+1)k - c >= 0.  Knapsack centroid gives Xi_T >= n m only.
Usage: python r0study.py anneal NR IT SEED MMAX NMIN | python r0study.py eval m g1 .. gn"""
import sys, random, math
def sg(m, G):
    """Apery set of <m, G>; returns (c, Ap list) or None if gcd>1."""
    INF = 10**18; w = [INF] * m; w[0] = 0; done = [False] * m
    for _ in range(m):
        u = min((x for x in range(m) if not done[x] and w[x] < INF), key=lambda x: w[x], default=None)
        if u is None: break
        done[u] = True
        for g in G:
            v = w[u] + g; s = v % m
            if v < w[s]: w[s] = v
    if any(x >= INF for x in w): return None
    return max(w) - m + 1, w
def evalS(m, G):
    G = sorted(set(G))
    if any(g <= m or g % m == 0 for g in G): return None
    R = sg(m, G)
    if R is None: return None
    c, w = R
    if c <= 4 * m: return None
    gens = [x for i, x in enumerate(w) if i and not any(w[a] + w[(i - a) % m] == x for a in range(1, m) if (i - a) % m)]
    if any(x >= c for x in gens): return None     # r = 0 required
    n = len(gens); g = sum(x // m for x in w); ell = c - g
    W = (n + 1) * ell - c
    T = c + m; XiT = n * T * m - (n + 1) * sum(w)
    need = m * ((n - 1) * m + n + 1) / 2
    return W, n, c, g, XiT - need, gens
def anneal(NR, IT, SEED, MMAX, NMIN):
    rnd = random.Random(SEED); best = None
    for rs in range(NR):
        while True:
            m = rnd.randint(max(8, 3 * NMIN), MMAX); n = rnd.randint(NMIN, max(NMIN, min(8, m // 3))); G = sorted(rnd.sample(range(m + 1, 4 * m), n))
            v = evalS(m, G)
            if v is not None and v[1] >= NMIN: break
        cur = (m, v[5]); T = 2.0
        for it in range(IT):
            m, G = cur[0], list(cur[1]); u = rnd.random()
            if u < 0.5: i = rnd.randrange(len(G)); G[i] += rnd.choice([-3, -2, -1, 1, 2, 3, m, -m])
            elif u < 0.6 and len(G) > NMIN: G.pop(rnd.randrange(len(G)))
            elif u < 0.75: G.append(rnd.randint(m + 1, 5 * m))
            else: m += rnd.choice([-2, -1, 1, 2])
            if m < 6 or m > MMAX: continue
            v2 = evalS(m, G)
            if v2 is None or v2[1] < NMIN: continue
            f1, f2 = v[0] / m, v2[0] / m
            if f2 <= f1 or rnd.random() < math.exp((f1 - f2) / T):
                cur, v = (m, v2[5]), v2
                if best is None or f2 < best[0]:
                    best = (f2, v, m); print("best W/m=%.3f W=%d n=%d c=%d g=%d m=%d gens=%s" % (f2, v[0], v[1], v[2], v[3], m, v[5]), flush=True)
            T = max(0.02, T * 0.995)
        if rs % 10 == 0: print("restart", rs, "best", best[0] if best else None, flush=True)
if sys.argv[1] == 'eval':
    a = list(map(int, sys.argv[2:])); print(evalS(a[0], a[1:]))
else:
    anneal(*map(int, sys.argv[2:7]))
