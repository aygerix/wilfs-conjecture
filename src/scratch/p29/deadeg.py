r"""Per-degree versions of DEAD (lead, 2026-10-20).  slots_k = dead pool tokens of degree k that are not forced
(forced: (u, b, k) with u carried and k in D(u)); n_k = #{u carried : k in D(u)}.  DEAD <=> sum_k slots_k >= sum_k n_k.
PDEG: slots_k >= n_k for every k;  UP: sum_{k>=K} slots_k >= sum_{k>=K} n_k for every K;  DOWN: same with k <= K.
usage: deadeg.py rnd mlo mhi kmin kmax N seed [p18|hiK]"""
import sys, random
sys.path.insert(0, ".")
from deadloc import build
def analyse(gens):
    D = build(gens)
    if D is None: return None
    w, gen, e, o, L, t, lam, q, h, m = (D[k] for k in "w gen e o L t lam q h m".split())
    top = lambda u: q if u % m < h else q - 1
    slots = {}; n = {}
    for u in w:
        for b in range(e - 1):
            for j in range(lam[u, b] + 1, L[u] + 1):  # slots j in (lam, L_u]
                k = o[u] + j; slots[k] = slots.get(k, 0) + 1
        if t[u] > 0:
            for k in range(top(u) - t[u] + 1, top(u) + 1): n[k] = n.get(k, 0) + 1
    ks = sorted(set(slots) | set(n))
    pdeg = min(slots.get(k, 0) - n.get(k, 0) for k in ks) if ks else 0
    up = min(sum(slots.get(k, 0) - n.get(k, 0) for k in ks if k >= K) for K in ks) if ks else 0
    down = min(sum(slots.get(k, 0) - n.get(k, 0) for k in ks if k <= K) for K in ks) if ks else 0
    return dict(m=m, e=e, q=q, W=D["W"], tot=sum(slots.values()) - sum(n.values()), PDEG=pdeg, UP=up, DOWN=down, gens=[m] + gen)
if __name__ == "__main__":
    a = sys.argv[1:]
    mlo, mhi, kmin, kmax, N, seed = map(int, a[1:7]); random.seed(seed); mode = a[7] if len(a) > 7 else "hi4"
    keys = ["tot", "PDEG", "UP", "DOWN"]; bad = {k: 0 for k in keys}; worst = {}; cnt = 0
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
