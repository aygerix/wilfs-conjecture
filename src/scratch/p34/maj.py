"""MAJ(v) test (lead, 2026-10-21). For the lex tile Mhat (N = e-1 directions) and 1 <= v <= m:
   MAJ(v):  sum_{z in Mhat, phi(z) > c+m-1-v} (|z| + N)  <=  (N-1) v + m.
MAJ(v) for all v implies CH' (Wilf) by a Hall/layer-cake argument. Also reports the exact deficit form
   D := sum_{v=1}^m [cnt_v - (N-1)v - m]_+  vs  slack beyond m of early ends  E := sum_early (delta - m).
Usage: python maj.py rnd NS SEED MMAX DMIN | python maj.py ann NR IT SEED MMAX DMIN"""
import sys, random, math
sys.path.insert(0, '.')
from tile import build
def maj(m, G, DMIN):
    if m < 3 or any(g <= m for g in G): return None
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; N = len(gens)
    if N < 2 or c <= DMIN * m: return None
    F = c - 1; up = lambda a, i: tuple(a[t] + (t == i) for t in range(N))
    cnt = [0] * (m + 1); early = 0
    for a, x in M.items():
        dl = F + m - x
        for i in range(N):
            if up(a, i) not in M:
                if dl < m:
                    for v in range(dl + 1, m + 1): cnt[v] += a[i] + 1
                else: early += (a[i] + 1) * (dl - m)
    worst = min((N - 1) * v + m - cnt[v] for v in range(1, m + 1))
    D = sum(max(0, cnt[v] - (N - 1) * v - m) for v in range(1, m + 1))
    return worst, D, early, c, gens
if __name__ == '__main__':
    if sys.argv[1] == 'rnd':
        NS, SEED, MMAX, DMIN = map(int, sys.argv[2:6]); rnd = random.Random(SEED); nb = fail = 0; mn = None
        for _ in range(NS):
            m = rnd.randint(4, MMAX); G = [rnd.randint(m + 1, rnd.choice([2, 3, 5, 8]) * m + 1) for _ in range(rnd.randint(2, 7))]
            v = maj(m, G, DMIN)
            if v is None: continue
            nb += 1
            if v[0] < 0:
                fail += 1
                if fail <= 5: print("MAJ FAIL m=%d c=%d gens=%s worst=%d D=%d early=%d" % (m, v[3], v[4], v[0], v[1], v[2]), flush=True)
            if mn is None or v[0] < mn[0]: mn = (v[0], m) + v[1:]
        print("tested", nb, "MAJ failures", fail, "min slack", mn)
    else:
        NR, IT, SEED, MMAX, DMIN = map(int, sys.argv[2:7]); rnd = random.Random(SEED); best = None
        for rs in range(NR):
            while True:
                m = rnd.randint(4, MMAX); G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 5]) * m + 2), rnd.randint(2, 6)))
                v = maj(m, G, DMIN)
                if v is not None: break
            cur = (m, v[4]); T = 2.0
            for it in range(IT):
                m, G = cur[0], list(cur[1]); u = rnd.random()
                if u < 0.5: i = rnd.randrange(len(G)); G[i] += rnd.choice([-2, -1, 1, 2, m, -m])
                elif u < 0.6 and len(G) > 2: G.pop(rnd.randrange(len(G)))
                elif u < 0.75: G.append(rnd.randint(m + 1, 4 * m))
                else: m += rnd.choice([-1, 1])
                if m < 3 or m > MMAX: continue
                v2 = maj(m, G, DMIN)
                if v2 is None: continue
                f1, f2 = v[0] / m, v2[0] / m
                if f2 <= f1 or rnd.random() < math.exp((f1 - f2) / T):
                    cur, v = (m, v2[4]), v2
                    if best is None or f2 < best:
                        best = f2; print("best MAJslack/m=%.3f slack=%d D=%d early=%d m=%d c=%d gens=%s" % (f2, v[0], v[1], v[2], m, v[3], v[4]), flush=True)
                T = max(0.01, T * 0.995)
            if rs % 20 == 0: print("restart", rs, "best", best, flush=True)
