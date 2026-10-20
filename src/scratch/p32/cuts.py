"""Cut decomposition J - C = sum_{k>=1} mu(U_k), mu = K+1-u, U_k = {alpha : sigma >= k m} (PROOFS, cut form).
Question CUT2: is mu(U_k) <= 0 for every k >= 2?  If so, J - C <= mu(U_1) and every deficit bound reduces to the first
cut. Also reports max mu(U_1) - (rho + r). Usage: python cuts.py NR SEED"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from idq import canon
NR, SEED = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(SEED)
def cutvals(m, rho, B, q):
    K = len(B); best = canon(m, rho, B, q, q + 3); reach = {x: v for x, v in best.items() if v[0] <= q}
    if (m - 1) not in best or best[m - 1][0] < q: return None
    mus = {}
    for x, (lx, tx, cx, ax) in reach.items():
        sig = rho + sum(a * b for a, b in zip(ax, B)); j = sig // m
        u = 0
        for i, b in enumerate(B):
            y = (x + b) % m; ay = tuple(ax[k] + (k == i) for k in range(K))
            if not (y in reach and reach[y][3] == ay): u += ax[i] + 1
        for k in range(1, j + 1): mus[k] = mus.get(k, 0) + (K + 1 - u)
    return mus, m - len(reach)
pos2 = 0; n = 0; worst = None
models = [(66, 4, [1, 5, 6, 32, 37, 62], 5), (61, 10, [1, 2, 6, 27, 28, 51], 5), (64, 2, [1, 5, 11, 31, 36], 6)]
for it in range(NR):
    q = rnd.randint(5, 8); m = rnd.randint(15, 90); rho = rnd.randint(0, m - 2)
    hi = m if rnd.random() < 0.4 else m - rho
    if hi < 6: continue
    K = rnd.randint(2, min(8, hi - 2)); lo = rnd.randint(1, hi - 1); top = rnd.randint(lo, hi - 1)
    if top - lo + 1 < K: continue
    models.append((m, rho, sorted(rnd.sample(range(lo, top + 1), K)), q))
for (m, rho, B, q) in models:
    res = cutvals(m, rho, B, q)
    if res is None: continue
    mus, r = res; n += 1
    for k, v in mus.items():
        if k >= 2 and v > 0:
            pos2 += 1
            if worst is None or v > worst[0]: worst = (v, k, m, rho, B, q, mus)
    if (m, rho) in [(66, 4), (61, 10), (64, 2)]: print("T1-cex", m, rho, B, q, "cuts", mus, "r", r)
print("models", n, "positive mu(U_k), k>=2:", pos2, "worst", worst)
