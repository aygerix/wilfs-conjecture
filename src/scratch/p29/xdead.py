r"""Conductor-free versions (lead, 2026-10-20).  X(u) = max{x(w) : u + w in Ap} <= L_u (general reflection lemma).
XWILF: (e-1) sum_u X(u) >= g.     XDEAD: sum_u sum_b (X(u) - lambda(u,b)) >= T_c.   (Each implies Wilf / DEAD.)
Also reports ell - sum X (>= 0).  usage: xdead.py rnd mlo mhi kmin kmax N seed [p18|hiK] | gens..."""
import sys, random
sys.path.insert(0, ".")
from twin import build
def analyse(gens):
    D = build(gens)
    if D is None: return None
    m, w, aps, gen, e, order, car, q, h, W = (D[k] for k in "m w aps gen e order car q h W".split())
    top = lambda u: q if u % m < h else q - 1
    X = {u: max(z // m for z in w if (z - u) in aps) - 0 for u in w}
    X = {u: max((z - u) // m for z in w if (z - u) in aps) for u in w}
    L = {u: top(u) - u // m for u in w}
    assert all(X[u] <= L[u] for u in w)
    lam = {(u, b): next(j for j in range(m + 1) if (u + (j + 1) * g) not in aps) for u in w for b, g in enumerate(gen)}
    g = sum(u // m for u in w); Tc = sum(car.values())
    xw = (e - 1) * sum(X.values()) - g
    xd = sum(X[u] - lam[u, b] for u in w for b in range(e - 1)) - Tc
    return dict(m=m, e=e, q=q, W=W, XWILF=xw, XDEAD=xd, gap=sum(L.values()) - sum(X.values()), gens=[m] + gen)
if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] != "rnd": print(analyse(list(map(int, a)))); sys.exit()
    mlo, mhi, kmin, kmax, N, seed = map(int, a[1:7]); random.seed(seed); mode = a[7] if len(a) > 7 else "hi4"
    keys = ["XWILF", "XDEAD"]; bad = {k: 0 for k in keys}; worst = {}; cnt = 0
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
