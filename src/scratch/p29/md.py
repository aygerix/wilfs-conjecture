r"""Conjecture MD (lead, 2026-10-20): inside, dead, degree-monotone matching.  Each carry unit (v, k) (v carried,
k in D(v)) is matched injectively to a slot (u, b, k') [dead, non-forced token: lambda(u,b) < k'-o(u) <= L_u] with
u a sub-sum of v's chosen factorization (0 and v allowed) and k' <= k.  MD => DOWN => DEAD => Wilf.
TMD: the same after first fixing one fresh twin per unit that has one.
usage: md.py rnd mlo mhi kmin kmax N seed [p18|hiK] | gens..."""
import sys, random
sys.path.insert(0, ".")
from twin import build, subsums
sys.setrecursionlimit(1000000)
def match(adj, nl):
    mt = {}
    def aug(x, seen):
        for y in adj[x]:
            if y in seen: continue
            seen.add(y)
            if y not in mt or aug(mt[y], seen): mt[y] = x; return True
        return False
    return sum(1 for x in range(nl) if aug(x, set()))
def analyse(gens):
    D = build(gens)
    if D is None: return None
    m, w, aps, gen, e, order, car, rep, q, h, W = (D[k] for k in "m w aps gen e order car rep q h W".split())
    top = lambda u: q if u % m < h else q - 1
    lam = {}
    for u in w:
        for b, g in enumerate(gen):
            j = 0
            while (u + (j + 1) * g) in aps: j += 1
            lam[u, b] = j
    L = {u: top(u) - u // m for u in w}
    slots_of = {u: [(u, b, order[u] + j) for b in range(e - 1) for j in range(lam[u, b] + 1, L[u] + 1)] for u in w}
    units = [(v, k) for v in w if car[v] > 0 for k in range(top(v) - car[v] + 1, top(v) + 1)]
    if not units: return dict(m=m, e=e, q=q, W=W, Tc=0, MD=0, TMD=0, gens=[m] + gen)
    sub = {v: subsums(rep[v], gen) for v in w if car[v] > 0}
    adj = [[s for u in sub[v] for s in slots_of[u] if s[2] <= k] for (v, k) in units]
    md = match(adj, len(units)) - len(units)
    fixed = set(); rest = []
    for (v, k) in units:
        tw = None
        for b in sorted(rep[v]):
            tk = (v - gen[b], b, k)
            if tk in set(slots_of[v - gen[b]]) and tk not in fixed: tw = tk; break
        if tw: fixed.add(tw)
        else: rest.append((v, k))
    adj2 = [[s for s in a if s not in fixed] for (v, k), a in zip(units, adj) if (v, k) in set(rest)]
    tmd = (match(adj2, len(adj2)) - len(adj2)) if adj2 else 0
    return dict(m=m, e=e, q=q, W=W, Tc=len(units), delta=len(rest), MD=md, TMD=tmd, gens=[m] + gen)
if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] != "rnd": print(analyse(list(map(int, a)))); sys.exit()
    mlo, mhi, kmin, kmax, N, seed = map(int, a[1:7]); random.seed(seed); mode = a[7] if len(a) > 7 else "hi4"
    keys = ["MD", "TMD"]; bad = {k: 0 for k in keys}; worst = {}; cnt = 0
    for _ in range(N):
        m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); hi = 2 * m if mode == "p18" else int(mode[2:]) * m
        if hi - m - 1 < k: continue
        r = analyse([m] + random.sample(range(m + 1, hi), k))
        if r is None or r["e"] < 3: continue
        cnt += 1
        for kk in keys:
            bad[kk] += r[kk] < 0
            if kk not in worst or r[kk] < worst[kk][kk]: worst[kk] = r
    print(a, "S", cnt, "fails", bad)
    for kk in keys: print("  worst", kk, worst[kk])
