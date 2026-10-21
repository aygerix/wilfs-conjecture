r"""How negative can Tile-CL get? (lead, 2026-10-20). Annealer minimizing min_sigma V(sigma) (V = Tile-CL slack/m,
V = (m-1)/2 - f/m), reporting Dep, |B| (non-maximal boundary cells), #spikes, and the ratio -V/Dep.
SCORE: 'V' minimizes min V / m; 'R' maximizes -min V / Dep.  Usage: python tcldef.py NR IT SEED MMIN MMAX DMIN EMAX OPEN SCORE"""
import sys, random, math
sys.path.insert(0, '.')
from tile import build
NR, IT, SEED, MMIN, MMAX, DMIN, EMAX, OPEN = map(int, sys.argv[1:9]); SC = sys.argv[9]; rnd = random.Random(SEED); top = None
def stats(m, gens, M):
    N = len(gens); D = list(M); Ds = set(D); delta = [g % m for g in gens]
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    om = {x: 0 for x in D}
    for b in range(N):
        for x in D:
            if up(x, b) not in Ds: om[x] += x[b] + 1
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    dep = sum(v for x, v in om.items() if x not in mx)
    B = sum(1 for x in D if om[x] > 0 and x not in mx)
    spikes = sum(1 for b in range(N) if sum(1 for x in D if x[b] >= 1) == 1)
    lab0 = [sum(p * q for p, q in zip(x, delta)) % m for x in D]
    wt = [0] * m
    for x, l in zip(D, lab0): wt[l] += om[x]
    Mp = m * (m - 1) // 2
    vmin = min((Mp - (sum(wt[l] * ((l + rho) % m) for l in range(m)) - N * Mp)) // m for rho in range(m))
    return vmin, dep, B, spikes
def value(m, G):
    if m < 4 or any(g <= m for g in G): return None
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; d = len(gens)
    if d < DMIN or d + 1 > EMAX or (OPEN and (3 * (d + 1) >= m or c <= 4 * m)): return None
    v, dep, B, sp = stats(m, gens, M)
    sc = v / m if SC == 'V' else (-v / max(dep, 1))
    if SC == 'R': sc = -sc
    return sc, v, dep, B, sp, c, gens
for rs in range(NR):
    v = None
    for _ in range(3000):
        m = rnd.randint(MMIN, MMAX); k = rnd.randint(DMIN, max(DMIN, min(EMAX - 1, (m // 3 - 2) if OPEN else m - 1)))
        G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 5]) * m + 2), min(k, m)))
        v = value(m, G)
        if v is not None: break
    if v is None: continue
    cur = (m, v[-1]); T = 0.05
    for it in range(IT):
        m, G = cur[0], list(cur[1]); r = rnd.random()
        if r < 0.45: i = rnd.randrange(len(G)); G[i] += rnd.choice([-2, -1, 1, 2, m, -m])
        elif r < 0.6 and len(G) > 2: G.pop(rnd.randrange(len(G)))
        elif r < 0.8: G.append(rnd.randint(m + 1, 4 * m))
        else: m += rnd.choice([-1, 1])
        if m < MMIN or m > MMAX: continue
        v2 = value(m, sorted(G))
        if v2 is None: continue
        if v2[0] <= v[0] or rnd.random() < math.exp((v[0] - v2[0]) / T):
            cur, v = (m, v2[-1]), v2
            if top is None or v[0] < top:
                top = v[0]; print("best score %.4f minV %d Dep %d |B| %d spikes %d m=%d c=%d e=%d gens=%s" % (v[0], v[1], v[2], v[3], v[4], m, v[5], len(v[6]) + 1, v[6]), flush=True)
        T = max(0.001, T * 0.995)
    if rs % 20 == 0: print("restart", rs, "best", top, flush=True)
