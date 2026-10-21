r"""Annealer for DEP-CARRY in the open regime (lead, 2026-10-20): S with e >= EMIN, 3e < m, c > 4m.  Score =
min over phases (u = 1 and 2 random units) of (V + Dep)/m, and separately at the conductor phase (mode 'cond').
Usage: python depann2.py NR IT SEED MMIN MMAX EMIN [cond]"""
import sys, random, math
from math import gcd
sys.path.insert(0, '.')
from tile import build
from depforms import forms
COND = len(sys.argv) > 7 and sys.argv[7] == 'cond'
def value(m, G, rnd, EMIN):
    if m < 4 or any(g <= m for g in G): return None
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; e = len(gens) + 1
    if e < EMIN or 3 * e >= m or c <= 4 * m: return None
    D = list(M)
    if COND:
        V, dep, BD, RA = forms(m, D, [g % m for g in gens], (-c) % m); return ((V + dep) / m, 1, (-c) % m, V, dep, c, gens)
    best = None; us = [u for u in range(2, m) if gcd(u, m) == 1]
    for u in [1] + rnd.sample(us, min(2, len(us))):
        delta = [(u * g) % m for g in gens]
        for s in range(m):
            V, dep, BD, RA = forms(m, D, delta, s)
            if best is None or V + dep < best[0]: best = (V + dep, u, s, V, dep)
    return (best[0] / m,) + best[1:] + (c, gens)
NR, IT, SEED, MMIN, MMAX, EMIN = map(int, sys.argv[1:7]); rnd = random.Random(SEED); top = None
for rs in range(NR):
    for _ in range(2000):
        m = rnd.randint(MMIN, MMAX); k = rnd.randint(EMIN - 1, max(EMIN - 1, m // 3 - 2))
        G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 5]) * m + 2), k))
        v = value(m, G, rnd, EMIN)
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
        v2 = value(m, sorted(G), rnd, EMIN)
        if v2 is None: continue
        if v2[0] <= v[0] or rnd.random() < math.exp((v[0] - v2[0]) / T):
            cur, v = (m, v2[-1]), v2
            if top is None or v[0] < top:
                top = v[0]; print("best (V+Dep)/m %.4f u=%d s=%d V=%d Dep=%d m=%d c=%d e=%d gens=%s" % (v[0], v[1], v[2], v[3], v[4], m, v[5], len(v[6]) + 1, v[6]), flush=True)
        T = max(0.001, T * 0.995)
    if rs % 10 == 0: print("restart", rs, "best", top, flush=True)
