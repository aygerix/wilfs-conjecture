r"""Matching test for the carry deficit at P18 depth four (lead, 2026-10-20).
Each carried Apery element v (carry 1) needs ONE unit beyond its own (e-1) dead tokens.  Supply: unused power tokens with
uncarried first coordinate, plus spare unused tokens of carried elements (beyond e-1 each).
Edges (rule R): v -> token (u, x, k) when u is a proper sub-sum of v's chosen representation (u = 0 allowed); v -> its own spare.
Reports whether a matching saturating all carried elements exists (Hall), and the deficit otherwise.
usage: match4.py exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, heapq
from collections import defaultdict
def build(m, B):
    k = len(B); e = k + 1; g = [m + b for b in B]
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in g:
            v = d0 + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    c = max(w) - m + 1
    if not (3 * m < c <= 4 * m): return None
    h = c - 3 * m; aps = set(w); srt = sorted(w)
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
    top = lambda u: 4 if u % m < h else 3
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
    return dict(m=m, B=B, e=e, h=h, w=w, g=g, order=order, rep=rep, car=car, unused=unused, W=W, k=k)
def subsums(v, M, g):
    out = set([0])
    for r in range(1, len(M)):
        for S in itertools.combinations(M, r): out.add(sum(g[i] for i in S))
    return out
def test(m, B):
    D = build(m, B)
    if D is None: return None
    w, car, unused, e = D["w"], D["car"], D["unused"], D["e"]
    carried = [v for v in w if car[v] > 0]
    by_u = defaultdict(list)
    for t in unused: by_u[t[0]].append(t)
    # supply: uncarried tokens individually; carried u: spare capacity = (#unused(u) - (e-1)) (as tokens 'spare', any of its unused)
    spare = {}
    for v in carried:
        s = len(by_u[v]) - (e - 1) * car[v]
        assert s >= 0, ("own-token bound fails", m, B, v)
        spare[v] = s
    adj = {}
    for v in carried:
        ss = subsums(v, D["rep"][v], D["g"])
        lst = []
        for u in ss:
            if car.get(u, 0) == 0:
                lst.extend(by_u[u])
            elif spare.get(u, 0) > 0:
                lst.append(("spare", u))
        if spare[v] > 0: lst.append(("spare", v))
        adj[v] = lst
    # capacities: tokens 1, ('spare', u) spare[u]
    cap = defaultdict(int)
    for v in carried:
        for t in adj[v]: cap[t] = spare[t[1]] if t[0] == "spare" else 1
    matchR = defaultdict(list)
    def aug(v, seen):
        for t in adj[v]:
            if t in seen: continue
            seen.add(t)
            if len(matchR[t]) < cap[t]: matchR[t].append(v); return True
            for v2 in list(matchR[t]):
                if aug(v2, seen):
                    matchR[t].remove(v2); matchR[t].append(v); return True
        return False
    msize = sum(1 for v in carried if aug(v, set()))
    return dict(m=m, B=tuple(B), e=e, h=D["h"], W=D["W"], Tc=len(carried), matched=msize, deficit=len(carried) - msize)
if __name__ == "__main__":
    recs = []
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                r = test(m, list(B))
                if r: recs.append(r)
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); B = sorted(random.sample(range(1, m), k))
            r = test(m, B)
            if r: recs.append(r)
    bad = [r for r in recs if r["deficit"] > 0]
    print(sys.argv[1:], "S", len(recs), "Hall failures", len(bad), "h>e failures", sum(1 for r in bad if r["h"] > r["e"]))
    for r in sorted(bad, key=lambda r: -r["deficit"])[:5]: print("  ", r)
