"""[UCG is FALSE (two-generated S, the m=16 tile): G is needed. Mode GDB (append GDB): certificate W(r := max(R_gen, 1)) + 1 > 0 for r >= 1.]
Gate for Conjecture UCG (every S with c > 4m):
     sum_{y in Y} (|y| - 1) <= R* (k - q) + P~,   R* = max(R_gen, min(r, 1)),
which implies Wilf via the ray identity W = rho r/m + G + P~ - Lam + r(k - q) (PROOFS "Ray identity ...").
For r = 0 it reads: sum_Y(|y|-1) <= P~.  Fast evaluation + simulated annealing minimizing the slack.
Usage: python ucg.py anneal NRESTART ITERS SEED MMAX | python ucg.py eval m g1 ... c"""
import sys, random, math
from fractions import Fraction as Fr
def slack(m, G, c):
    n = len(G); T = c + m
    if c <= 4 * m or any(g <= m or g >= c or g % m == 0 for g in G) or len(set(G)) != n: return None
    S = bytearray(T); S[0] = 1
    for x in range(1, T):
        if (x >= m and S[x - m]) or any(g <= x and S[x - g] for g in G): S[x] = 1
    if S[c - 1]: return None
    for g in G:   # minimality
        if any(h < g and S[g - h] for h in [m] + G if h != g): return None
    fac = {0: (0,) * n}
    for x in range(1, T):
        if not S[x] or (x >= m and S[x - m]): continue
        best = None
        for i, g in enumerate(G):
            if g <= x and (x - g) in fac:
                a = list(fac[x - g]); a[i] += 1; a = tuple(a)
                if best is None or a[::-1] < best[::-1]: best = a
        fac[x] = best
    M = {a: x for x, a in fac.items()}
    q = -(-c // m); d = len(M); r = m - d
    k = sum(-(-(c - x) // m) for x in M.values() if x < c)
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(n))
    dn = lambda a, i: tuple(a[t] - (t == i) for t in range(n))
    I = {a for a in M if all(up(a, i) in M for i in range(n))}
    Rgen = sum(sum(1 for i in range(n) if a[i] >= 1 and dn(a, i) in I) - 1 for a in M if a not in I)
    Pt = Fr(0); Yt = 0
    for a, x in M.items():
        if x < c:
            for i in range(n):
                if up(a, i) not in M: Pt += Fr((a[i] + 1) * (c - x), m)
        else: Yt += sum(a) - 1
    Rs = max(Rgen, min(r, 1))
    W = (n + 1 + r) * k - c
    if MODE == 'GDB':
        if r == 0 or n < 2: return None
        rho = q * m - c; ell = n + 1
        Gn = ell * sum(Fr(-(-(c - x) // m)) - Fr(c - x, m) for x in M.values() if x < c)
        Lam = sum(Fr((sum(a) - 1) * (x - c), m) for a, x in M.items() if x >= c)
        return Fr(rho * Rs, m) + Gn + Pt - Lam + Rs * (k - q) + 1, r, Rgen, k - q, Pt, Yt, W   # >= 0 <=> certificate > -1
    if MODE in ('TOP', 'TOP0', 'TOPP'):   # TOP: Lam <= G (ceiling gains alone pay the top loss); TOP0: only r = 0
        if n < 2 or (MODE == 'TOP0' and r > 0) or (MODE == 'TOPP' and Pt == 0): return None
        ell = n + 1
        Gn = ell * sum(Fr((x - c) % m, m) for x in M.values() if x < c)
        Lam = sum(Fr((sum(a) - 1) * (x - c), m) for a, x in M.items() if x >= c)
        return Gn - Lam, r, Rgen, k - q, Pt, Yt, W
    if MODE == 'TOPH':   # TOP-hat on the full tile: sum_{Ap >= c} (deg + N) h <= (N+1) m(m-1)/2, N = n + r; slack / m
        if n < 1: return None
        N = n + r; cov = {x % m for x in M.values()}
        top = sum((sum(a) + N) * (x - c) for a, x in M.items() if x >= c)
        top += (N + 1) * sum((u - c) % m for u in range(m) if u not in cov)
        return Fr((N + 1) * m * (m - 1) // 2 - top, m), r, Rgen, k - q, Pt, Yt, W
    if MODE == 'GT':   # GT: Lam <= G + max(R_gen, 0)(k - q)
        if n < 2: return None
        ell = n + 1
        Gn = ell * sum(Fr((x - c) % m, m) for x in M.values() if x < c)
        Lam = sum(Fr((sum(a) - 1) * (x - c), m) for a, x in M.items() if x >= c)
        return Gn + max(Rgen, 0) * (k - q) - Lam, r, Rgen, k - q, Pt, Yt, W
    return Rs * (k - q) + Pt - Yt, r, Rgen, k - q, Pt, Yt, W
def anneal(NR, IT, SEED, MMAX):
    rnd = random.Random(SEED); best = None
    for rs in range(NR):
        while True:
            m = rnd.randint(6, MMAX); n = rnd.randint(1, 6); c = rnd.randint(4 * m + 1, 9 * m)
            hi = rnd.choice([2 * m, 3 * m, c])
            if min(hi, c) - m - 1 < n: continue
            G = sorted(rnd.sample(range(m + 1, min(hi, c)), n)); v = slack(m, G, c)
            if v is not None: break
        cur = (m, G, c); T = 3.0
        for it in range(IT):
            m, G, c = cur[0], list(cur[1]), cur[2]; u = rnd.random()
            if u < 0.4 and G: i = rnd.randrange(len(G)); G[i] += rnd.choice([-3, -2, -1, 1, 2, 3])
            elif u < 0.5 and len(G) > 1: G.pop(rnd.randrange(len(G)))
            elif u < 0.6 and len(G) < 8: G.append(rnd.randint(m + 1, c - 1))
            elif u < 0.8: c += rnd.choice([-3, -2, -1, 1, 2, 3, m, -m])
            else: m += rnd.choice([-2, -1, 1, 2])
            if m < 5 or m > MMAX or c > 12 * m: continue
            G = sorted(G); v2 = slack(m, G, c)
            if v2 is None: continue
            if v2[0] <= v[0] or rnd.random() < math.exp(float(v[0] - v2[0]) / T):
                cur, v = (m, G, c), v2
                if best is None or v[0] < best[0][0]:
                    best = (v, cur); print("best slack %.3f r=%d Rgen=%d k-q=%d P=%.2f Ytot=%d W=%d at m=%d G=%s c=%d" % ((float(v[0]),) + v[1:4] + (float(v[4]),) + v[5:] + cur), flush=True)
            T = max(0.05, T * 0.998)
        if rs % 10 == 0: print("restart", rs, "best", float(best[0][0]) if best else None, flush=True)
MODE = 'UCG'
if len(sys.argv) > 1 and sys.argv[-1] in ('GDB', 'TOP', 'TOP0', 'TOPP', 'GT', 'TOPH'): MODE = sys.argv.pop()
if sys.argv[1] == 'eval':
    v = list(map(int, sys.argv[2:])); print(slack(v[0], v[1:-1], v[-1]))
else:
    anneal(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
