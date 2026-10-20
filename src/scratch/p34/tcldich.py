r"""TCL-DICHOTOMY (lead, 2026-10-21): if Dep < Sigma_supp := sum_x (|supp x| - 1)^+ then Tile-CL holds (min_sigma V >= 0).
Together with the trivial V = N - kappa0 >= -kappa0 >= -Sigma_supp this gives DEP-ALL.  Modes:
 'list m g..' | 'rnd NS SEED MMIN MMAX' | 'ann NR IT SEED MMIN MMAX DMIN EMAX OPEN MIRROR' (minimize min V over tiles with
 Dep < Sigma_supp; MIRROR=1 also scores (D, -delta))."""
import sys, random, math
sys.path.insert(0, '.')
from tile import build
def stats(m, D, delta):
    N = len(delta); Ds = set(D); up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    om = {x: 0 for x in D}
    for b in range(N):
        for x in D:
            if up(x, b) not in Ds: om[x] += x[b] + 1
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    dep = sum(v for x, v in om.items() if x not in mx)
    ss = sum(max(0, sum(1 for t in x if t) - 1) for x in D)
    wt = [0] * m
    for x in D: wt[sum(p * q for p, q in zip(x, delta)) % m] += om[x]
    Mp = m * (m - 1) // 2
    vmin = min((Mp - (sum(wt[l] * ((l + rho) % m) for l in range(m)) - N * Mp)) // m for rho in range(m))
    return vmin, dep, ss
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'list':
        v = list(map(int, sys.argv[2:])); c, gens, M = build(v[0], v[1:]); m = v[0]
        for sg in (1, -1): print(gens, 'sign', sg, '(minV, Dep, Sigma_supp) =', stats(m, list(M), [(sg * g) % m for g in gens]))
    elif mode == 'rnd':
        NS, SEED, MMIN, MMAX = map(int, sys.argv[2:6]); rnd = random.Random(SEED); cnt = 0; st = [0, 0, 0, 0]; bad = []
        while cnt < NS:
            m = rnd.randint(MMIN, MMAX); c0 = rnd.randint(m + 1, 9 * m)
            G = sorted(rnd.sample(range(m + 1, c0 + m), rnd.randint(2, min(14, c0 - 2))))
            R = build(m, G)
            if R is None: continue
            c, gens, M = R
            if len(gens) < 2: continue
            cnt += 1
            for sg in (1, -1):
                v, dep, ss = stats(m, list(M), [(sg * g) % m for g in gens])
                caseB = dep < ss; st[0] += caseB; st[1] += (not caseB)
                if v < 0: st[2 + caseB] += 1
                if v < 0 and caseB: bad.append((v, dep, ss, m, gens, sg))
        print("tiles (both signs) %d: caseB (Dep < Ssupp) %d, caseA %d; Tile-CL fails in caseA %d, in caseB %d; ex %s" % (2 * cnt, st[0], st[1], st[2], st[3], bad[:3]))
    else:
        NR, IT, SEED, MMIN, MMAX, DMIN, EMAX, OPEN, MIR = map(int, sys.argv[2:11]); rnd = random.Random(SEED); top = None
        def value(m, G):
            if m < 4 or any(g <= m for g in G): return None
            R = build(m, G)
            if R is None: return None
            c, gens, M = R; d = len(gens)
            if d < DMIN or d + 1 > EMAX or (OPEN and (3 * (d + 1) >= m or c <= 4 * m)): return None
            best = None
            for sg in ((1, -1) if MIR else (1,)):
                v, dep, ss = stats(m, list(M), [(sg * g) % m for g in gens])
                if dep >= ss: continue
                sc = v / m + 0.5 * (dep / ss)     # prefer small Dep/Ssupp too
                if best is None or sc < best[0]: best = (sc, v, dep, ss, sg)
            if best is None: return None
            return best + (c, gens)
        for rs in range(NR):
            v = None
            for _ in range(3000):
                m = rnd.randint(MMIN, MMAX); k = rnd.randint(DMIN, max(DMIN, min(EMAX - 1, (m // 3 - 2) if OPEN else m - 1)))
                G = sorted(rnd.sample(range(m + 1, rnd.choice([2, 3, 5]) * m + 2), min(k, m)))
                v = value(m, G)
                if v is not None: break
            if v is None: continue
            cur = (m, v[-1]); T = 0.05; topv = None
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
                    if top is None or v[1] < top:
                        top = v[1]; print("best minV %d Dep %d Ssupp %d sign %d m=%d c=%d e=%d gens=%s" % (v[1], v[2], v[3], v[4], m, v[5], len(v[6]) + 1, v[6]), flush=True)
                T = max(0.001, T * 0.995)
            if rs % 20 == 0: print("restart", rs, "best", top, flush=True)
