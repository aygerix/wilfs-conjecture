r"""Twin tokens (lead, 2026-10-20).  Any numerical semigroup S, multiplicity m, depth q, c = (q-1)m + h.
Carried v (order d, carry t, chosen rep) has own-dead degrees D(v) = [q-t+1, q] if r(v) < h else [q-t, q-1].
TWIN: for b in supp(v), u = v - g_b, the token (u, b, k), k in D(v), has the same target as (v, b, k), so it is dead.
It is FRESH if k <= top(u) and (u uncarried or k not in D(u)).  A token (u, b, k) determines v = u + g_b, so twins of
distinct v are distinct.  Delta = units (v, k), k in D(v), with no fresh twin.
Reports T_c, Delta (split: cross = all failures out-of-pool, chain = all failures in D(u), mixed), W, and a Hall test
MT: after fixing one fresh twin per covered unit, can every Delta unit be matched to a distinct unused token outside
all Dead(u) and outside the fixed twins, with first coordinate a sub-sum of v's chosen rep (0 and v allowed)?
Also DEAD tests: #pool tokens with target not in Ap (DB) / not an Ap element of order k (DA) vs e*T_c.
usage: twin.py gens... | rnd mlo mhi kmin kmax N seed [p18|hiMULT]"""
import sys, random, heapq, itertools
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
    order = {0: 0}; par = {0: None}
    for v in srt[1:]:
        best = -1; bp = None
        for b, g in enumerate(gen):
            u = v - g
            if u >= 0 and u in aps and order[u] + 1 > best: best = order[u] + 1; bp = b
        order[v] = best; par[v] = bp
    q = -(-c // m); h = c - (q - 1) * m
    gg = sum(v // m for v in w); W = e * (c - gg) - c
    car = {v: v // m - order[v] for v in w}
    rep = {}
    for v in w:
        mult = {}; x = v
        while x != 0:
            b = par[x]; mult[b] = mult.get(b, 0) + 1; x -= gen[b]
        rep[v] = mult
    return dict(m=m, w=w, aps=aps, gen=gen, e=e, order=order, car=car, rep=rep, q=q, h=h, c=c, W=W)
def subsums(mult, gen):
    items = list(mult.items()); out = set()
    for js in itertools.product(*[range(a + 1) for _, a in items]):
        out.add(sum(j * gen[b] for (b, _), j in zip(items, js)))
    return out
def bpm(adj, nl):
    match = {}
    def aug(x, seen):
        for y in adj[x]:
            if y in seen: continue
            seen.add(y)
            if y not in match or aug(match[y], seen): match[y] = x; return True
        return False
    sys.setrecursionlimit(100000)
    return sum(1 for x in range(nl) if aug(x, set()))
def analyse(gens):
    D = build(gens)
    if D is None: return None
    m, w, aps, gen, e, order, car, rep, q, h, W = (D[k] for k in "m w aps gen e order car rep q h W".split())
    top = lambda u: q if u % m < h else q - 1
    def Dg(v):
        t = car[v]
        return range(q - t + 1, q + 1) if v % m < h else range(q - t, q)
    pool = lambda u, k: max(2, order[u] + 1) <= k <= top(u)
    used = set()
    for v in w:
        k = order[v]
        if k < 2: continue
        for b, a in rep[v].items():
            for j in range(1, a + 1): used.add((v - j * gen[b], b, k))
    forced = set((u, b, k) for u in w if car[u] > 0 for k in Dg(u) for b in range(e - 1))
    Tc = sum(car.values()); fixed = set(); delta = []; ncross = nchain = nmix = 0
    for v in w:
        if car[v] == 0: continue
        for k in Dg(v):
            ok = None; reasons = set()
            for b in sorted(rep[v]):
                u = v - gen[b]
                if not pool(u, k): reasons.add("x"); continue
                if car[u] > 0 and k in Dg(u): reasons.add("c"); continue
                ok = (u, b, k); break
            if ok is not None:
                assert ok not in used and ok not in forced; fixed.add(ok)
            else:
                delta.append((v, k))
                if reasons == {"x"}: ncross += 1
                elif reasons == {"c"}: nchain += 1
                else: nmix += 1
    DB = DA = 0
    for u in w:
        for k in range(max(2, order[u] + 1), top(u) + 1):
            for b in range(e - 1):
                T = u + (k - order[u]) * gen[b]
                if T not in aps: DB += 1; DA += 1
                elif order[T] != k: DA += 1
    # Hall test for delta
    mt = None
    if delta:
        toks = []; idx = {}; adj = []
        for (v, k) in delta:
            F = subsums(rep[v], gen); lst = []
            for u in F:
                for kk in range(max(2, order[u] + 1), top(u) + 1):
                    for b in range(e - 1):
                        tk = (u, b, kk)
                        if tk in used or tk in forced or tk in fixed: continue
                        if tk not in idx: idx[tk] = len(idx)
                        lst.append(idx[tk])
            adj.append(lst)
        mt = bpm(adj, len(delta)) - len(delta)
    return dict(m=m, e=e, q=q, h=h, W=W, Tc=Tc, delta=len(delta), cross=ncross, chain=nchain, mix=nmix, MT=mt,
                DB=DB - e * Tc, DA=DA - e * Tc, gens=[m] + gen)
if __name__ == "__main__":
    if sys.argv[1] != "rnd":
        print(analyse(list(map(int, sys.argv[1:])))); sys.exit()
    mlo, mhi, kmin, kmax, N, seed = map(int, sys.argv[2:8]); random.seed(seed)
    mode = sys.argv[8] if len(sys.argv) > 8 else "hi4"
    st = {}; worst = {}
    for _ in range(N):
        m = random.randint(mlo, mhi); k = random.randint(kmin, kmax)
        hi = 2 * m if mode == "p18" else int(mode[2:]) * m
        if hi - m - 1 < k: continue
        r = analyse([m] + random.sample(range(m + 1, hi), k))
        if r is None or r["e"] < 3: continue
        s = st.setdefault(r["q"], [0, 0, 0, 0, 0, 0, 0, 0])
        s[0] += 1; s[1] += r["Tc"]; s[2] += r["delta"]; s[3] += r["cross"]; s[4] += r["chain"]
        s[5] += (r["MT"] is not None and r["MT"] < 0); s[6] += r["DB"] < 0; s[7] += r["DA"] < 0
        for key in ("MT", "DB", "DA"):
            if r[key] is not None and (key not in worst or r[key] < worst[key][key]): worst[key] = r
    print(sys.argv[1:])
    print("  q: [#S, sum Tc, sum delta, cross, chain, MTfail, DBfail, DAfail]")
    for q, s in sorted(st.items()): print("   ", q, s)
    for key, r in worst.items(): print("  worst", key, r)
