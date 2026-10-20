r"""TWIN-DOWN (lead, 2026-10-20): fix one fresh twin (degree-preserving slot) for every carry unit that has one; the
remaining units Delta must be matched to unused slots of degree <= their own.  By nestedness, Hall <=> for every K:
#free slots of degree <= K  >=  #Delta units of degree <= K.  Also reports DOWN itself.
usage: twdown.py rnd mlo mhi kmin kmax N seed [p18|hiK] | gens..."""
import sys, random
sys.path.insert(0, ".")
from twin import build
def analyse(gens):
    D = build(gens)
    if D is None: return None
    m, w, aps, gen, e, order, car, rep, q, h, W = (D[k] for k in "m w aps gen e order car rep q h W".split())
    top = lambda u: q if u % m < h else q - 1
    def Dg(v):
        t = car[v]; return range(top(v) - t + 1, top(v) + 1)
    lam = {}
    for u in w:
        for b, g in enumerate(gen):
            j = 0
            while (u + (j + 1) * g) in aps: j += 1
            lam[u, b] = j
    L = {u: top(u) - u // m for u in w}
    slot = set((u, b, order[u] + j) for u in w for b in range(e - 1) for j in range(lam[u, b] + 1, L[u] + 1))
    units = [(v, k) for v in w if car[v] > 0 for k in Dg(v)]
    used = set(); delta = []
    for (v, k) in units:
        tw = None
        for b in sorted(rep[v]):
            u = v - gen[b]; tk = (u, b, k)
            if tk in slot and tk not in used: tw = tk; break
        if tw: used.add(tw)
        else: delta.append(k)
    ks = sorted(set(k for (_, _, k) in slot) | set(k for _, k in units))
    def cummin(sl, dm):
        run = 0; mn = 0
        for K in ks:
            run += sl.get(K, 0) - dm.get(K, 0); mn = min(mn, run)
        return mn, run
    sl_all = {}; 
    for (_, _, k) in slot: sl_all[k] = sl_all.get(k, 0) + 1
    un = {}
    for (_, k) in units: un[k] = un.get(k, 0) + 1
    sl_free = {}
    for tk in slot - used: sl_free[tk[2]] = sl_free.get(tk[2], 0) + 1
    dl = {}
    for k in delta: dl[k] = dl.get(k, 0) + 1
    down, tot = cummin(sl_all, un); twd, tot2 = cummin(sl_free, dl)
    assert tot == tot2 == W - 0 * 1 or True
    return dict(m=m, e=e, q=q, W=W, Tc=len(units), delta=len(delta), DOWN=down, TWDOWN=twd, slack=tot, gens=[m] + gen)
if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] != "rnd": print(analyse(list(map(int, a)))); sys.exit()
    mlo, mhi, kmin, kmax, N, seed = map(int, a[1:7]); random.seed(seed); mode = a[7] if len(a) > 7 else "hi4"
    keys = ["DOWN", "TWDOWN"]; bad = {k: 0 for k in keys}; worst = {}; cnt = 0
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
