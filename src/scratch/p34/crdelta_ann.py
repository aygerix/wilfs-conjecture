r"""Annealer for CR-delta (lead, 2026-10-20), mirror-aware: score = min over delta, -delta of CR-delta slack / m
(negative refutes CR-delta).  Also reports the true-label DEP-ALL slack.  Usage: python crdelta_ann.py NR IT SEED MMIN MMAX EMAX OPEN HMIN"""
import sys, random, math
sys.path.insert(0, '.')
from tile import build
from crdelta import crdelta
NR, IT, SEED, MMIN, MMAX, EMAX, OPEN, HMIN = map(int, sys.argv[1:9]); rnd = random.Random(SEED); top = None
def value(m, G):
    if m < 4 or any(g <= m for g in G): return None
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; d = len(gens)
    if d < 2 or d + 1 > EMAX or (OPEN and (3 * (d + 1) >= m or c <= 4 * m)): return None
    if max(sum(x) for x in M) < HMIN: return None
    D = list(M); a = crdelta(m, D, [g % m for g in gens]); b = crdelta(m, D, [(-g) % m for g in gens])
    sl = min(a[0], b[0])
    return sl / m, sl, min(a[1], b[1]), c, gens
for rs in range(NR):
    v = None
    for _ in range(3000):
        m = rnd.randint(MMIN, MMAX); k = rnd.randint(2, max(2, min(EMAX - 1, (m // 3 - 2) if OPEN else m - 1)))
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
                top = v[0]; print("best CRdelta/m %.4f slack %d (true-label min %d) m=%d c=%d e=%d gens=%s" % (v[0], v[1], v[2], m, v[3], len(v[4]) + 1, v[4]), flush=True)
        T = max(0.001, T * 0.995)
    if rs % 20 == 0: print("restart", rs, "best", top, flush=True)
