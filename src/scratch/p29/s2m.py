r"""S2-inside at P18 depth four (lead, 2026-10-20): fix pi for carried pairs; match carried triples v = g1+g2+g3
(b1<=b2<=b3) to generator slots (g_b, x, j) [g_b + j g_x not in Ap, 1 <= j <= L_b] with b in {b1,b2,b3}, not used by pi.
Reports failures and the slot-type statistics of a matching (position of b, whether x in supp(v), x vs b3, j).
usage: s2m.py exh k mlo mhi | rnd k mlo mhi N seed | pts m b..."""
import sys, itertools, random
sys.path.insert(0, ".")
from twin import build
sys.setrecursionlimit(100000)
def test(m, B, stats=None):
    D = build([m] + [m + b for b in B])
    if D is None or D["q"] != 4: return None
    w, aps, gen, e, order, car, rep, h, W = (D[k] for k in "w aps gen e order car rep h W".split())
    if any(g >= 2 * m for g in gen): return None
    bb = lambda i: gen[i] - m
    Lb = lambda i: 3 if bb(i) < h else 2
    slot = set((i, x, j) for i in range(e - 1) for x in range(e - 1) for j in range(1, Lb(i) + 1) if (gen[i] + j * gen[x]) not in aps)
    used = set(); trip = []
    for v in w:
        if not car[v]: continue
        idx = sorted((i for i, a in rep[v].items() for _ in range(a)), key=bb)
        if len(idx) == 2:
            b, b2 = idx; tk = (b, b2, 2) if bb(b2) >= h else (b, b2, 3)
            assert tk in slot and tk not in used; used.add(tk)
        else: trip.append(idx)
    adj = [[s for s in slot if s not in used and s[0] in set(t)] for t in trip]
    mt = {}
    def aug(x, seen):
        for y in adj[x]:
            if y in seen: continue
            seen.add(y)
            if y not in mt or aug(mt[y], seen): mt[y] = x; return True
        return False
    ok = sum(1 for x in range(len(trip)) if aug(x, set()))
    if stats is not None:
        for y, x in mt.items():
            t = trip[x]; i, xx, j = y
            pos = "b1" if i == t[0] else ("b2" if i == t[1] else "b3")
            xin = "x=b3" if xx == t[2] else ("x in v" if xx in t else "x out")
            key = (pos, xin, j); stats[key] = stats.get(key, 0) + 1
    return dict(m=m, B=tuple(B), e=e, h=h, W=W, q=len(trip), matched=ok, def_=len(trip) - ok, free=len(slot) - len(used))
if __name__ == "__main__":
    a = sys.argv[1:]; recs = []; stats = {}
    if a[0] == "pts": print(test(int(a[1]), list(map(int, a[2:])), stats)); print(stats); sys.exit()
    if a[0] == "exh":
        k, mlo, mhi = map(int, a[1:4])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                r = test(m, list(B), stats)
                if r: recs.append(r)
    else:
        k, mlo, mhi, N, seed = map(int, a[1:6]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); r = test(m, sorted(random.sample(range(1, m), k)), stats)
            if r: recs.append(r)
    bad = [r for r in recs if r["def_"] > 0]
    print(a, "S", len(recs), "S2-inside fails", len(bad))
    for r in bad[:3]: print("  ", r)
    tot = sum(stats.values()) or 1
    for key, v in sorted(stats.items(), key=lambda t: -t[1])[:12]: print("   ", key, v, "%.3f" % (v / tot))
