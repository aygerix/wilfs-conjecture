r"""box-DEAD (lead, 2026-10-20): for each carried v, sum over the box of v's chosen factorization of
(slots - carry) >= 0 (a Hall-necessary condition for MD).  Reports min slack over boxes and over S, and how often
the minimising box is the whole top element's box.  usage: boxdead.py rnd mlo mhi kmin kmax N seed [p18|hiK]"""
import sys, random
sys.path.insert(0, ".")
from twin import build, subsums
def analyse(gens):
    D = build(gens)
    if D is None: return None
    m, w, aps, gen, e, order, car, rep, q, h, W = (D[k] for k in "m w aps gen e order car rep q h W".split())
    top = lambda u: q if u % m < h else q - 1
    lam = {(u, b): next(j for j in range(m + 1) if (u + (j + 1) * g) not in aps) for u in w for b, g in enumerate(gen)}
    sig = {u: sum(top(u) - u // m - lam[u, b] for b in range(e - 1)) for u in w}
    best = None
    for v in w:
        if car[v] == 0: continue
        bx = subsums(rep[v], gen)
        sl = sum(sig[u] - car[u] for u in bx)
        if best is None or sl < best[0]: best = (sl, v, len(bx), car[v], top(v) - v // m)
    return dict(m=m, e=e, q=q, W=W, minbox=best[0] if best else None, v=best[1] if best else None, boxsize=best[2] if best else None,
                tv=best[3] if best else None, Lv=best[4] if best else None, gens=[m] + gen)
if __name__ == "__main__":
    a = sys.argv[1:]
    mlo, mhi, kmin, kmax, N, seed = map(int, a[1:7]); random.seed(seed); mode = a[7] if len(a) > 7 else "hi4"
    cnt = bad = 0; worst = None; ratios = []
    for _ in range(N):
        m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); hi = 2 * m if mode == "p18" else int(mode[2:]) * m
        if hi - m - 1 < k: continue
        r = analyse([m] + random.sample(range(m + 1, hi), k))
        if r is None or r["e"] < 3 or r["minbox"] is None: continue
        cnt += 1; bad += r["minbox"] < 0
        if worst is None or r["minbox"] < worst["minbox"]: worst = r
    print(a, "S", cnt, "box-DEAD fails", bad); print("  worst", worst)
