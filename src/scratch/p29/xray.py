r"""XRAY (lead, 2026-10-20): g <= sum_b sum_{u in Ap} x(lambda(u,b) g_b).  Since X(u) >= x(lambda(u,b) g_b) for every b,
XRAY => XWILF ((e-1) sum X >= g) => Wilf.  Also XRAYmax: g <= sum_u max_b ... no; reports both XRAY and XWILF slack.
usage: xray.py rnd mlo mhi kmin kmax N seed [p18|hiK] | gens..."""
import sys, random
sys.path.insert(0, ".")
from twin import build
def analyse(gens):
    D = build(gens)
    if D is None: return None
    m, w, aps, gen, e, order, car, q, h, W = (D[k] for k in "m w aps gen e order car q h W".split())
    lam = {(u, b): next(j for j in range(m + 1) if (u + (j + 1) * g) not in aps) for u in w for b, g in enumerate(gen)}
    X = {u: max((z - u) // m for z in w if (z - u) in aps) for u in w}
    g = sum(u // m for u in w)
    xray = sum((lam[u, b] * gen[b]) // m for u in w for b in range(e - 1)) - g
    xw = (e - 1) * sum(X.values()) - g
    return dict(m=m, e=e, q=q, W=W, XRAY=xray, XWILF=xw, type=sum(1 for u in w if all((u + gg) not in aps for gg in gen)), gens=[m] + gen)
if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] != "rnd": print(analyse(list(map(int, a)))); sys.exit()
    mlo, mhi, kmin, kmax, N, seed = map(int, a[1:7]); random.seed(seed); mode = a[7] if len(a) > 7 else "hi4"
    keys = ["XRAY", "XWILF"]; bad = {k: 0 for k in keys}; worst = {}; cnt = 0; bigt = 0
    for _ in range(N):
        m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); hi = 2 * m if mode == "p18" else int(mode[2:]) * m
        if hi - m - 1 < k: continue
        r = analyse([m] + random.sample(range(m + 1, hi), k))
        if r is None or r["e"] < 3: continue
        cnt += 1; bigt += r["type"] > r["e"] - 1
        for kk in keys:
            bad[kk] += r[kk] < 0
            if kk not in worst or r[kk] < worst[kk][kk]: worst[kk] = r
    print(a, "S", cnt, "(type > e-1:", bigt, ") fails", bad)
    for kk in keys: print("  worst", kk, worst[kk])
