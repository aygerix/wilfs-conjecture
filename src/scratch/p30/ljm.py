r"""Local matching test for CARRY-ID at P18 depth four (lead, 2026-10-20).
W = 2*d2el - p - q + slA + slB.  Slack units: unused incidences, unused repeat entries, unused uncarried tokens of
degree four, and 2 units per redundant pair multiset.  Carries: carried pairs (CP) and carried triples (C).
Local edges (a carry may only use slack 'attached' to one of its own representations):
  carried pair u, rep {x <= y}:  entries (x,y), (y,x) [or both copies of x]; incidences (m+u, b) for all b (u < h);
                                 redundancy units of the pair multiset {x,y} when u has >= 2 pair reps.
  carried triple r, rep {x,y,z}: tokens (s, t) for pair sum s < h with third t; incidences (s, b) for each pair value
                                 s of the rep (s in U2 or m + CP_lo) and all b; the six entries (a, a') with a, a' in
                                 the rep; redundancy units of its pair multisets.
Reports instances where the maximum matching (with unit capacities) does not saturate all carries.
usage: exh k mlo mhi | rnd k mlo mhi N seed | list m b..."""
import sys, itertools, random, heapq
sys.setrecursionlimit(100000)
def build(m, B):
    B = sorted(B); k = len(B); e = k + 1
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in B:
            v = d0 + m + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    c = max(w) - m + 1
    if not (3 * m < c <= 4 * m): return None
    h = c - 3 * m; lv = [w[r] // m for r in range(m)]; inB = set(B)
    ps = {}; ts = {}
    for i in range(k):
        for j in range(i, k): ps.setdefault(B[i] + B[j], []).append((B[i], B[j]))
    for i in range(k):
        for j in range(i, k):
            for l in range(j, k): ts.setdefault(B[i] + B[j] + B[l], []).append((B[i], B[j], B[l]))
    S2 = set([0]) | inB | set(s for s in ps if s < m)
    U2 = set(s for s in ps if s < m and s not in inB)
    T = set(t for t in ts if t < m and t not in S2)
    CP = set(s - m for s in ps if s >= m and (s - m) not in S2 and (s - m) not in T)
    fs = set()
    for t in ts:
        if t < m:
            for x in B:
                if t + x < m: fs.add(t + x)
    H4set = set(r for r in range(h) if lv[r] == 4 and r in fs)
    C = set(r for r in range(h) if lv[r] == 4 and r not in fs)
    plo = set(u for u in CP if u < h)
    pool_rows = set(U2) | set(m + u for u in plo)
    # chosen reps and used slots
    usedI = set(); usedD = set()
    for val in list(T) + [m + r for r in C]:
        reps = ts[val]; dist = [t for t in reps if t[0] < t[1] < t[2]]
        x, yy, z = dist[0] if dist else reps[0]
        if x < yy < z: usedI.update([(x + yy, z), (x + z, yy), (yy + z, x)])
        elif x == yy == z: usedI.add((2 * x, x)); usedD.update([(x, x, 0), (x, x, 1)])
        else:
            a2 = x if x == yy else z; o1 = z if x == yy else x
            usedI.update([(2 * a2, o1), (a2 + o1, a2)]); usedD.add((a2, o1, 0))
    # tokens: order-4 elements' used tokens
    order = {}
    for r in range(m):
        if lv[r] <= 3: order[r] = lv[r] if not (lv[r] == 3 and r in CP) else 2
    usedT = set()
    for r in H4set:
        # one fixed 4-representation: find a 4-multiset summing to r
        rep = None
        for t in ts:
            if t < m and (r - t) in inB:
                rep = sorted(list(ts[t][0]) + [r - t]); break
        cnt = {}
        for b in rep: cnt[b] = cnt.get(b, 0) + 1
        for b, a in cnt.items():
            for j in range(1, a + 1): usedT.add((r - j * b, b))
    X_unc = [r for r in range(h) if lv[r] <= 3 and r not in CP]
    unusedI = set((s, b) for s in pool_rows for b in B if (s, b) not in usedI)
    unusedD = set()
    for x in B:
        for z in B:
            if x != z and (x, z, 0) not in usedD: unusedD.add((x, z, 0))
        for cp in (0, 1):
            if (x, x, cp) not in usedD: unusedD.add((x, x, cp))
    unusedT = set((u, b) for u in X_unc for b in B if (u, b) not in usedT)
    # redundancy units: pair multisets beyond the first for each new pair residue, plus pairs landing in S_1/old
    red = []
    seen = {}
    for s, lst in ps.items():
        res = s if s < m else s - m
        new = (s < m and s in U2) or (s >= m and res in CP)
        for idx, pr in enumerate(lst):
            if new and idx == 0 and res not in seen: seen[res] = pr; continue
            red.append((pr, 0)); red.append((pr, 1))
    items = {}
    for it in unusedI: items[("I",) + it] = 1
    for it in unusedD: items[("D",) + it] = 1
    for it in unusedT: items[("T",) + it] = 1
    for it in red: items[("R",) + it] = 1
    W = e * (c - sum(lv)) - c
    assert len(items) - len(CP) - len(C) == W, (m, B, len(items), len(CP), len(C), W)
    # local edges
    adj = {}
    redby = {}
    for (pr, cp) in red: redby.setdefault(pr, []).append(("R", pr, cp))
    for u in CP:
        L = []
        for (x, yy) in ps[u + m]:
            if x < yy: L += [("D", x, yy, 0), ("D", yy, x, 0)]
            else: L += [("D", x, x, 0), ("D", x, x, 1)]
            L += redby.get((x, yy), [])
        if u < h: L += [("I", m + u, b) for b in B]
        for (x, yy) in ps[u + m]:   # summand tokens: sources x, y (if uncarried, < h) and 0, toward x, y
            for a1 in (0, x, yy):
                for b1 in (x, yy): L.append(("T", a1, b1))
        adj[("cp", u)] = [t for t in L if t in items]
    for r in C:
        L = []
        for rep in ts[r + m]:
            x, yy, z = rep
            for (s, t) in ((x + yy, z), (x + z, yy), (yy + z, x)):
                if s < h: L.append(("T", s, t))
                if s in pool_rows: L += [("I", s, b) for b in B]
                pr = tuple(sorted((s - t if False else 0, 0)))
            for a1 in set(rep):
                for a2 in set(rep):
                    if a1 != a2: L.append(("D", a1, a2, 0))
                    else: L += [("D", a1, a1, 0), ("D", a1, a1, 1)]
            for pr in ((x, yy), (x, z), (yy, z)): L += redby.get(pr, [])
            for a1 in (0, x, yy, z):          # summand tokens
                for b1 in (x, yy, z): L.append(("T", a1, b1))
        adj[("c", r)] = [t for t in set(L) if t in items]
    # carry types: A = carried pair with some rep u + y >= h (owns entry (y, x)); C = carried triple with a pair < h
    # (owns the pair token); B = other carried pairs; D = other carried triples.
    fixed = {}
    for u in CP:
        for (x, yy) in ps[u + m]:
            if u + yy >= h:
                fixed[("cp", u)] = ("D", yy, x, 0) if x < yy else ("D", x, x, 0); break
    for r in C:
        for (x, yy, z) in ts[r + m]:
            for (s0, t0) in ((x + yy, z), (x + z, yy), (yy + z, x)):
                if s0 < h and ("c", r) not in fixed: fixed[("c", r)] = ("T", s0, t0)
    for key, it in fixed.items(): assert it in items, (m, B, key, it)
    assert len(set(fixed.values())) == len(fixed)
    return dict(m=m, B=tuple(B), h=h, W=W, p=len(CP), q=len(C), fixed=fixed), adj
def maxmatch(adj):
    match = {}
    def aug(u, seen):
        for v in adj[u]:
            if v in seen: continue
            seen.add(v)
            if v not in match or aug(match[v], seen):
                match[v] = u; return True
        return False
    n = 0
    for u in adj:
        if aug(u, set()): n += 1
    return n
def _main():
    gen = []
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        gen = ((m, B) for m in range(mlo, mhi + 1) for B in itertools.combinations(range(1, m), k))
    elif sys.argv[1] == "rnd":
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        def g():
            for _ in range(N):
                m = random.randint(mlo, mhi); yield m, sorted(random.sample(range(1, m), k))
        gen = g()
    else:
        m = int(sys.argv[2]); B = list(map(int, sys.argv[3:])); gen = [(m, B)]
    n = bad = 0; worst = None
    for m, B in gen:
        out = build(m, B)
        if not out: continue
        info, adj = out; n += 1
        mm = maxmatch(adj); deficit = len(adj) - mm
        if deficit > 0:
            bad += 1
            if worst is None or deficit > worst[0]: worst = (deficit, info)
            if bad <= 8: print("UNSAT", deficit, info, flush=True)
    print(sys.argv[1:], "S:", n, "local-matching failures:", bad, "worst:", worst)
if __name__ == "__main__":
    _main()
