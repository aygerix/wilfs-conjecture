"""Annealer for shape-only REARR on lex tiles of S = <m, G> with m > 3e (lead, 2026-10-21).
REARR: sum_k w_(k) (m-k) <= (N+1) C(m,2), w = |y| + N over Max(M^) sorted decreasingly (N = e-1).
REARR for all S with m > 3e + TM-implication + Eliahou (e >= m/3) would give Wilf. Maximizes the ratio.
Usage: python rearr_ann.py NR IT SEED MMIN MMAX"""
import sys, random, math
sys.path.insert(0, '.')
from tile import build
def ratio(m, G):
    if m < 4 or any(g <= m for g in G): return None
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; N = len(gens)
    if N < 2 or m <= 3 * (N + 1): return None
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(N))
    w = sorted((sum(a) + N for a in M if all(up(a, i) not in M for i in range(N))), reverse=True)
    return sum(wk * (m - k) for k, wk in enumerate(w, 1)) / ((N + 1) * m * (m - 1) / 2), c, gens, N, len(w)
NR, IT, SEED, MMIN, MMAX = map(int, sys.argv[1:6]); rnd = random.Random(SEED); best = None
for rs in range(NR):
    while True:
        m = rnd.randint(MMIN, MMAX); k = rnd.randint(2, max(2, m // 3 - 2))
        G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 5]) * m + 2), min(m, k)))
        v = ratio(m, G)
        if v is not None: break
    cur = (m, v[2]); T = 0.03
    for it in range(IT):
        m, G = cur[0], list(cur[1]); u = rnd.random()
        if u < 0.45: i = rnd.randrange(len(G)); G[i] += rnd.choice([-2, -1, 1, 2, m, -m])
        elif u < 0.6 and len(G) > 2: G.pop(rnd.randrange(len(G)))
        elif u < 0.8: G.append(rnd.randint(m + 1, 4 * m))
        else: m += rnd.choice([-1, 1])
        if m < MMIN or m > MMAX: continue
        v2 = ratio(m, sorted(G))
        if v2 is None: continue
        if v2[0] >= v[0] or rnd.random() < math.exp((v2[0] - v[0]) / T):
            cur, v = (m, v2[2]), v2
            if best is None or v[0] > best:
                best = v[0]; print("best REARR ratio %.5f m=%d c=%d N=%d #max=%d gens=%s" % (v[0], m, v[1], v[3], v[4], v[2]), flush=True)
        T = max(0.0005, T * 0.995)
    if rs % 20 == 0: print("restart", rs, "best", best, flush=True)
