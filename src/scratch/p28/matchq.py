r"""Matching form of the carry deficit, ANY depth, ANY numerical semigroup (lead, 2026-10-20).
Carried v (carry t(v) >= 1) needs t(v) units beyond its own (e-1)t(v) forced dead tokens.  Supply: unused power tokens with
uncarried first coordinate (capacity 1 each) and spare capacity of carried u: #unused(u) - (e-1) t(u).
Edges: v -> tokens whose first coordinate is a proper sub-sum of v's chosen representation, and -> own spare.
W = U - e T_c guarantees total supply - total demand = W >= 0 iff Wilf; Hall (local) is the stronger claim tested here.
usage: matchq.py rnd mlo mhi kmin kmax N seed [p18|qMAX] [QMAX]"""
import sys, itertools, random, heapq
from collections import defaultdict
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
    g = [v for v in srt[1:] if not any((v - u) in aps for u in srt[1:] if 0 < v - u and u < v)]
    e = len(g) + 1; k = len(g)
    q = -(-c // m); h = c - (q - 1) * m
    order = {0: 0}; par = {0: None}
    for v in srt[1:]:
        best = -1; bp = None
        for i, x in enumerate(g):
            u = v - x
            if u >= 0 and u in aps and order[u] + 1 > best: best = order[u] + 1; bp = i
        order[v] = best; par[v] = bp
    rep = {}
    for v in srt:
        M = []; x = v
        while x != 0: M.append(par[x]); x -= g[par[x]]
        rep[v] = tuple(sorted(M))
    car = {v: v // m - order[v] for v in w}
    top = lambda u: q if u % m < h else q - 1
    pool = set()
    for u in w:
        for i in range(k):
            for kk in range(max(2, order[u] + 1), top(u) + 1): pool.add((u, i, kk))
    used = set()
    for v in w:
        kk = order[v]
        if kk < 2: continue
        cnt = defaultdict(int)
        for i in rep[v]: cnt[i] += 1
        for i, a in cnt.items():
            for j in range(1, a + 1): used.add((v - j * g[i], i, kk))
    unused = pool - used
    W = e * (c - sum(v // m for v in w)) - c
    return dict(m=m, e=e, q=q, h=h, w=w, g=g, rep=rep, car=car, unused=unused, W=W)
QMAX = 10 ** 9
NARROW = False
def test(gens):
    D = build(gens)
    if D is None or D["q"] > QMAX: return None
    w, car, unused, e, g = D["w"], D["car"], D["unused"], D["e"], D["g"]
    carried = [v for v in w if car[v] > 0]
    by_u = defaultdict(list)
    for t in unused: by_u[t[0]].append(t)
    spare = {v: len(by_u[v]) - (e - 1) * car[v] for v in carried}
    if any(s < 0 for s in spare.values()): return dict(err="own-token bound fails", gens=gens)
    adj = {}
    for v in carried:
        M = D["rep"][v]; ss = set([0])
        if NARROW: ss |= set(g[i] for i in M)
        else:
            for r in range(1, len(M)):
                for S in itertools.combinations(M, r): ss.add(sum(g[i] for i in S))
        lst = []
        for u in ss:
            if car.get(u, 0) == 0: lst.extend(by_u[u])
            elif spare.get(u, 0) > 0: lst.append(("spare", u))
        if spare[v] > 0: lst.append(("spare", v))
        adj[v] = lst
    cap = {}
    for v in carried:
        for t in adj[v]: cap[t] = spare[t[1]] if t[0] == "spare" else 1
    # demand t(v): replicate v
    slots = [(v, j) for v in carried for j in range(car[v])]
    matchR = defaultdict(list)
    def aug(sl, seen):
        v = sl[0]
        for t in adj[v]:
            if t in seen: continue
            seen.add(t)
            if len(matchR[t]) < cap[t]: matchR[t].append(sl); return True
            for s2 in list(matchR[t]):
                if aug(s2, seen):
                    matchR[t].remove(s2); matchR[t].append(sl); return True
        return False
    sys.setrecursionlimit(100000)
    ms = sum(1 for sl in slots if aug(sl, set()))
    return dict(m=D["m"], e=e, q=D["q"], h=D["h"], W=D["W"], Tc=len(slots), deficit=len(slots) - ms, gens=[D["m"]] + g)
if __name__ == "__main__":
    mlo, mhi, kmin, kmax, N, seed = map(int, sys.argv[2:8]); p18 = len(sys.argv) > 8 and sys.argv[8] == "p18"; random.seed(seed)
    if "narrow" in sys.argv: NARROW = True
    if len(sys.argv) > 9 and sys.argv[9].isdigit(): QMAX = int(sys.argv[9])
    elif len(sys.argv) > 8 and sys.argv[8].startswith("q"): QMAX = int(sys.argv[8][1:])
    st = {}; worst = None
    for _ in range(N):
        m = random.randint(mlo, mhi); k = random.randint(kmin, kmax)
        gens = [m] + random.sample(range(m + 1, (2 if p18 else 4) * m), k)
        r = test(gens)
        if r is None: continue
        if "err" in r: print(r); continue
        s = st.setdefault(r["q"], [0, 0]); s[0] += 1; s[1] += r["deficit"] > 0
        if r["deficit"] > 0 and (worst is None or r["deficit"] > worst["deficit"]): worst = r
    print(sys.argv[1:], {q: tuple(v) for q, v in sorted(st.items())})
    print("  worst", worst)
