"""Annealer for TILE-MAX-AFF on lex Apery tiles of random S (full tile, N = e-1 directions incl. right primitives)
(lead, 2026-10-21). For the tile M^ and every unit u mod m and shift s, eps(a) = (u * phi(a) + s) mod m (all such
eps are the affine mod-linear bijections compatible with the lattice). Value = max_{u,s} LHS / ((N+1) m(m-1)/2),
LHS = sum_{y in Max(M^)} (|y| + N) eps(y).  Value > 1 refutes TILE-MAX-AFF.  (u = 1, s = rho restricted to the
top window is TOPH, i.e. Wilf.)  Usage: python tilemax_ann.py NR IT SEED MMAX [MMIN]"""
import sys, random, math
from math import gcd
sys.path.insert(0, '.')
from tile import build
def value(m, G):
    if m < 3 or any(g <= m for g in G): return None
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; N = len(gens)
    if N < 2: return None
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(N))
    mx = [(sum(a) + N, x % m) for a, x in M.items() if all(up(a, i) not in M for i in range(N))]
    best = -1.0; arg = None; den = (N + 1) * m * (m - 1) / 2
    for u in range(1, m):
        if gcd(u, m) != 1: continue
        base = [(w, (u * r) % m) for w, r in mx]
        for s in range(m):
            v = sum(w * ((r + s) % m) for w, r in base) / den
            if v > best: best, arg = v, (u, s)
    return best, arg, c, gens, N, len(mx)
NR, IT, SEED, MMAX = map(int, sys.argv[1:5]); MMIN = int(sys.argv[5]) if len(sys.argv) > 5 else 4; rnd = random.Random(SEED); top = None
for rs in range(NR):
    while True:
        m = rnd.randint(MMIN, MMAX); G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 5]) * m + 2), min(m, rnd.randint(2, 7))))
        v = value(m, G)
        if v is not None: break
    cur = (m, v[3]); T = 0.05
    for it in range(IT):
        m, G = cur[0], list(cur[1]); r = rnd.random()
        if r < 0.45: i = rnd.randrange(len(G)); G[i] += rnd.choice([-2, -1, 1, 2, m, -m])
        elif r < 0.6 and len(G) > 2: G.pop(rnd.randrange(len(G)))
        elif r < 0.8: G.append(rnd.randint(m + 1, 4 * m))
        else: m += rnd.choice([-1, 1])
        if m < MMIN or m > MMAX: continue
        v2 = value(m, sorted(G))
        if v2 is None: continue
        if v2[0] >= v[0] or rnd.random() < math.exp((v2[0] - v[0]) / T):
            cur, v = (m, v2[3]), v2
            if top is None or v[0] > top:
                top = v[0]; print("best ratio %.5f u,s=%s m=%d c=%d N=%d #max=%d gens=%s" % (v[0], v[1], m, v[2], v[4], v[5], v[3]), flush=True)
        T = max(0.001, T * 0.995)
    if rs % 20 == 0: print("restart", rs, "best", top, flush=True)
