r"""HALL-TM on lex Apery tiles of numerical semigroups (lead, 2026-10-20). Tile M^ (N = e-1 directions incl. right
primitives), positions eps(a) = (u * phi(a)) mod m for a unit u (so eps(0) = 0; u = 1 is the m | c phase).
HALL-TM: for every set Y of maximal cells, sum_Y (|y|-1) eps(y) <= (N+1) sum_{z in down(Y) \ Y} eps(z).
lam* = max_Y demand/supply (exact via bisection on scaled max-flow); lam* > 1 refutes HALL-TM; Y = Max gives MaxCL.
Usage: python hallsg.py show m g1 ..  | python hallsg.py ann NR IT SEED MMIN MMAX"""
import sys, random, math
from math import gcd
sys.path.insert(0, '.')
from tile import build
from halltop import maxflow
def lamstar(N, mx, low, below, e, Q=4096):
    dem = {y: (sum(y) - 1) * e[y] for y in mx if sum(y) > 1}
    D = sum(dem.values())
    if D == 0: return 0.0
    idx = {a: i for i, a in enumerate(low)}; yi = {y: 2 + len(low) + j for j, y in enumerate(mx)}
    def feas(P):   # demands * P, supplies * Q
        edges = [(0, yi[y], dem[y] * P) for y in dem] + [(2 + idx[a], 1, (N + 1) * e[a] * Q) for a in low]
        edges += [(yi[y], 2 + idx[a], 1 << 50) for y in dem for a in below[y]]
        return maxflow(2 + len(low) + len(mx), edges, 0, 1) == D * P
    lo, hi = 0, 8 * Q   # largest feasible P is Q / lam*
    if feas(hi): return 0.125
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feas(mid): lo = mid
        else: hi = mid
    return Q / lo if lo else 99.0   # lam* in [Q/hi, Q/lo]
def value(m, G, units=None):
    if m < 3 or any(g <= m for g in G): return None
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; N = len(gens)
    if N < 2: return None
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(N))
    mx = [a for a in M if all(up(a, i) not in M for i in range(N))]
    low = [a for a in M if a not in set(mx) and any(a)]
    below = {y: [a for a in low if all(a[i] <= y[i] for i in range(N))] for y in mx}
    best = -1; arg = None
    for u in (units if units is not None else [u for u in range(1, m) if gcd(u, m) == 1]):
        e = {a: (u * x) % m for a, x in M.items()}
        l = lamstar(N, mx, low, below, e)
        if VERB: print("  u=%d lam*=%.4f" % (u, l))
        if l > best: best, arg = l, u
    return best, arg, c, gens, N, len(mx)
VERB = False
if __name__ == '__main__':
  if sys.argv[1] == 'show':
    VERB = True; a = list(map(int, sys.argv[2:])); print(value(a[0], a[1:]))
  else:
    NR, IT, SEED, MMIN, MMAX = map(int, sys.argv[2:7]); rnd = random.Random(SEED); top = None
    for rs in range(NR):
        while True:
            m = rnd.randint(MMIN, MMAX); G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 5]) * m + 2), min(m, rnd.randint(2, 7))))
            v = value(m, G, [1] + rnd.sample([u for u in range(2, m) if gcd(u, m) == 1], 2))
            if v is not None: break
        cur = (m, v[3]); T = 0.05
        for it in range(IT):
            m, G = cur[0], list(cur[1]); r = rnd.random()
            if r < 0.45: i = rnd.randrange(len(G)); G[i] += rnd.choice([-2, -1, 1, 2, m, -m])
            elif r < 0.6 and len(G) > 2: G.pop(rnd.randrange(len(G)))
            elif r < 0.8: G.append(rnd.randint(m + 1, 4 * m))
            else: m += rnd.choice([-1, 1])
            if m < MMIN or m > MMAX: continue
            us = [u for u in range(2, m) if gcd(u, m) == 1]
            v2 = value(m, sorted(G), [1] + rnd.sample(us, min(2, len(us))))
            if v2 is None: continue
            if v2[0] >= v[0] or rnd.random() < math.exp((v2[0] - v[0]) / T):
                cur, v = (m, v2[3]), v2
                if top is None or v[0] > top:
                    top = v[0]; print("best lam* %.4f u=%s m=%d c=%d N=%d #max=%d gens=%s" % (v[0], v[1], m, v[2], v[4], v[5], v[3]), flush=True)
            T = max(0.001, T * 0.995)
        if rs % 10 == 0: print("restart", rs, "best", top, flush=True)
