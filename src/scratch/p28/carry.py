r"""Power-token form of Wilf for ANY numerical semigroup (lead, 2026-10-20).
m = multiplicity, Ap = Ap(S,m), level x(w) = w//m, order o(w) = max # minimal generators (m never used), carry t = x - o.
Power token (u, b, k): u in Ap with o(u) < k, b a non-m minimal generator g_b, degree k with 2 <= k <= q-1, or k = q
when r(u) < h.  Its target is u + (k - o(u)) g_b.  An order-k element v (k = q only for r(v) < h) USES the k tokens
(v - j g_b, b, k), j = 1..a_b, of one chosen max-order representation (multiplicities a_b).  U = #unused tokens.
Claims: (1) W = U - e*T_c (exact).  (2) each carried u owns >= (e-1)*t(u) dead tokens, so W >= U_unc - T_c.
Carry Lemma CL: T_c <= U_unc (pessimistic version: every token of an uncarried u that is the first coordinate of a
chosen rep token of ANY target counts as used).
usage: python3 carry.py gens... | rnd mlo mhi kmin kmax N seed [p18]"""
import sys, random, heapq
def analyse(gens):
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
    aps = set(w)
    # minimal generators other than m: elements of Ap that are not a sum of two nonzero Ap elements
    srt = sorted(w)
    gen = [v for v in srt[1:] if not any((v - u) in aps for u in srt[1:] if u < v and (v - u) > 0 and (v - u) in aps)]
    e = len(gen) + 1
    order = {0: 0}; par = {0: None}
    for v in srt[1:]:
        best = -1; bp = None
        for b, g in enumerate(gen):
            u = v - g
            if u >= 0 and u in aps and order[u] + 1 > best: best = order[u] + 1; bp = b
        order[v] = best; par[v] = bp
    q = -(-c // m); h = c - (q - 1) * m
    g_ = sum(v // m for v in w); W = e * (c - g_) - c
    car = {v: v // m - order[v] for v in w}
    Tc = sum(car.values())
    def topdeg(v): return q if (v % m) < h else q - 1
    tot = sum((e - 1) * max(0, topdeg(u) - order[u] - (1 if order[u] < 1 else 0) + (0)) for u in w)
    # tokens of u: degrees k with max(2, o(u)+1) <= k <= topdeg(u)
    def ntok(u): return (e - 1) * max(0, topdeg(u) - max(2, order[u] + 1) + 1)
    total = sum(ntok(u) for u in w)
    # used tokens: each v with 2 <= o(v) <= topdeg(v)... v of order k uses k tokens (k = o(v) >= 2; o(v) <= topdeg(v) always)
    used = 0; used_unc = 0
    for v in w:
        k = order[v]
        if k < 2: continue
        # chosen rep: follow parent pointers to get multiset
        mult = {}; x = v
        while x != 0:
            b = par[x]; mult[b] = mult.get(b, 0) + 1; x = x - gen[b]
        for b, a in mult.items():
            for j in range(1, a + 1):
                u = v - j * gen[b]
                used += 1
                if car[u] == 0: used_unc += 1
    U = total - used
    tot_unc = sum(ntok(u) for u in w if car[u] == 0)
    Uunc = tot_unc - used_unc
    # per-degree split of U_unc
    Ud = {}
    def degs(u): return range(max(2, order[u] + 1), topdeg(u) + 1)
    for u in w:
        if car[u] == 0:
            for kk in degs(u): Ud[kk] = Ud.get(kk, 0) + (e - 1)
    for v in w:
        k = order[v]
        if k < 2: continue
        mult = {}; x = v
        while x != 0:
            b = par[x]; mult[b] = mult.get(b, 0) + 1; x = x - gen[b]
        for b, a in mult.items():
            for j in range(1, a + 1):
                if car[v - j * gen[b]] == 0: Ud[k] -= 1
    ncar = {}
    for v in w:
        if car[v] > 0: ncar[order[v]] = ncar.get(order[v], 0) + car[v]
    own = sum((e - 1) * car[u] for u in w)
    return dict(m=m, e=e, c=c, q=q, h=h, W=W, U=U, Tc=Tc, Uunc=Uunc, CL=Uunc - Tc, idok=(W == U - e * Tc), ownok=(U - Uunc >= own), gens=[m] + gen,
                Ud=dict(sorted(Ud.items())), ncar=dict(sorted(ncar.items())))
if __name__ == "__main__":
    if sys.argv[1] != "rnd":
        print(analyse(list(map(int, sys.argv[1:]))))
    else:
        mlo, mhi, kmin, kmax, N, seed = map(int, sys.argv[2:8]); p18 = len(sys.argv) > 8; random.seed(seed)
        n = 0; idbad = ownbad = clbad = 0; mn = None; byq = {}
        for _ in range(N):
            m = random.randint(mlo, mhi); k = random.randint(kmin, kmax)
            hi = 2 * m if p18 else 4 * m
            gens = [m] + random.sample(range(m + 1, hi), k)
            r = analyse(gens)
            if r is None: continue
            n += 1; idbad += not r["idok"]; ownbad += not r["ownok"]; clbad += r["CL"] < 0
            if mn is None or r["CL"] < mn["CL"]: mn = r
            s = byq.setdefault(r["q"], [0, 0, 10**9]); s[0] += 1; s[1] += r["CL"] < 0; s[2] = min(s[2], r["CL"])
        print(sys.argv[1:], "S", n, "identity fails", idbad, "own-token fails", ownbad, "CL fails", clbad)
        print("  by depth:", {q: tuple(v) for q, v in sorted(byq.items())})
        print("  min CL", mn)
