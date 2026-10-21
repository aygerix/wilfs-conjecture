r"""Search for case-B tiles (Dep < Sigma_supp, i.e. Sigma_A |y| > m - 1 + Q) of height >= HMIN (lead, 2026-10-20).
Anneal over residue sets delta (|delta| = d) with S = <m, m+delta_1, .., m+delta_d> (all generators in (m, 2m), so the
tile is close to the min-length representation tile), and also over lifts in (m, 3m) (LIFT=1).  Score = (Dep - Ssupp)/m.
Reports Tile-CL (min V) at both signs for every case-B hit.  Usage: python caseb.py NR IT SEED DMIN DMAX MMIN MMAX HMIN LIFT"""
import sys, random, math
sys.path.insert(0, '.')
from tile import build
from tcldich import stats
NR, IT, SEED, DMIN, DMAX, MMIN, MMAX, HMIN, LIFT = map(int, sys.argv[1:10]); rnd = random.Random(SEED); top = None; hits = 0
def value(m, R, K):
    G = sorted(set(x + k * m for x, k in zip(R, K)))
    if len(G) < 2 or any(x % m == 0 for x in G): return None
    B = build(m, G)
    if B is None: return None
    c, gens, M = B
    if len(gens) < DMIN: return None
    h = max(sum(x) for x in M)
    if h < HMIN: return None
    v, dep, ss = stats(m, list(M), [g % m for g in gens])
    return (dep - ss) / m, dep, ss, v, c, gens, h
for rs in range(NR):
    m = rnd.randint(MMIN, MMAX); d = rnd.randint(DMIN, DMAX)
    R = rnd.sample(range(1, m), d); K = [1 + (LIFT and rnd.random() < 0.3) for _ in R]
    v = value(m, R, K)
    if v is None: continue
    T = 0.05
    for it in range(IT):
        R2, K2, m2 = list(R), list(K), m; u = rnd.random()
        if u < 0.6: i = rnd.randrange(len(R2)); R2[i] = rnd.randrange(1, m2) if rnd.random() < 0.3 else (R2[i] + rnd.choice([-2, -1, 1, 2])) % m2
        elif u < 0.7 and LIFT: i = rnd.randrange(len(K2)); K2[i] = 3 - K2[i]
        elif u < 0.8 and len(R2) < DMAX: R2.append(rnd.randrange(1, m2)); K2.append(1)
        elif u < 0.9 and len(R2) > DMIN: i = rnd.randrange(len(R2)); R2.pop(i); K2.pop(i)
        else: m2 = max(MMIN, min(MMAX, m2 + rnd.choice([-1, 1]))); R2 = [x % m2 for x in R2]
        if any(x == 0 for x in R2): continue
        v2 = value(m2, R2, K2)
        if v2 is None: continue
        if v2[0] <= v[0] or rnd.random() < math.exp((v[0] - v2[0]) / T):
            R, K, m, v = R2, K2, m2, v2
            if v[1] < v[2]:
                hits += 1
                B = build(m, v[5]); vm = stats(m, list(B[2]), [(-g) % m for g in v[5]])[0]
                if hits <= 30 or v[3] < 0 or vm < 0: print("CASE-B h=%d m=%d e=%d c=%d Dep %d Ssupp %d minV %d minV(-delta) %d open %d gens %s" % (v[6], m, len(v[5]) + 1, v[4], v[1], v[2], v[3], vm, int(3 * (len(v[5]) + 1) < m and v[4] > 4 * m), v[5]), flush=True)
            if top is None or v[0] < top: top = v[0]; print("best (Dep-Ss)/m %.4f Dep %d Ss %d h %d m %d e %d gens %s" % (v[0], v[1], v[2], v[6], m, len(v[5]) + 1, v[5]), flush=True)
        T = max(0.001, T * 0.995)
    if rs % 20 == 0: print("restart", rs, "best", top, "hits", hits, flush=True)
