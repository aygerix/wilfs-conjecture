r"""Local refinements of DEAD (lead, 2026-10-20).  S_b = ell - Lambda_b = sum_u s(u,b), s(u,b) = L_u - lambda(u,b) >= 0,
L_u = #left elements in u's residue class, lambda(u,b) = max{j: u + j g_b in Ap}.  DEAD: sum_b S_b >= T_c.
Candidates:  PERB  (e-1) min_b S_b >= T_c;   CHAIN  per b-chain C=(u_0..u_L): sum s(u_i,b) >= sum (t(u_i) - t(u_0));
BASE  sum_b sum_z t(base_b z) <= (e-2) T_c, base_b z = z - mu_b(z) g_b  (CHAIN + BASE => DEAD).
usage: deadloc.py rnd mlo mhi kmin kmax N seed [p18|hiK] | gens..."""
import sys, random, heapq
def build(gens):
    m = min(gens); G = sorted(set(gens))
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in G:
            if x == m: continue
            v = d0 + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    c = max(w) - m + 1
    if c <= m: return None
    aps = set(w); srt = sorted(w)
    gen = [v for v in srt[1:] if not any((v - u) in aps for u in srt[1:] if u < v and (v - u) in aps)]
    e = len(gen) + 1
    o = {0: 0}
    for v in srt[1:]: o[v] = max(o[v - g] + 1 for g in gen if (v - g) in aps)
    q = -(-c // m); h = c - (q - 1) * m
    L = {u: (q if u % m < h else q - 1) - u // m for u in w}
    t = {u: u // m - o[u] for u in w}
    lam = {}; mu = {}
    for u in w:
        for b, g in enumerate(gen):
            j = 0
            while (u + (j + 1) * g) in aps: j += 1
            lam[u, b] = j
            j = 0
            while (u - (j + 1) * g) in aps: j += 1
            mu[u, b] = j
    gg = sum(u // m for u in w); W = e * (c - gg) - c
    return dict(m=m, w=w, gen=gen, e=e, o=o, L=L, t=t, lam=lam, mu=mu, W=W, c=c, q=q, h=h)
def analyse(gens):
    D = build(gens)
    if D is None: return None
    w, gen, e, L, t, lam, mu, W = (D[k] for k in "w gen e L t lam mu W".split())
    Tc = sum(t.values())
    Sb = [sum(L[u] - lam[u, b] for u in w) for b in range(e - 1)]
    assert min(L[u] - lam[u, b] for u in w for b in range(e - 1)) >= 0
    chain_min = 0
    for b, g in enumerate(gen):
        for u0 in w:
            if mu[u0, b] != 0: continue
            ch = [u0 + i * g for i in range(lam[u0, b] + 1)]
            sl = sum(L[u] - lam[u, b] for u in ch) - sum(t[u] - t[u0] for u in ch)
            chain_min = min(chain_min, sl)
    base = sum(t[z - mu[z, b] * gen[b]] for z in w for b in range(e - 1))
    return dict(m=D["m"], e=e, q=D["q"], W=W, Tc=Tc, DEAD=sum(Sb) - Tc, PERB=(e - 1) * min(Sb) - Tc, CHAIN=chain_min,
                BASE=(e - 2) * Tc - base, gens=[D["m"]] + gen)
if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] != "rnd": print(analyse(list(map(int, a)))); sys.exit()
    mlo, mhi, kmin, kmax, N, seed = map(int, a[1:7]); random.seed(seed); mode = a[7] if len(a) > 7 else "hi4"
    keys = ["DEAD", "PERB", "CHAIN", "BASE"]; bad = {k: 0 for k in keys}; worst = {}; n = 0
    for _ in range(N):
        m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); hi = 2 * m if mode == "p18" else int(mode[2:]) * m
        if hi - m - 1 < k: continue
        r = analyse([m] + random.sample(range(m + 1, hi), k))
        if r is None or r["e"] < 3: continue
        n += 1
        for kk in keys:
            bad[kk] += r[kk] < 0
            if kk not in worst or r[kk] < worst[kk][kk]: worst[kk] = r
    print(a, "S", n, "fails", bad)
    for kk in keys: print("  worst", kk, worst[kk])
