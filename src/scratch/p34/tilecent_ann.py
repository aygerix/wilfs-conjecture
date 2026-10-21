"""Annealer for TILE-CENTROID on NON-minimal down-set tiles (lead, 2026-10-20).
Take the lex Apery tile M' of S' = <m, gens'> (N = e'-1 directions). For a unit u mod m and lifts k_i >= 1,
gamma_i = (u*gens'_i mod m) + k_i*m gives the same lattice L, so M' is a down-set tile of L_gamma (usually NOT
phi_gamma-minimal). Slack := N max phi - (N-1)(m-1)/2 - (N+1) mean phi  (= W(S') when u = 1, k_i = floor(gens'_i/m)).
Usage: python tilecent_ann.py NR IT SEED MMAX [MMIN]"""
import sys, random, math
sys.path.insert(0, '.')
from tile import build
from math import gcd
def slack(m, G, u, ks):
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; N = len(gens)
    if N < 2 or gcd(u, m) != 1: return None
    ks = (ks + [1] * N)[:N]
    gam = [(u * g) % m + max(1, k) * m for g, k in zip(gens, ks)]
    vals = [sum(g * a for g, a in zip(gam, p)) for p in M]
    assert len(set(v % m for v in vals)) == m
    sl = N * max(vals) - (N - 1) * (m - 1) / 2 - (N + 1) * sum(vals) / m
    return sl, gens, gam, c
NR, IT, SEED, MMAX = map(int, sys.argv[1:5]); MMIN = int(sys.argv[5]) if len(sys.argv) > 5 else 4; rnd = random.Random(SEED); best = None
for rs in range(NR):
    while True:
        m = rnd.randint(max(5, MMIN), MMAX); G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 5]) * m + 2), rnd.randint(2, 6)))
        u = rnd.choice([x for x in range(1, m) if gcd(x, m) == 1]); ks = [rnd.randint(1, 4) for _ in G]
        v = slack(m, G, u, ks)
        if v is not None: break
    cur = (m, v[1], u, ks); T = 2.0
    for it in range(IT):
        m, G, u, ks = cur[0], list(cur[1]), cur[2], list(cur[3]); r = rnd.random()
        if r < 0.3: i = rnd.randrange(len(G)); G[i] += rnd.choice([-2, -1, 1, 2, m, -m])
        elif r < 0.4 and len(G) > 2: G.pop(rnd.randrange(len(G)))
        elif r < 0.5: G.append(rnd.randint(m + 1, 4 * m)); ks.append(rnd.randint(1, 4))
        elif r < 0.65: u = rnd.randrange(1, m)
        elif r < 0.85 and ks: i = rnd.randrange(len(ks)); ks[i] = max(1, ks[i] + rnd.choice([-1, 1]))
        else: m += rnd.choice([-1, 1])
        if m < MMIN or m > MMAX or any(g <= m for g in G): continue
        v2 = slack(m, sorted(G), u, ks)
        if v2 is None: continue
        f1, f2 = v[0] / m, v2[0] / m
        if f2 <= f1 or rnd.random() < math.exp((f1 - f2) / T):
            cur, v = (m, v2[1], u, ks), v2
            if best is None or f2 < best:
                best = f2; print("best slack/m=%.4f slack=%.3f m=%d gens'=%s u=%d gamma=%s c'=%d" % (f2, v[0], m, v[1], u, v[2], v[3]), flush=True)
        T = max(0.01, T * 0.995)
    if rs % 20 == 0: print("restart", rs, "best", best, flush=True)
