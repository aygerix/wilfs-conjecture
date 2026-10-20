r"""Annealer for S1 / DEP-CARRY on lex Apery tiles (lead, 2026-10-21). Score = min over phases s and units u (u = 1
plus 2 random units) of V + BD (S1) where V = s + sum kappa_s; DEP-CARRY uses Dep >= BD.  Minimizes the score
normalized by m (score < 0 refutes S1).  Usage: python depann.py NR IT SEED MMIN MMAX"""
import sys, random, math
from math import gcd
sys.path.insert(0, '.')
from tile import build
from depforms import forms
def value(m, G, rnd):
    if m < 4 or any(g <= m for g in G): return None
    R = build(m, G)
    if R is None: return None
    c, gens, M = R
    if len(gens) < 2: return None
    D = list(M); best = None
    us = [u for u in range(2, m) if gcd(u, m) == 1]
    for u in [1] + rnd.sample(us, min(2, len(us))):
        delta = [(u * g) % m for g in gens]
        for s in range(m):
            V, dep, BD, RA = forms(m, D, delta, s)
            sc = V + BD
            if best is None or sc < best[0]: best = (sc, u, s, V, dep, BD)
    return (best[0] / m,) + best + (c, gens)
NR, IT, SEED, MMIN, MMAX = map(int, sys.argv[1:6]); rnd = random.Random(SEED); top = None
for rs in range(NR):
    while True:
        m = rnd.randint(MMIN, MMAX); G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 5]) * m + 2), min(m, rnd.randint(2, 8))))
        v = value(m, G, rnd)
        if v is not None: break
    cur = (m, v[-1]); T = 0.05
    for it in range(IT):
        m, G = cur[0], list(cur[1]); r = rnd.random()
        if r < 0.45: i = rnd.randrange(len(G)); G[i] += rnd.choice([-2, -1, 1, 2, m, -m])
        elif r < 0.6 and len(G) > 2: G.pop(rnd.randrange(len(G)))
        elif r < 0.8: G.append(rnd.randint(m + 1, 4 * m))
        else: m += rnd.choice([-1, 1])
        if m < MMIN or m > MMAX: continue
        v2 = value(m, sorted(G), rnd)
        if v2 is None: continue
        if v2[0] <= v[0] or rnd.random() < math.exp((v[0] - v2[0]) / T):
            cur, v = (m, v2[-1]), v2
            if top is None or v[0] < top:
                top = v[0]; print("best S1/m %.4f score %d u=%d s=%d V=%d Dep=%d BD=%d m=%d c=%d gens=%s" % (v[0], v[1], v[2], v[3], v[4], v[5], v[6], m, v[7], v[8]), flush=True)
        T = max(0.001, T * 0.995)
    if rs % 10 == 0: print("restart", rs, "best", top, flush=True)
