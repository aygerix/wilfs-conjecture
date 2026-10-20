r"""ZG at P18 depth four (lead, 2026-10-20): p + |R| <= Z + G, where Z = sum_x (4 - lambda(0,x)) (slots of 0) and
G = sum_b sum_x (L_{g_b} - lambda(g_b, x)) (slots of the generators).  pi uses p generator slots; rho uses pair slots;
so ZG + (pi injective) + Hall would give DEAD there.  Also ZG' : p + q <= Z + G + P (P = slots of uncarried pairs).
usage: zg.py exh k mlo mhi | rnd k mlo mhi N seed | pts m b..."""
import sys, itertools, random
sys.path.insert(0, ".")
from twin import build
def test(m, B):
    D = build([m] + [m + b for b in B])
    if D is None or D["q"] != 4: return None
    w, aps, gen, e, order, car, rep, h, W = (D[k] for k in "w aps gen e order car rep h W".split())
    if any(g >= 2 * m for g in gen): return None
    top = lambda u: 4 if u % m < h else 3
    lam = lambda u, b: next(j for j in range(m + 1) if (u + (j + 1) * gen[b]) not in aps)
    L = {u: top(u) - u // m for u in w}
    Z = sum(L[0] - lam(0, b) for b in range(e - 1))
    G = sum(L[g] - lam(g, b) for g in gen for b in range(e - 1))
    P = sum(L[u] - lam(u, b) for u in w if order[u] == 2 and car[u] == 0 for b in range(e - 1))
    p = sum(1 for u in w if car[u] and order[u] == 2); q = sum(1 for u in w if car[u] and order[u] == 3)
    R = 0
    for v in w:
        if car[v] and order[v] == 3:
            bs = sorted(gen[i] - m for i, a in rep[v].items() for _ in range(a))
            if bs[0] + bs[1] >= h: R += 1
    G2 = sum(L[g] for g in gen for b in range(e - 1) if (g + gen[b]) not in aps)   # generator slots from dead pairs only
    kk = e - 1; a = sum(1 for g in gen if g - m < h)
    D1 = sum(1 for g in gen for x in gen if (g + x) not in aps)
    N2 = sum(1 for g in gen for x in gen if (g + 2 * x) in aps); N3 = sum(1 for g in gen for x in gen if (g + 3 * x) in aps)
    assert G == kk * kk + a * kk + D1 - N2 - N3
    Ful = sum(1 for g in gen for b in range(e - 1) if L[g] - lam(g, b) == 0)
    Ext = sum(max(0, L[g] - lam(g, b) - 1) for g in gen for b in range(e - 1))
    assert G == kk * kk - Ful + Ext
    return dict(m=m, B=tuple(B), e=e, h=h, W=W, p=p, q=q, R=R, Z=Z, G=G, P=P, ZG=Z + G - p - R, ZGP=Z + G + P - p - q,
                S2=G - p - q, S3=Z + G - p - q, TF=kk * kk - p - q - Ful, Ful=Ful, Ext=Ext, TFZ=kk * kk + Z - p - q - Ful)
if __name__ == "__main__":
    a = sys.argv[1:]; recs = []
    if a[0] == "pts": print(test(int(a[1]), list(map(int, a[2:])))); sys.exit()
    if a[0] == "exh":
        k, mlo, mhi = map(int, a[1:4])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                r = test(m, list(B))
                if r: recs.append(r)
    else:
        k, mlo, mhi, N, seed = map(int, a[1:6]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); r = test(m, sorted(random.sample(range(1, m), k)))
            if r: recs.append(r)
    for key in ("S2", "S3", "TF", "TFZ"):
        bad = [r for r in recs if r[key] < 0]
        print(a, key, "S", len(recs), "fails", len(bad), "min", min((r[key] for r in recs), default=None))
        for r in sorted(bad, key=lambda r: r[key])[:3]: print("   ", r)
