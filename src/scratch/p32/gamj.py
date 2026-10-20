"""Layer CORE1: for a P18 model (m, rho, B) at true depth q, N_k = #{x : lam_x <= k} (shifted levels).
Gamma_j = (K+1)*sum_{k<j} N_k + m + rho - (j+1)*N_j  (j <= q; Gamma_q = E + r = CORE1).
Question: is Gamma_j >= 0 for every j <= q?  And the degree form E = rho + sum_x (q - t_x) u(x) - (K+1) J (assert).
Usage: python gamj.py NR SEED QMAX"""
import sys, random
sys.path.insert(0, __import__('os').path.dirname(__file__))
from idq import canon
NR, SEED, QMAX = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); rnd = random.Random(SEED)
neg = 0; n = 0; worst = None; badid = 0
for it in range(NR):
    m = rnd.randint(10, 90); rho = rnd.randint(0, m // 2); hi = m if rnd.random() < 0.3 else m - rho
    K = rnd.randint(2, min(10, hi - 2)); lo = rnd.randint(1, hi - 1); top = rnd.randint(lo, hi - 1)
    if top - lo + 1 < K: continue
    B = sorted(rnd.sample(range(lo, top + 1), K))
    best = canon(m, rho, B, 60, 64)
    lam = [best[x][0] if x in best else 99 for x in range(m)]
    q = max(lam)
    if q > QMAX or q < 3 or max(lam) >= 99: continue
    # true depth: conductor = q m - rho iff position m-1... require the model's own conductor: largest gap
    n += 1
    N = [sum(1 for l in lam if l <= k) for k in range(q + 1)]
    # degree-form identity at the true depth q
    reach = {x: v for x, v in best.items() if v[0] <= q}
    d = len(reach); r = m - d; ell = sum(q - v[0] for v in reach.values())
    E = (K + 1) * ell - q * d + rho
    tot = 0; J = 0
    for x, (lx, tx, cx, ax) in reach.items():
        J += lx - tx
        for i, b in enumerate(B):
            y = (x + b) % m; ay = tuple(ax[k] + (k == i) for k in range(K))
            if not (y in reach and reach[y][3] == ay): tot += (q - tx) * (ax[i] + 1)
    if E != rho + tot - (K + 1) * J: badid += 1
    for j in range(1, q + 1):
        G = (K + 1) * sum(N[:j]) + m + rho - (j + 1) * N[j]
        if G < 0:
            neg += 1
            if worst is None or G < worst[0]: worst = (G, j, q, m, rho, B, N)
print("models", n, "degree-form mismatches", badid, "negative Gamma_j", neg, "worst", worst)
