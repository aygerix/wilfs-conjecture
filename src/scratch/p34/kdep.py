r"""KAPPA-DEP (lead, 2026-10-21): for a lattice tile (D, delta),  sum_a sum_{a-cols C} S_a(|C|) <= M' + m Dep,
S_a(L) = sum_{k<L} <k delta_a>.  Slack (integer) = Dep - kappa0.  Implies DEP-CARRY at every phase (N >= 0).
Modes: one m g1..gk | ann NR IT SEED MMIN MMAX EMAX OPEN [HMIN MIRROR] | tiles4 MMIN MMAX (all 4-D down-sets, all delta)"""
import sys, random, math, itertools
sys.path.insert(0, '.')
def ds4(m):
    from subadd_lp import downsets
    D3 = {0: [frozenset()]}
    for k in range(1, m + 1): D3[k] = [frozenset(D) for D in downsets(3, k)]
    def chains(rem, prev):
        if rem == 0: yield []; return
        for k in range(1, rem + 1):
            for L in D3[k]:
                if prev is None or L <= prev:
                    for rest in chains(rem - k, L): yield [L] + rest
    for ch in chains(m, None): yield [(i,) + x for i, L in enumerate(ch) for x in L]
def kslack(m, D, delta):
    N = len(delta); Ds = set(D); up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    tot = 0; dep = 0
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    for a in range(N):
        da = delta[a]
        for x in D:
            if x[a] == 0:
                L = 0; y = x
                while y in Ds: L += 1; t = y; y = up(y, a)
                tot += sum((k * da) % m for k in range(L))
                if t not in mx: dep += L
    Mp = m * (m - 1) // 2
    assert (tot - Mp) % m == 0
    return dep - (tot - Mp) // m, dep
if __name__ == '__main__':
    from tile import build
    if sys.argv[1] == 'one':
        v = list(map(int, sys.argv[2:])); c, gens, M = build(v[0], v[1:])
        print("m=%d gens=%s c=%d: KAPPA-DEP slack, Dep =" % (v[0], gens, c), kslack(v[0], list(M), [g % v[0] for g in gens]))
    elif sys.argv[1] == 'ann':
        NR, IT, SEED, MMIN, MMAX, EMAX, OPEN = map(int, sys.argv[2:9]); rnd = random.Random(SEED); top = None
        HMIN = int(sys.argv[9]) if len(sys.argv) > 9 else 0; MIRROR = int(sys.argv[10]) if len(sys.argv) > 10 else 0
        def value(m, G):
            if m < 4 or any(g <= m for g in G): return None
            R = build(m, G)
            if R is None: return None
            c, gens, M = R; d = len(gens)
            if d < 2 or d + 1 > EMAX or (OPEN and (3 * (d + 1) >= m or c <= 4 * m)): return None
            if max(sum(x) for x in M) < HMIN: return None
            sl, dep = kslack(m, list(M), [g % m for g in gens])
            if MIRROR: sl = min(sl, kslack(m, list(M), [(-g) % m for g in gens])[0])
            return sl / m, sl, dep, c, gens
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
                        top = v[0]; print("best KDEP/m %.4f slack %d Dep %d m=%d c=%d e=%d gens=%s" % (v[0], v[1], v[2], m, v[3], len(v[4]) + 1, v[4]), flush=True)
                T = max(0.001, T * 0.995)
            if rs % 20 == 0: print("restart", rs, "best", top, flush=True)
    else:
        MMIN, MMAX = map(int, sys.argv[2:4])
        for m in range(MMIN, MMAX + 1):
            nt = fl = 0; worst = None; neq = 0
            for D in ds4(m):
                if any(all(x[b] == 0 for x in D) for b in range(4)): continue
                for b in itertools.product(range(1, m), repeat=4):
                    if len({sum(x * y for x, y in zip(a, b)) % m for a in D}) != m: continue
                    nt += 1; sl, dep = kslack(m, D, list(b))
                    fl += sl < 0; neq += sl == 0
                    if worst is None or sl < worst[0]: worst = (sl, dep, sorted(D), b)
            print("d=4 m=%d tiles %d fails %d equality %d worst %s" % (m, nt, fl, neq, worst), flush=True)
