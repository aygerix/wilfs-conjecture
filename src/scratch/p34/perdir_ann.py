"""Annealer for ALL-BUT-ONE (lead, 2026-10-21): minimize the second-smallest normalized per-direction depth
B^i / (m(m-1)/2) over S (any depth unless CMIN given). Value < 1 refutes ALL-BUT-ONE.
Usage: python perdir_ann.py NR IT SEED MMAX DEPTHMIN"""
import sys, random, math
sys.path.insert(0, '.')
from tile import build
def val(m, G, DMIN):
    if m < 3 or any(g <= m for g in G): return None
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; N = len(gens)
    if N < 2 or c <= DMIN * m: return None
    top = c + m - 1; h = m * (m - 1) / 2
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(N))
    B = [0] * N
    for a, x in M.items():
        for i in range(N):
            if up(a, i) not in M: B[i] += (a[i] + 1) * (top - x)
    s = sorted(b / h for b in B)
    return s[1], c, gens, [round(b / h, 3) for b in B]
NR, IT, SEED, MMAX, DMIN = map(int, sys.argv[1:6]); rnd = random.Random(SEED); best = None
for rs in range(NR):
    while True:
        m = rnd.randint(4, MMAX); G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 5]) * m + 2), rnd.randint(2, 6)))
        v = val(m, G, DMIN)
        if v is not None: break
    cur = (m, v[2]); T = 0.3
    for it in range(IT):
        m, G = cur[0], list(cur[1]); u = rnd.random()
        if u < 0.5: i = rnd.randrange(len(G)); G[i] += rnd.choice([-2, -1, 1, 2, m, -m])
        elif u < 0.6 and len(G) > 2: G.pop(rnd.randrange(len(G)))
        elif u < 0.75: G.append(rnd.randint(m + 1, 4 * m))
        else: m += rnd.choice([-1, 1])
        if m < 3 or m > MMAX: continue
        v2 = val(m, G, DMIN)
        if v2 is None: continue
        if v2[0] <= v[0] or rnd.random() < math.exp((v[0] - v2[0]) / T):
            cur, v = (m, v2[2]), v2
            if best is None or v[0] < best[0]:
                best = v; print("best 2nd=%.4f m=%d c=%d gens=%s B/h=%s" % (v[0], m, v[1], v[2], v[3]), flush=True)
        T = max(0.005, T * 0.995)
    if rs % 20 == 0: print("restart", rs, "best", best[0] if best else None, flush=True)
