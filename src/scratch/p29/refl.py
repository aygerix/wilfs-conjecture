r"""Reflection matching for DEAD (lead, 2026-10-20).
High gaps: gamma = z - k m, z in Ap carried, 1 <= k <= t(z) (levels o(z) .. x(z)-1).  #high gaps = T_c.
Slots: (u, i, b), u in Ap, lambda(u,b) <= i < L_u (L_u = # left elements in u's class).  #slots = sum_b (ell - Lambda_b).
DEAD <=> #slots >= T_c.  Reflection: for a maximal Apery element M >=_S z (M = f + m, f pseudo-Frobenius), u = M - z,
gamma -> (u, i = o(z) + k - 1, b) [the left element f + o(z) m - gamma] whenever lambda(u, b) <= i.
For symmetric S every b works.  REFL: is there a matching saturating all high gaps (any M, any b)?
Variants: REFL1 = only the M that is largest among maximal elements above z; GOODB = #high gaps with no candidate at all.
usage: refl.py gens... | rnd mlo mhi kmin kmax N seed [p18|hiK]"""
import sys, random, heapq
sys.setrecursionlimit(1000000)
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
    lam = {(u, b): next(j for j in range(m + 1) if (u + (j + 1) * g) not in aps) for u in w for b, g in enumerate(gen)}
    maxi = [u for u in w if all((u + g) not in aps for g in gen)]
    gg = sum(u // m for u in w); W = e * (c - gg) - c
    return dict(m=m, w=w, aps=aps, gen=gen, e=e, o=o, L=L, lam=lam, maxi=maxi, W=W, c=c, q=q, h=h)
def hk(adj, nl):
    match = {}
    def aug(x, seen):
        for y in adj[x]:
            if y in seen: continue
            seen.add(y)
            if y not in match or aug(match[y], seen): match[y] = x; return True
        return False
    return sum(1 for x in range(nl) if aug(x, set()))
def analyse(gens, only_top=False):
    D = build(gens)
    if D is None: return None
    w, aps, gen, e, o, L, lam, maxi, m = (D[k] for k in "w aps gen e o L lam maxi m".split())
    adj = []; nocand = 0; Tc = 0
    for z in w:
        t = z // m - o[z]
        if t <= 0: continue
        Ms = [M for M in maxi if (M - z) in aps]
        if only_top: Ms = [max(Ms)]
        for k in range(1, t + 1):
            i = o[z] + k - 1; lst = []
            for M in Ms:
                u = M - z
                assert i < L[u]
                for b in range(e - 1):
                    if lam[u, b] <= i: lst.append((u, i, b))
            if not lst: nocand += 1
            adj.append(lst); Tc += 1
    mt = hk(adj, len(adj))
    return dict(m=m, e=e, q=D["q"], W=W if (W := D["W"]) is not None else None, Tc=Tc, nocand=nocand, REFL=mt - Tc, sym=(len(maxi) == 1), gens=[m] + gen)
if __name__ == "__main__" and sys.argv[1] != "flow":
    a = sys.argv[1:]
    if a[0] != "rnd":
        print(analyse(list(map(int, a)))); print(analyse(list(map(int, a)), True)); sys.exit()
    mlo, mhi, kmin, kmax, N, seed = map(int, a[1:7]); random.seed(seed); mode = a[7] if len(a) > 7 else "hi4"
    n = 0; bad = bad1 = nc = 0; worst = worst1 = None
    for _ in range(N):
        m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); hi = 2 * m if mode == "p18" else int(mode[2:]) * m
        if hi - m - 1 < k: continue
        gens = [m] + random.sample(range(m + 1, hi), k)
        r = analyse(gens)
        if r is None or r["e"] < 3: continue
        r1 = analyse(gens, True)
        n += 1; bad += r["REFL"] < 0; bad1 += r1["REFL"] < 0; nc += r["nocand"] > 0
        if worst is None or r["REFL"] < worst["REFL"]: worst = r
        if worst1 is None or r1["REFL"] < worst1["REFL"]: worst1 = r1
    print(a, "S", n, "REFL fails", bad, "REFL-top fails", bad1, "S with uncovered high gap", nc)
    print("  worst", worst); print("  worst top", worst1)

class Dinic:
    def __init__(self): self.g = {}
    def add(self, a, b, c):
        self.g.setdefault(a, []); self.g.setdefault(b, [])
        ea = [b, c, None]; eb = [a, 0, ea]; ea[2] = eb; self.g[a].append(ea); self.g[b].append(eb)
    def maxflow(self, s, t):
        if s not in self.g or t not in self.g: return 0
        from collections import deque
        tot = 0
        while True:
            lv = {s: 0}; dq = deque([s])
            while dq:
                x = dq.popleft()
                for e_ in self.g[x]:
                    if e_[1] > 0 and e_[0] not in lv: lv[e_[0]] = lv[x] + 1; dq.append(e_[0])
            if t not in lv: return tot
            it = {x: 0 for x in self.g}
            def dfs(x, f):
                if x == t: return f
                while it[x] < len(self.g[x]):
                    e_ = self.g[x][it[x]]
                    if e_[1] > 0 and lv.get(e_[0], -1) == lv[x] + 1:
                        d = dfs(e_[0], min(f, e_[1]))
                        if d > 0: e_[1] -= d; e_[2][1] += d; return d
                    it[x] += 1
                return 0
            while True:
                f = dfs(s, 10 ** 18)
                if f == 0: break
                tot += f
def flow_test(gens):
    """REFLF: flow from carried z (demand t(z)) to u = M - z (M maximal >= z) with capacity S(u) = sum_b (L_u - lam(u,b))."""
    D = build(gens)
    if D is None: return None
    w, aps, gen, e, o, L, lam, maxi, m = (D[k] for k in "w aps gen e o L lam maxi m".split())
    F = Dinic(); Tc = 0
    for z in w:
        t = z // m - o[z]
        if t <= 0: continue
        Tc += t; F.add("s", ("z", z), t)
        for M in maxi:
            if (M - z) in aps: F.add(("z", z), ("u", M - z), t)
    for u in w:
        cap = sum(L[u] - lam[u, b] for b in range(e - 1))
        if cap > 0: F.add(("u", u), "t", cap)
    if Tc == 0: return dict(m=m, e=e, Tc=0, REFLF=0, W=D["W"], gens=[m] + gen)
    fv = F.maxflow("s", "t")
    return dict(m=m, e=e, q=D["q"], Tc=Tc, REFLF=fv - Tc, W=D["W"], nmax=len(maxi), gens=[m] + gen)
if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "flow":
    mlo, mhi, kmin, kmax, N, seed = map(int, sys.argv[2:8]); random.seed(seed); mode = sys.argv[8] if len(sys.argv) > 8 else "hi4"
    n = bad = 0; worst = None; byq = {}
    for _ in range(N):
        m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); hi = 2 * m if mode == "p18" else int(mode[2:]) * m
        if hi - m - 1 < k: continue
        r = flow_test([m] + random.sample(range(m + 1, hi), k))
        if r is None or r["e"] < 3: continue
        n += 1; bad += r["REFLF"] < 0
        if worst is None or r["REFLF"] < worst["REFLF"]: worst = r
    print(sys.argv[1:], "S", n, "REFLF fails", bad); print("  worst", worst)
